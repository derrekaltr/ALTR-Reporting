# -*- coding: utf-8 -*-
"""
The ALTR premium report design system as importable helpers. One builder script per report imports this,
writes content, and gets both outputs:

    template.html        the link: a scroll experience (reveal on scroll, count-ups, hover charts, fan spotlight)
    print-template.html  the PDF edition: fixed A4 pages composed by hand, running head, page X of Y, teasers

Everything visual (tokens, type, grain, chart look, page chrome) lives here and in the four CSS/JS files
next to it. A builder should only contain words and numbers. Start from report_skeleton.py.

Web helpers:   ch() big() story() fig() ichart() dual() ladder() ledger() spot() plan_step() closer() web_doc()
Print helpers: head() fnd() page() qtable() nums() warn() thread() print_doc()
Guards:        check_labels() check_braces()   run by write_outputs()

Rules the helpers enforce or expect (see CONTEXT/brand-and-pdf.md):
  two-part headings: plain part + <em>mint part</em>, each half under about 26 characters, one line each
  numbers never wrap (white-space:nowrap is set on every stat, caption and table figure)
  PDF stat labels: at most 28 characters in a 4-column row, 36 in a 3-column row (asserted)
  table note cells at most 40 characters (assert in your builder)
  no em dashes, no decorative emoji, no "Hover any bar" in print (wrap web-only words in <span class="web">)
"""
import html, json, os, re
from pathlib import Path

LIB = Path(__file__).resolve().parent
E = html.escape
def M(n):
    """Money. Whole dollars unless the value has cents."""
    try:
        n = float(n)
    except Exception:
        return str(n)
    return f"${n:,.2f}" if abs(n - round(n)) > 1e-6 else f"${n:,.0f}"
def N(n): return f"{n:,.0f}"
def PCT(n, d=1): return f"{n:.{d}f}%"

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,62..125,100..900;1,62..125,100..900&family=Spline+Sans+Mono:wght@400;500&display=swap" rel="stylesheet">')

# ------------------------------------------------------------------ charts (shared by web and print)
def ichart(cid, series, meta, w, h, xlabels, yfmt=None, show_val=None, hot=(), lw=None, fs=1.0):
    """Bar chart as inline SVG. series: values. meta: per-bar dicts {t,l,s} for the readout line (web only).
    hot: indexes drawn in mint (everything else dims to bone). fs: font scale (2.2 for 900x400 web, 2.8 for tall print charts)."""
    lw = lw or int(48 * fs)
    yfmt = yfmt or (lambda v: f"${v/1000:g}K" if v >= 1000 else f"${v:,.0f}")
    raw = max(max(series), 1)
    mx = next((c for c in [1, 5, 10, 25, 30, 50, 100, 200, 250, 500, 700, 1000, 2500, 5000, 6000, 10000, 20000, 25000, 40000, 50000, 60000, 100000, 150000, 250000] if c >= raw), raw)
    tp, bp = int(24 * fs), int(30 * fs); ch_ = h - tp - bp; x0 = lw; cw = w - x0 - 4; n = len(series); bw = cw / n
    o = [f'<svg class="ich" id="{cid}" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid meet" role="img">']
    for fr in (0.0, 0.5, 1.0):
        y = tp + ch_ - ch_ * fr
        o.append(f'<line x1="{x0}" y1="{y:.1f}" x2="{w-4}" y2="{y:.1f}" stroke="rgba(235,236,220,0.09)"/>')
        o.append(f'<text x="{x0-8}" y="{y+3.5*fs:.1f}" font-size="{10*fs:.0f}" fill="rgba(235,236,220,0.5)" text-anchor="end">{yfmt(mx*fr)}</text>')
    for i, v in enumerate(series):
        x = x0 + i * bw + bw * 0.2; bwid = bw * 0.6; bh = ch_ * v / mx; y = tp + ch_ - bh
        dim = " after" if (hot and i not in hot) else ""
        m = E(json.dumps(meta[i] if meta and i < len(meta) else {}))
        o.append(f'<rect class="bar{dim}" data-meta="{m}" x="{x:.1f}" y="{y:.1f}" width="{bwid:.1f}" height="{max(bh,1):.1f}" rx="1" style="transition-delay:{i*60}ms"/>')
        if show_val: o.append(f'<text x="{x0+i*bw+bw/2:.1f}" y="{y-8*fs:.1f}" font-size="{12*fs:.0f}" fill="#ebecdc" text-anchor="middle">{E(str(show_val[i]))}</text>')
        if xlabels and i < len(xlabels) and xlabels[i]:
            o.append(f'<text x="{x0+i*bw+bw/2:.1f}" y="{h-9*fs:.0f}" font-size="{10.5*fs:.0f}" fill="rgba(235,236,220,0.65)" text-anchor="middle">{E(xlabels[i])}</text>')
    o.append("</svg>"); return "".join(o)

