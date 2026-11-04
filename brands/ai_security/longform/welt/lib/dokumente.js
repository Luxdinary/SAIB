// dokumente.js · wiederkehrende Bilder von Scutoria (braucht welt.js): Memo mit sieben Fragen, Weg der sechs Schritte.
// Aus der Probe 01 übernommen (Note 1), als Bausteine, damit jeder Akt eine eigene Kopie mit gleichem Aussehen baut.

// ---------- Memo „Womit fangen wir bei KI-Regeln an?“ ----------
function bauMemo(p, o = {}) {
  const M = { g: g(p) };
  const memo = M.g;
  el('rect', { x: -240 + 14, y: -340 + 10, width: 480, height: 680, rx: 6, fill: C.paperBack }, memo);
  el('rect', { x: -240, y: -340, width: 480, height: 680, rx: 6, fill: C.paper, filter: 'url(#shadow)' }, memo);
  T(memo, -200, -288, 'MEMO · SCUTORIA', { mono: 1, size: 15, fill: C.pMuted, ls: '0.08em' });
  T(memo, 200, -288, { de: '30. OKTOBER 2026', en: '30 OCTOBER 2026' }, { mono: 1, size: 15, fill: C.pMuted, anchor: 'end', ls: '0.06em' });
  el('rect', { x: -200, y: -268, width: 400, height: 1.5, fill: C.pLine }, memo);
  T(memo, -200, -216, { de: 'Womit fangen wir', en: 'Where do we start' }, { size: 34, weight: 800, fill: C.pInk });
  T(memo, -200, -176, { de: 'bei KI-Regeln an?', en: 'with AI rules?' }, { size: 34, weight: 800, fill: C.pInk });
  M.qRows = [];
  for (let i = 0; i < 7; i++) {
    const y = -122 + i * 44, gr = g(memo);
    T(gr, -200, y + 5, String(i + 1), { mono: 1, size: 15, fill: C.pMuted });
    const bar = el('rect', { x: -176, y: y - 5, width: 190 + ((i * 37) % 70), height: 10, rx: 5, fill: C.pBar }, gr);
    for (let j = 0; j < 3; j++) el('circle', { cx: 116 + j * 30, cy: y, r: 8, fill: 'none', stroke: '#aab3c2', 'stroke-width': 2 }, gr);
    const sel = el('circle', { cx: 116 + ((i * 2 + 1) % 3) * 30, cy: y, r: 8.5, fill: C.pInk }, gr);
    M.qRows.push({ bar, sel });
  }
  M.band = g(memo);
  el('rect', { x: -214, y: 200, width: 428, height: 100, rx: 10, fill: C.blueSoft }, M.band);
  M.lampe = el('circle', { cx: -180, cy: 250, r: 13, fill: C.red }, M.band);
  T(M.band, -152, 238, { de: 'ERSTER SCHRITT', en: 'FIRST STEP' }, { mono: 1, size: 15, fill: C.blueDeep, ls: '0.08em' });
  el('rect', { x: -152, y: 254, width: 250, height: 10, rx: 5, fill: C.blueBar }, M.band);
  el('rect', { x: -152, y: 274, width: 176, height: 10, rx: 5, fill: C.blueBar }, M.band);
  return M;
}

