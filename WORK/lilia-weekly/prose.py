HOOK = [["A quiet week,", "one loyal regular"], ["Frank carried it,", "room to grow next"]]

LEAD_1 = f"This week closed at {M(NET)} against {M(PREV)} the week before, down {PCT(abs(CHANGE),1)}. {N(BUYERS)} people bought, and <em>{E(FANS[0]['name'])} alone brought in {M(FANS[0]['net_w'])}</em>."

SHAPE = f"Your best day was {E(BEST_DAY)} at {M(BEST_NET)}, which is {PCT(BEST_SHARE,1)} of the week in one evening. The rest of the week was quiet. The middle purchase came in at {M(MED)}, so most of your income this week came from one strong night with someone who already knows you."

SHAPE2 = (f"Spending landed in two price ranges: {E(BANDS[0]['band'])} brought {M(BANDS[0]['gross'])} and {E(BANDS[1]['band'])} brought {M(BANDS[1]['gross'])}. Nothing sold above that this week. That means the higher price ranges are wide open for next week." if len(BANDS) > 1 else (f"Spending landed mostly in the {E(BANDS[0]['band'])} range, at {M(BANDS[0]['gross'])}. Nothing sold above that this week. That means the higher price ranges are wide open for next week." if BANDS else f"Spending this week stayed in the smaller price ranges. That means the higher price ranges are wide open for next week."))

NOTES = {
    FANS[0]["id"]: ("A year with you, top spender", f"{E(FANS[0]['name'])} spent {M(FANS[0]['net_w'])} across {N(FANS[0]['n_sessions'])} visits, with one purchase at {M(FANS[0]['max_ticket'])}."),
    FANS[1]["id"]: ("New buyer, bought today", f"{E(FANS[1]['name'])} made a first purchase of {M(FANS[1]['max_ticket'])}, a fresh start to build on."),
    FANS[2]["id"]: ("New buyer, one small unlock", f"{E(FANS[2]['name'])} spent {M(FANS[2]['net_w'])} this week, a first step in."),
}

MOVES = [
    ("Today", "A warm hello to Frank", f"{E(FANS[0]['name'])} has been with you a year and spent {M(FANS[0]['net_w'])} this week, so a personal note keeps that going."),
    ("This week", "Welcome the new buyers", f"{E(FANS[1]['name'])} and {E(FANS[2]['name'])} each made a first purchase, and a friendly follow-up turns one buy into a habit."),
    ("All week", "Spread the good nights", f"Your best day carried {PCT(BEST_SHARE,1)} of the week, so we will space your offers so more days look like {E(BEST_DAY)}."),
]

GOOD30 = f"In 30 days, good looks like more than {N(BUYERS)} buyers a week, a middle purchase back above {M(MED)}, and a week that does not depend on one night. Getting back past {M(PREV)} is a fair first target."

PENDING = [
    ("On ours", "Steadier weekdays", f"We are spacing your offers across the week so the {M(BEST_NET)} night is not the only strong one."),
]

CLOSE = f"A {M(NET)} week is a quiet one, and it showed us something useful. <em>Your regulars are still here, and two new people just said yes.</em>"

WEEK_HEAD = f"A slower week, <em>a loyal core</em>"

KN = [
    ("Your top supporter", f"{E(FANS[0]['name'])} spent {M(FANS[0]['net_w'])} this week and has been with you for a year."),
    ("Your best day", f"{E(BEST_DAY)} brought in {M(BEST_NET)}, {PCT(BEST_SHARE,1)} of the whole week."),
    ("Your buyers", f"{N(BUYERS)} people bought this week, with a middle purchase of {M(MED)}."),
]

WARN_FANS = ("Two new faces, one regular", f"Three people made up the whole week, and {E(FANS[0]['name'])} was {M(FANS[0]['net_w'])} of the {M(NET)}.", f"{E(FANS[1]['name'])} and {E(FANS[2]['name'])} are new buyers, so the people who carry next week are already on your page.")

STORY_X = [
    f"{E(FANS[0]['name'])} has been with you for a year and came back {N(FANS[0]['n_sessions'])} times this week, with one purchase at {M(FANS[0]['max_ticket'])}.",
    f"That kind of loyalty is the base of your page, and it gives every quiet week a floor of about {M(FANS[0]['net_w'])}.",
]