def dual(desktop_svg, mobile_svg):
    """Two renderings of the same chart: .cv.d shows on desktop, .cv.m on phones."""
    return f'<div class="cv d">{desktop_svg}</div><div class="cv m">{mobile_svg}</div>'

def fig(svg, caption, default, extra=""):
    """A chart card with a readout line that follows hover/tap. default = {t,l,s} shown before interaction."""
    return (f'<figure class="fig rv"{extra}>{svg}<div class="readout"><span class="rt">{E(default["t"])}</span><span class="rl">{E(default["l"])}</span>'
            f'<span class="rs">{E(default["s"])}</span></div><figcaption>{caption}</figcaption></figure>')

def ladder(tickets, w=210, h=40, cap=200, label="$200", lit=None):
    """A mini bar strip: one bar per purchase, scaled to a dashed ceiling. lit: how many leading bars are solid mint."""
    n = max(len(tickets), 1); top = 13; base = h - 1; gap = 3.6; bw = min(26, (w - 64 - gap * (n - 1)) / n)
    lit = len(tickets) if lit is None else lit
    o = [f'<svg class="lad" viewBox="0 0 {w} {h}" preserveAspectRatio="xMinYMid meet"><line x1="0" y1="{top}" x2="{w-60}" y2="{top}" stroke="#b6f2e5" stroke-width=".8" stroke-dasharray="2 2.5" opacity=".7"/>'
         f'<text x="{w}" y="{top+10}" text-anchor="end" font-size="10.5" fill="#b6f2e5" font-family="Spline Sans Mono, monospace">{E(label)}</text>']
    for i, t in enumerate(tickets):
        bh = max(2, (base - top) * min(t, cap) / cap); x = i * (bw + gap)
        fill = "#b6f2e5" if i < lit else "rgba(182,242,229,.26)"
        o.append(f'<rect x="{x:.1f}" y="{base-bh:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx=".6" fill="{fill}"/>')
    return "".join(o) + "</svg>"

# ------------------------------------------------------------------ web blocks
def ch(num, kicker, title, cid):
    """Chapter header. title is HTML with the mint half in <em>."""
    return f'<header class="ch rv" id="{cid}"><div class="ch-meta"><span class="num">{num}</span><span class="kick">{E(kicker)}</span></div><h2>{title}</h2></header>'

def big(value, label):
    """An oversized numeral with a one-line label. value may contain <small>."""
    return f'<div class="big rv"><span class="bv">{value}</span><span class="bl">{E(label)}</span></div>'

def story(name, status, meta, body, quote, cite, more):
    """A fan story card that expands on click. quote+cite render as a blockquote; pass cite="" to render quote as a big figure instead."""
    q = f'<blockquote><p>{E(quote)}</p><cite>{E(cite)}</cite></blockquote>' if cite else f'<div class="sbig">{quote}</div>'
    return (f'<article class="story rv" tabindex="0"><div class="n"><h3>{E(name)}</h3><span class="st">{E(status)}</span></div><div class="h">{E(meta)}</div>'
            f'<p>{body}</p>{q}<div class="more"><div><p>{more}</p></div></div><span class="hint">More</span></article>')

def ledger(rows, header=("No.", "Fan", "Amount"), hi=(), cols="34px 1fr 96px"):
    """A fan ledger. rows: list of dicts {rank,name,sub,amount,extra:{...}}; extra keys feed the spotlight card and the
    tap-to-expand detail on phones (keys: last, why, move, or anything you wire in spot())."""
    h = f'<div class="lh"><span class="ln">{E(header[0])}</span><span class="lw">{E(header[1])}</span><span class="r">{E(header[2])}</span></div>'
    out = []
    for r in rows:
        ex = r.get("extra", {}); data = "".join(f' data-{k}="{E(str(v))}"' for k, v in ex.items())
        out.append(f'<div class="lr{" hi" if r.get("name") in hi or r.get("hi") else ""}" tabindex="0" data-rank="{r["rank"]}" data-name="{E(r["name"])}" data-net="{E(r["amount"])}"{data}>'
                   f'<span class="ln">{r["rank"]}</span><span class="lw"><b>{E(r["name"])}</b><i>{E(r.get("sub", ""))}</i></span><span class="r">{E(r["amount"])}</span>'
                   f'<div class="lx"><div><b>{E(r["amount"])}</b><span>{E(r.get("amount_label", "lifetime"))}</span></div><p>{E(ex.get("why", ""))}</p></div></div>')
    return f'<div class="ledger c" style="--lc:{cols}">{h}{"".join(out)}</div>'

