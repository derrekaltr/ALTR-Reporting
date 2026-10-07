# -*- coding: utf-8 -*-
"""
PDF typography scanner. Exit code 1 when anything is found.

    python3 ../../lib/qa_pdf.py <file.pdf>

Checks every page for:
  LONE WORD   a prose block whose last line is a single word (a widow); shorten or rephrase at the source
  SMALL       any text under 6pt (unreadable in print; usually a chart label scaled down in a half-width card)
  EDGE        text within the page margin (about 46pt from the sides, 8pt from the bottom): something overflowed or shifted
  OVERFLOW    a page whose text extends past the sheet (content did not fit, flex squeezed it, or a card collided)
  WRAPPED     (informational, not counted) a heading or short label that took two lines. Expected for the
              two-part chapter heading, chart axis labels and merged table cells; shorten anything else.
Also writes qa/q<N>a.png and qa/q<N>b.png, the top and bottom halves of every page at 150 dpi. Read them.
"""
import sys, os
try:
    import pymupdf
except ImportError:
    sys.exit("pymupdf missing: python3 -m pip install -r requirements.txt")
f = sys.argv[1] if len(sys.argv) > 1 else next((x for x in os.listdir(".") if x.lower().endswith(".pdf")), None)
if not f: sys.exit("no pdf given")
d = pymupdf.open(f); print("pages", d.page_count)
os.makedirs("qa", exist_ok=True)
issues = 0
for pi, p in enumerate(d):
    W, H = p.rect.width, p.rect.height
    for b in p.get_text("dict")["blocks"]:
        if b.get("type") != 0: continue
        L = [("".join(x["text"] for x in l["spans"]).strip(), l) for l in b["lines"]]; L = [x for x in L if x[0]]
        if len(L) >= 2:
            s1, s2 = L[-1][1]["spans"][0]["size"], L[-2][1]["spans"][0]["size"]
            if abs(s1 - s2) < .2 and 7 <= s1 <= 30 and len(L[-1][0].split()) <= 1 and not L[-1][0][0].isdigit() and "$" not in L[-1][0]:
                print(f"p{pi+1} LONE WORD '{L[-1][0]}' after '{L[-2][0][-40:]}'"); issues += 1
            txt = " ".join(t for t, _ in L)
            if len(txt) <= 78 and s2 >= 8.5 and s2 != 21.0:
                print(f"p{pi+1} WRAPPED {s2:.0f}pt {len(L)} lines: {txt[:70]}")
        for t, l in L:
            for sp in l["spans"]:
                if not sp["text"].strip(): continue
                if sp["size"] < 6: print(f"p{pi+1} SMALL {sp['size']:.1f}pt '{sp['text'][:25]}'"); issues += 1
                x0, y0, x1, y1 = sp["bbox"]
                if x1 > W - 46 or y1 > H - 8 or x0 < 30: print(f"p{pi+1} EDGE '{sp['text'][:25]}'"); issues += 1
                if y1 > H + 1 or x1 > W + 1: print(f"p{pi+1} OVERFLOW '{sp['text'][:25]}'"); issues += 1
    r = p.rect
    p.get_pixmap(dpi=150, clip=pymupdf.Rect(0, 0, r.width, r.height / 2)).save(f"qa/q{pi+1}a.png")
    p.get_pixmap(dpi=150, clip=pymupdf.Rect(0, r.height / 2, r.width, r.height)).save(f"qa/q{pi+1}b.png")
print("issues", issues)
sys.exit(1 if issues else 0)
