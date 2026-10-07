# -*- coding: utf-8 -*-
"""Vale. Private top-fan review written TO Vale (creator-facing).
One source renders both the scroll experience (screen) and the five-page A4 PDF (print CSS, .pg wrappers).
Run: python build_creator.py && python build.py"""
import json, html, datetime as dt, collections, os
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
E = html.escape
M = lambda n: f"${n:,.0f}"
ET = dt.timezone(dt.timedelta(hours=-4))
P = json.load(open("data/pack.json", encoding="utf-8"))
C = json.load(open("data/cohort.json", encoding="utf-8")); co = {w["id"]: w for w in C["cohort"]}
tx = [t for t in json.load(open("data/transactions150.json", encoding="utf-8")) if t["status"] not in ("undo", "pending_return")]
def ts(s): return dt.datetime.fromisoformat(s)
def md(iso): return ts(iso).astimezone(ET).strftime("%b %-d") if os.name != "nt" else ts(iso).astimezone(ET).strftime("%b %#d")

W = P["windows"]; cur, prev = W[4], W[3]
board = P["board"]; ids = {b["id"] for b in board}
top_net = sum(b["net"] for b in board)
quiet = [b for b in board if b["status"] in ("Cooling", "Lapsed")]; quiet_net = sum(b["net"] for b in quiet)
og = co[307055077]; ogw = P["og_windows"]; ogt = P["og_tickets_by_window"]
paying = len({(t.get("user") or {}).get("id") for t in tx})
n_cap = sum(1 for t in tx if (t.get("user") or {}).get("id") in ids and t["type"] in ("message", "tip") and t["amount"] >= 199)
val200 = sum(1 for t in tx if (t.get("user") or {}).get("id") == 31836535 and t["amount"] >= 199)

# price bands for top fans
bands = [("Under $25", 0, 25), ("$25 to $49", 25, 50), ("$50 to $99", 50, 100), ("$100 to $149", 100, 150), ("$150 to $198", 150, 199), ("$199 to $200", 199, 10**6)]
bn = collections.OrderedDict((b[0], [0, 0.0]) for b in bands)
for t in tx:
    if (t.get("user") or {}).get("id") in ids and t["type"] in ("message", "tip"):
        for lab, lo, hi in bands:
            if lo <= t["amount"] < hi: bn[lab][0] += 1; bn[lab][1] += t["net"]; break
band_tot = sum(v[1] for v in bn.values()); cap_share = round(bn["$199 to $200"][1] / band_tot * 100)
hrs = [P["hours"].get(str(h), 0) for h in range(24)]; hsum = sum(hrs)
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]; dv = [P["dows"].get(d, 0) for d in days]; dsum = sum(dv)
fri = round(dv[4] / dsum * 100)

# ------------------------------------------------------------------ charts
def ichart(cid, series, meta, w, h, xlabels, every=1, yfmt=None, show_val=None, stack=None, hot=(), lw=None, fs=1.0):
    lw = lw or int(48 * fs)
    yfmt = yfmt or (lambda v: f"${v/1000:g}K" if v >= 1000 else f"${v:,.0f}")
    tot = [series[i] + (stack[i] if stack else 0) for i in range(len(series))]
    raw = max(max(tot), 1)
    mx = next(c for c in [10, 20, 25, 40, 50, 100, 200, 250, 500, 1000, 1500, 2000, 2500, 3000, 4000, 5000, 6000, 8000, 10000, 15000, 20000, 25000, 30000, 40000, 50000] + [raw] if c >= raw)
    tp, bp = int(24 * fs), int((44 if xlabels and any('|' in str(x) for x in xlabels) else 30) * fs); ch_ = h - tp - bp; x0 = lw; cw = w - x0 - 4; n = len(series); bw = cw / n
    o = [f'<svg class="ich" id="{cid}" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid meet" role="img">']
    for fr in (0.0, 0.5, 1.0):
        y = tp + ch_ - ch_ * fr
        o.append(f'<line x1="{x0}" y1="{y:.1f}" x2="{w-4}" y2="{y:.1f}" stroke="rgba(235,236,220,0.09)"/>')
        o.append(f'<text x="{x0-8}" y="{y+3.5*fs:.1f}" font-size="{10*fs:.0f}" fill="rgba(235,236,220,0.5)" text-anchor="end">{yfmt(mx*fr)}</text>')
    for i, v in enumerate(series):
        x = x0 + i * bw + bw * 0.18; bwid = bw * 0.64; bh = ch_ * v / mx; y = tp + ch_ - bh
        dim = " after" if (hot and i not in hot) else ""
        o.append(f'<rect class="bar{dim}" data-meta="{E(json.dumps(meta[i]))}" x="{x:.1f}" y="{y:.1f}" width="{bwid:.1f}" height="{max(bh,1):.1f}" rx="1" style="transition-delay:{i*40}ms"/>')
        if stack:
            sh = ch_ * stack[i] / mx
            o.append(f'<rect class="bar after" data-meta="{E(json.dumps(meta[i]))}" x="{x:.1f}" y="{y-sh:.1f}" width="{bwid:.1f}" height="{max(sh,0):.1f}" rx="1" style="transition-delay:{i*40+120}ms"/>')
        if show_val:
            yv = tp + ch_ - ch_ * tot[i] / mx - 8 * fs
            o.append(f'<text x="{x0+i*bw+bw/2:.1f}" y="{yv:.1f}" font-size="{11*fs:.0f}" fill="#ebecdc" text-anchor="middle">{show_val[i]}</text>')
        if xlabels and i % every == 0:
            parts = xlabels[i].split("|"); cx = x0 + i*bw + bw/2
            if len(parts) == 1:
                o.append(f'<text x="{cx:.1f}" y="{h-9*fs:.0f}" font-size="{10*fs:.0f}" fill="rgba(235,236,220,0.6)" text-anchor="middle">{E(parts[0])}</text>')
            else:
                o.append(f'<text x="{cx:.1f}" y="{h-bp+12*fs:.0f}" font-size="{10*fs:.0f}" fill="rgba(235,236,220,0.6)" text-anchor="middle"><tspan x="{cx:.1f}">{E(parts[0])}</tspan><tspan x="{cx:.1f}" dy="{11*fs:.0f}">{E(parts[1])}</tspan></text>')
    o.append("</svg>"); return "".join(o)

