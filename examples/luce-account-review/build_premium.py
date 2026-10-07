# -*- coding: utf-8 -*-
"""Lucé transition audit, prepared by ALTR for Lucé. Two accounts: @itslucesworld (VIP) and @lucenextdoor (Free),
both run by the previous agency up to handover. Source: Derrek's diagnostic, Sep 28 2026.
Web scroll experience -> template.html, PDF reading edition -> print-template.html. Then run build.py."""
import html, os, json
os.chdir(os.path.dirname(os.path.abspath(__file__)))
E = html.escape
M = lambda n: (f"${n:,.2f}" if isinstance(n, float) and abs(n - round(n)) > 1e-6 else f"${n:,.0f}")

VIP_NET30, VIP_DROP, VIP_NET90 = 34_124, 27.8, 142_796
FREE_NET30, FREE_DROP = 8_391, 79.1
VIP_PEAK, VIP_TROUGH = 5_000, 400          # Jul 15-20 $4-6k/day, last week Sep $296-505/day
FREE_PEAK, FREE_TROUGH = 4_600, 135        # Jul 27-31 $4-5.2k/day, late Sep $30-240/day
FREE_COLLAPSE = 95
VIP_LIST, FREE_LIST = 42_000, 71_800
VAULT_VIEWS, VIP_BEST, VIP_WORST = 624, 435, 13
FREE_BEST, FREE_WORST = 239, 11
LETTER_PRICE, LETTERS_SENT, LETTERS_OPENED = 99.99, 5, 1
IG_CLICKS, IG_SUBS = 87_412, 4_474
OFTV_CLICKS, OFTV_SUBS = 16_073, 2_290
VIP_LINKS, S4S_CLICKS = 20, 1
COMMISSION = 35
PPV_LINE = "are you ready to suck my hard nips and make my pussy wet?"
LETTER_NAMES = "To William, To Marc, To Daddy, To Richard, To GONZO"
LETTERS = [LETTER_PRICE] * LETTERS_SENT

WH_VIP = [
    ("STEVE", "1", 22_400, "No note on the account", "Ten hours of his messages sitting unread"),
    ("David", "2", 10_700, "VIP 300/500, also on the free page", "A $150 bundle stalled after he asked why"),
    ("Jay Jay", "3", 9_500, "DNM, DON'T SPEND MORE, CRAZY", "Sent the same script as everyone else"),
    ("Kevin", "4", 7_900, "No note on the account", "No personal handling anywhere on record"),
    ("Ryan", "5", 7_300, "No note on the account", "No personal handling anywhere on record"),
    ("Steven", "6", 6_900, "No note on the account", "No personal handling anywhere on record"),
    ("Geoffrey", "7", 6_200, "200/800VIP", "Tracking note never resolved"),
]
WH_FREE = [
    ("David", "1", 3_300, "Cross subscribed to the VIP page", "Treated as two strangers, two pages"),
    ("Paco Hertz", "2", 2_600, "Saving to spoil later, LETTER", "A promised letter never followed up"),
    ("Drew", "3", 1_400, "NO MONEY VIP", "Written off, no winback attempted"),
]
for _w in WH_VIP + WH_FREE:
    assert len(_w[3]) <= 40, f"note too long for the table ({len(_w[3])}): {_w[3]}"
    assert len(_w[4]) <= 40, f"status too long for the table ({len(_w[4])}): {_w[4]}"
VIP_TOP_TOTAL = sum(w[2] for w in WH_VIP)
TOP3 = WH_VIP[0][2] + WH_VIP[1][2] + WH_VIP[2][2]


def ichart(cid, series, meta, w, h, xlabels, yfmt=None, show_val=None, hot=(), lw=None, fs=1.0):
    lw = lw or int(48 * fs)
    yfmt = yfmt or (lambda v: f"${v/1000:g}K" if v >= 1000 else f"${v:,.0f}")
    raw = max(max(series), 1)
    mx = next((c for c in [1, 5, 10, 25, 30, 50, 100, 200, 250, 500, 700, 1000, 2500, 5000, 6000, 10000, 20000, 25000, 40000, 50000, 60000, 100000, 150000] if c >= raw), raw)
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
vf = lambda v: f"{v:,.0f}"
m_vip = [{"t": "Jul 15 to 20", "l": "$4,000 to $6,000 a day", "s": "The peak, on a promo push."},
         {"t": "Last week of Sep", "l": "$296 to $505 a day", "s": "The floor, ten weeks later."}]
fig_vip = dual(ichart("c-vip", [VIP_PEAK, VIP_TROUGH], m_vip, 900, 400, ["Jul 15 to 20", "Last week of Sep"], hot=(0,), fs=2.2, show_val=["$4K to $6K", "$296 to $505"]),
               ichart("c-vip-m", [VIP_PEAK, VIP_TROUGH], m_vip, 420, 250, ["July", "Late Sep"], hot=(0,), fs=1.5, lw=52, show_val=["$4-6K", "$296-505"]))
m_free = [{"t": "Jul 27 to 31", "l": "$4,000 to $5,200 a day", "s": "290 to 505 transactions a day."},
          {"t": "Late Sep", "l": "$30 to $240 a day", "s": f"About {FREE_COLLAPSE}% below the peak."}]
fig_free = dual(ichart("c-free", [FREE_PEAK, FREE_TROUGH], m_free, 900, 400, ["Jul 27 to 31", "Late Sep"], hot=(0,), fs=2.2, show_val=["$4K to $5.2K", "$30 to $240"]),
                ichart("c-free-m", [FREE_PEAK, FREE_TROUGH], m_free, 420, 250, ["July", "Late Sep"], hot=(0,), fs=1.5, lw=52, show_val=["$4-5.2K", "$30-240"]))
m_blast = [{"t": "Vault unlock", "l": f"{VAULT_VIEWS} views", "s": "The one send with a game in it."},
           {"t": "Best ordinary send", "l": f"{VIP_BEST} views", "s": f"Out of about {VIP_LIST:,} fans."},
           {"t": "Worst send", "l": f"{VIP_WORST} views", "s": "Same list, same day."}]
fig_blast = dual(ichart("c-bl", [VAULT_VIEWS, VIP_BEST, VIP_WORST], m_blast, 900, 400, ["Vault unlock", "Best ordinary", "Worst"], hot=(0,), fs=2.2, yfmt=vf, show_val=[str(VAULT_VIEWS), str(VIP_BEST), str(VIP_WORST)]),
                 ichart("c-bl-m", [VAULT_VIEWS, VIP_BEST, VIP_WORST], m_blast, 420, 250, ["Vault", "Best", "Worst"], hot=(0,), fs=1.5, lw=46, yfmt=vf, show_val=[str(VAULT_VIEWS), str(VIP_BEST), str(VIP_WORST)]))