// ---------- Weg der sechs Schritte ----------
// Weltkoordinaten wie in der Probe; Kamera für die Gesamtsicht: WEG_BLICK. Bildschirmpunkt der Station i: wegPunkt(i).
const WEG_SLOTS = [[1200, 660], [1450, 600], [1700, 640], [1950, 585], [2200, 625], [2450, 570]];
const WEG_BLICK = { f: [1825, 600], z: 1 };
const WEG_NAMEN = [
  { de: 'Bestand', en: 'Stock' }, { de: 'Konten', en: 'Accounts' }, { de: 'Richtlinie', en: 'Policy' },
  { de: 'Einweisung', en: 'Briefing' }, { de: 'Kennzeichnung', en: 'Labelling' }, { de: 'Datum', en: 'Date' },
];
const wegPunkt = (i, blick = WEG_BLICK) => [(WEG_SLOTS[i][0] - blick.f[0]) * blick.z + 960, (WEG_SLOTS[i][1] - blick.f[1]) * blick.z + 540];
function bauWeg(p) {
  const Wg = {};
  Wg.d = catmull([[1040, 700], ...WEG_SLOTS, [2640, 540]]);
  Wg.base = el('path', { d: Wg.d, fill: 'none', stroke: '#172340', 'stroke-width': 18, 'stroke-linecap': 'round' }, p);
  Wg.road = el('path', { d: Wg.d, fill: 'none', stroke: '#33466e', 'stroke-width': 6, 'stroke-linecap': 'round' }, p);
  Wg.pulse = el('path', { d: Wg.d, fill: 'none', stroke: C.blue, 'stroke-width': 8, 'stroke-linecap': 'round' }, p);
  Wg.len = Wg.road.getTotalLength();
  Wg.slotAt = WEG_SLOTS.map(([x]) => { let lo = 0, hi = Wg.len; for (let i = 0; i < 40; i++) { const m = (lo + hi) / 2; if (Wg.road.getPointAtLength(m).x < x) lo = m; else hi = m; } return lo; });
  Wg.nodes = WEG_NAMEN.map((n, i) => {
    const gr = g(p);
    const glow = el('circle', { r: 150, fill: 'url(#gBlue)' }, gr);
    const c = el('circle', { r: 22, fill: C.surface, stroke: C.line, 'stroke-width': 3 }, gr);
    const num = T(gr, 0, 10, String(i + 1), { mono: 1, size: 28, anchor: 'middle', fill: C.muted });
    const haken = g(gr); iconCheck(haken, 26, C.blue); O(haken, 0);
    const lab = T(gr, 0, 92, n, { size: 28, weight: 700, anchor: 'middle', fill: C.muted });
    return { g: gr, glow, c, num, haken, lab, pos: WEG_SLOTS[i].slice() };
  });
  return Wg;
}
// Weg zeichnen: k Anteil gezeichnet (0..1), puls 0..1 (Lichtlauf, -1 aus)
function wegStrecke(Wg, k, puls = -1) {
  const rd = clamp(k) * Wg.len;
  [Wg.road, Wg.base].forEach((q) => { q.setAttribute('stroke-dasharray', `${Wg.len} ${Wg.len}`); q.setAttribute('stroke-dashoffset', (Wg.len - rd).toFixed(1)); });
  if (puls < 0 || puls > 1) { O(Wg.pulse, 0); return -1e9; }
  const head = puls * Wg.len;
  Wg.pulse.setAttribute('stroke-dasharray', `160 ${Wg.len + 400}`); Wg.pulse.setAttribute('stroke-dashoffset', (-(head - 160)).toFixed(1));
  O(Wg.pulse, Math.min(1, puls * 20, (1 - puls) * 8)); return head;
}
// Station zeichnen. s: {da (erscheinen 0..1), aktiv, erledigt, gross, nah, nummer, pos, labAus (0..1), nummerDeck}
function wegKnoten(n, s) {
  const da = s.da == null ? 1 : s.da, act = s.aktiv || 0, done = s.erledigt || 0, grow = s.gross || 0, near = s.nah || 0;
  const r = (22 + act * 24 + grow * 8 + done * 8 + near * 8) * da;
  n.c.setAttribute('r', Math.max(0.1, r).toFixed(2));
  n.c.setAttribute('fill', act > 0.5 ? C.blue : done > 0.5 ? C.raised : C.surface);
  n.c.setAttribute('stroke', act > 0.5 || done > 0.5 || near > 0.4 ? C.blue : C.line);
  O(n.glow, (act * 0.9 + near * 0.6) * da);
  n.num.setAttribute('fill', act > 0.5 ? '#fff' : done > 0.5 ? C.blue : C.muted);
  n.num.setAttribute('font-size', (28 + act * 8).toFixed(1)); n.num.setAttribute('y', (10 + act * 3).toFixed(1));
  if (s.nummer != null && n.num.textContent !== String(s.nummer)) n.num.textContent = String(s.nummer);
  const hk = s.haken || 0; O(n.num, da * (s.nummerDeck == null ? 1 : s.nummerDeck) * (1 - hk)); O(n.haken, da * hk);
  n.lab.setAttribute('fill', act > 0.5 ? C.ink : C.muted);
  n.lab.setAttribute('font-size', (26 + act * 6).toFixed(1)); n.lab.setAttribute('y', (78 + act * 22).toFixed(1));
  O(n.lab, da * (act > 0.5 ? 1 : 0.8) * (1 - (s.labAus || 0)));
  const pos = s.pos || n.pos; tr(n.g, pos[0], pos[1], 1, 0);
}

