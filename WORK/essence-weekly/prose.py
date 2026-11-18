HOOK = [["A stronger week,", "up 12 percent"], ["One loyal supporter", "set the pace"]]

LEAD_1 = f"Your week closed at {M(NET)} net, up from {M(PREV)} the week before. <em>{N(BUYERS)} people bought from you, and one of them came back five times.</em>"

SHAPE = f"The week built toward its finish. {BEST_DAY} was the best day at {M(BEST_NET)}, about a third of the whole week, and the quieter days still held steady between {M(55)} and {M(334)}."

SHAPE2 = f"The {BANDS[0]['band']} range earned the most this week, {M(BANDS[0]['gross'])} gross{(', with ' + BANDS[1]['band'] + ' close behind at ' + M(BANDS[1]['gross'])) if len(BANDS) > 1 else ''}. The typical purchase was {M(MED)}, which means more people said yes at friendly prices."

NOTES = {
    FANS[0]["id"]: ("Five visits, led the whole week", f"{E(FANS[0]['name'])} spent {M(FANS[0]['net_w'])} over {N(FANS[0]['n_sessions'])} visits, with a top purchase of {M(FANS[0]['max_ticket'])}."),
    FANS[1]["id"]: ("New this week, strong first days", f"{E(FANS[1]['name'])} arrived recently and has already spent {M(FANS[1]['net_w'])}, topping out at {M(FANS[1]['max_ticket'])}."),
    FANS[2]["id"]: ("Long-time supporter, back again", f"{E(FANS[2]['name'])} has been with you about a year and added {M(FANS[2]['net_w'])} this week."),
}

MOVES = [
    ("Today", "Thank the week's leader", f"We follow up personally with {E(FANS[0]['name'])}, who spent {M(FANS[0]['net_w'])} across {N(FANS[0]['n_sessions'])} visits, so the connection stays warm."),
    ("This week", "Welcome the newest regular", f"{E(FANS[1]['name'])} spent {M(FANS[1]['net_w'])} in their first days, and we keep the conversation personal while the interest is fresh."),
    ("All week", "Spread the strong nights", f"{BEST_DAY} brought in {M(BEST_NET)}, so we plan more of your best moments across the quieter days."),
]

GOOD30 = f"In 30 days, good looks like weekly totals above {M(NET)}, more than {N(BUYERS)} buyers each week, and a few more names sharing the top of your list."

PENDING = [
    ("On ours", "Your invoice is in", "This week's invoice lands today alongside this report. It comes from the Infloww record, so small differences from these platform-reported figures are normal."),
]

CLOSE = f"A {M(NET)} week, up 12 percent, built on people who keep coming back. <em>The next step is giving more of them a reason to.</em>"

WEEK_HEAD = f"Up 12 percent, <em>{M(NET)} net</em>"

KN = [
    (E(FANS[0]["name"]), f"Your biggest supporter this week at {M(FANS[0]['net_w'])}, returning {N(FANS[0]['n_sessions'])} times with a top purchase of {M(FANS[0]['max_ticket'])}."),
    (E(FANS[1]["name"]), f"New to your page and already at {M(FANS[1]['net_w'])}, with a single purchase as high as {M(FANS[1]['max_ticket'])}."),
    (E(FANS[2]["name"]), f"About a year with you and still buying, adding {M(FANS[2]['net_w'])} this week."),
]

WARN_FANS = (
    "Room for more names",
    f"{E(FANS[0]['name'])} brought in {M(FANS[0]['net_w'])} of your {M(NET)} this week, a wonderful run from one person.",
    f"Your top ten buyers made up about 82 percent of the week, so building up the next {N(BUYERS)} names is where the steady growth sits.",
)

STORY_X = [
    f"{E(FANS[0]['name'])} has been with you about a year and came back {N(FANS[0]['n_sessions'])} times this week, spending {M(FANS[0]['net_w'])} in total.",
    f"Their biggest single purchase was {M(FANS[0]['max_ticket'])}, and they were back within the last day, so the connection is clearly strong.",
]