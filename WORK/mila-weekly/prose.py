HOOK = [["A softer week,", f"{M(NET)} net"], ["Bigger tickets,", "fewer of them"]]

LEAD_1 = f"You made {M(NET)} this week, down {PCT(abs(CHANGE),1)} from {M(PREV)}. <em>Your median ticket rose to {M(MED)}, so the fans who bought spent more each time.</em>"

SHAPE = f"All of it came through your messages, from {N(BUYERS)} buyers. Your best day was {BEST_DAY} at {M(BEST_NET)}, {PCT(BEST_SHARE,1)} of the week on its own."

SHAPE2 = f"The {BANDS[0]['band']} range did the most work, {M(BANDS[0]['gross'])} of the week." + (f" Next came {BANDS[1]['band']} at {M(BANDS[1]['gross'])}." if len(BANDS) > 1 else "") + " Fans are saying yes at higher prices, and that is a good base to build on."

NOTES = {
    FANS[0]["id"]: ("Top of the week, one evening", f"{E(FANS[0]['name'])} spent {M(FANS[0]['net_w'])} this week, with a top unlock of {M(FANS[0]['max_ticket'])}."),
    FANS[1]["id"]: ("New name near the top", f"{E(FANS[1]['name'])} added {M(FANS[1]['net_w'])}, with their biggest single buy at {M(FANS[1]['max_ticket'])}."),
    FANS[2]["id"]: ("With you a year, $1,205 lifetime", f"{E(FANS[2]['name'])} came back {N(FANS[2]['n_sessions'])} times for {M(FANS[2]['net_w'])}, topping out at {M(FANS[2]['max_ticket'])}."),
}

MOVES = [
    ("Today", "Thank the top three", f"We open warm, personal threads with {E(FANS[0]['name'])}, {E(FANS[1]['name'])} and {E(FANS[2]['name'])}, with nothing for sale in the first message."),
    ("This week", "Lead with the best range", f"We build more offers in the {BANDS[0]['band']} range, since that is where your fans spent the most this week."),
    ("All week", "Widen the circle", f"We reach past this week's {N(BUYERS)} buyers to the quieter fans on your list, one real conversation at a time."),
]

GOOD30 = f"In 30 days, good looks like weekly net back above {M(PREV)}, the median ticket holding near {M(MED)}, and more than {N(BUYERS)} buyers in a week."

PENDING = [("On ours", "This week's invoice", "Your invoice lands with this report. It uses platform-reported figures, and the final split follows the usual record.")]

CLOSE = f"Fewer buyers, bigger tickets, and a year-long fan still coming back. <em>{M(NET)} this week, with clear room to grow from here.</em>"

WEEK_HEAD = f"Your week in review, <em>{M(NET)} net</em>"

KN = [
    (E(FANS[0]["name"]), f"Your top spender this week at {M(FANS[0]['net_w'])}, with one buy at {M(FANS[0]['max_ticket'])}."),
    (E(FANS[1]["name"]), f"Spent {M(FANS[1]['net_w'])} this week and is new to the top of your list."),
    (E(FANS[2]["name"]), f"With you for a year and $1,205 lifetime, they bought {N(FANS[2]['n_sessions'])} times this week."),
]

WARN_FANS = ("A small circle, room to grow", f"This week {N(BUYERS)} buyers made up the whole {M(NET)}.", "Every new buyer we bring in from your list moves the total quickly, so that is where our focus goes next week.")

STORY_X = [
    f"{E(FANS[2]['name'])} has been with you for a year and has spent $1,205 in that time.",
    f"This week they came back {N(FANS[2]['n_sessions'])} times, and their biggest buy was {M(FANS[2]['max_ticket'])}.",
]