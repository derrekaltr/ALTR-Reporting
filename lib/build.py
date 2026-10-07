# -*- coding: utf-8 -*-
"""
Build step for any report folder. Run from inside the report folder (WORK/<slug>/):

    python3 ../../lib/build.py                # inline brand kit, render PDF, run the PDF scanners
    python3 ../../lib/build.py --no-qa        # skip the scanners (for a quick look only)

Reads  template.html        -> writes index.html        (the link)
Reads  print-template.html  -> writes print.html        (the PDF edition) -> renders <pdf name>.pdf with headless Chrome
The PDF filename comes from report.json ("pdf": "ALTR-<slug>-<mon><dd>.pdf") or defaults to ALTR-<folder>.pdf.

Then runs qa_pdf.py (lone words, text under 6pt, text at the page edge, overflow, wrapped headings) and
exits non-zero when it finds a defect, so a build with defects cannot be mistaken for a finished one.
Fix at the source and build again.

Chrome is found automatically on macOS, Windows and Linux; override with env CHROME=/path/to/chrome.
"""
import base64, os, sys, subprocess, json, shutil, platform
from pathlib import Path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ofapi import kit_root

HERE = Path.cwd()
ROOT = kit_root(HERE)
KIT = ROOT / "BRAND-KIT"
LIB = Path(__file__).resolve().parent
meta = json.loads((HERE / "report.json").read_text(encoding="utf-8")) if (HERE / "report.json").exists() else {}
PDF = meta.get("pdf") or f"ALTR-{HERE.name}.pdf"


def chrome_path():
    c = os.environ.get("CHROME")
    if c and Path(c).exists(): return c
    cands = {
        "Darwin": ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                   str(Path.home() / "Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
                   "/Applications/Chromium.app/Contents/MacOS/Chromium",
                   "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
                   "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"],
        "Windows": [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                    str(Path.home() / r"AppData\Local\Google\Chrome\Application\chrome.exe"),
                    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"],
        "Linux": ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser"],
    }[platform.system()]
    for c in cands:
        if Path(c).exists() or shutil.which(c): return c
    sys.exit("Chrome not found. Install Google Chrome, or set CHROME=/path/to/chrome.")


def b64(n): return "data:image/png;base64," + base64.b64encode((KIT / n).read_bytes()).decode()
LOGO, GHOST, MARK = b64("altr-logo.png"), b64("altr-ghost.png"), b64("altr-mark-dark.png")

def inline(src, dst):
    if not (HERE / src).exists(): return False
    h = (HERE / src).read_text(encoding="utf-8")
    h = h.replace("__LOGO__", LOGO).replace("__GHOST__", GHOST).replace("__MARK__", MARK)
    (HERE / dst).write_text(h, encoding="utf-8")
    print(f"{dst}: {len(h)//1024} KB")
    return True

inline("template.html", "index.html")
have_print = inline("print-template.html", "print.html")
if not have_print:
    sys.exit("no print-template.html in this folder; the builder (build_premium.py) must write it first")

chrome = chrome_path()
url = (HERE / "print.html").resolve().as_uri()
r = subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=10000",
                    f"--print-to-pdf={HERE / PDF}", url], capture_output=True, text=True, timeout=180)
if not (HERE / PDF).exists():
    sys.exit(f"PDF was not written. Chrome said:\n{r.stderr[-1500:]}")
print(f"{PDF}: {os.path.getsize(HERE / PDF)//1024} KB")

if "--no-qa" in sys.argv:
    sys.exit(0)
print("\n== qa_pdf (must end with 'issues 0') ==", flush=True)
q = subprocess.run([sys.executable, str(LIB / "qa_pdf.py"), PDF], text=True)
print("\nNow LOOK at every qa/q<N>a.png and q<N>b.png before deploying. The scanner catches what it can; the renders catch the rest.", flush=True)
sys.exit(q.returncode)
