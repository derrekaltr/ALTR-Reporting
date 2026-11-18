HOOK = [["A softer week", "with real depth in it"], ["Three fans carried", "the top of the week"]]

LEAD_1 = f"You made {M(NET)} this week from {N(BUYERS)} buyers, {PCT(abs(CHANGE),1)} under last week's {M(PREV)}. <em>Your best night, {BEST_DAY}, brought in {M(BEST_NET)} on its own.</em>"

SHAPE = f"Every day of the week cleared {M(196)}, so the floor held steady. {BEST_DAY} led at {M(BEST_NET)}, and the week closed strong with {M(575)} on the last day."

SHAPE2 = f"""Most of your money came from purchases in the {BANDS[0]['band']} range, worth {M(BANDS[0]['gross'])}{f', with {BANDS[1]["band"]} next at {M(BANDS[1]["gross"])}' if len(BANDS) > 1 else ''}. The typical purchase was {M(MED)}, a touch under last week's {M(23)}."""

NOTES = {
    FANS[0]["id"]: (f"Five nights, up to {M(FANS[0]['max_ticket'])}", f"{E(FANS[0]['name'])} gave {M(FANS[0]['net_w'])} this week and {M(3775)} in just two months with you."),
    FANS[1]["id"]: ("With you three years, $3,949 total", f"{E(FANS[1]['name'])} came back across {N(FANS[1]['n_sessions'])} nights for {M(FANS[1]['net_w'])}, and bought again on the last day."),
    FANS[2]["id"]: (f"One {M(FANS[2]['max_ticket'])} purchase this week", f"{E(FANS[2]['name'])} spent {M(FANS[2]['net_w'])} in a single night, their first purchase in three months of following you."),
}

MOVES = [
    ("Today", "Thank your top three", f"{E(FANS[0]['name'])}, {E(FANS[1]['name'])} and {E(FANS[2]['name'])} gave {M(FANS[0]['net_w'] + FANS[1]['net_w'] + FANS[2]['net_w'])} between them, so each gets a personal note from us today."),
    ("This week", "Bring back the big night", f"{BEST_DAY} earned {M(BEST_NET)}, so we are building this week around a repeat of that night."),
    ("All week", "Lift the typical purchase", f"The typical purchase slipped from {M(23)} to {M(MED)}, so we are leading with your stronger sets to bring it back up."),
]

GOOD30 = f"In 30 days, good looks like weeks back above {M(PREV)}, more than {N(BUYERS)} buyers each week, and the typical purchase back over {M(23)}."

PENDING = [
    ("On ours", "This week's invoice", f"It lands today with this report, based on platform-reported figures for the {M(NET)} week."),
    ("On ours", "Custom requests", "We are tracking every open custom request so each one is answered on time."),
]

CLOSE = f"Your top three fans gave {M(FANS[0]['net_w'] + FANS[1]['net_w'] + FANS[2]['net_w'])} this week, and two of them bought again on the last day. <em>The people who love your work are still right here.</em>"

WEEK_HEAD = f"Down a little, <em>still {M(NET)}</em>"

KN = [
    ("Your top fan", f"{E(FANS[0]['name'])} gave {M(FANS[0]['net_w'])} over {N(FANS[0]['n_sessions'])} nights, with a best single purchase of {M(FANS[0]['max_ticket'])}."),
    ("Your longest", f"{E(FANS[1]['name'])} has been with you three years and has given {M(3949)} in that time, {M(FANS[1]['net_w'])} of it this week."),
    ("A new name", f"{E(FANS[2]['name'])} made a first purchase of {M(FANS[2]['max_ticket'])} this week after three months of following you."),
]

WARN_FANS = ("Two names to keep warm", "Corne gave $174 over two nights and last bought four days ago.", "Will gave $167 in one night five days ago, so we will check in with both this week.")

STORY_X = [
    f"{E(FANS[0]['name'])} has been with you for two months and has already given {M(3775)}.",
    f"This week they came back on {N(FANS[0]['n_sessions'])} different nights for {M(FANS[0]['net_w'])}, and their latest purchase was on the last day.",
]