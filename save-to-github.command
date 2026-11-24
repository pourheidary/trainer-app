#!/bin/bash
# Double-click (or run ./save-to-github.command in Terminal) to push a version of the trainer app to GitHub.
# 1. Choose the folder that holds your trainer-app-v*.html files (default: Downloads).
# 2. Pick any version from the list. It is copied into app/ and history/, committed, tagged and pushed.
#    A connected static host (Cloudflare) then redeploys, so the website shows the version you picked.
# You can push several versions one after another; the last one pushed is the one the website shows.
cd "$(dirname "$0")" || exit 1
DIR="${DOWNLOADS_DIR:-$HOME/Downloads}"
LAST=""
pause() { read -n 1 -s -r -p "Press any key to close..."; echo; }

choose_folder() {
  local p=""
  if command -v osascript >/dev/null 2>&1; then
    p=$(osascript -e 'try' -e 'POSIX path of (choose folder with prompt "Choose the folder that contains the trainer-app-v*.html files")' -e 'end try' 2>/dev/null)
  fi
  if [ -z "$p" ]; then
    echo "Drag the folder into this window (or type its path) and press Enter."
    echo "Press Enter with nothing typed to keep: $DIR"
    read -r p
    p=$(printf '%s' "$p" | sed "s/^['\"]//; s/['\"]\$//; s/\\\\\(.\)/\1/g; s/[[:space:]]*\$//")
    p="${p/#\~/$HOME}"
  fi
  if [ -z "$p" ]; then return; fi
  if [ -d "$p" ]; then DIR="${p%/}"; else echo "Folder not found: $p"; echo "Keeping: $DIR"; fi
}

list_versions() {
  FILES=(); VERS=()
  local tmp f v k
  tmp=$(mktemp)
  for f in "$DIR"/trainer-app*.html; do
    [ -f "$f" ] || continue
    v=$(grep -o 'name="app-version" content="[^"]*"' "$f" | head -1 | sed 's/.*content="//; s/"$//')
    k=$(printf '%s' "${v:-0}" | awk -F. '{printf "%05d%05d", $1, $2}')
    printf '%s\t%s\t%s\n' "$k" "${v:-?}" "$f" >> "$tmp"
  done
  while IFS=$'\t' read -r k v f; do FILES+=("$f"); VERS+=("$v"); done < <(sort -r "$tmp")
  rm -f "$tmp"
}

show_list() {
  local i f notes when mark
  echo
  echo "Folder: $DIR"
  if [ ${#FILES[@]} -eq 0 ]; then
    echo "No trainer-app*.html files in this folder."
    return
  fi
  echo "Versions found (newest first):"
  for i in "${!FILES[@]}"; do
    f="${FILES[$i]}"
    notes=$(grep -o 'name="app-notes" content="[^"]*"' "$f" | head -1 | sed 's/.*content="//; s/"$//' | cut -c1-70)
    when=$(stat -c '%y' "$f" 2>/dev/null | cut -c1-16)
    [ -z "$when" ] && when=$(stat -f '%Sm' -t '%Y-%m-%d %H:%M' "$f" 2>/dev/null)
    mark=""
    if [ -f app/index.html ] && cmp -s "$f" app/index.html; then mark="   <-- this is on GitHub now"; fi
    printf '  %2d)  v%-6s %s  (%s)%s\n' "$((i + 1))" "${VERS[$i]}" "$(basename "$f")" "$when" "$mark"
    [ -n "$notes" ] && printf '        %s\n' "$notes"
  done
}

push_version() {
  local SRC="$1" VER NOTES MSG
  echo
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
    return 1
  else
    [ -n "$VER" ] && git tag -a "v$VER" -m "$MSG" 2>/dev/null
  fi
  if git push --follow-tags; then
    echo "Done: $MSG"
    echo "A connected static host redeploys automatically; the website will show v$VER in a minute or two."
    LAST="$VER"
    return 0
  else
    echo "Push failed. Check your internet connection and GitHub login (token), then try again."
    return 1
  fi
}

while true; do
  list_versions
  show_list
  echo
  read -r -p "Type a number to push that version, f = choose another folder, q = quit: " ans
  case "$ans" in
    q|Q|"") break ;;
    f|F) choose_folder ;;
    *)
      if [[ "$ans" =~ ^[0-9]+$ ]] && [ "$ans" -ge 1 ] && [ "$ans" -le ${#FILES[@]} ]; then
        f="${FILES[$((ans - 1))]}"
        read -r -p "Push v${VERS[$((ans - 1))]} ($(basename "$f")) to GitHub? The website will show this version. (y/n) " yn
        case "$yn" in y|Y|yes|YES) push_version "$f" ;; *) echo "Cancelled." ;; esac
      else
        echo "Not a valid choice."
      fi ;;
  esac
done
[ -n "$LAST" ] && echo "Last version pushed in this session: v$LAST"
pause
