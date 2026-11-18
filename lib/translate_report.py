# -*- coding: utf-8 -*-
"""Translate a built report into Latin American Spanish, as a sibling folder.

    python3 lib/translate_report.py WORK/naza-weekly WORK/naza-es-weekly

Reads the SOURCE folder's built template.html + print-template.html (run its build first),
extracts every visible text segment (plus chart tooltip strings), translates them in one
`claude -p` call, validates (same keys, digits preserved, no em dashes), and writes the
translated templates into DEST. Numbers, names, @handles and ALTR are kept exactly.

DEST then builds and deploys like any report folder:  cd DEST && python3 ../../lib/build.py

First run scaffolds DEST (slug.txt, vercel.json, report.json, deploy.sh, es-meta.json).
Exits non-zero on any validation failure so a bad translation cannot publish.
"""
import json, re, sys, subprocess, random, string, shutil
from pathlib import Path

LETTERS = re.compile(r"[A-Za-z]{2,}")
DIGITS = re.compile(r"\d")
# segments never sent for translation
# Never send these for translation: they must come back byte-identical. Bare domain names matter
# here because the DMCA table lists leak sites, and a translator may mangle or refuse them.
KEEP = re.compile(r"^(ALTR|@[\w.]+|https?://\S+|[a-z0-9][a-z0-9.-]*\.[a-z]{2,}|[\d\s.,:$%+()/-]*)$", re.I)


ENTITY = re.compile(r"&#?\w+;")
def nums_in(t):
    """Numbers that are real content. HTML entities like &#x27; carry digits that are not numbers."""
    return sorted(re.findall(r"\d+(?:[.,]\d+)*", ENTITY.sub(" ", t)))

def segments(html):
    """Collect translatable strings: text nodes outside script/style, and tooltip strings inside scripts."""
    segs = set()
    scripts = re.findall(r"<script[^>]*>(.*?)</script>", html, re.S)
    body = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", html, flags=re.S)
    for m in re.finditer(r">([^<>]+)<", body):
        t = m.group(1)
        if LETTERS.search(t) and not KEEP.match(t.strip()):
            segs.add(t)
    for sc in scripts:
        for m in re.finditer(r'"(?:t|s)":\s*"([^"]+)"', sc):
            t = m.group(1)
            if LETTERS.search(t) and not KEEP.match(t.strip()):
                segs.add(t)
    return sorted(segs, key=len, reverse=True)

def translate(segs, cache=None):
    cache = cache or {}
    reused = {s: cache[s] for s in segs if s in cache}
    segs = [s for s in segs if s not in cache]
    if not segs:
        print(f"all {len(reused)} segments reused from es-map.json cache")
        return reused
    print(f"reusing {len(reused)} cached segments, translating {len(segs)} new ones")
    src = {str(i): s for i, s in enumerate(segs)}
    prompt = f"""Translate the VALUES of this JSON object from English to natural Latin American Spanish.
It is a web report, written to a creator named Naza, about her own OnlyFans earnings. Address her as tu (informal).

Hard rules:
- Plain everyday Spanish a non-technical reader understands instantly. No corporate words, no analytics jargon, no metaphors.
- Keep EXACTLY as they are: every number, dollar amount ($1,234 stays $1,234), percent, date digits, @handles, the word ALTR, people's names (fans like Dez), URLs, and any HTML entities such as &amp; or &#39;.
- Translate month names and date wording naturally (October 15, 2026 -> 15 de octubre de 2026).
- Never use em dashes. Use commas or periods.
- Keep leading/trailing spaces of each value as in the original.
- Keep it warm and direct, the register of a manager writing to the creator herself.

Reply with ONLY the translated JSON object, same keys, no commentary, no code fences.

{json.dumps(src, ensure_ascii=False, indent=0)}"""
    out = subprocess.run(["claude", "-p"], input=prompt, capture_output=True, text=True, timeout=600, cwd=str(Path.home())).stdout
    m = re.search(r"\{.*\}", out, re.S)
    if not m:
        if re.search(r"usage credits|rate limit|quota", out, re.I):
            sys.exit("Claude usage credits are exhausted, so the Spanish edition cannot be translated. "
                     "Top up at https://claude.ai/settings/usage and rerun this deploy. "
                     "The English report is unaffected.")
        sys.exit(f"translator returned no JSON. First 200 chars of its reply: {out[:200]!r}")
    got = json.loads(m.group(0))
    if set(got) != set(src):
        sys.exit(f"translator dropped keys: {sorted(set(src) ^ set(got))[:5]}")
    for k, s in src.items():
        t = got[k]
        if nums_in(s) != nums_in(t):
            sys.exit(f"numbers changed in segment {k}: {s!r} -> {t!r}")
        if "—" in t or not t.strip():
            sys.exit(f"bad segment {k}: {t!r}")
    return reused | {src[k]: got[k] for k in src}

