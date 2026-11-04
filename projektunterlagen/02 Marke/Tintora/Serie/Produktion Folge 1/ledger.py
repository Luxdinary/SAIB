# Kleines Hilfsskript: hält Job-Nummern, Credits und Prompt-Bausteine fest und schreibt LICENSE.md.
import json, sys, os, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
LED = os.path.join(HERE, 'ledger.json')
BLOCKS = {
 'STYLE': "Classic TV anime still for a children's series (ages 6-9): crisp clean line art, cel shading with sharp two-tone shadows, vivid colours, richly painted background. No text, no letters, no logos, not photorealistic.",
 'JUNA': "JUNA (copy the design exactly from the Juna reference sheet): 9-year-old cartoon adventurer, short messy sunset-orange hair with one magenta streak, two star hair clips, amber eyes, freckles, yellow hooded raincoat over blue-white striped shirt, green rubber boots, carved wooden leaf pendant.",
 'LUCI': "LUCI (copy from the Luci reference sheet): tiny firefly, smaller than Juna's hand, plum-brown body, big amber eyes, red wing covers with several white dots, tail glowing warm yellow.",
 'TASSILO': "TASSILO (copy from the Tassilo reference sheet): hermit crab living in a round white teapot with blue flowers, lid worn as a hat, orange-red claws with the right one bigger, about as tall as Juna's boot.",
 'MIRA': "MIRA (copy from the Mira reference sheet): large gentle moth of pale-grey mist, about twice Juna's height, big sad round eyes, old brass lantern; not scary.",
}
def load():
    return json.load(open(LED, encoding='utf-8')) if os.path.exists(LED) else []
def save(d):
    json.dump(d, open(LED, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
def add(rows):
    d = load(); d.extend(rows); save(d)
def fetch(job, url, name):
    sub = 'Videos' if url.endswith('.mp4') else 'Bilder'
    p = os.path.join(HERE, sub, name)
    urllib.request.urlretrieve(url, p)
    d = load()
    for r in d:
        if r['job'] == job: r['file'] = f'{sub}/{name}'
    save(d)
    return p
def license():
    d = load()
    out = ['# Lizenz und Herkunft: Produktion Folge 1', '',
           'Erzeugt mit Higgsfield, Tarif Ultra, über den MCP-Server `higgsfield`, ab 02.11.2026. Es gelten die Higgsfield-Nutzungsbedingungen Abschnitt 4.4: keine Einschränkung der kommerziellen Nutzung der Ergebnisse.',
           r'Referenzen: eigene Modellblätter und Schauplätze aus `Stufe 0\05 Rebrand Anime-Stil\` (Job-IDs dort in `Stufe 0\LICENSE.md`).',
           '', '**Prompt-Bausteine** (wörtlich; in der Tabelle mit Namen genannt):', '']
    for k, v in BLOCKS.items(): out.append(f'- `{k}`: {v}')
    out += ['', '| Shot | Datei | Modell | Job-ID | Credits | Prompt |', '|---|---|---|---|---|---|']
    tot = 0
    for r in d:
        tot += r['credits']
        out.append(f"| {r['shot']} | {r.get('file','–')} | {r['model']} | {r['job']} | {r['credits']} | {r['prompt']} |")
    out += ['', f'**Summe: {len(d)} Aufträge, {tot} Credits**', '']
    open(os.path.join(HERE, 'LICENSE.md'), 'w', encoding='utf-8').write('\n'.join(out))
    print('Summe', tot, 'Aufträge', len(d))
if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'add': add(json.load(open(sys.argv[2], encoding='utf-8')))
    elif cmd == 'fetch':
        for line in open(sys.argv[2], encoding='utf-8'):
            if line.strip():
                job, url, name = line.rstrip('\n').split('|'); print(fetch(job, url, name))
    elif cmd == 'addq':
        rows=[]
        for line in open(sys.argv[2], encoding='utf-8'):
            if line.strip():
                shot, job, summ = line.rstrip(chr(10)).split('|', 2)
                rows.append({'shot': shot, 'job': job, 'model': 'Nano Banana Pro 2K', 'credits': 2, 'prompt': summ})
        add(rows)
    elif cmd == 'license': license()
