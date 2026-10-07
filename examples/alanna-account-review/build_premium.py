# -*- coding: utf-8 -*-
"""Alanna's World (@alannasworldx) account review, prepared by ALTR for Alanna.
Her main page, run by her current chat team. Source: Derrek's diagnostic, Sep 25 2026.
Web scroll experience -> template.html, PDF reading edition -> print-template.html. Then run build.py."""
import html, os, json
os.chdir(os.path.dirname(os.path.abspath(__file__)))
E = html.escape
M = lambda n: f"${n:,.0f}"

NET30, NET_PREV, GROSS30, GROSS_PREV, DROP = 93_400, 119_000, 116_700, 148_700, 23.6
VIS_JAN, VIS_SEP, VIS_DROP = 56_000, 7_200, 87
BLAST_SENT, BLAST_VIEWED = 153_146, 366
BLAST_RATE = round(BLAST_VIEWED / BLAST_SENT * 100, 2)
AUG_SENT, AUG_RATE, AUG_SALES = 145_563, 25.5, 22
LINK_CLICKS, LINK_SUBS = 2_360, 408
TOP_LIFETIME = 12_378
OPENER = ("thanks for coming to my page love 😘 your timing is insane 👀 I just finished putting together a "
          "SEXY XXX BUNDLE I know you are going to love 🫶 only 3 people can unlock it this week...")
ZIGGY_PPVS = [199.78, 199.79, 199.78, 199.79, 199.78, 199.79, 199.78, 199.79]
WHALES = [
    ("Top fan", "1", TOP_LIFETIME, "Active", "No notes, no summary"),
    ("Ziggy", "2", 8_165, "Lapsed since Apr 9, about 5.5 months", "NO COVERS ALLOWED"),
    ("Zach", "3", 7_981, "Lapsed Sep 13, 12 days ago", "Custom Dr and 15min Vidcall"),
    ("Dan", "4", 7_563, "Active", "DO DAMAGE CONTROL, FAILED CAPTION FOR ULTRA SVIP"),
    ("Petros", "5", 4_822, "Lapsed since Aug 2025, chat now returns user not found", "VC PAID"),
    ("arod761 (Tony)", "7", 4_449, "Lapsed 8 days ago", "No notes, no summary"),
    ("Tyler", "8", 3_849, "Lapsed since Jan 20, over 8 months", "Pending VC and Dick Rate"),
    ("Noah", "10", 3_800, "Lapsed about a year, since Sep 2025", "No notes, no summary"),
]

def ichart(cid, series, meta, w, h, xlabels, yfmt=None, show_val=None, hot=(), lw=None, fs=1.0):
    lw = lw or int(48 * fs)
    yfmt = yfmt or (lambda v: f"${v/1000:g}K" if v >= 1000 else f"${v:,.0f}")
    raw = max(max(series), 1)
    mx = next((c for c in [1, 5, 10, 25, 30, 50, 100, 200, 250, 500, 1000, 2500, 5000, 10000, 20000, 25000, 50000, 60000, 100000, 125000, 150000] if c >= raw), raw)
    tp, bp = int(24 * fs), int(30 * fs); ch_ = h - tp - bp; x0 = lw; cw = w - x0 - 4; n = len(series); bw = cw / n
    o = [f'<svg class="ich" id="{cid}" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid meet" role="img">']
    for fr in (0.0, 0.5, 1.0):
        y = tp + ch_ - ch_ * fr
        o.append(f'<line x1="{x0}" y1="{y:.1f}" x2="{w-4}" y2="{y:.1f}" stroke="rgba(235,236,220,0.09)"/>')
        o.append(f'<text x="{x0-8}" y="{y+3.5*fs:.1f}" font-size="{10*fs:.0f}" fill="rgba(235,236,220,0.5)" text-anchor="end">{yfmt(mx*fr)}</text>')
    for i, v in enumerate(series):
        x = x0 + i * bw + bw * 0.2; bwid = bw * 0.6; bh = ch_ * v / mx; y = tp + ch_ - bh
        dim = " after" if (hot and i not in hot) else ""
        o.append(f'<rect class="bar{dim}" data-meta="{E(json.dumps(meta[i]))}" x="{x:.1f}" y="{y:.1f}" width="{bwid:.1f}" height="{max(bh,1):.1f}" rx="1" style="transition-delay:{i*60}ms"/>')
        if show_val: o.append(f'<text x="{x0+i*bw+bw/2:.1f}" y="{y-8*fs:.1f}" font-size="{12*fs:.0f}" fill="#ebecdc" text-anchor="middle">{show_val[i]}</text>')
        if xlabels and xlabels[i]:
            o.append(f'<text x="{x0+i*bw+bw/2:.1f}" y="{h-9*fs:.0f}" font-size="{10.5*fs:.0f}" fill="rgba(235,236,220,0.65)" text-anchor="middle">{E(xlabels[i])}</text>')
    o.append("</svg>"); return "".join(o)
def dual(d, m): return f'<div class="cv d">{d}</div><div class="cv m">{m}</div>'
def fig(svg, caption, default, extra=""):
    return (f'<figure class="fig rv"{extra}>{svg}<div class="readout"><span class="rt">{E(default["t"])}</span><span class="rl">{E(default["l"])}</span>'
            f'<span class="rs">{E(default["s"])}</span></div><figcaption>{caption}</figcaption></figure>')
pctf = lambda v: f"{v:g}%"; kf = lambda v: f"{v/1000:g}K"
m_view = [{"t": "Aug 28", "l": f"{AUG_RATE}% of {AUG_SENT:,} opened it", "s": f"{AUG_SALES} sales from that one send."},
          {"t": "Sep 25", "l": f"{BLAST_RATE}% of {BLAST_SENT:,} opened it", "s": f"{BLAST_VIEWED} views, one of ten sends in under five hours."}]
fig_view = dual(ichart("c-view", [AUG_RATE, BLAST_RATE], m_view, 900, 400, ["Aug 28, one send", "Sep 25, ten sends"], hot=(0,), fs=2.2, yfmt=pctf, show_val=[f"{AUG_RATE}%", f"{BLAST_RATE}%"]),
                ichart("c-view-m", [AUG_RATE, BLAST_RATE], m_view, 420, 250, ["Aug 28", "Sep 25"], hot=(0,), fs=1.5, lw=52, yfmt=pctf, show_val=[f"{AUG_RATE}%", f"{BLAST_RATE}%"]))
m_rev = [{"t": "Prior 30 days", "l": f"{M(NET_PREV)} net", "s": f"{M(GROSS_PREV)} gross."},
         {"t": "Last 30 days", "l": f"{M(NET30)} net", "s": f"{M(GROSS30)} gross, down {DROP}%."}]
fig_rev = dual(ichart("c-rev", [NET_PREV, NET30], m_rev, 900, 400, ["Prior 30 days", "Last 30 days"], hot=(1,), fs=2.2, show_val=[M(NET_PREV), M(NET30)]),
               ichart("c-rev-m", [NET_PREV, NET30], m_rev, 420, 250, ["Prior 30", "Last 30"], hot=(1,), fs=1.5, lw=58, show_val=[M(NET_PREV), M(NET30)]))