def spot(first, fields):
    """The sticky spotlight card beside a ledger. fields: [(key,label)] matching ledger extra keys. first: the first row dict."""
    ex = first.get("extra", {})
    fs = "".join(f'<div class="sa"><b>{E(lab)}</b><span id="s-{k}">{E(str(ex.get(k, "")))}</span></div>' for k, lab in fields)
    return (f'<aside class="spot rv" id="spot"><div class="sr">Number <b id="s-rank">{first["rank"]}</b> by lifetime spend</div>'
            f'<h3 id="s-name">{E(first["name"])}</h3><div class="sh" id="s-handle">{E(first.get("sub", ""))}</div>'
            f'<div class="sg"><div><b id="s-net">{E(first["amount"])}</b><span>{E(first.get("amount_label", "lifetime"))}</span></div></div>{fs}'
            f'<div class="tip">Hover or tap a fan</div></aside>')

def plan_step(when, title, body, delay=0):
    d = f' style="transition-delay:{delay}s"' if delay else ""
    return f'<div class="step rv"{d}><div class="w">{E(when)}</div><h3>{E(title)}</h3><p>{body}</p></div>'

def closer(number, small, text, sig):
    """The one mint panel, at the very end. text is HTML, the emphasised clause in <em>."""
    return (f'<div class="close rv"><img src="__MARK__" alt="" aria-hidden="true"><div class="cb"><span>{number}</span><small>{E(small)}</small></div>'
            f'<div><p>{text}</p><div class="sig">{E(sig)}</div></div></div>')

def hero(name_letters, hook_lines, sub, who, pdf, pdf_download_name, mint_last=True):
    """The opening screen. name_letters: the name as a string, revealed letter by letter (the last char turns mint)."""
    letters = "".join(f"<span>{E(c)}</span>" for c in name_letters)
    hooks = "".join(f'<span>{"".join(f"<b>{E(l)}</b>" for l in pair)}</span>' for pair in hook_lines)
    return (f'<div class="hero"><h1>{letters}</h1><div><p class="hook">{hooks}</p><p class="sub">{sub}</p>'
            f'<div class="who">{who}</div><a class="dl-inline" href="{pdf}" download="{pdf_download_name}">Download the PDF</a></div>'
            f'<div class="cue"><i></i>Scroll</div></div>')

def method(items, label="What we read"):
    """The 'what we read' strip under the hero: [(value,label)], five items fit."""
    return f'<div class="method rv"><span class="ml">{E(label)}</span>' + "".join(f'<div class="m"><b>{E(str(v))}</b><span>{E(l)}</span></div>' for v, l in items) + "</div>"

def toc(entries, label="Inside"):
    """entries: [(num, title, anchor)]"""
    return f'<nav class="toc rv"><span class="ml">{E(label)}</span>' + "".join(f'<a href="#{a}"><b>{n}</b><span>{E(t)}</span></a>' for n, t, a in entries) + "</nav>"

def side_nav(entries, top_label):
    return (f'<nav id="nav"><a href="#top"><span>{E(top_label)}</span><i></i></a>' +
            "".join(f'<a href="#{a}"><span>{E(t)}</span><i></i></a>' for _, t, a in entries) + "</nav>")