def ladder(tickets, w=210, h=40, cap=100, label="$99.99", opened=1):
    n = len(tickets); top = 13; base = h - 1; gap = 3.6; bw = min(26, (w - 64 - gap * (n - 1)) / n)
    o = [f'<svg class="lad" viewBox="0 0 {w} {h}" preserveAspectRatio="xMinYMid meet"><line x1="0" y1="{top}" x2="{w-60}" y2="{top}" stroke="#b6f2e5" stroke-width=".8" stroke-dasharray="2 2.5" opacity=".7"/>'
         f'<text x="{w}" y="{top+10}" text-anchor="end" font-size="10.5" fill="#b6f2e5" font-family="Spline Sans Mono, monospace">{label}</text>']
    for i, t in enumerate(tickets):
        bh = max(2, (base - top) * min(t, cap) / cap); x = i * (bw + gap)
        fill = "#b6f2e5" if i < opened else "rgba(182,242,229,.26)"
        o.append(f'<rect x="{x:.1f}" y="{base-bh:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx=".6" fill="{fill}"/>')
    return "".join(o) + "</svg>"

def ch(num, kicker, title, cid):
    return f'<header class="ch rv" id="{cid}"><div class="ch-meta"><span class="num">{num}</span><span class="kick">{E(kicker)}</span></div><h2>{title}</h2></header>'
def big(v, label): return f'<div class="big rv"><span class="bv">{v}</span><span class="bl">{E(label)}</span></div>'
def story(name, status, meta, body, quote, cite, more):
    q = f'<blockquote><p>{E(quote)}</p><cite>{E(cite)}</cite></blockquote>' if cite else f'<div class="sbig">{quote}</div>'
    return (f'<article class="story rv" tabindex="0"><div class="n"><h3>{E(name)}</h3><span class="st">{E(status)}</span></div><div class="h">{E(meta)}</div>'
            f'<p>{body}</p>{q}<div class="more"><div><p>{more}</p></div></div><span class="hint">More</span></article>')
def wrow(w, flag=False):
    name, rank, life, note, state = w
    return (f'<div class="lr{" hi" if flag else ""}" tabindex="0" data-rank="{rank}" data-name="{E(name)}" data-handle="Number {rank} by lifetime spend" '
            f'data-net="{M(life)}" data-last="{E(note)}" data-why="{E(state)}" data-move="{E(note)}">'
            f'<span class="ln">{rank}</span><span class="lw"><b>{E(name)}</b><i>{E(note)}</i></span><span class="r">{M(life)}</span>'
            f'<div class="lx"><div><b>{M(life)}</b><span>lifetime</span></div><p>{E(state)}</p></div></div>')
LH = '<div class="lh"><span class="ln">No.</span><span class="lw">Fan, and their note</span><span class="r">Lifetime</span></div>'
ledger_vip = f'<div class="ledger c">{LH}{"".join(wrow(w, w[0] in ("STEVE", "David", "Jay Jay")) for w in WH_VIP)}</div>'
ledger_free = f'<div class="ledger c">{LH}{"".join(wrow(w, True) for w in WH_FREE)}</div>'

BASE = open("creator_base.css", encoding="utf-8").read() + open("web_extra.css", encoding="utf-8").read()
EXTRA = """
h2{max-width:26ch}h2 em{display:block}
.asks{grid-template-columns:repeat(4,1fr)}
@media(max-width:920px){.asks{grid-template-columns:1fr}}
.warn{margin-top:44px;padding:28px 32px;border:1px solid rgba(182,242,229,.35);border-radius:6px;background:var(--wash)}
.warn h3{font-weight:300;font-size:26px;letter-spacing:-.02em}.warn p{margin-top:10px;color:var(--bone2);font-size:15px;max-width:72ch}
.warn p + p{margin-top:12px}
.lad{display:block;width:100%;height:auto;margin-top:16px;max-width:420px}
.bv,.method .m b,.spot .sg b,.readout .rl,.ledger .r{white-space:nowrap}
.fig figcaption{text-wrap:balance}
.ledger .lh,.ledger .lr{grid-template-columns:34px 1fr 96px}
.bigquote{margin-top:26px;border-left:2px solid var(--mint);padding:4px 0 4px 20px}
.bigquote p{font-weight:300;font-style:italic;font-size:22px;line-height:1.45;max-width:48ch;color:var(--bone)}
.bigquote cite{display:block;margin-top:10px;font-style:normal;font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--bone3)}
.pages{display:grid;grid-template-columns:1fr 1fr;gap:28px;margin-top:34px}
@media(max-width:920px){.pages{grid-template-columns:1fr;gap:20px}}
.pg-c{border:1px solid var(--line);border-radius:6px;padding:26px 28px}
.pg-c .tag{font-family:var(--mono);font-size:10px;letter-spacing:.18em;text-transform:uppercase;color:var(--mint)}
.pg-c h3{margin-top:10px;font-weight:300;font-size:30px;letter-spacing:-.02em}
.pg-c .hd2{margin-top:4px;font-family:var(--mono);font-size:11px;color:var(--bone3)}
.pg-c p{margin-top:14px;color:var(--bone2);font-size:15px;line-height:1.6}
"""
H = [f'''<div id="prog"></div><div id="glow"></div>
<nav id="nav"><a href="#top"><span>Luc&eacute;</span><i></i></a><a href="#c1"><span>Two pages</span><i></i></a><a href="#c2"><span>The sending</span><i></i></a><a href="#c3"><span>The script</span><i></i></a><a href="#c4"><span>Your top three</span><i></i></a><a href="#c5"><span>The rest</span><i></i></a><a href="#c6"><span>The funnel</span><i></i></a><a href="#c7"><span>What changes</span><i></i></a></nav>
<div class="dl-wrap"><a class="dl-btn" href="ALTR-luce-account-review-sep28.pdf" download="Luce-Account-Review-ALTR-Sep-2026.pdf">Download PDF</a></div>
<div class="page" id="top">
  <header class="mast"><img src="__LOGO__" alt="ALTR"><span>A transition audit prepared by ALTR for Luc&eacute;, confidential, September 28, 2026</span></header>
  <div class="hero">
    <h1><span>L</span><span>u</span><span>c</span><span>&eacute;</span><span>.</span></h1>
    <div>
      <p class="hook"><span><b>Both pages peaked in July.</b><b>Both have been falling since.</b></span><span><b>Your biggest fan has been</b><b>talking to nobody for ten hours.</b></span></p>
      <p class="sub">We pulled a full diagnostic across both accounts before taking anything over: @itslucesworld and @lucenextdoor. What they earn, what has been going out in your name, and how your biggest spenders have actually been handled. We read the real threads, not summaries. Everything here comes from your own live data.</p>
      <div class="who">Reviewed September 28, 2026<br>Prepared by ALTR for Luc&eacute;<br>Confidential</div>
      <a class="dl-inline" href="ALTR-luce-account-review-sep28.pdf" download="Luce-Account-Review-ALTR-Sep-2026.pdf">Download the PDF</a>
    </div>
    <div class="cue"><i></i>Scroll</div>
  </div>
  <div class="teaser">
    {big(f"{FREE_COLLAPSE}<small>%</small>", "collapse on the free page from its July peak to its September floor")}
    {big("10 hrs", f"of messages from your top spender, {M(22_400)} lifetime, every one of them unread")}
    {big("1 line", "recycled across both pages at every price from $4.99 to $14.99")}
  </div>
  <div class="method rv"><span class="ml">What we read</span>
    <div class="m"><b>2</b><span>accounts</span></div><div class="m"><b>90</b><span>days of revenue</span></div>
    <div class="m"><b>10</b><span>top spenders</span></div><div class="m"><b>Full</b><span>whale threads</span></div><div class="m"><b>{VIP_LINKS}</b><span>tracking links</span></div>
  </div>
  <nav class="toc rv"><span class="ml">Inside</span>
    <a href="#c1"><b>01</b><span>Two pages, one pattern</span></a><a href="#c2"><b>02</b><span>The sending</span></a><a href="#c3"><b>03</b><span>The script</span></a><a href="#c4"><b>04</b><span>Your top three</span></a>
    <a href="#c5"><b>05</b><span>The rest of the list</span></a><a href="#c6"><b>06</b><span>The funnel</span></a><a href="#c7"><b>07</b><span>What changes</span></a>
  </nav>''']