m_vis = [{"t": "Jan 2026", "l": f"{VIS_JAN:,} profile visitors", "s": "The peak month."},
         {"t": "Sep 2026", "l": f"{VIS_SEP:,} profile visitors", "s": f"About {VIS_DROP}% below the peak."}]
fig_vis = dual(ichart("c-vis", [VIS_JAN, VIS_SEP], m_vis, 900, 400, ["Jan 2026", "Sep 2026"], hot=(0,), fs=2.2, yfmt=kf, show_val=[f"{VIS_JAN//1000}K", f"{VIS_SEP/1000:g}K"]),
               ichart("c-vis-m", [VIS_JAN, VIS_SEP], m_vis, 420, 250, ["Jan", "Sep"], hot=(0,), fs=1.5, lw=52, yfmt=kf, show_val=[f"{VIS_JAN//1000}K", f"{VIS_SEP/1000:g}K"]))
def ladder(tickets, w=210, h=40, cap=200, label="$199.78"):
    n = len(tickets); top = 13; base = h - 1; gap = 3.2; bw = min(16, (w - 64 - gap * (n - 1)) / n)
    o = [f'<svg class="lad" viewBox="0 0 {w} {h}" preserveAspectRatio="xMinYMid meet"><line x1="0" y1="{top}" x2="{w-60}" y2="{top}" stroke="#b6f2e5" stroke-width=".8" stroke-dasharray="2 2.5" opacity=".7"/>'
         f'<text x="{w}" y="{top+10}" text-anchor="end" font-size="10.5" fill="#b6f2e5" font-family="Spline Sans Mono, monospace">{label}</text>']
    for i, t in enumerate(tickets):
        bh = max(2, (base - top) * min(t, cap) / cap); x = i * (bw + gap)
        o.append(f'<rect x="{x:.1f}" y="{base-bh:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx=".6" fill="#b6f2e5"/>')
    return "".join(o) + "</svg>"

def ch(num, kicker, title, cid):
    return f'<header class="ch rv" id="{cid}"><div class="ch-meta"><span class="num">{num}</span><span class="kick">{E(kicker)}</span></div><h2>{title}</h2></header>'
def big(v, label): return f'<div class="big rv"><span class="bv">{v}</span><span class="bl">{E(label)}</span></div>'
def story(name, status, meta, body, quote, cite, more):
    q = f'<blockquote><p>{E(quote)}</p><cite>{E(cite)}</cite></blockquote>' if cite else f'<div class="sbig">{quote}</div>'
    return (f'<article class="story rv" tabindex="0"><div class="n"><h3>{E(name)}</h3><span class="st">{E(status)}</span></div><div class="h">{E(meta)}</div>'
            f'<p>{body}</p>{q}<div class="more"><div><p>{more}</p></div></div><span class="hint">More</span></article>')
def wrow(w):
    name, rank, life, status, tag = w
    lapsed = status != "Active"
    return (f'<div class="lr{" hi" if lapsed else ""}" tabindex="0" data-rank="{rank}" data-name="{E(name)}" data-handle="Number {rank} by lifetime spend" '
            f'data-net="{M(life)}" data-last="{"Lapsed" if lapsed else "Active"}" data-why="{E(status)}" data-move="{E(tag)}">'
            f'<span class="ln">{rank}</span><span class="lw"><b>{E(name)}</b><i>{E(tag)}</i></span><span class="r">{M(life)}</span>'
            f'<span class="r">{"Lapsed" if lapsed else "Active"}</span>'
            f'<div class="lx"><div><b>{M(life)}</b><span>lifetime</span></div><div><b>{"Lapsed" if lapsed else "Active"}</b><span>status</span></div><p>{E(status)}</p></div></div>')
LH = '<div class="lh"><span class="ln">No.</span><span class="lw">Fan, and their tag</span><span class="r">Lifetime</span><span class="r">Status</span></div>'
ledger_a = f'<div class="ledger c">{LH}{"".join(wrow(w) for w in WHALES[:4])}</div>'
ledger_b = f'<div class="ledger c">{LH}{"".join(wrow(w) for w in WHALES[4:])}</div>'

BASE = open("creator_base.css", encoding="utf-8").read() + open("web_extra.css", encoding="utf-8").read()
EXTRA = """
.asks{grid-template-columns:repeat(4,1fr)}
@media(max-width:920px){.asks{grid-template-columns:1fr}}
.warn{margin-top:44px;padding:28px 32px;border:1px solid rgba(182,242,229,.35);border-radius:6px;background:var(--wash)}
.warn h3{font-weight:300;font-size:26px;letter-spacing:-.02em}.warn p{margin-top:10px;color:var(--bone2);font-size:15px;max-width:72ch}
.lad{display:block;width:100%;height:auto;margin-top:16px}
.bv,.method .m b,.spot .sg b,.readout .rl,.ledger .r{white-space:nowrap}
.fig figcaption{text-wrap:balance}
h2{max-width:26ch}h2 em{display:block}
.bigquote{margin-top:26px;border-left:2px solid var(--mint);padding:4px 0 4px 20px}
.bigquote p{font-weight:300;font-style:italic;font-size:22px;line-height:1.45;max-width:48ch;color:var(--bone)}
.bigquote cite{display:block;margin-top:10px;font-style:normal;font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--bone3)}
"""
H = [f'''<div id="prog"></div><div id="glow"></div>
<nav id="nav"><a href="#top"><span>Alanna</span><i></i></a><a href="#c1"><span>Where it stands</span><i></i></a><a href="#c2"><span>The sending</span><i></i></a><a href="#c3"><span>Your top ten</span><i></i></a><a href="#c4"><span>The script</span><i></i></a><a href="#c5"><span>Thread by thread</span><i></i></a><a href="#c6"><span>What works</span><i></i></a><a href="#c7"><span>What changes</span><i></i></a></nav>
<div class="dl-wrap"><a class="dl-btn" href="ALTR-alanna-account-review-sep25.pdf" download="Alanna-Account-Review-ALTR-Sep-2026.pdf">Download PDF</a></div>
<div class="page" id="top">
  <header class="mast"><img src="__LOGO__" alt="ALTR"><span>An account review prepared by ALTR for Alanna, confidential, September 25, 2026</span></header>
  <div class="hero">
    <h1><span>A</span><span>l</span><span>a</span><span>n</span><span>n</span><span>a</span><span>.</span></h1>
    <div>
      <p class="hook"><span><b>Your offers are going out.</b><b>Almost nobody sees them.</b></span><span><b>Your biggest fans get</b><b>the same copy and paste.</b></span></p>
      <p class="sub">ALTR does not run this page. We pulled the diagnostic anyway, from your own account data: what it earns, where the traffic went, and what the team currently running your chats has actually been sending. We read the complete chat histories of your ten biggest spenders, not just the recent messages.</p>
      <div class="who">Reviewed September 25, 2026<br>Prepared by ALTR for Alanna<br>Confidential</div>
      <a class="dl-inline" href="ALTR-alanna-account-review-sep25.pdf" download="Alanna-Account-Review-ALTR-Sep-2026.pdf">Download the PDF</a>
    </div>
    <div class="cue"><i></i>Scroll</div>
  </div>
  <div class="teaser">
    {big(f"{BLAST_RATE}<small>%</small>", f"of a {BLAST_SENT:,} fan send was opened on Sep 25, against {AUG_RATE}% on Aug 28")}
    {big(f"{DROP}<small>%</small>", f"down on revenue, {M(NET30)} net in 30 days against {M(NET_PREV)} the month before")}
    {big("6 of 10", "of your biggest lifetime spenders are no longer subscribed")}
  </div>
  <div class="method rv"><span class="ml">What we read</span>
    <div class="m"><b>30</b><span>days of revenue</span></div><div class="m"><b>9</b><span>months of traffic</span></div>
    <div class="m"><b>10</b><span>top spenders</span></div><div class="m"><b>Full</b><span>chat histories</span></div><div class="m"><b>0</b><span>notes found on any of them</span></div>
  </div>
  <nav class="toc rv"><span class="ml">Inside</span>
    <a href="#c1"><b>01</b><span>Where it stands</span></a><a href="#c2"><b>02</b><span>The sending</span></a><a href="#c3"><b>03</b><span>Your top ten</span></a><a href="#c4"><b>04</b><span>The script</span></a>
    <a href="#c5"><b>05</b><span>Thread by thread</span></a><a href="#c6"><b>06</b><span>What works</span></a><a href="#c7"><b>07</b><span>What changes</span></a>
  </nav>''']

