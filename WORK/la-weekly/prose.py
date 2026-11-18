HOOK = [["A stronger week", "up 23 percent"], ["It built all week", "Saturday led it"]]

LEAD_1 = f"You made {M(NET)} this week, up from {M(PREV)}, a rise of {PCT(CHANGE,1)}. <em>The last two days earned more than the first five together.</em>"

SHAPE = f"The week started slowly and kept climbing. Your best day was {E(BEST_DAY)} at {M(BEST_NET)}, which is {PCT(BEST_SHARE,1)} of the whole week, and the day before it was the second best. {N(BUYERS)} people bought from you, and the typical purchase held steady at {M(MED)}."

SHAPE2 = f"Most of your money came from messages, with tips adding a little on top. The {BANDS[0]['band']} range earned the most at {M(BANDS[0]['gross'])}" + (f", followed by {BANDS[1]['band']} at {M(BANDS[1]['gross'])}." if len(BANDS) > 1 else ".") + f" You also had {N(NEWSUBS)} new subscribers and {N(REBILLS)} renewals this week."

NOTES = {
    FANS[0]["id"]: ("New this month, top of the week", f"{E(FANS[0]['name'])} joined under a month ago and spent {M(FANS[0]['net_w'])} this week, with a top purchase of {M(FANS[0]['max_ticket'])}."),
    FANS[1]["id"]: ("Two years in, still buying", f"{E(FANS[1]['name'])} has been around for two years and spent {M(FANS[1]['net_w'])} with you this week."),
    FANS[2]["id"]: ("Five years with you", f"{E(FANS[2]['name'])} has supported you for five years and added {M(FANS[2]['net_w'])} this week, with a top purchase of {M(FANS[2]['max_ticket'])}."),
}

MOVES = [
    ("Today", "Thank the newest top fan", f"We send {E(FANS[0]['name'])} a personal thank you after their {M(FANS[0]['net_w'])} first big week, so that early energy keeps going."),
    ("This week", "Start the week stronger", f"Monday and Tuesday were the quietest days, so we put a warm, personal offer early in the week to lift the floor before the weekend."),
    ("All week", "Look after the regulars", f"We keep personal conversations going with the fans who have been with you for years, like {E(FANS[2]['name'])}, so they feel seen."),
]

GOOD30 = f"In 30 days, good looks like weeks that hold above {M(NET)}, early-week days that do not dip as low, and more than {N(BUYERS)} people buying each week, so the total rests on a wider group."

PENDING = [("On ours", "Your weekly invoice", "It lands today alongside this report, based on platform-reported figures.")]

CLOSE = f"You finished the week at {M(NET)}, up {PCT(CHANGE,1)}. <em>The weekend showed how much more the week can hold.</em>"

WEEK_HEAD = f"A week that built <em>to {M(BEST_NET)}</em>"

KN = [
    ("Your newest top fan", f"{E(FANS[0]['name'])} found you under a month ago and already led the week at {M(FANS[0]['net_w'])}."),
    ("A long-time favourite", f"{E(FANS[1]['name'])} has been with you for two years and spent {M(FANS[1]['net_w'])} this week."),
    ("Your longest supporter", f"{E(FANS[2]['name'])} has been with you for five years and bought again this week for {M(FANS[2]['net_w'])}."),
]

WARN_FANS = ("A few fans carry a lot", f"Your top ten fans brought in about 60 percent of the week, out of {N(BUYERS)} buyers in total.", "Widening that group, even a little, makes each week steadier and less dependent on any one person.")

STORY_X = [f"{E(FANS[2]['name'])} has been with you for five years, and this week they came back to spend {M(FANS[2]['net_w'])}, with a top purchase of {M(FANS[2]['max_ticket'])}.", "That kind of loyalty is rare, and it says a lot about the connection you have built over time."]