H.append(f'''<section>
  {ch("01", "Two pages, one pattern", "Both peaked in July. <em>Both have fallen since.</em>", "c1")}
  <div class="spread">
    <div class="rv"><p class="lead">The VIP page took <em>{M(VIP_NET30)} net in the last 30 days, down {VIP_DROP}%</em>. The free page took {M(FREE_NET30)}, down {FREE_DROP}%.</p>
      <div class="prose" style="margin-top:16px"><p>The 90 day figure on VIP, {M(VIP_NET90)}, looks healthy until you see where it came from. Almost all of it sits in one burst between July 15 and 20, where the page ran at $4,000 to $6,000 a day on a promo push. Every week since has been lower than the one before, bottoming at $296 to $505 a day in the final week of September.</p>
      <p>The free page did the same thing five days later and fell harder. July 27 to 31 ran $4,000 to $5,200 a day on 290 to 505 transactions. By late September it was doing $30 to $240. That is the page whose entire job is to feed the VIP page.</p></div></div>
    <div class="stack">{big(M(VIP_NET30), f"VIP net in 30 days, down {VIP_DROP}%")}{big(M(FREE_NET30), f"free page net in 30 days, down {FREE_DROP}%")}{big("1 burst", "in July accounts for most of the 90 day total")}</div>
  </div>
  <div class="pages">
    <div class="pg-c rv"><span class="tag">VIP</span><h3>@itslucesworld</h3><div class="hd2">{M(VIP_NET30)} net in 30 days, {M(VIP_NET90)} in 90</div>
      <p>Slid every week after the July push. A small bump on Sep 26 and 27, around $1,600 a day, comes from the free trial promo that has only just launched, not from anything the chat team changed.</p></div>
    <div class="pg-c rv"><span class="tag">Free</span><h3>@lucenextdoor</h3><div class="hd2">{M(FREE_NET30)} net in 30 days, down {FREE_DROP}%</div>
      <p>About a {FREE_COLLAPSE}% fall from peak to trough. No recovery attempt shows anywhere in the data. The funnel that is supposed to fill the VIP page has effectively been left to run down.</p></div>
  </div>
  <div class="figs">
    {fig(fig_vip, "VIP daily net, the July peak against the September floor. <em>Mint is the peak.</em>", m_vip[1])}
    {fig(fig_free, f"Free page daily net. <em>About {FREE_COLLAPSE}% down from peak to trough.</em>", m_free[1])}
  </div>
</section>''')

H.append(f'''<section>
  {ch("02", "The sending", "A send every hour, <em>around the clock.</em>", "c2")}
  <div class="spread">
    <div class="rv"><p class="lead">The VIP list gets a mass message <em>every 45 to 60 minutes, day and night</em>, to about {VIP_LIST:,} fans. View rates have fallen under 1%.</p>
      <div class="prose" style="margin-top:16px"><p>Individual sends are being seen by between {VIP_WORST} and {VIP_BEST} people. The free page is worse: about {FREE_LIST:,} recipients a send and {FREE_WORST} to {FREE_BEST} views, well under half a percent.</p>
      <p>One send broke the pattern. A vault unlock with a game built into it pulled {VAULT_VIEWS} views, more than any ordinary send on the page. The creative still works when somebody bothers to make it. They have simply stopped trying, and gone back to volume on a list that has learned to ignore it.</p></div></div>
    <div class="stack">{big("45 to 60", "minutes between sends on the VIP page, around the clock")}{big(f"{VIP_WORST} to {VIP_BEST}", f"views per send out of about {VIP_LIST:,} fans")}{big(f"{VAULT_VIEWS}", "views on the one send with a game in it")}</div>
  </div>
  {fig(fig_blast, "Views per send on the VIP page. <em>Mint is the vault unlock.</em>", m_blast[0])}
  <div class="warn rv"><h3>Neither list is being split</h3><p>Every send goes to everybody. Active fans, expired fans, people who have spent five figures and people who have never spent a cent all receive the same message at the same price at the same moment. Fans mute what they cannot use, and OnlyFans quietly deprioritises accounts that send at this rate. Until the sending changes, nothing else on either page gets a fair test, because the offers are not reaching the inbox.</p></div>
</section>''')

