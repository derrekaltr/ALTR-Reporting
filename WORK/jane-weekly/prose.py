HOOK = [["A level week,", "a floor that held"], ["Three people", "carried the top"]]

LEAD_1 = f"You made {M(NET)} net this week from {N(BUYERS)} buyers, {'down' if CHANGE < 0 else 'up'} {PCT(abs(CHANGE),1)} on last week's {M(PREV)}. <em>That is almost exactly level, and {N(NEWSUBS)} new people joined while it held.</em>"

SHAPE = f"The best day was {BEST_DAY} at {M(BEST_NET)}, {PCT(BEST_SHARE,1)} of the week on its own. The other days settled between roughly $200 and $650. The middle purchase was {M(MED)}, so most of the money came from steady everyday buying with a few big moments on top."

SHAPE2 = f"The {BANDS[0]['band']} range brought in the most this week at {M(BANDS[0]['gross'])}." + (f" Next came {BANDS[1]['band']} at {M(BANDS[1]['gross'])}." if len(BANDS) > 1 else "") + " Items at $150 and up opened three times in four, so your top tier is ready for your best work."

NOTES = {
    FANS[0]["id"]: ("Biggest week, one sitting", f"{E(FANS[0]['name'])} spent {M(FANS[0]['net_w'])} this week, with a top purchase of {M(FANS[0]['max_ticket'])}."),
    FANS[1]["id"]: ("Bought at the top of the range", f"{E(FANS[1]['name'])} added {M(FANS[1]['net_w'])}, including one purchase of {M(FANS[1]['max_ticket'])}."),
    FANS[2]["id"]: ("New this week, straight to the top", f"{E(FANS[2]['name'])} spent {M(FANS[2]['net_w'])} in their first days, with a {M(FANS[2]['max_ticket'])} top purchase."),
}

MOVES = [
    ("Today", "Welcome the new faces", f"{N(NEWSUBS)} people joined this week, and a warm first hello is where their first purchase starts."),
    ("This week", "Keep the top three close", f"{E(FANS[0]['name'])}, {E(FANS[1]['name'])} and {E(FANS[2]['name'])} brought in {M(FANS[0]['net_w'] + FANS[1]['net_w'] + FANS[2]['net_w'])} between them, so each gets a personal follow-up from us."),
    ("All week", "Lift the quieter days", f"Your best day brought {M(BEST_NET)}. We will pace your premium sets so more days come closer to that."),
]

GOOD30 = f"In 30 days, good looks like weeks above {M(NET*1.1)}, more of this week's {N(NEWSUBS)} new people buying a second time, and your top buyers coming back for more than one sitting."

PENDING = [
    ("On ours", "Your weekly invoice", "It lands today with this report, built on the same platform-reported figures."),
    ("On your side", "Fresh sets for new faces", f"Anything new you shoot this week goes first to the {N(NEWSUBS)} people who just joined."),
]

CLOSE = f"{M(NET)} this week from {N(BUYERS)} buyers, with {N(REBILLS)} renewals behind it. <em>The floor held, and next week we build on it.</em>"

WEEK_HEAD = f"Level with last week, <em>{M(NET)} net</em>"

KN = [
    ("Your top buyer", f"{E(FANS[0]['name'])} spent {M(FANS[0]['net_w'])} this week, your biggest single total."),
    ("Your top tier works", f"{E(FANS[1]['name'])} bought at {M(FANS[1]['max_ticket'])}, proof that your premium pricing lands."),
    ("A brand new regular", f"{E(FANS[2]['name'])} spent {M(FANS[2]['net_w'])} in their first week with you."),
]

WARN_FANS = ("One visit, big spend", f"Your top three bought in {N(FANS[0]['n_sessions'] + FANS[1]['n_sessions'] + FANS[2]['n_sessions'])} sittings between them this week.", "A warm personal note now is how one big visit becomes a habit.")

STORY_X = [
    f"{E(FANS[0]['name'])} spent {M(FANS[0]['net_w'])} with you this week, across {N(FANS[0]['n_sessions'])} sitting and a top purchase of {M(FANS[0]['max_ticket'])}.",
    f"That one visit was close to a fifth of your {M(NET)} week, and it shows how far your best content can go.",
]