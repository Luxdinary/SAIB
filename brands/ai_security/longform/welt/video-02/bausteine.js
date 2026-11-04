// bausteine.js · Bausteine, die Video 02 braucht und die (noch) nicht in lib/ stehen (braucht welt.js, betrieb.js, dokumente.js).
// Nach VORLAGE-PARALLEL.md, Abschnitt 5: lib/ wird nur gelesen; was hier steht, kann der Chat von Video 01 in die Bibliothek übernehmen.
// Inhalt: Zahlwörter für Wortanker, Quellenleiste ohne Marker, die vier Antworten,
// Fragebogen, Kunde und Lieferant, IT-Betreuung, Belegkarte und Nachweisordner, Weg mit fünf Stationen.

// ---------- Wortanker: Zahlwörter ----------
// Whisper schreibt Zahlen mal als Wort, mal als Ziffer. welt.js kennt nur einfache Zahlwörter; diese hier kommen in Skript 02 vor.
// Danach werden die Wortzeiten neu normiert, damit Skript- und Whisper-Seite dieselbe Tabelle benutzen.
Object.assign(ZAHLWORT, {
  dreizehn: '13', achtzehn: '18', einundzwanzig: '21', dreiundzwanzig: '23', zweiunddreissig: '32', zweiunddreißig: '32', vierzig: '40',
  siebenundvierzig: '47', neunundvierzig: '49', zwanzig: '20', dreissig: '30', dreißig: '30',
  thirteen: '13', eighteen: '18', twentyone: '21', twentythree: '23', thirtytwo: '32', thirtyseven: '37', forty: '40', fortyseven: '47', fortynine: '49', twenty: '20', thirty: '30',
  niszwei: 'nis2', nistwo: 'nis2', niszweirichtlinie: 'nis2richtlinie', niszweikunden: 'nis2kunden',
});
WORT.forEach((w) => { w.n = norm(w.w); });

// ---------- Quellenleiste ohne Marker ----------
// Für Absätze mit [QUELLE], aber ohne [MARKER] (Daten aus video-02/quellen.py). Gleiches Aussehen wie die Leiste von marke().
function leiste(ab, bis, quelle) {
  return hinweis(ab, bis, (gr) => {
    const bg = el('rect', { x: 0, y: 952, width: W, height: 72, fill: 'rgba(18,27,47,0.96)' }, gr);
    const ln = el('rect', { x: 0, y: 952, width: W, height: 1.5, fill: 'rgba(226,232,246,0.14)' }, gr);
    const tx = TB(gr, 96, 998, L({ de: 'Quelle: ', en: 'Source: ' }) + L(quelle), { mono: 1, size: 22, fill: C.muted, maxW: 1728, lh: 30 });
    if (tx.zeilen > 1) { const extra = (tx.zeilen - 1) * 30; bg.setAttribute('y', 952 - extra); bg.setAttribute('height', 72 + extra); ln.setAttribute('y', 952 - extra); tx.setAttribute('y', 998 - extra); }
  });
}
// Nächster Absatz mit Quelle ohne Marker, in Sprechreihenfolge (wie belegt() für die markierten Absätze)
let QUELL_I = 0;
function quelle(opt = {}) {
  const d = (window.QUELLEN_DATEN || [])[QUELL_I++];
  if (!d) { ANKER_FEHLT.push('kein Eintrag in QUELLEN_DATEN'); return { s: 0, e: 0 }; }
  const a = cue(d.start);
  let e = DAUER;
  if (L(d.weiter)) { const n = cue(d.weiter, { halten: true }); e = Math.min(stilleVor(n.s) + 0.6, n.s - 0.05); }
  if (opt.bis) e = opt.bis;
  leiste(a.s - 0.15, e, d.quelle);
  return { s: a.s, e };
}

