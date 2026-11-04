#!/usr/bin/env bash
# Render, check and export Gigastruct "Bauaufgabe" plans one after another (no Claude needed while it runs).
#   bash brands/megaconstruction/tools/bauaufgabe_batch.sh <log> "<topic>|<lang>|<short title>" ...
# Each item "topic|lang|short title[|version]" (version default P1): render via scripts/render_queue.py (Gemini voice, version P1), node scripts/overlap_check.mjs,
# export to OneDrive\Business\05 Produktion (only when the render validated and the overlap check is empty).
cd /c/Automation/faceless-network || exit 1
export PYTHONIOENCODING=utf-8
LOG="$1"; shift
for item in "$@"; do
  IFS="|" read -r topic lang short ver <<< "$item"; ver=${ver:-P1}
  id="megaconstruction-$topic-$lang"
  plan="data/direction/$id.P1.json"
  echo "=== $id $(date +%H:%M)" >> "$LOG"
  voice="storage/direction/voice_${id}_${ver}_gemini.wav"
  if [ -f "$voice" ]; then tts=(--reuse-voice "$voice"); else tts=(--tts gemini); fi
  .venv/Scripts/python.exe scripts/render_queue.py megaconstruction -- brands/megaconstruction/render/render_gigastruct.py "$plan" \
      --version "$ver" "${tts[@]}" --mirror "gigastruct/w1/$id" 2>&1 | grep -E "^voice:|status |length |NOT |FAIL|Error|error" >> "$LOG"
  if grep -q "\"passed\": true" "storage/direction/$id-$ver/report.json" 2>/dev/null; then
    ov=$(node scripts/overlap_check.mjs "storage/direction/$id-$ver/project" 2>&1 | tail -1)
    echo "overlap: $ov" >> "$LOG"
    if echo "$ov" | grep -q '"overlaps":\[\]'; then
      .venv/Scripts/python.exe scripts/export_production_folder.py "$plan" --version "$ver" --short "$short" ${FORCE:+--force} 2>&1 | grep -E "^export:|rror" >> "$LOG"
    fi
  else
    echo "not validated, no export" >> "$LOG"
  fi
done
echo "=== done $(date +%H:%M)" >> "$LOG"
