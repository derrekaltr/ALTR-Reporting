# -*- coding: utf-8 -*-
"""Upcoming content-calendar moments for creator reports. Returns the next shoot-worthy
holiday within a planning window, with a creator-facing "plan ahead" suggestion.

    from holidays import next_occasion
    occ = next_occasion()   # or next_occasion(dt.date(2026,10,15))
    -> {"name": "Halloween", "date": date(2026,10,31), "days": 16,
        "line": "Halloween is 16 days out. ..."} or None if nothing is close
"""
import datetime as dt

# (month, day, name, theme suggestion). Fixed-date occasions that suit themed shoots.
FIXED = [
    (1, 1,  "New Year",         "fresh-start and lingerie sets"),
    (2, 14, "Valentine's Day",  "a Valentine's set and a few couples-style teases"),
    (3, 17, "St. Patrick's Day","a green themed set"),
    (4, 20, "4/20",             "a laid-back themed set"),
    (5, 5,  "Cinco de Mayo",    "a bright themed set"),
    (7, 4,  "Fourth of July",   "a red-white-and-blue set"),
    (10, 31,"Halloween",        "themed costume sets, the biggest themed earner of the year"),
    (12, 25,"Christmas",        "a festive set and a gift-guide style tease"),
    (12, 31,"New Year's Eve",   "a countdown set"),
]

def _thanksgiving(y):   # 4th Thursday of November
    d = dt.date(y, 11, 1)
    thurs = [dt.date(y, 11, day) for day in range(1, 31) if dt.date(y, 11, day).weekday() == 3]
    return thurs[3]

def next_occasion(today=None, within_days=45, lead_floor=7):
    today = today or dt.date.today()
    cand = []
    for yr in (today.year, today.year + 1):
        for mo, da, name, theme in FIXED:
            try:
                d = dt.date(yr, mo, da)
            except ValueError:
                continue
            cand.append((d, name, theme))
        tg = _thanksgiving(yr)
        cand.append((tg, "Thanksgiving", "a cozy autumn set"))
        cand.append((tg + dt.timedelta(days=1), "Black Friday", "a Black Friday bundle or sale"))
    future = sorted((d, n, t) for d, n, t in cand if 0 <= (d - today).days <= within_days)
    if not future:
        return None
    d, name, theme = future[0]
    days = (d - today).days
    if days <= lead_floor:
        lead = f"{name} is almost here, {days} days out."
        plan = f"Anything you want to post for it should be shot this week."
    else:
        lead = f"{name} is {days} days away."
        plan = f"Now is the moment to plan {theme}, while there is time to shoot and tease it."
    return {"name": name, "date": d, "days": days, "theme": theme, "line": f"{lead} {plan}"}