def dual(d, m):
    return f'<div class="cv d">{d}</div><div class="cv m">{m}</div>'
short = [w["from"] for w in W]
def fig(svg, caption, default, extra=""):
    return (f'<figure class="fig rv"{extra}>{svg}<div class="readout"><span class="rt">{E(default["t"])}</span><span class="rl">{E(default["l"])}</span>'
            f'<span class="rs">{E(default["s"])}</span></div><figcaption>{caption}</figcaption></figure>')

wl = [f'{w["from"]} to {w["to"]}' for w in W]
meta_layer = [{"t": wl[i], "l": f'{M(W[i]["total"])} earned', "s": f'{W[i]["n500"]} fans spent $500 or more and brought in {M(W[i]["rev500"])}. {W[i]["buyers"]} fans bought in total.'} for i in range(5)]
fig_layer_d = ichart("c-layer", [w["rev500"] for w in W], meta_layer, 900, 280, wl, fs=1.3, stack=[w["total"] - w["rev500"] for w in W], show_val=[f'${w["total"]/1000:.1f}K' for w in W])
fig_layer = dual(fig_layer_d, ichart("c-layer-m", [w["rev500"] for w in W], meta_layer, 420, 300, short, fs=1.45, lw=58, stack=[w["total"] - w["rev500"] for w in W], show_val=[f'${w["total"]/1000:.0f}K' for w in W]))
meta_og = [{"t": wl[i], "l": f"{M(ogw[i])} from OG Ry", "s": f'{ogt[i]["n"]} purchases, typically ${ogt[i]["median"]:.0f} each' + (f', {ogt[i]["n200"]} at $200' if ogt[i]["n200"] else "")} for i in range(5)]
fig_og_d = ichart("c-og", ogw, meta_og, 900, 520, [w["from"] for w in W], fs=2.6, hot=(2,), show_val=[f"${v/1000:.1f}K" if v >= 1000 else f"${v}" for v in ogw])
fig_og = dual(fig_og_d, ichart("c-og-m", ogw, meta_og, 420, 300, short, fs=1.45, lw=58, hot=(2,), show_val=[f"${v/1000:.1f}K" if v >= 1000 else f"${v}" for v in ogw]))
bl = list(bn.keys()); bshort = ["Under|$25", "$25|to $49", "$50|to $99", "$100|to $149", "$150|to $198", "$199|to $200"]
meta_band = [{"t": k, "l": f"{round(bn[k][1]/band_tot*100)} percent of what your top fans spend", "s": f"{bn[k][0]} purchases, {M(bn[k][1])}"} for k in bl]
fig_band_d = ichart("c-band", [bn[k][1] for k in bl], meta_band, 900, 520, bshort, fs=2.5, hot=(5,), show_val=[f"{round(bn[k][1]/band_tot*100)}%" for k in bl])
fig_band = dual(fig_band_d, ichart("c-band-m", [bn[k][1] for k in bl], meta_band, 420, 330, bshort, fs=1.3, lw=52, hot=(5,), show_val=[f"{round(bn[k][1]/band_tot*100)}%" for k in bl]))
def hname(h): return f"{(h % 12) or 12}{'am' if h < 12 else 'pm'}"
top4 = sorted(range(24), key=lambda h: -hrs[h])[:4]
meta_h = [{"t": f"{hname(h)} to {hname((h+1)%24)}, Eastern", "l": f"{hrs[h]/hsum*100:.1f} percent of what your top fans spend", "s": "One of your four strongest hours." if h in top4 else ""} for h in range(24)]
hl = [hname(h) if h % 3 == 0 else "" for h in range(24)]
fig_hours_d = ichart("c-hours", hrs, meta_h, 900, 560, hl, fs=2.8, hot=tuple(top4), yfmt=lambda v: f"{v/hsum*100:.0f}%")
fig_hours = dual(fig_hours_d, ichart("c-hours-m", hrs, meta_h, 420, 280, [hname(h) if h % 6 == 0 else "" for h in range(24)], fs=1.45, lw=52, hot=tuple(top4), yfmt=lambda v: f"{v/hsum*100:.0f}%"))
meta_d = [{"t": d, "l": f"{dv[i]/dsum*100:.0f} percent of what your top fans spend", "s": "Your biggest day by far." if i == 4 else ""} for i, d in enumerate(days)]
fig_days_d = ichart("c-days", dv, meta_d, 900, 560, days, fs=2.8, hot=(4,), yfmt=lambda v: f"{v/dsum*100:.0f}%", show_val=[f"{v/dsum*100:.0f}%" for v in dv])
fig_days = dual(fig_days_d, ichart("c-days-m", dv, meta_d, 420, 280, days, fs=1.45, lw=52, hot=(4,), yfmt=lambda v: f"{v/dsum*100:.0f}%", show_val=[f"{v/dsum*100:.0f}%" for v in dv]))

