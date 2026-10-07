#!/usr/bin/env bash
# One-time setup on a Mac. From the kit folder:  bash setup.sh
set -e
cd "$(dirname "$0")"
echo "== ALTR reports kit setup =="

command -v python3 >/dev/null 2>&1 || { echo "python3 is missing. Run:  xcode-select --install   then re-run."; exit 1; }
echo "python3: $(python3 --version)"
[ -e "/Applications/Google Chrome.app" ] || [ -e "$HOME/Applications/Google Chrome.app" ] \
  || { echo "Google Chrome is missing (it renders the PDFs). Install from https://www.google.com/chrome/ then re-run."; exit 1; }
echo "chrome: found"

python3 -m pip install --user -q -r requirements.txt 2>/dev/null \
  || python3 -m pip install --user -q --break-system-packages -r requirements.txt \
  || { echo "pip install failed. Try: python3 -m pip install --user -r requirements.txt"; exit 1; }
echo "python packages: ok"

if [ -f .mcp.json ] && ! grep -q PASTE .mcp.json; then
  echo ".mcp.json already has a key; keeping it."
else
  printf "Paste your OnlyFans API key (https://app.onlyfansapi.com/api-keys, MCP access enabled): "
  read -r KEY; KEY="$(echo "$KEY" | tr -d '[:space:]')"
  [ -n "$KEY" ] || { echo "no key given"; exit 1; }
  python3 - "$KEY" <<'EOF'
import json, sys
m = json.load(open(".mcp.example.json")); m["mcpServers"]["onlyfans"]["headers"]["Authorization"] = "Bearer " + sys.argv[1]
json.dump(m, open(".mcp.json", "w"), indent=2); print("wrote .mcp.json (git-ignored; the scripts read the key from here too)")
EOF
fi

if [ ! -d .git ]; then
  git init -q && git add -A && git commit -q -m "ALTR reports kit" && echo "git: initialised"
fi
chmod +x lib/*.sh 2>/dev/null || true

echo; echo "== connected accounts =="
python3 lib/ofapi.py accounts
echo; echo "Done. Open this folder in Conductor. For publishing links later:  npm i -g vercel && vercel login"
