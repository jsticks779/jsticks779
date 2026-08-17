#!/usr/bin/env bash
#
# Rebuilds assets/showreel.mp4 + assets/showreel.gif from the hero animation.
#
# Headless Chrome's virtual clock does not advance CSS animations, so each frame
# is captured by seeking every animation with the Web Animations API and then
# screenshotting that exact moment. Frames are rendered 4 at a time.
#
# Needs: google-chrome, ffmpeg, python3
set -euo pipefail
cd "$(dirname "$0")"

SVG="${1:-assets/hero-dark.svg}"
FPS=15            # frame rate of the reel
SECS=13.5         # one full loop of the hero animation
W=1200; H=340
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

{
  printf '<!doctype html><meta charset="utf-8"><style>html,body{margin:0;padding:0;background:#0d1117}svg{display:block}</style>\n'
  cat "$SVG"
  cat <<'JS'
<script>
var t = parseFloat(new URLSearchParams(location.search).get('t') || '0') * 1000;
document.getAnimations().forEach(function (a) { try { a.pause(); a.currentTime = t; } catch (e) {} });
</script>
JS
} > "$WORK/frame.html"

mkdir -p "$WORK/frames"
TOTAL=$(python3 -c "print(int($FPS*$SECS))")
echo "rendering $TOTAL frames…"

seq 0 $((TOTAL-1)) | xargs -P 4 -I{} sh -c '
  i={}
  t=$(python3 -c "print(round($i/'"$FPS"',3))")
  google-chrome --headless=new --disable-gpu --no-sandbox --hide-scrollbars \
    --force-device-scale-factor=1 --window-size='"$W,$H"' --virtual-time-budget=800 \
    --user-data-dir='"$WORK"'/profile-$i \
    --screenshot="'"$WORK"'/frames/$(printf %04d $i).png" \
    "file://'"$WORK"'/frame.html?t=$t" >/dev/null 2>&1
'

echo "encoding…"
ffmpeg -y -loglevel error -framerate $FPS -i "$WORK/frames/%04d.png" \
  -vf "scale=1000:-2:flags=lanczos" -c:v libx264 -pix_fmt yuv420p -crf 22 -movflags +faststart \
  assets/showreel.mp4

ffmpeg -y -loglevel error -framerate $FPS -i "$WORK/frames/%04d.png" \
  -vf "fps=12,scale=820:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=128[p];[b][p]paletteuse=dither=bayer:bayer_scale=3" \
  assets/showreel.gif

ls -lh assets/showreel.mp4 assets/showreel.gif
