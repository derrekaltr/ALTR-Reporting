# -*- coding: utf-8 -*-
"""
ALTR OnlyFans API client. One file, no dependencies beyond the standard library.

    from ofapi import get, raw, walk, rows, save, accounts, BASE, FMT

The key is read from .mcp.json at the kit root (the same file that gives Claude the MCP tools), so there is
exactly one place it lives. The environment variable ONLYFANS_API_KEY overrides it.

Every request sends a custom User-Agent. Cloudflare in front of onlyfansapi.com blocks
Python's default "Python-urllib" agent with error 1010 (a 403 that looks like a bad key).
Retries 429/5xx up to three times. Never raises on an HTTP error; returns
{"_error": code, "_body": text, "_url": url} so a long pull does not die on one bad call.
"""
import json, os, sys, time, datetime as dt, urllib.request, urllib.parse, urllib.error
from pathlib import Path

BASE = "https://app.onlyfansapi.com/api"
UA = "ALTR-Reports/2.0"
FMT = lambda d: d.strftime("%Y-%m-%d %H:%M:%S")          # the format statistics endpoints want
DAY = lambda d: d.strftime("%Y-%m-%d")                   # the format transactions?startDate wants


def kit_root(start=None):
    """Walk up from `start` (default: this file) until a folder containing BRAND-KIT/ is found."""
    p = Path(start or __file__).resolve()
    for q in [p] + list(p.parents):
        if (q / "BRAND-KIT").is_dir():
            return q
    return Path(__file__).resolve().parents[1]


def api_key():
    k = os.environ.get("ONLYFANS_API_KEY")
    if not k:
        mcp = kit_root() / ".mcp.json"
        try:
            k = json.loads(mcp.read_text(encoding="utf-8"))["mcpServers"]["onlyfans"]["headers"]["Authorization"].split()[-1]
        except Exception:
            k = None
    if not k or k.startswith("PASTE"):
        sys.exit("No OnlyFans API key. Run  bash setup.sh  once (it writes .mcp.json), or export ONLYFANS_API_KEY. "
                 "Keys: https://app.onlyfansapi.com/api-keys")
    return k


_KEY = None
def raw(url, timeout=120, tries=4):
    """GET an absolute URL. Returns parsed JSON, or an {_error,...} dict."""
    global _KEY
    if _KEY is None:
        _KEY = api_key()
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + _KEY,
                                               "Accept": "application/json", "User-Agent": UA})
    for a in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "ignore")[:400]
            if e.code in (429, 500, 502, 503, 504) and a < tries - 1:
                time.sleep(2 + 2 * a); continue
            if e.code == 402:
                print("!! 402 insufficient credits. Top up at app.onlyfansapi.com before pulling more.", file=sys.stderr)
            if e.code == 403 and "1010" in body:
                print("!! 403 with Cloudflare 1010: user-agent block, not the key.", file=sys.stderr)
            return {"_error": e.code, "_body": body, "_url": url}
        except Exception as e:
            if a < tries - 1:
                time.sleep(2 + 2 * a); continue
            return {"_error": "exc", "_body": str(e), "_url": url}


def get(path, **params):
    """GET {BASE}/{path}?params. Example: get(f"{acct}/chats", limit=100, order="recent")."""
    p = {k: v for k, v in params.items() if v is not None}
    return raw(f"{BASE}/{path}" + ("?" + urllib.parse.urlencode(p) if p else ""))


def rows(d):
    """Flatten the API's response shapes (list / data:list / data:{list|items|data:list}) to a list."""
    if isinstance(d, list): return d
    if not isinstance(d, dict): return []
    x = d.get("data", d)
    if isinstance(x, list): return x
    if isinstance(x, dict):
        for k in ("list", "items", "data", "users"):
            if isinstance(x.get(k), list): return x[k]
    return []


def walk(url, cap=200, key="id", quiet=False):
    """Follow _pagination.next_page from an absolute URL, de-duplicating by `key`. Returns (items, pages)."""
    out, seen, n = [], set(), 0
    while url and n < cap:
        d = raw(url); n += 1
        if isinstance(d, dict) and "_error" in d:
            print("walk error", d["_error"], str(d.get("_body"))[:160], file=sys.stderr); break
        b = rows(d)
        new = [x for x in b if x.get(key) not in seen]
        for x in new: seen.add(x.get(key))
        out += new
        if not new: break
        url = (d.get("_pagination") or {}).get("next_page") if isinstance(d, dict) else None
        if not quiet and n % 5 == 0:
            print(f"  ...{n} pages, {len(out)} items", file=sys.stderr); sys.stderr.flush()
    return out, n


def save(name, obj, folder="data"):
    """Write data/<name>.json (relative to the current working directory) and print a one-line status."""
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, name + ".json")
    json.dump(obj, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    err = f"  ERROR {obj.get('_error')} {str(obj.get('_body'))[:120]}" if isinstance(obj, dict) and "_error" in obj else ""
    n = len(rows(obj)) if not err else 0
    print(f"saved {path}  ({n} rows){err}"); sys.stdout.flush()
    return obj


def accounts():
    """Connected creator accounts: [{id: acct_..., username, name, authenticated, ...}]."""
    return rows(get("accounts"))


def find_account(q):
    """Resolve 'acct_...', an OF username, or a display name fragment to the account dict."""
    q = (q or "").strip().lstrip("@").lower()
    acc = accounts()
    for a in acc:
        if a.get("id", "").lower() == q: return a
    for a in acc:
        if (a.get("onlyfans_username") or a.get("username") or "").lower() == q: return a
    for a in acc:
        blob = json.dumps(a).lower()
        if q and q in blob: return a
    sys.exit(f"No connected account matches '{q}'. Connected: " +
             ", ".join(f"{a.get('onlyfans_username') or a.get('username')} ({a.get('id')})" for a in acc))


if __name__ == "__main__":
    # python3 lib/ofapi.py              -> list connected accounts
    # python3 lib/ofapi.py <path> k=v   -> ad-hoc GET, e.g. "acct_x/me" or "acct_x/chats" limit=10
    if len(sys.argv) == 1 or sys.argv[1] == "accounts":
        acc = accounts()
        print(f"{len(acc)} connected account(s)")
        for a in acc:
            print(f"  {a.get('id')}  @{a.get('onlyfans_username') or a.get('username')}  "
                  f"{(a.get('display_name') or a.get('name') or '')}  auth={a.get('is_authenticated', a.get('authenticated'))}")
    else:
        kv = dict(x.split("=", 1) for x in sys.argv[2:])
        print(json.dumps(get(sys.argv[1], **kv), indent=1, ensure_ascii=False)[:6000])
