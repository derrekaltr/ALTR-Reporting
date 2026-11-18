HOOK = [["A steadier week,", "a bigger ticket"], ["Median buy rose", "from $12 to $20"]]

LEAD_1 = f"You made {M(NET)} this week, {PCT(abs(CHANGE),1)} under last week's {M(PREV)}. <em>Your median purchase climbed to {M(MED)}, so each of your {N(BUYERS)} buyers spent more.</em>"

SHAPE = f"The week started quietly at about $40 a day, then lifted from Saturday. {BEST_DAY} was your best day at {M(BEST_NET)}, {PCT(BEST_SHARE,1)} of the week, and the last three days all stayed above $80."

SHAPE2 = f"Price worked in your favour. Messages priced $40 to $69 sold at 30.8%, against 5.9% for anything under $20. Your audience is telling us the middle of the range is where they buy."

NOTES = {
    FANS[0]["id"]: ("One big buy, very recent", f"{E(FANS[0]['name'])} spent {M(FANS[0]['net_w'])} in a single sitting, on a {M(FANS[0]['max_ticket'])} purchase."),
    FANS[1]["id"]: ("Came back twice this week", f"{E(FANS[1]['name'])} bought across {N(FANS[1]['n_sessions'])} visits for {M(FANS[1]['net_w'])}, with a top buy of {M(FANS[1]['max_ticket'])}."),
    FANS[2]["id"]: ("Six years with you", f"{E(FANS[2]['name'])} added {M(FANS[2]['net_w'])} this week, on top of $1,248 across six years subscribed."),
}

MOVES = [
    ("Today", "Follow up with Wulfas", f"Their {M(FANS[0]['max_ticket'])} purchase is less than a day old, so we reach out while it is fresh."),
    ("This week", "Lead with $40 to $69", "That range sold at 30.8% this week, so we build the week's offers around it."),
    ("All week", "Lift the quiet days", f"Thursday and Friday sat near $40 each; matching {BEST_DAY} pacing on those days closes the gap to {M(PREV)}."),
]

GOOD30 = f"In 30 days, good looks like weekly net back above {M(PREV)}, a median purchase holding at {M(MED)} or higher, and more than {N(BUYERS)} buyers each week so the top ten carry less than 61.7%."

PENDING = [
    ("On ours", "Weekly invoice", "This week's invoice arrives alongside this report, based on platform-reported figures."),
]

CLOSE = f"{M(NET)} this week and a median buy of {M(MED)}. <em>Bigger purchases are the base we build on next.</em>"

WEEK_HEAD = f"A {M(NET)} week, <em>{N(BUYERS)} buyers strong</em>"

KN = [
    ("New subscribers", f"{N(NEWSUBS)} people joined this week and {N(REBILLS)} renewed, bringing in $256 from subscriptions."),
    ("Best day", f"{BEST_DAY} brought in {M(BEST_NET)}, the strongest day of the week by a clear margin."),
    ("Where it came from", "Messages earned $413 of the week, subscriptions $256 and tips $120."),
]

WARN_FANS = (
    "A few names carry it",
    "Your top ten buyers made up 61.7% of the week's net, so a handful of people set the pace.",
    f"Growing past {N(BUYERS)} buyers spreads that out and keeps quiet weeks steady.",
)

STORY_X = [
    f"{E(FANS[2]['name'])} has been subscribed for six years and has spent $1,248 with you in that time.",
    f"This week they came back for a {M(FANS[2]['max_ticket'])} purchase, a sign of how loyal your longest subscribers stay.",
]