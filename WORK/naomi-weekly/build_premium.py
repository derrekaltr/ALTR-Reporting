# -*- coding: utf-8 -*-
"""Liza Kovalenko. Weekly report, creator-facing. Built October 15, 2026.

ALTR WEEKLY TEMPLATE, pilot. Every number is read from data/ (cohort.json, visitors7.json).
The prose that changes per model sits in the PROSE block below; everything else is computed.
Run:  python3 build_premium.py && python3 ../../lib/build.py   then read qa/*.png, then ./deploy.sh
"""
import os, sys, json, datetime as dt
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join("..", "..", "lib"))
from premium import *
from holidays import next_occasion
OCCASION = next_occasion()

# ------------------------------------------------------------------ facts, all from data/
NAME = "Naomi"; FIRST = NAME.split()[0]; HANDLE = "@bindilondon.vip"
DATE = "November 15, 2026"
PDF = "ALTR-naomi-weekly-nov15.pdf"; PDF_DL = f"{FIRST}-Weekly-Report-ALTR.pdf"
TITLE = f"{FIRST}. Weekly report by ALTR"

R = json.load(open("data/cohort.json", encoding="utf-8"))
W, P, S = R["period"]["window"], R["period"]["previous"], R["summary"]
NET, PREV, CHANGE = W["net"], P["net"], S["change_pct"]
CHANGE = CHANGE if CHANGE is not None else 0.0
CH_SIGN = "+" if CHANGE >= 0 else "-"
CH_STR = f"{CH_SIGN}{abs(CHANGE):.1f}%"
CH_VERB = "rose" if CHANGE >= 0 else "eased"
CH_DIR = "up" if CHANGE >= 0 else "down"
NEW_ACCT = (PREV == 0)
BUYERS, MED = W["buyers"], W["median_ticket"]
NEWSUBS, REBILLS = W["n_new_subs"], W["n_rebills"]
MASS, DM = R["mass"], R["dm"]

days = sorted(R["daily"].items())[:7]                      # seven full days; the pull day is partial
DAILY = [(dt.date.fromisoformat(d).strftime("%a %-d"), round(v["net"])) for d, v in days]
BEST_I = max(range(len(DAILY)), key=lambda i: DAILY[i][1])
BEST_DAY, BEST_NET = dt.date.fromisoformat(days[BEST_I][0]).strftime("%A %B %-d"), DAILY[BEST_I][1]
BEST_SHARE = BEST_NET / NET * 100
# The reporting window, written out. This used to be a literal October date range in four
# places, left over from the first report, so every later report named the wrong week. (Nov 15 2026.)
_w0, _w1 = dt.date.fromisoformat(days[0][0]), dt.date.fromisoformat(days[-1][0])
WINDOW = (f"{_w0.strftime('%B %-d')} to {_w1.day}" if _w0.month == _w1.month
          else f"{_w0.strftime('%B %-d')} to {_w1.strftime('%B %-d')}")
WEEK_OF = _w0.strftime('%B %-d')

FANS = sorted(R["fans"], key=lambda f: -(f.get("net_w") or 0))[:8]
for f in FANS:
    f["net_w"] = round(f["net_w"])
    if not any(c.isalnum() for c in (f.get("name") or "")):
        f["name"] = f.get("user") or f"Fan {f['id']}"
NFANS = len([f for f in FANS if f.get("net_w")])
while len(FANS) < 3:
    FANS.append({"id": -len(FANS), "name": "", "net_w": 0, "max_ticket": 0, "n_sessions": 0,
                 "days_since_buy": None, "duration": None, "sub_active": False, "user": ""})
TOP5 = round(sum(f["net_w"] for f in FANS[:5])); TOP5_SHARE = (TOP5 / NET * 100) if NET else 0
# High-spender nurture trigger: a fan over $5,000 in the week gets a real-connection plan.
NURTURE = None
if FANS and (FANS[0].get("net_w") or 0) >= 5000:
    _nf = FANS[0]
    NURTURE = {"name": _nf["name"], "amount": round(_nf["net_w"]),
               "body": (f"{E(_nf['name'])} spent {M(_nf['net_w'])} with you this week, more than anyone else. "
                        f"A supporter at this level stays when the connection feels real and personal. The things that keep him close: "
                        f"a voice note that uses his name, a reply that remembers what he told you last time, and a short personal video just for him. "
                        f"Those land harder than any new set. The team keeps his daily messages personal and in your voice, and one quick custom this week would mean a lot to him."),
               "short": f"{E(_nf['name'])} spent {M(_nf['net_w'])} this week, more than anyone. Keep him close with voice notes that use his name, replies that remember his details, and a short personal video. Real and personal is what keeps a supporter like this."}

VIS = json.load(open("data/visitors7.json", encoding="utf-8"))["data"]["topCountries"]["totals"]["total"]

# net by type (from the daily series) and gross, for the Where it came from page
rest = max(0, round(NET - W["msg"] - W["subs"] - W["tips"]))
TYPES = [("Messages", round(W["msg"])), ("Subs", round(W["subs"])), ("Tips", round(W["tips"])),
         ("Posts", rest), ("Streams", 0)]
MSG_SHARE = round(TYPES[0][1] / NET * 100)
GROSS = round(NET / 0.8)
DAYNAMES = [dt.date.fromisoformat(d).strftime("%b %-d") for d, _ in days]
TYPE_LINE = f"Messages {M(TYPES[0][1])}, subscriptions {M(TYPES[1][1])}, tips {M(TYPES[2][1])}, posts {M(TYPES[3][1])}, streams {M(TYPES[4][1])}."
HOWTO = ("Figures are platform-reported net, after the platform fee, as the OnlyFans statistics report them. "
         "They are here to show the shape of the week; your ALTR statement remains the official record.")