H.append(f'''<section>
  {ch("01", "Where it stands", f"Down <em>{DROP}% in a month.</em>", "c1")}
  <div class="spread">
    <div class="rv"><p class="lead">The page took <em>{M(NET30)} net</em> in the last 30 days, {M(GROSS30)} gross. The 30 days before brought {M(NET_PREV)} net and {M(GROSS_PREV)} gross.</p>
      <div class="prose" style="margin-top:16px"><p>Daily transactions fell with it. The page used to spike at 200 to 315 a day and now runs at roughly 120 to 175. Profile visitors peaked near {VIS_JAN//1000}K a month in January 2026 and sit at about {VIS_SEP/1000:g}K now, a fall of roughly {VIS_DROP}% across eight months.</p>
      <p>Fewer people land on the profile, so fewer subscribe, so the team leans harder on messaging the fans already there. That is where it compounds, and it is the next chapter.</p></div></div>
    <div class="stack">{big(M(NET30), f"net in the last 30 days, {M(GROSS30)} gross")}{big("120 to 175", "transactions a day now, against 200 to 315 a month ago")}{big(f"{VIS_SEP/1000:g}K", f"profile visitors a month, down from {VIS_JAN//1000}K in January")}</div>
  </div>
  <div class="figs">
    {fig(fig_rev, f"Net revenue, 30 days against the 30 before. <em>Down {DROP}%.</em>", m_rev[1])}
    {fig(fig_vis, f"Profile visitors a month. <em>About {VIS_DROP}% below the January peak.</em>", m_vis[1])}
  </div>
</section>''')

H.append(f'''<section>
  {ch("02", "The sending", "Ten sends in five hours. <em>Almost nobody saw them.</em>", "c2")}
  <div class="spread">
    <div class="rv"><p class="lead">On Sep 25 the team sent <em>ten separate mass messages to about 153,000 fans in under five hours</em>, roughly one every 20 to 30 minutes.</p>
      <div class="prose" style="margin-top:16px"><p>Those recent sends are opened by 0.2% to 1.2% of the list. One went to {BLAST_SENT:,} fans and was viewed {BLAST_VIEWED} times. A send on Aug 28 to a list of almost the same size, {AUG_SENT:,} fans, was opened by {AUG_RATE}% and converted {AUG_SALES} sales.</p>
      <p>Same page, same audience, four weeks apart. The difference is how often the list is hit. Fans mute notifications, and OnlyFans deprioritises accounts that over send. This is the single biggest leak on the page right now, because the offers never reach the inbox.</p></div></div>
    <div class="stack">{big("10", "mass messages in under five hours on Sep 25")}{big(f"{BLAST_VIEWED}", f"people opened one that went to {BLAST_SENT:,}")}{big(f"{AUG_SALES} sales", f"from the single Aug 28 send at {AUG_RATE}%")}</div>
  </div>
  {fig(fig_view, "Open rate on a full list send, same page, four weeks apart. <em>Mint is Aug 28.</em>", m_view[0])}
</section>''')

H.append(f'''<section>
  {ch("03", "Your top ten", "Six of the ten <em>have already left.</em>", "c3")}
  <div class="spread rev rv" style="margin-top:24px">
    <p class="lead">Your top spender has paid <em>{M(TOP_LIFETIME)}</em> and is still here. Six of the ten biggest are no longer subscribed, and two of those left over a year ago.</p>
    <div class="prose"><p>There are no notes and no AI summaries on a single one of these ten. The only record anyone kept is in the tags chatters typed into the fans' display names, and those tags describe work that was never finished. Greg, Marius and irain are the other three still active. <span class="web"><span class="t-h">Move down the list and the card follows you.</span><span class="t-t">Tap a fan for the detail.</span></span></p></div>
  </div>
  <div class="whales">
    <aside class="spot rv" id="spot">
      <div class="sr">Number <b id="s-rank">1</b> by lifetime spend</div>
      <h3 id="s-name">{E(WHALES[0][0])}</h3><div class="sh" id="s-handle">Number 1 by lifetime spend</div>
      <div class="sg"><div><b id="s-net">{M(TOP_LIFETIME)}</b><span>lifetime</span></div><div><b id="s-last">Active</b><span>status</span></div></div>
      <div class="sa"><b>Where they stand</b><span id="s-why">{E(WHALES[0][3])}</span></div>
      <div class="sa"><b>The tag on their name</b><span id="s-move">{E(WHALES[0][4])}</span></div>
      <div class="tip">Hover or tap a fan</div>
    </aside>
    <div class="twin" style="margin-top:0">{ledger_a}{ledger_b}</div>
  </div>
  <div class="warn rv"><h3>What the tags say</h3><p>Petros paid for a video call and is tagged VC PAID. Tyler is tagged Pending VC and Dick Rate. Zach is tagged Custom Dr and 15min Vidcall. Dan, still active and your fourth biggest fan, carries DO DAMAGE CONTROL, FAILED CAPTION FOR ULTRA SVIP. Ziggy is tagged NO COVERS ALLOWED, a preference about what he wants. Three of those tags describe services that were paid for or promised, and none of them appear anywhere in the chats as delivered.</p></div>
</section>''')

H.append(f'''<section>
  {ch("04", "The script", "One script, <em>three different whales.</em>", "c4")}
  <div class="spread eq rv" style="margin-top:30px">
    <p class="lead">Dan, Tyler and Ziggy are worth $7,563, $3,849 and $8,165. <em>All three received the identical opener at the identical price, $10.69.</em></p>
    <div class="prose"><p>Not a version of it. The same words, the same emojis and the same line about only three people being able to unlock it this week, sent to three fans who between them have paid nearly $20,000 to this page.</p><p>None of this is girlfriend experience. It is a bot script with your name on it. The prices work the same way: Dan was asked for a $60 tip on the claim that the same video normally sells for $300, which is pricing theatre rather than a real offer. Once a fan stops paying he drops to cross promotion for other creators, the same my bestie has an OnlyFans, go check her out sends a stranger receives.</p></div>
  </div>
  <div class="bigquote rv"><p>{E(OPENER)}</p><cite>Sent to Dan, Tyler and Ziggy, same words, same $10.69</cite></div>
  <div class="row4">
    {big("3", "whales who received the identical opener")}
    {big("$10.69", "the price each of them was quoted")}
    {big("0", "notes or summaries kept on any of the ten")}
    {big("$60", "tip asked for on the claim it normally sells for $300")}
  </div>
</section>''')

