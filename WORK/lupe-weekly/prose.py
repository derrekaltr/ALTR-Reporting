HOOK = [["A week that more","than tripled the last"],["Higher prices,","and more of them sold"]]

LEAD_1 = f"You made {M(NET)} this week, up from {M(PREV)} the week before. That is {PCT(CHANGE,1)} more, <em>and the typical purchase rose from $20 to {M(MED)}</em>."

SHAPE = f"{N(BUYERS)} people bought from you this week, and {E(FANS[0]['name'])} accounted for {M(FANS[0]['net_w'])} of the {M(NET)}. Your best day was {E(BEST_DAY)} at {M(BEST_NET)}, and only one day came in under $400."

SHAPE2 = f"Almost all of it came through personal messages, {M(DM)} of the week. Your best seller was the {E(BANDS[0]['band'])} range at {M(BANDS[0]['gross'])}" + (f", followed by {E(BANDS[1]['band'])} at {M(BANDS[1]['gross'])}." if len(BANDS) > 1 else ".") + " Offers at $150 and up were bought 79% of the time, against 29% for those under $20."

NOTES = {
    FANS[0]["id"]: (f"{N(FANS[0]['n_sessions'])} visits, top {M(FANS[0]['max_ticket'])}", f"{E(FANS[0]['name'])} spent {M(FANS[0]['net_w'])} with you this week and bought again within the last day."),
    FANS[1]["id"]: (f"Five years, {M(FANS[1]['net_w'])} this week", f"{E(FANS[1]['name'])} has been with you five years and spent {M(FANS[1]['net_w'])} across {N(FANS[1]['n_sessions'])} visits this week."),
    FANS[2]["id"]: (f"One visit, {M(FANS[2]['net_w'])}", f"{E(FANS[2]['name'])} came by once this week and spent {M(FANS[2]['net_w'])}, with a top purchase of {M(FANS[2]['max_ticket'])}."),
}

MOVES = [
    ("Today", "Thank your top three", f"A personal note to {E(FANS[0]['name'])}, {E(FANS[1]['name'])} and {E(FANS[2]['name'])}, who together spent {M(FANS[0]['net_w'] + FANS[1]['net_w'] + FANS[2]['net_w'])} this week."),
    ("This week", "Keep the higher price", f"Offers at $150 and up sold 79% of the time, so we keep the {E(BANDS[0]['band'])} range at the centre of the week."),
    ("All week", "Spread the attention", f"One buyer carried most of the {M(NET)}, so we keep long-time fans close and bring a few more of them into the top ten."),
]

GOOD30 = f"In 30 days, a good result is four weeks near {M(NET)}, a typical purchase holding close to {M(MED)}, and more of the week coming from fans beyond the top three."

PENDING = [
    ("On ours", "This week's invoice", f"Your invoice for the week lands today, based on the {M(NET)} in this report."),
    ("On your side", "Fresh sets", "Anything new you shoot this week goes to your longest fans first, while the higher price is working."),
]

CLOSE = f"{M(NET)} in seven days, {PCT(CHANGE,1)} above last week, <em>with your fans paying more and saying yes more often</em>."

WEEK_HEAD = f"Up from {M(PREV)}, <em>now {M(NET)}</em>"

KN = [
    (E(FANS[0]["name"]), f"Ten months with you and {M(FANS[0]['net_w'])} this week over {N(FANS[0]['n_sessions'])} visits, the biggest week of anyone on your page."),
    (E(FANS[1]["name"]), f"Five years with you and over $58,000 in lifetime spend, adding {M(FANS[1]['net_w'])} this week."),
    (E(FANS[2]["name"]), f"Another five-year fan, who spent {M(FANS[2]['net_w'])} in a single visit this week."),
]

WARN_FANS = (
    "Two long-time fans, quiet",
    f"{E(FANS[1]['name'])} and {E(FANS[2]['name'])} both bought about four days ago and have not been back since.",
    "Both have been with you for five years, so a warm hello this week keeps them close.",
)

STORY_X = [
    f"{E(FANS[0]['name'])} has spent over $63,000 with you in ten months, and {M(FANS[0]['net_w'])} of that came this week.",
    f"Their biggest single purchase was {M(FANS[0]['max_ticket'])}, and they came back {N(FANS[0]['n_sessions'])} times in seven days.",
]