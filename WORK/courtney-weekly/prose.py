HOOK = [["Two days in,", f"{M(NET)} already"], [f"{N(BUYERS)} people bought,", "three led the way"]]

LEAD_1 = f"Your first two days with us brought in {M(NET)} from {N(BUYERS)} buyers, and every dollar came through your messages. <em>{E(FANS[0]['name'])} alone spent {M(FANS[0]['net_w'])} across {N(FANS[0]['n_sessions'])} visits.</em>"

SHAPE = f"There is no earlier week to compare against yet, so this is your starting line. {BEST_DAY} was the strongest day at {M(BEST_NET)}, which is {PCT(BEST_SHARE,1)} of the total, and the next day held up with {M(NET - BEST_NET)}."

SHAPE2 = f"The typical purchase was {M(MED)}, but the top three buyers each went up to {M(FANS[2]['max_ticket'])} or more in one go. Of the 48 personal messages with a price on them, {PCT(83.3,1)} were unlocked, and sets from {M(40)} to {M(69)} sold every time."

NOTES = {
    FANS[0]["id"]: ("Came back four times in two days", f"{E(FANS[0]['name'])} spent {M(FANS[0]['net_w'])} with a top single buy of {M(FANS[0]['max_ticket'])}."),
    FANS[1]["id"]: ("One visit, one big moment", f"{E(FANS[1]['name'])} spent {M(FANS[1]['net_w'])} in a single visit, topping out at {M(FANS[1]['max_ticket'])}."),
    FANS[2]["id"]: ("Bought at the same high level", f"{E(FANS[2]['name'])} spent {M(FANS[2]['net_w'])} in one visit, with a best buy of {M(FANS[2]['max_ticket'])}."),
}

MOVES = [
    ("Today", "Thank the top three", f"{E(FANS[0]['name'])}, {E(FANS[1]['name'])} and {E(FANS[2]['name'])} spent {M(FANS[0]['net_w'] + FANS[1]['net_w'] + FANS[2]['net_w'])} between them, so each gets a personal thank you with no price attached."),
    ("This week", "Lean on the middle", f"Sets priced {M(40)} to {M(69)} unlocked every time, so more of the week's new content goes out at that level."),
    ("All week", "Turn views into visits", f"Your best reel reached 27,058 views, and we will point that attention toward your page with a clear link in every caption."),
]

GOOD30 = f"In 30 days, good looks like a steady daily floor rather than one big night, at least 15 regular buyers instead of {N(BUYERS)}, and the first new subscribers arriving from your 303,265 Instagram followers. If your first two days are anything to go by, {M(NET)} a week is the floor, not the ceiling."

PENDING = [
    ("On ours", "A full week to compare", "Next week's report sets seven full days against these two, so your trend line starts there."),
    ("On your side", "Fresh sets land well", f"New content goes straight to the {N(BUYERS)} people already buying, which is where this week's {M(NET)} came from."),
]

CLOSE = f"Two days, {N(BUYERS)} buyers and {M(NET)} in. <em>This is the start, and it is a strong one.</em>"

WEEK_HEAD = f"Two days in, <em>{M(NET)} earned</em>"

KN = [
    ("Your top buyer", f"{E(FANS[0]['name'])} came back {N(FANS[0]['n_sessions'])} times and spent {M(FANS[0]['net_w'])}, nearly half the week on their own."),
    ("Where it came from", f"All {M(NET)} came through your messages, with {PCT(83.3,1)} of priced messages unlocked."),
    ("Your reach", f"Instagram brought 35,007 views from 4 posts, and one reel carried 27,058 of them."),
]

WARN_FANS = (
    "Three people, most of the week",
    f"{E(FANS[0]['name'])}, {E(FANS[1]['name'])} and {E(FANS[2]['name'])} made up {PCT(100 * (FANS[0]['net_w'] + FANS[1]['net_w'] + FANS[2]['net_w']) / NET, 1)} of your {M(NET)}.",
    f"Keeping those three close while we grow past {N(BUYERS)} buyers is the main goal for next week.",
)

STORY_X = [
    f"{E(FANS[0]['name'])} found you this week and came back {N(FANS[0]['n_sessions'])} times in two days, spending {M(FANS[0]['net_w'])} with a best single buy of {M(FANS[0]['max_ticket'])}.",
    f"Their last purchase was only hours ago, so they are still close and still enjoying what you share.",
]