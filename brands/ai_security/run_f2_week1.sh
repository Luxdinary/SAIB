#!/usr/bin/env bash
# Scutoria week 1 in format F2 (review of 03.11.2026). Priority (main session, goal 05.11.2026): the pilot DE+EN and the
# first two topics of 09.11. (DE+EN), then the rest of week 1. Run from the repository root:
#   bash brands/ai_security/run_f2_week1.sh
export PYTHONIOENCODING=utf-8
PY=.venv/Scripts/python.exe
S=brands/ai_security/specs

# 1) DE pilot: approved text and paid voice, new layout
$PY scripts/render_queue.py ai_security -- scripts/render_direction.py data/direction/ai_security-20261115-3-de.P1.json \
  --version P2 --reuse-voice storage/direction/voice_ai_security-20261115-3-de_P1_gemini.wav --assets \
  --mirror scutoria-format/ai_security-20261115-3-de > storage/direction/ai_security-20261115-3-de-P2.log 2>&1
if grep -q "status VALIDATED" storage/direction/ai_security-20261115-3-de-P2.log \
   && node scripts/overlap_check.mjs storage/direction/ai_security-20261115-3-de-P2/project | grep -q '"overlaps":\[\]'; then
  $PY scripts/export_production_folder.py data/direction/ai_security-20261115-3-de.P1.json --version P2 --short "Pilot Neue Bankverbindung" \
    && $PY brands/ai_security/run_specs.py --book-only $S/20261115-3-de.yaml
  echo "pilot de: done"
else
  echo "pilot de: FAILED (see storage/direction/ai_security-20261115-3-de-P2.log)"
fi

# 2) priority: EN pilot, 09.11. topics 1 and 2
$PY brands/ai_security/run_specs.py $S/20261115-3-en.yaml $S/20261109-1-de.yaml $S/20261109-1-en.yaml $S/20261109-2-de.yaml $S/20261109-2-en.yaml
echo "priority batch finished"

# 3) the rest of week 1
$PY brands/ai_security/run_specs.py $(ls $S/2026111[0-5]-*.yaml | grep -v 20261115-3)