// ---------- Die vier Antworten ----------
// Form und Wort, nie Farbe allein. Grün nur für den erreichten Zustand „vorhanden“.
function icVorhanden(p, s, col) { const gr = g(p); el('circle', { r: s * 0.42, fill: col }, gr); iconCheck(gr, s * 0.62, C.ground); return gr; }
function icTeilweise(p, s, col) { const gr = g(p); el('rect', { x: -s * 0.38, y: -s * 0.3, width: s * 0.76, height: s * 0.6, rx: s * 0.08, fill: 'none', stroke: col, 'stroke-width': s * 0.1 }, gr); el('rect', { x: -s * 0.38, y: -s * 0.3, width: s * 0.38, height: s * 0.6, rx: s * 0.06, fill: col }, gr); return gr; }
function icNA(p, s, col) { const gr = g(p); el('circle', { r: s * 0.38, fill: 'none', stroke: col, 'stroke-width': s * 0.1 }, gr); el('path', { d: `M${-s * 0.2} 0 H${s * 0.2}`, stroke: col, 'stroke-width': s * 0.12, 'stroke-linecap': 'round' }, gr); return gr; }
const ANTWORT = {
  vorhanden: { t: { de: 'Vorhanden', en: 'In place' }, col: C.green, icon: icVorhanden },
  teilweise: { t: { de: 'Teilweise', en: 'Partly' }, col: C.amber, icon: icTeilweise },
  termin: { t: { de: 'Noch nicht, mit Termin', en: 'Not yet, with a date' }, col: C.amber, icon: 'calendar', gestrichelt: true },
  na: { t: { de: 'Nicht anwendbar, mit Grund', en: 'Not applicable, with a reason' }, col: C.muted, icon: icNA },
};
// Antwortkapsel; text ersetzt das Standardwort (z. B. „keine Kopie außer Reichweite“)
function antwort(p, art, o = {}) { const a = ANTWORT[art]; return pille(p, o.text || a.t, { icon: a.icon, col: a.col, gestrichelt: a.gestrichelt, size: o.size || 26, mono: o.mono != null ? o.mono : false, weight: o.weight || 700, fill: o.fill }); }

// ---------- Fragebogen ----------
// Blatt mit Themenzeilen (Symbol, Wort, Antwortfeld rechts) und einer Terminzeile unten. Mitte 0,0.
function fragebogen(p, zeilen, o = {}) {
  const w = o.w || 560, gap = o.gap || 62;
  const h = o.h || (150 + zeilen.length * gap + (o.termin === false ? 0 : 80));
  const b = blatt(p, { w, h, kicker: o.kicker || { de: 'FRAGEBOGEN · INFORMATIONSSICHERHEIT', en: 'QUESTIONNAIRE · INFORMATION SECURITY' }, kSize: 14, pad: 32 });
  const F = { b, g: b.g, zeilen: [] };
  zeilen.forEach(([ic, txt], i) => {
    const y = b.y + 34 + i * gap, gr = g(b.g);
    const icg = ikon(gr, ic, b.left + 16, y - 8, 30, C.blueDeep);
    const label = T(gr, b.left + 46, y, txt, { size: o.size || 23, weight: 700, fill: C.pInk });
    const fx = b.right - (o.feldW || 120), feld = el('rect', { x: fx, y: y - 26, width: o.feldW || 120, height: 36, rx: 6, fill: 'none', stroke: C.pLine, 'stroke-width': 2 }, gr);
    const ein = g(gr, { transform: `translate(${fx + (o.feldW || 120) / 2} ${y - 8})` }); // Platz für Einträge im Antwortfeld
    F.zeilen.push({ g: gr, icon: icg, label, feld, ein, y, fx });
  });
  if (o.termin !== false) {
    const y = b.y0 + h - 44; F.termin = g(b.g);
    el('rect', { x: b.left - 8, y: y - 30, width: w - 2 * b.pad + 16, height: 46, rx: 8, fill: C.amberSoft }, F.termin);
    ikon(F.termin, 'calendar', b.left + 14, y - 7, 28, C.amberDeep);
    T(F.termin, b.left + 42, y + 2, { de: 'TERMIN FÜR DIE ANTWORT', en: 'ANSWER DUE BY' }, { mono: 1, size: 16, fill: C.amberDeep, ls: '0.08em' });
    el('rect', { x: b.right - 150, y: y - 12, width: 140, height: 10, rx: 5, fill: '#f0d9a0' }, F.termin);
  }
  return F;
}
// Häkchen „Ja“ in ein Antwortfeld setzen (Kästchen plus Wort); gibt Gruppe mit .haken zurück
function jaFeld(z) { const gr = g(z.ein); const k = kaestchen(gr, -30, 0, 22); T(gr, -10, 8, { de: 'Ja', en: 'Yes' }, { size: 22, weight: 800, fill: C.pInk }); return { g: gr, haken: k.haken }; }

