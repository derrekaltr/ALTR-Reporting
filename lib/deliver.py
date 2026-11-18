# -*- coding: utf-8 -*-
"""Deliver finished report PDFs to the ALTR Google Drive folder (via rclone remote "gdrive").

Structure:  ALTR Reports/<Model Name>/<Model Name> - @ofusername - <date>.pdf

    python3 ../../lib/deliver.py             from inside a WORK/<slug>/ folder: upload its PDF
    python3 lib/deliver.py sync              ensure a subfolder exists for every connected OF account
    python3 lib/deliver.py link              print the shareable link for the top folder

`sync` reads the live OnlyFans account list, so a newly connected creator gets her folder
automatically; deploy.sh runs a deliver after every publish, and each deliver also runs sync.
"""
import json, os, re, subprocess, sys
from pathlib import Path

LIB = Path(__file__).resolve().parent
sys.path.insert(0, str(LIB))
# Pinned to the ALTR Reports folder by ID, so moving/renaming it in Drive cannot break delivery.
# (The folder now lives at ALTR Management/04 Reporting & Analytics/ALTR Reports.)
ROOT_REMOTE = "gdrive-reports:"

def rc(*args, timeout=180):
    return subprocess.run(["rclone", *args], capture_output=True, text=True, timeout=timeout)

def accounts():
    from ofapi import accounts as of_accounts
    return [a for a in of_accounts() if a.get("is_authenticated") or a.get("authenticated")]

def folder_name(display, username):
    name = re.sub(r'[\\/:*?"<>|]', "", (display or username or "unknown")).strip()
    return name or username

def sync():
    """Create a Drive folder for every model we actually report on.

    This used to loop over all connected OnlyFans accounts and name folders from the OnlyFans
    display name, while deliver() files reports under the roster name. Any difference between the
    two left an empty orphan folder that looked like a missing report ("Amber" vs "Amber
    Rodriguez"), and accounts that were connected but never rostered got empty folders too.
    Driving this from the roster keeps the folder list exactly equal to the reports we produce.
    """
    roster = LIB / "roster.txt"
    made = []
    for line in roster.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        name = line.split("|")[2]
        r = rc("mkdir", f"{ROOT_REMOTE}{name}")
        if r.returncode == 0:
            made.append(name)
        else:
            print(f"  !! mkdir {name}: {r.stderr.strip()[:120]}", file=sys.stderr)
    print(f"synced {len(made)} model folders under '{ROOT_REMOTE}'")

def _sync_from_accounts_unused():
    made = []
    for a in accounts():
        f = folder_name(a.get("display_name") or a.get("name"), a.get("onlyfans_username") or a.get("username"))
        r = rc("mkdir", f"{ROOT_REMOTE}{f}")
        if r.returncode == 0:
            made.append(f)
        else:
            print(f"  !! mkdir {f}: {r.stderr.strip()[:120]}", file=sys.stderr)
    print(f"synced {len(made)} model folders under '{ROOT_REMOTE}'")

def deliver(folder="."):
    folder = Path(folder).resolve()
    meta = json.loads((folder / "report.json").read_text())
    src = folder / meta["pdf"]
    if not src.exists():
        sys.exit(f"{src} not found; build first")
    b = (folder / "build_premium.py").read_text()
    name = re.search(r'NAME = "([^"]+)"', b).group(1)
    handle = re.search(r'HANDLE = "([^"]+)"', b).group(1)
    date = re.search(r'DATE = "([^"]+)"', b).group(1).replace(",", "")
    dest = f"{ROOT_REMOTE}{folder_name(name, handle)}/{name} - {handle} - {date}.pdf"
    sync()
    r = rc("copyto", str(src), dest, timeout=600)
    if r.returncode != 0:
        sys.exit(f"upload failed: {r.stderr.strip()[:300]}")
    print(f"uploaded -> {dest}")

def link():
    r = rc("link", ROOT_REMOTE)
    print(r.stdout.strip() or r.stderr.strip())

if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "."
    if arg == "sync": sync()
    elif arg == "link": link()
    else: deliver(arg)