H.append(f'''<section>
  {ch("03", "The script", "One line, <em>both pages, every price.</em>", "c3")}
  <div class="spread eq rv" style="margin-top:30px">
    <p class="lead">The same paid message is going out across both accounts at <em>every price from $4.99 to $14.99</em>, to different fans within minutes of each other.</p>
    <div class="prose"><p>Most of them record zero opens and zero purchases. The price moves, the words never do. Nothing in it is tailored to the fan receiving it, which is why the same line can be sent three times in an hour without anyone noticing.</p></div>
  </div>
  <div class="bigquote rv"><p>{E(PPV_LINE)}</p><cite>Sent on both pages, $4.99 to $14.99, mostly zero opens</cite></div>
  <div class="warn rv"><h3>And the {M(LETTER_PRICE)} letters</h3>
    <p>The VIP page also runs a batch of appreciation letters at {M(LETTER_PRICE)} each. They are the same template with the name swapped: {E(LETTER_NAMES)}. One of the five shown was opened at all.</p>
    <p>A hundred dollar message that is meant to read as personal, sent as a mail merge, to the people who spend the most on the page. That is the whole problem in one product.</p>
    {ladder(LETTERS, opened=LETTERS_OPENED)}
    <p style="font-size:13px;color:var(--bone3);margin-top:8px">Five letters at {M(LETTER_PRICE)}. The solid bar is the only one that was opened.</p>
  </div>
  <div class="row4">
    {big("$4.99", "the low end the same line was sent at")}
    {big("$14.99", "the high end, same words")}
    {big(f"{LETTERS_OPENED} of {LETTERS_SENT}", f"{M(LETTER_PRICE)} letters that were opened")}
    {big("0", "sign of the message being written for the fan")}
  </div>
</section>''')

H.append(f'''<section>
  {ch("04", "Your top three", "Silence, a bad ask, <em>and a flag ignored.</em>", "c4")}
  <div class="spread eq rv" style="margin-top:30px">
    <p class="lead">Your three biggest fans on the VIP page are worth <em>{M(TOP3)} between them.</em> We read all three threads in full.</p>
    <div class="prose"><p>None of them is getting the handling their spend should command. One is being ignored outright, one was pushed into a sale nobody explained, and one is being sent the same mass copy as everybody else despite a warning sitting on his own file.</p></div>
  </div>
  <div class="stories">
    {story("STEVE", f"{M(22_400)}, number one", "Ten hours of messages, all unread",
      "Between 5:05am and 2:57pm on Sep 28 he wrote at length about his life. Two young kids, a marriage he describes as high conflict, chronic fatigue, coming out of a depressive episode, being on medication. He asked her to check in on him and to remind him to stay safe.",
      "Every one of those messages is still marked unopened.", "Sep 28, 5:05am to 2:57pm",
      "Nobody on the team has read them. There is no sales attempt anywhere in the thread, which is not the problem: the problem is that the single biggest spender on the account is carrying a real conversation on his own and getting nothing back. That is the clearest retention risk on the page. It also needs a proper approach written down, because a fan is disclosing medication and depression to this account and there is currently no guidance at all for how that gets handled.")}
    {story("David", f"{M(10_700)}, number two", "VIP 300/500, also on the free page",
      "He asked for one video. The chatter came back with a bundle of four for $150. He pushed back and asked directly why it had jumped to four.",
      "you're close to my heart", "The whole justification he was given",
      "That was the answer. No reason, no value, nothing he could say yes to. Two nudges followed, 'are you still there david?', more than 90 minutes apart, with no reply in between. He is also your number one on the free page at $3,300, and the two pages are treating him as two different strangers.")}
    {story("Jay Jay", f"{M(9_500)}, number three", "Flagged DNM, DON'T SPEND MORE, CRAZY",
      "Somebody on the team wrote an explicit warning on his file. Despite that, he is receiving the standard VAULT UNLOCK mass script at $12.34, the same one sent word for word to David, plus an earlier free custom ticket push at $12.69.",
      "No notes driven approach, no caution, just the canned copy.", "What his thread actually contains",
      "A fan the team themselves marked as volatile is being run through the exact same automated sequence as everyone else. The flag was written and then ignored, which makes it worse than not having written it, because it shows somebody saw the risk and nothing changed.")}
  </div>
</section>''')

H.append(f'''<section>
  {ch("05", "The rest of the list", "Notes written, <em>then left to rot.</em>", "c5")}
  <div class="spread rev rv" style="margin-top:24px">
    <p class="lead">Your top seven on VIP are worth <em>{M(VIP_TOP_TOTAL)} in lifetime spend.</em> Four of them have no note of any kind.</p>
    <div class="prose"><p>Where notes do exist they read as unfinished business rather than knowledge. Geoffrey carries a tracking note nobody closed. On the free page, Paco Hertz was promised a letter that never shows up in the thread, and Drew was written off in a note with no winback attempted. <span class="web"><span class="t-h">Move down the list and the card follows you.</span><span class="t-t">Tap a fan for the detail.</span></span></p></div>
  </div>
  <div class="whales">
    <aside class="spot rv" id="spot">
      <div class="sr">Number <b id="s-rank">1</b> by lifetime spend</div>
      <h3 id="s-name">{E(WH_VIP[0][0])}</h3><div class="sh" id="s-handle">Number 1 by lifetime spend</div>
      <div class="sg"><div><b id="s-net">{M(22_400)}</b><span>lifetime</span></div></div>
      <div class="sa"><b>The note on his file</b><span id="s-last">{E(WH_VIP[0][3])}</span></div>
      <div class="sa"><b>What is happening</b><span id="s-why">{E(WH_VIP[0][4])}</span></div>
      <div class="sa" style="display:none"><span id="s-move"></span></div>
      <div class="tip">Hover or tap a fan</div>
    </aside>
    <div class="twin" style="margin-top:0">
      <div><div class="ml" style="margin-bottom:10px">VIP, @itslucesworld</div>{ledger_vip}</div>
      <div><div class="ml" style="margin-bottom:10px">Free, @lucenextdoor</div>{ledger_free}</div>
    </div>
  </div>
  <div class="warn rv"><h3>What a note is supposed to be</h3><p>A note on a top spender should tell the next person who opens that chat what he buys, what he has been promised and how he wants to be spoken to. On these two pages the notes record a price band, a warning, or an unfinished promise, and then nothing was done with any of them. Four of your seven biggest VIP fans have nothing written on them at all, so whoever opens those chats is starting from zero every time.</p></div>
</section>''')

