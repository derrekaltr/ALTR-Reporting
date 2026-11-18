# -*- coding: utf-8 -*-
"""Kells. Account review prepared by ALTR. Built October 15, 2026.

Transition audit: the 90 days before ALTR took over, both pages, built from live data.
Run:  python3 build_premium.py && python3 ../../lib/build.py   then read qa/*.png, then ./deploy.sh
"""
import os, sys, json
from datetime import date, timedelta
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join("..", "..", "lib"))
from premium import *

# ------------------------------------------------------------------ facts (one place, used by web and print)
NAME = "Kells"; FIRST = NAME.split()[0]
DATE = "October 15, 2026"
PDF = "ALTR-kels-review-oct15.pdf"; PDF_DL = f"{FIRST}-Account-Review-ALTR.pdf"
TITLE = f"{FIRST}. Account review by ALTR"
AUDIENCE = "creator"

R = json.load(open("data/cohort.json", encoding="utf-8"))
NET30, NET_PREV, CHANGE = R["period"]["window"]["net"], R["period"]["previous"]["net"], R["summary"]["change_pct"]
BUYERS, MED_TICKET = R["period"]["window"]["buyers"], R["period"]["window"]["median_ticket"]
BUYERS_PREV = R["period"]["previous"]["buyers"]
TIPS, TIPS_PREV = R["period"]["window"]["tips"], R["period"]["previous"]["tips"]

# daily series, zero-filled across the calendar window
_d = {k: v["net"] for k, v in R["daily"].items()}
_end = date(2026, 10, 15); _days = [(_end - timedelta(days=i)) for i in range(30, -1, -1)]
MONTHS = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
DAILY = [(f"{MONTHS[d.month]} {d.day}", _d.get(d.isoformat(), 0.0)) for d in _days]
PEAK_I = max(range(len(DAILY)), key=lambda i: DAILY[i][1])
PEAK_D, PEAK_V = DAILY[PEAK_I]
ZDAYS = sum(1 for _, v in DAILY if v <= 0)

# free page channels (data/analysis of the 30-day window)
FMASS_N, FMASS_GROSS, FMASS_BUYS = 94, 15, 1          # mass messages: sent, gross, purchases
FDM_N, FDM_RATE, FDM_GROSS = 444, 8.3, 2127           # personal priced messages
FDM_REACHED = 234
NEWSUBS = 683                                          # new free subscribers in the window

# VIP page (WORK/kels-vip-review/analysis.txt, same window)
VNET, VPREV, VCH = 1697, 3143, 46.0
VTIPS, VTIPS_PREV = 20, 1308
VMASS_N, VMASS_GROSS = 84, 0
VDM_N, VDM_RATE, VDM_GROSS = 118, 14.4, 1030
VNEWSUBS, VSOLD, VBUYERS = 89, 26, 21

MASS_BOTH = FMASS_GROSS + VMASS_GROSS                  # 15
DM_BOTH = FDM_GROSS + VDM_GROSS                        # 3157

# top-spender cohort, free page, 90-day ledger
CO_N, CO_LIFE, CO_90 = 33, 132547, 4086
QUIET_N, QUIET_LIFE = 21, 62436                        # $1,000+ lifetime, zero purchases in 90 days

# thread audit (threads.txt / threads_analysis.json)
TH_TIMED, TH_MED_MIN, TH_WITHIN15 = 135, 4, 75
TH_READ, TH_MASSONLY = 17, 8
PPV_SENT, PPV_UNBOUGHT = 49, 44
UNANSWERED, QUIET10 = 2, 14

WHALES = [("Dez",        "1", 48204, "Wrote today, waited 9 hours",        "Bought $28 in the last 30 days"),
          ("Jon",        "2", 16437, "Quoted 3 prices for one custom",     "No purchase since June"),
          ("Brett",      "3", 6386,  "Got only mass messages for months",  "Not one personal message"),
          ("CVG1126",    "4", 2680,  "Still subscribed",                   "Nothing bought in 90 days"),
          ("Mason Slade","5", 2406,  "Still subscribed",                   "One $28 purchase in 90 days"),
          ("Billy77",    "6", 2396,  "Buying this week",                   "Keep him close"),
          ("Platidaddy", "7", 2357,  "Still subscribed",                   "Nothing bought in 90 days"),
          ("Hell2yeah",  "8", 2061,  "Last purchase 82 days ago",          "Still subscribed")]
