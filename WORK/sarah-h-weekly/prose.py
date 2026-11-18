HOOK = [["A quiet week", "on the page"], ["Next week starts", "from a clean slate"]]

LEAD_1 = f"The platform reported {M(NET)} for this week, against {M(PREV)} the week before, <em>so the next seven days are a fresh start.</em>"

SHAPE = f"There were {N(BUYERS)} buyers this week and no single day stood out, so there is no pattern to read yet. This week becomes the baseline we measure the next one against."

SHAPE2 = f"{N(NEWSUBS)} new subscribers and {N(REBILLS)} renewals came through, with {N(VIS)} profile visits on record. The first steady days of posting will show up clearly against this."

NOTES = {f["id"]: (f"{M(f['net_w'])} this week", f"Top purchase of {M(f['max_ticket'])} across {N(f['n_sessions'])} visits.") for f in FANS[:3]}

MOVES = [
    ("Today", "Fresh posts on the page", f"We open the week with new posts so the {N(VIS)} visitors from last week find something new when they come back."),
    ("This week", "A warm welcome", f"Every new subscriber gets a personal hello, building on the {N(NEWSUBS)} who joined last week."),
    ("All week", "Steady, every evening", f"We keep a steady rhythm each evening so the week can move past last week's {M(NET)}."),
]

GOOD30 = f"In 30 days, good looks like four steady weeks in a row, each above this week's {M(NET)}, with buyers coming back on more than one night."

PENDING = [
    ("On ours", "Checking the numbers", f"A week reading {M(NET)} across the board is unusual, so we are confirming the account connection and will share anything we find."),
]

CLOSE = f"This week closed at {M(NET)}. <em>Every week from here builds on it.</em>"

WEEK_HEAD = f"A quiet week, <em>a clean slate</em>"

KN = [
    ("Earnings", f"The platform reported {M(NET)} this week, against {M(PREV)} the week before."),
    ("Buyers", f"There were {N(BUYERS)} buyers this week, so the first purchase next week sets the new pace."),
    ("New faces", f"{N(NEWSUBS)} new subscribers joined, and everyone who arrives next week gets a warm welcome."),
]

WARN_FANS = (
    "No one slipping away",
    f"With {N(BUYERS)} buyers on record this week, there is no one to flag as going quiet.",
    "We start watching for that again as soon as the first buyers return.",
)

STORY_X = [
    "No single person shaped this week, so there is no spender story to tell yet.",
    f"The first person to spend next week is the one we follow here, measured against this week's {M(NET)}.",
]