H.append(f'''<section>
  {ch("06", "The funnel", "The two links that work <em>have not been touched.</em>", "c6")}
  <div class="spread">
    <div class="rv"><p class="lead">Of <em>{VIP_LINKS} tracking links on the VIP page, almost all sit at zero clicks.</em> Yerba Link, ggswaps_manager_50, Fanstats, Dating Apps, Ad Set number one, Chatterbate, and more.</p>
      <div class="prose" style="margin-top:16px"><p>Two links carry the entire page. Your main Instagram link has brought {IG_CLICKS:,} clicks and {IG_SUBS:,} subscribers. OFTV has brought {OFTV_CLICKS:,} clicks and {OFTV_SUBS:,} subscribers. Neither has been refreshed since December 2025 and the middle of 2025 respectively.</p>
      <p>The newest thing built was a Lucé S4S link on Sep 3. It has {S4S_CLICKS} click. That is the entire marketing effort of the last month on the page that earns the most.</p>
      <p>The free page is better run here, which makes the VIP neglect harder to explain. Somebody has been putting out monthly sub recapture links from April through September, each pulling 19 to 82 subscribers. But its main Instagram link has sat at zero clicks since March 2025, a dead front door nobody fixed in eighteen months.</p></div></div>
    <div class="stack">{big(f"{IG_SUBS:,}", f"subscribers from your main Instagram link, off {IG_CLICKS:,} clicks")}{big(f"{OFTV_SUBS:,}", f"from OFTV, off {OFTV_CLICKS:,} clicks")}{big(f"{S4S_CLICKS} click", "on the only new link built in the last month")}</div>
  </div>
  <div class="warn rv"><h3>And nobody can tell you what either page actually makes</h3>
    <p>Commission is configured at {COMMISSION}% on both accounts, but no costs have been entered on either one. That means real profit and margin cannot be calculated for either page, for any period.</p>
    <p>For the whole time this setup has been running, nobody has been able to answer what a promo actually returned or what a month actually cleared. Decisions were being made on gross revenue alone, which is how a page can look fine in a 90 day total while every single week inside it gets worse.</p></div>
</section>''')