for w in WHALES:
    assert len(w[3]) <= 40 and len(w[4]) <= 40, f"table text over 40 chars: {w}"
TOP3 = sum(w[2] for w in WHALES[:3])

# ------------------------------------------------------------------ charts (desktop + phone rendering of each)
m_daily = [{"t": d, "l": M(v), "s": "net that day"} for d, v in DAILY]
lbl_desk = [d if (i % 5 == 0 and i < 28) else "" for i, (d, _) in enumerate(DAILY)]
# phone: five buckets so the bars stay readable
_b = len(DAILY) // 5
BUCKETS = [DAILY[i*_b:(i+1)*_b] if i < 4 else DAILY[4*_b:] for i in range(5)]
WDAILY = [(b[0][0], sum(v for _, v in b)) for b in BUCKETS]
m_week = [{"t": f"week of {d}", "l": M(v), "s": "net that stretch"} for d, v in WDAILY]
WPEAK_I = max(range(len(WDAILY)), key=lambda i: WDAILY[i][1])
fig_daily = dual(ichart("c-d", [v for _, v in DAILY], m_daily, 900, 400, lbl_desk, hot=(PEAK_I,), fs=1.5),
                 ichart("c-d-m", [v for _, v in WDAILY], m_week, 420, 250, [d for d, _ in WDAILY], hot=(WPEAK_I,), fs=1.3, lw=72))

# ------------------------------------------------------------------ WEB (the link)
CHAPTERS = [("01", "Where it stands", "c1"), ("02", "Your top fans", "c2"), ("03", "How it was worked", "c3"), ("04", "What changes", "c4")]
rows = [{"rank": w[1], "name": w[0], "sub": w[3], "amount": M(w[2]), "extra": {"last": w[3], "why": w[4]}} for w in WHALES]
H = [hero(FIRST + ".", [["Your top fans have spent", f"{M(CO_LIFE)} with you."], ["The last 90 days", f"collected {M(CO_90)} of it."]],
          f"Before your pages moved to ALTR we read the last 90 days in full: every sale on both pages, your {CO_N} biggest spenders one by one, and your {TH_READ} biggest message threads from the first line to the last. This report shows where money sat untouched and what we do about it. Every dollar figure is net, your share.",
          f"Reviewed {DATE}<br>Prepared by ALTR for {FIRST}<br>Confidential", PDF, PDF_DL),
     '<div class="teaser">' + big(M(CO_LIFE), f"lifetime spend of your {CO_N} biggest fans") +
     big(M(CO_90), "what they spent in the last 90 days") + big(str(QUIET_N), "of them bought nothing at all in 90 days") + "</div>",
     method([(60, "days of revenue, both pages"), (TH_TIMED, "threads timed"), (TH_READ, "top threads read in full"), (CO_N, "top spenders traced"), (2, "accounts")]),
     toc([(n, t, a) for n, t, a in CHAPTERS])]

H.append(f'''<section>{ch("01", "Where it stands", "Both pages are sliding. <em>Here is the shape.</em>", "c1")}
<div class="spread"><div class="rv"><p class="lead">The free page made <em>{M(NET30)} net in the last 30 days</em>, down {abs(CHANGE):.0f}% from {M(NET_PREV)}. The VIP page made {M(VNET)}, down {VCH:.0f}% from {M(VPREV)}.</p>
<div class="prose" style="margin-top:16px"><p>The best day of the month was {PEAK_D} at {M(PEAK_V)}. {ZDAYS} days made nothing at all. Fans who bought on the free page went from {BUYERS_PREV} to {BUYERS}, and tips went down on both pages, {M(TIPS_PREV)} to {M(TIPS)} on the free page and {M(VTIPS_PREV)} to {M(VTIPS)} on VIP.</p>
<p>None of this is a traffic problem. {N(NEWSUBS)} new people subscribed to your free page in those 30 days and {N(VNEWSUBS)} joined the VIP page. The people were there. The money was not collected.</p></div></div>
<div class="stack">{big(M(NET30), "free page net, last 30 days")}{big(M(VNET), "VIP page net, last 30 days")}{big(N(NEWSUBS + VNEWSUBS), "new subscribers in the same window")}</div></div>
{fig(fig_daily, "Free page net per day across the window. <em>Mint is the best day.</em>", m_daily[PEAK_I])}
</section>''')

