# -*- coding: utf-8 -*-
"""Kells VIP. Account review prepared by ALTR. Built October 15, 2026.

THE ONLY FILE YOU EDIT. Everything visual comes from ../../lib/premium.py and the CSS next to it.
Structure: constants at the top (every number once), then the WEB chapters, then the PDF pages.
Run:  python3 build_premium.py && python3 ../../lib/build.py   then read qa/*.png, then ./deploy.sh

Replace every placeholder below with real findings. Delete chapters you do not need; keep the order
cover / short version / evidence chapters / what changes. Keep each heading half under 26 characters.
"""
import os, sys, json
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join("..", "..", "lib"))
from premium import *

# ------------------------------------------------------------------ facts (one place, used by web and print)
NAME = "Kells VIP"; FIRST = NAME.split()[0]
DATE = "October 15, 2026"
PDF = "ALTR-kels-vip-weekly-oct15.pdf"; PDF_DL = f"{FIRST}-Account-Review-ALTR.pdf"
TITLE = f"{FIRST}. Account review by ALTR"
AUDIENCE = "creator"          # "creator": written TO her, no asks, no internal jargon.  "team": internal, chatter language allowed.

# If data/cohort.json exists (lib/pull_account.py + lib/analyze_ledger.py), pull the headline numbers from it.
R = json.load(open("data/cohort.json", encoding="utf-8")) if os.path.exists("data/cohort.json") else None
if R:
    NET30, NET_PREV, CHANGE = R["period"]["window"]["net"], R["period"]["previous"]["net"], R["summary"]["change_pct"]
    BUYERS, MED_TICKET = R["period"]["window"]["buyers"], R["period"]["window"]["median_ticket"]
    DAILY = [(k[5:], v["net"]) for k, v in R["daily"].items()]
    WHALES = [(f["name"], str(i + 1), f.get("life") or f["net"], f"{f['days_since_buy']:.0f} days since a purchase" if f.get("days_since_buy") is not None else "No purchase in the ledger",
               "Active subscriber" if f.get("sub_active") else "Subscription lapsed") for i, f in enumerate(R["cohort"][:8])]
else:   # hardcode when the findings come from someone else's diagnostic (see examples/luce-account-review)
    NET30, NET_PREV, CHANGE = 34_124, 47_260, -27.8
    BUYERS, MED_TICKET = 412, 25
    DAILY = [("Sep 01", 1480), ("Sep 08", 1210), ("Sep 15", 990), ("Sep 22", 640)]
    WHALES = [("Steve", "1", 22_400, "No note on the account", "Ten hours of messages unread"),
              ("David", "2", 10_700, "Also on the free page", "A bundle stalled after he asked why"),
              ("Jay Jay", "3", 9_500, "Flagged on his file", "Sent the same script as everyone")]
for w in WHALES:
    assert len(w[3]) <= 40 and len(w[4]) <= 40, f"table text over 40 chars: {w}"
TOP3 = sum(w[2] for w in WHALES[:3])

# ------------------------------------------------------------------ charts (desktop + phone rendering of each)
m_daily = [{"t": d, "l": M(v), "s": "net that day"} for d, v in DAILY]
fig_daily = dual(ichart("c-d", [v for _, v in DAILY], m_daily, 900, 400, [d for d, _ in DAILY], hot=(0,), fs=2.2),
                 ichart("c-d-m", [v for _, v in DAILY], m_daily, 420, 250, [d[:3] for d, _ in DAILY], hot=(0,), fs=1.5, lw=52))

# ------------------------------------------------------------------ WEB (the link)
CHAPTERS = [("01", "Where it stands", "c1"), ("02", "Your top fans", "c2"), ("03", "What changes", "c3")]
rows = [{"rank": w[1], "name": w[0], "sub": w[3], "amount": M(w[2]), "extra": {"last": w[3], "why": w[4]}} for w in WHALES]
H = [hero(FIRST + ".", [["Headline finding,", "in two short lines."], ["The mint line is", "the sharpest sentence."]],
          "One paragraph on what was read and why. We read the real threads, not summaries. Everything here comes from your own live data.",
          f"Reviewed {DATE}<br>Prepared by ALTR for {FIRST}<br>Confidential", PDF, PDF_DL),
     '<div class="teaser">' + big(f"{abs(CHANGE):.0f}<small>%</small>", "change in net over the last 30 days against the 30 before") +
     big(M(NET30), "net in the last 30 days") + big(str(BUYERS), "fans who bought something in the window") + "</div>",
     method([(30, "days of revenue"), (BUYERS, "paying fans"), (len(WHALES), "top spenders"), ("Full", "top-fan threads"), (1, "account")]),
     toc([(n, t, a) for n, t, a in CHAPTERS])]

