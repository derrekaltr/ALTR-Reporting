HOOK = [["A softer week,", "a strong finish"], ["Four big nights", "in the last five"]]

LEAD_1 = f"You made {M(NET)} this week, down {PCT(abs(CHANGE),1)} from {M(PREV)} the week before. <em>From Tuesday on, four of five nights passed $1,200.</em>"

SHAPE = f"The week started quiet, with $318 on Sunday and $293 on Monday. Then {BEST_DAY} brought {M(BEST_NET)}, {PCT(BEST_SHARE,1)} of the week, and Thursday and Saturday came close behind."

SHAPE2 = f"{N(BUYERS)} people bought from you this week. The typical purchase was {M(MED)}, down from $29 last week, and the {BANDS[0]['band']} range earned the most at {M(BANDS[0]['gross'])}" + (f", followed by {BANDS[1]['band']} at {M(BANDS[1]['gross'])}." if len(BANDS) > 1 else ".")

NOTES = {
    FANS[0]["id"]: ("New this week, one big night", f"{E(FANS[0]['name'])} joined four days ago and sent {M(FANS[0]['net_w'])} in a single evening."),
    FANS[1]["id"]: (f"Two nights, top buy {M(FANS[1]['max_ticket'])}", f"{E(FANS[1]['name'])} came back for a second night and sent {M(FANS[1]['net_w'])} in total."),
    FANS[2]["id"]: (f"Two visits, best at {M(FANS[2]['max_ticket'])}", f"{E(FANS[2]['name'])} bought on {N(FANS[2]['n_sessions'])} nights this week for {M(FANS[2]['net_w'])}."),
}

MOVES = [
    ("Today", "A thank you to the top three", f"{E(FANS[0]['name'])}, {E(FANS[1]['name'])} and {E(FANS[2]['name'])} together sent {M(FANS[0]['net_w'] + FANS[1]['net_w'] + FANS[2]['net_w'])}, and a personal note from you keeps that warmth going."),
    ("This week", f"Lead with {BANDS[0]['band']}", f"That range brought {M(BANDS[0]['gross'])} this week, so your best new sets will be priced there first."),
    ("All week", "Lift the quiet start", "Sunday and Monday brought $611 together, so we are moving your strongest sets earlier in the week to match the Tuesday pace."),
]

GOOD30 = f"In 30 days, good looks like every night closer to the $1,359 you made on Saturday, the typical purchase back near $29, and a week that tops {M(PREV)} again."

PENDING = [
    ("On ours", "This week's invoice", "Your invoice for the week arrives with this report, built from the same platform-reported figures."),
]

CLOSE = f"This week ended at {M(NET)}, and the back half ran strong. <em>Four nights over $1,200 is the pace we build on.</em>"

WEEK_HEAD = f"A slow start, <em>a strong back half</em>"

KN = [
    (E(FANS[0]["name"]), f"New to your page four days ago, {E(FANS[0]['name'])} sent {M(FANS[0]['net_w'])} in one night, with a top purchase of {M(FANS[0]['max_ticket'])}."),
    (E(FANS[1]["name"]), f"{E(FANS[1]['name'])} bought on {N(FANS[1]['n_sessions'])} nights for {M(FANS[1]['net_w'])}, and went as high as {M(FANS[1]['max_ticket'])}."),
    (E(FANS[2]["name"]), f"{E(FANS[2]['name'])} also reached {M(FANS[2]['max_ticket'])} at the top and sent {M(FANS[2]['net_w'])} across {N(FANS[2]['n_sessions'])} nights."),
]

WARN_FANS = (
    "Smaller purchases, more room",
    f"The typical purchase was {M(MED)} this week, down from $29, while {N(BUYERS)} people still bought from you.",
    "Your top ten gave 41% of the week, so there is a lot of room in the rest of your list.",
)

STORY_X = [
    f"{E(FANS[0]['name'])} found your page four days ago and spent {M(FANS[0]['net_w'])} on the first night, with one purchase of {M(FANS[0]['max_ticket'])}.",
    f"That one evening made {E(FANS[0]['name'])} your top buyer of the week, ahead of people who came back two or three times.",
]