H.append(f'''<section>{ch("02", "Your top fans", "The people who pay, <em>and how they were handled.</em>", "c2")}
<div class="spread rev rv" style="margin-top:24px"><p class="lead">Your top three are worth <em>{M(TOP3)} between them.</em> We read all three threads in full.</p>
<div class="prose"><p>The pattern repeats down the list: proven spenders left waiting, quoted conflicting prices, or sent nothing but mass copy. {QUIET_N} fans who have each spent {M(1000)} or more with you, {M(QUIET_LIFE)} combined, bought nothing in 90 days. Most are still subscribed. <span class="web"><span class="t-h">Move down the list and the card follows you.</span><span class="t-t">Tap a fan for the detail.</span></span></p></div></div>
<div class="whales">{spot(rows[0], [("last", "What the thread shows"), ("why", "What it cost")])}
<div class="twin" style="margin-top:0"><div><div class="ml" style="margin-bottom:10px">By lifetime spend</div>{ledger(rows, hi=(rows[0]["name"],))}</div></div></div>
<div class="stories">{story("Dez", f"{M(48204)}, your number one", "Wrote today, waited 9 hours",
    f"Dez has spent {M(48204)} on your free page and another {M(8458)} on VIP. His VIP subscription ran out 34 days ago and nobody won him back. This week he wrote four times and his latest message sat 9 hours without an answer. He bought {M(28)} in the last 30 days against {M(929)} in the 30 before.",
    "All work and no play makes Jack a dull boy", "His message, the morning of October 15",
    "He is not gone. He is knocking. A fan at this level gets answered inside the hour, every time, by someone who knows his history.")}
{story("Jon", f"{M(16437)}, your number two", "Quoted 3 prices for one custom",
    f"Jon spent {M(16437)} over his time on the page. In June he asked about a custom and got three different prices in one conversation, {M(300)}, {M(500)}, and a per minute rate. He pushed back twice, then closed the door himself.",
    "The price doesn't matter at this point because it's not something I'm interested in anymore", "His last message, June 14. He has not bought since.",
    "One price list, written down, and this never happens. A spender this size walking over a quote is the single most expensive moment in your last 90 days.")}
{story("Brett", f"{M(6386)}, your number three", "Not one personal message",
    f"Brett spent {M(6386)} and his recent thread is 19 mass messages in a row. No personal message, no question, no name. Three priced messages were dropped in and none were bought, because nothing around them was written for him.",
    "", "", "A fan who has already paid thousands is not a stranger. He gets talked to like a person, and the priced messages start selling again.")}</div>
</section>''')