# RemoveLabs DMCA numbers (pulled from the WhatsApp group by ~/Documents/altr-telegram/removelabs.py)
RL_PATH = os.path.expanduser("~/Documents/altr-telegram/exports/removelabs.json")
PROT, RL_DATE = None, ""
if os.path.exists(RL_PATH):
    RL = json.load(open(RL_PATH, encoding="utf-8"))
    rl_name = next((k for k, v in RL["of_aliases"].items() if v == HANDLE.lstrip("@")), None)
    PROT, RL_DATE = RL["models"].get(rl_name), RL["created"]
# The vendor report sometimes carries the totals with no per-site breakdown. Keep the chapter
# (the totals are real) but drop the "where it was stolen from" table instead of crashing.
PROT_SITES = bool(PROT and PROT.get("top"))
# The vendor lists ten sites; only five fit the page, and the tail is a long thin tail anyway.
PROT_TOP = (PROT.get("top") or [])[:5] if PROT else []

# Social results from the What Is Working CRM (pulled by ~/Documents/altr-telegram/social_pull.py)
SOC_PATH = os.path.expanduser("~/Documents/altr-telegram/exports/social.json")
SOC = None
if os.path.exists(SOC_PATH):
    SOC = json.load(open(SOC_PATH, encoding="utf-8"))["models"].get(HANDLE.lstrip("@"))
    if SOC and (SOC.get("views") or 0) < 100 and (SOC.get("likes") or 0) < 100 and (SOC.get("followers_gained") or 0) < 50:
        SOC = None            # negligible social activity this week: drop the chapter rather than embarrass

# chapter and page numbering, with Social and Protection both optional
SECTIONS = ["week", "split", "fans"] + (["social"] if SOC else []) + (["protection"] if PROT else []) + ["next"]
TITLES = {"week": "The week", "split": "Where it came from", "fans": "Fans to know", "social": "Your pages", "protection": "Protection", "next": "Next week"}
NUM = {k: f"{i + 1:02d}" for i, k in enumerate(SECTIONS)}
AID = {k: f"c{i + 1}" for i, k in enumerate(SECTIONS)}
BANDS = sorted(DM["bands"], key=lambda b: -b["gross"])[:2]
HOT_HOUR = max(R["hour_rev"].items(), key=lambda x: x[1])
HOUR_LBL = f"{int(HOT_HOUR[0]) % 12 or 12}{'pm' if int(HOT_HOUR[0]) >= 12 else 'am'}"
MB = MASS["best"][0] if MASS.get("best") else None
MB_DAY = dt.date.fromisoformat(MB["date"][:10]).strftime("%A") if MB else ""
MASS_WEB = (f"Mass messages reached {PCT(MASS['view_rate'], 1)} of inboxes this week; the one that landed best went out {MB_DAY} at {M(MB['price'])} and was bought {MB['purch']} times." if MB else "No mass messages went out this week; everything came from personal conversations.")
MASS_PDF = (f'<div class="ac"><span class="tag">Mass messages</span><h4>{PCT(MASS["view_rate"], 1)} viewed</h4><div class="fig2">{MASS["n"]} sent, {MASS["purchases"]} purchases</div><p>The one that landed best went out {MB_DAY} at {M(MB["price"])} and was bought {MB["purch"]} times.</p></div>' if MB else '<div class="ac"><span class="tag">Mass messages</span><h4>None this week</h4><div class="fig2">0 sent</div><p>Every sale came from personal conversations this week.</p></div>')

def since(f):
    d = f.get("days_since_buy")
    return "No purchase this week" if d is None else f"Bought {max(d, 1):.0f} day{'s' if d >= 1.5 else ''} ago"
def subline(f):
    return f"Subscriber {f['duration']}" if f.get("duration") and f.get("sub_active") else "Reached through messages"

# ------------------------------------------------------------------ PROSE: the only block edited per model
HOOK = [["A quieter week", "one big Friday"], ["Three new names", "worth knowing"]]

LEAD_1 = f"You made {M(NET)} this week, down {PCT(abs(CHANGE),1)} from {M(PREV)}. <em>{E(BEST_DAY)} alone brought in {M(BEST_NET)}, so the demand is there.</em>"

SHAPE = f"Most of the week sat low, and then one evening carried it: {E(BEST_DAY)} made {M(BEST_NET)}, or {PCT(BEST_SHARE,1)} of the total. {N(BUYERS)} people bought something, with a typical purchase of {M(MED)}."

SHAPE2 = f"Your best price range was {E(BANDS[0]['band'])} at {M(BANDS[0]['gross'])}{(', followed by ' + E(BANDS[1]['band']) + ' at ' + M(BANDS[1]['gross'])) if len(BANDS) > 1 else ''}. Fans paid well when the offer felt worth it, which tells us the next step is more good evenings, not lower prices."

NOTES = {
    FANS[0]["id"]: (f"New, {M(FANS[0]['net_w'])} in one night", f"{E(FANS[0]['name'])} found you this week and spent {M(FANS[0]['net_w'])} in a single evening, topping out at {M(FANS[0]['max_ticket'])}."),
    FANS[1]["id"]: (f"{N(FANS[1]['n_sessions'])} visits, up to {M(FANS[1]['max_ticket'])}", f"{E(FANS[1]['name'])} keeps coming back, with {M(FANS[1]['net_w'])} this week across {N(FANS[1]['n_sessions'])} visits."),
    FANS[2]["id"]: (f"One buy at {M(FANS[2]['max_ticket'])}", f"{E(FANS[2]['name'])} spent {M(FANS[2]['net_w'])} this week and is worth a warm hello to bring back."),
}

