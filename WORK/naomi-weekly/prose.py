HOOK = [["A quieter week", "one big Friday"], ["Three new names", "worth knowing"]]

LEAD_1 = f"You made {M(NET)} this week, down {PCT(abs(CHANGE),1)} from {M(PREV)}. <em>{E(BEST_DAY)} alone brought in {M(BEST_NET)}, so the demand is there.</em>"

SHAPE = f"Most of the week sat low, and then one evening carried it: {E(BEST_DAY)} made {M(BEST_NET)}, or {PCT(BEST_SHARE,1)} of the total. {N(BUYERS)} people bought something, with a typical purchase of {M(MED)}."

SHAPE2 = f"Your best price range was {E(BANDS[0]['band'])} at {M(BANDS[0]['gross'])}{(', followed by ' + E(BANDS[1]['band']) + ' at ' + M(BANDS[1]['gross'])) if len(BANDS) > 1 else ''}. Fans paid well when the offer felt worth it, which tells us the next step is more good evenings, not lower prices."

NOTES = {
    FANS[0]["id"]: (f"New, {M(FANS[0]['net_w'])} in one night", f"{E(FANS[0]['name'])} found you this week and spent {M(FANS[0]['net_w'])} in a single evening, topping out at {M(FANS[0]['max_ticket'])}."),
    FANS[1]["id"]: (f"{N(FANS[1]['n_sessions'])} visits, up to {M(FANS[1]['max_ticket'])}", f"{E(FANS[1]['name'])} keeps coming back, with {M(FANS[1]['net_w'])} this week across {N(FANS[1]['n_sessions'])} visits."),
    FANS[2]["id"]: (f"One buy at {M(FANS[2]['max_ticket'])}", f"{E(FANS[2]['name'])} spent {M(FANS[2]['net_w'])} this week and is worth a warm hello to bring back."),
}

MOVES = [
    ("Today", "Thank your top three", f"A personal note to {E(FANS[0]['name'])}, {E(FANS[1]['name'])} and {E(FANS[2]['name'])}, who gave {M(FANS[0]['net_w'] + FANS[1]['net_w'] + FANS[2]['net_w'])} between them."),
    ("This week", "Two more big nights", f"We plan two evenings built like {E(BEST_DAY)}, which made {M(BEST_NET)} on its own."),
    ("All week", "Welcome the new faces", f"{N(NEWSUBS)} new fans joined and {N(REBILLS)} renewed, and each one gets a real hello in their first days."),
]

GOOD30 = f"In 30 days, good looks like three or four evenings like {E(BEST_DAY)} every week, so a quieter week still lands well above {M(NET)}, and {E(FANS[1]['name'])} stays among your regulars."

PENDING = [
    ("On ours", "Weekly invoice", "Your invoice for the week lands today alongside this report."),
    ("On your side", "Fresh sets", "Any new photos or short clips you shoot this week go straight into the plan for your big evenings."),
]

CLOSE = f"This week was {M(NET)}, softer than {M(PREV)}, but one evening made {M(BEST_NET)}. <em>We build the next week around that night.</em>"

WEEK_HEAD = f"{M(NET)} this week, <em>{E(BEST_DAY)} led the way</em>"

KN = [
    (E(FANS[0]["name"]), f"Brand new and spent {M(FANS[0]['net_w'])} in one night, topping out at {M(FANS[0]['max_ticket'])}."),
    (E(FANS[1]["name"]), f"Spent {M(FANS[1]['net_w'])} this week across {N(FANS[1]['n_sessions'])} visits, a regular in the making."),
    (E(FANS[2]["name"]), f"Spent {M(FANS[2]['net_w'])} with a single buy of {M(FANS[2]['max_ticket'])}, worth a warm hello."),
]

WARN_FANS = (
    "Worth a hello",
    f"{E(FANS[2]['name'])} spent {M(FANS[2]['net_w'])} this week, and a warm note keeps them close.",
    f"Your top three gave {M(FANS[0]['net_w'] + FANS[1]['net_w'] + FANS[2]['net_w'])} between them, so each one hears from you this week.",
)

STORY_X = [
    f"{E(FANS[0]['name'])} arrived this week and spent {M(FANS[0]['net_w'])} in one evening, the biggest single night from anyone.",
    f"Their top purchase was {M(FANS[0]['max_ticket'])}, which shows how far a new fan will go when the moment feels personal.",
]