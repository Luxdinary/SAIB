// betrieb.js · der erfundene Beispielbetrieb „Muster Elektrotechnik e.U.“ als Kulisse (braucht welt.js).
// Ein Schnitt durch das Haus mit drei Räumen: Leitung, Büro, Montage und Lager. Feste Besetzung, alle ohne Gesicht:
// Inhaberin (zugleich Leitung, langes Haar), Büro A (kurzes Haar, graues Hemd), Büro B (Dutt, braunes Hemd), Büro C (Locken),
// Monteur 1 und 2 (Helm, Reflexstreifen, privates Telefon), Lehrling (Kappe, etwas kleiner). Niemand ist echt.
// Weltkoordinaten: Haus von x 40 bis 3320, Boden y 860. Räume: Leitung 80–880, Büro 920–2160, Montage 2200–3280.

const BESETZUNG = {
  inhaberin: { shirt: '#4a4f74', hair: 'long', collar: '#b9c3d8' },
  a: { shirt: '#56647f', hair: 'short' },
  b: { shirt: '#7c6c5c', hair: 'bun' },
  c: { shirt: '#5d6e66', hair: 'curly' },
  monteur1: { jacke: '#3b4860', helm: true, streifen: true, telefon: true },
  monteur2: { jacke: '#45526b', helm: true, streifen: true, telefon: true },
  lehrling: { jacke: '#3d5566', kappe: '#8d99b2', skala: 0.86, streifen: true },
};
const RAUM = { leitung: [80, 880], buero: [920, 2160], montage: [2200, 3280] };
// Kamerapunkte für typische Einstellungen
const BLICK = {
  haus: { f: [1680, 560], z: 0.56 },
  leitung: { f: [480, 560], z: 1.15 },
  buero: { f: [1540, 560], z: 1.0 },
  montage: { f: [2740, 560], z: 1.12 },
  bueroMontage: { f: [2100, 560], z: 0.72 },
};