MOVES = [
    ("Today", "Thank your top three", f"A personal note to {E(FANS[0]['name'])}, {E(FANS[1]['name'])} and {E(FANS[2]['name'])}, who gave {M(FANS[0]['net_w'] + FANS[1]['net_w'] + FANS[2]['net_w'])} between them."),
    ("This week", "Two more big nights", f"We plan two evenings built like {E(BEST_DAY)}, which made {M(BEST_NET)} on its own."),
    ("All week", "Welcome the new faces", f"{N(NEWSUBS)} new fans joined and {N(REBILLS)} renewed, and each one gets a real hello in their first days."),
]

GOOD30 = f"In 30 days, good looks like three or four evenings like {E(BEST_DAY)} every week, so a quieter week still lands well above {M(NET)}, and {E(FANS[1]['name'])} stays among your regulars."

PENDING = [
    ("On ours", "Weekly invoice", "Your invoice for the week lands today alongside this report."),
    ("On your side", "Fresh sets", "Any new photos or short clips you shoot this week go straight into the plan for your big evenings."),
]

CLOSE = f"This week was {M(NET)}, softer than {M(PREV)}, but one evening made {M(BEST_NET)}. <em>We build the next week around that night.</em>"

WEEK_HEAD = f"{M(NET)} this week, <em>{E(BEST_DAY)} led the way</em>"

KN = [
    (E(FANS[0]["name"]), f"Brand new and spent {M(FANS[0]['net_w'])} in one night, topping out at {M(FANS[0]['max_ticket'])}."),
    (E(FANS[1]["name"]), f"Spent {M(FANS[1]['net_w'])} this week across {N(FANS[1]['n_sessions'])} visits, a regular in the making."),
    (E(FANS[2]["name"]), f"Spent {M(FANS[2]['net_w'])} with a single buy of {M(FANS[2]['max_ticket'])}, worth a warm hello."),
]

WARN_FANS = (
    "Worth a hello",
    f"{E(FANS[2]['name'])} spent {M(FANS[2]['net_w'])} this week, and a warm note keeps them close.",
    f"Your top three gave {M(FANS[0]['net_w'] + FANS[1]['net_w'] + FANS[2]['net_w'])} between them, so each one hears from you this week.",
)

STORY_X = [
    f"{E(FANS[0]['name'])} arrived this week and spent {M(FANS[0]['net_w'])} in one evening, the biggest single night from anyone.",
    f"Their top purchase was {M(FANS[0]['max_ticket'])}, which shows how far a new fan will go when the moment feels personal.",
]

PENDING = [
    ("On ours", "Midweek plan", f"We are rebuilding Wednesday and Thursday around personal conversations with the six fans above, with content chosen for each of them, so the floor moves up from {M(1029)}."),
    ("On your side", "This week's statement", "Your statement for the week lands today alongside this report, with the platform-reported figures as the directional view and the ledger as the record."),
]

PENDING = [
    ("On ours", "Midweek plan", f"We are rebuilding Wednesday and Thursday around personal conversations with the six fans above, with content chosen for each of them, so the floor moves up from {M(1029)}."),
    ("On your side", "This week's statement", "Your statement for the week lands today alongside this report, with the platform-reported figures as the directional view and the ledger as the record."),
]

for f in FANS:
    s = f.get("n_sessions", 0)
    auto = f"{s} buying session{'s' if s != 1 else ''}, top {M(f.get('max_ticket') or 0)}"
    f["note"], f["story"] = NOTES.get(f["id"], (auto, ""))[0], NOTES.get(f["id"], ("", ""))[1]
    assert len(f["note"]) <= 40 and len(since(f)) <= 40, f"table text over 40 chars: {f['note']}"

# ------------------------------------------------------------------ charts
m_daily = [{"t": d, "l": M(v), "s": "net that day"} for d, v in DAILY]
m_type = [{"t": t, "l": M(v), "s": "net by type"} for t, v in TYPES]
fig_type = dual(ichart("c-t", [v for _, v in TYPES], m_type, 900, 400, [t for t, _ in TYPES], hot=(0,), fs=2.2,
                       show_val=[M(v) for _, v in TYPES]),
                ichart("c-t-m", [v for _, v in TYPES], m_type, 420, 250, [t for t, _ in TYPES], hot=(0,), fs=1.3, lw=52))
fig_daily = dual(ichart("c-d", [v for _, v in DAILY], m_daily, 900, 400, [d for d, _ in DAILY], hot=(BEST_I,), fs=2.2),
                 ichart("c-d-m", [v for _, v in DAILY], m_daily, 420, 250, [d.split()[1] for d, _ in DAILY], hot=(BEST_I,), fs=1.5, lw=52))

# ------------------------------------------------------------------ WEB
CHAPTERS = [(NUM[k], TITLES[k], AID[k]) for k in SECTIONS]
rows = [{"rank": str(i + 1), "name": f["name"], "sub": subline(f), "amount": M(f["net_w"]), "amount_label": "this week",
         "extra": {"last": since(f), "why": f["note"]}} for i, f in enumerate(FANS)]
H = [hero(FIRST + ".", HOOK,
          f"Your week, {WINDOW}, read from the live account: every purchase, every day, and the fans behind them. Figures are platform-reported.",
          f"Week of {WEEK_OF}<br>Prepared by ALTR for {FIRST}<br>Confidential", PDF, PDF_DL),
     '<div class="teaser">' + big(f"{CH_SIGN}{abs(CHANGE):.1f}<small>%</small>", "on the week before") +
     big(M(NET), "net in seven days") + big(str(BUYERS), "fans bought something") + "</div>",
     method([(7, "days of revenue"), (BUYERS, "paying fans"), (N(VIS), "profile visits"), (N(DM["sent"]), "personal messages"), (MASS["n"], "mass messages")]),
     toc([(n, t, a) for n, t, a in CHAPTERS])]

