#!/bin/bash
# Double-click: saves the newest downloaded trainer-app*.html into this repository,
# names the version from the file's own metadata, commits, tags and pushes it to GitHub.
# It also keeps app/index.html in sync so a static host (Cloudflare Pages, GitHub Pages) serves the app at the site root.
cd "$(dirname "$0")" || exit 1
DL="${DOWNLOADS_DIR:-$HOME/Downloads}"
pause() { read -n 1 -s -r -p "Press any key to close..."; echo; }
SRC=$(ls -t "$DL"/trainer-app*.html 2>/dev/null | head -1)
if [ -z "$SRC" ]; then
  echo "No file named trainer-app*.html found in $DL."
  echo "Click the GitHub button in the app (or download the file from the chat) first."
  pause; exit 1
fi
echo "Using: $SRC"
VER=$(grep -o 'name="app-version" content="[^"]*"' "$SRC" | head -1 | sed 's/.*content="//; s/"$//')
NOTES=$(grep -o 'name="app-notes" content="[^"]*"' "$SRC" | head -1 | sed 's/.*content="//; s/"$//')
mkdir -p app
cp "$SRC" app/trainer-app.html
cp "$SRC" app/index.html
if [ -n "$VER" ]; then
  mkdir -p history
  cp "$SRC" "history/v$VER.html"
  MSG="v$VER: $NOTES"
else
  MSG="Update trainer app ($(date '+%Y-%m-%d %H:%M'))"
fi
git add -A
if git diff --cached --quiet; then
  echo "This version is already committed; checking that it is pushed."
elif ! git commit -m "$MSG"; then
  echo "Commit failed. If git asked who you are, run these two commands once and try again:"
  echo '  git config --global user.name "Your Name"'
  echo '  git config --global user.email "you@example.com"'
  pause; exit 1
else
  [ -n "$VER" ] && git tag -a "v$VER" -m "$MSG" 2>/dev/null
fi
if git push --follow-tags; then
  echo "Done: $MSG"
  echo "The newest version is saved on GitHub. A connected static host redeploys automatically."
else
  echo "Push failed. Check your internet connection and GitHub login (token), then run this again."
fi
pause
