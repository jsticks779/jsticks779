#!/usr/bin/env bash
#
# Rebuilds assets/showreel.mp4 + assets/showreel.gif from a hero SVG: one
# screenshot of the static banner, then a slow cinematic zoom into an MP4, and a
# looping GIF for the README.
#
# Needs: google-chrome, ffmpeg
set -euo pipefail
cd "$(dirname "$0")"

SVG="${1:-assets/hero-dark.svg}"
SECS=4
W=1200; H=340
SIZE=1000
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

{
  printf '<!doctype html><meta charset="utf-8"><style>html,body{margin:0;padding:0;background:%s}svg{display:block}</style>\n' "${BG:-#0d1117}"
  cat "$SVG"
} > "$WORK/frame.html"

google-chrome --headless=new --disable-gpu --no-sandbox --hide-scrollbars \
  --force-device-scale-factor=1 --window-size="$W,$H" \
  --screenshot="$WORK/hero.png" "file://$WORK/frame.html" >/dev/null 2>&1

ffmpeg -y -loglevel error -i "$WORK/hero.png" \
  -vf "zoompan=z='min(zoom+0.0015,1.20)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=$(python3 -c "print(int(24*$SECS))"):s=${SIZE}x-1:fps=24" \
  -c:v libx264 -pix_fmt yuv420p -crf 22 -movflags +faststart \
  assets/showreel.mp4

ffmpeg -y -loglevel error -i assets/showreel.mp4 \
  -vf "fps=12,scale=900:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=192[p];[b][p]paletteuse" \
  assets/showreel.gif

ls -lh assets/showreel.mp4 assets/showreel.gif