// ---------- Offenlegung am Schluss (Fassung 2, Stefan, 30. Oktober 2026) ----------
// „Hier ist Scutoria. Die Stimme, die Sie hören, ist synthetisch. Das Skript wurde mit einem KI-Tool entworfen und von uns Satz für Satz
// geprüft. Jede Zahl und jede Rechtsaussage trägt ihre Quelle am Bildschirm. Quellenbasiert, keine Rechtsberatung.“
// Zeichen und Wortmarke, Welle der Stimme, Skript mit Haken je Satz, eine Aussage mit Quellenstreifen, zwei Grundsätze.
// z: Wortzeiten {scut, stimme, synth, skript, entw, pruef, zahl, recht, quelle, qb, keine}; o.aussage: {zeile, wert, rahmen, quelle}
function offenlegungsBuehne(name, z, o = {}) {
  const b = buehne(name, { seed: 5, regalDeckkraft: 0.5 });
  const S = { b, z };
  S.marke = g(b.cam);
  const zg = zeichen(g(S.marke, { transform: 'translate(960 330)' }), 170, C.blue, 1.5);
  S.pfade = [...zg.querySelectorAll('path')];
  S.wort = T(S.marke, 960, 520, 'Scutoria', { size: 92, weight: 800, anchor: 'middle' });
  S.stimme = g(b.cam);
  S.wellen = Array.from({ length: 23 }, (_, i) => el('rect', { x: 960 - 11 * 22 + i * 22 - 5, y: 0, width: 10, height: 10, rx: 5, fill: C.blue }, S.stimme));
  S.stimmPille = pille(S.stimme, { de: 'Synthetische Stimme', en: 'Synthetic voice' }, { size: 28, col: C.blue, icon: 'wave' });
  tr(S.stimmPille, 960, 470);
  S.skript = g(b.cam);
  const sk1 = blatt(S.skript, { w: 440, h: 420, kicker: o.kicker || { de: 'SKRIPT', en: 'SCRIPT' } });
  S.zeilen = linien(sk1.g, sk1.left, sk1.y + 6, 300, 7, 36, C.pBar2, 11);
  S.haken = S.zeilen.map((zz, i) => { const h = g(sk1.g, { transform: `translate(${sk1.right - 14} ${sk1.y + 11 + i * 36})` }); iconCheck(h, 26, C.blueDeep); return h; });
  S.kiTool = pille(S.skript, { de: 'KI-Tool', en: 'AI tool' }, { icon: 'spark', col: C.blue, size: 22 }); tr(S.kiTool, -150, -236);
  S.geprueft = pille(S.skript, { de: 'Satz für Satz geprüft', en: 'checked sentence by sentence' }, { icon: 'check', col: C.green, size: 22 });
  S.aussage = g(b.cam);
  const a = o.aussage || {};
  const sk2 = blatt(S.aussage, { w: 520, h: 420, kicker: { de: 'AUSSAGE', en: 'STATEMENT' } });
  const z1 = T(sk2.g, sk2.left, sk2.y + 40, a.zeile || '', { size: 34, weight: 700, fill: C.pInk });
  const wert = T(sk2.g, sk2.left, sk2.y + 92, a.wert || '', { size: 40, weight: 800, fill: C.pInk });
  S.wertBox = el('rect', { x: sk2.left - 10, y: sk2.y + 50, width: breite(wert) + 20, height: 58, rx: 8, fill: 'none', stroke: C.blue, 'stroke-width': 4 }, sk2.g);
  S.rahmenBox = el('rect', { x: sk2.left - 6, y: sk2.y + 4, width: 150, height: 50, rx: 8, fill: 'none', stroke: C.blue, 'stroke-width': 4 }, sk2.g);
  { const tmp = T(sk2.g, -1000, -1000, a.rahmen || '', { size: 34, weight: 700 }); S.rahmenBox.setAttribute('width', (breite(tmp) + 12).toFixed(0)); tmp.remove(); }
  S.quelle = g(sk2.g);
  el('rect', { x: sk2.x0 + 20, y: sk2.y + 150, width: sk2.w - 40, height: 96, rx: 10, fill: C.blueSoft }, S.quelle);
  T(S.quelle, sk2.left, sk2.y + 184, { de: 'QUELLE', en: 'SOURCE' }, { mono: 1, size: 16, fill: C.blueDeep, ls: '0.1em' });
  TB(S.quelle, sk2.left, sk2.y + 214, a.quelle || '', { mono: 1, size: 17, fill: C.pInk, maxW: sk2.w - 2 * sk2.pad, lh: 22 });
  S.satz1 = pille(b.cam, { de: 'Quellenbasiert', en: 'Source-based' }, { icon: 'book', col: C.blue, size: 34, mono: false, weight: 800 });
  S.satz2 = pille(b.cam, { de: 'Keine Rechtsberatung', en: 'No legal advice' }, { icon: 'para', col: C.muted, size: 34, mono: false, weight: 800 });
  S.zeichnen = (t) => {
    if (!b.vis) return;
    kamera(b, [960, 540], 1);
    S.pfade.forEach((p, i) => zeichne(p, P(t, z.scut + i * 0.25, 0.9)));
    O(S.wort, P(t, z.scut + 0.35, 0.6, E.out));
    const hoch = P(t, z.stimme - 0.5, 0.7);
    tr(S.marke, 960 - 960 * lerp(1, 0.55, hoch), lerp(0, -250, hoch) + 540 - 540 * lerp(1, 0.55, hoch), lerp(1, 0.55, hoch));
    O(S.stimme, fenster(t, z.stimme + 0.1, 0.4, z.skript - 0.3, 0.3)); // erst wenn der Schriftzug oben ist, sonst überlagern sich Welle, Pille und Schriftzug
    const amp = spricht(t);
    S.wellen.forEach((r, i) => { const h = 12 + amp * (26 + 34 * Math.abs(Math.sin(t * 9.3 + i * 1.7)) * Math.abs(Math.sin(t * 3.1 + i * 0.6))); r.setAttribute('y', (370 - h / 2).toFixed(1)); r.setAttribute('height', h.toFixed(1)); });
    tr(S.stimmPille, 960, 470, 1 + 0.06 * puls(t, z.synth, 0.8, 10));
    const sIn = P(t, z.skript - 0.1, 0.7, E.out), unten = P(t, z.qb - 0.45, 0.5, E.in); // Blätter weg, bevor die Pillen kommen
    tr(S.skript, lerp(560, 600, sIn), 650 + unten * 60 + 6 * Math.sin(t * 0.9), 1.12, lerp(-6, -2, sIn)); O(S.skript, Math.min(sIn, 1 - unten));
    S.zeilen.forEach((zz, i) => O(zz, P(t, z.entw + i * 0.16, 0.2)));
    O(S.kiTool, fenster(t, z.entw - 0.1, 0.4, z.pruef + 1.2, 0.4));
    S.haken.forEach((h, i) => { const t0 = z.pruef + 0.15 + i * 0.2; O(h, P(t, t0, 0.15)); h.firstChild.setAttribute('transform', `scale(${Math.max(0.01, P(t, t0, 0.35, E.back)).toFixed(3)})`); });
    tr(S.geprueft, 0, 244, Math.max(0.01, P(t, z.pruef + 1.6, 0.45, E.back))); O(S.geprueft, P(t, z.pruef + 1.6, 0.2));
    const aIn = P(t, z.zahl - 0.15, 0.7, E.out);
    tr(S.aussage, lerp(1400, 1330, aIn), 650 + unten * 60 + 6 * Math.sin(t * 0.8 + 1), 1.12, lerp(5, 2, aIn)); O(S.aussage, Math.min(aIn, 1 - unten));
    zeichne(S.wertBox, P(t, z.zahl + 0.25, 0.6)); zeichne(S.rahmenBox, P(t, z.recht, 0.6));
    const qk = P(t, z.quelle, 0.5, E.out); O(S.quelle, qk); tr(S.quelle, 0, (1 - qk) * 14);
    rein(S.satz1, 960, 560, t, z.qb + 0.15, 0.5); rein(S.satz2, 960, 690, t, z.keine, 0.5);
  };
  return S;
}
