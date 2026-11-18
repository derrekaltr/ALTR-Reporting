HOOK = [["Up 74% on last week", "led by your regulars"], ["Fewer buyers, bigger", "nights from each one"]]

LEAD_1 = f"You made {M(NET)} this week, up from {M(PREV)}, a change of {PCT(CHANGE,1)}. <em>{N(BUYERS)} people bought, and the typical purchase rose to {M(MED)}.</em>"

SHAPE = f"The week opened strong. {BEST_DAY} brought in {M(BEST_NET)}, or {PCT(BEST_SHARE,1)} of the whole week, and the next few days held well above the floor. Almost all of the money came through private messages, and your ten biggest supporters made up about 80% of it."

SHAPE2 = f"Price was not a barrier this week. Most of the revenue came from the {BANDS[0]['band']} range ({M(BANDS[0]['gross'])})" + (f", with {BANDS[1]['band']} next at {M(BANDS[1]['gross'])}." if len(BANDS) > 1 else ".") + f" A higher median of {M(MED)} shows people paid more each time they bought."

NOTES = {
    FANS[0]["id"]: ("5 years with you, one $200 night", f"{E(FANS[0]['name'])} spent {M(FANS[0]['net_w'])} in a single evening, with a top purchase of {M(FANS[0]['max_ticket'])}."),
    FANS[1]["id"]: ("Back 12 times this week", f"{E(FANS[1]['name'])} came back {N(FANS[1]['n_sessions'])} times for {M(FANS[1]['net_w'])}, the steadiest presence of your week."),
    FANS[2]["id"]: ("Four days in, already a top three", f"{E(FANS[2]['name'])} joined this week and has already spent {M(FANS[2]['net_w'])} across {N(FANS[2]['n_sessions'])} visits."),
}

MOVES = [
    ("Today", "Thank the top three", f"We reply personally to {E(FANS[0]['name'])}, {E(FANS[1]['name'])} and {E(FANS[2]['name'])}, so the people who carried {M(FANS[0]['net_w'] + FANS[1]['net_w'] + FANS[2]['net_w'])} this week feel noticed."),
    ("This week", "Welcome the newest", "Two of your top six joined in the last four days. We keep their first week warm and personal so they settle in."),
    ("All week", "Hold the midweek line", f"The opening day reached {M(BEST_NET)}. We spread the strongest moments across the week so the quieter days rise toward it."),
]

GOOD30 = f"In 30 days, a good result is weeks that hold near {M(NET)} with less riding on one night. That means more people buying a second time and the newest arrivals turning into regulars like {E(FANS[1]['name'])}."

PENDING = [
    ("On ours", "This week's statement", "Your weekly statement arrives alongside this report, built from the same platform-reported figures."),
]

CLOSE = f"A week of {M(NET)}, up {PCT(CHANGE,1)}, with long-time supporters and brand new ones both showing up. <em>The people who love your page are spending more each time.</em>"

WEEK_HEAD = f"Up {PCT(CHANGE,1)} this week <em>at {M(NET)} in</em>"

KN = [
    ("Rob", "Two years with you and $16,385 lifetime. He came back three times this week for $160, the last visit less than a day ago."),
    ("John", "Joined two days ago and spent $100 on his first purchase, $150 so far. A strong first impression to build on."),
    ("Paul", "Five years with you and $147 this week across two visits, with a top purchase of $85."),
]

WARN_FANS = (
    "Two familiar faces resting",
    f"{E(FANS[0]['name'])} spent {M(FANS[0]['net_w'])} in one night nearly seven days ago and has been quiet since. With five years and $5,704 behind him, he is worth a warm hello.",
    "Paul last bought about five days ago. Long-time supporters like these two often return with a personal note rather than a new offer.",
)

STORY_X = [
    f"{E(FANS[0]['name'])} has been with you for five years and has spent $5,704 in that time. This week he made one visit and spent {M(FANS[0]['net_w'])}, with a top purchase of {M(FANS[0]['max_ticket'])}.",
    f"That single evening was more than a quarter of your {M(NET)} week. Loyalty like that comes from years of feeling seen, and that is what we keep giving him.",
]