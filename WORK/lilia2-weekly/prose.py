HOOK = [["Up on last week", "by nearly three quarters"], ["Your closest supporters", "carried the week"]]

LEAD_1 = f"You made {M(NET)} this week against {M(PREV)} the week before, up {PCT(CHANGE,1)}. <em>{N(BUYERS)} people bought, and the typical purchase rose to {M(MED)}.</em>"

SHAPE = f"The week came in waves, not a steady line. {BEST_DAY} brought {M(BEST_NET)} on its own, and the quieter days still held between {M(9)} and {M(632)}. Most of the money came through your messages, where people who already know you said yes again."

SHAPE2 = f"Your highest-priced sets did best. {E(BANDS[0]['band'])} brought in {M(BANDS[0]['gross'])}{(', and ' + E(BANDS[1]['band']) + ' added ' + M(BANDS[1]['gross'])) if len(BANDS) > 1 else ''}. {N(NEWSUBS)} new subscribers joined this week, so the whole lift came from people already with you."

NOTES = {
    FANS[0]["id"]: ("Best week, 11 sessions", f"{E(FANS[0]['name'])} spent {M(FANS[0]['net_w'])} this week over {N(FANS[0]['n_sessions'])} sessions, topping out at {M(FANS[0]['max_ticket'])}."),
    FANS[1]["id"]: ("A year with you, still buying", f"{E(FANS[1]['name'])} added {M(FANS[1]['net_w'])} this week after a full year together, with a top purchase of {M(FANS[1]['max_ticket'])}."),
    FANS[2]["id"]: ("New this month, growing fast", f"{E(FANS[2]['name'])} joined a month ago and spent {M(FANS[2]['net_w'])} this week across {N(FANS[2]['n_sessions'])} sessions."),
}

MOVES = [
    ("Today", "A thank you to your top three", f"We open the week with a personal note to {E(FANS[0]['name'])}, {E(FANS[1]['name'])} and {E(FANS[2]['name'])}, with no offer attached."),
    ("This week", "More at the top of the range", f"Sets priced like {E(BANDS[0]['band'])} sold best, so we lead with those for the people who already buy at that level."),
    ("All week", "Fill the quiet days", f"We spread the warm conversations across the whole week, so the days that brought under {M(120)} catch up to the strong ones."),
]

GOOD30 = f"In 30 days, good looks like four weeks near {M(NET)}, not one. That means more than {N(BUYERS)} buyers each week, the typical purchase holding at {M(MED)} or above, and the first new subscribers arriving to join the people already with you."

PENDING = [
    ("On ours", "This week's invoice", "Your invoice lands today. It is built from these same platform figures, and the final split follows your usual statement."),
    ("On ours", "Notes for your top three", f"We are keeping a running note on {E(FANS[0]['name'])}, {E(FANS[1]['name'])} and {E(FANS[2]['name'])} so every conversation picks up where the last one ended."),
]

CLOSE = f"{M(NET)} this week, up {PCT(CHANGE,1)} on the last. <em>The people closest to you are spending more, and the plan is to keep it that way.</em>"

WEEK_HEAD = f"A stronger week <em>up {PCT(CHANGE,1)}</em>"

KN = [
    ("Two years with you", "awest42 has been subscribed for two years and spent $80 this week, with a top purchase of $100."),
    ("A first purchase", "JuanDoe bought for the first time this week, a single $100 purchase made in the last day."),
    ("Back twice", "Lee came back twice this week for $68 in total, the most recent one yesterday."),
]

WARN_FANS = (
    "A small, loyal circle",
    f"Ten people brought in 99% of this week, and {E(FANS[0]['name'])} alone brought {M(FANS[0]['net_w'])} of your {M(NET)}.",
    f"That loyalty is the strength of this account, and adding new buyers alongside them is the next step we are working on.",
)

STORY_X = [
    f"{E(FANS[0]['name'])} has been with you two months and has already spent over $13,000. This week alone they bought across {N(FANS[0]['n_sessions'])} sessions for {M(FANS[0]['net_w'])}.",
    f"Their biggest single purchase was {M(FANS[0]['max_ticket'])}, and their last one was under four days ago, so they are still close and still enjoying what you share.",
]