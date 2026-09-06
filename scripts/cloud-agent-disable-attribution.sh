#!/usr/bin/env bash
# Disable Cursor Cloud Agent commit/PR attribution trailers on this VM.
# Idempotent: safe to run from environment start on every boot.
set -euo pipefail

disable_co_author_hook() {
  local hook_path="$1"
  cat >"$hook_path" <<'EOF'
#!/bin/bash
# @cursor-managed-override
# Co-author trailer injection disabled by environment policy.
exit 0
EOF
  chmod +x "$hook_path"
}

install_strip_hook() {
  local hook_path="$1"
  cat >"$hook_path" <<'EOF'
#!/bin/bash
# @cursor-managed-override
# Remove AI/tool co-author and attribution trailers from commit messages.
set -euo pipefail
MSG_FILE="${1:?}"
tmp="$(mktemp)"
grep -Eiv \
  -e '^[[:space:]]*Co-authored-by:' \
  -e '^[[:space:]]*Made-with:[[:space:]]*Cursor' \
  -e '^[[:space:]]*Made with Cursor' \
  -e 'Submitted by[[:space:]]+Cursorbot' \
  -e 'Submitted by[[:space:]]+cursor\[bot\]' \
  "$MSG_FILE" >"$tmp" || true
# Drop trailing blank lines introduced by removals.
python3 - "$tmp" "$MSG_FILE" <<'PY'
import pathlib
import sys
src, dst = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
text = src.read_text(encoding="utf-8", errors="replace")
dst.write_text(text.rstrip() + ("\n" if text.strip() else ""), encoding="utf-8")
PY
  rm -f "$tmp"
  exit 0
EOF
  chmod +x "$hook_path"
}

shopt -s nullglob
for hooks_dir in /home/ubuntu/.cursor/agent-hooks/*/; do
  [ -d "$hooks_dir" ] || continue
  if [ -e "${hooks_dir}commit-msg.cursor.co-author" ] || [ -e "${hooks_dir}commit-msg" ]; then
    disable_co_author_hook "${hooks_dir}commit-msg.cursor.co-author"
    install_strip_hook "${hooks_dir}commit-msg.cursor.zz-strip-co-authors"
  fi
done

# Also honor a CLI attribution opt-out when the file is writable.
CLI_CONFIG="${HOME}/.cursor/cli-config.json"
if [ -d "$(dirname "$CLI_CONFIG")" ]; then
  python3 - "$CLI_CONFIG" <<'PY'
import json
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
data = {}
if path.exists():
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        data = {}
if not isinstance(data, dict):
    data = {}
attr = data.get("attribution")
if not isinstance(attr, dict):
    attr = {}
attr["attributeCommitsToAgent"] = False
attr["attributePRsToAgent"] = False
data["attribution"] = attr
path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
PY
fi

echo "cloud-agent-disable-attribution: co-author injection disabled; strip hook installed"
