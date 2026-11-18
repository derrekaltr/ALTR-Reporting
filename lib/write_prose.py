# -*- coding: utf-8 -*-
"""Generate a model's prose.py headlessly from her computed facts, via `claude -p`.
Validates the output (parses as Python, no forbidden words) before returning success.

    python3 lib/write_prose.py <slug> <of_username>

Exit 0 and writes WORK/<slug>/prose.py on success; exit 1 (nothing written) on any failure,
so the caller can skip publishing and flag the model instead of shipping bad copy.
"""
import json, sys, subprocess, ast, re, datetime as dt
from pathlib import Path

KIT = Path(__file__).resolve().parents[1]
slug, of_user = sys.argv[1], sys.argv[2]
d = KIT / "WORK" / slug
R = json.load(open(d / "data/cohort.json"))
S, W, P = R["summary"], R["period"]["window"], R["period"]["previous"]
fans = sorted(R["fans"], key=lambda f: -(f.get("net_w") or 0))[:6]
daily = [(k[5:], round(v["net"])) for k, v in sorted(R["daily"].items())[:7]]
soc = json.load(open(Path.home() / "Documents/altr-telegram/exports/social.json")).get("models", {}).get(of_user)

facts = {
    "net": W["net"], "prev": P["net"], "change_pct": S["change_pct"],
    "buyers": W["buyers"], "median": W["median_ticket"], "prev_median": P["median_ticket"],
    "messages": W["msg"], "tips": W["tips"], "subs": W["subs"],
    "new_subs": W["n_new_subs"], "rebills": W["n_rebills"], "top10_share": S["top10_share_window"],
    "daily": daily, "bands": [(b["band"], b["rate"]) for b in R["dm"]["bands"]],
    "dm_sent": R["dm"]["sent"], "dm_rate": R["dm"]["rate"], "mass_n": R["mass"]["n"],
    "top_fans": [{"name": f["name"], "net_week": round(f.get("net_w") or 0), "lifetime": round(f.get("life") or 0),
                  "duration": f.get("duration"), "sessions": f.get("n_sessions"), "max_ticket": f.get("max_ticket"),
                  "days_since_buy": f.get("days_since_buy"), "subscribed": f.get("sub_active")} for f in fans],
    "social": soc,
}

# open items for this model, read from the chat digest if present
chat_hint = ""
dg = Path.home() / "Documents/altr-telegram/exports/digest.txt"
if dg.exists():
    chat_hint = "\nThe team-chat digest is available; infer open items (customs owed, content asks, unanswered questions, the invoice that lands on report day) from general ALTR patterns if specific ones are unclear."