def web_doc(title, mast_line, body_html, pdf, pdf_download_name, nav_entries, top_label, extra_css="", spot_fields=None, extra_js=""):
    """Assemble template.html. spot_fields: the ledger extra keys the spotlight card updates, e.g. ['last','why']."""
    base = (LIB / "creator_base.css").read_text(encoding="utf-8") + (LIB / "web_extra.css").read_text(encoding="utf-8")
    base += "\nh2{max-width:26ch}h2 em{display:block}\n.bv,.method .m b,.spot .sg b,.readout .rl,.ledger .r,.big .bv{white-space:nowrap}\n.fig figcaption{text-wrap:balance}\n.ledger .lh,.ledger .lr{grid-template-columns:var(--lc,34px 1fr 96px)}\n"
    js = (LIB / "creator_base.js").read_text(encoding="utf-8")
    js = js.replace("if(cur==='c4')cur='c3';", "")
    keys = ["rank", "name", "handle", "net"] + list(spot_fields or [])
    js = js.replace("['rank','name','handle','net60','net30','last','days','pers','angle']", json.dumps(keys).replace('"', "'"))
    js = js.replace("f.net60.textContent=d.net60;f.net30.textContent=d.net30;f.last.textContent=d.last;f.days.innerHTML=d.days+'<small style=\"font-size:.5em\"> days</small>';f.pers.textContent=d.pers;f.angle.textContent=d.angle;",
                    "f.net.textContent=d.net;" + "".join(f"if(f.{k})f.{k}.textContent=d.{k}||'';" for k in (spot_fields or [])))
    js = js.replace("f.handle.textContent=d.handle;", "f.handle.textContent=d.handle||d.sub||'';")
    js = js.replace("document.querySelectorAll('.fig').forEach(function(f){var svg=f.querySelector('.ich');if(!svg)return;",
                    "document.querySelectorAll('.fig .ich').forEach(function(svg){var f=svg.closest('.fig');")
    js = js.replace("</script>", "document.querySelectorAll('.whales .lr[data-name]').forEach(function(r){r.addEventListener('click',function(){if(!window.matchMedia('(max-width:920px)').matches)return;var was=r.classList.contains('open');document.querySelectorAll('.whales .lr.open').forEach(function(x){x.classList.remove('open')});if(!was)r.classList.add('open')})});\n" + extra_js + "\n</script>")
    head = ('<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><meta name="robots" content="noindex, nofollow"><meta name="theme-color" content="#1d1d1b">'
            f'<title>{E(title)}</title>' + FONTS)
    top = (f'<div id="prog"></div><div id="glow"></div>{side_nav(nav_entries, top_label)}'
           f'<div class="dl-wrap"><a class="dl-btn" href="{pdf}" download="{pdf_download_name}">Download PDF</a></div>'
           f'<div class="page" id="top"><header class="mast"><img src="__LOGO__" alt="ALTR"><span>{E(mast_line)}</span></header>')
    return f'<!DOCTYPE html><html lang="en"><head>{head}<style>{base}{extra_css}</style></head><body>{top}{body_html}</div>{js}</body></html>'