H.append(f'''<section>
  {ch("05", "Thread by thread", "What the <em>full histories show.</em>", "c5")}
  <div class="stories">
    {story("Ziggy", "$8,165, lapsed since Apr 9", "Number 2 by lifetime spend, tagged NO COVERS ALLOWED",
      "On the night he subscribed he was sent eight near identical messages at $199.78 and $199.79 inside about 90 minutes, each relabelled (2), (3), (4), (5) as if it were something new, wrapped in escalating love bombing between the unlocks.",
      "I love you daddy... lifetime VIP status... I never spoil anyone like this", "The messages sent between the unlocks",
      "The session closes with: 'Seems like you're going to stay here with me forever, so I locked it so you can easily check it whenever you miss me.' That is a lock tactic, not a conversation. He spent somewhere between several hundred and over a thousand dollars in that one sitting and never subscribed again. In the 5.5 months since he has had no personal winback at all, only the same $5 to $25 bundle sends any stranger gets.")}
    {story("Dan", "$7,563, still active", "Number 4, tagged DO DAMAGE CONTROL, FAILED CAPTION FOR ULTRA SVIP, your highest risk active fan",
      "He asked a direct question about his status. The answer skipped it and pushed another paid message, and shortly after a $60 tip was requested for a rate video on the claim that it normally sells for $300.",
      "Hey babe. Im a VIP on your free page but wanted to join here too... Does my VIP count here too?", "Dan, never answered",
      "The reply was 'Mmmmm since you already spoiled me ill send it for a lower price just for you', followed immediately by another paid send. The tag on his name says a paid message sent to him went out wrong and a chatter flagged it for follow up. His activity since, Sep 19 and 20, is cross promotion for other creators' pages. The damage control never happened, and he is a loyal cross page VIP who is still paying.")}
    {story("Tyler", "$3,849, lapsed since Jan 20", "Number 8, tagged Pending VC and Dick Rate",
      "His entire subscription month, Dec 20 and 21 2025, was bundle sends and urgency lines one after another, with no actual conversation in between.",
      "$5 CUM BUNDLE... EPIC VAULT SALE... I'm never doing this again", "The messages he received",
      "Nothing in the thread shows the video call or the rate video he was tagged as owed ever being delivered. He left after one month and nobody approached him personally again in the eight months since.")}
    {story("Zach", "$7,981, lapsed Sep 13", "Number 3, tagged Custom Dr and 15min Vidcall",
      "The one thread where someone genuinely tried. A $200 message was discounted to $149.78 with second chance messaging, and there were attempts to schedule the video call he was owed.",
      "I kept checking to see if you unlocked it...", "The follow up he received",
      "He never unlocked it and lapsed anyway. The pressure went on the discount rather than on delivering the call he had already been promised. At 12 days lapsed he is the most recoverable name on the list.")}
  </div>
  <div class="warn rv"><h3>Petros, arod761 and Noah</h3><p>Petros, $4,822 and tagged VC PAID, paid for a video call and then went quiet around the time his subscription lapsed in August 2025. He has been silent for over 13 months and his chat thread now returns user not found, which usually means he deleted his account, so nobody can even ask whether that call happened. arod761, $4,449 and lapsed 8 days, and Noah, $3,800 and lapsed about a year, now receive only cross promotion for other creators, autumnren, vanessav and bronwina. Noah is still getting those a full year after he stopped paying, which means no winback was ever attempted for a fan worth nearly $4,000.</p></div>
</section>''')

H.append(f'''<section>
  {ch("06", "What works", "The page itself <em>is not the problem.</em>", "c6")}
  <div class="row4">
    {big(M(TOP_LIFETIME), "from your top fan, with several others between $4K and $8K")}
    {big("25<small>%</small>", "view rate on the $22 Anal Extravaganza bundle, 22 purchases and $484")}
    {big(f"{LINK_SUBS}", f"subscribers from one tracking link, off {LINK_CLICKS:,} clicks")}
    {big("7", "unread messages, all from the last few minutes")}
  </div>
  <div class="spread eq rv" style="margin-top:34px">
    <div class="prose"><p>Your whale base is real and it still spends. The best performing send in the account's history is a $22 bundle, not a $200 one, and it worked because it was specific. One tracking link posted on Aug 4, sweetalanna.pdf, turned {LINK_CLICKS:,} clicks into {LINK_SUBS} subscribers, which is a funnel worth running again rather than a one off. Four newer links were created in the last day or two and have no data yet.</p></div>
    <div class="prose"><p>Chat responsiveness is fine. Seven messages sit unread and all arrived in the last few minutes, so nobody is being left waiting on a reply. The fans are there, the content sells when it is aimed properly, and the traffic used to arrive.</p><p>This is not random churn. The page has been run on autopilot sending rather than relationship management, and that is a way of working, not a fact about your audience. It is the part that can change fastest.</p></div>
  </div>
</section>''')

H.append(f'''<section>
  {ch("07", "What changes", "Four things, <em>in order.</em>", "c7")}
  <div class="asks rv">
    <div><b data-n="01">Cut the sending</b><p>Once or twice a day at most, and split the list into active and expired fans instead of sending everything to everyone. Open rates recover when the list stops being hit every 20 minutes, and every other fix depends on this one.</p></div>
    <div><b data-n="02">Find what stopped</b><p>Traffic fell about {VIS_DROP}% from the January peak. Work out which marketing or promo activity ended around January and February 2026, because that is what used to fill the funnel.</p></div>
    <div><b data-n="03">Reuse the link that worked</b><p>The Aug 4 creative turned {LINK_CLICKS:,} clicks into {LINK_SUBS} subscribers. Run it again across the next promo push, and judge the four new links once they have data behind them.</p></div>
    <div><b data-n="04">Handle the top ten personally</b><p>Real notes on each of them, then outreach written from their own history. Dan first, since he is active and still waiting, then Zach at 12 days lapsed, then arod761 at 8 days.</p></div>
  </div>
  <div class="plan">
    <div class="step rv"><div class="w">Today</div><h3>Answer Dan</h3><p>He asked whether his VIP status on your free page carries over here, and he never got a reply. He is worth $7,563, he is still subscribed, and someone already flagged his name for damage control. One honest answer, from someone who has read his thread, with nothing for sale attached to it.</p></div>
    <div class="step rv" style="transition-delay:.12s"><div class="w">This week</div><h3>Close what was promised</h3><p>Zach is owed a custom and a 15 minute call. Tyler was tagged for a call and a rate video that never arrived. Petros paid for a call before he disappeared. Each one gets delivered, or refunded and closed honestly, and written down this time.</p></div>
    <div class="step rv" style="transition-delay:.24s"><div class="w">This week</div><h3>Stop the copy and paste</h3><p>No identical openers to different fans, no relabelled duplicates of the same message, no scarcity lines that are not true. Your biggest fans should be able to tell they are talking to your page and not to a script.</p></div>
  </div>
  <div class="close rv"><img src="__MARK__" alt="" aria-hidden="true">
    <div class="cb"><span>6 of 10</span><small>of your biggest spenders are gone</small></div>
    <div><p>None of this is a content problem, and none of it needs new traffic to start fixing. <em>The fans who pay the most are being handled by a script, and the ones who left were never asked to come back.</em></p><div class="sig">ALTR, September 25, 2026</div></div>
  </div>
  <footer><img src="__LOGO__" alt="ALTR"><span>Prepared by ALTR for Alanna. Built from the account's own data and full chat histories. Confidential.</span></footer>
</section>
</div>''')

