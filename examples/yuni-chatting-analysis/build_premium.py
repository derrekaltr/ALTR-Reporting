# -*- coding: utf-8 -*-
"""Yuni chatting analysis, premium edition (internal, team-facing).
Web: scroll experience on the Vale/Yuni design system -> template.html
PDF: reading edition -> print-template.html. Then run build.py."""
import json, html, os, datetime as dt
os.chdir(os.path.dirname(os.path.abspath(__file__)))
E = html.escape
M = lambda n: f"${n:,.0f}"
R = json.load(open("data/analysis.json", encoding="utf-8"))
TA = json.load(open("data/threads_analysis.json", encoding="utf-8")); TH, RP = TA["threads"], TA["summary"]["reply"]
D, DM, MS = R["daily"], R["dm"], R["mass"]
days = sorted(D.keys())
def rng(a, b):
    ks = [k for k in days if a <= k <= b]; n = len(ks)
    return {"net": round(sum(D[k].get("net", 0) for k in ks) / n), "dm": round(sum(R["dm_daily"].get(k, 0) for k in ks) / n, 1),
            "mass": round(sum(R["mass_daily"].get(k, 0) for k in ks) / n, 1)}
A1, A2, B0, BL = rng("08-22", "09-03"), rng("09-04", "09-14"), rng("09-15", "09-17"), rng("09-18", "09-20")
fans = {f["id"]: f for f in R["fans"]}
new_b = [fans[i] for i in R["b_new_buyers"]]; new_spend = sum(f["B"] for f in new_b)
resA = sum(1 for r in R["resends"] if r["per"] == "A"); resB = sum(1 for r in R["resends"] if r["per"] == "B")
canA, canB = R["dm_canceled"]["A"], R["dm_canceled"]["B"]
N_TX = len(json.load(open("data/transactions60.json", encoding="utf-8")))
N_DM = DM["A"]["sent"] + DM["B"]["sent"]; N_MS = MS["A"]["n"] + MS["B"]["n"]; N_TH = len(TH)
bands = R["dm_bands"]
lab = [dt.date(2026, int(k[:2]), int(k[3:])).strftime("%b %d") for k in days]
live = tuple(i for i, k in enumerate(days) if k >= "09-18")

# ------------------------------------------------------------------ charts (same engine as the Vale and Yuni reviews)
def ichart(cid, series, meta, w, h, xlabels, yfmt=None, show_val=None, hot=(), lw=None, fs=1.0, every=1):
    lw = lw or int(48 * fs)
    yfmt = yfmt or (lambda v: f"${v/1000:g}K" if v >= 1000 else f"${v:,.0f}")
    raw = max(max(series), 1)
    mx = next(c for c in [10, 20, 25, 40, 50, 60, 100, 200, 250, 500, 1000, 1500, 2000, 2500, 3000, 4000, 5000] + [raw] if c >= raw)
    tp, bp = int(24 * fs), int(30 * fs); ch_ = h - tp - bp; x0 = lw; cw = w - x0 - 4; n = len(series); bw = cw / n
    o = [f'<svg class="ich" id="{cid}" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid meet" role="img">']
    for fr in (0.0, 0.5, 1.0):
        y = tp + ch_ - ch_ * fr
        o.append(f'<line x1="{x0}" y1="{y:.1f}" x2="{w-4}" y2="{y:.1f}" stroke="rgba(235,236,220,0.09)"/>')
        o.append(f'<text x="{x0-8}" y="{y+3.5*fs:.1f}" font-size="{10*fs:.0f}" fill="rgba(235,236,220,0.5)" text-anchor="end">{yfmt(mx*fr)}</text>')
    for i, v in enumerate(series):
        x = x0 + i * bw + bw * 0.18; bwid = bw * 0.64; bh = ch_ * v / mx; y = tp + ch_ - bh
        dim = " after" if (hot and i not in hot) else ""
        o.append(f'<rect class="bar{dim}" data-meta="{E(json.dumps(meta[i]))}" x="{x:.1f}" y="{y:.1f}" width="{bwid:.1f}" height="{max(bh,1):.1f}" rx="1" style="transition-delay:{i*25}ms"/>')
        if show_val: o.append(f'<text x="{x0+i*bw+bw/2:.1f}" y="{y-8*fs:.1f}" font-size="{11*fs:.0f}" fill="#ebecdc" text-anchor="middle">{show_val[i]}</text>')
        if xlabels and i % every == 0 and xlabels[i]:
            o.append(f'<text x="{x0+i*bw+bw/2:.1f}" y="{h-9*fs:.0f}" font-size="{10*fs:.0f}" fill="rgba(235,236,220,0.6)" text-anchor="middle">{E(xlabels[i])}</text>')
    o.append("</svg>"); return "".join(o)
def dual(d, m): return f'<div class="cv d">{d}</div><div class="cv m">{m}</div>'
def fig(svg, caption, default, extra=""):
    return (f'<figure class="fig rv"{extra}>{svg}<div class="readout"><span class="rt">{E(default["t"])}</span><span class="rl">{E(default["l"])}</span>'
            f'<span class="rs">{E(default["s"])}</span></div><figcaption>{caption}</figcaption></figure>')
def ph(k): return "Previous team, selling" if k <= "09-03" else ("Previous team, stopped" if k <= "09-14" else ("ALTR, not live yet" if k <= "09-17" else ("ALTR, live" + (", partial day" if k == "09-21" else ""))))
meta_net = [{"t": lab[i], "l": f'{M(D[k].get("net",0))} earned', "s": f'{ph(k)}. {R["dm_daily"].get(k,0)} paid DMs, {R["mass_daily"].get(k,0)} mass messages.'} for i, k in enumerate(days)]
net = [D[k].get("net", 0) for k in days]
fig_net = dual(ichart("c-net", net, meta_net, 900, 260, [l if i % 5 == 0 else "" for i, l in enumerate(lab)], hot=live, fs=1.3),
               ichart("c-net-m", net, meta_net, 420, 280, [l[4:] if i % 7 == 0 else "" for i, l in enumerate(lab)], hot=live, fs=1.4, lw=56))
