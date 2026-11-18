HOOK = [["A quieter week", "with a strong close"], ["Three people led", "and a new one arrived"]]

LEAD_1 = f"You made {M(NET)} this week, down from {M(PREV)} the week before, across {N(BUYERS)} buyers. <em>The last three days brought $747 of it, and your typical purchase rose to {M(MED)}.</em>"

SHAPE = f"The week started slowly, with four days between $84 and $118. Then {E(str(BEST_DAY))} lifted to {M(BEST_NET)}, your best day, and the two days after it held above $190. Your ten biggest supporters made up 82.9% of the week, so a small group is carrying most of it."

SHAPE2 = f"Most of the money came from personal messages and a little from tips. Your strongest price range was {E(BANDS[0]['band'])} at {M(BANDS[0]['gross'])}" + (f", followed by {E(BANDS[1]['band'])} at {M(BANDS[1]['gross'])}." if len(BANDS) > 1 else ".") + " The people who buy from you are happy to spend more when the moment feels personal."

NOTES = {
    FANS[0]["id"]: ("Eleven months in, top buy of $200", f"{E(FANS[0]['name'])} spent {M(FANS[0]['net_w'])} across {N(FANS[0]['n_sessions'])} separate visits this week, more than anyone else."),
    FANS[1]["id"]: ("Long-time subscriber, two buys", f"{E(FANS[1]['name'])} spent {M(FANS[1]['net_w'])} this week, with a single purchase of {M(FANS[1]['max_ticket'])}."),
    FANS[2]["id"]: ("First day here, $168 already", f"{E(FANS[2]['name'])} spent {M(FANS[2]['net_w'])} within a day of subscribing, a strong start."),
}

MOVES = [
    ("Today", "Thank the top three", f"{E(FANS[0]['name'])}, {E(FANS[1]['name'])} and {E(FANS[2]['name'])} all bought in the last two days, so a warm personal note lands while it is fresh."),
    ("This week", "Build on the strong close", f"{E(str(BEST_DAY))} reached {M(BEST_NET)}, so we plan the next personal offers around the same days and hours."),
    ("All week", "Keep the new arrival close", f"{E(FANS[2]['name'])} spent {M(FANS[2]['net_w'])} on day one, and we keep the conversation going so that first week becomes a habit."),
]

GOOD30 = f"In 30 days, good looks like weeks back above {M(PREV)}, more than {N(BUYERS)} buyers each week, and {E(FANS[2]['name'])} still buying a month after joining."

PENDING = [
    ("On ours", "This week's invoice", "Your invoice for the week lands today alongside this report, built from the same platform-reported figures."),
    ("On ours", "A note for newcomers", f"We are keeping a close eye on {E(FANS[2]['name'])} and anyone else who joins, so their first week feels personal."),
]

CLOSE = f"A softer week at {M(NET)}, but the people who love your page showed up when it counted. <em>{E(FANS[0]['name'])} alone gave {M(FANS[0]['net_w'])}, and the week ended stronger than it began.</em>"

WEEK_HEAD = f"Down from {M(PREV)}, <em>strong at the top</em>"

KN = [
    ("Your most loyal", f"{E(FANS[0]['name'])} has been with you for eleven months and spent {M(FANS[0]['net_w'])} this week, with a top purchase of {M(FANS[0]['max_ticket'])}."),
    ("A big spend", f"{E(FANS[1]['name'])} has subscribed for ten months and spent {M(FANS[1]['net_w'])} this week in {N(FANS[1]['n_sessions'])} visits."),
    ("The newcomer", f"{E(FANS[2]['name'])} joined a day ago and has already spent {M(FANS[2]['net_w'])}, with one purchase of {M(FANS[2]['max_ticket'])}."),
]

WARN_FANS = ("Two names to warm up", "Vagician and Chad Scott each bought earlier in the week and have been quiet for about five days since.", "A friendly personal message is usually all it takes to bring regulars like these back.")

STORY_X = [
    f"{E(FANS[0]['name'])} has been with you for eleven months and spent {M(FANS[0]['net_w'])} this week across {N(FANS[0]['n_sessions'])} visits, the most of anyone.",
    f"Their biggest single purchase was {M(FANS[0]['max_ticket'])}, so they are glad to spend more when something feels made for them.",
]