function bauBetrieb(p, o = {}) {
  const B = { p };
  // Haus
  el('rect', { x: 40, y: 228, width: 3280, height: 652, rx: 28, fill: '#0d1628', stroke: '#1c2944', 'stroke-width': 4 }, p);
  B.schild = g(p);
  el('rect', { x: 1340, y: 172, width: 680, height: 46, rx: 8, fill: '#101a2e', stroke: '#22304c', 'stroke-width': 3 }, B.schild);
  T(B.schild, 1680, 204, { de: 'MUSTER ELEKTROTECHNIK E.U.', en: 'EXAMPLE ELECTRICAL LTD' }, { mono: 1, size: 22, fill: C.muted, anchor: 'middle', ls: '0.12em' });
  raum(p, 80, 270, 800, 590, { de: 'LEITUNG', en: 'MANAGEMENT' });
  raum(p, 920, 270, 1240, 590, { de: 'BÜRO', en: 'OFFICE' });
  raum(p, 2200, 270, 1080, 590, { de: 'MONTAGE · LAGER', en: 'FIELD WORK · STORE' });
  // Leitung: Schrank mit Laden, leerer Rahmen für die Regel an der Wand, Schreibtisch der Inhaberin
  B.schrank = schrank(p, 110, 562, 150, 290);
  B.rahmen = g(p);
  B.rahmenRect = el('rect', { x: 320, y: 340, width: 250, height: 210, rx: 8, fill: 'rgba(255,255,255,0.02)', stroke: C.line, 'stroke-width': 3, 'stroke-dasharray': '12 9' }, B.rahmen);
  B.rahmenLabel = T(B.rahmen, 445, 452, { de: 'REGEL · KI', en: 'RULE · AI' }, { mono: 1, size: 18, fill: C.dim, anchor: 'middle', ls: '0.1em' });
  B.rahmenSlot = g(p, { transform: 'translate(445 445)' }); // hier kann ein Blatt angeheftet werden
  B.figL = seated(p, 534, 772, BESETZUNG.inhaberin);
  tisch(p, 470, 800);
  el('rect', { x: 620, y: 690, width: 70, height: 10, rx: 3, fill: '#2a3858' }, p);
  B.monL = monitor(p, 618, 566, 172, 108, iconDoc);
  // Büro: drei Arbeitsplätze
  ordnerRegal(p, 990, 340, 10);
  fenster2(p, 1430, 330, 250, 160);
  fenster2(p, 1800, 330, 250, 160);
  B.figA = seated(p, 1024, 772, BESETZUNG.a); tisch(p, 960, 1290); el('rect', { x: 1110, y: 690, width: 70, height: 10, rx: 3, fill: '#2a3858' }, p);
  B.monA = monitor(p, 1108, 566, 172, 108, iconSpark);
  B.figB = seated(p, 1424, 772, BESETZUNG.b); tisch(p, 1360, 1690); el('rect', { x: 1510, y: 690, width: 70, height: 10, rx: 3, fill: '#2a3858' }, p);
  B.monB = monitor(p, 1508, 566, 172, 108, iconSpark);
  B.figC = seated(p, 1824, 772, BESETZUNG.c); tisch(p, 1760, 2090); el('rect', { x: 1910, y: 690, width: 70, height: 10, rx: 3, fill: '#2a3858' }, p);
  B.monC = monitor(p, 1908, 566, 172, 108, iconSpark);
  // Montage und Lager: Regal mit Kabeltrommeln, Rolltor, zwei Monteure, ein Lehrling
  el('rect', { x: 2240, y: 400, width: 200, height: 450, rx: 6, fill: '#101a2c', stroke: '#1f2c47', 'stroke-width': 4 }, p);
  for (let r = 0; r < 3; r++) { el('rect', { x: 2246, y: 530 + r * 140, width: 188, height: 8, fill: '#1f2c47' }, p); for (let k = 0; k < 2; k++) { el('circle', { cx: 2296 + k * 82, cy: 486 + r * 140, r: 36, fill: '#16223a', stroke: '#2a3858', 'stroke-width': 4 }, p); el('circle', { cx: 2296 + k * 82, cy: 486 + r * 140, r: 11, fill: '#2a3858' }, p); } }
  B.tor = g(p); el('rect', { x: 3090, y: 400, width: 170, height: 460, rx: 6, fill: '#0c1424', stroke: '#1f2c47', 'stroke-width': 5 }, B.tor);
  for (let i = 0; i < 11; i++) el('rect', { x: 3096, y: 418 + i * 40, width: 158, height: 5, fill: '#1a263f' }, B.tor);
  B.figM1 = stehend(p, 2600, 852, BESETZUNG.monteur1);
  B.figM2 = stehend(p, 2820, 852, BESETZUNG.monteur2);
  B.figLe = stehend(p, 3000, 852, BESETZUNG.lehrling);
  B.monitore = [B.monA, B.monB, B.monC];
  B.telefone = [B.figM1, B.figM2];
  // Ruhezustand
  B.monitore.forEach((m) => bildschirm(m, 0)); bildschirm(B.monL, 0); B.telefone.forEach((f) => { O(f.dim, 0.78); O(f.glow, 0.12); });
  return B;
}
// Bewegungen der Besetzung, die fast jede Einstellung braucht: atmen, tippen, Kopf
function betriebLeben(B, t, o = {}) {
  const tp = o.tippen || {};
  const sitz = [['figA', 0], ['figB', 1.7], ['figC', 3.1], ['figL', 0.8]];
  for (const [k, ph] of sitz) {
    const f = B[k]; const w = tp[k];
    const typ = w ? tippen(t, w[0], w[1], ph) : 0;
    const z = (o.zeigen && o.zeigen[k]) || 0;
    pose(f, -112 * z, typ - 20 * z, 2 * Math.sin(t * 1.2 + ph) - 8 * z);
  }
  for (const [k, ph] of [['figM1', 0.4], ['figM2', 2.2], ['figLe', 1.1]]) {
    const f = B[k]; const hoch = (o.telefonHoch && o.telefonHoch[k] != null) ? o.telefonHoch[k] : (k === 'figLe' ? 0 : 1);
    if (k === 'figLe') arme(f, -6 + 3 * Math.sin(t * 0.8), 0, -6, 0, 3 * Math.sin(t * 0.9 + ph));
    else arme(f, lerp(-6, 18, hoch), lerp(0, 131, hoch), -6, 0, 3 * Math.sin(t * 0.9 + ph) - 6 * hoch);
  }
}

// Kleine Stadt bei Nacht: Häuser mit Fenstern; eines davon ist der Beispielbetrieb (Index B.unser)
function bauStadt(p) {
  const S = { haeuser: [], fenster: [] };
  el('rect', { x: -400, y: 820, width: 2800, height: 8, rx: 4, fill: '#16213a' }, p);
  const formen = [[120, 260, 210], [360, 200, 320], [560, 240, 250], [800, 320, 190], [1100, 230, 300], [1330, 200, 230], [1530, 280, 340], [1810, 220, 260], [-120, 220, 280], [2030, 240, 200]];
  formen.forEach(([x, w, h], i) => {
    const hg = g(p); const y = 820 - h;
    el('rect', { x, y, width: w, height: h, rx: 8, fill: i === 4 ? '#14203a' : '#0f182b', stroke: i === 4 ? '#2a3858' : '#162238', 'stroke-width': 3 }, hg);
    if (i % 3 === 0) el('path', { d: `M ${x - 6} ${y + 2} L ${x + w / 2} ${y - 50} L ${x + w + 6} ${y + 2} Z`, fill: '#0f182b', stroke: '#162238', 'stroke-width': 3 }, hg);
    const fs = [];
    for (let r = 0; r < Math.floor((h - 50) / 62); r++) for (let c = 0; c < Math.floor((w - 30) / 56); c++) {
      const f = el('rect', { x: x + 24 + c * 56, y: y + 30 + r * 62, width: 30, height: 36, rx: 3, fill: '#1a253c' }, hg); fs.push(f);
    }
    S.haeuser.push({ g: hg, x, w, h, y, fs });
  });
  S.unser = 4;
  return S;
}