dmd = [R["dm_daily"].get(k, 0) for k in days]; msd = [R["mass_daily"].get(k, 0) for k in days]
meta_dm = [{"t": lab[i], "l": f"{dmd[i]} paid DMs sent", "s": ph(k)} for i, k in enumerate(days)]
meta_ms = [{"t": lab[i], "l": f"{msd[i]} mass messages", "s": ph(k)} for i, k in enumerate(days)]
cnt = lambda v: f"{v:.0f}"
fig_dm = dual(ichart("c-dm", dmd, meta_dm, 900, 420, [l if i % 7 == 0 else "" for i, l in enumerate(lab)], hot=live, fs=2.2, yfmt=cnt),
              ichart("c-dm-m", dmd, meta_dm, 420, 260, [l[4:] if i % 7 == 0 else "" for i, l in enumerate(lab)], hot=live, fs=1.4, lw=48, yfmt=cnt))
fig_ms = dual(ichart("c-ms", msd, meta_ms, 900, 420, [l if i % 7 == 0 else "" for i, l in enumerate(lab)], hot=live, fs=2.2, yfmt=cnt),
              ichart("c-ms-m", msd, meta_ms, 420, 260, [l[4:] if i % 7 == 0 else "" for i, l in enumerate(lab)], hot=live, fs=1.4, lw=48, yfmt=cnt))
blab = ["$0-19", "$20-39", "$40-69", "$70-99", "$100-149", "$150+"]
rates = [b["B"]["rate"] for b in bands]
meta_b = [{"t": blab[i], "l": f'{b["B"]["rate"]:.0f}% unlocked this week', "s": f'{b["B"]["bought"]} of {b["B"]["sent"]} sent. Previous team: {b["A"]["rate"]:.0f}% of {b["A"]["sent"]}.'} for i, b in enumerate(bands)]
pct = lambda v: f"{v:.0f}%"
fig_b = dual(ichart("c-b", rates, meta_b, 900, 420, blab, hot=(2, 4), fs=2.2, yfmt=pct, show_val=[f"{r:.0f}%" for r in rates]),
             ichart("c-b-m", rates, meta_b, 420, 280, ["$0", "$20", "$40", "$70", "$100", "$150"], hot=(2, 4), fs=1.4, lw=48, yfmt=pct, show_val=[f"{r:.0f}%" for r in rates]))

def ch(num, kicker, title, cid):
    return f'<header class="ch rv" id="{cid}"><div class="ch-meta"><span class="num">{num}</span><span class="kick">{E(kicker)}</span></div><h2>{title}</h2></header>'
def big(v, label): return f'<div class="big rv"><span class="bv">{v}</span><span class="bl">{E(label)}</span></div>'
def story(name, status, meta, body, quote, cite, more):
    q = f'<blockquote><p>{E(quote)}</p><cite>{E(cite)}</cite></blockquote>' if cite else f'<div class="sbig">{quote}</div>'
    return (f'<article class="story rv" tabindex="0"><div class="n"><h3>{E(name)}</h3><span class="st">{E(status)}</span></div><div class="h">{E(meta)}</div>'
            f'<p>{body}</p>{q}<div class="more"><div><p>{more}</p></div></div><span class="hint">More</span></article>')

# ------------------------------------------------------------------ the queue (spotlight ledger)
Q = [(575340641, "Said goodbye Sep 10", "Told us it was their last time. Sub ends Sep 26, renewal off. Since then only mass messages, including another creator's promo.", "Personal note today. Acknowledge the goodbye, no offer."),
     (142787499, "Quiet since Aug 27", "Biggest spender of the 30 days. Complained the old team 'unsend a lot'. Sub renews Sep 27.", "Re-open by referencing Aug 27. Never unsend here."),
     (542707770, "Quiet since Aug 28", "$428 in late August. Since then one overnight note and one check-in. Sub ends Sep 28, renewal off.", "Personal, warm, by name."),
     (22280448, "Waiting on us", "Asking where the Snapchat and 10 videos the old team sold them are. Told 'idk what happened'.", "Escalate now. No Snapchat. Management decides the fix."),
     (519634712, "Waiting 44 hours", "Sent four long messages on Sep 19 after buying. No reply since.", "Reply today, picking up their last message."),
     (394961070, "Owed a custom", "New this week, $500 in one night. Promised a named custom ('Tai').", "Deliver once Yuni confirms a date."),
     (543332471, "Owed a custom", "New this week. Paid $125 for a custom. Told a friend was at the door.", "Deliver once Yuni confirms. Give a real date."),
     (14367266, "Renews Sep 22", "$192 on Aug 22. Has never had a personal message. Sub ends tomorrow, renewal off.", "First real conversation, today."),
     (136706871, "Never messaged", "$281 in August. No personal message ever, only mass blasts.", "First real conversation."),
     (560093651, "Asked for a preview", "$329. Asked for a photo preview before buying on Sep 18 and never got one.", "Send a preview, then the offer.")]
def qrow(i, q):
    uid, status, why, move = q; t = TH[str(uid)]; f = fans.get(uid, {})
    last = dt.datetime.fromisoformat(f["last"]).strftime("%b %d") if f.get("last") else "n/a"
    return (f'<div class="lr{" hi" if i <= 5 else ""}" tabindex="0" data-rank="{i:02d}" data-name="{E(t["name"])}" data-handle="@{E(t["user"])}" '
            f'data-net="{M(f.get("net30", t["net30"]))}" data-last="{last}" data-why="{E(why)}" data-move="{E(move)}">'
            f'<span class="ln">{i:02d}</span><span class="lw"><b>{E(t["name"])}</b><i>{E(status)}</i></span><span class="r">{M(f.get("net30", t["net30"]))}</span><span class="r">{last}</span>'
            f'<div class="lx"><div><b>{M(f.get("net30", t["net30"]))}</b><span>last 30 days</span></div><div><b>{last}</b><span>last purchase</span></div><p>{E(why)} {E(move)}</p></div></div>')
