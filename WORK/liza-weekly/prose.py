HOOK = [["A quieter week,", f"{M(NET)} still earned"], ["Your top three", "carried the week"]]

LEAD_1 = f"You made {M(NET)} this week from {N(BUYERS)} buyers, down from {M(PREV)} the week before. <em>The people who love your content kept showing up, and {E(FANS[0]['name'])} led with {M(FANS[0]['net_w'])}.</em>"

SHAPE = f"This week came in {M(PREV - NET)} under last week, so it was a softer seven days. Your best day was {E(BEST_DAY)} at {M(BEST_NET)}, and every day stayed above a solid floor."

SHAPE2 = f"Offers priced {E(BANDS[0]['band'])} brought in the most, at {M(BANDS[0]['gross'])}." + (f" Next came {E(BANDS[1]['band'])} at {M(BANDS[1]['gross'])}." if len(BANDS) > 1 else "") + f" The typical purchase held at {M(MED)}, so each buyer still spent what they usually do."

NOTES = {
    FANS[0]["id"]: ("Top spender, four nights", f"{E(FANS[0]['name'])} spent {M(FANS[0]['net_w'])} over {N(FANS[0]['n_sessions'])} nights, with a top purchase of {M(FANS[0]['max_ticket'])}."),
    FANS[1]["id"]: ("One night, top price", f"{E(FANS[1]['name'])} spent {M(FANS[1]['net_w'])} in a single night, with a top purchase of {M(FANS[1]['max_ticket'])}."),
    FANS[2]["id"]: ("Five years, a true regular", f"{E(FANS[2]['name'])} added {M(FANS[2]['net_w'])} this week, on top of {M(15276)} across five years with you."),
}

MOVES = [
    ("Today", "Thank your top three", f"We open warm, personal chats with {E(FANS[0]['name'])}, {E(FANS[1]['name'])} and {E(FANS[2]['name'])}, who gave you {M(FANS[0]['net_w'] + FANS[1]['net_w'] + FANS[2]['net_w'])} between them."),
    ("This week", "Bring back the regulars", f"We reach out one by one to people who bought last week and stayed quiet this week, to win back the {M(PREV - NET)} gap."),
    ("All week", "Lead with your best range", f"We keep offers in the {E(BANDS[0]['band'])} range at the front, since that range earned {M(BANDS[0]['gross'])} this week."),
]

GOOD30 = f"In 30 days, a good week is back near {M(PREV)}, with more than {N(BUYERS)} buyers and your top three still coming back night after night."

PENDING = [
    ("On ours", "Weekly invoice", f"Your invoice for this week lands today with this report, based on {M(NET)} in platform-reported figures."),
    ("On ours", "Custom requests", "We are tracking every custom request from this week so each one is delivered on time."),
]

CLOSE = f"A softer week still earned you {M(NET)}. <em>Your most loyal people are still here, and that is the base we build back on.</em>"

WEEK_HEAD = f"A softer week, <em>a steady top</em>"

KN = [
    (E(FANS[0]["name"]), f"Spent {M(FANS[0]['net_w'])} over {N(FANS[0]['n_sessions'])} nights and bought again in the last day, a regular for five years."),
    (E(FANS[1]["name"]), f"Spent {M(FANS[1]['net_w'])} in one night, with a top purchase of {M(FANS[1]['max_ticket'])}."),
    (E(FANS[2]["name"]), f"Added {M(FANS[2]['net_w'])} this week and has spent {M(15276)} with you over five years."),
]

WARN_FANS = (
    "Worth a warm hello",
    f"{E(FANS[2]['name'])} last bought about six days ago, after {N(FANS[2]['n_sessions'])} nights of buying this week.",
    "After five years with you, a personal note from us keeps that connection close.",
)

STORY_X = [
    f"{E(FANS[0]['name'])} has been with you for five years and spent {M(FANS[0]['net_w'])} this week across {N(FANS[0]['n_sessions'])} nights.",
    f"Their top purchase was {M(FANS[0]['max_ticket'])}, and they came back again within the last day.",
]