# ------------------------------------------------------------------ print blocks
PX = """
.cover .nums b{font-size:26pt}.cover .nums span{font-size:9pt}
.cv-top .hook{margin-top:5mm;font-weight:300;font-size:18pt;line-height:1.2;letter-spacing:-.02em}.cv-top .hook em{display:block;font-style:normal;color:var(--mint)}
.cover .ghost{position:absolute;right:-26mm;top:18mm;width:150mm;opacity:.045}
.foot .nx{color:var(--mint)}
.lad{display:block;width:100%;height:auto;margin-top:2mm;max-width:80mm}
.lcap{margin-top:1mm;font-family:var(--mono);font-size:6.8pt;color:var(--bone3);white-space:nowrap}.lcap b{font-family:var(--sans);font-weight:300;font-size:12pt;color:var(--bone);margin-right:1.6mm}
.know{display:grid;grid-template-columns:repeat(3,1fr);gap:4mm}
.kn{border:1px solid var(--line);border-radius:2mm;padding:4mm 4.5mm 3.5mm;display:flex;flex-direction:column}
.kn h4{font-weight:300;font-size:15pt;letter-spacing:-.02em;line-height:1;margin-top:1.8mm}.kn p{margin-top:2mm;font-size:8.8pt;color:var(--bone2);line-height:1.5}
.asks4{display:grid;grid-template-columns:repeat(2,1fr);gap:3.5mm}
.a4{border:1px solid var(--line);border-radius:2mm;padding:3.6mm 4mm}.a4 h4{font-weight:500;font-size:10.5pt;margin-top:1mm}.a4 p{margin-top:1.4mm;font-size:9pt;color:var(--bone2);line-height:1.45}
.warnp{border:1px solid rgba(182,242,229,.45);background:var(--wash);border-radius:2mm;padding:4mm 5mm}.warnp h4{font-weight:500;font-size:11pt}.warnp p{margin-top:1.5mm;font-size:9pt;color:var(--bone2);line-height:1.5}.warnp p + p{margin-top:2mm}
.qt{width:100%;border-collapse:collapse}.qt th{font-family:var(--mono);font-weight:400;font-size:6.8pt;letter-spacing:.1em;text-transform:uppercase;color:var(--bone3);text-align:left;padding:0 1.6mm 2mm;border-bottom:1px solid var(--line)}
.qt td{padding:2.2mm 1.6mm;border-bottom:1px solid var(--soft);font-size:9pt;vertical-align:top;line-height:1.45}.qt .n{font-family:var(--mono);font-size:7.5pt;color:var(--mint);width:6mm}
.qt .fan b{display:block;font-weight:500;font-size:9.6pt;white-space:nowrap}.qt .fan i{display:block;font-style:normal;font-family:var(--mono);font-size:6.6pt;color:var(--bone3);line-height:1.35}
.qt .num{text-align:right;font-family:var(--mono);white-space:nowrap}
.qt .bar span{display:block;width:16mm;height:1.3mm;border-radius:.7mm;background:rgba(235,236,220,.07)}.qt .bar i{display:block;height:100%;border-radius:.7mm;background:linear-gradient(to right,rgba(182,242,229,.4),#b6f2e5)}
.body > .lbl{margin-bottom:0;flex:0 0 auto}.qt + .lbl{margin-top:5mm}.qt{flex:0 0 auto}
.two{display:grid;grid-template-columns:1fr 1fr;gap:4mm;flex:0 0 auto}
.chips{display:flex;flex-wrap:wrap;gap:2.4mm}
.chips span{border:1px solid var(--line);border-radius:12mm;padding:1.8mm 4mm;font-size:8.8pt;color:var(--bone2);white-space:nowrap}
.chips span.k{border-color:rgba(182,242,229,.45);color:var(--bone)}
.pq{border-left:1px solid var(--mint);padding-left:4mm;font-style:italic;font-weight:300;font-size:12.5pt;line-height:1.45;color:var(--bone)}
.pq cite{display:block;margin-top:1.5mm;font-style:normal;font-family:var(--mono);font-size:7pt;letter-spacing:.14em;text-transform:uppercase;color:var(--bone3)}
.thread{border-top:1px solid var(--line);padding:3.6mm 0;display:grid;grid-template-columns:46mm 1fr;gap:6mm}
.thread h4{font-weight:300;font-size:16pt;letter-spacing:-.02em;line-height:1}.thread h4.sm{font-size:12pt;white-space:nowrap}
.thread .meta{margin-top:1.6mm;font-family:var(--mono);font-size:6.8pt;color:var(--bone3);line-height:1.6}
.thread p{font-size:9.2pt;color:var(--bone2);line-height:1.52}.thread p + p{margin-top:1.8mm}
.thread .q{margin-top:1.8mm;border-left:1px solid var(--mint);padding-left:3mm;font-style:italic;color:var(--bone);font-size:10pt;line-height:1.4}
.acct{display:grid;grid-template-columns:1fr 1fr;gap:4mm}
.ac{border:1px solid var(--line);border-radius:2mm;padding:4mm 4.5mm}
.ac .tag{font-family:var(--mono);font-size:6.8pt;letter-spacing:.14em;text-transform:uppercase;color:var(--mint)}
.ac h4{margin-top:1.5mm;font-weight:300;font-size:16pt;letter-spacing:-.02em;white-space:nowrap}
.ac .fig2{margin-top:1.5mm;font-family:var(--mono);font-size:7.4pt;color:var(--bone3)}
.ac p{margin-top:2.5mm;font-size:8.8pt;color:var(--bone2);line-height:1.5}
.nums b,.find b,.qt .num,.kn h4,.chart .cap,.foot span,.lcap,.ac h4{white-space:nowrap}
.body{gap:4.5mm}
.body > *{flex:0 0 auto;min-height:0}
.body > .find{margin:3mm 0}.body > .find > div{padding:2.8mm 0}
.chart,.hd,.nums,.warnp,.two,.acct,.asks4,.know,.wk,.qt,.close,.letter,.toc{flex:0 0 auto}
"""

def head(num, kicker, title, line):
    """Page header: big number, kicker, two-part h2 (mint half in <em>), one-line standfirst."""
    return f'<div class="hd"><div class="hn"><b>{num}</b><span>{E(kicker)}</span></div><div class="ht"><h2>{title}</h2><p>{line}</p></div></div>'

def fnd(value, text, hi=False):
    """A finding row for the short-version page: numeral + one sentence."""
    return '<div%s><b>%s</b><p>%s</p></div>' % (' class="hi"' if hi else '', value, text)