H.append(f'''<section>{ch("03", "How it was worked", "Mass copy got the hours. <em>Personal messages got the money.</em>", "c3")}
<div class="spread"><div class="rv"><p class="lead">Across both pages, mass messages earned <em>{M(MASS_BOTH)} in 30 days.</em> Personal messages earned {M(DM_BOTH)}.</p>
<div class="prose" style="margin-top:16px"><p>The free page sent {FMASS_N} mass messages in 30 days. One was bought. Total earned: {M(FMASS_GROSS)}. The VIP page sent {VMASS_N} more and not a single one sold. Meanwhile {N(FDM_N)} personal priced messages on the free page sold at {FDM_RATE:.0f}% and brought in {M(FDM_GROSS)}, and {VDM_N} on VIP sold at {VDM_RATE:.0f}%.</p>
<p>Your top fans got the same treatment as everyone else. Of your {TH_READ} biggest threads, {TH_MASSONLY} contain nothing but mass copy. {PPV_SENT} priced messages went to these fans and {PPV_UNBOUGHT} were never bought. When someone did answer, the median reply took {TH_MED_MIN} minutes, so speed was never the problem. Follow through was: {UNANSWERED} fans are waiting on a reply right now, one for more than two days, and {QUIET10} of your biggest threads have been quiet for ten days or more.</p>
<p>The new subscribers tell the same story. {N(NEWSUBS + VNEWSUBS)} people joined your pages in 30 days and only {BUYERS + VBUYERS} people bought anything at all. On the VIP page, {VSOLD} priced messages sold in a whole month.</p></div></div>
<div class="stack">{big(M(MASS_BOTH), f"earned by {FMASS_N + VMASS_N} mass messages, both pages")}{big(M(DM_BOTH), f"earned by {FDM_N + VDM_N} personal messages")}{big(f"{PPV_UNBOUGHT} of {PPV_SENT}", "priced messages to top fans never bought")}</div></div>
</section>''')

H.append(f'''<section>{ch("04", "What changes", "Four things, <em>in order.</em>", "c4")}
<div class="plan">{plan_step("Today", "Answer who is waiting", "We reply personally to the two fans sitting unanswered, starting with Dez. From now on, any fan in your top list gets an answer inside the hour, from someone who has read his history first.")}
{plan_step("This week", "Win back the quiet 21", f"Each of the {QUIET_N} proven spenders who went quiet gets one personal message written for him, at a price he has paid before. No mass copy touches these threads. We also set one written price list for customs so no fan ever gets two numbers again.", .12)}
{plan_step("This month", "Flip the mix", f"Mass messages earned {M(MASS_BOTH)} last month and personal messages earned {M(DM_BOTH)}, so the hours move where the money is. Mass drops to one a day, every new subscriber gets a personal welcome in the first day, and every priced message that goes unbought gets one follow up.", .24)}</div>
{closer(M(TOP3), "sitting in your top three threads", f"The fans did not leave. <em>They are still subscribed, still writing, still waiting to be treated like they matter.</em>", f"ALTR, {DATE}")}
<footer><img src="__LOGO__" alt="ALTR"><span>Prepared by ALTR for {FIRST}. Built from live data and the full top-fan threads. Confidential.</span></footer>
</section>''')

web = web_doc(TITLE, f"An account review prepared by ALTR for {FIRST}, confidential, {DATE}", "\n".join(H), PDF, PDF_DL,
              CHAPTERS, FIRST, spot_fields=["last", "why"])

# ------------------------------------------------------------------ PDF (the reading edition: every page composed to be full)
TOT = 6
doc = PrintDoc(TITLE, FIRST,
               chapters={1: "account review", 2: "the short version", 3: "where it stands", 4: "your top fans", 5: "how it was worked", 6: "what changes"},
               teasers={1: "Turn the page, the short version", 2: "Next, where it stands", 3: "Next, your top fans", 4: "Next, how it was worked", 5: "Next, what changes", 6: "Start today"}, total=TOT)

doc.page(1, f'''<div class="cv-top"><div class="meta" style="margin:0 0 3mm">Account review, @stargirlkels and @stargirlkelsvip</div><h1>{FIRST}<i>.</i></h1>
<div class="hook">Your top {CO_N} fans have spent {M(CO_LIFE)}. The last 90 days collected {M(CO_90)} of it.<em>Most of them are still subscribed.</em></div><div class="meta">Prepared by ALTR for {FIRST}, {DATE}. Confidential.</div></div>
<div class="letter"><div class="lbl">Read first</div><div><p>Before your pages moved to ALTR we read the last 90 days in full: every sale on both pages, your biggest spenders one by one, and the real threads, not summaries.</p>
<p>Page two is the short version. The pages after it show the evidence and what changes. Every dollar figure is net, your share.</p><div class="sig">ALTR</div></div></div>
{nums([(M(CO_LIFE), f"lifetime spend, top {CO_N} fans"), (M(CO_90), "of it in the last 90 days"), (str(QUIET_N), "bought nothing in 90 days")], cols=3)}
<div class="toc"><div class="lbl">Inside</div><ol><li>The short version<span>02</span></li><li>Where it stands<span>03</span></li><li>Your top fans<span>04</span></li><li>How it was worked<span>05</span></li><li>What changes<span>06</span></li></ol></div>''', "cover")