H.append(f'''<section>
  {ch("07", "What changes", "Five things, <em>in order.</em>", "c7")}
  <div class="asks rv">
    <div><b data-n="01">Answer Steve today</b><p>Ten hours of unread messages on the fan who has spent {M(22_400)}. Someone reads the whole thread and replies properly, with nothing attached to it, and a written approach for how this fan is handled from here.</p></div>
    <div><b data-n="02">Cut the sending</b><p>Once or twice a day on each page instead of hourly, split into active and expired. The vault unlock proves the list still responds when the send is worth opening.</p></div>
    <div><b data-n="03">Retire the script</b><p>One recycled line at six price points and a mail merged {M(LETTER_PRICE)} letter is not chatting. Real notes on the top ten first, then copy written off what each fan actually buys.</p></div>
    <div><b data-n="04">Rebuild the VIP funnel</b><p>Two links carry the page and both are over nine months stale. Refresh them, kill the {VIP_LINKS - 3} dead ones, and copy the free page's monthly recapture habit across.</p></div>
  </div>
  <div class="plan">
    <div class="step rv"><div class="w">Today</div><h3>Open Steve's thread</h3><p>He has been writing into silence since 5:05am. He is your biggest spender and the most personal relationship on the account, and right now it is the one nobody has looked at. Read it, reply as a person, and write down how this fan is to be handled before anyone sells him anything again.</p></div>
    <div class="step rv" style="transition-delay:.12s"><div class="w">This week</div><h3>Close David and settle Jay Jay</h3><p>David asked a fair question and got nothing. Go back with either a reason for the four video bundle or a smaller ask he can actually say yes to, and start treating him as one fan across both pages. Jay Jay comes off the mass sends entirely until there is a real approach on his file.</p></div>
    <div class="step rv" style="transition-delay:.24s"><div class="w">This month</div><h3>Turn the lights on</h3><p>Costs entered on both accounts so profit and margin can be read for the first time. Until that exists, nobody can tell whether a promo made money or just moved it.</p></div>
  </div>
  <div class="close rv"><img src="__MARK__" alt="" aria-hidden="true">
    <div class="cb"><span>{M(TOP3)}</span><small>sitting in your top three threads</small></div>
    <div><p>Neither page has a content problem and neither needs new traffic to start recovering. <em>Both were run on volume and a script while the people who actually pay were left to handle themselves.</em></p><div class="sig">ALTR, September 28, 2026</div></div>
  </div>
  <footer><img src="__LOGO__" alt="ALTR"><span>Prepared by ALTR for Luc&eacute;. Built from live data across both accounts and the full whale threads. Confidential.</span></footer>
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
        '<title>Lucé. Account review by ALTR</title><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,62..125,100..900;1,62..125,100..900&family=Spline+Sans+Mono:wght@400;500&display=swap" rel="stylesheet">')
open("template.html", "w", encoding="utf-8").write('<!DOCTYPE html><html lang="en"><head>' + HEAD + "<style>" + BASE + EXTRA + "</style></head><body>" + "\n".join(H) + JS + "</body></html>")

# ------------------------------------------------------------------ PDF reading edition
PCSS = open("print_base.css", encoding="utf-8").read()
TOT = 10
CH = {1: "transition audit", 2: "the short version", 3: "where it stands", 4: "the sending", 5: "the script",
      6: "your top three", 7: "your top three", 8: "the rest of the list", 9: "the funnel", 10: "what changes"}
NX = {1: "Turn the page, the short version", 2: "Next, where it stands", 3: "Next, the sending", 4: "Next, the script",
      5: "Next, your top three", 6: "Next, David and Jay Jay", 7: "Next, the rest of the list", 8: "Next, the funnel",
      9: "Next, what changes", 10: "Start with Steve"}
def page(n, body, cls=""):
    ghost = '<img class="ghost" src="__GHOST__" alt="">' if cls == "cover" else ""
    return (f'<section class="pg {cls}">{ghost}<header class="run"><img src="__LOGO__" alt="ALTR"><span>Luc&eacute;, {CH[n]}</span></header><div class="body">{body}</div>'
            f'<footer class="foot"><span>Prepared by ALTR for Luc&eacute;</span><span class="nx">{NX[n]}</span><span>{n:02d} / {TOT:02d}</span></footer></section>')
def head(num, kicker, title, line):
    return f'<div class="hd"><div class="hn"><b>{num}</b><span>{E(kicker)}</span></div><div class="ht"><h2>{title}</h2><p>{line}</p></div></div>'
def fnd(v, t, hi=False): return '<div%s><b>%s</b><p>%s</p></div>' % (' class="hi"' if hi else '', v, t)
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
.kn .lad{margin-top:auto;padding-top:3mm}
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
def qrows(rows, maxv):
    return "".join(
        f'<tr><td class="n">{r[1]}</td><td class="fan"><b>{E(r[0])}</b><i>{E(r[3])}</i></td>'
        f'<td class="bar"><span><i style="width:{r[2]/maxv*100:.0f}%"></i></span></td><td class="num">{M(r[2])}</td><td>{E(r[4])}</td></tr>' for r in rows)
QH = '<thead><tr><th>No.</th><th>Fan, and the note left on them</th><th></th><th class="num">Lifetime</th><th>What is happening</th></tr></thead>'

PP = []
PP.append(page(1, f'''<div class="cv-top"><div class="meta" style="margin:0 0 3mm">Transition audit, @itslucesworld and @lucenextdoor</div><h1>Luc&eacute;<i>.</i></h1>
<div class="hook">Both pages peaked in July and have fallen since.<em>Your top fan wrote for ten hours. Nobody read it.</em></div><div class="meta">Prepared by ALTR for Luc&eacute;, September 28, 2026. Confidential.</div></div>
<div class="letter"><div class="lbl">Read first</div><div><p>Before taking anything over we pulled a full diagnostic across both of your accounts. What each one earns, what has been going out in your name, and how your biggest spenders have actually been handled. We read the real threads, not summaries.</p>
<p>Page two is the short version. The pages after it show the evidence and the five things that change.</p><div class="sig">ALTR</div></div></div>
<div class="nums c3"><div><b>{FREE_COLLAPSE}%</b><span>collapse on the free page</span></div><div><b>10 hrs</b><span>unread, from your top fan</span></div><div><b>1 line</b><span>recycled on both pages</span></div></div>
<div class="toc"><div class="lbl">Inside</div><ol><li>The short version<span>02</span></li><li>Where it stands<span>03</span></li><li>The sending<span>04</span></li><li>The script<span>05</span></li><li>Your top three<span>06</span></li><li>The rest of the list<span>08</span></li><li>The funnel<span>09</span></li><li>What changes<span>10</span></li></ol></div>''', "cover"))

PP.append(page(2, f'''{head("02", "The short version", "Everything on one page. <em>Start here.</em>", "What we found across both accounts, the sending, the script and the ten biggest spenders.")}
<div><div class="lbl" style="margin-bottom:2mm">What we found</div><div class="find">
{fnd("10 hours", f"Of messages from STEVE, your biggest fan at {M(22_400)} lifetime, every one of them still marked unread. No reply, no acknowledgement, nobody has opened the thread.", True)}
{fnd(f"{FREE_DROP}%", f"Down on the free page in 30 days, {M(FREE_NET30)} net. About a {FREE_COLLAPSE}% collapse from its July peak. VIP is down {VIP_DROP}% to {M(VIP_NET30)}.")}
{fnd("Every hour", f"A mass message goes out to about {VIP_LIST:,} VIP fans every 45 to 60 minutes around the clock. Views have fallen to between {VIP_WORST} and {VIP_BEST} a send.")}
{fnd("1 line", f"The same paid message runs on both pages at every price from $4.99 to $14.99, mostly with zero opens. The {M(LETTER_PRICE)} appreciation letters are the same template with the name swapped.")}
{fnd("4 of 7", "Of your biggest VIP fans have no note of any kind. The notes that do exist record a warning or an unfinished promise that nobody acted on.")}
</div></div>
<div><div class="lbl" style="margin-bottom:2.5mm">Three fans that explain it</div><div class="know">
<div class="kn"><span class="lbl">Ignored</span><h4>STEVE</h4><p>{M(22_400)} lifetime. Ten hours of personal messages on Sep 28, all unopened. No sales attempt, and no reply either.</p></div>
<div class="kn"><span class="lbl">Oversold</span><h4>David</h4><p>{M(10_700)} lifetime. Asked for one video, offered four for $150, asked why, and was told he is close to her heart.</p></div>
<div class="kn"><span class="lbl">Flag ignored</span><h4>Jay Jay</h4><p>{M(9_500)} lifetime. Flagged DON'T SPEND MORE, then sent the same $12.34 mass script as everyone else.</p></div>
</div></div>
<div><div class="lbl" style="margin-bottom:2.5mm">What needs to change</div><div class="wk">
<div><span class="lbl">Today</span><h4>Answer Steve</h4><p>Read the whole thread and reply as a person, with nothing for sale attached, then write down how he is handled.</p></div>
<div><span class="lbl">This week</span><h4>Cut the sending</h4><p>Once or twice a day per page, split into active and expired, instead of a blast every 45 minutes.</p></div>
<div><span class="lbl">This month</span><h4>Turn the lights on</h4><p>No costs are configured on either account, so nobody can calculate profit or margin for any period.</p></div></div></div>'''))

PP.append(page(3, f'''{head("03", "Where it stands", "Both peaked in July. <em>Both have fallen since.</em>", f"VIP took {M(VIP_NET30)} net in the last 30 days, down {VIP_DROP}%. The free page took {M(FREE_NET30)}, down {FREE_DROP}%.")}
<div class="two"><div class="chart">{ichart("p-vip", [VIP_PEAK, VIP_TROUGH], [{}]*2, 900, 1180, ["Jul 15 to 20", "Last week of Sep"], hot=(0,), fs=2.8, show_val=["$4-6K", "$296-505"])}<div class="cap">VIP daily net, peak against floor. <em>Mint is July.</em></div></div>
<div class="chart">{ichart("p-free", [FREE_PEAK, FREE_TROUGH], [{}]*2, 900, 1180, ["Jul 27 to 31", "Late Sep"], hot=(0,), fs=2.8, show_val=["$4-5.2K", "$30-240"])}<div class="cap">Free page daily net. <em>About {FREE_COLLAPSE}% down.</em></div></div></div>
<div class="acct">
<div class="ac"><span class="tag">VIP</span><h4>@itslucesworld</h4><div class="fig2">{M(VIP_NET30)} in 30 days, {M(VIP_NET90)} in 90</div>
<p>The 90 day figure looks healthy only because of one burst between July 15 and 20. Every week since has been lower than the one before. The small bump on Sep 26 and 27, around $1,600 a day, comes from the free trial promo that has only just launched.</p></div>
<div class="ac"><span class="tag">Free</span><h4>@lucenextdoor</h4><div class="fig2">{M(FREE_NET30)} in 30 days, down {FREE_DROP}%</div>
<p>Peaked five days after VIP on 290 to 505 transactions a day, then bled down to $30 to $240. No recovery attempt appears anywhere in the data, on the one page whose entire job is to fill the VIP page.</p></div></div>'''))

PP.append(page(4, f'''{head("04", "The sending", "A send every hour, <em>around the clock.</em>", f"The VIP list gets a mass message every 45 to 60 minutes, day and night, to about {VIP_LIST:,} fans. View rates have fallen under 1%.")}
<div class="chart">{ichart("p-bl", [VAULT_VIEWS, VIP_BEST, VIP_WORST], [{}]*3, 900, 470, ["Vault unlock", "Best ordinary send", "Worst send"], hot=(0,), fs=1.5, yfmt=vf, show_val=[str(VAULT_VIEWS), str(VIP_BEST), str(VIP_WORST)])}<div class="cap">Views per send on the VIP page. <em>Mint is the vault unlock.</em></div></div>
<div class="nums c4"><div><b>45 to 60</b><span>minutes between VIP sends</span></div><div><b>{VIP_WORST} to {VIP_BEST}</b><span>views per VIP send</span></div><div><b>{FREE_WORST} to {FREE_BEST}</b><span>per send on the free page</span></div><div><b>{VAULT_VIEWS}</b><span>views on the gamified send</span></div></div>
<div class="warnp"><h4>Neither list is being split</h4><p>Every send goes to everybody. Active fans, expired fans, people who have spent five figures and people who have never spent a cent all get the same message at the same price at the same moment. Fans mute what they cannot use, and OnlyFans quietly deprioritises accounts that send at this rate. Until this changes, nothing else on either page gets a fair test, because the offers are not reaching the inbox.</p></div>
<div class="warnp"><h4>The one send that worked</h4><p>A vault unlock with a game built into it pulled {VAULT_VIEWS} views, more than any ordinary send on the page. The creative still works when somebody bothers to make it. That is the proof the list is not dead, it is bored, and the answer was already in their own data.</p></div>'''))

PP.append(page(5, f'''{head("05", "The script", "One line, <em>both pages, every price.</em>", "The same paid message goes out across both accounts at every price from $4.99 to $14.99, to different fans within minutes of each other.")}
<div class="pq">{E(PPV_LINE)}<cite>Sent on both pages, $4.99 to $14.99, mostly zero opens and zero purchases</cite></div>
<div class="nums c4"><div><b>$4.99</b><span>the low end it was sent at</span></div><div><b>$14.99</b><span>the high end, same words</span></div><div><b>{LETTERS_OPENED} of {LETTERS_SENT}</b><span>{M(LETTER_PRICE)} letters opened</span></div><div><b>0</b><span>written for the fan</span></div></div>
<div class="warnp"><h4>The {M(LETTER_PRICE)} appreciation letters</h4>
<p>The VIP page runs a batch of appreciation letters at {M(LETTER_PRICE)} each. They are one template with the name swapped: {E(LETTER_NAMES)}. One of the five shown was opened at all.</p>
<p>A hundred dollar message whose entire premise is that it was written for one person, sent as a mail merge, to the people who spend the most on the page. That is the whole problem in a single product.</p>
{ladder(LETTERS, opened=LETTERS_OPENED)}<div class="lcap"><b>1 of 5</b>opened, solid bar</div></div>
<div class="warnp"><h4>Both accounts are running it at once</h4><p>The same line is live on the VIP page and on the free page at the same time. A fan subscribed to both, which David is, receives the identical message twice from what are supposed to be two different experiences at two different price points. Nothing distinguishes the paid page from the free one in his inbox.</p></div>
<div class="warnp"><h4>Why the price moving does not help</h4><p>The same line at $4.99 and at $14.99 is not a test, because nothing else about it changed. Sending it to different fans within minutes of each other means the page cannot learn anything from the result either. Most of these record zero opens and zero purchases, and that outcome has not changed the approach.</p></div>'''))

PP.append(page(6, f'''{head("06", "Your top three", "Ten hours of messages, <em>every one unread.</em>", f"Your three biggest VIP fans are worth {M(TOP3)} between them. We read all three threads in full. This is the first.")}
<div class="thread"><div><h4>STEVE</h4><div class="meta">Number 1, {M(22_400)} lifetime<br>Active<br>No note on his file</div></div>
<div><p>Between 5:05am and 2:57pm on Sep 28 he wrote at length about his own life. Two young kids, a marriage he describes as high conflict, chronic fatigue, coming out of a depressive episode, being on medication. He asked her to check in on him and to remind him to stay safe.</p>
<div class="q">Every one of those messages is still marked unopened.</div>
<p>Nobody on the team has read them. There is no sales attempt anywhere in the thread, and that is not the problem. The problem is that the single biggest spender on the account is carrying a real relationship on his own and getting nothing back at all. That is the clearest retention risk on either page.</p>
<p>It also needs an approach written down. A fan is disclosing medication, depression and marriage trouble to this account, and there is currently no guidance anywhere for how that gets handled or by whom.</p></div></div>
<div><div class="lbl" style="margin-bottom:2.6mm">What he wrote about, in his own thread</div>
<div class="chips"><span>Two young kids</span><span>A high conflict marriage</span><span>Chronic fatigue</span><span>Coming out of a depressive episode</span><span>On medication</span><span class="k">Asked her to check in on him</span><span class="k">Asked to be reminded to stay safe</span></div></div>
<div class="two"><div class="warnp"><h4>What this costs if it keeps going</h4><p>{M(22_400)} of lifetime spend sits in this one thread, more than double the next fan. A whale who is answered by silence does not usually complain first. He simply stops writing, and the page finds out a month later when the revenue moves.</p></div>
<div class="warnp"><h4>What good looks like here</h4><p>Read and respond inside the hour, from someone who has read all of it. Then a short written note on his file: what he talks about, what he has asked for, and where the line sits, so the next person is not guessing.</p></div></div>'''))

PP.append(page(7, f'''{head("07", "Your top three", "A bad ask, <em>and a flag ignored.</em>", "Your second and third biggest fans on the VIP page, worth $20,200 between them.")}
<div class="thread"><div><h4>David</h4><div class="meta">Number 2, {M(10_700)} lifetime<br>Also number 1 on the free page at {M(3_300)}<br>Noted VIP 300/500</div></div>
<div><p>He asked for one video. The chatter came back with a bundle of four for $150. He pushed back and asked directly why it had jumped to four.</p>
<div class="q">you're close to my heart</div>
<p>That was the justification. No reason, no added value, nothing he could say yes to. Two nudges followed, 'are you still there david?', more than 90 minutes apart, with no reply in between. The deal is sitting stalled on a question that was never answered.</p>
<p>He is also your biggest fan on the free page, and the two accounts are treating him as two different strangers. Nothing in either thread shows anyone knows he is the same person.</p></div></div>
<div class="thread"><div><h4>Jay Jay</h4><div class="meta">Number 3, {M(9_500)} lifetime<br>Active<br>Flagged DNM, DON'T SPEND MORE, CRAZY</div></div>
<div><p>Somebody on the team wrote an explicit warning on his file. Despite that, he is receiving the standard VAULT UNLOCK mass script at $12.34, the same one sent word for word to David, plus an earlier free custom ticket push at $12.69.</p>
<div class="q">No notes driven approach, no caution, just the canned copy.</div>
<p>A fan the team themselves marked as volatile is being run through the identical automated sequence as everyone else. The flag was written and then ignored, which is worse than never writing it, because it shows somebody saw the risk and nothing changed.</p></div></div>
<div class="nums c4"><div><b>4 for $150</b><span>after he asked for one</span></div><div><b>90 min</b><span>between his two nudges</span></div><div><b>$12.34</b><span>the same script to both fans</span></div><div><b>$14,000</b><span>David, across both pages</span></div></div>
<div class="warnp"><h4>The pattern across all three</h4><p>Total silence on Steve, an unjustified upsell on David, copy paste blasts on Jay Jay despite an active risk flag. Three different failures, one cause: nobody is reading these threads before they send into them.</p></div>'''))

PP.append(page(8, f'''{head("08", "The rest of the list", "Notes written, <em>then left to rot.</em>", f"Your top seven on VIP are worth {M(VIP_TOP_TOTAL)} in lifetime spend. Four of them have no note of any kind.")}
<div class="lbl">VIP, @itslucesworld</div>
<table class="qt">{QH}<tbody>{qrows(WH_VIP, 22_400)}</tbody></table>
<div class="lbl">Free, @lucenextdoor</div>
<table class="qt">{QH}<tbody>{qrows(WH_FREE, 22_400)}</tbody></table>
<div class="warnp"><h4>What a note is supposed to be</h4><p>A note on a top spender should tell the next person who opens that chat what he buys, what he has been promised and how he wants to be spoken to. Here they record a price band, a warning or an unfinished promise, and then nothing was done with any of them. Geoffrey's tracking note was never closed. Paco Hertz was promised a letter that never appears in his thread. Drew was written off in writing without a single winback attempt.</p></div>'''))

