HOOK = [["A flat week on paper,", "bigger tickets inside"], ["Three new names led,", "each one spending big"]]

LEAD_1 = f"You made {M(NET)} this week against {M(PREV)} the week before, down {PCT(abs(CHANGE),1)}, which is effectively level. <em>The median purchase rose to {M(MED)} from {M(21.44)}, and three people who arrived this week brought in {M(FANS[0]['net_w'] + FANS[1]['net_w'] + FANS[2]['net_w'])} between them.</em>"

SHAPE = f"The week started quietly at {M(85)} on Sunday and built from there. {E(BEST_DAY)} was the high point at {M(BEST_NET)}, {PCT(BEST_SHARE,1)} of the whole week in a single day."

SHAPE2 = f"{N(BUYERS)} people bought something, and most of your income came from private conversations, {M(2057)} of it, with {M(144)} more in tips. The {BANDS[0]['band']} range earned the most{(' and ' + BANDS[1]['band'] + ' came next') if len(BANDS) > 1 else ''}, so higher prices are landing well."

NOTES = {
    FANS[0]["id"]: (f"New this week, top buy {M(FANS[0]['max_ticket'])}", f"{E(FANS[0]['name'])} spent {M(FANS[0]['net_w'])} within a day of arriving, the biggest total of the week."),
    FANS[1]["id"]: (f"{N(FANS[1]['n_sessions'])} visits in four days", f"{E(FANS[1]['name'])} kept coming back and spent {M(FANS[1]['net_w'])}, most recently yesterday."),
    FANS[2]["id"]: (f"Top buy {M(FANS[2]['max_ticket'])}, {N(FANS[2]['n_sessions'])} visits", f"{E(FANS[2]['name'])} arrived three days ago and has already spent {M(FANS[2]['net_w'])}."),
}

MOVES = [
    ("Today", "Welcome the new three", f"Warm, personal notes go to {E(FANS[0]['name'])}, {E(FANS[1]['name'])} and {E(FANS[2]['name'])}, who spent {M(FANS[0]['net_w'] + FANS[1]['net_w'] + FANS[2]['net_w'])} between them in their first days."),
    ("This week", "Build toward Friday", f"{E(BEST_DAY)} brought in {M(BEST_NET)}, so the best new sets are saved for the end of the week, when people are already spending."),
    ("All week", "Keep prices confident", f"The median purchase is now {M(MED)}, and the {BANDS[0]['band']} range is earning the most, so new sets stay in that range."),
]

GOOD30 = f"In thirty days, the three newest top spenders are regulars, the week has two strong days instead of one, and your median purchase holds above {M(MED)}. That puts a {M(2500)} week well within reach."

PENDING = [
    ("On ours", "Welcome the new three", f"We are writing personal hellos to this week's three newest top spenders, who brought in {M(FANS[0]['net_w'] + FANS[1]['net_w'] + FANS[2]['net_w'])}."),
    ("On ours", "This week's invoice", "It lands today, based on the platform-reported figures in this report."),
]

CLOSE = f"A level week with a stronger core: {N(BUYERS)} buyers, a {M(MED)} median and three new people already in your top spenders. <em>{M(NET)} this week, and the new names give next week a head start.</em>"

WEEK_HEAD = f"A level week, <em>new names on top</em>"

KN = [
    ("Bigger purchases", f"Your median purchase rose to {M(MED)} from {M(21.44)}, so people are paying more each time they buy."),
    ("New arrivals", f"Three people who joined this week spent {M(FANS[0]['net_w'] + FANS[1]['net_w'] + FANS[2]['net_w'])}, almost half of your {M(NET)}."),
    ("Your best day", f"{E(BEST_DAY)} earned {M(BEST_NET)}, {PCT(BEST_SHARE,1)} of the week in one day."),
]

WARN_FANS = (
    "Ten people, most of the week",
    f"Your top ten spenders made up {PCT(80.1,1)} of this week's {M(NET)}, so a small group carries a lot.",
    f"Two steady regulars, {E(FANS[3]['name'])} and {E(FANS[4]['name'])}, last bought five and six days ago, so they are the first people we will check in with.",
)

STORY_X = [
    f"{E(FANS[0]['name'])} found your page this week and spent {M(FANS[0]['net_w'])} within a day, including one {M(FANS[0]['max_ticket'])} purchase.",
    f"That single arrival was {PCT(FANS[0]['net_w'] / NET * 100, 1)} of your week, and they are still subscribed.",
]