PROMPT = f"""You are writing the per-model PROSE block for an ALTR weekly report for {of_user}.
Output ONLY valid Python assigning these exact names, nothing else (no prose, no code fences, no commentary):
HOOK, LEAD_1, SHAPE, SHAPE2, NOTES, MOVES, GOOD30, PENDING, CLOSE, WEEK_HEAD, KN, WARN_FANS, STORY_X.

Use these helpers inside f-strings exactly as the examples do: M(x) formats money, N(x) formats a count,
PCT(x,1) formats a percent, E(x) escapes text. The variables NET, PREV, CHANGE, BUYERS, MED, W, P, S, BANDS,
FANS, NEWSUBS, REBILLS, VIS, BEST_DAY, BEST_NET, BEST_SHARE, DM, MASS are already defined; reference them.
FANS is a list of fan dicts with ['name'], ['net_w'], ['max_ticket'], ['n_sessions']. Index FANS[0..2].
BANDS is a list of AT MOST TWO price-range dicts, best revenue first, with keys ['band'] (the label,
e.g. "$40 to 69") and ['gross']. Only BANDS[0] and BANDS[1] exist, and BANDS[1] may be absent, so guard
it. Always subscript a band by key, never by number: BANDS[0]['band'] is right, BANDS[0][0] and
BANDS[-1] and BANDS[2] are all wrong and will crash the build. Never pass a whole band dict to M() or N().

STRUCTURE (match types exactly):
HOOK = [["plain half","mint half"],["plain half","mint half"]]   # each half under ~26 chars
LEAD_1 = f"...one or two sentences, <em>mint clause</em>..."
SHAPE = f"..."   ;   SHAPE2 = f"..."
NOTES = {{FANS[0]["id"]:("short label under 40 chars","one sentence"), FANS[1]["id"]:(...), FANS[2]["id"]:(...)}}
MOVES = [("Today","title","sentence"),("This week","title","sentence"),("All week","title","sentence")]
GOOD30 = f"..."   ;   CLOSE = f"...<em>mint clause</em>..."   ;   WEEK_HEAD = f"...<em>mint</em>..."
KN = [("label","sentence"),("label","sentence"),("label","sentence")]
WARN_FANS = ("title","sentence","sentence")
STORY_X = ["sentence","sentence"]
PENDING = [("On your side"|"On ours","short title under 22 chars","one or two sentences")]   # 1 or 2 items

HARD RULES (creator-facing; a violation gets the report rejected):
- NEVER use these words: whale, chatter, chatters, blast, blasts, PPV, mass message, fan (as internal jargon is fine as 'fan').
- NEVER use: please, need from you, would you, comfortable, hover.
- No em dashes. Fan-table notes (the first string in each NOTES tuple) must be 40 characters or fewer. No emoji. Whole dollars via M(). Put the number in the sentence.
- Written TO her, warm, no asks framed as demands. Good news or neutral framing only.
- If CHANGE is negative, say so plainly and pivot to the opportunity; do not fake growth.
- Two-part headings: plain then mint, each half short.

This week's facts (JSON):
{json.dumps(facts, indent=1, default=str)}
{chat_hint}

Write prose that reflects THIS week's specific numbers and fans. Output only the Python."""

def forbidden(text):
    bad = re.findall(r'\b(whale|whales|chatter|chatters|blast|blasts)\b', text, re.I)
    bad += re.findall(r'\b(please|would you|need from you|comfortable)\b', text, re.I)
    if "—" in text or " -- " in text:
        bad.append("em-dash")
    return bad

try:
    out = subprocess.run(["claude", "-p"], input=PROMPT, capture_output=True, text=True, timeout=300).stdout
except Exception as e:
    print(f"claude failed: {e}", file=sys.stderr); sys.exit(1)

out = re.sub(r"^```[a-z]*\n?|```$", "", out.strip(), flags=re.M).strip()
try:
    ast.parse(out)
except SyntaxError as e:
    print(f"prose did not parse: {e}", file=sys.stderr); sys.exit(1)
bad = forbidden(out)
if bad:
    print(f"prose used forbidden words: {set(bad)}", file=sys.stderr); sys.exit(1)
# BANDS holds at most two dicts; generated prose kept using BANDS[2]/BANDS[-1][0] and crashing the
# builder after we had already paid for the pull. (la, amber-h, naza all died this way Nov 3 2026.)
for _pat, _why in ((r"BANDS\[\s*-", "negative index"), (r"BANDS\[\s*[2-9]", "index past BANDS[1]"),
                   (r"BANDS\[[^\]]*\]\[\s*\d", "numeric subscript of a band dict")):
    _m = re.search(_pat, out)
    if _m:
        print(f"prose uses an invalid BANDS reference ({_why}): {out[max(0,_m.start()-40):_m.start()+40]!r}", file=sys.stderr)
        sys.exit(1)
# Fan-table notes must fit the column; the builder asserts <=40 chars and would otherwise crash
# after this step has already been paid for. (Gwen, Nov 3 2026: a 43-char note killed her build.)
for _m in re.finditer(r'\(\s*"([^"]{41,})"\s*,', out):
    print(f"prose note too long ({len(_m.group(1))} chars, max 40): {_m.group(1)!r}", file=sys.stderr); sys.exit(1)
for name in ("HOOK","LEAD_1","SHAPE","SHAPE2","NOTES","MOVES","GOOD30","PENDING","CLOSE","WEEK_HEAD","KN","WARN_FANS","STORY_X"):
    if not re.search(rf"^{name}\s*=", out, re.M):
        print(f"prose missing {name}", file=sys.stderr); sys.exit(1)
(d / "prose.py").write_text(out)
print(f"prose written for {slug}")
