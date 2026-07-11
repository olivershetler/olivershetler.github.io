#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
export PATH="$PWD/.venv/Scripts:$PATH"

PYTHON="$PWD/.venv/Scripts/python"
FFMPEG="$PWD/.venv/Scripts/ffmpeg"
OUTPUT_DIR="../../public/media/pubs"
MAX_BYTES=1572864

mkdir -p "$OUTPUT_DIR"

render_one() {
  local file="$1"
  local scene="$2"
  local slug="$3"
  local poster_time="$4"
  local rendered="media/videos/$file/720p30/$slug.mp4"
  local output="$OUTPUT_DIR/$slug.mp4"
  local temporary="$OUTPUT_DIR/$slug.reencode.mp4"

  "$PYTHON" -m manim render -qm --format mp4 -o "$slug" "scenes/$file.py" "$scene"

  if ! "$FFMPEG" -y -i "$rendered" -c copy -movflags +faststart "$output"; then
    "$FFMPEG" -y -i "$rendered" -an -c:v libx264 -crf 25 -pix_fmt yuv420p -movflags +faststart "$output"
  fi

  local size
  size=$(wc -c < "$output")
  if (( size > MAX_BYTES )); then
    "$FFMPEG" -y -i "$output" -an -c:v libx264 -preset medium -b:v 700k -maxrate 800k -bufsize 1400k -pix_fmt yuv420p -movflags +faststart "$temporary"
    mv "$temporary" "$output"
    size=$(wc -c < "$output")
  fi

  "$FFMPEG" -y -ss "$poster_time" -i "$output" -frames:v 1 -update 1 "$OUTPUT_DIR/$slug.png"
  printf '%-24s %10d bytes\n' "$slug.mp4" "$size"
}

render_one "beyond_correlation" "BeyondCorrelation" "beyond-correlation" "7.3"
render_one "mec_spatial_coding" "MecSpatialCoding" "mec-spatial-coding" "7.8"
render_one "lec_dysfunction" "LecDysfunction" "lec-dysfunction" "7.5"
render_one "lfp_tools" "LfpTools" "lfp-tools" "8.6"
render_one "quantile_risk" "QuantileRisk" "quantile-risk" "8.5"

TALK_OUTPUT_DIR="../../public/media/talks"
TALK_SLUG="risk-filtered-automation"
TALK_RENDERED="media/videos/risk_filtered_automation/720p30/$TALK_SLUG.mp4"
TALK_OUTPUT="$TALK_OUTPUT_DIR/$TALK_SLUG.mp4"
TALK_TEMPORARY="$TALK_OUTPUT_DIR/$TALK_SLUG.reencode.mp4"

mkdir -p "$TALK_OUTPUT_DIR"
"$PYTHON" -m manim render -qm --format mp4 -o "$TALK_SLUG" \
  "scenes/risk_filtered_automation.py" "RiskFilteredAutomation"
"$FFMPEG" -y -i "$TALK_RENDERED" -an -c:v libx264 -crf 25 \
  -pix_fmt yuv420p -movflags +faststart "$TALK_OUTPUT"

talk_size=$(wc -c < "$TALK_OUTPUT")
if (( talk_size > MAX_BYTES )); then
  "$FFMPEG" -y -i "$TALK_OUTPUT" -an -c:v libx264 -preset medium \
    -b:v 650k -maxrate 750k -bufsize 1300k -pix_fmt yuv420p \
    -movflags +faststart "$TALK_TEMPORARY"
  mv "$TALK_TEMPORARY" "$TALK_OUTPUT"
  talk_size=$(wc -c < "$TALK_OUTPUT")
fi

"$FFMPEG" -y -ss "14.7" -i "$TALK_OUTPUT" -frames:v 1 -update 1 \
  "$TALK_OUTPUT_DIR/$TALK_SLUG.png"
printf '%-24s %10d bytes\n' "$TALK_SLUG.mp4" "$talk_size"
