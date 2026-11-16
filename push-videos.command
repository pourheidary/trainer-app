#!/bin/bash
# Sends the animation files in app/videos to GitHub in small batches.
# Safe to run again: it only handles files that are not committed yet, so after an interruption it simply continues.
cd "$(dirname "$0")" || exit 1
BATCH="${BATCH:-150}"
pause() { read -n 1 -s -r -p "Press any key to close..."; echo; }
if [ ! -d app/videos ]; then
  echo "The folder app/videos was not found. Copy the videos folder into app first."
  pause; exit 1
fi
IN_FOLDER=$(ls app/videos | wc -l | tr -d ' ')
TODO=$(git ls-files --others --exclude-standard app/videos | wc -l | tr -d ' ')
echo "Files in app/videos : $IN_FOLDER (expected 1324)"
echo "Not yet in git      : $TODO"
if [ "$TODO" -eq 0 ]; then
  echo "All video files are already committed. Checking that they are pushed..."
  git push && echo "Done."
  pause; exit 0
fi
read -r -p "Press Enter to send them in batches of $BATCH (or press Ctrl+C to stop)... "
N=0
while true; do
  FILES=$(git ls-files --others --exclude-standard app/videos | head -n "$BATCH")
  [ -z "$FILES" ] && break
  N=$((N + 1))
  COUNT=$(echo "$FILES" | wc -l | tr -d ' ')
  echo "$FILES" | tr '\n' '\0' | xargs -0 git add --
  if ! git commit -q -m "Add exercise animations (batch $N, $COUNT files)" 2>/dev/null; then
    echo "Commit failed for batch $N. Nothing was lost. Send me this screen."
    pause; exit 1
  fi
  echo "Batch $N committed ($COUNT files). Sending..."
  if ! git push -q; then
    echo "Push failed for batch $N. Nothing is lost: run this script again to continue."
    pause; exit 1
  fi
  echo "Batch $N sent. Left: $(git ls-files --others --exclude-standard app/videos | wc -l | tr -d ' ') files."
done
echo ""
echo "Done. All animations are on GitHub."
git status -sb | head -2
pause