LH = '<div class="lh"><span class="ln"></span><span class="lw">Fan</span><span class="r">30 days</span><span class="r">Last buy</span></div>'
ledger_a = f'<div class="ledger c">{LH}{"".join(qrow(i, q) for i, q in enumerate(Q[:5], 1))}</div>'
ledger_b = f'<div class="ledger c">{LH}{"".join(qrow(i, q) for i, q in enumerate(Q[5:], 6))}</div>'
q0 = TH[str(Q[0][0])]; f0 = fans[Q[0][0]]

# ------------------------------------------------------------------ WEB
BASE = open("creator_base.css", encoding="utf-8").read() + open("web_extra.css", encoding="utf-8").read()
EXTRA = """
.asks{grid-template-columns:repeat(4,1fr)}
@media(max-width:920px){.asks{grid-template-columns:1fr}}
.warn{margin-top:44px;padding:28px 32px;border:1px solid rgba(182,242,229,.35);border-radius:6px;background:var(--wash)}
.warn h3{font-weight:300;font-size:26px;letter-spacing:-.02em}.warn p{margin-top:10px;color:var(--bone2);font-size:15px;max-width:70ch}
.spot .sa span{display:block}
"""
H = [f'''<div id="prog"></div><div id="glow"></div>
<nav id="nav"><a href="#top"><span>Yuni</span><i></i></a><a href="#c1"><span>The 30 days</span><i></i></a><a href="#c2"><span>What's working</span><i></i></a><a href="#c3"><span>Promises</span><i></i></a><a href="#c4"><span>Mass and pricing</span><i></i></a><a href="#c5"><span>The queue</span><i></i></a><a href="#c6"><span>For Yuni</span><i></i></a></nav>
<div class="dl-wrap"><a class="dl-btn" href="ALTR-yuni-chatting-analysis-sep21.pdf" download="Yuni-Chatting-Analysis-ALTR-Sep-2026.pdf">Download PDF</a></div>
<div class="page" id="top">
  <header class="mast"><img src="__LOGO__" alt="ALTR"><span>Chatting analysis for the ALTR chat team, confidential, September 21, 2026</span></header>
  <div class="hero">
    <h1><span>Y</span><span>u</span><span>n</span><span>i</span><span>.</span></h1>
    <div>
      <p class="hook"><span><b>The team is fast</b><b>and fans are buying.</b></span><span><b>The promises</b><b>are the risk.</b></span></p>
      <p class="sub">Thirty days of Yuni's page: the previous team's last three weeks and our first week. Every paid message, every mass message, and the full conversations with the fans who matter. What is working, what we fix this week, and what we need from Yuni.</p>
      <div class="who">Aug 22 to Sep 21, 2026<br>Internal, for the chat team and management<br>Confidential, team only</div>
      <a class="dl-inline" href="ALTR-yuni-chatting-analysis-sep21.pdf" download="Yuni-Chatting-Analysis-ALTR-Sep-2026.pdf">Download the PDF</a>
    </div>
    <div class="cue"><i></i>Scroll</div>
  </div>
  <div class="teaser">
    {big(M(BL["net"]), "a day since we went live on Sep 18, up from $232 in the old team's last 11 days")}
    {big(f'{RP["B"]["within_15"]}<small>%</small>', f"of fan messages answered within 15 minutes. The previous team managed {RP['A']['within_15']}%")}
    {big("4", "customs promised this week to close sales, none confirmed with Yuni first")}
  </div>
  <div class="method rv"><span class="ml">What we read</span>
    <div class="m"><b>30</b><span>days of the page</span></div><div class="m"><b>{N_TX:,}</b><span>transactions</span></div>
    <div class="m"><b>{N_DM}</b><span>paid DMs</span></div><div class="m"><b>{N_MS}</b><span>mass messages</span></div><div class="m"><b>{N_TH}</b><span>conversations read</span></div>
  </div>
  <nav class="toc rv"><span class="ml">Inside</span>
    <a href="#c1"><b>01</b><span>The 30 days</span></a><a href="#c2"><b>02</b><span>What's working</span></a><a href="#c3"><b>03</b><span>Promises</span></a>
    <a href="#c4"><b>04</b><span>Mass and pricing</span></a><a href="#c5"><b>05</b><span>The queue</span></a><a href="#c6"><b>06</b><span>For Yuni</span></a>
  </nav>''']

H.append(f'''<section>
  {ch("01", "The 30 days", "The page went cold. <em>We brought it back.</em>", "c1")}
  <div class="spread">
    <div class="rv"><p class="lead">From Aug 22 to Sep 3 the old team earned <em>{M(A1["net"])} a day</em>. Then they stopped selling, and the page fell to {M(A2["net"])}.</p>
      <div class="prose" style="margin-top:16px"><p>We took the chats on Sep 15, but paid messaging only restarted on Sep 18. Those three days earned {M(B0["net"])} a day, with two paid DMs between them. Next handover, we go live on day one.</p>
      <p>Since Sep 18 the page has averaged {M(BL["net"])} a day and {BL["dm"]:.0f} paid DMs a day. Sep 20 was the best day since Aug 28, at $1,141. Mint bars are ALTR live. Sep 21 is a partial day. <span class="web"><span class="t-h">Hover any bar.</span><span class="t-t">Tap any bar.</span></span></p></div></div>
    <div class="stack">{big(M(A1["net"]), "a day, old team while selling")}{big(M(A2["net"]), "a day, old team's last 11 days")}{big(M(BL["net"]), "a day, ALTR since Sep 18")}</div>
  </div>
  {fig(fig_net, "Net revenue per day. <em>Mint is ALTR live.</em>", meta_net[days.index("09-20")])}
</section>''')