// ---------- Kunde, Lieferant, Behörde ----------
// Größerer Kunde: Bürohaus mit vielen Fenstern, Fuß bei y. Erfunden, ohne Namen.
function kundeHaus(p, x, y, s = 1, o = {}) {
  const gr = g(p, { transform: `translate(${x} ${y}) scale(${s})` });
  el('rect', { x: -150, y: -460, width: 300, height: 460, rx: 10, fill: '#13203a', stroke: C.edge, 'stroke-width': 4 }, gr);
  el('rect', { x: -110, y: -500, width: 220, height: 44, rx: 6, fill: '#13203a', stroke: C.edge, 'stroke-width': 4 }, gr);
  const fenster = [];
  for (let r = 0; r < 7; r++) for (let c = 0; c < 5; c++) fenster.push(el('rect', { x: -122 + c * 50, y: -436 + r * 56, width: 30, height: 34, rx: 3, fill: (r * 5 + c) % 4 === 1 ? '#2a3d62' : '#1a2742' }, gr));
  el('rect', { x: -34, y: -70, width: 68, height: 70, rx: 4, fill: '#0c1424', stroke: C.edge, 'stroke-width': 3 }, gr);
  const lab = o.label === null ? null : T(gr, 0, 46, o.label || { de: 'GRÖSSERER KUNDE', en: 'LARGER CUSTOMER' }, { mono: 1, size: 24, fill: C.muted, anchor: 'middle', ls: '0.1em' });
  return { g: gr, fenster, lab, x, y, s };
}
// Kleiner Betrieb: Haus mit Giebel, Fuß bei y
function kleinHaus(p, x, y, s = 1, o = {}) {
  const gr = g(p, { transform: `translate(${x} ${y}) scale(${s})` });
  el('path', { d: 'M -120 -170 L 0 -260 L 120 -170 Z', fill: '#16233d', stroke: C.edge, 'stroke-width': 4, 'stroke-linejoin': 'round' }, gr);
  el('rect', { x: -110, y: -172, width: 220, height: 172, rx: 6, fill: '#13203a', stroke: C.edge, 'stroke-width': 4 }, gr);
  const fenster = [el('rect', { x: -84, y: -138, width: 50, height: 46, rx: 4, fill: '#2a3d62' }, gr), el('rect', { x: 34, y: -138, width: 50, height: 46, rx: 4, fill: '#1a2742' }, gr)];
  el('rect', { x: -26, y: -76, width: 52, height: 76, rx: 4, fill: '#0c1424', stroke: C.edge, 'stroke-width': 3 }, gr);
  const lab = o.label === null ? null : T(gr, 0, 46, o.label || { de: 'IHR BETRIEB', en: 'YOUR BUSINESS' }, { mono: 1, size: 24, fill: C.muted, anchor: 'middle', ls: '0.1em' });
  return { g: gr, fenster, lab, x, y, s };
}
// Behörde: Säulenhaus mit Wort
function behoerde(p, x, y, s = 1, label) {
  const gr = g(p, { transform: `translate(${x} ${y}) scale(${s})` });
  el('circle', { cx: 0, cy: -80, r: 120, fill: 'url(#gPaper)' }, gr);
  const ic = g(gr, { transform: 'translate(0 -84)' }); iconInstitution(ic, 130, C.ink);
  if (label) T(gr, 0, 30, label, { mono: 1, size: 24, fill: C.muted, anchor: 'middle', ls: '0.1em' });
  return { g: gr, x, y, s };
}