H.append(f'''<section>{ch(NUM["week"], "The week", WEEK_HEAD, AID["week"])}
<div class="spread"><div class="rv"><p class="lead">{LEAD_1}</p>
<div class="prose" style="margin-top:16px"><p>{SHAPE}</p><p>{SHAPE2}</p></div></div>
<div class="stack">{big(M(NET), "net this week")}{big(M(PREV), "net the week before")}{big(M(MED), "median purchase")}</div></div>
{fig(fig_daily, f"Net per day, {WINDOW}. <em>Mint is {BEST_DAY}.</em>", m_daily[BEST_I])}
<div class="spread" style="margin-top:28px"><div class="rv"><div class="prose"><p>{N(VIS)} people visited the profile this week. Of {N(DM['sent'])} personal messages sent, {PCT(DM['rate'], 1)} were opened and bought, at a median price of {M(DM['median_price'])}.</p>
<p>{MASS_WEB}</p></div></div>
<div class="stack">{big(N(VIS), "profile visits")}{big(str(BUYERS), "fans bought something")}{big(PCT(DM['rate'], 1), "of personal messages bought")}</div></div>
</section>''')

H.append(f'''<section>{ch(NUM["split"], "Where it came from", f"Messages first. <em>{MSG_SHARE}% of net.</em>", AID["split"])}
<div class="spread"><div class="rv"><p class="lead">{TYPE_LINE}</p>
<div class="prose" style="margin-top:16px"><p>{HOWTO}</p></div></div>
<div class="stack">{big(M(GROSS), "gross before platform fee")}{big(M(TYPES[0][1]), "net from messages")}{big(M(W["net_day"]), "average day")}</div></div>
{fig(fig_type, "Net by type. <em>Mint is the largest.</em>", m_type[0])}
</section>''')

H.append(f'''<section>{ch(NUM["fans"], "Fans to know", "Three fans <em>to know this week.</em>", AID["fans"])}
<div class="spread rev rv" style="margin-top:24px"><p class="lead">Your top five are worth <em>{M(TOP5)} between them</em>, {TOP5_SHARE:.0f}% of the whole week.</p>
<div class="prose"><p>The table is the week's top eight by what they spent. <span class="web"><span class="t-h">Move down the list and the card follows you.</span><span class="t-t">Tap a fan for the detail.</span></span></p></div></div>
<div class="whales">{spot(rows[0], [("last", "Last purchase"), ("why", "The week")])}
<div class="twin" style="margin-top:0"><div><div class="ml" style="margin-bottom:10px">By spend this week</div>{ledger(rows, header=("No.", "Fan", "This week"), hi=(rows[0]["name"],))}</div></div></div>
<div class="stories">{story(FANS[0]["name"], f"{M(FANS[0]['net_w'])} this week, number one", subline(FANS[0]), FANS[0]["story"], M(FANS[0]["max_ticket"]), "", STORY_X[0])}
{story(FANS[2]["name"], f"{M(FANS[2]['net_w'])} this week, number three", subline(FANS[2]), FANS[2]["story"], M(FANS[2]["max_ticket"]), "", STORY_X[1])}</div>
{(f'<div class="nurture rv"><span class="k">Your biggest supporter</span><h3>Keep {E(NURTURE["name"])} close</h3><p>{NURTURE["body"]}</p></div>') if NURTURE else ''}
</section>''')

if SOC:
    PLAT = {"instagram": "Instagram", "x": "X", "twitter": "X", "facebook": "Facebook", "tiktok": "TikTok"}
    VK, VL = ("views", "views") if SOC["views"] else ("likes", "likes")
    SOC_N = SOC["views"] or SOC["likes"]
    pg_rows = [{"rank": str(i + 1), "name": r["handle"], "sub": PLAT.get((r["platform"] or "").lower(), r["platform"] or "") + (" promo" if r["farm"] else ""),
                "amount": N(r.get(VK) or 0), "amount_label": VL + " this week", "extra": {}}
               for i, r in enumerate(sorted(SOC["pages"], key=lambda r: -(r.get(VK) or 0))[:8])]
    g = SOC["followers_gained"]
    soc_growth = f'up {SOC["growth"]:.0f}% on last week' if SOC.get("growth") and SOC["growth"] > 0 and VK == "views" else f'across {SOC["accounts_posting"]} page{"s" if SOC["accounts_posting"] != 1 else ""}'
    slot2 = big(f"{g:+,}", "followers gained") if g > 0 else big(N(sum(r["followers"] for r in SOC["pages"])), "followers across pages")
    best_html = ""
    if SOC.get("best") and SOC["best"]["ratio"] >= 1.5:
        b = SOC["best"]
        best_html = story(b["handle"], f'x{b["ratio"]:g} its average', PLAT.get((b["platform"] or "").lower(), ""),
                          f'The standout of the week: one post reached {N(b["views"])} views, {b["ratio"]:g} times what that page usually does.',
                          f'x{b["ratio"]:g}', "", "When a page beats its own average like this, the team repeats the format across the network the following week.")
    H.append(f'''<section>{ch(NUM["social"], "Your pages", "The pages working <em>while you sleep.</em>", AID["social"])}
<div class="spread"><div class="rv"><p class="lead">Your pages did <em>{N(SOC_N)} {VL}</em> this week, {soc_growth}.</p>
<div class="prose" style="margin-top:16px"><p>{SOC["posts"]} posts went out across {SOC["accounts_total"]} backup and promo pages. The table shows the pages that carried the week, and every one of them points fans back to you.</p></div></div>
<div class="stack">{big(N(SOC_N), VL + " this week")}{slot2}{big(str(SOC["posts"]), "posts published")}</div></div>
<div class="twin" style="margin-top:26px"><div><div class="ml" style="margin-bottom:10px">By {VL} this week</div>{ledger(pg_rows, header=("No.", "Page", VL.title()), hi=(pg_rows[0]["name"],) if pg_rows else ())}</div></div>
{('<div class="stories">' + best_html + '</div>') if best_html else ''}
</section>''')