def apply(html, mapping):
    for o, t in sorted(mapping.items(), key=lambda kv: len(kv[0]), reverse=True):
        html = html.replace(f">{o}<", f">{t}<")
        if o != t:
            jo, jt = json.dumps(o, ensure_ascii=False)[1:-1], json.dumps(t, ensure_ascii=False)[1:-1]
            html = html.replace(f'"{jo}"', f'"{jt}"')
    return html

def scaffold(src: Path, dst: Path):
    dst.mkdir(exist_ok=True)
    if not (dst / "slug.txt").exists():
        suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=7))
        (dst / "slug.txt").write_text(f"{dst.name}-{suffix}\n", encoding="utf-8")
    for f in ("vercel.json", ".vercelignore", "takedown.sh"):
        if (src / f).exists() and not (dst / f).exists():
            shutil.copy(src / f, dst / f)
    b = (src / "build_premium.py").read_text(encoding="utf-8")
    name = re.search(r'NAME = "([^"]+)"', b).group(1)
    handle = re.search(r'HANDLE = "([^"]+)"', b).group(1)
    date = re.search(r'DATE = "([^"]+)"', b).group(1)
    (dst / "es-meta.json").write_text(json.dumps({"name": name, "handle": handle, "date": date}), encoding="utf-8")
    meta = json.loads((src / "report.json").read_text(encoding="utf-8"))
    meta["pdf"] = meta["pdf"].replace("ALTR-", "ALTR-es-")
    meta["title"] = f"{name}. Reporte semanal de ALTR"
    (dst / "report.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")
    if not (dst / "deploy.sh").exists():
        (dst / "deploy.sh").write_text(f"""#!/usr/bin/env bash
# Spanish edition of ../{src.name}. Translates the built source templates, renders, deploys, files to Drive.
set -e
cd "$(dirname "$0")"
python3 ../../lib/translate_report.py "../{src.name}" .
# Spanish runs longer than English; if qa_pdf flags overflow or lone words, shorten those segments and retry (twice).
for try in 1 2 3; do
  if python3 ../../lib/build.py > /tmp/es-build.log 2>&1; then tail -2 /tmp/es-build.log; break; fi
  [ "$try" = 3 ] && {{ echo "!! Spanish render still failing qa_pdf after 2 shorten passes:"; tail -12 /tmp/es-build.log; exit 1; }}
  python3 ../../lib/translate_report.py --shorten "../{src.name}" . --log /tmp/es-build.log
done
NAME="$(tr -d '[:space:]' < slug.txt)"
export VERCEL_TELEMETRY_DISABLED=1
if [ ! -d .vercel ]; then
  vercel link --yes --project "$NAME" >/dev/null 2>&1 || vercel project add "$NAME" && vercel link --yes --project "$NAME"
fi
vercel deploy --prod --yes
PDF=$(python3 -c "import json;print(json.load(open('report.json'))['pdf'])")
DEST=$(python3 -c "import json;m=json.load(open('es-meta.json'));print(f\\"{{m['name']}}/{{m['name']}} - {{m['handle']}} - {{m['date'].replace(',','')}} (Espanol).pdf\\")")
rclone copyto "$PDF" "gdrive-reports:$DEST" && echo "uploaded -> $DEST" || echo "!! Drive upload failed; retry the rclone line by hand."
echo "live: https://$NAME.vercel.app   pdf: https://$NAME.vercel.app/$PDF"
""", encoding="utf-8")

