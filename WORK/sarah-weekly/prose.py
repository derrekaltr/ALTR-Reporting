HOOK = [["A softer week", "with real depth"], ["The top end held", "$100 and up sold best"]]

LEAD_1 = f"You made {M(NET)} this week, {PCT(abs(CHANGE),1)} below last week's {M(PREV)}. <em>{N(BUYERS)} people still bought from you, and the biggest single purchases reached {M(FANS[1]['max_ticket'])}.</em>"

SHAPE = f"The week opened at {M(936)} and built steadily to {M(BEST_NET)} on {BEST_DAY}, which was {PCT(BEST_SHARE,1)} of the week on its own. The weekend carried you, and the two days after it held above {M(1250)} each."

SHAPE2 = f"Price was never the thing holding people back. Pieces at $100 to $149 sold to 36.7% of the people who received them, and pieces under $20 sold to 17.6%. Your personal messages sold to 24.3% of the people who got them, across 750 sent, and the median purchase sat at {M(MED)}."

NOTES = {
    FANS[0]["id"]: ("Top spender this week", f"{E(FANS[0]['name'])} spent {M(FANS[0]['net_w'])} over {N(FANS[0]['n_sessions'])} visits, with one piece at {M(FANS[0]['max_ticket'])}."),
    FANS[1]["id"]: ("Four months with you", f"{E(FANS[1]['name'])} spent {M(FANS[1]['net_w'])} this week and {M(2161)} since they joined, with a top piece at {M(FANS[1]['max_ticket'])}."),
    FANS[2]["id"]: ("Four days in, already big", f"This new subscriber has spent {M(FANS[2]['net_w'])} in their first four days, across {N(FANS[2]['n_sessions'])} visits."),
}

MOVES = [
    ("Today", "A warm welcome back", f"{E(FANS[1]['name'])} spent {M(FANS[1]['net_w'])} this week before their subscription ended, so we are reaching out to them first."),
    ("This week", "Lead with the top tier", f"Pieces at $100 to $149 sold to 36.7% of people, double the rate under $20, so the bigger pieces go out first."),
    ("All week", "A stronger start", f"The first day of the week brought in {M(936)}. We are moving the best evenings earlier so the week opens closer to {BEST_DAY}'s {M(BEST_NET)}."),
]

GOOD30 = f"In 30 days, good looks like weeks back near {M(PREV)}. That means the {N(NEWSUBS)} people who joined this week buying a second time, {E(FANS[1]['name'])} subscribed again, and the $100 tier offered every week rather than now and then."

PENDING = [
    ("On ours", "Your weekly invoice", f"It lands today alongside this report, built from the same platform-reported figures as the {M(NET)} above."),
]

CLOSE = f"{N(BUYERS)} people bought from you this week, {N(NEWSUBS)} new subscribers joined, and {N(REBILLS)} renewed. <em>The people who spend the most are still here, and they are paying {M(FANS[0]['max_ticket'])} at a time.</em>"

WEEK_HEAD = f"{M(NET)} this week, <em>{N(BUYERS)} buyers</em>"

KN = [
    ("Jason", f"Six days in and already {M(385)} across 3 visits, with a top piece at {M(144)}."),
    ("WesR", f"Came back 7 times this week for {M(376)}, the most visits of anyone."),
    ("BigStun", f"Two days in, one purchase at {M(199)}, and still subscribed."),
]

WARN_FANS = (
    "One regular stepped back",
    f"{E(FANS[1]['name'])} has been with you for four months and has spent {M(2161)} in that time.",
    f"Their subscription ended this week, four days after a {M(FANS[1]['net_w'])} week, so a warm welcome back is the first move.",
)

STORY_X = [
    f"{E(FANS[0]['name'])} was your biggest spender this week at {M(FANS[0]['net_w'])}, across {N(FANS[0]['n_sessions'])} visits.",
    f"Their largest single purchase was {M(FANS[0]['max_ticket'])}, and they last bought a day and a half ago.",
]