if PROT:
    prot_rows = [{"rank": str(i + 1), "name": d, "sub": "", "amount": N(v), "amount_label": "removed",
                  "extra": {}} for i, (d, v) in enumerate(PROT_TOP)]
    H.append(f'''<section>{ch(NUM["protection"], "Protection", "Your content, <em>kept protected.</em>", AID["protection"])}
<div class="spread"><div class="rv"><p class="lead">{N(PROT["total"])} stolen copies of your content have been <em>found and removed</em>, {N(PROT["last7"])} of them in the last seven days.</p>
<div class="prose" style="margin-top:16px"><p>Another {N(PROT["filed"])} takedown notices are filed and waiting on the hosts. {N(PROT["cases"])} cases have been detected in total since monitoring began, and the sweep runs every week.</p>
<p>{"The table shows where the copies were taken down from. " if PROT_SITES else ""}From the RemoveLabs report of {RL_DATE}.</p></div></div>
<div class="stack">{big(N(PROT["total"]), "stolen copies removed")}{big("+" + N(PROT["last7"]), "removed this week")}{big(N(PROT["filed"]), "notices filed and waiting")}</div></div>
{('<div class="twin" style="margin-top:26px"><div><div class="ml" style="margin-bottom:10px">Where it was stolen from</div>' + ledger(prot_rows, header=("No.", "Site", "Removed")) + '</div></div>') if PROT_SITES else ''}
</section>''')

OI_ITEMS = "".join(f'<div class="item rv"><span class="k">{E(w)}</span><h3>{E(t)}</h3><p>{b}</p></div>' for w, t, b in PENDING)
H.append(f'''<section>{ch(NUM["next"], "Next week", "Open items first. <em>Then next week.</em>", AID["next"])}
<div class="oi"><div class="oik">Open items, from the team chat</div>{OI_ITEMS}</div>
<div class="plan">{plan_step(MOVES[0][0], MOVES[0][1], MOVES[0][2])}
{plan_step(MOVES[1][0], MOVES[1][1], MOVES[1][2], .12)}{plan_step(MOVES[2][0], MOVES[2][1], MOVES[2][2], .24)}</div>
{(f'<div class="ahead rv"><span class="k">On the calendar</span><h3>{E(OCCASION["name"])}, {OCCASION["days"]} days out</h3><p>{E(OCCASION["line"])}</p></div>') if OCCASION else ''}
{closer(M(NET), "net this week", CLOSE, f"ALTR, {DATE}")}
<footer><img src="__LOGO__" alt="ALTR"><span>Prepared by ALTR for {FIRST}. Platform-reported figures. Confidential.</span></footer>
</section>''')

OI_CSS = """
.nurture{border:1.5px solid rgba(182,242,229,.55);background:var(--wash2);border-radius:10px;padding:26px 32px;margin:34px 0 0}
.nurture .k{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--mint)}
.nurture h3{font-weight:360;font-size:clamp(22px,2.8vw,30px);letter-spacing:-.02em;margin:7px 0 9px}
.nurture p{font-size:16px;line-height:1.55;color:var(--bone2);max-width:64ch}
.ahead{border:1.5px solid rgba(182,242,229,.4);background:var(--wash);border-radius:10px;padding:26px 32px;margin:34px 0 10px}
.ahead .k{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--mint)}
.ahead h3{font-weight:360;font-size:clamp(22px,2.8vw,30px);letter-spacing:-.02em;margin:7px 0 9px}
.ahead p{font-size:16px;line-height:1.55;color:var(--bone2);max-width:60ch}

.oi{border:1.5px solid rgba(182,242,229,.55);background:var(--wash);border-radius:10px;padding:34px 38px 14px;margin:30px 0 50px}
.oik{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--mint);margin-bottom:4px}
.oi .item{padding:22px 0 26px;border-top:1px solid var(--line)}.oi .item:first-of-type{border-top:0}
.oi .k{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--bone3)}
.oi h3{font-weight:300;font-size:clamp(26px,3.4vw,38px);letter-spacing:-.02em;line-height:1.08;margin:8px 0 10px}
.oi p{font-size:17px;line-height:1.55;color:var(--bone2);max-width:62ch}
@media(max-width:700px){.oi{padding:24px 22px 8px}.oi h3{font-size:24px}.oi p{font-size:14.5px}}
"""
web = web_doc(TITLE, f"A weekly report prepared by ALTR for {FIRST}, confidential, {DATE}", "\n".join(H), PDF, PDF_DL,
              CHAPTERS, FIRST, extra_css=OI_CSS, spot_fields=["last", "why"])

# ------------------------------------------------------------------ PDF
pdf_keys = ["short", "week", "split", "fans"] + (["social"] if SOC else []) + (["protection"] if PROT else []) + ["next"]
PG = {k: i + 2 for i, k in enumerate(pdf_keys)}
TOT = PG["next"]
PDF_LBL = {"short": "the short version", "week": "the week", "split": "where it came from", "fans": "fans to know", "social": "your pages",
           "protection": "protection", "next": "next week"}
TOC_LBL = {"short": "The short version", "week": "The week", "split": "Where it came from", "fans": "Fans to know", "social": "Your pages",
           "protection": "Protection", "next": "Next week"}
TEASE_FOR = {"week": "Next, the week in detail", "split": "Next, where it came from", "fans": "Next, three fans to know", "social": "Next, your pages",
             "protection": "Next, the protection report", "next": "Next, the plan"}
chapters, teasers = {1: "weekly report"}, {1: "Turn the page, the short version"}
for i, k in enumerate(pdf_keys):
    chapters[PG[k]] = PDF_LBL[k]
    teasers[PG[k]] = TEASE_FOR[pdf_keys[i + 1]] if i + 1 < len(pdf_keys) else "Same time next week"