# ------------------------------------------------------------------ pieces
def ch(num, kicker, title, cid, sm=False):
    return f'<header class="ch rv{" sm" if sm else ""}" id="{cid}"><div class="ch-meta"><span class="num">{num}</span><span class="kick">{E(kicker)}</span></div><h2>{title}</h2></header>'
def big(v, label, count=None, prefix="", suffix=""):
    dc = f' data-count="{count}" data-prefix="{prefix}" data-suffix="{suffix}"' if count is not None else ""
    return f'<div class="big rv"><span class="bv"{dc}>{v}</span><span class="bl">{E(label)}</span></div>'

def next_step(b):
    special = {307055077: "Your number one. One planned night a week from next week, built the way July was.",
               61293007: "New this month, with the biggest night of it. A personal follow-up on that night, today.",
               297584968: "Their subscription ends Sep 18 without renewal. A personal note from you before it does.",
               497409744: "Their subscription ends Sep 18 without renewal. A personal note from you before it does.",
               31836535: "Left on Aug 9 after seeing everything on your menu. Invited back with a return offer this week."}
    if b["id"] in special: return special[b["id"]]
    if b["flag"].startswith("Chat unavailable"): return "Their subscription has ended. We invite them back with a return offer this week."
    if b["status"] == "Active": return "Buying right now. They hear from you personally and never from a mass message."
    if b["status"] == "Warm": return "A warm hello this week that picks up your last real conversation."
    return "Gone quiet. A personal message with nothing for sale in it, sent when they usually buy."

top24 = board[:24]
def rows(items, off):
    out = []
    for i, b in enumerate(items):
        f = co[b["id"]]; n = off + i + 1; bs = f["best_session"]
        best = f'{M(bs["gross"])} on {md(bs["start"])}' if bs else "n/a"
        last = md(f["last_buy"]) if f["last_buy"] else "n/a"
        out.append(f'<div class="lr{" hi" if b["status"] == "Active" else ""}" tabindex="0" data-rank="{n:02d}" data-name="{E(b["name"])}" data-handle="@{E(b["user"])}" '
                   f'data-net="{M(b["net"])}" data-net30="{M(b["net30"])}" data-last="{last}" data-best="{E(best)}" data-angle="{E(next_step(b))}">'
                   f'<span class="ln">{n:02d}</span><span class="lw"><b>{E(b["name"])}</b><i>@{E(b["user"])}</i></span><span class="r">{M(b["net"])}</span><span class="r">{last}</span>'
                   f'<div class="lx"><div><b>{M(b["net30"])}</b><span>last thirty days</span></div><div><b>{M(bs["gross"]) if bs else "n/a"}</b><span>best night{", " + md(bs["start"]) if bs else ""}</span></div><p>{E(next_step(b))}</p></div></div>')
    return "".join(out)
LH = '<div class="lh"><span class="ln"></span><span class="lw">Fan</span><span class="r">150 days</span><span class="r">Last buy</span></div>'
ledger_a = f'<div class="ledger c">{LH}{rows(top24[:12], 0)}</div>'
ledger_b = f'<div class="ledger c">{LH}{rows(top24[12:], 12)}</div>'
b0 = top24[0]; f0 = co[b0["id"]]
spot = dict(rank="01", name=b0["name"], handle="@" + b0["user"], net=M(b0["net"]), net30=M(b0["net30"]), last=md(f0["last_buy"]),
            best=f'{M(f0["best_session"]["gross"])} on {md(f0["best_session"]["start"])}', angle=next_step(b0))

def story(name, status, meta, body, quote, cite, more):
    q = (f'<blockquote><p>{E(quote)}</p><cite>{E(cite)}</cite></blockquote>' if cite else f'<div class="sbig">{quote}</div>')
    return (f'<article class="story rv" tabindex="0"><div class="n"><h3>{E(name)}</h3><span class="st">{E(status)}</span></div><div class="h">{E(meta)}</div>'
            f'<p>{body}</p>{q}<div class="more"><div><p>{more}</p></div></div><span class="hint">More</span></article>')

asaf, jg, dw, val = co[75127224], co[458928755], co[9349559], co[31836535]