H.append(f'''<section>
  {ch("02", "What's working", "Fast, warm, <em>and closing.</em>", "c2")}
  <div class="row4">
    {big(f'{RP["B"]["within_15"]}<small>%</small>', f"answered within 15 minutes, median {RP['B']['median_min']:.0f} minute")}
    {big(str(len(new_b)), f"first-time buyers this week, {M(new_spend)} between them")}
    {big(str(resB), f"discounted resends this week. The old team did {resA}")}
    {big(str(len(canB)), f"paid messages unsent. The old team unsent {len(canA)}, worth {M(sum(canA))}")}
  </div>
  <div class="stories">
    {story("Tai", "$500, Sep 20", "@u394961070, new this week", "Came in cold and bought $100, $200 and $200 in one night. The chatter built the scene first and asked for their name before selling.", "$500<small>in one night</small>", "", "Copy the order: rapport, then a named, personal offer. They asked for 'more like this', which is on Yuni's list in chapter 06.")}
    {story("Malgus", "6 of 7 unlocked", "@u523447965, new this week", "Six of seven paid messages unlocked in two nights. A playful, consistent persona the fan plays along with.", "$280<small>in two nights</small>", "", "Keep the voice consistent across shifts. Fans buy from a person they recognise.")}
  </div>
</section>''')

H.append(f'''<section>
  {ch("03", "Promises", "Every custom we promise, <em>Yuni has to keep.</em>", "c3")}
  <div class="spread eq rv" style="margin-top:30px">
    <p class="lead">The old team lost this page by promising customs and not delivering. <em>In our first four live days, chatters promised four more</em> to close sales, without checking with Yuni.</p>
    <div class="prose"><p>Three customs from the old team are still open: Dan since August, andy since Aug 15 and Blitzen since Sep 2. Add ours and seven fans are waiting on Yuni. From today, no chatter promises a custom, call or personal video until Yuni says yes and it is in the tracker with price, script and date. Until then the line is 'let me see what I can do for you'.</p></div>
  </div>
  <div class="stories">
    {story("Tai", "Promised Sep 20", "@u394961070, paid $500", "After a $200 bundle, the chatter promised a named custom: 'I'm going to cum so hard in that video for you.' No date.", "Owed<small>needs Yuni</small>", "", "On Yuni's list in chapter 06. Once she confirms, give Tai a real date.")}
    {story("Nocluebono", "Paid $125", "@u543332471, new this week", "Paid $125 for a custom masturbation and orgasm video. The chatter left mid-session with a made-up excuse.", "Sooo is the video ready?", "Nocluebono, Sep 21", "The excuse was 'a friend told me I need to go out with her urgently'. Never invent excuses. Tell the fan when it will be ready.")}
    {story("Alex Guy", "Quoted $350", "@u22280448", "Asked for a toys custom. The chatter quoted $350, then offered two bundles 'and then I'll make you the custom'.", "$350<small>not confirmed</small>", "", "Hold until Yuni says yes. Alex is also waiting on a Snapchat the old team sold. See the warning below.")}
    {story("Malgus", "Offered as bait", "@u523447965", "'Just open that bundle, it's to make that custom.' The custom was used to sell a $200 bundle.", "Stop<small>customs are products, not closers</small>", "", "A custom is sold on its own terms, once Yuni agrees to it.")}
  </div>
  <div class="warn rv"><h3>Compliance, today</h3><p>Alex Guy is asking for the Snapchat access and 10 videos the old team sold: 'I was just wondering when I would get the snap and the 10 vids.' We answered 'idk what happened'. No Snapchat, ever. Management decides the on-platform fix. The Tyler thread (L L), where the old team offered Zelle and Telegram, was re-opened on Sep 19. Any fan who asks to pay outside OnlyFans gets a polite no.</p></div>
</section>''')

H.append(f'''<section>
  {ch("04", "Mass messages and pricing", "More noise, <em>lower prices.</em>", "c4")}
  <div class="row4">
    {big(str(MS["B"]["n"]), f"mass messages in 7 days, {MS['B']['per_day']:.0f} a day. The old team sent {MS['A']['per_day']:.1f}")}
    {big(f'{MS["B"]["view_rate"]:.2f}<small>%</small>', f"of sends viewed, down from {MS['A']['view_rate']:.2f}%")}
    {big("2", "promos for other creators' pages sent to Yuni's paying fans")}
    {big(M(DM["B"]["avg_sent"]), f"average paid DM this week, down from {M(DM['A']['avg_sent'])}")}
  </div>
  <div class="figs">
    {fig(fig_ms, "Mass messages per day. <em>26 on Sep 19 alone, roughly hourly through the night.</em>", meta_ms[days.index("09-19")])}
    {fig(fig_b, "Our unlock rate by price. <em>$40-69 and $100-149 sold best.</em> Price barely changes the rate.", meta_b[2])}
  </div>
  <div class="spread eq rv" style="margin-top:34px">
    <div class="prose"><p><strong>Mass messages.</strong> 68 of 70 were free one-line teasers. The Sep 21 promo for @arianamarie reached 17 of our top 30 fans, and on Sep 21, 16 of them got four blasts in five hours. On Sep 19, 9 lapsed fans got overnight notes like 'Take care and stay sweet, Dan' and 13 more got a single '🥺'. They read as goodbyes. Cap mass messages at three a day, exclude the top 50 fans, and re-open lapsed fans by referencing their last real conversation.</p></div>
    <div class="prose"><p><strong>Pricing.</strong> The old team sold $150+ messages at 40%. We are talking ourselves down: 'If that's too much for you, I can lower it to $100' to Tai, who had not objected and paid $200 again half an hour later. 'Could you do $60?' hands the fan the negotiation. Open at $50 to $60, ladder to $100+, one counter at most, and bundles go up in value, never down in price.</p></div>
  </div>
</section>''')

