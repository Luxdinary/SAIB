#!/usr/bin/env bash
# snapshots at 40 % and 85 % of every beat of a dry build: snap.sh <topic_id> <outdir>
cd /c/Automation/faceless-network/storage/direction/$1-dry || exit 1
AT=$(PYTHONIOENCODING=utf-8 python -c "
import json;p=json.load(open('plan.timed.json',encoding='utf-8'));print(','.join(str(round(b['start']+b['duration']*f,1)) for b in p['beats'] for f in (0.4,0.85)))")
cd project && timeout 500 npx hyperframes snapshot . -o "$2" --at $AT --no-end 2>&1 | tail -1