BASE = open("creator_base.css", encoding="utf-8").read()
EXTRA = r"""
.sbig{margin-top:18px;font-weight:200;font-size:46px;letter-spacing:-.04em;line-height:1}.sbig small{font-size:15px;font-weight:400;letter-spacing:0;color:var(--bone3);margin-left:10px}
.toc{display:grid;grid-template-columns:auto repeat(6,1fr);align-items:stretch;border-bottom:1px solid var(--line)}
.toc .ml{font-family:var(--mono);font-size:10px;letter-spacing:.18em;text-transform:uppercase;color:var(--mint);padding:22px 30px 22px 0;align-self:center}
.toc a{padding:20px 18px;border-left:1px solid var(--soft);text-decoration:none;color:var(--bone);transition:background .3s}.toc a:hover{background:var(--wash)}
.toc a b{display:block;font-family:var(--mono);font-weight:400;font-size:10px;color:var(--mint);letter-spacing:.14em}.toc a span{display:block;margin-top:6px;font-size:14px;line-height:1.25}
.fig .legend{display:flex;gap:18px;margin-top:10px;font-family:var(--mono);font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--bone3)}.legend i{display:inline-block;width:9px;height:9px;margin-right:7px;vertical-align:-1px;border-radius:1px}
.spot .sg b small{font-size:.5em}
.pg{display:contents}
p,h2,h3,li,.bl,.lead,blockquote p,figcaption,.rs,.rl{text-wrap:pretty}
.cv.m{display:none}
.dl-inline{display:none}
.lx{display:none}
.t-t{display:none}
@media (hover:none){.t-h{display:none}.t-t{display:inline}}
@media(max-width:920px){
 .cv.d{display:none}.cv.m{display:block}
 .spot{display:none}
 .whales{margin-top:28px}
 .whales .lh,.whales .lr{grid-template-columns:24px minmax(0,1fr) 66px 64px!important;gap:6px!important;padding:13px 4px!important}
 .whales .lr{cursor:pointer;position:relative}
 .whales .lr::after{content:"+";position:absolute;right:-2px;top:13px;font-family:var(--mono);font-size:12px;color:var(--bone3);display:none}
 .whales .lw b{font-size:15px}.whales .lw i{font-size:11px}.whales .r{font-size:13px}.ln{font-size:11px}
 .lh{font-size:11px;letter-spacing:.12em}
 .whales .lh .r{font-size:10.5px!important;letter-spacing:.04em!important;white-space:nowrap}
 .story .h{font-size:12px}.story .hint{font-size:11px}.close .sig{font-size:11px}
 .lr.open{background:var(--wash2)}
 .lr.open .lx{display:grid;grid-column:1/-1;grid-template-columns:1fr 1fr;gap:10px 14px;padding:12px 0 4px 36px;border-top:1px solid var(--soft);margin-top:10px}
 .lx b{display:block;font-weight:300;font-size:22px;letter-spacing:-.02em;line-height:1.1}
 .lx span{display:block;margin-top:4px;font-size:12px;color:var(--bone3)}
 .lx p{grid-column:1/-1;font-size:14px;color:var(--bone2);line-height:1.5}
 .ch-meta,.method .ml,.toc .ml,.toc a b,.story .st,.story cite,.step .w,.readout .rt,.mast span{font-size:11px!important}
 .method .m span,.bl{font-size:13px}
 .readout .rl{font-size:15px}.readout .rs{font-size:13px}
 .story{padding:22px 20px 20px}.story h3{font-size:30px}.story .n{flex-wrap:wrap;gap:6px 12px}
 .asks b{font-size:16px}.asks p{font-size:14.5px}
 .dl-wrap{display:none!important}
 .dl-inline{display:inline-flex;align-items:center;justify-content:center;margin-top:24px;min-height:48px;padding:0 22px;border-radius:999px;background:var(--mint);color:var(--ink);font-family:var(--mono);font-size:12px;letter-spacing:.16em;text-transform:uppercase;text-decoration:none;font-weight:500}
 .dl-inline.end{display:flex;margin:56px 0 0}
 footer{padding-bottom:30px}footer span{font-size:11px;text-align:left}
 .close .cb{font-size:64px}
}
h2 em{display:block}
.hero .hook span b{display:block;font-weight:inherit;white-space:nowrap}
.method .m span{white-space:nowrap}
.og{margin-top:120px}
.asks{grid-template-columns:repeat(3,1fr)}
.figs .readout .rs,.spread .readout .rs{flex-basis:100%}
@media(max-width:920px){.og{margin-top:90px}.asks{grid-template-columns:1fr}.whales .lh,.whales .lr{grid-template-columns:22px minmax(0,1fr) 62px 50px!important;gap:6px!important}.whales .lh .r{font-size:8px;letter-spacing:.08em}}
.p-run{display:none}
@media(max-width:920px){.toc{grid-template-columns:1fr 1fr}.toc .ml{grid-column:1/-1;padding:14px 0 6px}.toc a{border-left:0;border-top:1px solid var(--soft);padding:14px 12px 14px 0}}
@media print{
 @page{size:A4;margin:0}
 html,body{background:var(--ink)}body{-webkit-print-color-adjust:exact;print-color-adjust:exact;font-size:11px}
 body::before,#glow,#prog,#nav,.dl-wrap,.cue,.story .hint,.spot .tip,.readout{display:none!important}
 .rv,.hero h1 span,.hero .hook span,.hero .sub,.hero .who{opacity:1!important;transform:none!important;animation:none!important;transition:none!important}
 .ich .bar{transform:none!important;transition:none!important}
 .page{max-width:none;padding:0}
 .pg{display:flex;flex-direction:column;width:210mm;height:296.5mm;padding:10mm 13mm 9mm;overflow:hidden;page-break-after:always;break-after:page}
 .pg:last-child{page-break-after:auto}
 .p-run{display:flex;justify-content:space-between;align-items:center;padding-bottom:8px;border-bottom:1px solid var(--line);margin-bottom:14px}
 .p-run img{height:11px}.p-run span{font-family:var(--mono);font-size:7.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--bone3)}
 section{margin-top:0}
 .mast{padding:0 0 12px}.mast span{display:block;font-size:8px}
 .hero{min-height:0;grid-template-columns:1fr 1fr;gap:34px;padding:34px 0 30px}
 .hero h1{font-size:130px}.hero .hook{font-size:30px}.hero .sub{font-size:12px;margin-top:16px}.hero .who{font-size:8px;margin-top:14px}
 .teaser .big{padding:18px 16px 18px 0}.teaser .big+.big{padding-left:16px}
 .bv{font-size:44px}.bl{font-size:10.5px;margin-top:7px}
 .method{grid-template-columns:auto repeat(5,1fr);padding:14px 0}.method .ml{font-size:8px;padding-right:18px}.method .m{padding:0 12px}.method .m b{font-size:19px}.method .m span{font-size:9.5px}
 .toc{grid-template-columns:auto repeat(6,1fr)}.toc .ml{font-size:8px;padding:14px 18px 14px 0}.toc a{padding:12px 10px}.toc a span{font-size:10.5px}.toc a b{font-size:8px}
 .ch{grid-template-columns:1fr 2.4fr;gap:20px;padding-bottom:12px}.ch-meta{font-size:8px}.ch-meta .num{font-size:34px}
 h2{font-size:28px;max-width:none}
 .ch.sm .ch-meta .num{font-size:24px}.ch.sm h2{font-size:22px}
 .spread,.spread.rev,.spread.eq{gap:24px;margin-top:16px}
 .lead{font-size:15px}.prose p{font-size:10.5px;margin-top:8px;max-width:none}
 .stack .big{padding:9px 0}.stack .bv{font-size:30px}
 .row4{gap:14px;margin-top:14px}.row4 .big{padding-top:9px}.row4 .bv{font-size:28px}
 .fig{margin-top:14px;padding:12px 14px 8px}.fig figcaption{font-size:9.5px;margin-top:6px}.fig .legend{font-size:7.5px;margin-top:6px}
 .figs{gap:12px;margin-top:14px}
 .stories{gap:10px;margin-top:14px}.story{padding:14px 16px 12px}.story h3{font-size:22px}.story .st{font-size:8px}.story .h{font-size:8.5px}.story p{font-size:10px;margin-top:8px}
 .story blockquote{margin-top:8px}.story blockquote p{font-size:13px}.story cite{font-size:7.5px}.sbig{font-size:30px;margin-top:8px}.sbig small{font-size:10px}
 .story .more{grid-template-rows:0fr}
 .asks-h{font-size:17px;margin-top:14px}.asks{grid-template-columns:repeat(3,1fr);gap:10px;margin-top:10px}.asks div{padding:12px 14px}.asks b{font-size:12px}.asks p{font-size:10px}
 .whales{grid-template-columns:1fr;margin-top:12px}.spot{display:none}.twin{grid-template-columns:1fr 1fr;gap:18px;margin-top:0}
 .whales .lh,.whales .lr{grid-template-columns:22px 1fr 58px 48px;padding:5.2px 4px}.whales .lw b{font-size:10.5px}.whales .lw i{font-size:8px}.whales .r{font-size:9.5px}.lh{font-size:7.5px}
 .plan{gap:10px;margin-top:14px}.step{padding:14px 16px}.step .w{font-size:8px}.step h3{font-size:16px;margin-top:6px}.step p{font-size:10px;margin-top:8px}
 .close{margin-top:auto;padding:26px 30px 24px;gap:26px}.close .cb{font-size:62px}.close .cb small{font-size:10px}.close p{font-size:13px}.close img{width:220px;bottom:-40px}.close .sig{font-size:8px;margin-top:12px}
 footer{margin-top:12px;padding-top:10px}footer span{font-size:7.5px}footer img{height:10px}
 .grow{margin-top:auto}
 .page{padding:0!important}
 .hero{grid-template-columns:1fr 1fr!important;gap:34px!important;padding:30px 0 26px!important}.hero h1{font-size:128px!important}
 .teaser{grid-template-columns:repeat(3,1fr)!important}.teaser .big{border-right:1px solid var(--soft)!important;border-bottom:0!important;padding:18px 16px 18px 0!important}.teaser .big+.big{padding-left:16px!important}.teaser .big:last-child{border-right:0!important}
 .method{grid-template-columns:auto repeat(5,1fr)!important;gap:0!important}.method .ml{grid-column:auto!important;padding:0 18px 0 0!important}.method .m{border-left:1px solid var(--soft)!important;padding:0 12px!important}
 .toc{grid-template-columns:auto repeat(6,1fr)!important}.toc .ml{grid-column:auto!important}.toc a{border-top:0!important;border-left:1px solid var(--soft)!important;padding:12px 10px!important}
 .ch{grid-template-columns:1fr 2.4fr!important;gap:20px!important}.ch.sm{grid-template-columns:1fr!important;gap:6px!important}
 .spread{grid-template-columns:5fr 7fr!important;gap:24px!important}.spread.rev{grid-template-columns:7fr 5fr!important}.spread.eq{grid-template-columns:1fr 1fr!important}
 .figs{grid-template-columns:1fr 1fr!important}.stories{grid-template-columns:1fr 1fr!important}.plan{grid-template-columns:repeat(3,1fr)!important}
 .close{grid-template-columns:1fr 1.3fr!important;padding:24px 28px 22px!important;gap:24px!important}
 .twin{grid-template-columns:1fr 1fr!important}.whales{grid-template-columns:1fr!important}
 section{margin-top:0!important}
 .story .more{display:none!important}
 .row4{grid-template-columns:repeat(4,1fr)!important}
 .web{display:none!important}
 .p-run span,.story .st,.story cite,.step .w,.ch-meta,.method .ml,.toc .ml,.toc a b,.close .sig{font-size:8px!important}
 .lh{font-size:8px!important}.whales .lw i{font-size:8px!important}
 h2{font-size:26px!important;line-height:1.08!important}
 .hero{grid-template-columns:1fr 1.15fr!important}.pg:first-child .hero .hook{font-size:31px!important;max-width:none!important}
 .bl{max-width:none!important}.row4 .bl{font-size:10.5px}
 .whales .lh,.whales .lr{grid-template-columns:24px minmax(0,1fr) 66px 58px!important;gap:8px!important}
 .pg .whales .ledger .lr{padding:12.5px 4px!important}
 .asks p{font-size:11px!important;line-height:1.55}.asks div{padding:14px 16px!important}.whales .lh .r{font-size:8px!important;letter-spacing:.1em!important;white-space:nowrap}
 .pg>section+section{padding-top:20px!important}
 .step h3{white-space:nowrap}
 .fig figcaption{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
 footer{flex-wrap:nowrap!important;gap:24px}footer span{font-size:8px!important;line-height:1.7}
 .pg.sv{justify-content:space-between}.pg.sv>*{margin-top:0!important}
 .og .spread{flex:0 0 auto;align-items:start}.og{flex:0 0 auto!important}
 .pg:first-child .hero{padding:44px 0 40px!important}.pg:first-child .hero h1{font-size:150px!important}.pg:first-child .hero .hook{font-size:34px!important}.pg:first-child .hero .sub{font-size:13px!important}
 .pg:first-child .teaser .big{padding:30px 16px 30px 0!important}.pg:first-child .teaser .big+.big{padding-left:18px!important}.pg:first-child .teaser .bv{font-size:56px}.pg:first-child .teaser .bl{font-size:11.5px}
 .pg:first-child .method{padding:22px 0!important}.pg:first-child .method .m b{font-size:24px}
 .og{margin-top:22px!important;display:flex;flex-direction:column;flex:1}.og .spread{flex:1;align-items:center}
 .s1 .stack .bv{font-size:36px}
 .whales .lh,.whales .lr{padding:8.4px 4px!important}.whales .lw b{font-size:11.5px!important}.whales .lw i{font-size:8.5px!important}.whales .r{font-size:10.5px!important}
 .stories .story p{font-size:10.5px}
 .figs .fig,.og .fig{padding:14px 16px 10px}
 .plan .step p{font-size:10.8px}
}
"""