JS = open("creator_base.js", encoding="utf-8").read()
JS = JS.replace("if(cur==='c4')cur='c3';", "")
JS = JS.replace("['rank','name','handle','net60','net30','last','days','pers','angle']", "['rank','name','handle','net','last','why','move']")
JS = JS.replace("f.net60.textContent=d.net60;f.net30.textContent=d.net30;f.last.textContent=d.last;f.days.innerHTML=d.days+'<small style=\"font-size:.5em\"> days</small>';f.pers.textContent=d.pers;f.angle.textContent=d.angle;",
                "f.net.textContent=d.net;f.last.textContent=d.last;f.why.textContent=d.why;f.move.textContent=d.move;")
old = "document.querySelectorAll('.fig').forEach(function(f){var svg=f.querySelector('.ich');if(!svg)return;"
assert old in JS and "f.why.textContent" in JS
JS = JS.replace(old, "document.querySelectorAll('.fig .ich').forEach(function(svg){var f=svg.closest('.fig');")
JS = JS.replace("</script>", "document.querySelectorAll('.whales .lr[data-name]').forEach(function(r){r.addEventListener('click',function(){if(!window.matchMedia('(max-width:920px)').matches)return;var was=r.classList.contains('open');document.querySelectorAll('.whales .lr.open').forEach(function(x){x.classList.remove('open')});if(!was)r.classList.add('open')})});\n</script>")
HEAD = ('<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><meta name="robots" content="noindex, nofollow"><meta name="theme-color" content="#1d1d1b">'
        '<title>Alanna. Account review by ALTR</title><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,62..125,100..900;1,62..125,100..900&family=Spline+Sans+Mono:wght@400;500&display=swap" rel="stylesheet">')
open("template.html", "w", encoding="utf-8").write('<!DOCTYPE html><html lang="en"><head>' + HEAD + "<style>" + BASE + EXTRA + "</style></head><body>" + "\n".join(H) + JS + "</body></html>")

# ------------------------------------------------------------------ PDF reading edition
PCSS = open("print_base.css", encoding="utf-8").read()
TOT = 9
CH = {1: "account review", 2: "the short version", 3: "where it stands", 4: "the sending", 5: "your top ten", 6: "the script", 7: "thread by thread", 8: "thread by thread", 9: "what works, what changes"}
NX = {1: "Turn the page, the short version", 2: "Next, where it stands", 3: "Next, the sending", 4: "Next, your top ten", 5: "Next, the script", 6: "Next, thread by thread", 7: "Next, the rest of the threads", 8: "Next, what works and what changes", 9: "Start with Dan"}
def page(n, body, cls=""):
    ghost = '<img class="ghost" src="__GHOST__" alt="">' if cls == "cover" else ""
    return (f'<section class="pg {cls}">{ghost}<header class="run"><img src="__LOGO__" alt="ALTR"><span>Alanna, {CH[n]}</span></header><div class="body">{body}</div>'
            f'<footer class="foot"><span>Prepared by ALTR for Alanna</span><span class="nx">{NX[n]}</span><span>{n:02d} / {TOT:02d}</span></footer></section>')
def head(num, kicker, title, line):
    return f'<div class="hd"><div class="hn"><b>{num}</b><span>{E(kicker)}</span></div><div class="ht"><h2>{title}</h2><p>{line}</p></div></div>'
def fnd(v, t, hi=False): return '<div%s><b>%s</b><p>%s</p></div>' % (' class="hi"' if hi else '', v, t)
PX = """
.cover .nums b{font-size:26pt}.cover .nums span{font-size:9pt}
.cv-top .hook{margin-top:6mm;font-weight:300;font-size:19pt;line-height:1.2;letter-spacing:-.02em}.cv-top .hook em{display:block;font-style:normal;color:var(--mint)}
.cover .ghost{position:absolute;right:-26mm;top:18mm;width:150mm;opacity:.045}
.foot .nx{color:var(--mint)}
.lad{display:block;width:100%;height:auto;margin-top:2mm}
.lcap{margin-top:1mm;font-family:var(--mono);font-size:6.8pt;color:var(--bone3);white-space:nowrap}.lcap b{font-family:var(--sans);font-weight:300;font-size:12pt;color:var(--bone);margin-right:1.6mm}
.know{display:grid;grid-template-columns:repeat(3,1fr);gap:4mm}
.kn{border:1px solid var(--line);border-radius:2mm;padding:4mm 4.5mm 3.5mm;display:flex;flex-direction:column}
.kn h4{font-weight:300;font-size:15pt;letter-spacing:-.02em;line-height:1;margin-top:1.8mm}.kn p{margin-top:2mm;font-size:8.8pt;color:var(--bone2);line-height:1.5}
.kn .lad{margin-top:auto;padding-top:3mm}
.asks4{display:grid;grid-template-columns:repeat(2,1fr);gap:3.5mm}
.a4{border:1px solid var(--line);border-radius:2mm;padding:3.6mm 4mm}.a4 h4{font-weight:500;font-size:10.5pt;margin-top:1mm}.a4 p{margin-top:1.4mm;font-size:9pt;color:var(--bone2);line-height:1.45}
.warnp{border:1px solid rgba(182,242,229,.45);background:var(--wash);border-radius:2mm;padding:4mm 5mm}.warnp h4{font-weight:500;font-size:11pt}.warnp p{margin-top:1.5mm;font-size:9pt;color:var(--bone2);line-height:1.5}
.qt{width:100%;border-collapse:collapse}.qt th{font-family:var(--mono);font-weight:400;font-size:6.8pt;letter-spacing:.1em;text-transform:uppercase;color:var(--bone3);text-align:left;padding:0 1.6mm 2mm;border-bottom:1px solid var(--line)}
.qt{flex:0 0 auto}.qt td{padding:4.4mm 1.6mm;border-bottom:1px solid var(--soft);font-size:9pt;vertical-align:top;line-height:1.45}.qt .n{font-family:var(--mono);font-size:7.5pt;color:var(--mint);width:6mm}
.qt .fan b{display:block;font-weight:500;font-size:9.6pt;white-space:nowrap}.qt .fan i{display:block;font-style:normal;font-family:var(--mono);font-size:6.6pt;color:var(--bone3);line-height:1.35}
.qt .num{text-align:right;font-family:var(--mono);white-space:nowrap}
.qt .bar span{display:block;width:16mm;height:1.3mm;border-radius:.7mm;background:rgba(235,236,220,.07)}.qt .bar i{display:block;height:100%;border-radius:.7mm;background:linear-gradient(to right,rgba(182,242,229,.4),#b6f2e5)}
.two{display:grid;grid-template-columns:1fr 1fr;gap:4mm;flex:0 0 auto}
.pq{border-left:1px solid var(--mint);padding-left:4mm;font-style:italic;font-weight:300;font-size:12.5pt;line-height:1.45;color:var(--bone)}
.pq cite{display:block;margin-top:1.5mm;font-style:normal;font-family:var(--mono);font-size:7pt;letter-spacing:.14em;text-transform:uppercase;color:var(--bone3)}
.thread{border-top:1px solid var(--line);padding:3.6mm 0;display:grid;grid-template-columns:46mm 1fr;gap:6mm}
.thread h4{font-weight:300;font-size:16pt;letter-spacing:-.02em;line-height:1}
.thread .meta{margin-top:1.6mm;font-family:var(--mono);font-size:6.8pt;color:var(--bone3);line-height:1.6}
.thread p{font-size:9.2pt;color:var(--bone2);line-height:1.52}.thread p + p{margin-top:1.8mm}
.thread h4.sm{font-size:12pt;white-space:nowrap}
.thread .lad{max-width:74mm}.thread .q{margin-top:1.8mm;border-left:1px solid var(--mint);padding-left:3mm;font-style:italic;color:var(--bone);font-size:10pt;line-height:1.4}
.nums b,.find b,.qt .num,.kn h4,.chart .cap,.foot span,.lcap{white-space:nowrap}
.body > .find{flex:0 0 auto;margin:3mm 0}.body > .find > div{padding:2.8mm 0}
.chart,.hd{flex:0 0 auto}
"""
wrows = "".join(
    f'<tr><td class="n">{w[1]}</td><td class="fan"><b>{E(w[0])}</b><i>{E(w[4])}</i></td>'
    f'<td class="bar"><span><i style="width:{w[2]/TOP_LIFETIME*100:.0f}%"></i></span></td><td class="num">{M(w[2])}</td><td>{E(w[3])}</td></tr>' for w in WHALES)