// ---------- Externe IT-Betreuung ----------
// Stehende Figur ohne Gesicht mit Jacke und Laptop (nicht Teil der festen Besetzung des Betriebs, weil extern)
function itBetreuung(p, x, y, s = 1) {
  const f = stehend(p, x, y, { jacke: '#36597a', haar: 'short', kragen: '#cfd6e3', skala: s });
  const lap = g(f.foreR, { transform: 'translate(14 70) rotate(-12)' });
  el('rect', { x: -40, y: -26, width: 80, height: 52, rx: 5, fill: '#0f1626', stroke: '#3a4d75', 'stroke-width': 3 }, lap);
  el('rect', { x: -33, y: -20, width: 66, height: 38, rx: 3, fill: '#c9d6ef' }, lap);
  f.laptop = lap; return f;
}
// Baustelle: Absperrung mit Streifen und Leitkegel, Fuß bei y
function baustelle(p, x, y) {
  const gr = g(p, { transform: `translate(${x} ${y})` });
  for (const dx of [-150, 150]) el('rect', { x: dx - 6, y: -120, width: 12, height: 120, fill: '#3a4d75' }, gr);
  el('rect', { x: -170, y: -120, width: 340, height: 40, rx: 6, fill: '#1c2943', stroke: '#3a4d75', 'stroke-width': 3 }, gr);
  for (let i = 0; i < 6; i++) el('path', { d: `M ${-160 + i * 56} -82 L ${-136 + i * 56} -118 L ${-112 + i * 56} -118 L ${-136 + i * 56} -82 Z`, fill: C.amber, opacity: 0.55 }, gr);
  for (const dx of [-240, 230]) { el('path', { d: `M ${dx - 26} 0 L ${dx} -76 L ${dx + 26} 0 Z`, fill: '#b9852a' }, gr); el('rect', { x: dx - 18, y: -40, width: 36, height: 9, fill: '#e9eef8', opacity: 0.6 }, gr); }
  return gr;
}

// ---------- Belege und Nachweisordner ----------
// Belegkarte (Papier) mit Symbol und Wort; o.offen: gestrichelt bernsteinfarben mit Kalender (fehlt noch, hat einen Termin)
function belegKarte(p, ic, text, o = {}) {
  const gr = g(p); const w = o.w || 300, h = o.h || 70;
  const r = el('rect', { x: -w / 2, y: -h / 2, width: w, height: h, rx: 8, fill: o.offen ? C.amberSoft : C.paper, stroke: o.offen ? C.amberLine : 'none', 'stroke-width': 3, 'stroke-dasharray': o.offen ? '10 7' : '', filter: o.offen ? '' : 'url(#shadowS)' }, gr);
  ikon(gr, o.offen ? 'calendar' : ic, -w / 2 + 34, 0, 34, o.offen ? C.amberDeep : C.blueDeep);
  const tx = TB(gr, -w / 2 + 62, 8, text, { size: o.size || 22, weight: 700, fill: o.offen ? C.amberDeep : C.pInk, maxW: w - 76, lh: (o.size || 22) * 1.15 });
  if (tx.zeilen > 1) tx.setAttribute('y', 8 - (tx.zeilen - 1) * (o.size || 22) * 0.58);
  gr.w = w; gr.h = h; gr.rect = r; return gr;
}
// Nachweisordner: Mappe mit Reiter und Aufschrift; Mitte 0,0
function nachweisOrdner(p, o = {}) {
  const gr = g(p); const w = o.w || 420, h = o.h || 300;
  el('path', { d: `M ${-w / 2} ${-h / 2 + 30} V ${h / 2} H ${w / 2} V ${-h / 2 + 30} H ${-w / 2 + 170} L ${-w / 2 + 140} ${-h / 2} H ${-w / 2 + 16} Q ${-w / 2} ${-h / 2} ${-w / 2} ${-h / 2 + 16} Z`, fill: '#1f3150', stroke: C.blue, 'stroke-width': 3, 'stroke-linejoin': 'round' }, gr);
  const vorne = g(gr);
  el('rect', { x: -w / 2, y: -h / 2 + 64, width: w, height: h - 64, rx: 10, fill: '#22385d', stroke: C.blue, 'stroke-width': 3 }, vorne);
  T(vorne, 0, h / 2 - 34, o.label || { de: 'NACHWEISORDNER', en: 'EVIDENCE FOLDER' }, { mono: 1, size: 24, fill: C.ink, anchor: 'middle', ls: '0.12em' });
  return { g: gr, vorne, w, h };
}

