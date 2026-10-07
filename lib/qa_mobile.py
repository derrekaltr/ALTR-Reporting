# -*- coding: utf-8 -*-
"""
Phone QA for the link, with real device emulation (touch, DPR 2, 390px) through the installed Chrome via Playwright.

    python3 ../../lib/qa_mobile.py                 # index.html in the current folder
    python3 ../../lib/qa_mobile.py https://...     # a deployed link
    python3 ../../lib/qa_mobile.py index.html 430  # another width

Reports anything wider than the viewport, text clipped inside its box, text under 11px, SVG text under 9px tall,
and tap targets under 36px. Writes qa/m<width>-full.png, the full-page screenshot. Why not plain headless
Chrome screenshots: headless Chrome enforces about a 500px minimum layout width, so a 390px shot is really a
cropped 504px layout and shows false overflow.
Needs: python3 -m pip install playwright  (uses the installed Chrome, no browser download required).
"""
import sys, os, json
from pathlib import Path
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit("playwright missing: python3 -m pip install playwright")
arg = sys.argv[1] if len(sys.argv) > 1 else "index.html"
url = arg if arg.startswith("http") else Path(arg).resolve().as_uri()
W = int(sys.argv[2]) if len(sys.argv) > 2 else 390
os.makedirs("qa", exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    ctx = b.new_context(viewport={"width": W, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True,
                        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1")
    pg = ctx.new_page(); pg.goto(url); pg.wait_for_timeout(2500)
    H = pg.evaluate("document.documentElement.scrollHeight")
    for y in range(0, H, 500):
        pg.evaluate(f"window.scrollTo(0,{y})"); pg.wait_for_timeout(60)
    pg.wait_for_timeout(1500); pg.evaluate("window.scrollTo(0,0)"); pg.wait_for_timeout(300)
    rep = pg.evaluate("""() => {
      const vw = document.documentElement.clientWidth, out = [];
      out.push({docScrollWidth: document.documentElement.scrollWidth, vw});
      document.querySelectorAll('body *').forEach(el => {
        const r = el.getBoundingClientRect(); if (!r.width) return;
        const cs = getComputedStyle(el); if (cs.position === 'fixed') return;
        if (r.right > vw + 1 && !el.closest('.fig-scroll')) out.push({over: el.tagName + '.' + el.className, right: Math.round(r.right), txt: (el.textContent||'').trim().slice(0,40)});
        if (el.children.length === 0 && el.scrollWidth > el.clientWidth + 2 && cs.overflow !== 'visible') out.push({clip: el.tagName + '.' + el.className, txt: (el.textContent||'').trim().slice(0,40)});
      });
      const small = []; document.querySelectorAll('body *').forEach(el => {
        if (el.children.length) return; const t=(el.textContent||'').trim(); if(!t) return;
        const r = el.getBoundingClientRect(); if(!r.width) return;
        const fs = parseFloat(getComputedStyle(el).fontSize); if (fs < 11 && el.tagName !== 'text' && el.tagName !== 'tspan') small.push(fs + 'px ' + t.slice(0,30));
      });
      document.querySelectorAll('svg text').forEach(t => { const r=t.getBoundingClientRect(); if (r.width && r.height < 9) small.push('svg ' + r.height.toFixed(1) + 'px ' + t.textContent.slice(0,20)); });
      out.push({smallCount: small.length, small: small.slice(0,25)});
      const taps=[]; document.querySelectorAll('a,button,[tabindex]').forEach(el=>{const r=el.getBoundingClientRect(); if(r.width && (r.height<36)) taps.push(el.tagName+' '+Math.round(r.width)+'x'+Math.round(r.height)+' '+(el.textContent||'').trim().slice(0,20));});
      out.push({smallTaps: taps.slice(0,15), nSmallTaps: taps.length});
      return out; }""")
    print(json.dumps(rep, indent=1, ensure_ascii=False)[:6000])
    pg.screenshot(path=f"qa/m{W}-full.png", full_page=True)
    b.close()
print(f"screenshot qa/m{W}-full.png. docScrollWidth must equal vw; small/clip/over lists should be empty.")