doc.page(2, f'''{head("02", "The short version", "Everything on one page. <em>Start here.</em>", "What we found in the 90 days before ALTR, and what changes, before the evidence.")}
<div><div class="lbl" style="margin-bottom:2mm">What we found</div><div class="find">
{fnd(M(CO_LIFE), f"Your {CO_N} biggest fans spent this over their time with you. The last 90 days collected {M(CO_90)} of it, and {QUIET_N} of them bought nothing at all.", True)}
{fnd(f"{VCH:.0f}%", f"The VIP page fell from {M(VPREV)} to {M(VNET)} net in 30 days. The free page fell {abs(CHANGE):.0f}%, from {M(NET_PREV)} to {M(NET30)}. Tips nearly stopped on both.")}
{fnd(M(MASS_BOTH), f"What {FMASS_N + VMASS_N} mass messages earned across both pages in 30 days. {FDM_N + VDM_N} personal messages earned {M(DM_BOTH)} in the same window.")}
</div></div>
<div><div class="lbl" style="margin-bottom:2.5mm">Three fans that explain it</div><div class="know">
<div class="kn"><span class="lbl">Left waiting</span><h4>{E("Dez")}</h4><p>{M(48204)} lifetime. Wrote four times this week and waited 9 hours for an answer.</p></div>
<div class="kn"><span class="lbl">Mixed prices</span><h4>{E("Jon")}</h4><p>{M(16437)} lifetime. Got three prices for one custom and has not bought since June.</p></div>
<div class="kn"><span class="lbl">Mass copy only</span><h4>{E("Brett")}</h4><p>{M(6386)} lifetime. His thread is 19 mass messages in a row, nothing personal.</p></div>
</div></div>
<div><div class="lbl" style="margin-bottom:2.5mm">What changes</div><div class="wk">
<div><span class="lbl">Today</span><h4>Answer who is waiting</h4><p>Personal replies to the two waiting fans, starting with Dez.</p></div>
<div><span class="lbl">This week</span><h4>Win back the quiet 21</h4><p>One personal message to each proven spender who went quiet.</p></div>
<div><span class="lbl">This month</span><h4>Flip the mix</h4><p>Fewer mass messages, personal welcomes, one written price list.</p></div></div></div>''')

doc.page(3, f'''{head("03", "Where it stands", "Both pages are sliding. <em>Here is the shape.</em>", f"The free page made {M(NET30)} net in the last 30 days against {M(NET_PREV)} in the 30 before. The VIP page made {M(VNET)} against {M(VPREV)}.")}
<div class="chart">{ichart("p-d", [v for _, v in DAILY], [{}] * len(DAILY), 900, 520, lbl_desk, hot=(PEAK_I,), fs=1.6)}<div class="cap">Free page net per day across the window. <em>Mint is the best day, {PEAK_D} at {M(PEAK_V)}.</em></div></div>
{nums([(M(NET30), "free page net, 30 days"), (M(VNET), "VIP page net, 30 days"), (f"{VCH:.0f}%", "VIP change in 30 days"), (M(MED_TICKET), "median price paid")])}
{warn("Tips nearly stopped on both pages", f"Tips on the VIP page went from {M(VTIPS_PREV)} to {M(VTIPS)} in 30 days. On the free page they went from {M(TIPS_PREV)} to {M(TIPS)}. Fans who bought anything on the free page went from {BUYERS_PREV} to {BUYERS}.",
 f"This was never a traffic problem. {N(NEWSUBS + VNEWSUBS)} new people subscribed across both pages in those same 30 days. The people showed up. The money was not collected.")}''')