PP.append(page(9, f'''{head("09", "The funnel", "The two links that work <em>have not been touched.</em>", f"Of {VIP_LINKS} tracking links on the VIP page, almost all sit at zero clicks.")}
<div class="nums c4"><div><b>{IG_SUBS:,}</b><span>subs from your main IG link</span></div><div><b>{OFTV_SUBS:,}</b><span>subs from OFTV</span></div><div><b>{S4S_CLICKS} click</b><span>on the newest link, Sep 3</span></div><div><b>{COMMISSION}%</b><span>commission set, no costs</span></div></div>
<div class="warnp"><h4>VIP: the marketing funnel is effectively dead</h4><p>Yerba Link, ggswaps_manager_50, Fanstats, Dating Apps, Ad Set number one, Chatterbate and more all sit at zero clicks each. The newest thing built was a Luc&eacute; S4S link on Sep 3, which has {S4S_CLICKS} click on it. That is the entire marketing effort of the last month on the account that earns the most.</p></div>
<div class="warnp"><h4>Two links are carrying the whole page</h4><p>Your main Instagram link has brought {IG_CLICKS:,} clicks and {IG_SUBS:,} subscribers. OFTV has brought {OFTV_CLICKS:,} clicks and {OFTV_SUBS:,} subscribers. Between them that is {IG_SUBS + OFTV_SUBS:,} subscribers off two pieces of creative, and neither has been refreshed since December 2025 and the middle of 2025 respectively. The things that work are the things nobody has touched.</p></div>
<div class="warnp"><h4>Free: better run, which makes VIP harder to explain</h4><p>Somebody has been putting out monthly sub recapture links from April through September, each pulling 19 to 82 subscribers. So the habit exists on one page and simply was not applied to the other. Its own main Instagram link, though, has sat at zero clicks since March 2025, a dead front door nobody fixed in eighteen months.</p></div>
<div class="warnp"><h4>And nobody can tell you what either page actually makes</h4><p>Commission is configured at {COMMISSION}% on both accounts, but no costs have been entered on either, so real profit and margin cannot be calculated for any period. Decisions have been made on gross revenue alone. That is how a page looks fine in a 90 day total while every week inside it gets worse.</p></div>'''))

