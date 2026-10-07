# -*- coding: utf-8 -*-
"""
Scaffold a new report folder under WORK/.

    python3 lib/new_report.py <slug> "<Creator name>" [--pdf ALTR-<slug>-<mon><dd>.pdf]

Creates WORK/<slug>/ with:
  build_premium.py     a copy of report_skeleton.py: the one file you edit (content and numbers only)
  deploy.sh            builds, then deploys to Vercel under a share-ready project name (slug.txt)
  takedown.sh          takes the link offline
  slug.txt             the Vercel project name: <slug>-<7 random chars>
  vercel.json          noindex + no-store headers
  data/ qa/            (gitignored) raw pulls and QA renders

Then: pull data (lib/pull_account.py), analyse (lib/analyze_ledger.py), write the builder, run
python3 build_premium.py && python3 ../../lib/build.py, look at qa/*.png, deploy.
"""
import sys, os, re, secrets, string, datetime as dt, shutil
from pathlib import Path
LIB = Path(__file__).resolve().parent; ROOT = LIB.parent
if len(sys.argv) < 3:
    sys.exit(__doc__)
slug = re.sub(r"[^a-z0-9-]", "-", sys.argv[1].lower()).strip("-"); name = sys.argv[2]
pdf = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--pdf=")), f"ALTR-{slug}-{dt.date.today().strftime('%b%d').lower()}.pdf")
d = ROOT / "WORK" / slug
if d.exists(): sys.exit(f"{d} already exists")
(d / "data").mkdir(parents=True); (d / "qa").mkdir()
tail = "".join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(7))
(d / "slug.txt").write_text(f"{slug}-{tail}\n")
(d / "vercel.json").write_text('{ "headers": [ { "source": "/(.*)", "headers": [ { "key": "X-Robots-Tag", "value": "noindex, nofollow" }, { "key": "Cache-Control", "value": "no-store" } ] } ] }\n')
(d / ".gitignore").write_text("data/\nqa/\n.vercel\nindex.html\nprint.html\n")
sk = (LIB / "report_skeleton.py").read_text(encoding="utf-8")
sk = sk.replace("__NAME__", name).replace("__PDF__", pdf).replace("__DATE__", dt.date.today().strftime("%B %d, %Y").replace(" 0", " "))
(d / "build_premium.py").write_text(sk, encoding="utf-8")
for s in ("deploy.sh", "takedown.sh", ".vercelignore"):
    shutil.copy(LIB / s, d / s); os.chmod(d / s, 0o755)
print(f"created WORK/{slug}/  (vercel project will be {slug}-{tail}, pdf {pdf})")
print(f"next:  cd WORK/{slug} && python3 ../../lib/pull_account.py <account> --days 30")
