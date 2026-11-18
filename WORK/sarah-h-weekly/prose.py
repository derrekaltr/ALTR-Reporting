HOOK = [["A softer week", "with a strong middle"], [f"{M(NET)} in seven days", "at a higher median"]]

LEAD_1 = f"You made {M(NET)} this week, {PCT(abs(CHANGE),1)} under last week's {M(PREV)}. {N(BUYERS)} people bought from you, and <em>the median purchase rose from {M(33)} to {M(MED)}</em>."

SHAPE = f"The week built to a peak. {BEST_DAY} was the best day at {M(BEST_NET)}, {PCT(BEST_SHARE,1)} of the week, and four days in a row cleared {M(8700)}. The last two days were quieter at {M(4958)} and {M(4055)}, and that drop is most of the gap to last week."

SHAPE2 = f"Messages brought in {M(50157)} of the {M(NET)}, with {M(4296)} in tips and {M(4438)} from subscriptions. Higher prices held up well. Offers from {M(70)} to {M(99)} were bought {PCT(39.1,1)} of the time, and offers of {M(150)} and up were bought {PCT(36.0,1)} of the time. Under {M(20)}, it was {PCT(21.3,1)}."

NOTES = {
    FANS[0]["id"]: ("13 visits, top purchase $200", f"{E(FANS[0]['name'])} spent {M(FANS[0]['net_w'])} across {N(FANS[0]['n_sessions'])} separate visits this week."),
    FANS[1]["id"]: ("New this week, $1,440 in 3 days", f"{E(FANS[1]['name'])} joined three days ago and has already spent {M(FANS[1]['net_w'])}."),
    FANS[2]["id"]: ("Three visits, up to $200", f"{E(FANS[2]['name'])} spent {M(FANS[2]['net_w'])} in {N(FANS[2]['n_sessions'])} visits, topping out at {M(FANS[2]['max_ticket'])}."),
}

MOVES = [
    ("Today", "Lift the quiet days", f"We are building the start of the week to match the middle, with new sets ready for the days that came in under {M(5000)}."),
    ("This week", "Welcome the new ones", f"{N(NEWSUBS)} people subscribed this week, and we are writing to each top new arrival personally in their first days."),
    ("All week", "Keep the higher prices", f"Offers from {M(70)} up sold almost twice as often as those under {M(20)}, so we are keeping your best work at your best prices."),
]

GOOD30 = f"In 30 days, good looks like every day clearing {M(7000)}, the median purchase holding at {M(MED)} or above, and more of this week's {N(NEWSUBS)} new subscribers spending in their first month."

PENDING = [
    ("On ours", "This week's invoice", "The invoice for this week lands today with this report. It uses the same platform-reported figures."),
]

CLOSE = f"Even in a softer week, {N(BUYERS)} people chose to spend with you, and <em>the strong middle of the week shows the room you have to grow</em>."

WEEK_HEAD = f"{M(NET)} this week, <em>{BEST_DAY} led the way</em>"

KN = [
    (E(FANS[0]["name"]), f"Your most loyal buyer this week, spending {M(FANS[0]['net_w'])} over {N(FANS[0]['n_sessions'])} visits with a top purchase of {M(FANS[0]['max_ticket'])}."),
    (E(FANS[1]["name"]), f"Brand new and already at {M(FANS[1]['net_w'])} in three days, with a top purchase of {M(FANS[1]['max_ticket'])}."),
    (E(FANS[2]["name"]), f"Spent {M(FANS[2]['net_w'])} in {N(FANS[2]['n_sessions'])} visits and is happy at the {M(200)} level."),
]

WARN_FANS = ("One to welcome back", f"The dude spent {M(1123)} this week and {M(1726)} since joining a month ago, and their subscription is no longer active.", "We are reaching out warmly so they stay close to you.")

STORY_X = [
    f"{E(FANS[0]['name'])} came back {N(FANS[0]['n_sessions'])} times in seven days and spent {M(FANS[0]['net_w'])}, the most of anyone this week.",
    f"Their last purchase was less than a day ago, so they are still very much with you going into next week.",
]