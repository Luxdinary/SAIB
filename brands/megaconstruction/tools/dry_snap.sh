#!/usr/bin/env bash
# dry build (mock voice, no video) and snapshots for each topic id: dry_snap.sh <outbase> <id> [<id> ...]
cd /c/Automation/faceless-network
OUT=$1; shift
for id in "$@"; do
  .venv/Scripts/python.exe brands/megaconstruction/render/render_gigastruct.py data/direction/$id.json --version dry --tts mock --no-render --tail 8 --mirror gigastruct/dry > /tmp/dry_$id.txt 2>&1
  grep -E "dry run|problem|anchor|Error|error" /tmp/dry_$id.txt | head -5 | sed "s/^/$id: /"
  bash brands/megaconstruction/tools/snap.sh $id "$OUT/$id" > /dev/null
done
echo done
