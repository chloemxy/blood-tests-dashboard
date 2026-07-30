#!/usr/bin/env bash
# Take a new version snapshot of the live index.html.
#
#   ./pipeline/snapshot.sh v1.1 landing-copy-pass
#
# Copies index.html into versions/, commits, and tags the commit so the
# rollback commands shown in history.html actually resolve. Then add the
# entry to the VERSIONS list at the top of pipeline/build_history.py and
# re-run it to regenerate the panel.
set -euo pipefail

if [ $# -lt 2 ]; then
  echo "usage: $0 <version-id> <slug>   e.g. $0 v1.1 landing-copy-pass" >&2
  exit 1
fi

ID="$1"; SLUG="$2"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

FILE="versions/${ID}-${SLUG}.html"
[ -e "$FILE" ] && { echo "refusing to overwrite $FILE" >&2; exit 1; }

cp index.html "$FILE"
git add -A
git commit -m "${ID}: ${SLUG//-/ }"
git tag "${ID}-${SLUG}"

echo
echo "snapshot  $FILE"
echo "tag       ${ID}-${SLUG}"
echo
echo "next: add the entry to VERSIONS in pipeline/build_history.py, then"
echo "      python3 pipeline/build_history.py"
