HOOK = [[f"{M(NET)} this week,", "spread across many"], [f"{N(BUYERS)} people bought,", "nobody carried it"]]

LEAD_1 = f"You made {M(NET)} this week, {PCT(abs(CHANGE),1)} under last week's {M(PREV)}. <em>{N(BUYERS)} people bought from you, and the median purchase held at {M(MED)}.</em>"

SHAPE = f"Your best day was {E(BEST_DAY)} at {M(BEST_NET)}, and the week finished strong with {M(3127)} on Wednesday. Monday was the quiet one at {M(2126)}, about {M(1260)} under the best day. Lifting that one day is most of the gap to last week."

SHAPE2 = f"Messages brought in {M(17102)}, about 84% of the week, with tips at {M(1582)} and subscriptions at {M(1607)}. Your top ten spenders made up about 22% of the total. Hundreds of people each added a little, which makes the week steady."

NOTES = {
    FANS[0]["id"]: ("New this week, your top spender", f"{E(FANS[0]['name'])} spent {M(FANS[0]['net_w'])} across {N(FANS[0]['n_sessions'])} sessions, with a top purchase of {M(FANS[0]['max_ticket'])}."),
    FANS[1]["id"]: ("Three visits in three days", f"{E(FANS[1]['name'])} spent {M(FANS[1]['net_w'])} over {N(FANS[1]['n_sessions'])} sessions, with a top purchase of {M(FANS[1]['max_ticket'])}."),
    FANS[2]["id"]: ("One night, one big purchase", f"{E(FANS[2]['name'])} spent {M(FANS[2]['net_w'])} in a single visit, with a top purchase of {M(FANS[2]['max_ticket'])}."),
}

MOVES = [
    ("Today", f"A hello for {E(FANS[0]['name'])}", f"{E(FANS[0]['name'])} spent {M(FANS[0]['net_w'])} in his first six days and has been quiet for five, so we open a warm, personal conversation today."),
    ("This week", "Lift the Monday dip", f"Monday was your lowest day at {M(2126)}, so we plan something special for that evening to bring it closer to {M(2800)}."),
    ("All week", "Reels into new subscribers", f"Your best reel reached 700,675 views while {N(NEWSUBS)} new subscribers joined, so we point more of those viewers toward your page."),
]

GOOD30 = f"In 30 days, good looks like weeks back above {M(PREV)}, Mondays near {M(2800)}, and well over {N(NEWSUBS)} new subscribers a week as your reels send more people to your page."

PENDING = [
    ("On ours", "This week's invoice", f"Your invoice for this week arrives today with this report. It uses the same platform-reported figures you see here."),
]

CLOSE = f"{N(BUYERS)} people chose to spend with you this week. <em>That wide base is the floor we build on next.</em>"

WEEK_HEAD = f"Just under last week, <em>held up by many</em>"

KN = [
    (E(FANS[0]["name"]), f"{E(FANS[0]['name'])} is new, spent {M(FANS[0]['net_w'])} in six days and was happy to pay {M(FANS[0]['max_ticket'])} for one purchase."),
    (E(FANS[1]["name"]), f"{E(FANS[1]['name'])} came back {N(FANS[1]['n_sessions'])} times in three days and spent {M(FANS[1]['net_w'])}, with a last purchase about two days ago."),
    (E(FANS[2]["name"]), f"{E(FANS[2]['name'])} spent {M(FANS[2]['net_w'])} in a single visit just yesterday, so this is a fresh conversation."),
]

WARN_FANS = (
    "Two gone quiet",
    f"{E(FANS[0]['name'])} spent {M(FANS[0]['net_w'])} and has not bought in about five days.",
    f"josh2000 spent {M(330)} across two visits and has been quiet for five days too. A friendly hello often brings people like this back.",
)

STORY_X = [
    f"{E(FANS[0]['name'])} found you six days ago and spent {M(FANS[0]['net_w'])} across {N(FANS[0]['n_sessions'])} visits, more than anyone else this week.",
    f"His biggest single purchase was {M(FANS[0]['max_ticket'])}, so he is happy to pay at your top price.",
]