H = []
H.append(f'''<div id="prog"></div><div id="glow"></div>
<nav id="nav">
  <a href="#top"><span>Vale</span><i></i></a><a href="#c1"><span>Your month</span><i></i></a><a href="#c2"><span>OG Ry</span><i></i></a><a href="#c3"><span>Your top fans</span><i></i></a><a href="#c4"><span>Gone quiet</span><i></i></a><a href="#c5"><span>Your ceiling</span><i></i></a><a href="#c6"><span>Next thirty days</span><i></i></a>
</nav>
<div class="dl-wrap"><a class="dl-btn" href="ALTR-vale-top-fans-sep16.pdf" download="Vale-Top-Fans-Review-ALTR-Sep-2026.pdf">Download PDF</a></div>
<div class="page" id="top">
<div class="pg sv">
  <header class="mast"><img src="__LOGO__" alt="ALTR"><span>A private review of your top fans, prepared for Vale, September 16, 2026</span></header>
  <div class="hero">
    <h1><span>V</span><span>a</span><span>l</span><span>e</span><span>.</span></h1>
    <div>
      <p class="hook"><span><b>Your best nights came</b><b>from a few people.</b></span><span><b>Most of them are</b><b>one message away.</b></span></p>
      <p class="sub">We went through five months of your page, purchase by purchase, to find the people behind your best nights: who they are, what they spend, when they buy, and which of them have gone quiet. This is what we found, and what we do next.</p>
      <div class="who">Apr 19 to Sep 16, 2026<br>Built from your own account data<br>Confidential, for you only</div>
      <a class="dl-inline" href="ALTR-vale-top-fans-sep16.pdf" download="Vale-Top-Fans-Review-ALTR-Sep-2026.pdf">Download the PDF</a>
    </div>
    <div class="cue"><i></i>Scroll</div>
  </div>
  <div class="teaser">
    {big(M(top_net), f"spent by your top {len(board)} fans in five months, 45 percent of your earnings", top_net, "$")}
    {big(M(quiet_net), f"of it from {len(quiet)} fans who have not bought in three weeks or more", quiet_net, "$")}
    {big(f"{cap_share}<small>%</small>", "of what your top fans spend lands on your $200 maximum")}
  </div>
  <div class="method rv"><span class="ml">What we read</span>
    <div class="m"><b>150</b><span>days of your page</span></div>
    <div class="m"><b>{len(tx):,}</b><span>purchases, one by one</span></div>
    <div class="m"><b>{paying:,}</b><span>fans who paid you</span></div>
    <div class="m"><b>{len(board)}</b><span>top fans, profiled</span></div>
    <div class="m"><b>{P["threads_ok"]}</b><span>conversations read</span></div>
  </div>
  <nav class="toc rv"><span class="ml">Inside</span>
    <a href="#c1"><b>01</b><span>Your month</span></a><a href="#c2"><b>02</b><span>OG Ry</span></a><a href="#c3"><b>03</b><span>Your top fans</span></a>
    <a href="#c4"><b>04</b><span>Gone quiet</span></a><a href="#c5"><b>05</b><span>Your ceiling</span></a><a href="#c6"><b>06</b><span>Next thirty days</span></a>
  </nav>
</div>''')