H.append(f'''<section>
  {ch("05", "The queue", "Ten fans, <em>in order, this week.</em>", "c5")}
  <div class="spread rev rv" style="margin-top:24px">
    <p class="lead">The first five are today. Seven of our top 30 fans have had no personal message since handover, worth $1,368 in 30 days.</p>
    <div class="prose"><p>Also on the list: Lando 92, Justin, CC, alohaoh and Jonnakeke have had no personal message since handover. Jamesdeans71 sent 101 messages this week and has not bought since Aug 31. Keep it warm, but that is not where the chatter's hours go. <span class="web"><span class="t-h">Move along the list and the card follows you.</span><span class="t-t">Tap a fan for the detail.</span></span></p></div>
  </div>
  <div class="whales">
    <aside class="spot rv" id="spot">
      <div class="sr">Fan <b id="s-rank">01</b> of 10</div>
      <h3 id="s-name">{E(q0["name"])}</h3><div class="sh" id="s-handle">@{E(q0["user"])}</div>
      <div class="sg"><div><b id="s-net">{M(f0["net30"])}</b><span>last 30 days</span></div><div><b id="s-last">{dt.datetime.fromisoformat(f0["last"]).strftime("%b %d")}</b><span>last purchase</span></div></div>
      <div class="sa"><b>Why</b><span id="s-why">{E(Q[0][2])}</span></div>
      <div class="sa"><b>Next move</b><span id="s-move">{E(Q[0][3])}</span></div>
      <div class="tip">Hover or tap a fan</div>
    </aside>
    <div class="twin" style="margin-top:0">{ledger_a}{ledger_b}</div>
  </div>
</section>''')