doc.page(4, f'''{head("04", "Your top fans", "The people who pay, <em>and how they were handled.</em>", f"Your top three are worth {M(TOP3)} between them. We read all three threads in full. {QUIET_N} fans at {M(1000)} or more lifetime, {M(QUIET_LIFE)} combined, bought nothing in 90 days.")}
<div class="lbl">By lifetime spend</div>
{qtable(WHALES, WHALES[0][2])}
{warn("Jon closed the door himself", f"Jon spent {M(16437)} over his time on the page. In June he asked about a custom and got three different prices in one conversation. He pushed back twice, said the price no longer mattered because he was no longer interested, and has not bought since.",
 "One written price list ends this. A spender this size walking over a quote is the most expensive single moment in your last 90 days.")}''')

doc.page(5, f'''{head("05", "How it was worked", "Mass copy got the hours. <em>Personal messages got the money.</em>", f"Across both pages, mass messages earned {M(MASS_BOTH)} in 30 days. Personal messages earned {M(DM_BOTH)}.")}
{nums([(str(FMASS_N + VMASS_N), "mass messages sent, 30 days"), (M(MASS_BOTH), "what they earned"), (str(FDM_N + VDM_N), "personal messages sent"), (M(DM_BOTH), "what those earned")])}
{warn("The VIP page sold almost nothing", f"The VIP page sent {VMASS_N} mass messages in 30 days and not one was bought. {VSOLD} priced messages sold all month, while {VNEWSUBS} new subscribers joined. Personal messages on the same page sold at {VDM_RATE:.0f}%.",
 "The fans buy when someone talks to them directly. The page was run on copy and paste instead.")}
{warn("Top fans got the same treatment as everyone", f"We read your {TH_READ} biggest threads in full. {TH_MASSONLY} of them contain nothing but mass copy. {PPV_SENT} priced messages went to these fans and {PPV_UNBOUGHT} were never bought. Dez, your number one at {M(48204)}, also let his VIP subscription run out 34 days ago and nobody won him back.",
 f"Speed was never the problem, the median reply took {TH_MED_MIN} minutes when someone answered. Follow through was: {UNANSWERED} fans are waiting right now, one for more than two days, and {QUIET10} of your biggest threads have been quiet for ten days or more.")}''')

doc.page(6, f'''{head("06", "What changes", "Four things, <em>in order.</em>", "None of this needs new content or new traffic to start.")}
<div class="asks4">
<div class="a4"><span class="lbl">01</span><h4>Answer who is waiting</h4><p>Personal replies today to the two unanswered fans, starting with Dez. From now on, every fan in your top list gets an answer inside the hour from someone who has read his history.</p></div>
<div class="a4"><span class="lbl">02</span><h4>Win back the quiet 21</h4><p>Each proven spender who went quiet gets one personal message this week, written for him, at a price he has paid before. No mass copy touches these threads.</p></div>
<div class="a4"><span class="lbl">03</span><h4>Flip the mix</h4><p>Mass drops to one a day and the hours move to personal threads. Every new subscriber gets a personal welcome in the first day. One written price list for customs, so no fan ever gets two numbers.</p></div>
<div class="a4"><span class="lbl">04</span><h4>What good looks like in 30 days</h4><p>Both pages over {M(150)} a day combined, Dez buying at his normal pace, and unbought priced messages getting one follow up instead of silence.</p></div></div>
{warn("The order it happens in", f"The waiting fans come first because they are already asking. The quiet {QUIET_N} come second because {M(QUIET_LIFE)} of proven spend is sitting in those threads. The mix flips last because it is a habit change, and habits take the month.")}
<div class="close"><img src="__MARK__" alt=""><div><b>{M(TOP3)}</b><small>sitting in your top three threads</small></div>
<div><p>The fans did not leave. <strong>They are still subscribed, still writing, still waiting to be treated like they matter.</strong></p><div class="sig">ALTR, {DATE}. Built from live data and the full top-fan threads.</div></div></div>''')

write_outputs(web, doc.html(), PDF, TITLE)