H.append(f'''<section>{ch("01", "Where it stands", f"Down {abs(CHANGE):.0f}% in thirty days. <em>Here is where it went.</em>", "c1")}
<div class="spread"><div class="rv"><p class="lead">Net was <em>{M(NET30)} in the last 30 days</em>, against {M(NET_PREV)} in the 30 before.</p>
<div class="prose" style="margin-top:16px"><p>Two or three plain sentences on the shape of the month. Where the peak was, where the floor is, what changed in between.</p>
<p>A second paragraph on what that means for her, written to her, without jargon.</p></div></div>
<div class="stack">{big(M(NET30), "net, last 30 days")}{big(M(NET_PREV), "net, the 30 days before")}{big(M(MED_TICKET), "median price paid per message")}</div></div>
{fig(fig_daily, "Net per day across the window. <em>Mint is the best day.</em>", m_daily[0])}
</section>''')

H.append(f'''<section>{ch("02", "Your top fans", "The people who pay, <em>and how they were handled.</em>", "c2")}
<div class="spread rev rv" style="margin-top:24px"><p class="lead">Your top three are worth <em>{M(TOP3)} between them.</em> We read all three threads in full.</p>
<div class="prose"><p>One paragraph on the pattern across the top of the list. <span class="web"><span class="t-h">Move down the list and the card follows you.</span><span class="t-t">Tap a fan for the detail.</span></span></p></div></div>
<div class="whales">{spot(rows[0], [("last", "The note on their file"), ("why", "What is happening")])}
<div class="twin" style="margin-top:0"><div><div class="ml" style="margin-bottom:10px">By lifetime spend</div>{ledger(rows, hi=(rows[0]["name"],))}</div></div></div>
<div class="stories">{story(WHALES[0][0], f"{M(WHALES[0][2])}, number one", WHALES[0][3], "What happened in the thread, in two sentences, with the dates.", "A short quote from the thread.", "When it was said", "What this means and what good handling looks like, one paragraph.")}
{story(WHALES[1][0], f"{M(WHALES[1][2])}, number two", WHALES[1][3], "What happened in the thread.", "A short quote.", "When", "What it means.")}</div>
</section>''')

H.append(f'''<section>{ch("03", "What changes", "Three things, <em>in order.</em>", "c3")}
<div class="plan">{plan_step("Today", "The first move", "One paragraph, first person plural: what ALTR does first and why.")}
{plan_step("This week", "The second move", "One paragraph.", .12)}{plan_step("This month", "The third move", "One paragraph.", .24)}</div>
{closer(M(TOP3), "sitting in your top three threads", "The closing sentence. <em>The clause that carries the whole report, in mint.</em>", f"ALTR, {DATE}")}
<footer><img src="__LOGO__" alt="ALTR"><span>Prepared by ALTR for {FIRST}. Built from live data and the full top-fan threads. Confidential.</span></footer>
</section>''')

web = web_doc(TITLE, f"An account review prepared by ALTR for {FIRST}, confidential, {DATE}", "\n".join(H), PDF, PDF_DL,
              CHAPTERS, FIRST, spot_fields=["last", "why"])

# ------------------------------------------------------------------ PDF (the reading edition: every page composed to be full)
TOT = 4
doc = PrintDoc(TITLE, FIRST,
               chapters={1: "account review", 2: "the short version", 3: "where it stands", 4: "what changes"},
               teasers={1: "Turn the page, the short version", 2: "Next, where it stands", 3: "Next, what changes", 4: "Start today"}, total=TOT)