PP.append(page(10, f'''{head("10", "What changes", "Five things, <em>in order.</em>", "None of this needs new content or new traffic to start. It is all in how the two pages are being run.")}
<div class="asks4">
<div class="a4"><span class="lbl">01</span><h4>Answer Steve today</h4><p>Ten hours of unread messages on the fan who has spent {M(22_400)}. Someone reads the whole thread and replies properly, with nothing attached, then writes down how he is handled from here.</p></div>
<div class="a4"><span class="lbl">02</span><h4>Cut the sending</h4><p>Once or twice a day per page instead of hourly, split into active and expired. The vault unlock already proved the list responds when a send is worth opening.</p></div>
<div class="a4"><span class="lbl">03</span><h4>Retire the script</h4><p>One recycled line at six price points and a mail merged {M(LETTER_PRICE)} letter is not chatting. Real notes on the top ten first, then copy written off what each fan actually buys.</p></div>
<div class="a4"><span class="lbl">04</span><h4>Rebuild the VIP funnel</h4><p>Two links carry the page and both are stale. Refresh them, clear the dead ones, and copy the free page's monthly recapture habit onto VIP.</p></div>
</div>
<div class="warnp"><h4>05. Turn the lights on</h4><p>Costs entered on both accounts so profit and margin can be read for the first time, and David treated as one person across the two pages rather than two strangers. Until the numbers are real, nobody can tell whether a promo made money or just moved it.</p></div>
<div class="two"><div class="warnp"><h4>The order it happens in</h4><p>Steve today, because he is writing right now and nobody has opened the thread. The sending schedule this week, because nothing else gets a fair test while the list is being hit hourly. Notes on the top ten before any new copy is written. The funnel and the cost setup this month.</p></div>
<div class="warnp"><h4>What good looks like in 30 days</h4><p>Steve answered and a written approach on his file. View rates back above the vault unlock benchmark on a split list. Notes on all ten top spenders. David closed or cleanly withdrawn, and recognised as one fan across both pages. Profit readable on both accounts for the first time.</p></div></div>
<div class="close"><img src="__MARK__" alt=""><div><b>{M(TOP3)}</b><small>sitting in your top three threads</small></div>
<div><p>Neither page has a content problem and neither needs new traffic to start recovering. <strong>Both were run on volume and a script while the people who actually pay were left to handle themselves.</strong></p><div class="sig">ALTR, September 28, 2026. Built from live data across both accounts and the full whale threads.</div></div></div>'''))

# guard: stat labels in the PDF must fit one line (c4 columns are ~40mm at 9pt, c3 ~55mm)
import re as _re
for _cls, _lim in (("c4", 28), ("c3", 36)):
    for _row in _re.findall(r'<div class="nums ' + _cls + r'">(.*?)</div></div>', "".join(PP), _re.S):
        for _lab in _re.findall(r"<span>(.*?)</span>", _row):
            assert len(_lab) <= _lim, f"stat label too long for {_cls} ({len(_lab)}>{_lim}): {_lab}"
open("print-template.html", "w", encoding="utf-8").write('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Lucé. Account review by ALTR</title>'
    '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,62..125,100..900;1,62..125,100..900&family=Spline+Sans+Mono:wght@400;500&display=swap" rel="stylesheet">'
    "<style>" + PCSS + PX + "</style></head><body>" + "".join(PP) + "</body></html>")
print("built web + print")