doc = PrintDoc(TITLE, FIRST, chapters=chapters, teasers=teasers, total=TOT)

doc.page(1, f'''<div class="cvc"><div class="meta">Weekly report, {HANDLE}</div><h1>{FIRST}<i>.</i></h1>
<div class="hook">{HOOK[0][0]} {HOOK[0][1]}<em>{HOOK[1][0]} {HOOK[1][1]}</em></div>
<div class="meta">Prepared by ALTR for {FIRST}, {DATE}. Confidential.</div></div>
<div class="letterc"><div class="lbl">Read first</div><p>Seven days, {WINDOW}, read from the live account: every purchase, every day, and the fans behind them. Figures are platform-reported.</p>
<p>Page two is the short version. The pages after it show the week in detail and what happens next.</p><div class="sig">ALTR</div></div>
{nums([((M(W["net_day"]), "average day") if NEW_ACCT else (CH_STR, "on the week before")), (M(NET), "net this week"), (str(BUYERS), "fans bought something")], cols=3)}
<div class="tocc"><div class="lbl">Inside</div><ol>{"".join(f"<li>{TOC_LBL[k]}<span>{PG[k]:02d}</span></li>" for k in pdf_keys)}</ol></div>''', "cover")

doc.page(2, f'''{head("02", "The short version", "Everything on one page. <em>Start here.</em>", "The week, the fans, and the plan, before the detail.")}
<div><div class="lbl" style="margin-bottom:2mm">What happened</div><div class="find">
{fnd((M(NET) if NEW_ACCT else CH_STR), (f"Net in the first days on the page. {BEST_DAY} brought {M(BEST_NET)}, {BEST_SHARE:.0f}% of it." if NEW_ACCT else f"Net income went {CH_DIR} {abs(CHANGE):.0f}% this week, from {M(PREV)} to {M(NET)}. {BEST_DAY} brought {M(BEST_NET)}, {BEST_SHARE:.0f}% of the week on its own."), True)}
{fnd(M(TOP5), f"What your top five fans spent between them, {TOP5_SHARE:.0f}% of the week.")}
{fnd(N(VIS), f"Profile visits in seven days, and {BUYERS} fans bought something.")}
</div></div>
<div><div class="lbl" style="margin-bottom:2.5mm">Three fans to know</div><div class="know">
<div class="kn"><span class="lbl">{E(KN[0][0])}</span><h4>{E(FANS[0]["name"])}</h4><p>{KN[0][1]}</p></div>
<div class="kn"><span class="lbl">{E(KN[1][0])}</span><h4>{E(FANS[1]["name"])}</h4><p>{KN[1][1]}</p></div>
<div class="kn"><span class="lbl">{E(KN[2][0])}</span><h4>{E(FANS[2]["name"])}</h4><p>{KN[2][1]}</p></div>
</div></div>
<div><div class="lbl" style="margin-bottom:2.5mm">Next week</div><div class="wk">
<div><span class="lbl">{MOVES[0][0]}</span><h4>{MOVES[0][1]}</h4><p>The best releases stack from Thursday night into Friday.</p></div>
<div><span class="lbl">{MOVES[1][0]}</span><h4>{MOVES[1][1]}</h4><p>Offers stay in the {BANDS[0]['band']} and {BANDS[1]['band']} ranges that worked.</p></div>
<div><span class="lbl">{MOVES[2][0]}</span><h4>{MOVES[2][1]}</h4><p>All {NEWSUBS} new fans get a personal hello inside two days.</p></div></div></div>''')

doc.page(PG["week"], f'''{head(f"{PG['week']:02d}", "The week", WEEK_HEAD, f"Net was {M(NET)} against {M(PREV)} the week before, {M(W['net_day'])} a day.")}
<div class="chart">{ichart("p-d", [v for _, v in DAILY], [{}] * len(DAILY), 900, 430, [d for d, _ in DAILY], hot=(BEST_I,), fs=1.6)}<div class="cap">Net per day, {WINDOW}. <em>Mint is {BEST_DAY}.</em></div></div>
{nums([(M(W["net_day"]), "net per day"), (str(BUYERS), "fans bought something"), (M(MED), "median purchase"), (N(VIS), "profile visits")])}
{warn(f"{BEST_DAY.split()[0]} was {BEST_SHARE:.0f}% of the week", f"{BEST_DAY} closed at {M(BEST_NET)} of the week's {M(NET)}, and the best single hour of the week was {HOUR_LBL}.", f"Messages carried {M(W['msg'])} of the total and tips {M(W['tips'])}; the median purchase rose from {M(P['median_ticket'])} to {M(MED)}.")}
<div class="acct">{'<div class="ac"><span class="tag">Personal messages</span><h4>' + PCT(DM["rate"], 1) + ' bought</h4><div class="fig2">' + N(DM["sent"]) + ' sent, median price ' + M(DM["median_price"]) + '</div><p>' + N(DM["fans_reached"]) + ' fans heard from you one to one this week, and ' + str(DM["bought"]) + ' of those messages were purchased.</p></div>' if DM["sent"] else '<div class="ac"><span class="tag">Personal messages</span><h4>None sent yet</h4><div class="fig2">0 sent this week</div><p>Not one personal message went out this week. The plan on the last page starts them, with the top of your list first.</p></div>'}
{MASS_PDF}</div>''')

half = (len(DAILY) + 1) // 2
def day_table(rows, offset):
    out = "".join(f'<tr><td class="n">{offset + i + 1}</td><td class="fan"><b>{DAYNAMES[offset + i]}</b></td>'
                  f'<td class="bar"><span><i style="width:{v / BEST_NET * 100:.0f}%"></i></span></td>'
                  f'<td class="num">{M(v)}</td><td>{v / NET * 100:.0f}% of the week</td></tr>'
                  for i, (_, v) in enumerate(rows))
    return f'<table class="qt"><thead><tr><th>No.</th><th>Day</th><th></th><th class="num">Net</th><th>Of the week</th></tr></thead><tbody>{out}</tbody></table>'

