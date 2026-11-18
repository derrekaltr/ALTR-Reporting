HOOK = [["A softer week", "with bigger sales"], ["Your typical sale", "more than doubled"]]

LEAD_1 = f"This week brought in {M(NET)}, down {PCT(abs(CHANGE),1)} on last week's {M(PREV)}. <em>Your median sale rose to {M(MED)} from about {M(18)}, so the people buying are spending more each time.</em>"

SHAPE = f"{BEST_DAY} led the week at {M(BEST_NET)}, {PCT(BEST_SHARE,1)} of everything you made. The week opened at {M(376)} and Sunday was the quietest day at {M(861)}. Monday came back strong at {M(3438)}, so the week finished on a high."

SHAPE2 = f"Paid messages brought in {M(18552)} and tips added {M(1042)}. {N(BUYERS)} people bought from you, and your top ten made up 55.6% of the week. Your best price range was {BANDS[0]['band']} at {M(BANDS[0]['gross'])}" + (f", followed by {BANDS[1]['band']} at {M(BANDS[1]['gross'])}." if len(BANDS) > 1 else ".")

NOTES = {
    FANS[0]["id"]: ("Top of the week, still buying", f"{E(FANS[0]['name'])} spent {M(FANS[0]['net_w'])} across {N(FANS[0]['n_sessions'])} nights, with a top sale of {M(FANS[0]['max_ticket'])}."),
    FANS[1]["id"]: ("Two big nights, then quiet", f"{E(FANS[1]['name'])} spent {M(FANS[1]['net_w'])} in {N(FANS[1]['n_sessions'])} nights early in the week, with a top sale of {M(FANS[1]['max_ticket'])}."),
    FANS[2]["id"]: ("The steadiest all week", f"{E(FANS[2]['name'])} came back {N(FANS[2]['n_sessions'])} times for {M(FANS[2]['net_w'])}, with a top sale of {M(FANS[2]['max_ticket'])}."),
}

MOVES = [
    ("Today", "Warm up the quiet two", f"Dan and CurlyMullet both last bought five days ago, after spending {M(1600)} and {M(924)} this week, so they hear from you first."),
    ("This week", "Lead with the top range", f"Your {BANDS[0]['band']} sets earned the most at {M(BANDS[0]['gross'])}, so the new sets go out at that level first."),
    ("All week", "Lift the quiet days", f"Sunday made {M(861)} against {M(BEST_NET)} on your best day, so we plan the strongest sets for the slow evenings."),
]

GOOD30 = f"Thirty days from now, good looks like weeks back near {M(PREV)} while your median sale holds close to {M(MED)}. It also looks like more than {N(BUYERS)} people buying each week, so the total rests on a wider group than your top ten."

PENDING = [
    ("On ours", "Quiet-day plan", f"We are lining up the slow evenings around your best day of {M(BEST_NET)}, so Sundays stop dipping to {M(861)}."),
    ("On your side", "New sets ready", "Anything fresh you shoot this week goes straight into the top price range, where your sales landed most."),
]

CLOSE = f"{N(BUYERS)} people bought from you this week and your median sale reached {M(MED)}. <em>The spending is there, and getting a few more of them back is the whole opportunity.</em>"

WEEK_HEAD = f"A quieter week, <em>bigger sales</em>"

KN = [
    ("The total", f"You made {M(NET)} this week, down {PCT(abs(CHANGE),1)} from {M(PREV)}."),
    ("The typical sale", f"Your median sale was {M(MED)}, up from about {M(18)} last week."),
    ("The best day", f"{BEST_DAY} brought in {M(BEST_NET)}, the strongest day of the week."),
]

WARN_FANS = (
    "Two who went quiet",
    f"Dan spent {M(1600)} this week and CurlyMullet spent {M(924)}, and both last bought about five days ago.",
    "Both have been with you for four years or more, so a warm hello usually brings them back.",
)

STORY_X = [
    f"{E(FANS[0]['name'])} has been with you for six years and was your biggest spender this week at {M(FANS[0]['net_w'])}.",
    f"They bought across {N(FANS[0]['n_sessions'])} nights, their top sale was {M(FANS[0]['max_ticket'])}, and their last one was only half a day ago.",
]