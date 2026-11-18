HOOK = [["A quieter week","with bright nights"],["Your top buyers","spent up to $200"]]

LEAD_1 = f"You made {M(NET)} this week, down {PCT(abs(CHANGE),1)} from {M(PREV)}, from {N(BUYERS)} buyers. <em>Your best night brought in {M(BEST_NET)} on its own.</em>"

SHAPE = f"The week came in waves, not a slide. {E(BEST_DAY)} led with {M(BEST_NET)}, which is {PCT(BEST_SHARE,1)} of the week. Two more nights cleared $240, and the quiet days sat under $100."

SHAPE2 = f"Your higher-priced sets did the work. The {E(BANDS[0]['band'])} range brought in {M(BANDS[0]['gross'])}{(', and the ' + E(BANDS[1]['band']) + ' range added ' + M(BANDS[1]['gross'])) if len(BANDS) > 1 else ''}. The typical purchase was {M(MED)}, so your fans are paying for quality."

NOTES = {
    FANS[0]["id"]: ("Top spender, two visits", f"{E(FANS[0]['name'])} spent {M(FANS[0]['net_w'])} over {N(FANS[0]['n_sessions'])} visits, the biggest single one at {M(FANS[0]['max_ticket'])}."),
    FANS[1]["id"]: ("One visit, one big purchase", f"{E(FANS[1]['name'])} spent {M(FANS[1]['net_w'])} in a single visit, with a top purchase of {M(FANS[1]['max_ticket'])}."),
    FANS[2]["id"]: ("New this week, came back twice", f"{E(FANS[2]['name'])} spent {M(FANS[2]['net_w'])} across {N(FANS[2]['n_sessions'])} visits, the largest at {M(FANS[2]['max_ticket'])}."),
}

MOVES = [
    ("Today", "Welcome back the top three", f"We reach out personally to {E(FANS[0]['name'])}, {E(FANS[1]['name'])} and {E(FANS[2]['name'])}, who spent {M(FANS[0]['net_w'] + FANS[1]['net_w'] + FANS[2]['net_w'])} between them."),
    ("This week", "Lead with your best range", f"Your {E(BANDS[0]['band'])} sets earned {M(BANDS[0]['gross'])}, so the week's offers lean toward that range."),
    ("All week", "Build on the strong nights", f"Your best nights topped $300, so we save the best offers for evenings like {E(BEST_DAY)}."),
]

GOOD30 = f"In 30 days, good looks like weekly earnings back above {M(PREV)}, more than {N(BUYERS)} buyers each week, and new subscribers well past this week's {N(NEWSUBS)}."

PENDING = [
    ("On ours", "This week's invoice", "Your invoice for the week lands today with this report, built from the numbers you see here."),
    ("On your side", "New sets when ready", "Any new sets you shoot go straight to the fans already spending $100 and up."),
]

CLOSE = f"{M(NET)} this week from {N(BUYERS)} buyers, with {N(REBILLS)} subscribers renewing. <em>The people who love your work are still here, and they are spending.</em>"

WEEK_HEAD = f"A quieter week, <em>a strong top end</em>"

KN = [
    ("Renewals", f"{N(REBILLS)} subscribers renewed this week and stayed with you."),
    ("Typical purchase", f"The typical purchase was {M(MED)}, close to last week's $35."),
    ("Best night", f"{E(BEST_DAY)} brought in {M(BEST_NET)}, {PCT(BEST_SHARE,1)} of the week."),
]

WARN_FANS = (
    "One to welcome back",
    f"{E(FANS[0]['name'])} was your top spender at {M(FANS[0]['net_w'])}, and their subscription has since ended.",
    f"Their biggest purchase was {M(FANS[0]['max_ticket'])}, so we will reach out warmly this week to keep them close.",
)

STORY_X = [
    f"{E(FANS[1]['name'])} came in once this week and spent {M(FANS[1]['net_w'])}, with one purchase at {M(FANS[1]['max_ticket'])}.",
    f"That one visit showed how far your best work can go, and they are still subscribed.",
]