doc.page(PG["split"], f'''{head(f"{PG['split']:02d}", "Where it came from", f"Messages first. <em>{MSG_SHARE}% of net.</em>", TYPE_LINE)}
<div class="chart">{ichart("p-t", [v for _, v in TYPES], [{}] * 5, 900, 330, [t for t, _ in TYPES], hot=(0,), fs=1.6,
                           show_val=[M(v) for _, v in TYPES])}<div class="cap">Net by type. <em>Mint is the largest.</em></div></div>
<div class="lbl">Every day in the window</div>
<div class="two">{day_table(DAILY[:half], 0)}{day_table(DAILY[half:], half)}</div>
{nums([(M(GROSS), "gross before platform fee"), (f"{MSG_SHARE}%", "of net from messages"), (M(W["net_day"]), "average day"), (M(MED), "median purchase")])}
{warn("How to read the figures", HOWTO)}''')

doc.page(PG["fans"], f'''{head(f"{PG['fans']:02d}", "Fans to know", "The week's top eight, <em>and their stories.</em>", f"Your top five spent {M(TOP5)} between them, {TOP5_SHARE:.0f}% of the week.")}
<div class="lbl">By spend this week</div>
{qtable([(f["name"], str(i + 1), round(f["net_w"]), f["note"], since(f)) for i, f in enumerate(FANS)], round(FANS[0]["net_w"]),
        header='<thead><tr><th>No.</th><th>Fan, and the week they had</th><th></th><th class="num">This week</th><th>Last purchase</th></tr></thead>')}
{warn("Your biggest supporter this week", NURTURE["body"]) if NURTURE else warn(WARN_FANS[0], WARN_FANS[1], WARN_FANS[2])}
{nums([(M(TOP5), "top five, this week"), (f"{TOP5_SHARE:.0f}%", "their share of the week"), (M(FANS[0]["net_w"]), "the number one fan"), (M(FANS[0]["max_ticket"]), "largest single purchase")])}''')

if SOC:
    spages = sorted(SOC["pages"], key=lambda r: -(r.get(VK) or 0))
    fg = SOC["followers_gained"]
    slot2_pdf = (f"{fg:+,}", "followers gained") if fg > 0 else (N(sum(r["followers"] for r in SOC["pages"])), "followers across pages")
    top_pg = (spages[0].get(VK) or 1) if spages else 1
    pg_tbl = "".join(f'<tr><td class="n">{i + 1}</td><td class="fan"><b>{E(r["handle"])}</b><i>{PLAT.get((r["platform"] or "").lower(), "")}{" promo" if r["farm"] else ""}</i></td>'
                     f'<td class="bar"><span><i style="width:{(r.get(VK) or 0) / top_pg * 100:.0f}%"></i></span></td>'
                     f'<td class="num">{r["views"]:,}</td><td>{r["posts"]} posts sent</td></tr>' for i, r in enumerate(spages[:8]))
    gr = f", up {SOC['growth']:.0f}% on last week" if SOC.get("growth") and SOC["growth"] > 0 else ""
    b = SOC.get("best")
    stand = (f'One post on {E(b["handle"])} reached {N(b["views"])} views, {b["ratio"]:g} times what that page usually does. The team repeats a format like that across the network the following week.'
             if b and b["ratio"] >= 1.5 else
             f'{SOC["accounts_posting"]} of {SOC["accounts_total"]} pages posted this week. The job of every one of them is to catch searches and trends and point the traffic back to you.')
    doc.page(PG["social"], f'''{head(f"{PG['social']:02d}", "Your pages", "The pages working <em>while you sleep.</em>", f"{N(SOC_N)} {VL} across {SOC['posts']} posts this week{gr}.")}
{nums([(N(SOC_N), VL + " this week"), slot2_pdf, (str(SOC["posts"]), "posts published"), (str(SOC["accounts_total"]), "page in the network" if SOC["accounts_total"] == 1 else "pages in the network")])}
<div class="lbl">By {VL} this week</div>
<table class="qt"><thead><tr><th>No.</th><th>Page</th><th></th><th class="num">{VL.title()}</th><th>Posts sent</th></tr></thead><tbody>{pg_tbl}</tbody></table>
<div class="acct"><div class="ac"><span class="tag">How it works</span><h4>Pages point home</h4><p>Your main page is never the only door. The backup and promo pages catch searches, reposts and trends, and send everyone back to you.</p></div>
<div class="ac"><span class="tag">The standout</span><h4>What worked this week</h4><p>{stand}</p></div></div>
{warn("Where these numbers come from", "View counts are read from each platform daily and cover posts published in the last seven days. Platform-reported figures, rolling window.")}''')

if PROT:
    top_v = PROT_TOP[0][1] if PROT_TOP else 1
    prot_tbl = "" if not PROT_SITES else "".join(f'<tr><td class="n">{i + 1}</td><td class="fan"><b>{E(d)}</b></td>'
                       f'<td class="bar"><span><i style="width:{v / top_v * 100:.0f}%"></i></span></td>'
                       f'<td class="num">{v:,}</td><td></td></tr>' for i, (d, v) in enumerate(PROT_TOP))
    doc.page(PG["protection"], f'''{head(f"{PG['protection']:02d}", "Protection", "Your content, <em>kept protected.</em>", f"{N(PROT['total'])} stolen copies found and removed, {N(PROT['last7'])} of them this week.")}
{nums([(N(PROT["total"]), "stolen copies removed"), ("+" + N(PROT["last7"]), "removed this week"), (N(PROT["filed"]), "notices filed, waiting"), (N(PROT["cases"]), "cases detected in total")])}
{'<div class="lbl">Where it was stolen from</div><table class="qt"><thead><tr><th>No.</th><th>Site</th><th></th><th class="num">Copies removed</th><th></th></tr></thead><tbody>' + prot_tbl + '</tbody></table>' if PROT_SITES else ''}
<div class="acct"><div class="ac"><span class="tag">How it works</span><h4>Found, filed, removed</h4><p>The sweep scans search results and leak sites for your content every week, files the takedown notices, and follows each one until the copy is gone.</p></div>
<div class="ac"><span class="tag">What it means</span><h4>Fans find you, not leaks</h4><p>Every removed copy is one less free version sitting between a searching fan and your page.</p></div></div>
{warn("Filed and waiting", f"{N(PROT['filed'])} notices are filed and waiting on the hosts, on top of the {N(PROT['total'])} already removed. From the RemoveLabs report of {RL_DATE}; next update lands in the team chat weekly.")}''')