H.append(f'''<div class="pg sv"><div class="p-run"><img src="__LOGO__" alt="ALTR"><span>Vale, your top fans, 02 / 05</span></div>
<section class="s1">
  {ch("01", "Your month", "Your month held. <em>The top of it thinned out.</em>", "c1")}
  <div class="spread">
    <div class="rv">
      <p class="lead">You earned <em>{M(cur["total"])}</em> in the last thirty days, close to the {M(prev["total"])} before it, and {cur["buyers"]} fans bought from you, more than in any thirty days since April.</p>
      <div class="prose" style="margin-top:16px">
        <p>What changed is who carried it. In the thirty days to Aug 17, {prev["n500"]} fans spent $500 or more with you and brought in {M(prev["rev500"])}. In the thirty days since, {cur["n500"]} did, and brought in {M(cur["rev500"])}. More people buying in smaller amounts filled the gap.</p>
        <p>That is healthy, and it is also the opportunity. Your biggest nights come from a small group of people, and most of them can still hear from you this week. <span class="web"><span class="t-h">Hover any bar.</span><span class="t-t">Tap any bar for the detail.</span></span></p>
      </div>
    </div>
    <div class="stack">
      {big(str(cur["n500"]), f"fans spent $500 or more in the last thirty days, down from {prev['n500']}", cur["n500"])}
      {big(M(cur["rev500"]), f"came from them, against {M(prev['rev500'])} the month before", cur["rev500"], "$")}
    </div>
  </div>
  {fig(fig_layer, "What you earned in each thirty-day window. <em>Mint is fans who spent $500 or more in that window.</em>", meta_layer[4])}
</section>
<section class="og">
  {ch("02", "OG Ry", "Still with you every day. <em>The big nights stopped.</em>", "c2")}
  <div class="spread rev">
    {fig(fig_og, "OG Ry, thirty days at a time from each date. <em>Mint is Jun 18 to Jul 18.</em>", meta_og[2], ' style="margin-top:0"')}
    <div>
      <p class="lead rv">{M(og["life"])} with you in five months. Between Jun 18 and Jul 18 a typical purchase was ${ogt[2]["median"]:.0f}. Since mid-August it has been ${ogt[4]["median"]:.0f}.</p>
      <div class="prose rv" style="margin-top:10px"><p>Nothing is wrong with the relationship. Your last hundred messages together cover about forty hours. What has not happened since is a night like Jul 17: $122, $167, $167, then five at $200. From next week OG Ry gets one planned night a week, on a Thursday or Friday, built the way July was.</p></div>
    </div>
  </div>
</section>
</div>''')

