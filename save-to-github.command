#!/bin/bash
# Double-click: saves the newest downloaded trainer-app*.html into this repository and pushes it to GitHub.
cd "$(dirname "$0")" || exit 1
DL="${DOWNLOADS_DIR:-$HOME/Downloads}"
pause() { read -n 1 -s -r -p "Press any key to close..."; echo; }
SRC=$(ls -t "$DL"/trainer-app*.html 2>/dev/null | head -1)
if [ -z "$SRC" ]; then
  echo "No file named trainer-app*.html found in $DL."
  echo "Download the new version from the chat first, then run this again."
  pause; exit 1
fi
echo "Using: $SRC"
cp "$SRC" app/trainer-app.html
git add -A
if git diff --cached --quiet; then
  echo "This version is already committed; checking that it is pushed."
elif ! git commit -m "Update trainer app ($(date '+%Y-%m-%d %H:%M'))"; then
  echo "Commit failed. If git asked who you are, run these two commands once and try again:"
  echo '  git config --global user.name "Your Name"'
  echo '  git config --global user.email "you@example.com"'
  pause; exit 1
fi
if git push; then
  echo "Done. The newest version is saved on GitHub."
else
  echo "Push failed. Check your internet connection and GitHub login (token), then run this again."
fi
pause
