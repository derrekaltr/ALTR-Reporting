HOOK = [["A quieter week,", "with a strong finish"], ["Same people buying,", "smaller tickets"]]

LEAD_1 = f"You earned {M(NET)} this week, down from {M(PREV)} the week before. <em>{N(BUYERS)} people still bought, and the typical purchase came in at {M(MED)}, so the gap is ticket size, not interest.</em>"

SHAPE = f"The week had a clear rhythm. Quiet days sat between {M(38)} and {M(47)}, and every other day jumped to {M(119)}, then {M(118)}, then {M(BEST_NET)} on {BEST_DAY}, your best day of the week. Each lift came after a slower day, so the interest is steady and it comes in waves."

SHAPE2 = f"Most of your income came from purchases in the {BANDS[0]['band']} range{(', followed by ' + BANDS[1]['band']) if len(BANDS) > 1 else ''}. Last week the typical purchase was {M(48)}, and this week it was {M(MED)}. The same people are here, so bringing back a few larger sets at the price that already works is the quickest way back toward {M(PREV)}."

NOTES = {
    FANS[0]["id"]: ("2 years with you, 3 visits this week", f"{E(FANS[0]['name'])} came back {N(FANS[0]['n_sessions'])} times this week for {M(FANS[0]['net_w'])}, with a top purchase of {M(FANS[0]['max_ticket'])}."),
    FANS[1]["id"]: ("3 years, top single buy this week", f"{E(FANS[1]['name'])} spent {M(FANS[1]['net_w'])} in one visit, and their {M(FANS[1]['max_ticket'])} purchase was the largest of your week."),
    FANS[2]["id"]: ("New face, first buy this week", f"{E(FANS[2]['name'])} is new to your page and already spent {M(FANS[2]['net_w'])}, with a top purchase of {M(FANS[2]['max_ticket'])}."),
}

MOVES = [
    ("Today", "A warm hello to new faces", f"We open personal conversations with the {N(NEWSUBS)} people who joined this week, starting with {E(FANS[2]['name'])}, who bought within a day."),
    ("This week", "Larger sets at the right price", f"We bring back offers in the {BANDS[0]['band']} range for your regulars, so the typical purchase climbs back from {M(MED)} toward {M(48)}."),
    ("All week", "Build on the rhythm", f"Your strong days came every other day, topping out at {M(BEST_NET)}, so we plan the best offers for those evenings and keep the quiet days personal."),
]

GOOD30 = f"In 30 days, good looks like weekly earnings back above {M(PREV)}, a typical purchase near {M(48)} instead of {M(MED)}, and the {N(NEWSUBS)} people who joined this week turning into regulars like {E(FANS[0]['name'])}."

PENDING = [
    ("On ours", "This week's invoice", f"Your invoice for the week lands today with this report, based on the {M(NET)} earned."),
    ("On your side", "Fresh sets in the vault", f"Any new sets you shoot this week give us more to offer in the {BANDS[0]['band']} range, which is where your regulars spend."),
]

CLOSE = f"{M(NET)} this week from {N(BUYERS)} people who keep coming back, <em>and {M(PREV)} is well within reach.</em>"

WEEK_HEAD = f"A softer week, <em>a strong finish</em>"

KN = [
    (E(FANS[0]["name"]), f"{E(FANS[0]['name'])} has been with you 2 years and visited {N(FANS[0]['n_sessions'])} times this week, spending {M(FANS[0]['net_w'])}, more than anyone else."),
    (E(FANS[1]["name"]), f"{E(FANS[1]['name'])} has been with you 3 years and made your largest single purchase of the week at {M(FANS[1]['max_ticket'])}."),
    (E(FANS[2]["name"]), f"{E(FANS[2]['name'])} is brand new and spent {M(FANS[2]['net_w'])} in their first week, which makes them a great person to get to know."),
]

WARN_FANS = (
    "Familiar faces to keep close",
    f"{E(FANS[1]['name'])} has been with you for 3 years and spent {M(FANS[1]['net_w'])} this week, but their auto-renew is currently off.",
    f"A personal note in the next few days keeps a {M(1413)} lifetime relationship warm, and we will handle it gently.",
)

STORY_X = [
    f"{E(FANS[0]['name'])} has been with you for 2 years, has spent {M(1407)} in that time, and came back {N(FANS[0]['n_sessions'])} times this week.",
    f"Their {M(FANS[0]['net_w'])} this week made them your top supporter, and their last purchase was just a day ago.",
]