doc.page(1, f'''<div class="cv-top"><div class="meta" style="margin:0 0 3mm">Account review, @username</div><h1>{FIRST}<i>.</i></h1>
<div class="hook">Headline finding in one line.<em>The sharpest sentence, in mint.</em></div><div class="meta">Prepared by ALTR for {FIRST}, {DATE}. Confidential.</div></div>
<div class="letter"><div class="lbl">Read first</div><div><p>Two sentences on what was read and why. We read the real threads, not summaries.</p>
<p>Page two is the short version. The pages after it show the evidence and what changes.</p><div class="sig">ALTR</div></div></div>
{nums([(f"{abs(CHANGE):.0f}%", "change in 30 days"), (M(NET30), "net, last 30 days"), (str(BUYERS), "fans who bought")], cols=3)}
<div class="toc"><div class="lbl">Inside</div><ol><li>The short version<span>02</span></li><li>Where it stands<span>03</span></li><li>What changes<span>04</span></li></ol></div>''', "cover")

doc.page(2, f'''{head("02", "The short version", "Everything on one page. <em>Start here.</em>", "What we found, and what changes, before the evidence.")}
<div><div class="lbl" style="margin-bottom:2mm">What we found</div><div class="find">
{fnd(f"{abs(CHANGE):.0f}%", f"Net is down from {M(NET_PREV)} to {M(NET30)} over thirty days. One sentence on why.", True)}
{fnd(M(TOP3), "Sitting in the top three threads, and one sentence on how they were handled.")}
{fnd(str(BUYERS), "Fans bought something this month. One sentence on who they are.")}
</div></div>
<div><div class="lbl" style="margin-bottom:2.5mm">Three fans that explain it</div><div class="know">
<div class="kn"><span class="lbl">Ignored</span><h4>{E(WHALES[0][0])}</h4><p>{M(WHALES[0][2])} lifetime. One sentence.</p></div>
<div class="kn"><span class="lbl">Oversold</span><h4>{E(WHALES[1][0])}</h4><p>{M(WHALES[1][2])} lifetime. One sentence.</p></div>
<div class="kn"><span class="lbl">Flag ignored</span><h4>{E(WHALES[2][0])}</h4><p>{M(WHALES[2][2])} lifetime. One sentence.</p></div>
</div></div>
<div><div class="lbl" style="margin-bottom:2.5mm">What changes</div><div class="wk">
<div><span class="lbl">Today</span><h4>The first move</h4><p>One sentence.</p></div>
<div><span class="lbl">This week</span><h4>The second move</h4><p>One sentence.</p></div>
<div><span class="lbl">This month</span><h4>The third move</h4><p>One sentence.</p></div></div></div>''')

doc.page(3, f'''{head("03", "Where it stands", f"Down {abs(CHANGE):.0f}% in thirty days. <em>Here is where it went.</em>", f"Net was {M(NET30)} in the last 30 days against {M(NET_PREV)} in the 30 before.")}
<div class="chart">{ichart("p-d", [v for _, v in DAILY], [{}] * len(DAILY), 900, 520, [d for d, _ in DAILY], hot=(0,), fs=1.6)}<div class="cap">Net per day across the window. <em>Mint is the best day.</em></div></div>
{nums([(M(NET30), "net, last 30 days"), (M(NET_PREV), "net, the 30 before"), (M(MED_TICKET), "median message price"), (str(BUYERS), "paying fans")])}
{warn("A finding with a title", "One paragraph of evidence.", "A second paragraph on what it means.")}
<div class="lbl">By lifetime spend</div>
{qtable(WHALES, WHALES[0][2])}''')

doc.page(4, f'''{head("04", "What changes", "Three things, <em>in order.</em>", "None of this needs new content or new traffic to start.")}
<div class="asks4">
<div class="a4"><span class="lbl">01</span><h4>The first move</h4><p>Two sentences.</p></div>
<div class="a4"><span class="lbl">02</span><h4>The second move</h4><p>Two sentences.</p></div>
<div class="a4"><span class="lbl">03</span><h4>The third move</h4><p>Two sentences.</p></div>
<div class="a4"><span class="lbl">04</span><h4>What good looks like in 30 days</h4><p>Two sentences.</p></div></div>
{warn("The order it happens in", "One paragraph.")}
<div class="close"><img src="__MARK__" alt=""><div><b>{M(TOP3)}</b><small>sitting in your top three threads</small></div>
<div><p>The closing sentence. <strong>The clause that carries the whole report.</strong></p><div class="sig">ALTR, {DATE}. Built from live data and the full top-fan threads.</div></div></div>''')

write_outputs(web, doc.html(), PDF, TITLE)