doc.page(PG["next"], f'''{head(f"{PG['next']:02d}", "Next week", "Open items first. <em>Then next week.</em>", "Two things from the team chat, then the plan.")}
<div class="lbl" style="color:var(--mint)">Open items, from the team chat</div>
<div class="oip{' solo' if len(PENDING) == 1 else ''}">{"".join(f'<div class="oc"><span class="k">{E(w)}</span><h3>{E(t)}</h3><p>{b}</p></div>' for w, t, b in PENDING)}</div>
<div class="asks4">
<div class="a4"><span class="lbl">01</span><h4>{MOVES[0][1]}</h4><p>{MOVES[0][2]}</p></div>
<div class="a4"><span class="lbl">02</span><h4>{MOVES[1][1]}</h4><p>{MOVES[1][2]}</p></div>
<div class="a4"><span class="lbl">03</span><h4>{MOVES[2][1]}</h4><p>{MOVES[2][2]}</p></div>
<div class="a4">{(f'<span class="lbl" style="color:var(--mint)">On the calendar</span><h4>{E(OCCASION["name"])}, {OCCASION["days"]} days out</h4><p>{E(OCCASION["line"])}</p>') if OCCASION else f'<span class="lbl">04</span><h4>What good looks like in 30 days</h4><p>{GOOD30}</p>'}</div></div>
<div class="close"><img src="__MARK__" alt=""><div><b>{M(NET)}</b><small>net this week</small></div>
<div><p>{CLOSE.replace("<em>", "<strong>").replace("</em>", "</strong>")}</p><div class="sig">ALTR, {DATE}. Platform-reported figures.</div></div></div>''')

OIP_CSS = """
.ahead{border:1px solid rgba(182,242,229,.45);background:var(--wash);border-radius:2mm;padding:4mm 5mm;margin-top:3mm;flex:0 0 auto}
.ahead .k{font-family:var(--mono);font-size:7pt;letter-spacing:.14em;text-transform:uppercase;color:var(--mint)}
.ahead h4{font-weight:500;font-size:11pt;margin-top:1.5mm}.ahead p{margin-top:1.5mm;font-size:9pt;color:var(--bone2);line-height:1.5}
.cvc{text-align:center;padding-top:2mm}
.cvc h1{font-weight:360;font-size:76pt;line-height:.85;letter-spacing:-.05em}.cvc h1 i{font-style:normal;color:var(--mint)}
.cvc .meta{font-family:var(--mono);font-size:8.1pt;letter-spacing:.18em;text-transform:uppercase;color:var(--bone3);margin:3mm 0}
.cvc .hook{margin:4mm auto 2mm;font-weight:360;font-size:19pt;line-height:1.2;letter-spacing:-.02em;max-width:150mm}
.cvc .hook em{display:block;font-style:normal;color:var(--mint)}
.letterc{max-width:152mm;margin:0 auto;text-align:center;padding:4.5mm 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line);width:100%;align-self:center}
.letterc .lbl{margin-bottom:3mm}
.letterc p{font-size:12.3pt;line-height:1.65;color:var(--bone2)}.letterc p + p{margin-top:3mm}
.letterc .sig{margin-top:4mm;font-family:var(--mono);font-size:8.1pt;letter-spacing:.18em;text-transform:uppercase;color:var(--bone)}
.tocc{max-width:118mm;margin:0;width:100%;text-align:left}
.tocc .lbl{margin-bottom:2mm}
.tocc ol{list-style:none}.tocc li{display:flex;justify-content:space-between;align-items:baseline;padding:1.7mm 0;border-bottom:1px solid var(--soft);font-size:11.4pt}
.tocc li span{font-family:var(--mono);font-size:8.6pt;color:var(--bone3)}
.two .qt td{padding:2mm 1.4mm}

.oip{display:grid;grid-template-columns:1fr 1fr;gap:4mm;flex:0 0 auto}
.oip.solo{grid-template-columns:1fr}.oip.solo .oc h3{white-space:normal}
.oc{border:1.5px solid rgba(182,242,229,.6);background:var(--wash);border-radius:2mm;padding:5mm 5.5mm 4.5mm}
.oc .k{font-family:var(--mono);font-size:7pt;letter-spacing:.14em;text-transform:uppercase;color:var(--mint)}
.oc h3{font-weight:300;font-size:16.5pt;letter-spacing:-.02em;line-height:1.05;margin-top:2mm;white-space:nowrap}
.oc p{margin-top:2.5mm;font-size:9.8pt;color:var(--bone);line-height:1.5}
"""
# Months the data actually covers, plus the month on the cover: anything else in the text is a bug.
WINDOW_MONTHS = {_w0.strftime("%B"), _w1.strftime("%B"), DATE.split()[0]}
if OCCASION: WINDOW_MONTHS.add(OCCASION["date"].strftime("%B"))
write_outputs(web, doc.html(OIP_CSS), PDF, TITLE, window_months=WINDOW_MONTHS)