def write_templates(src, dst, mapping):
    for f in ("template.html", "print-template.html"):
        h = apply((src / f).read_text(encoding="utf-8"), mapping)
        (dst / f).write_text(h.replace('lang="en"', 'lang="es"', 1), encoding="utf-8")
    (dst / "es-map.json").write_text(json.dumps(mapping, ensure_ascii=False, indent=0), encoding="utf-8")

def shorten(src, dst, fragments):
    """Re-translate the segments whose Spanish contains any of the given fragments, shorter.
    Used by deploy.sh when qa_pdf flags overflow or lone words in the Spanish render.
    Fragments may be given directly, or via  --log <file>  holding qa_pdf output."""
    if fragments[:1] == ["--log"]:
        log = Path(fragments[1]).read_text(encoding="utf-8")
        # LONE WORD lines carry context ("after '...'"); require both parts so one common
        # word does not sweep in half the report. OVERFLOW/EDGE fragments are specific enough alone.
        specs = [[w, after] for w, after in re.findall(r"LONE WORD '([^']+)' after '([^']+)'", log)]
        specs += [[f] for f in re.findall(r"(?:OVERFLOW|EDGE) '([^']+)'", log)]
        if not specs:
            sys.exit("qa log has no LONE WORD / OVERFLOW / EDGE lines to fix")
        print(f"shortening segments matching {len(specs)} flagged fragments")
    else:
        specs = [[f] for f in fragments]
    mapping = json.loads((dst / "es-map.json").read_text(encoding="utf-8"))
    hits = {o: t for o, t in mapping.items()
            if any(all(p.strip() and p.strip() in t for p in spec) for spec in specs)}
    if len(hits) > 25:
        sys.exit(f"flagged fragments matched {len(hits)} segments; matching too loose, not rewriting")
    if not hits:
        sys.exit("no translated segment matches the flagged fragments")
    src_j = {str(i): {"english": o, "spanish_too_long": t} for i, (o, t) in enumerate(hits.items())}
    prompt = f"""These Spanish translations broke the page layout because they run longer than the English originals.
Rewrite each Spanish text SHORTER: no longer than its English original, same meaning, same plain warm register (tu form), keeping every number, dollar amount, percent, name and @handle exactly. Never use em dashes.
Reply with ONLY a JSON object mapping each key to the new shorter Spanish string, no commentary, no code fences.

{json.dumps(src_j, ensure_ascii=False, indent=0)}"""
    out = subprocess.run(["claude", "-p"], input=prompt, capture_output=True, text=True, timeout=600, cwd=str(Path.home())).stdout
    m = re.search(r"\{.*\}", out, re.S)
    got = json.loads(m.group(0))
    for k, v in src_j.items():
        t = got[k]
        if nums_in(v["english"]) != nums_in(t) or "—" in t or not t.strip():
            sys.exit(f"bad shortened segment {k}: {t!r}")
        mapping[v["english"]] = t
        print(f"  shortened: {v['spanish_too_long'][:50]!r} -> {t[:50]!r}")
    write_templates(src, dst, mapping)
    print("rewrote templates with shortened segments. rebuild now.")

def main():
    if sys.argv[1] == "--shorten":
        src, dst = Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve()
        return shorten(src, dst, sys.argv[4:])
    src, dst = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    scaffold(src, dst)
    for f in ("template.html", "print-template.html"):
        if not (src / f).exists():
            sys.exit(f"{src / f} missing; build the source report first")
    web = (src / "template.html").read_text(encoding="utf-8")
    pdf = (src / "print-template.html").read_text(encoding="utf-8")
    segs = sorted(set(segments(web)) | set(segments(pdf)), key=len, reverse=True)
    print(f"{len(segs)} segments total")
    cache = json.loads((dst / "es-map.json").read_text(encoding="utf-8")) if (dst / "es-map.json").exists() else {}
    mapping = translate(segs, cache)
    write_templates(src, dst, mapping)
    print(f"wrote translated templates to {dst}. next: cd {dst} && python3 ../../lib/build.py")

if __name__ == "__main__":
    main()