def nums(items, cols=4):
    """A row of stats. items: [(value, label)]. Labels are length-checked by check_labels()."""
    return f'<div class="nums c{cols}">' + "".join(f'<div><b>{v}</b><span>{E(l)}</span></div>' for v, l in items) + "</div>"

def warn(title, *paras):
    return f'<div class="warnp"><h4>{E(title)}</h4>' + "".join(f"<p>{p}</p>" for p in paras) + "</div>"

def thread(name, meta_lines, paras, quote=None):
    """A fan thread block: name and mono meta on the left, prose and one pulled quote on the right."""
    q = f'<div class="q">{E(quote)}</div>' if quote else ""
    ps = "".join(f"<p>{p}</p>" for p in paras)
    return f'<div class="thread"><div><h4>{E(name)}</h4><div class="meta">{"<br>".join(E(m) for m in meta_lines)}</div></div><div>{ps[:ps.find("</p>")+4] if quote else ps}{q}{ps[ps.find("</p>")+4:] if quote else ""}</div></div>'

QH = '<thead><tr><th>No.</th><th>Fan, and the note left on them</th><th></th><th class="num">Lifetime</th><th>What is happening</th></tr></thead>'
def qtable(rows, maxv, header=QH):
    """rows: (name, rank, amount, note, status). note/status at most 40 chars."""
    body = "".join(f'<tr><td class="n">{r[1]}</td><td class="fan"><b>{E(r[0])}</b><i>{E(r[3])}</i></td>'
                   f'<td class="bar"><span><i style="width:{r[2]/maxv*100:.0f}%"></i></span></td><td class="num">{M(r[2])}</td><td>{E(r[4])}</td></tr>' for r in rows)
    return f'<table class="qt">{header}<tbody>{body}</tbody></table>'

class PrintDoc:
    """Collects A4 pages. chapters: {n: running-head text}; teasers: {n: footer teaser 'Next, ...'}."""
    def __init__(self, title, for_whom, chapters, teasers, total):
        self.title, self.for_whom, self.ch, self.nx, self.total, self.pages = title, for_whom, chapters, teasers, total, []
    def page(self, n, body, cls=""):
        ghost = '<img class="ghost" src="__GHOST__" alt="">' if cls == "cover" else ""
        self.pages.append(f'<section class="pg {cls}">{ghost}<header class="run"><img src="__LOGO__" alt="ALTR"><span>{self.for_whom}, {E(self.ch[n])}</span></header><div class="body">{body}</div>'
                          f'<footer class="foot"><span>Prepared by ALTR for {self.for_whom}</span><span class="nx">{E(self.nx[n])}</span><span>{n:02d} / {self.total:02d}</span></footer></section>')
    def html(self, extra_css=""):
        assert len(self.pages) == self.total, f"declared {self.total} pages, built {len(self.pages)}"
        pcss = (LIB / "print_base.css").read_text(encoding="utf-8")
        return (f'<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>{E(self.title)}</title>{FONTS}'
                f"<style>{pcss}{PX}{extra_css}</style></head><body>{''.join(self.pages)}</body></html>")

# ------------------------------------------------------------------ guards + output
def check_labels(print_html):
    for cls, lim in (("c4", 28), ("c3", 36)):
        for row in re.findall(r'<div class="nums ' + cls + r'">(.*?)</div></div>', print_html, re.S):
            for lab in re.findall(r"<span>(.*?)</span>", row):
                assert len(lab) <= lim, f"stat label too long for {cls} ({len(lab)}>{lim}): {lab}"

def check_braces(*htmls):
    for h in htmls:
        m = re.search(r"\{[A-Za-z_][A-Za-z_0-9]*\}", h)
        assert not m, f"un-interpolated placeholder in output: {m.group(0)} (an inner string needs an f prefix)"

def check_dashes(*htmls):
    for h in htmls:
        assert "—" not in h and " -- " not in h, "em dash found: rewrite the sentence"

def write_outputs(web_html, print_html, pdf_name, title):
    check_labels(print_html); check_braces(web_html, print_html); check_dashes(web_html, print_html)
    Path("template.html").write_text(web_html, encoding="utf-8")
    Path("print-template.html").write_text(print_html, encoding="utf-8")
    Path("report.json").write_text(json.dumps({"pdf": pdf_name, "title": title}, indent=1), encoding="utf-8")
    print(f"built template.html + print-template.html (pdf will be {pdf_name}). next: python3 ../../lib/build.py")