H.append(f'''<div class="pg"><div class="p-run"><img src="__LOGO__" alt="ALTR"><span>Vale, your top fans, 03 / 05</span></div>
<section>
  {ch("03", "Your top fans", f"{len(board)} fans. <em>{M(top_net)} spent with you.</em>", "c3")}
  <div class="spread rev rv" style="margin-top:24px">
    <p class="lead">These are the twenty-four who spent most in the last five months. The mint dot marks the ones buying right now.<span class="web"><span class="t-h"> Move along the list and the card follows you.</span><span class="t-t"> Tap any fan to see their details.</span></span></p>
    <div class="prose"><p>Each one gets their own plan. Buying fans hear from you personally and never from a mass message. Quiet fans get a message with nothing for sale in it, at the hour they usually buy. Fans whose subscription ended are invited back.</p></div>
  </div>
  <div class="whales">
    <aside class="spot rv" id="spot">
      <div class="sr">Fan <b id="s-rank">{spot["rank"]}</b> of 24</div>
      <h3 id="s-name">{E(spot["name"])}</h3><div class="sh" id="s-handle">{E(spot["handle"])}</div>
      <div class="sg">
        <div><b id="s-net">{spot["net"]}</b><span>spent in five months</span></div>
        <div><b id="s-net30">{spot["net30"]}</b><span>in the last thirty days</span></div>
        <div><b id="s-last">{spot["last"]}</b><span>last purchase</span></div>
        <div><b id="s-best" style="font-size:22px">{spot["best"]}</b><span>their best night</span></div>
      </div>
      <div class="sa"><b>What we do next</b><span id="s-angle">{E(spot["angle"])}</span></div>
      <div class="tip">Hover or tap a fan</div>
    </aside>
    <div class="twin" style="margin-top:0">{ledger_a}{ledger_b}</div>
  </div>
</section>
</div>''')

H.append(f'''<div class="pg"><div class="p-run"><img src="__LOGO__" alt="ALTR"><span>Vale, your top fans, 04 / 05</span></div>
<section>
  {ch("04", "Gone quiet", f"{len(quiet)} fans went quiet. <em>Four of them tell the story.</em>", "c4")}
  <div class="stories">
    {story("Val", "Left Aug 9", f"@u31836535, {M(val['net'])} in eleven days", f"Seven nights between Jul 9 and Jul 19, with {val200} purchases at $199 or $200. Then, on Aug 8, a goodbye.", "Feel like I've explored all there is without unlocking some club.", "Val, Aug 8", "Val did not leave over price. The menu ran out. We invite them back with a return offer this week.")}
    {story("Asaf", f"Quiet {asaf['days_since_buy']:.0f} days", "@u75127224, one night in August", "On Aug 13 Asaf unlocked $100, then $140, then seven messages at $200 in a row. It is the third biggest night on your page in five months, and they have not bought since.", "$1,640<small>in one night</small>", "", "Asaf can still be reached. This week they get a personal message that picks up that night, with nothing for sale in it, on a Thursday evening, which is when they bought.")}
    {story("John Gale", "Ended Sep 12", f"@u458928755, {M(jg['net'])} in nine days", "Six nights in mid-August, the last a climb from $50 to four messages at $200. They joined on your promotion, and that subscription ended on Sep 12.", "6<small>nights in nine days</small>", "", "Proof that your promotions bring in real spenders. We invite John Gale back with a return offer this week.")}
    {story("Dwayne", f"Quiet {dw['days_since_buy']:.0f} days", "@numbnutz05, a Saturday afternoon", "On Saturday Aug 15, mid-afternoon, Dwayne spent $999 in one sitting and came back for $180 a week later. Nothing since.", "$999<small>on a Saturday</small>", "", "Dwayne bought on a Saturday around 3pm Eastern. That is when they hear from you this week.")}
  </div>
</section>
<section class="grow" style="margin-top:22px">
  {ch("05", "Your ceiling", "Your best nights don't slow down. <em>They run out of menu.</em>", "c5")}
  <div class="spread eq" style="margin-top:18px">
    {fig(fig_band, f"What your top fans spend, by price. <em>{cap_share} percent lands at $200.</em>", meta_band[5], ' style="margin-top:0"')}
    <div class="rv">
      <p class="lead">When your biggest fans are in the mood, they don't stop at $200. <em>They repeat it.</em></p>
      <div class="prose" style="margin-top:10px"><p>Tuetken45 bought nine messages at $196.69 in a row on Jul 17. Asaf bought seven at $200. OG Ry bought five. {n_cap} purchases in five months landed on your maximum, because there was nothing above it to buy.</p></div>
    </div>
  </div>
</section>
</div>''')

