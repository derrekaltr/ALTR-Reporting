HOOK = [["Up a third", "on last week"], ["Bigger purchases,", "same people"]]

LEAD_1 = f"You made {M(NET)} this week, up from {M(PREV)} the week before. <em>Your typical purchase almost doubled, to {M(MED)}.</em>"

SHAPE = f"Your best day was {BEST_DAY} at {M(BEST_NET)}, and four other days came in near {M(1450)}. Wednesday and Thursday were quieter at {M(375)} and {M(498)}, which is where next week has the most room."

SHAPE2 = f"{N(BUYERS)} people bought from you this week, and {N(NEWSUBS)} new subscribers joined. Your top ten spenders made up {PCT(63.3,1)} of the week, so a few close relationships are carrying a lot of it."

NOTES = {
    FANS[0]["id"]: ("Biggest week, three weeks in", f"{E(FANS[0]['name'])} spent {M(FANS[0]['net_w'])} this week across {N(FANS[0]['n_sessions'])} long visits."),
    FANS[1]["id"]: (f"Back {N(FANS[1]['n_sessions'])} times, bought yesterday", f"{E(FANS[1]['name'])} spent {M(FANS[1]['net_w'])} and went as high as {M(FANS[1]['max_ticket'])} in one go."),
    FANS[2]["id"]: (f"Two visits, top buy {M(FANS[2]['max_ticket'])}", f"{E(FANS[2]['name'])} spent {M(FANS[2]['net_w'])} this week and is happy at the top of your range."),
}

MOVES = [
    ("Today", f"A thank you to {E(FANS[0]['name'])}", f"After {M(FANS[0]['net_w'])} this week, they get a personal note from you, with nothing attached."),
    ("This week", "Lift the quiet middle", f"We plan Wednesday and Thursday around fresh sets, aiming for {M(1000)} on each instead of under {M(500)}."),
    ("All week", "Keep prices where they sell", f"Your {BANDS[0]['band']} range brought in {M(BANDS[0]['gross'])}, so we keep building sets at that level." + (f" {BANDS[1]['band']} follows at {M(BANDS[1]['gross'])}." if len(BANDS) > 1 else "")),
]

GOOD30 = f"In 30 days, good looks like four weeks close to {M(NET)}, no day under {M(800)}, and {E(FANS[0]['name'])}, {E(FANS[1]['name'])} and {E(FANS[2]['name'])} still buying from you."

PENDING = [
    ("On ours", "Midweek plan", f"We are building Wednesday and Thursday around your strongest sets, using what worked on {BEST_DAY}."),
    ("On your side", "This week's invoice", "Your invoice arrives with this report, based on platform-reported figures."),
]

CLOSE = f"{M(NET)} in seven days, <em>and the people spending most are still here.</em>"

WEEK_HEAD = f"Up {PCT(CHANGE,1)} <em>on last week</em>"

KN = [
    (E(FANS[0]["name"]), f"Joined about three weeks ago and spent {M(FANS[0]['net_w'])} this week, your biggest single supporter."),
    (E(FANS[1]["name"]), f"Came back {N(FANS[1]['n_sessions'])} times this week for {M(FANS[1]['net_w'])}, and bought again within the last day."),
    (E(FANS[2]["name"]), f"Spent {M(FANS[2]['net_w'])} in two visits, with a top purchase of {M(FANS[2]['max_ticket'])}."),
]

WARN_FANS = (
    "Two quiet days",
    f"Wednesday and Thursday brought in {M(873)} together, about a third of {BEST_DAY}.",
    "Those are the days with the most room, and next week's plan starts there.",
)

STORY_X = [
    f"{E(FANS[0]['name'])} found you about three weeks ago and spent {M(FANS[0]['net_w'])} with you this week alone.",
    f"Their biggest single purchase was {M(FANS[0]['max_ticket'])}, so this came from steady attention over {N(FANS[0]['n_sessions'])} visits, not one big moment.",
]