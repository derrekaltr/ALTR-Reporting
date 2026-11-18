HOOK = [["A week that kept", "climbing to the end"], ["Your biggest night", "came on the last day"]]

LEAD_1 = f"You made {M(NET)} this week from {N(BUYERS)} buyers, with a typical purchase of {M(MED)}. <em>Your best night was the last one, {M(BEST_NET)} on {BEST_DAY}.</em>"

SHAPE = f"The week built day by day, from {M(329)} on the first day to {M(BEST_NET)} on {BEST_DAY}. That last night alone brought in {PCT(BEST_SHARE,1)} of the week, and every day after the first three cleared {M(1900)}."

SHAPE2 = f"Almost all of it came through private messages, {M(14212)} of {M(NET)}, with {M(186)} more in tips. Your strongest price range was {BANDS[0]['band']}" + (f", followed by {BANDS[1]['band']}." if len(BANDS) > 1 else ".") + f" Of the 588 personal offers sent, 31.1% were bought."

NOTES = {
    FANS[0]["id"]: ("Your top spender this week", f"{E(FANS[0]['name'])} spent {M(FANS[0]['net_w'])} across {N(FANS[0]['n_sessions'])} visits, with single buys up to {M(FANS[0]['max_ticket'])}."),
    FANS[1]["id"]: ("A big night in one visit", f"{E(FANS[1]['name'])} spent {M(FANS[1]['net_w'])} in a single visit, topping out at {M(FANS[1]['max_ticket'])}."),
    FANS[2]["id"]: ("Five years with you", f"{E(FANS[2]['name'])} added {M(FANS[2]['net_w'])} this week, with a best single buy of {M(FANS[2]['max_ticket'])}."),
}

MOVES = [
    ("Today", "A thank you to the top", f"We send a warm personal note to {E(FANS[0]['name'])} and {E(FANS[1]['name'])}, who together brought in {M(FANS[0]['net_w'] + FANS[1]['net_w'])} this week."),
    ("This week", "Build on the late nights", f"The last four days averaged over {M(3000)} a day, so we keep the evening rhythm that got you to {M(BEST_NET)} on {BEST_DAY}."),
    ("All week", "Lead with your best range", f"We keep offers centred on {BANDS[0]['band']}, where your buyers responded best this week."),
]

GOOD30 = f"Good in 30 days looks like this week's pace holding across the month. That means around {M(NET)} a week, more than {N(BUYERS)} buyers each week, and your longtime regulars spending as steadily as the new top names."

PENDING = [
    ("On ours", "This week's invoice", f"Your invoice for the week lands today alongside this report, based on the {M(NET)} shown here."),
    ("On your side", "Fresh sets help most", f"Your top buyers went straight for offers up to {M(200)}, so anything new you film gives us more to share with them."),
]

CLOSE = f"{N(BUYERS)} people bought from you this week, and the week finished at its peak. <em>You closed with {M(BEST_NET)} in one night.</em>"

WEEK_HEAD = f"{M(NET)} this week, <em>best night last</em>"

KN = [
    ("Vroom!", f"Six years with you and {M(14051)} lifetime, plus {M(572)} more this week across 4 visits."),
    ("Carl", f"Five years with you and {M(1032)} lifetime, with {M(788)} of it spent this week."),
    ("As Ff", f"Came back 3 times this week for {M(459)}, with single buys up to {M(200)}."),
]

WARN_FANS = (
    "Your top ten carried the week",
    f"Ten buyers brought in 62.8% of your {M(NET)}, led by {E(FANS[0]['name'])} at {M(FANS[0]['net_w'])}.",
    f"Your other {N(BUYERS - 10)} buyers are where the next step up comes from, and we are giving them more of our attention.",
)

STORY_X = [
    f"{E(FANS[0]['name'])} was your biggest buyer this week, spending {M(FANS[0]['net_w'])} over {N(FANS[0]['n_sessions'])} visits.",
    f"Their largest single buy was {M(FANS[0]['max_ticket'])}, and they bought again within the last day.",
]