H.append(f'''<div class="pg sv"><div class="p-run"><img src="__LOGO__" alt="ALTR"><span>Vale, your top fans, 05 / 05</span></div>
<section>
  {ch("06", "The next thirty days", "What we do, <em>in order, from today.</em>", "c6")}
  <div class="figs">
    {fig(fig_days, f"When your top fans spend, by weekday. <em>Friday alone is {fri} percent.</em>", meta_d[4])}
    {fig(fig_hours, "By hour, Eastern time. <em>Mid-afternoon into evening, and again just after midnight.</em>", meta_h[15])}
  </div>
  <div class="row4">
    {big(f"{fri}<small>%</small>", "of top-fan spending, on Fridays")}
    {big(hname(max(range(24), key=lambda h: hrs[h])), "Eastern, your strongest hour")}
    {big("12am", "to 2am Eastern, your second wave")}
    {big("4am", "to 8am, your quietest hours")}
  </div>
  <div class="plan">
    <div class="step rv"><div class="w">Today</div><h3>Save two renewals</h3><p>Jonny, {M(5885)} with you, and Matiu Dane, {M(3050)}, have subscriptions ending Sep 18 without renewal. Both hear from you personally today. Nik, who had the month's biggest night on Sep 14, gets a follow-up.</p></div>
    <div class="step rv" style="transition-delay:.12s"><div class="w">This week</div><h3>Reach every quiet fan</h3><p>Asaf, Carlos, Dwayne and Javi get personal messages at the hour they usually buy. Val, John Gale, aboveaverage and James Redmond get a return offer. Your top {len(board)} are taken off mass messages.</p></div>
    <div class="step rv" style="transition-delay:.24s"><div class="w">From next week</div><h3>Plan the big nights</h3><p>One planned Thursday or Friday night a week for OG Ry and your top fans, built the way July was. You get this page refreshed every month.</p></div>
  </div>
</section>
<div class="close rv"><img src="__MARK__" alt="" aria-hidden="true">
  <div class="cb"><span data-count="{quiet_net}" data-prefix="$">{M(quiet_net)}</span><small>spent with you by fans who have gone quiet</small></div>
  <div><p>In the thirty days to Aug 17, {prev["n500"]} fans spent $500 or more with you. In the thirty days since, {cur["n500"]} did. <em>Most of the rest are one message away,</em> and they hear from you this week.</p><div class="sig">ALTR, September 16, 2026</div></div>
</div>
<a class="dl-inline end" href="ALTR-vale-top-fans-sep16.pdf" download="Vale-Top-Fans-Review-ALTR-Sep-2026.pdf">Download the PDF</a>
<footer><img src="__LOGO__" alt="ALTR"><span>Prepared by ALTR for Vale. Built from your OnlyFans account data. Your ALTR statement remains the official record of your earnings. Confidential, for Vale only.</span></footer>
</div>
</div>''')

JS = open("creator_base.js", encoding="utf-8").read()
JS = JS.replace("if(cur==='c4')cur='c3';", "")
JS = JS.replace("['rank','name','handle','net60','net30','last','days','pers','angle']", "['rank','name','handle','net','net30','last','best','angle']")
JS = JS.replace("f.net60.textContent=d.net60;f.net30.textContent=d.net30;f.last.textContent=d.last;f.days.innerHTML=d.days+'<small style=\"font-size:.5em\"> days</small>';f.pers.textContent=d.pers;f.angle.textContent=d.angle;",
                "f.net.textContent=d.net;f.net30.textContent=d.net30;f.last.textContent=d.last;f.best.textContent=d.best;f.angle.textContent=d.angle;")
assert "d.net60" not in JS and "f.best.textContent" in JS
old = "document.querySelectorAll('.fig').forEach(function(f){var svg=f.querySelector('.ich');if(!svg)return;"
assert old in JS
JS = JS.replace(old, "document.querySelectorAll('.fig .ich').forEach(function(svg){var f=svg.closest('.fig');")
JS = JS.replace("</script>", """  document.querySelectorAll('.whales .lr[data-name]').forEach(function(r){r.addEventListener('click',function(){if(!window.matchMedia('(max-width:920px)').matches)return;var was=r.classList.contains('open');document.querySelectorAll('.whales .lr.open').forEach(function(x){x.classList.remove('open')});if(!was)r.classList.add('open')})});
</script>""")

HEAD = ('<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><meta name="robots" content="noindex, nofollow"><meta name="theme-color" content="#1d1d1b">'
        '<title>Vale. Your top fans, a private review by ALTR</title>'
        '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,62..125,100..900;1,62..125,100..900&family=Spline+Sans+Mono:wght@400;500&display=swap" rel="stylesheet">')
out = '<!DOCTYPE html><html lang="en"><head>' + HEAD + "<style>" + BASE + EXTRA + "</style></head><body>" + "\n".join(H) + JS + "</body></html>"
if __name__ == "__main__":
    open("template.html", "w", encoding="utf-8").write(out)
    print("template.html", len(out))
