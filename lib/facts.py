import json, sys, datetime as dt
from pathlib import Path
slug = sys.argv[1]
d = Path.home() / "Documents/altr-reports-kit/WORK" / slug
R = json.load(open(d / "data/cohort.json"))
S, W, P = R["summary"], R["period"]["window"], R["period"]["previous"]
print(f"net {W['net']:,} prev {P['net']:,} chg {S['change_pct']} | buyers {W['buyers']} med {W['median_ticket']} prevmed {P['median_ticket']}")
print(f"msg {W['msg']:,} tips {W['tips']:,} subs {W['subs']:,} newsubs {W['n_new_subs']} rebills {W['n_rebills']} | top10share {S['top10_share_window']}")
for dd, v in sorted(R["daily"].items())[:7]:
    print(f"  {dd[5:]} {dt.date.fromisoformat(dd).strftime('%a')} {round(v['net']):>6,}")
fans = sorted(R["fans"], key=lambda f: -(f.get("net_w") or 0))
w = W["net"] or 1
print("top5share", round(sum(f["net_w"] for f in fans[:5]) / w * 100, 1))
for f in fans[:6]:
    print(f"  {round(f['net_w']):>6,} {f['name'][:18]:<18} life {round(f.get('life') or 0):>7,} dur {str(f.get('duration')):<9} sess {f.get('n_sessions')} max {f.get('max_ticket')} since {round(f.get('days_since_buy') or -1,1)} sub {f.get('sub_active')}")
print("bands", [(b["band"], b["rate"]) for b in R["dm"]["bands"]])
print(f"dm sent {R['dm']['sent']} rate {R['dm']['rate']} medprice {R['dm']['median_price']} | mass {R['mass']['n']} view {R['mass']['view_rate']}")
try:
    V = json.load(open(d / "data/visitors7.json"))["data"]["topCountries"]["totals"]["total"]
except Exception:
    V = "?"
print("visits", V)
soc = json.load(open(Path.home() / "Documents/altr-telegram/exports/social.json"))["models"]
rl = json.load(open(Path.home() / "Documents/altr-telegram/exports/removelabs.json"))
of = sys.argv[2] if len(sys.argv) > 2 else None
if of:
    sc = soc.get(of)
    print("social:", {k: sc[k] for k in ("views","posts","likes","followers_gained","accounts_total","growth")} if sc else None)
    rlname = next((k for k, v in rl["of_aliases"].items() if v == of), None)
    print("removelabs:", rl["models"].get(rlname, {}).get("total") if rlname else None)