// ---------- Weg mit fünf Stationen (wie dokumente.js, eigene Stationen) ----------
const WEG5_SLOTS = [[1250, 650], [1530, 592], [1810, 640], [2090, 582], [2370, 626]];
const WEG5_BLICK = { f: [1810, 610], z: 1 };
const WEG5_NAMEN = [
  { de: 'Verstehen', en: 'Understand' }, { de: 'Vier Antworten', en: 'Four answers' }, { de: 'Größe', en: 'Size' },
  { de: 'Nachweise', en: 'Evidence' }, { de: 'Senden', en: 'Send' },
];
const weg5Punkt = (i, blick = WEG5_BLICK) => [(WEG5_SLOTS[i][0] - blick.f[0]) * blick.z + 960, (WEG5_SLOTS[i][1] - blick.f[1]) * blick.z + 540];
function bauWeg5(p) {
  const Wg = {};
  Wg.d = catmull([[1080, 700], ...WEG5_SLOTS, [2540, 560]]);
  Wg.base = el('path', { d: Wg.d, fill: 'none', stroke: '#172340', 'stroke-width': 18, 'stroke-linecap': 'round' }, p);
  Wg.road = el('path', { d: Wg.d, fill: 'none', stroke: '#33466e', 'stroke-width': 6, 'stroke-linecap': 'round' }, p);
  Wg.pulse = el('path', { d: Wg.d, fill: 'none', stroke: C.blue, 'stroke-width': 8, 'stroke-linecap': 'round' }, p);
  Wg.len = Wg.road.getTotalLength();
  Wg.nodes = WEG5_NAMEN.map((n, i) => {
    const gr = g(p);
    const glow = el('circle', { r: 150, fill: 'url(#gBlue)' }, gr);
    const c = el('circle', { r: 22, fill: C.surface, stroke: C.line, 'stroke-width': 3 }, gr);
    const num = T(gr, 0, 10, String(i + 1), { mono: 1, size: 28, anchor: 'middle', fill: C.muted });
    const haken = g(gr); iconCheck(haken, 26, C.blue); O(haken, 0);
    const lab = T(gr, 0, 92, n, { size: 28, weight: 700, anchor: 'middle', fill: C.muted });
    return { g: gr, glow, c, num, haken, lab, pos: WEG5_SLOTS[i].slice() };
  });
  return Wg;
}
// Zustand des ganzen Wegs zum Zeitpunkt t: aktiv = Index der aktiven Station (oder -1), erledigt = Anzahl erledigter Stationen
function weg5Zeichnen(Wg, t, s) {
  wegStrecke(Wg, s.strecke == null ? 1 : s.strecke, s.puls == null ? -1 : s.puls);
  Wg.nodes.forEach((n, i) => wegKnoten(n, { da: s.da ? s.da[i] : 1, aktiv: s.aktiv === i ? (s.aktivK == null ? 1 : s.aktivK) : 0, erledigt: i < (s.erledigt || 0) ? 1 : 0, haken: i < (s.erledigt || 0) ? 1 : 0, nah: s.nah === i ? 1 : 0 }));
}

// ---------- Kleinigkeiten ----------
// Durchstreichen: roter oder grauer Strich über einer Kapsel der Breite w, Mitte 0,0
function streich(p, w, col = C.muted) { return el('path', { d: `M ${-w / 2 - 8} 6 L ${w / 2 + 8} -6`, stroke: col, 'stroke-width': 5, 'stroke-linecap': 'round', fill: 'none' }, p); }
// Kalenderkapsel „Termin“
function terminPille(p, text, size = 24) { return pille(p, text || { de: 'Termin', en: 'Due date' }, { icon: 'calendar', col: C.amber, gestrichelt: true, size }); }