PP = []
PP.append(page(1, f'''<div class="cv-top"><div class="meta" style="margin:0 0 3mm">Account review, @alannasworldx</div><h1>Alanna<i>.</i></h1>
<div class="hook">Your offers are going out and almost nobody sees them.<em>Your biggest fans get the same copy and paste.</em></div><div class="meta">Prepared by ALTR for Alanna, September 25, 2026. Confidential.</div></div>
<div class="letter"><div class="lbl">Read first</div><div><p>ALTR does not run this page. We pulled the diagnostic anyway, from your own account data: what it earns, where the traffic went, and what the team currently running your chats has actually been sending. We read the complete chat histories of your ten biggest spenders, not just recent messages.</p>
<p>Page two is the short version. The pages after it show the evidence fan by fan, and the four things that need to change.</p><div class="sig">ALTR</div></div></div>
<div class="nums c3"><div><b>{BLAST_RATE}%</b><span>opened a {BLAST_SENT:,} fan send on Sep 25</span></div><div><b>{DROP}%</b><span>down on revenue in 30 days</span></div><div><b>6 of 10</b><span>top spenders no longer subscribed</span></div></div>
<div class="toc"><div class="lbl">Inside</div><ol><li>The short version<span>02</span></li><li>Where it stands<span>03</span></li><li>The sending<span>04</span></li><li>Your top ten<span>05</span></li><li>The script<span>06</span></li><li>Thread by thread<span>07</span></li><li>What works, what changes<span>09</span></li></ol></div>''', "cover"))
PP.append(page(2, f'''{head("02", "The short version", "Everything on one page. <em>Start here.</em>", "What we found across the revenue, the traffic, the sending and the ten biggest fans.")}
<div><div class="lbl" style="margin-bottom:2mm">What we found</div><div class="find">
{fnd(f"{BLAST_RATE}%", f"Opened a send that went to {BLAST_SENT:,} fans on Sep 25, one of ten sent in under five hours. A single send on Aug 28 to {AUG_SENT:,} fans was opened by {AUG_RATE}% and made {AUG_SALES} sales.", True)}
{fnd(M(NET30), f"Net in the last 30 days, {M(GROSS30)} gross, down {DROP}% from {M(NET_PREV)}. Transactions fell from 200 to 315 a day to roughly 120 to 175.")}
{fnd(f"{VIS_JAN//1000}K to {VIS_SEP/1000:g}K", f"Profile visitors a month, January to September, about {VIS_DROP}% down. Fewer new subscribers, more pressure on the fans already there.")}
{fnd("6 of 10", "Of your biggest lifetime spenders are no longer subscribed. No notes and no summaries exist on any of the ten.")}
{fnd("1 script", "The same opener, word for word at $10.69, went to Dan, Tyler and Ziggy, who are worth nearly $20,000 between them. None of it is girlfriend experience. It is a bot script.")}
</div></div>
<div><div class="lbl" style="margin-bottom:2.5mm">Three fans that explain it</div><div class="know">
<div class="kn"><span class="lbl">Still here, waiting</span><h4>Dan</h4><p>{M(7563)} lifetime. Asked whether his VIP status carried over and never got an answer. His name is tagged DO DAMAGE CONTROL.</p></div>
<div class="kn"><span class="lbl">Eight unlocks, one night</span><h4>Ziggy</h4><p>{M(8165)} lifetime. Eight near identical messages at $199.78 in about 90 minutes, then gone for 5.5 months.</p>{ladder(ZIGGY_PPVS)}<div class="lcap"><b>8</b>in about 90 minutes</div></div>
<div class="kn"><span class="lbl">Most recoverable</span><h4>Zach</h4><p>{M(7981)} lifetime, lapsed only 12 days. Owed a custom and a 15 minute call. Someone did try with him.</p></div>
</div></div>
<div><div class="lbl" style="margin-bottom:2.5mm">What needs to change</div><div class="wk">
<div><span class="lbl">Today</span><h4>Answer Dan</h4><p>One honest reply on his VIP status, from someone who has read his thread, with nothing for sale attached.</p></div>
<div><span class="lbl">This week</span><h4>Cut the sending</h4><p>Once or twice a day, split into active and expired fans, instead of ten sends to the whole list.</p></div>
<div><span class="lbl">This week</span><h4>Close what was promised</h4><p>Zach, Tyler and Petros were each tagged as owed a call. Deliver it, or refund and close it honestly.</p></div></div></div>'''))
PP.append(page(3, f'''{head("03", "Where it stands", f"Down <em>{DROP}% in a month.</em>", f"{M(NET30)} net in the last 30 days against {M(NET_PREV)} the month before, on traffic that has fallen about {VIS_DROP}% since January.")}
<div class="two"><div class="chart">{ichart("p-rev", [NET_PREV, NET30], [{}]*2, 900, 1280, ["Prior 30 days", "Last 30 days"], hot=(1,), fs=2.8, show_val=[M(NET_PREV), M(NET30)])}<div class="cap">Net revenue. <em>Down {DROP}%.</em></div></div>
<div class="chart">{ichart("p-vis", [VIS_JAN, VIS_SEP], [{}]*2, 900, 1280, ["Jan 2026", "Sep 2026"], hot=(0,), fs=2.8, yfmt=kf, show_val=[f"{VIS_JAN//1000}K", f"{VIS_SEP/1000:g}K"])}<div class="cap">Profile visitors a month. <em>About {VIS_DROP}% down.</em></div></div></div>
<div class="find">
{fnd(M(GROSS30), f"Gross in the last 30 days against {M(GROSS_PREV)} the month before, which is where the {DROP}% shows up before OnlyFans takes its cut.")}
{fnd("120 to 175", "Transactions a day now. The page used to spike at 200 to 315.")}
{fnd("Jan to Feb", "The window worth investigating. Something that used to drive visitors stopped around then, and the funnel has not recovered since.", True)}
</div>'''))
PP.append(page(4, f'''{head("04", "The sending", "Ten sends in five hours. <em>Almost nobody saw them.</em>", "On Sep 25 the team sent ten separate mass messages to about 153,000 fans in under five hours, roughly one every 20 to 30 minutes.")}
<div class="chart">{ichart("p-view", [AUG_RATE, BLAST_RATE], [{}]*2, 900, 560, ["Aug 28, one send", "Sep 25, ten sends"], hot=(0,), fs=1.5, yfmt=pctf, show_val=[f"{AUG_RATE}%", f"{BLAST_RATE}%"])}<div class="cap">Open rate on a full list send, same page, four weeks apart. <em>Mint is Aug 28.</em></div></div>
<div class="nums c4"><div><b>10</b><span>sends in under five hours, Sep 25</span></div><div><b>{BLAST_VIEWED}</b><span>opened one sent to {BLAST_SENT:,}</span></div><div><b>0.2 to 1.2%</b><span>open rate across the recent sends</span></div><div><b>{AUG_SALES} sales</b><span>from the single Aug 28 send</span></div></div>
<div class="warnp"><h4>Why this is the biggest leak</h4><p>Same page, same audience, four weeks apart. The difference is frequency. Fans mute notifications when a page messages them every 20 minutes, and OnlyFans deprioritises accounts that over send. Until this changes every offer on the page is invisible no matter how good it is, and everything else in this review is held back by it.</p></div>
<div class="warnp"><h4>What good looked like</h4><p>The Aug 28 send reached {AUG_SENT:,} fans, was opened by {AUG_RATE}% of them and converted {AUG_SALES} sales. The best performing paid send in the account's history is a $22 bundle, the Anal Extravaganza, with 22 purchases, $484 and a 25% view rate. Specific beats frequent on this page, and the account's own data already proves it.</p></div>'''))
PP.append(page(5, f'''{head("05", "Your top ten", "Six of the ten <em>have already left.</em>", f"Your top spender has paid {M(TOP_LIFETIME)} and is still here. There are no notes and no AI summaries on a single one of these ten.")}
<table class="qt"><thead><tr><th>No.</th><th>Fan, and the tag left on their name</th><th></th><th class="num">Lifetime</th><th>Where they stand</th></tr></thead><tbody>{wrows}</tbody></table>
<div class="two"><div class="warnp"><h4>What the tags say</h4><p>The only record anyone kept on these fans is in the tags typed into their display names. Three of them describe services that were paid for or promised: VC PAID on Petros, Pending VC and Dick Rate on Tyler, Custom Dr and 15min Vidcall on Zach. None appear anywhere in the chats as delivered.</p></div>
<div class="warnp"><h4>What is missing</h4><p>No notes and no AI summaries exist on any of these ten, so anyone opening one of these chats starts from nothing and the only paper trail on your biggest spenders is what a chatter once typed into a display name. Greg, Marius and irain are the other three still active. Dan is your highest risk active fan, and his tag says DO DAMAGE CONTROL.</p></div></div>'''))
PP.append(page(6, f'''{head("06", "The script", "One script, <em>three different whales.</em>", "Dan, Tyler and Ziggy are worth $7,563, $3,849 and $8,165. All three received the identical opener at the identical price.")}
<div class="pq">{E(OPENER)}<cite>Sent to Dan, Tyler and Ziggy, same words, same $10.69</cite></div>
<div class="nums c4"><div><b>3</b><span>whales who got the identical opener</span></div><div><b>$10.69</b><span>the price each was quoted</span></div><div><b>0</b><span>notes kept on any of the ten</span></div><div><b>3</b><span>paid or promised services never delivered</span></div></div>
<div class="warnp"><h4>What that means in practice</h4><p>Not a version of the same message. The same words, the same emojis and the same line about only three people being able to unlock it this week, sent to three different fans who between them have paid nearly $20,000 to this page. None of this is girlfriend experience. It is a bot script with your name on it, and nothing in it reflects what any of them had already spent.</p></div>
<div class="pq">I always sell my vid rate for $300 but not for you<cite>Pricing theatre: the line used on Dan to bait a $60 tip</cite></div>
<div class="warnp"><h4>The scarcity is not real, and your fans can tell</h4><p>Only 3 people can unlock it this week went to three fans at three different times. I'm never doing this again went to Tyler in the middle of a run of bundle sends. I never spoil anyone like this went to Ziggy between two of eight near identical unlocks in the same hour. A fan who has paid thousands has heard all of these before, and each time one of them turns out not to be true, the next message is worth a little less.</p></div>
<div class="warnp"><h4>And once they stop paying</h4><p>Lapsed fans drop to cross promotion for other creators' pages, the my bestie has an OnlyFans, go check her out sends a stranger receives, for autumnren, vanessav and bronwina. arod761 and Noah now get nothing else. Noah is still receiving them a full year after he stopped paying, which means no winback was ever attempted for a fan worth nearly $4,000.</p></div>'''))
PP.append(page(7, f'''{head("07", "Thread by thread", "Ziggy <em>and Dan.</em>", "Your second biggest fan, and your highest value fan still subscribed.")}
<div class="thread"><div><h4>Ziggy</h4><div class="meta">Number 2, {M(8165)} lifetime<br>Lapsed since Apr 9, about 5.5 months<br>Tagged NO COVERS ALLOWED</div></div>
<div><p>On the night he subscribed he was sent eight near identical messages at $199.78 and $199.79 inside about 90 minutes, each relabelled (2), (3), (4), (5) as if it were something new, wrapped in escalating love bombing between the unlocks.</p>
<div class="q">I love you daddy... lifetime VIP status... I never spoil anyone like this</div>
<p>The session closes with: 'Seems like you're going to stay here with me forever, so I locked it so you can easily check it whenever you miss me.' That is a lock tactic, not a conversation. He spent somewhere between several hundred and over a thousand dollars in that one sitting and never subscribed again. In the 5.5 months since he has had no personal winback at all, only the same $5 to $25 bundle sends any stranger gets.</p>
{ladder(ZIGGY_PPVS)}<div class="lcap"><b>8 unlocks</b>at $199.78 and $199.79, about 90 minutes</div></div></div>
<div class="thread"><div><h4>Dan</h4><div class="meta">Number 4, {M(7563)} lifetime<br>Still active, highest risk<br>Tagged DO DAMAGE CONTROL, FAILED CAPTION FOR ULTRA SVIP</div></div>
<div><p>He asked a direct question about his status and never got an answer.</p>
<div class="q">Hey babe. Im a VIP on your free page but wanted to join here too... Does my VIP count here too?</div>
<p>The reply was 'Mmmmm since you already spoiled me ill send it for a lower price just for you', followed immediately by another paid send. Shortly after, a $60 tip was requested for a rate video on the claim that it normally sells for $300, which is pricing theatre rather than a real offer. His activity since, Sep 19 and 20, is cross promotion for other creators' pages.</p>
<p>The tag on his name says a paid message sent to him went out wrong and a chatter flagged it for follow up. That follow up never happened. He is a loyal cross page VIP, he is still paying, and he is the one to fix today.</p></div></div>
<div class="two"><div class="warnp"><h4>The same pattern in both</h4><p>Neither thread contains a single question about the fan himself. Ziggy was escalated through eight unlocks in one night. Dan asked a question and was answered with a price. In both cases the fan led and the page pushed, and in both cases nothing was written down afterwards.</p></div>
<div class="warnp"><h4>What it cost</h4><p>Ziggy has been gone 5.5 months with no personal message in that time. Dan is still paying and still waiting, which makes him the cheapest thing on this list to fix. Between them they represent {M(8165 + 7563)} in lifetime spend.</p></div></div>'''))
PP.append(page(8, f'''{head("08", "Thread by thread", "Tyler, Zach, <em>and the ones already gone.</em>", "Two threads that show the pattern, and three fans nobody went back for.")}
<div class="thread"><div><h4>Tyler</h4><div class="meta">Number 8, {M(3849)} lifetime<br>Lapsed since Jan 20, over 8 months<br>Tagged Pending VC and Dick Rate</div></div>
<div><p>His entire subscription month, Dec 20 and 21 2025, was bundle sends and urgency lines one after another with no actual conversation in between.</p>
<div class="q">$5 CUM BUNDLE... EPIC VAULT SALE... I'm never doing this again</div>
<p>Nothing in the thread shows the video call or the rate video he was tagged as owed ever being delivered. He left after one month and nobody approached him personally again in the eight months since.</p>
<p>He spent $3,849 in that one month, which puts him in the top ten of a page with over a hundred thousand fans on the list. A fan who spends that fast and leaves that quickly is usually a fan who ran out of reasons to stay, not one who ran out of money.</p></div></div>
<div class="thread"><div><h4>Zach</h4><div class="meta">Number 3, {M(7981)} lifetime<br>Lapsed Sep 13, 12 days ago<br>Tagged Custom Dr and 15min Vidcall</div></div>
<div><p>The one thread where someone genuinely tried. A $200 message was discounted to $149.78 with second chance messaging, and there were attempts to schedule the video call he was owed.</p>
<div class="q">I kept checking to see if you unlocked it...</div>
<p>He never unlocked it and lapsed anyway. The pressure went on the discount rather than on delivering the call he had already been promised. At 12 days lapsed he is the most recoverable name on the list.</p>
<p>He is also the clearest example of the order being wrong. He had already paid for something that had not arrived, and the next message he received was a discount on something else.</p></div></div>
<div class="thread"><div><h4 class="sm">Petros, arod761, Noah</h4><div class="meta">Numbers 5, 7 and 10<br>{M(4822)}, {M(4449)} and {M(3800)} lifetime<br>All lapsed</div></div>
<div><p>Petros is tagged VC PAID. He paid for a video call, went quiet around the time his subscription lapsed in August 2025, and has now been silent for over 13 months. His chat thread returns user not found, which usually means he deleted his account, so nobody can even ask whether that call happened.</p>
<p>arod761, lapsed 8 days, and Noah, lapsed about a year, now receive only cross promotion for other creators, the my bestie has an OnlyFans, go check her out sends for autumnren, vanessav and bronwina. Noah is still receiving those a full year after he stopped paying, which means no winback was ever attempted for a fan worth nearly $4,000.</p></div></div>
<div class="two"><div class="warnp"><h4>What all six have in common</h4><p>Not one of the six lapsed fans in your top ten received a personal message after they left. Not a check in, not an offer built from what they used to buy, not an acknowledgement that they had been one of the biggest spenders on the page. They were moved into the general list and sent the same thing as everyone else.</p></div>
<div class="warnp"><h4>What that is worth</h4><p>The six lapsed names in the top ten represent {M(8165 + 7981 + 4822 + 4449 + 3849 + 3800)} in proven lifetime spend. These are not cold leads. They are people who already decided this page was worth paying for, repeatedly, and then stopped hearing from anyone who knew that.</p></div></div>'''))
PP.append(page(9, f'''{head("09", "What works, what changes", "The page is not <em>the problem.</em>", "Your whale base, your best performing send and your best traffic source all still work. Four things need to change around them.")}
<div class="nums c4"><div><b>{M(TOP_LIFETIME)}</b><span>from your top fan, several more at $4K to $8K</span></div><div><b>25%</b><span>view rate on the $22 bundle, 22 sales, $484</span></div><div><b>{LINK_SUBS} subs</b><span>from one link, off {LINK_CLICKS:,} clicks</span></div><div><b>7 unread</b><span>all from the last few minutes</span></div></div>
<div class="asks4">
<div class="a4"><span class="lbl">01</span><h4>Cut the sending</h4><p>Once or twice a day at most, split into active and expired fans. Open rates recover when the list stops being hit every 20 minutes, and every other fix depends on this one.</p></div>
<div class="a4"><span class="lbl">02</span><h4>Find what stopped</h4><p>Traffic fell about {VIS_DROP}% from the January peak. Work out which marketing or promo activity ended around January and February 2026.</p></div>
<div class="a4"><span class="lbl">03</span><h4>Reuse the link that worked</h4><p>The Aug 4 creative, sweetalanna.pdf, turned {LINK_CLICKS:,} clicks into {LINK_SUBS} subscribers. Run it again, and judge the four new links once they have data.</p></div>
<div class="a4"><span class="lbl">04</span><h4>Handle the top ten personally</h4><p>Real notes on each of them, then outreach written from their own history. Dan first, then Zach at 12 days lapsed, then arod761 at 8 days.</p></div>
</div>
<div class="two"><div class="warnp"><h4>In what order</h4><p>Dan today, because he is still subscribed and still waiting on an answer. Zach this week, at 12 days lapsed, with the call he was promised rather than a discount. arod761 at 8 days after that. The sending schedule changes in parallel, because none of the personal outreach lands while the list is being hit ten times a day.</p></div>
<div class="warnp"><h4>What good looks like in 30 days</h4><p>Open rates back above 10% on a properly split list. Notes on every fan in the top ten. The three paid or promised services closed out. Two of the six lapsed whales back on the page. None of that requires new content or new traffic, only a different way of running the chats.</p></div></div>
<div class="close"><img src="__MARK__" alt=""><div><b>6 of 10</b><small>of your biggest spenders are gone</small></div>
<div><p>None of this is a content problem, none of it is random churn, and none of it needs new traffic to start fixing. <strong>The page has been run on autopilot sending instead of relationship management, and the fans who pay the most were handed a script.</strong></p><div class="sig">ALTR, September 25, 2026. Built from your own account data and full chat histories.</div></div></div>'''))
open("print-template.html", "w", encoding="utf-8").write('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Alanna. Account review by ALTR</title>'
    '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,62..125,100..900;1,62..125,100..900&family=Spline+Sans+Mono:wght@400;500&display=swap" rel="stylesheet">'
    "<style>" + PCSS + PX + "</style></head><body>" + "".join(PP) + "</body></html>")
print("built web + print")
