HOOK = [["A softer week", "with a strong finish"], ["Saturday closed", "as your best night"]]

LEAD_1 = f"You made {M(NET)} this week, down {PCT(abs(CHANGE),1)} from {M(PREV)} the week before. <em>The last three days brought in {M(214)}, and the week ended on its best night.</em>"

SHAPE = f"The week opened at {M(35)}, then sat at {M(18)} for two days. From there it climbed every evening until {E(BEST_DAY)} closed at {M(BEST_NET)}, {PCT(BEST_SHARE,1)} of the whole week on one night."

SHAPE2 = f"{N(BUYERS)} people bought from you this week, and the typical purchase was {M(MED)}, close to last week's {M(24)}. Your top ten supporters made up {PCT(95.3,1)} of the week, so a few familiar names carry a lot of it."

NOTES = {
    FANS[0]["id"]: ("Six buys this week, top one $57", f"{E(FANS[0]['name'])} has been with you 18 days and has already spent {M(307)} in total."),
    FANS[1]["id"]: ("Three months in, one $39 buy", f"{E(FANS[1]['name'])} spent {M(FANS[1]['net_w'])} in a single visit and has given you {M(276)} so far."),
    FANS[2]["id"]: ("New name, two buys this week", f"{E(FANS[2]['name'])} came back a second time inside the week for {M(FANS[2]['net_w'])}."),
}

MOVES = [
    ("Today", "A thank you to alfaman", f"We open the week with a personal note to {E(FANS[0]['name'])}, who bought {N(FANS[0]['n_sessions'])} times for {M(FANS[0]['net_w'])}."),
    ("This week", "Lean into late week", f"Thursday to Saturday made {M(214)} of your {M(NET)}, so we save the strongest offers for those nights."),
    ("All week", "Warm up longtime names", f"Ero_E has been with you five months and spent {M(300)}. We check in with supporters like them with something new."),
]

GOOD30 = f"A good month from here looks like four nights a week at {M(50)} or more, {N(20)} buyers a week instead of {N(BUYERS)}, and the week back above {M(PREV)}."

PENDING = [
    ("On ours", "Late-week lineup", f"We are planning your best sets for Thursday to Saturday, the nights that brought in {M(214)} this week."),
]

CLOSE = f"{M(NET)} this week, and <em>{M(BEST_NET)} on the final night alone</em>."

WEEK_HEAD = f"A quiet start, <em>a strong finish</em>"

KN = [
    (E(FANS[0]["name"]), f"{N(FANS[0]['n_sessions'])} buys this week for {M(FANS[0]['net_w'])}, the most of anyone, with a top purchase of {M(FANS[0]['max_ticket'])}."),
    (E(FANS[1]["name"]), f"Three months with you and {M(FANS[1]['net_w'])} this week in one visit, {M(276)} in total."),
    (E(FANS[2]["name"]), f"New to the list this week, came back twice for {M(FANS[2]['net_w'])} in all."),
]

WARN_FANS = (
    "Familiar names, lighter week",
    f"Beanie Girl and Ero_E have been with you for months and bought once each this week, {M(49)} and {M(18)}.",
    f"Both are still subscribed, and between them they have spent {M(576)} with you so far.",
)

STORY_X = [
    f"{E(FANS[0]['name'])} found you 18 days ago and has already spent {M(307)}, with {M(FANS[0]['net_w'])} of it this week.",
    f"They came back {N(FANS[0]['n_sessions'])} times in seven days, and their biggest purchase was {M(FANS[0]['max_ticket'])}.",
]