H.append(f'''<section>
  {ch("06", "For Yuni, and this week", "What we need from her, <em>and what we do.</em>", "c6")}
  <p class="lead rv" style="margin-top:24px;max-width:60ch">Her account manager raises these in one message today. Chatters don't promise any of it until she answers.</p>
  <div class="asks rv">
    <div><b data-n="01">Tai's custom</b><p>A personal video for Ninja8954, saying 'Tai', finishing on camera. Paid for Sep 20. Will she film it, and by when?</p></div>
    <div><b data-n="02">Nocluebono's custom</b><p>Masturbation and orgasm video, $125 paid. The fan also asked if a creampie BG clip is included. Date, and yes or no on the BG part.</p></div>
    <div><b data-n="03">Alex Guy's request</b><p>A plug, a dildo and a vibrator at once, quoted $350. Yes or no.</p></div>
    <div><b data-n="04">Dan and andy</b><p>Dan's call-turned-custom from August and andy's five-minute custom from Aug 15. Film them, or close them out?</p></div>
    <div><b data-n="05">Blitzen</b><p>Paid $200 toward a custom with a partner on Sep 2. Does she film with partners? If not, credit or refund.</p></div>
    <div><b data-n="06">New content</b><p>Fans ask for more finishing-on-camera videos, scissoring, explicit photos rather than squirting, and 'something new'. One new set this week.</p></div>
    <div><b data-n="07">Instagram and Fansly</b><p>Fans are asking if her Instagram is disabled and her Fansly deleted. What should chatters say?</p></div>
    <div><b data-n="08">Promo swaps</b><p>Two promos for other creators went to her fans. Management confirms these with her before any more go out.</p></div>
  </div>
  <div class="plan">
    <div class="step rv"><div class="w">Today</div><h3>Stop the risks</h3><p>Shut down the Snapchat thread and escalate Alex Guy. Send Yuni the eight items above. New rule live: no custom promises without her yes. Reply to queue 1 to 5.</p></div>
    <div class="step rv" style="transition-delay:.12s"><div class="w">This week</div><h3>Clean up the noise</h3><p>Three mass messages a day at most, top 50 fans excluded, no more overnight 'Take care' notes. Hold prices: open at $50 to $60, one counter, no unprompted drops.</p></div>
    <div class="step rv" style="transition-delay:.24s"><div class="w">This week</div><h3>Re-open the silent seven</h3><p>Au Martin, Lando 92, Justin, Sean Hung (renews Sep 22), CC, alohaoh and Jonnakeke. A first real conversation, by name, with no offer in it.</p></div>
  </div>
  <div class="close rv"><img src="__MARK__" alt="" aria-hidden="true">
    <div class="cb"><span>{M(BL["net"])}</span><small>a day since we went live</small></div>
    <div><p>The team is fast and fans are buying again. <em>The last team lost this page by promising and not delivering.</em> Log it, confirm it with Yuni, then sell it.</p><div class="sig">ALTR Chat Operations, September 21, 2026</div></div>
  </div>
  <footer><img src="__LOGO__" alt="ALTR"><span>Internal, for the ALTR chat team and management. Built from Yuni's OnlyFans account data. Directional, for chat operations only. Infloww remains ALTR's financial record.</span></footer>
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
        '<title>Yuni. Chatting analysis, ALTR internal</title><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,62..125,100..900;1,62..125,100..900&family=Spline+Sans+Mono:wght@400;500&display=swap" rel="stylesheet">')
open("template.html", "w", encoding="utf-8").write('<!DOCTYPE html><html lang="en"><head>' + HEAD + "<style>" + BASE + EXTRA + "</style></head><body>" + "\n".join(H) + JS + "</body></html>")

# ------------------------------------------------------------------ PDF (reading edition)
PCSS = open("print_base.css", encoding="utf-8").read()
TOT = 7
CH = {1: "internal chatting analysis", 2: "02, the short version", 3: "03, the 30 days", 4: "04, promises", 5: "05, mass and pricing", 6: "06, the queue", 7: "07, for Yuni and this week"}
NX = {1: "Turn the page, the short version", 2: "Next, the 30 days", 3: "Next, promises", 4: "Next, mass and pricing", 5: "Next, the queue", 6: "Next, for Yuni and this week", 7: "Log it, confirm it, then sell it"}
def page(n, body, cls=""):
    ghost = '<img class="ghost" src="__GHOST__" alt="">' if cls == "cover" else ""
    return (f'<section class="pg {cls}">{ghost}<header class="run"><img src="__LOGO__" alt="ALTR"><span>Yuni, {CH[n]}</span></header><div class="body">{body}</div>'
            f'<footer class="foot"><span>ALTR chat operations, team only</span><span class="nx">{NX[n]}</span><span>{n:02d} / {TOT:02d}</span></footer></section>')
def head(num, kicker, title, line):
    return f'<div class="hd"><div class="hn"><b>{num}</b><span>{E(kicker)}</span></div><div class="ht"><h2>{title}</h2><p>{line}</p></div></div>'
def pch(svg): return f'<div class="chart">{svg}'
def lad(tickets, w=210, h=40):
    n = len(tickets); top = 13; base = h - 1; gap = 3.2; bw = min(16, (w - 44 - gap * (n - 1)) / n)
    o = [f'<svg class="lad" viewBox="0 0 {w} {h}" preserveAspectRatio="xMinYMid meet"><line x1="0" y1="{top}" x2="{w-40}" y2="{top}" stroke="#b6f2e5" stroke-width=".8" stroke-dasharray="2 2.5" opacity=".7"/>'
         f'<text x="{w}" y="{top+10}" text-anchor="end" font-size="10.5" fill="#b6f2e5" font-family="Spline Sans Mono, monospace">$200</text>']
    for i, t in enumerate(tickets):
        bh = max(2, (base - top) * min(t, 200) / 200); x = i * (bw + gap)
        o.append(f'<rect x="{x:.1f}" y="{base-bh:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx=".6" fill="{"#b6f2e5" if t >= 195 else "rgba(235,236,220,.34)"}"/>')
    return "".join(o) + "</svg>"
tai_t = [a for (_, a, ty, p) in [] ]  # ladders use the per-fan tickets below
def tickets(uid, since="2026-09-15"):
    import collections
    tx = [t for t in json.load(open("data/transactions60.json", encoding="utf-8")) if (t.get("user") or {}).get("id") == uid and t["type"] in ("message", "tip") and t["createdAt"] >= since and t["status"] not in ("undo",)]
    return [t["amount"] for t in sorted(tx, key=lambda t: t["createdAt"])]
PX = """
.cover .nums b{font-size:26pt}.cover .nums span{font-size:9pt}
.cv-top .hook{margin-top:6mm;font-weight:300;font-size:21pt;line-height:1.18;letter-spacing:-.02em}.cv-top .hook em{display:block;font-style:normal;color:var(--mint)}
.cover .ghost{position:absolute;right:-26mm;top:18mm;width:150mm;opacity:.045}
.foot .nx{color:var(--mint)}
.lad{display:block;width:100%;height:auto;margin-top:2mm}
.lcap{margin-top:1mm;font-family:var(--mono);font-size:6.8pt;color:var(--bone3);white-space:nowrap}.lcap b{font-family:var(--sans);font-weight:300;font-size:12pt;color:var(--bone);margin-right:1.6mm}
.know{display:grid;grid-template-columns:repeat(3,1fr);gap:4mm}
.kn{border:1px solid var(--line);border-radius:2mm;padding:4mm 4.5mm 3.5mm;display:flex;flex-direction:column}
.kn h4{font-weight:300;font-size:15pt;letter-spacing:-.02em;line-height:1;margin-top:1.8mm}.kn p{margin-top:2mm;font-size:8.8pt;color:var(--bone2);line-height:1.5}
.kn .lad{margin-top:auto;padding-top:3mm}
.asks4{display:grid;grid-template-columns:repeat(2,1fr);gap:3.5mm}
.a4{border:1px solid var(--line);border-radius:2mm;padding:3.2mm 4mm}.a4 h4{font-weight:500;font-size:10pt;margin-top:1mm}.a4 p{margin-top:1.2mm;font-size:8.8pt;color:var(--bone2);line-height:1.45}
.warnp{border:1px solid rgba(182,242,229,.45);background:var(--wash);border-radius:2mm;padding:4mm 5mm}.warnp h4{font-weight:500;font-size:11pt}.warnp p{margin-top:1.5mm;font-size:9pt;color:var(--bone2);line-height:1.5}
.qt{width:100%;border-collapse:collapse}.qt th{font-family:var(--mono);font-weight:400;font-size:6.8pt;letter-spacing:.1em;text-transform:uppercase;color:var(--bone3);text-align:left;padding:0 1.6mm 2mm;border-bottom:1px solid var(--line)}
.qt td{padding:2.2mm 1.6mm;border-bottom:1px solid var(--soft);font-size:8.8pt;vertical-align:top;line-height:1.4}.qt .n{font-family:var(--mono);font-size:7.5pt;color:var(--mint);width:6mm}
.qt .fan b{display:block;font-weight:500;font-size:9.4pt;white-space:nowrap}.qt .fan i{display:block;font-style:normal;font-family:var(--mono);font-size:6.8pt;color:var(--bone3)}
.qt .num{text-align:right;font-family:var(--mono);white-space:nowrap}.qt .mv{color:var(--bone)}
.two{display:grid;grid-template-columns:1fr 1fr;gap:4mm}
"""
def fnd(v, t, hi=False): return f'<div{" class=\"hi\"" if hi else ""}><b>{v}</b><p>{t}</p></div>'
PP = []
PP.append(page(1, f'''<div class="cv-top"><div class="meta" style="margin:0 0 3mm">Internal chatting analysis, last 30 days</div><h1>Yuni<i>.</i></h1>
<div class="hook">The team is fast and fans are buying.<em>The promises are the risk.</em></div><div class="meta">Prepared by ALTR chat operations, September 21, 2026. Team only.</div></div>
<div class="letter"><div class="lbl">Read first</div><div><p>Thirty days of Yuni's page, Aug 22 to Sep 21: the previous team's last three weeks and our first week. We read every paid message, every mass message and the full conversations with the fans who matter.</p>
<p>Page two is the short version. The rest is the detail, the fan queue, and what the account manager takes to Yuni today.</p><div class="sig">ALTR chat operations</div></div></div>
<div class="nums c3"><div><b>{M(BL["net"])}</b><span>a day since we went live on Sep 18</span></div><div><b>{RP["B"]["within_15"]}%</b><span>of fan messages answered within 15 minutes</span></div><div><b>4</b><span>customs promised this week, none confirmed</span></div></div>
<div class="toc"><div class="lbl">Inside</div><ol><li>The short version<span>02</span></li><li>The 30 days, and what's working<span>03</span></li><li>Promises and compliance<span>04</span></li><li>Mass messages and pricing<span>05</span></li><li>The queue<span>06</span></li><li>For Yuni, and this week<span>07</span></li></ol></div>''', "cover"))
PP.append(page(2, f'''{head("02", "The short version", "Everything on one page. <em>Start here.</em>", "What we found, three fans to know by name, and what happens this week.")}
<div><div class="lbl" style="margin-bottom:2mm">What we found</div><div class="find">
{fnd(M(BL["net"]), f"A day since we went live on Sep 18. The old team earned {M(A1['net'])} while selling and {M(A2['net'])} in its last 11 days.")}
{fnd(f'{RP["B"]["within_15"]}%', f"Of fan messages answered within 15 minutes, against {RP['A']['within_15']}% before. {len(new_b)} first-time buyers spent {M(new_spend)}.")}
{fnd("4 + 3", "Customs promised this week to close sales, plus three still open from the old team. None confirmed with Yuni.", True)}
{fnd(str(MS["B"]["n"]), f"Mass messages in 7 days, {MS['B']['view_rate']:.2f}% viewed. Two promoted other creators' pages to Yuni's fans.")}
{fnd(M(DM["B"]["avg_sent"]), f"Our average paid DM, down from {M(DM['A']['avg_sent'])}. Chatters drop prices before fans ask.")}
</div></div>
<div><div class="lbl" style="margin-bottom:2.5mm">Three fans to know by name</div><div class="know">
<div class="kn"><span class="lbl">Biggest new fan</span><h4>Tai</h4><p>Ninja8954. $500 in one night, Sep 20. Owed a named custom.</p>{lad(tickets(394961070))}<div class="lcap"><b>$500</b>this week</div></div>
<div class="kn"><span class="lbl">Waiting on us</span><h4>Alex Guy</h4><p>Asking for a Snapchat the old team sold. Compliance, today.</p>{lad(tickets(22280448, "2026-08-22"))}<div class="lcap"><b>{M(fans[22280448]["net30"])}</b>last 30 days</div></div>
<div class="kn"><span class="lbl">Said goodbye</span><h4>palewalrus</h4><p>'After this, I probably won't be going on here anymore.' Sub ends Sep 26.</p>{lad(tickets(575340641, "2026-08-22"))}<div class="lcap"><b>{M(fans[575340641]["net30"])}</b>last 30 days</div></div>
</div></div>
<div><div class="lbl" style="margin-bottom:2.5mm">What happens this week</div><div class="wk">
<div><span class="lbl">Today</span><h4>Stop the risks</h4><p>Escalate the Snapchat thread. Send Yuni the list on page 7. No custom promises without her yes.</p></div>
<div><span class="lbl">This week</span><h4>Clean up the noise</h4><p>Three mass messages a day, top 50 fans excluded. Hold prices.</p></div>
<div><span class="lbl">This week</span><h4>Work the queue</h4><p>Ten fans in order on page 6, the first five today.</p></div></div></div>'''))
PP.append(page(3, f'''{head("03", "The 30 days", "The page went cold. <em>We brought it back.</em>", f"We took the chats on Sep 15, but paid messaging only restarted on Sep 18.")}
{pch(ichart("p-net", net, [{}]*len(net), 900, 250, [l if i % 5 == 0 else "" for i, l in enumerate(lab)], hot=live, fs=1.35))}<div class="cap">Net revenue per day. <em>Mint is ALTR live.</em> Sep 21 is a partial day.</div></div>
<div class="nums c4"><div><b>{M(A1["net"])}</b><span>a day, old team while selling, Aug 22 to Sep 3</span></div><div><b>{M(A2["net"])}</b><span>a day, old team's last 11 days</span></div><div><b>{M(B0["net"])}</b><span>a day, Sep 15 to 17, before we went live</span></div><div><b>{M(BL["net"])}</b><span>a day, ALTR from Sep 18</span></div></div>
<div><div class="lbl" style="margin-bottom:2.5mm">What's working</div><div class="find">
{fnd(f'{RP["B"]["median_min"]:.0f} min', f"Median reply time. {RP['B']['within_15']}% of fan messages answered within 15 minutes.", True)}
{fnd(str(len(new_b)), f"First-time buyers this week, {M(new_spend)} between them. Tai spent $500 and Malgus $280, with 6 of 7 paid messages unlocked.")}
{fnd(f"{resB} and {len(canB)}", f"Discounted resends and unsent paid messages this week. The old team did {resA} and {len(canA)}, worth {M(sum(canA))}.")}
</div></div>'''))
PP.append(page(4, f'''{head("04", "Promises", "Every custom we promise, <em>Yuni has to keep.</em>", "The old team lost this page by promising and not delivering. In our first four live days, chatters promised four more.")}
<table class="qt"><thead><tr><th></th><th>Fan</th><th>What was promised</th><th>Status</th></tr></thead><tbody>
<tr><td class="n">01</td><td class="fan"><b>Tai</b><i>@u394961070</i></td><td>Named custom after a $200 bundle: 'I'm going to cum so hard in that video for you.' No date.</td><td class="mv">Owed, needs Yuni</td></tr>
<tr><td class="n">02</td><td class="fan"><b>Nocluebono</b><i>@u543332471</i></td><td>$125 paid for a custom masturbation and orgasm video. Chatter left with a made-up excuse.</td><td class="mv">Owed, needs Yuni</td></tr>
<tr><td class="n">03</td><td class="fan"><b>Alex Guy</b><i>@u22280448</i></td><td>Toys custom quoted at $350, then 'two bundles and then I'll make you the custom'.</td><td class="mv">Hold</td></tr>
<tr><td class="n">04</td><td class="fan"><b>Malgus</b><i>@u523447965</i></td><td>Custom used as bait for a $200 bundle.</td><td class="mv">Stop</td></tr>
<tr><td class="n">05</td><td class="fan"><b>Dan</b><i>@u109006099</i></td><td>Old team: a video call turned into a custom in August, never filmed. Sub ended Sep 17.</td><td class="mv">Inherited</td></tr>
<tr><td class="n">06</td><td class="fan"><b>andy</b><i>@u580301383</i></td><td>Old team: a five-minute custom promised since Aug 15.</td><td class="mv">Inherited</td></tr>
<tr><td class="n">07</td><td class="fan"><b>Blitzen</b><i>@u137350974</i></td><td>Old team: $200 paid toward a $1,000 custom with a partner, Sep 2.</td><td class="mv">Inherited</td></tr></tbody></table>
<div class="warnp"><h4>New rule, effective today</h4><p>No chatter promises a custom, call or personal video without Yuni's yes, logged in the tracker with price, script and delivery date. Until then the line is 'let me see what I can do for you'. Never invent an excuse to leave a session.</p></div>
<div class="warnp"><h4>Compliance, today</h4><p>Alex Guy is asking for the Snapchat access and 10 videos the old team sold. We answered 'idk what happened'. No Snapchat, ever, and management decides the on-platform fix. The Tyler thread (L L), where the old team offered Zelle and Telegram, was re-opened on Sep 19. Anyone asking to pay outside OnlyFans gets a polite no.</p></div>'''))
PP.append(page(5, f'''{head("05", "Mass, pricing", "More noise, <em>lower prices.</em>", f"{MS['B']['n']} mass messages in 7 days against {MS['A']['per_day']:.1f} a day before, and a lower average price.")}
<div class="two"><div class="chart">{ichart("p-ms", msd, [{}]*len(msd), 900, 440, [l if i % 7 == 0 else "" for i, l in enumerate(lab)], hot=live, fs=2.8, yfmt=cnt)}<div class="cap">Mass messages per day. <em>26 on Sep 19.</em></div></div>
<div class="chart">{ichart("p-b", rates, [{}]*6, 900, 440, ["$0", "$20", "$40", "$70", "$100", "$150+"], hot=(2, 4), fs=2.8, yfmt=pct, show_val=[f"{r:.0f}%" for r in rates])}<div class="cap">Our unlock rate by price. <em>$40 and $100 bands sold best.</em></div></div></div>
<div class="nums c4"><div><b>{MS["B"]["view_rate"]:.2f}%</b><span>of mass sends viewed, from {MS["A"]["view_rate"]:.2f}%</span></div><div><b>17</b><span>of our top 30 got the @arianamarie promo</span></div><div><b>9 + 13</b><span>lapsed fans got 'Take care' notes or a '🥺'</span></div><div><b>{M(DM["B"]["avg_sent"])}</b><span>average paid DM, from {M(DM["A"]["avg_sent"])}</span></div></div>
<div class="find">
{fnd("3 a day", "Cap mass messages. Exclude the top 50 fans from every free one. No more overnight 'Take care' notes, which read as goodbyes.", True)}
{fnd("$50-60", "Open here and ladder to $100+. Tai was offered a drop to $100 without objecting, then paid $200 again half an hour later.")}
{fnd("1 counter", "At most. Never ask 'could you do $60?', and bundles go up in value, never down in price.")}
</div>'''))
qrows = "".join(f'<tr><td class="n">{i:02d}</td><td class="fan"><b>{E(TH[str(u)]["name"])}</b><i>{E(s)}</i></td><td class="num">{M(fans.get(u, {}).get("net30", TH[str(u)]["net30"]))}</td><td>{E(w)}</td><td class="mv">{E(m)}</td></tr>' for i, (u, s, w, m) in enumerate(Q, 1))
PP.append(page(6, f'''{head("06", "The queue", "Ten fans, <em>in order, this week.</em>", "The first five are today. Seven of our top 30 have had no personal message since handover, worth $1,368.")}
<table class="qt"><thead><tr><th></th><th>Fan</th><th class="num">30 days</th><th>Why</th><th>Next move</th></tr></thead><tbody>{qrows}</tbody></table>
<p class="tx">Also on the list: Lando 92, Justin, CC, alohaoh and Jonnakeke have had no personal message since handover. Jamesdeans71 sent 101 messages this week and has not bought since Aug 31. Keep it warm, but that is not where the chatter's hours go.</p>'''))
PP.append(page(7, f'''{head("07", "For Yuni", "What we need from her, <em>and what we do.</em>", "Her account manager raises these in one message today. Chatters don't promise any of it until she answers.")}
<div class="asks4">
<div class="a4"><span class="lbl">01</span><h4>Tai's custom</h4><p>A personal video saying 'Tai', finishing on camera. Paid Sep 20. Will she film it, and by when?</p></div>
<div class="a4"><span class="lbl">02</span><h4>Nocluebono's custom</h4><p>Masturbation and orgasm video, $125 paid. Date, and yes or no on the creampie BG clip the fan asked about.</p></div>
<div class="a4"><span class="lbl">03</span><h4>Alex Guy's request</h4><p>A plug, a dildo and a vibrator at once, quoted $350. Yes or no.</p></div>
<div class="a4"><span class="lbl">04</span><h4>Dan and andy</h4><p>Two customs from the old team, still waiting. Film them, or close them out?</p></div>
<div class="a4"><span class="lbl">05</span><h4>Blitzen</h4><p>$200 paid toward a custom with a partner. Does she film with partners? If not, credit or refund.</p></div>
<div class="a4"><span class="lbl">06</span><h4>New content</h4><p>Fans ask for more finishing-on-camera videos, scissoring, explicit photos and 'something new'. One new set this week.</p></div>
<div class="a4"><span class="lbl">07</span><h4>Instagram and Fansly</h4><p>Fans ask if her Instagram is disabled and her Fansly deleted. What should chatters say?</p></div>
<div class="a4"><span class="lbl">08</span><h4>Promo swaps</h4><p>Two promos for other creators went to her fans. Confirm these with her before any more go out.</p></div>
</div>
<div class="close"><img src="__MARK__" alt=""><div><b>{M(BL["net"])}</b><small>a day since we went live</small></div>
<div><p>The team is fast and fans are buying again. <strong>The last team lost this page by promising and not delivering.</strong> Log it, confirm it with Yuni, then sell it.</p><div class="sig">ALTR chat operations, September 21, 2026. Directional, for chat ops only.</div></div></div>'''))
open("print-template.html", "w", encoding="utf-8").write('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Yuni. Chatting analysis, ALTR internal</title>'
    '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,62..125,100..900;1,62..125,100..900&family=Spline+Sans+Mono:wght@400;500&display=swap" rel="stylesheet">'
    "<style>" + PCSS + PX + "</style></head><body>" + "".join(PP) + "</body></html>")
print("built web + print")
