HOOK = [[f"{M(NET)} this week", "up from last week"], ["Your regulars", "led the way"]]

LEAD_1 = f"You made {M(NET)} this week against {M(PREV)} the week before, up {PCT(CHANGE,1)}. <em>{N(BUYERS)} people bought, and the typical purchase rose to {M(MED)}.</em>"

SHAPE = f"Every day this week cleared {M(794)}, and six of the seven landed above {M(1000)}. {BEST_DAY} was the high point at {M(BEST_NET)}, {PCT(BEST_SHARE,1)} of the week, so the money came from a steady rhythm rather than one lucky night."

SHAPE2 = f"Your private messages carried the week at {M(8844)} of the {M(NET)} total. The {BANDS[0]['band']} range brought in the most{(', with ' + BANDS[1]['band'] + ' close behind') if len(BANDS) > 1 else ''}, which shows your top buyers are happy to spend at the higher end."

NOTES = {
    FANS[0]["id"]: ("Four years in, top spender this week", f"Spent {M(FANS[0]['net_w'])} across {N(FANS[0]['n_sessions'])} visits this week, with a top purchase of {M(FANS[0]['max_ticket'])}."),
    FANS[1]["id"]: ("Bought again within the last day", f"Spent {M(FANS[1]['net_w'])} in {N(FANS[1]['n_sessions'])} visits, with a single purchase of {M(FANS[1]['max_ticket'])}."),
    FANS[2]["id"]: ("Two years in, first big week", f"Spent {M(FANS[2]['net_w'])} this week after two quiet years, topping out at {M(FANS[2]['max_ticket'])}."),
}

MOVES = [
    ("Today", "Thank your top three", f"We open personal notes with {E(FANS[0]['name'])}, {E(FANS[1]['name'])} and {E(FANS[2]['name'])}, who gave you {M(FANS[0]['net_w'] + FANS[1]['net_w'] + FANS[2]['net_w'])} between them this week."),
    ("This week", "Welcome the newest buyers", f"Several people who joined in the last ten days already spent up to {M(199)} in one go, so we give them the same warm attention your regulars get."),
    ("All week", "Keep the steady rhythm", f"Six days above {M(1000)} is the pattern to keep, so we hold the same pace of personal conversation every day, not only on the big nights."),
]

GOOD30 = f"In 30 days, good looks like every week landing near this one at about {M(NET)}, the typical purchase holding at {M(MED)} or higher, and the {N(REBILLS)} renewals this week growing as your longtime regulars stay close."

PENDING = [
    ("On ours", "Weekly invoice today", f"Your invoice for this week arrives alongside this report, based on the platform-reported {M(NET)}."),
]

CLOSE = f"A week up {PCT(CHANGE,1)} on the back of the people who know you best. <em>{M(NET)}, built one conversation at a time.</em>"

WEEK_HEAD = f"A steady climb, <em>up {PCT(CHANGE,1)}</em>"

KN = [
    (E(FANS[0]["name"]), f"With you four years and your top spender this week at {M(FANS[0]['net_w'])}, with a best purchase of {M(FANS[0]['max_ticket'])}."),
    (E(FANS[1]["name"]), f"Spent {M(FANS[1]['net_w'])} in just {N(FANS[1]['n_sessions'])} visits and bought again in the last day, so the conversation is warm right now."),
    (E(FANS[2]["name"]), f"Subscribed for two years and spent {M(FANS[2]['net_w'])} this week, the most they have ever spent with you."),
]

WARN_FANS = (
    "Worth a warm hello",
    f"{E(FANS[0]['name'])} last bought about six days ago, after spending {M(FANS[0]['net_w'])} earlier in the week.",
    "A friendly check-in keeps a four-year regular feeling seen, with nothing to sell attached.",
)

STORY_X = [
    f"{E(FANS[0]['name'])} has been with you for four years and spent {M(FANS[0]['net_w'])} this week across {N(FANS[0]['n_sessions'])} visits.",
    f"Their biggest single purchase was {M(FANS[0]['max_ticket'])}, a sign of how much a long, steady relationship is worth.",
]