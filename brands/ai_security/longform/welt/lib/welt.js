// Kopie von OneDrive\scutoria\marketing\youtube\ANIMATION\lib\welt.js, Stand 31.10.2026; geändert 03.11.2026: HUD oben rechts mit KI-Kennzeichnung.
// welt.js · Bausteine der animierten Erklärwelt von Scutoria („Nachtarchiv“: dunkler Raum, das einzige Licht ist Papier).
// Klassisches Skript ohne Module, damit eine Szene direkt als Datei geöffnet und von rendern.mjs aufgenommen werden kann.
// Inhalt: Grundlagen, Wortanker, Bühnen mit Übergängen, Symbole, Figuren, Möbel, Papier, Einblendungen (HUD), Ablauf.
// Regeln aus der Marke: kein Gesicht, nur Manrope und IBM Plex Mono, Marker immer mit Form und Wort, Farben aus tokens.css.
// Vor dem Laden muss window.WOERTER (Wortzeiten aus woerter.py) gesetzt sein.

// ================= Grundlagen =================
const W = 1920, H = 1080, NS = 'http://www.w3.org/2000/svg';
const LANG = new URLSearchParams(location.search).get('lang') || 'de';
const L = (o) => (o == null ? '' : typeof o === 'string' ? o : (o[LANG] != null ? o[LANG] : o.de));
const C = {
  ground: '#0b1120', surface: '#121b2f', raised: '#19243b', ink: '#e9eef8', muted: '#a1adc4', dim: '#5d6b88',
  paper: '#fbfbfd', paperBack: '#d9dfea', pInk: '#141a24', pMuted: '#5a6472', pLine: '#d7dce6', pBar: '#e1e6ee', pBar2: '#c9d1df',
  blue: '#4f8cff', blueDeep: '#1f5fd1', blueSoft: '#e6eeff', blueBar: '#c3d2f6', amber: '#ffd166', amberDeep: '#c98f00', amberLine: '#e0a800', amberSoft: '#fff4d6',
  red: '#ff6b6b', redDeep: '#d64545', redSoft: '#ffe3e3', green: '#2ec4b6', greenDeep: '#14907f', greenSoft: '#dff6f3', purple: '#b07cff', purpleDeep: '#7b4fd6', purpleSoft: '#efe6ff',
  wall: '#0f192c', desk: '#1b2740', edge: '#2e3d5e', lane: '#22314f', line: '#3a4d75', dark: '#0c1424', floor: '#1a2640'
};
const SKIN = '#c9d3e6', HAIR = '#26324a', PANTS = '#1d2840', SHOE = '#141c2c';
const F = { sans: 'Manrope, sans-serif', mono: '"IBM Plex Mono", monospace' };
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const lerp = (a, b, k) => a + (b - a) * k;
const lerp2 = (a, b, k) => [lerp(a[0], b[0], k), lerp(a[1], b[1], k)];
const E = {
  lin: (x) => x,
  io: (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2),
  out: (x) => 1 - Math.pow(1 - x, 3),
  in: (x) => x * x * x,
  back: (x) => { const c1 = 1.5, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); },
  sine: (x) => -(Math.cos(Math.PI * x) - 1) / 2,
};
// P: Fortschritt 0..1 einer Bewegung, die bei t0 beginnt und d Sekunden dauert
const P = (t, t0, d, e = E.io) => e(clamp((t - t0) / d));
// fenster: einblenden ab a (Dauer din), ausblenden ab b (Dauer dout)
const fenster = (t, a, din, b, dout = din) => Math.min(P(t, a, din, E.out), 1 - P(t, b, dout, E.in));
const swing = (t, t0) => (t < t0 ? 0 : Math.exp(-3.2 * (t - t0)) * Math.cos(9 * (t - t0)));
const puls = (t, t0, dauer = 1.2, f = 7) => (t > t0 && t < t0 + dauer ? Math.sin((t - t0) * f) * (1 - (t - t0) / dauer) : 0);
const tippen = (t, a, b, ph = 0, amp = 5) => (t > a && t < b ? amp * Math.sin(t * 2 * Math.PI * 4.5 + ph) : 0);
const qb = (p0, p1, p2, k) => [(1 - k) * (1 - k) * p0[0] + 2 * (1 - k) * k * p1[0] + k * k * p2[0], (1 - k) * (1 - k) * p0[1] + 2 * (1 - k) * k * p1[1] + k * k * p2[1]];
// Bogenflug von a nach b mit Scheitel h über dem höheren Punkt
const bogen = (a, b, k, h = 200) => qb(a, [(a[0] + b[0]) / 2, Math.min(a[1], b[1]) - h], b, k);
function el(tag, attrs = {}, parent) { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); if (parent) parent.appendChild(e); return e; }
const g = (parent, attrs = {}) => el('g', attrs, parent);
function T(parent, x, y, s, o = {}) {
  const e = el('text', { x, y, 'font-family': o.mono ? F.mono : F.sans, 'font-size': o.size || 28, 'font-weight': o.weight || (o.mono ? 400 : 600), fill: o.fill || C.ink, 'text-anchor': o.anchor || 'start' }, parent);
  if (o.ls) e.setAttribute('letter-spacing', o.ls);
  e.textContent = L(s); return e;
}
// Text mit Zeilenumbruch nach gemessener Breite (Schriften müssen geladen sein)
function TB(parent, x, y, s, o = {}) {
  const e = T(parent, x, y, '', o); const maxW = o.maxW || 800, lh = o.lh || (o.size || 28) * 1.25;
  const words = L(s).split(' '); let line = [], lines = [];
  const probe = el('tspan', {}, e);
  for (const w of words) { probe.textContent = [...line, w].join(' '); if (probe.getComputedTextLength() > maxW && line.length) { lines.push(line.join(' ')); line = [w]; } else line.push(w); }
  if (line.length) lines.push(line.join(' '));
  e.removeChild(probe);
  lines.forEach((ln, i) => { const ts = el('tspan', { x, dy: i === 0 ? 0 : lh }, e); ts.textContent = ln; });
  e.zeilen = lines.length; return e;
}
const breite = (e) => e.getComputedTextLength();
const tr = (e, x, y, s = 1, r = 0) => e.setAttribute('transform', `translate(${x.toFixed(2)} ${y.toFixed(2)}) rotate(${r.toFixed(3)}) scale(${Math.max(0.0001, s).toFixed(4)})`);
// Skalieren um einen Punkt (Aufpoppen an Ort und Stelle)
const sk = (e, cx, cy, s) => e.setAttribute('transform', `translate(${cx.toFixed(2)} ${cy.toFixed(2)}) scale(${Math.max(0.0001, s).toFixed(4)}) translate(${(-cx).toFixed(2)} ${(-cy).toFixed(2)})`);
function O(e, o) { o = clamp(o); e.setAttribute('opacity', o.toFixed(3)); e.setAttribute('visibility', o < 0.003 ? 'hidden' : 'visible'); }
// Aufpoppen: Skalierung mit Überschwingen und Deckkraft ab t0
function pop(e, cx, cy, t, t0, d = 0.45, bis = Infinity, dout = 0.35) { const k = P(t, t0, d, E.back); sk(e, cx, cy, Math.max(0.01, k)); O(e, Math.min(P(t, t0, d * 0.5), 1 - P(t, bis, dout))); }
// Einblenden mit kleiner Bewegung von unten
function rein(e, x, y, t, t0, d = 0.5, bis = Infinity, dy = 24, dout = 0.4) { const k = P(t, t0, d, E.out); tr(e, x, y + (1 - k) * dy); O(e, Math.min(k, 1 - P(t, bis, dout))); }
const cam = (e, fx, fy, s, cx = 960, cy = 540) => e.setAttribute('transform', `translate(${cx.toFixed(2)} ${cy.toFixed(2)}) scale(${s.toFixed(5)}) translate(${(-fx).toFixed(2)} ${(-fy).toFixed(2)})`);
// Kamerafahrt aus Einstellungen [{t, d, f:[x,y], z}], ausgehend von start {f, z}
function fahrt(t, start, shots) { let f = start.f.slice(), z = start.z; for (const s of shots) { const k = P(t, s.t, s.d || 0.8, s.e || E.io); f = lerp2(f, s.f, k); z = lerp(z, s.z, k); } return { f, z }; }
function typeText(e, s, t, t0, dur) { const str = L(s); const n = Math.round(clamp((t - t0) / dur) * str.length); const v = str.slice(0, n); if (e.textContent !== v) e.textContent = v; }
function setText(e, s) { const v = L(s); if (e.textContent !== v) e.textContent = v; }
// Strich zeichnet sich (Pfad, Linie, Rechteck)
function zeichne(p, k, len) { len = len || p.__len || (p.__len = p.getTotalLength()); p.setAttribute('stroke-dasharray', `${len.toFixed(1)} ${len.toFixed(1)}`); p.setAttribute('stroke-dashoffset', ((1 - clamp(k)) * len).toFixed(1)); }
function catmull(pts) {
  let d = `M ${pts[0][0]} ${pts[0][1]}`;
  for (let i = 0; i < pts.length - 1; i++) {
    const p0 = pts[i - 1] || pts[i], p1 = pts[i], p2 = pts[i + 1], p3 = pts[i + 2] || p2;
    d += ` C ${(p1[0] + (p2[0] - p0[0]) / 6).toFixed(1)} ${(p1[1] + (p2[1] - p0[1]) / 6).toFixed(1)} ${(p2[0] - (p3[0] - p1[0]) / 6).toFixed(1)} ${(p2[1] - (p3[1] - p1[1]) / 6).toFixed(1)} ${p2[0]} ${p2[1]}`;
  }
  return d;
}
// Punkte, die in Zeitfenstern ausgesandt werden und mit fester Geschwindigkeit einen Pfad entlang laufen
function emits(windows, interval) { const out = []; windows.forEach(([a, b]) => { for (let x = a; x <= b + 1e-6; x += interval) out.push(x); }); return out; }
function placeDots(pool, path, len, ems, t, speed = 360, reverse = false) {
  let n = 0;
  for (const e of ems) {
    const d = (t - e) * speed; if (d < 0 || d > len) continue;
    if (n >= pool.length) break;
    const pt = path.getPointAtLength(reverse ? len - d : d);
    const dot = pool[n++]; tr(dot, pt.x, pt.y, 1, 0); O(dot, Math.min(1, d / 30, (len - d) / 30));
  }
  for (; n < pool.length; n++) O(pool[n], 0);
}

// ================= Wortanker =================
// Jede Bildaktion hängt an einem gesprochenen Wort. cue('Schritt eins') sucht die Wortfolge ab der aktuellen Stelle
// in den Whisper-Wortzeiten und gibt {s, e} in Sekunden ab Videobeginn zurück. Alternativen mit „|“,
// kleine Abweichungen der Erkennung werden toleriert. Fehlt ein Anker, steht er in window.ANKER_FEHLT.
const ZAHLWORT = { eins: '1', zwei: '2', drei: '3', vier: '4', fuenf: '5', fünf: '5', sechs: '6', sieben: '7', acht: '8', neun: '9', zehn: '10', elf: '11', zwoelf: '12', zwölf: '12', fuenfzehn: '15', fünfzehn: '15', fuenfzig: '50', fünfzig: '50',
  one: '1', two: '2', three: '3', four: '4', five: '5', six: '6', seven: '7', eight: '8', nine: '9', ten: '10', eleven: '11', twelve: '12', fifteen: '15', fifty: '50' };
// Zahlen als Wort und als Ziffer gelten gleich (Whisper schreibt mal „drei“, mal „3“)
function roh(s) { return String(s).toLowerCase().replace(/ß/g, 'ss').replace(/[^\p{L}\p{N}]+/gu, ''); }
function norm(s) { const n = roh(s); return ZAHLWORT[n] || n; }
const WORT = (window.WOERTER || []).map((w) => ({ s: w.s, e: w.e, n: norm(w.w), r: roh(w.w), w: w.w })).filter((w) => w.n);
const DAUER = window.TON ? window.TON.dauer : 60;
function lev(a, b) { const m = a.length, n = b.length; const d = Array.from({ length: m + 1 }, (_, i) => [i]); for (let j = 1; j <= n; j++) d[0][j] = j; for (let i = 1; i <= m; i++) for (let j = 1; j <= n; j++) d[i][j] = Math.min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1)); return d[m][n]; }
function aehnlich(a, b) { if (a === b) return 1; if (a.length < 4 || b.length < 4) return 0; return 1 - lev(a, b) / Math.max(a.length, b.length); }
let CUR = 0; const ANKER_FEHLT = []; window.ANKER_FEHLT = ANKER_FEHLT;
function passt(toks, i) {
  let j = i, k = 0;
  while (k < toks.length) {
    if (j >= WORT.length) return null;
    const w = WORT[j].n, a = toks[k];
    if (aehnlich(a, w) >= 0.8 || aehnlich(roh(toks.roh[k]), WORT[j].r) >= 0.8) { j++; k++; continue; }
    if (j + 1 < WORT.length && aehnlich(a, w + WORT[j + 1].n) >= 0.85) { j += 2; k++; continue; }
    if (j + 2 < WORT.length && aehnlich(a, w + WORT[j + 1].n + WORT[j + 2].n) >= 0.85) { j += 3; k++; continue; }
    if (k + 1 < toks.length && aehnlich(a + toks[k + 1], w) >= 0.85) { j++; k += 2; continue; }
    if (k + 2 < toks.length && aehnlich(a + toks[k + 1] + toks[k + 2], w) >= 0.85) { j++; k += 3; continue; }
    return null;
  }
  return j;
}
function cue(p, opt = {}) {
  const txt = L(p), from = opt.ab != null ? opt.ab : CUR, bis = Math.min(WORT.length, from + (opt.weit || 500));
  for (const alt of txt.split('|')) {
    const teile = alt.trim().split(/\s+/).filter((x) => norm(x));
    const toks = teile.map(norm); toks.roh = teile;
    if (!toks.length) continue;
    for (let i = from; i < bis; i++) { const j = passt(toks, i); if (j != null) { if (!opt.halten) CUR = j; return { s: WORT[i].s, e: WORT[j - 1].e, i, j }; } }
  }
  if (opt.leise) return null; // optionaler Anker: fehlt er, entscheidet der Aufrufer
  ANKER_FEHLT.push(`„${txt}“ ab Wort ${from} (${from < WORT.length ? WORT[from].w : 'Ende'})`);
  const t0 = from > 0 && from <= WORT.length ? WORT[from - 1].e : 0;
  return { s: t0 + 0.5, e: t0 + 1, i: from, j: from };
}
const at = (p, opt) => cue(p, opt).s;
// Ende des letzten Wortes vor t (für Ausklänge in Pausen)
function stilleVor(t) { let e = 0; for (const w of WORT) { if (w.s >= t - 0.01) break; e = w.e; } return e; }

// ================= Bühne, Ebenen, Übergänge =================
const svg = document.getElementById('stage');
const defs = el('defs', {}, svg);
function radial(id, col, a) { const gr = el('radialGradient', { id, cx: '50%', cy: '50%', r: '50%' }, defs); el('stop', { offset: 0, 'stop-color': col, 'stop-opacity': a }, gr); el('stop', { offset: 0.55, 'stop-color': col, 'stop-opacity': a * 0.28 }, gr); el('stop', { offset: 1, 'stop-color': col, 'stop-opacity': 0 }, gr); }
radial('gBlue', '#4f8cff', 0.5); radial('gPaper', '#ffffff', 0.09); radial('gPaperS', '#ffffff', 0.16); radial('gAmber', '#ffd166', 0.45); radial('gRed', '#ff6b6b', 0.4); radial('gGreen', '#2ec4b6', 0.4); radial('gPurple', '#b07cff', 0.4);
{ const sp = el('radialGradient', { id: 'gSpot', gradientUnits: 'userSpaceOnUse', cx: 960, cy: 540, r: 640 }, defs); el('stop', { offset: 0, 'stop-color': '#0b1120', 'stop-opacity': 0 }, sp); el('stop', { offset: 0.55, 'stop-color': '#0b1120', 'stop-opacity': 0 }, sp); el('stop', { offset: 1, 'stop-color': '#0b1120', 'stop-opacity': 0.82 }, sp); }
{ const v = el('radialGradient', { id: 'gVig', cx: '50%', cy: '46%', r: '72%' }, defs); el('stop', { offset: 0.6, 'stop-color': '#000', 'stop-opacity': 0 }, v); el('stop', { offset: 1, 'stop-color': '#000', 'stop-opacity': 0.5 }, v); }
{ const f = el('filter', { id: 'shadow', x: '-30%', y: '-30%', width: '160%', height: '170%' }, defs); el('feDropShadow', { dx: 0, dy: 16, stdDeviation: 18, 'flood-color': '#000', 'flood-opacity': 0.5 }, f); }
{ const f = el('filter', { id: 'shadowS', x: '-40%', y: '-40%', width: '180%', height: '190%' }, defs); el('feDropShadow', { dx: 0, dy: 6, stdDeviation: 7, 'flood-color': '#000', 'flood-opacity': 0.45 }, f); }
const LAYER = g(svg);        // Bühnen
const RINGE = g(svg);        // Ringe der Kreisöffnungen
el('rect', { x: 0, y: 0, width: W, height: H, fill: 'url(#gVig)' }, svg);
const HUD = g(svg);          // Einblendungen
const FADE = el('rect', { x: 0, y: 0, width: W, height: H, fill: '#05080f', opacity: 0 }, svg);

function shelves(p, seed) {
  for (let i = 0; i < 10; i++) {
    const x = i * 290 - 220, h = 560 + ((i * 137 + seed * 53) % 5) * 46, y = 1080 - h - 20;
    el('rect', { x, y, width: 236, height: h, rx: 6, fill: '#0d1525' }, p);
    for (let r = 0; r < Math.floor(h / 124); r++) {
      const yy = y + 34 + r * 124;
      el('rect', { x: x + 12, y: yy + 74, width: 212, height: 4, fill: '#131d32' }, p);
      let xx = x + 20, k = (i * 7 + r * 3 + seed) % 11;
      while (xx < x + 206) { const w = 10 + ((k * 29) % 9), hh = 42 + ((k * 17) % 28);
        el('rect', { x: xx, y: yy + 74 - hh, width: w, height: hh, rx: 2, fill: k % 9 === 0 ? '#243049' : '#101a2c' }, p); xx += w + 3; k++; }
    }
  }
}
const BUEHNEN = [];
let bIdx = 0;
// Eine Bühne ist ein Vollbild mit eigenem Hintergrund und eigener Kamera (cam). front liegt über der Kamera im Bildraum.
function buehne(name, opt = {}) {
  const id = 'clip' + (bIdx++);
  const clip = el('clipPath', { id, clipPathUnits: 'userSpaceOnUse' }, defs);
  const cc = el('circle', { cx: 960, cy: 540, r: 0 }, clip);
  const root = g(LAYER, { display: 'none' });
  const wrap = g(root);
  el('rect', { x: -60, y: -60, width: W + 120, height: H + 120, fill: C.ground }, wrap);
  const back = g(wrap, { opacity: opt.regalDeckkraft != null ? opt.regalDeckkraft : 1 });
  if (opt.regale !== false) shelves(back, opt.seed != null ? opt.seed : bIdx);
  const glow = el('circle', { cx: 960, cy: 620, r: 860, fill: 'url(#gPaper)', opacity: opt.licht != null ? opt.licht : 1 }, wrap);
  const camG = g(wrap);
  const front = g(wrap);
  const spot = el('rect', { x: 0, y: 0, width: W, height: H, fill: 'url(#gSpot)', opacity: 0 }, wrap);
  const b = { name, id, root, wrap, back, cam: camG, front, spot, glow, cc, vis: false, ring: el('circle', { cx: 0, cy: 0, r: 0, fill: 'none', stroke: C.blue, 'stroke-width': 5, visibility: 'hidden' }, RINGE) };
  BUEHNEN.push(b); return b;
}
// Kamera einer Bühne setzen; Regale verschieben sich leicht mit (Tiefe)
function kamera(b, f, z) { cam(b.cam, f[0], f[1], z); tr(b.back, -(f[0] - 960) * 0.18, -(f[1] - 540) * 0.08, 1, 0); }
// Schnittliste: Bühne b ist ab Zeitpunkt ab zu sehen; ueber beschreibt den Übergang vom vorherigen Bild.
// Typen: schnitt, blende (Überblendung), schwarz (über Dunkel), kreis (Öffnung aus Punkt p der alten Bühne),
// kreisRaus (die alte Bühne schrumpft zurück in Punkt p der neuen), schieben (dir 1: neue kommt von rechts).
const SCHNITT = [];
function shot(b, ab, ueber = { typ: 'blende', d: 0.7 }) { SCHNITT.push({ b, ab, ueber }); }
function zeige(b, o = 1) { b.root.setAttribute('display', 'inline'); b.root.setAttribute('opacity', clamp(o).toFixed(3)); b.vis = true; }
function zuOben(b) { if (LAYER.lastChild !== b.root) LAYER.appendChild(b.root); }
function kreisDaten(k, p) { // aus der Probe übernommen: Zoom 1 auf 3 um p, Kreisradius bis Vollbild
  const e = E.io(k); const Z = lerp(1, 3, e); const ps = lerp2(p, [960, 540], e);
  const r = 46 * Z * lerp(1, 8.4, E.in(k)); return { Z, ps, r, sc: r / 1159 };
}
let UEBERGANG = null; // aktueller Übergang {typ, k, von, nach}, für Bühnen, die darauf reagieren wollen
function compose(t) {
  for (const b of BUEHNEN) { b.vis = false; b.root.setAttribute('display', 'none'); b.root.removeAttribute('clip-path'); b.wrap.removeAttribute('transform'); b.ring.setAttribute('visibility', 'hidden'); }
  UEBERGANG = null;
  let i = -1; for (let k = 0; k < SCHNITT.length; k++) if (SCHNITT[k].ab <= t) i = k;
  if (i < 0) { if (SCHNITT.length) zeige(SCHNITT[0].b); return; }
  const cur = SCHNITT[i], prev = SCHNITT[i - 1], u = cur.ueber || { typ: 'schnitt' };
  const d = u.d || 0.7, k = clamp((t - cur.ab) / d);
  if (!prev || u.typ === 'schnitt' || k >= 1 || prev.b === cur.b) { zeige(cur.b); return; }
  const A = prev.b, B = cur.b;
  UEBERGANG = { typ: u.typ, k, von: A, nach: B };
  if (u.typ === 'blende') { zeige(A); zeige(B, E.io(k)); zuOben(B); }
  else if (u.typ === 'schwarz') { if (k < 0.5) zeige(A, 1 - E.io(k * 2)); else zeige(B, E.io(k * 2 - 1)); }
  else if (u.typ === 'schieben') { const dir = u.dir || 1, e = E.io(k); zeige(A); zeige(B); A.wrap.setAttribute('transform', `translate(${(-dir * W * e).toFixed(1)} 0)`); B.wrap.setAttribute('transform', `translate(${(dir * W * (1 - e)).toFixed(1)} 0)`); }
  else if (u.typ === 'kreis' || u.typ === 'kreisRaus') {
    const inner = u.typ === 'kreis' ? B : A, outer = u.typ === 'kreis' ? A : B, kk = u.typ === 'kreis' ? k : 1 - k;
    const q = kreisDaten(kk, u.p);
    zeige(outer); zeige(inner); zuOben(inner);
    outer.wrap.setAttribute('transform', `translate(${q.ps[0].toFixed(2)} ${q.ps[1].toFixed(2)}) scale(${q.Z.toFixed(4)}) translate(${(-u.p[0]).toFixed(2)} ${(-u.p[1]).toFixed(2)})`);
    inner.wrap.setAttribute('transform', `translate(${q.ps[0].toFixed(2)} ${q.ps[1].toFixed(2)}) scale(${q.sc.toFixed(5)}) translate(-960 -540)`);
    inner.cc.setAttribute('cx', q.ps[0].toFixed(2)); inner.cc.setAttribute('cy', q.ps[1].toFixed(2)); inner.cc.setAttribute('r', Math.max(0, q.r).toFixed(2));
    inner.root.setAttribute('clip-path', `url(#${inner.id})`);
    const ring = inner.ring; ring.setAttribute('cx', q.ps[0].toFixed(2)); ring.setAttribute('cy', q.ps[1].toFixed(2)); ring.setAttribute('r', Math.max(0, q.r).toFixed(2)); O(ring, 1 - clamp((q.r - 150) / 500));
    if (kk >= 0.999) { outer.root.setAttribute('display', 'none'); outer.vis = false; }
  }
  else zeige(B);
}

// ================= Symbole (Form plus Wort, nie Farbe allein; Mitte 0,0, Größe s) =================
const sw = (s, f = 0.09) => s * f;
function iconBuilding(p, s, col) { const gr = g(p);
  el('path', { d: `M${-s * 0.42} ${s * 0.44} V${-s * 0.12} L0 ${-s * 0.44} L${s * 0.42} ${-s * 0.12} V${s * 0.44} Z`, fill: 'none', stroke: col, 'stroke-width': s * 0.1, 'stroke-linejoin': 'round' }, gr);
  el('rect', { x: -s * 0.12, y: s * 0.1, width: s * 0.24, height: s * 0.34, fill: col }, gr); return gr; }
function iconPerson(p, s, col) { const gr = g(p);
  el('circle', { cx: 0, cy: -s * 0.2, r: s * 0.19, fill: col }, gr);
  el('path', { d: `M${-s * 0.38} ${s * 0.44} Q${-s * 0.38} ${s * 0.04} 0 ${s * 0.04} Q${s * 0.38} ${s * 0.04} ${s * 0.38} ${s * 0.44} Z`, fill: col }, gr); return gr; }
function iconUnknown(p, s, col) { const gr = g(p);
  el('circle', { r: s * 0.42, fill: 'none', stroke: col, 'stroke-width': s * 0.09, 'stroke-dasharray': `${s * 0.18} ${s * 0.12}` }, gr);
  T(gr, 0, s * 0.2, '?', { size: s * 0.58, weight: 800, fill: col, anchor: 'middle' }); return gr; }
function iconSpark(p, s, col) { const r = s * 0.48, k = 0.16;
  return el('path', { d: `M0 ${-r} C${r * k} ${-r * k} ${r * k} ${-r * k} ${r} 0 C${r * k} ${r * k} ${r * k} ${r * k} 0 ${r} C${-r * k} ${r * k} ${-r * k} ${r * k} ${-r} 0 C${-r * k} ${-r * k} ${-r * k} ${-r * k} 0 ${-r} Z`, fill: col }, p); }
function iconTranslate(p, s, col) { const gr = g(p);
  el('rect', { x: -s * 0.46, y: -s * 0.42, width: s * 0.52, height: s * 0.52, rx: s * 0.1, fill: 'none', stroke: col, 'stroke-width': s * 0.09 }, gr);
  el('rect', { x: -s * 0.06, y: -s * 0.1, width: s * 0.52, height: s * 0.52, rx: s * 0.1, fill: col }, gr); return gr; }
function iconChat(p, s, col) { return el('path', { d: `M${-s * 0.44} ${-s * 0.34} h${s * 0.88} a${s * 0.08} ${s * 0.08} 0 0 1 ${s * 0.08} ${s * 0.08} v${s * 0.46} a${s * 0.08} ${s * 0.08} 0 0 1 ${-s * 0.08} ${s * 0.08} h${-s * 0.5} l${-s * 0.24} ${s * 0.2} v${-s * 0.2} h${-s * 0.06} a${s * 0.08} ${s * 0.08} 0 0 1 ${-s * 0.08} ${-s * 0.08} v${-s * 0.46} a${s * 0.08} ${s * 0.08} 0 0 1 ${s * 0.08} ${-s * 0.08} Z`, fill: col }, p); }
function iconInstitution(p, s, col) { const gr = g(p);
  el('path', { d: `M${-s * 0.5} ${-s * 0.2} L0 ${-s * 0.5} L${s * 0.5} ${-s * 0.2} Z`, fill: col }, gr);
  for (let i = 0; i < 4; i++) el('rect', { x: -s * 0.4 + i * s * 0.25, y: -s * 0.14, width: s * 0.1, height: s * 0.5, fill: col }, gr);
  el('rect', { x: -s * 0.52, y: s * 0.4, width: s * 1.04, height: s * 0.1, fill: col }, gr); return gr; }
function iconCheck(p, s, col) { return el('path', { d: `M${-s * 0.36} 0 L${-s * 0.1} ${s * 0.26} L${s * 0.38} ${-s * 0.26}`, fill: 'none', stroke: col, 'stroke-width': s * 0.14, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, p); }
function iconCross(p, s, col) { return el('path', { d: `M${-s * 0.3} ${-s * 0.3} L${s * 0.3} ${s * 0.3} M${s * 0.3} ${-s * 0.3} L${-s * 0.3} ${s * 0.3}`, fill: 'none', stroke: col, 'stroke-width': s * 0.13, 'stroke-linecap': 'round' }, p); }
function iconKey(p, s, col) { const gr = g(p);
  el('circle', { cx: -s * 0.22, cy: 0, r: s * 0.2, fill: 'none', stroke: col, 'stroke-width': sw(s, 0.11) }, gr);
  el('path', { d: `M${-s * 0.02} 0 H${s * 0.46} M${s * 0.3} 0 V${s * 0.16} M${s * 0.42} 0 V${s * 0.12}`, fill: 'none', stroke: col, 'stroke-width': sw(s, 0.11), 'stroke-linecap': 'round' }, gr); return gr; }
function iconMail(p, s, col, siegel) { const gr = g(p);
  el('rect', { x: -s * 0.46, y: -s * 0.3, width: s * 0.92, height: s * 0.6, rx: s * 0.06, fill: 'none', stroke: col, 'stroke-width': sw(s) }, gr);
  el('path', { d: `M${-s * 0.42} ${-s * 0.24} L0 ${s * 0.06} L${s * 0.42} ${-s * 0.24}`, fill: 'none', stroke: col, 'stroke-width': sw(s), 'stroke-linejoin': 'round' }, gr);
  if (siegel) el('circle', { cx: 0, cy: s * 0.1, r: s * 0.13, fill: col }, gr); return gr; }
function iconCalendar(p, s, col) { const gr = g(p);
  el('rect', { x: -s * 0.42, y: -s * 0.34, width: s * 0.84, height: s * 0.76, rx: s * 0.08, fill: 'none', stroke: col, 'stroke-width': sw(s) }, gr);
  el('rect', { x: -s * 0.42, y: -s * 0.34, width: s * 0.84, height: s * 0.2, rx: s * 0.06, fill: col }, gr);
  for (const x of [-0.22, 0.22]) el('rect', { x: s * x - s * 0.04, y: -s * 0.46, width: s * 0.08, height: s * 0.2, rx: s * 0.04, fill: col }, gr);
  for (let r = 0; r < 2; r++) for (let c = 0; c < 3; c++) el('rect', { x: -s * 0.27 + c * s * 0.21, y: -s * 0.04 + r * s * 0.2, width: s * 0.12, height: s * 0.1, rx: s * 0.02, fill: col }, gr); return gr; }
function iconClock(p, s, col) { const gr = g(p);
  el('circle', { r: s * 0.42, fill: 'none', stroke: col, 'stroke-width': sw(s) }, gr);
  el('path', { d: `M0 ${-s * 0.24} V0 L${s * 0.18} ${s * 0.12}`, fill: 'none', stroke: col, 'stroke-width': sw(s), 'stroke-linecap': 'round' }, gr); return gr; }
function iconBook(p, s, col) { const gr = g(p);
  el('rect', { x: -s * 0.34, y: -s * 0.44, width: s * 0.68, height: s * 0.88, rx: s * 0.05, fill: 'none', stroke: col, 'stroke-width': sw(s) }, gr);
  el('rect', { x: -s * 0.34, y: -s * 0.44, width: s * 0.14, height: s * 0.88, fill: col }, gr);
  el('rect', { x: -s * 0.08, y: -s * 0.2, width: s * 0.3, height: s * 0.07, fill: col }, gr); return gr; }
function iconPara(p, s, col) { return T(p, 0, s * 0.34, '§', { size: s * 0.95, weight: 700, fill: col, anchor: 'middle' }); }
function iconEuro(p, s, col) { return T(p, 0, s * 0.32, '€', { size: s * 0.9, weight: 700, fill: col, anchor: 'middle' }); }
function iconPhone(p, s, col) { const gr = g(p);
  el('rect', { x: -s * 0.24, y: -s * 0.44, width: s * 0.48, height: s * 0.88, rx: s * 0.08, fill: 'none', stroke: col, 'stroke-width': sw(s) }, gr);
  el('rect', { x: -s * 0.08, y: s * 0.3, width: s * 0.16, height: s * 0.05, rx: s * 0.02, fill: col }, gr); return gr; }
function iconDoc(p, s, col) { const gr = g(p);
  el('path', { d: `M${-s * 0.32} ${-s * 0.44} H${s * 0.14} L${s * 0.32} ${-s * 0.26} V${s * 0.44} H${-s * 0.32} Z`, fill: 'none', stroke: col, 'stroke-width': sw(s), 'stroke-linejoin': 'round' }, gr);
  for (let i = 0; i < 3; i++) el('rect', { x: -s * 0.18, y: -s * 0.1 + i * s * 0.16, width: s * (0.36 - i * 0.06), height: s * 0.06, rx: s * 0.03, fill: col }, gr); return gr; }
function iconFolder(p, s, col) { return el('path', { d: `M${-s * 0.46} ${-s * 0.3} H${-s * 0.12} L${-s * 0.02} ${-s * 0.18} H${s * 0.46} V${s * 0.34} H${-s * 0.46} Z`, fill: col }, p); }
function iconWarn(p, s, col) { const gr = g(p);
  el('path', { d: `M0 ${-s * 0.42} L${s * 0.46} ${s * 0.38} H${-s * 0.46} Z`, fill: 'none', stroke: col, 'stroke-width': sw(s), 'stroke-linejoin': 'round' }, gr);
  el('rect', { x: -s * 0.04, y: -s * 0.14, width: s * 0.08, height: s * 0.28, rx: s * 0.03, fill: col }, gr); el('circle', { cx: 0, cy: s * 0.26, r: s * 0.05, fill: col }, gr); return gr; }
function iconPen(p, s, col) { const gr = g(p, { transform: 'rotate(45)' });
  el('rect', { x: -s * 0.08, y: -s * 0.46, width: s * 0.16, height: s * 0.7, rx: s * 0.04, fill: col }, gr);
  el('path', { d: `M${-s * 0.08} ${s * 0.26} L0 ${s * 0.44} L${s * 0.08} ${s * 0.26} Z`, fill: col }, gr); return gr; }
function iconGlobe(p, s, col) { const gr = g(p);
  el('circle', { r: s * 0.42, fill: 'none', stroke: col, 'stroke-width': sw(s, 0.08) }, gr);
  el('ellipse', { rx: s * 0.18, ry: s * 0.42, fill: 'none', stroke: col, 'stroke-width': sw(s, 0.08) }, gr);
  el('path', { d: `M${-s * 0.42} 0 H${s * 0.42} M${-s * 0.36} ${-s * 0.2} H${s * 0.36} M${-s * 0.36} ${s * 0.2} H${s * 0.36}`, stroke: col, 'stroke-width': sw(s, 0.06) }, gr); return gr; }
function iconMegaphone(p, s, col) { const gr = g(p);
  el('path', { d: `M${-s * 0.4} ${-s * 0.12} L${s * 0.26} ${-s * 0.38} V${s * 0.38} L${-s * 0.4} ${s * 0.12} Z`, fill: col }, gr);
  el('rect', { x: -s * 0.3, y: s * 0.1, width: s * 0.12, height: s * 0.26, rx: s * 0.04, fill: col }, gr);
  el('path', { d: `M${s * 0.36} ${-s * 0.18} Q${s * 0.48} 0 ${s * 0.36} ${s * 0.18}`, fill: 'none', stroke: col, 'stroke-width': sw(s, 0.08), 'stroke-linecap': 'round' }, gr); return gr; }
function iconGroup(p, s, col) { const gr = g(p);
  [[-0.26, 0.82], [0.26, 0.82], [0, 1]].forEach(([x, k]) => { const h = g(gr, { transform: `translate(${s * x} ${s * 0.06 * (1 - k) * 4})` }); iconPerson(h, s * 0.62 * k, col); }); return gr; }
function iconPulse(p, s, col) { return el('path', { d: `M${-s * 0.46} 0 H${-s * 0.2} L${-s * 0.1} ${-s * 0.3} L${s * 0.04} ${s * 0.3} L${s * 0.14} 0 H${s * 0.46}`, fill: 'none', stroke: col, 'stroke-width': sw(s, 0.1), 'stroke-linejoin': 'round', 'stroke-linecap': 'round' }, p); }
function iconId(p, s, col) { const gr = g(p);
  el('rect', { x: -s * 0.46, y: -s * 0.3, width: s * 0.92, height: s * 0.6, rx: s * 0.07, fill: 'none', stroke: col, 'stroke-width': sw(s) }, gr);
  el('circle', { cx: -s * 0.2, cy: -s * 0.04, r: s * 0.1, fill: col }, gr); el('path', { d: `M${-s * 0.34} ${s * 0.2} Q${-s * 0.2} ${s * 0.02} ${-s * 0.06} ${s * 0.2} Z`, fill: col }, gr);
  for (let i = 0; i < 2; i++) el('rect', { x: s * 0.04, y: -s * 0.1 + i * s * 0.16, width: s * (0.3 - i * 0.08), height: s * 0.07, rx: s * 0.03, fill: col }, gr); return gr; }
function iconCalc(p, s, col) { const gr = g(p);
  el('rect', { x: -s * 0.32, y: -s * 0.44, width: s * 0.64, height: s * 0.88, rx: s * 0.07, fill: 'none', stroke: col, 'stroke-width': sw(s) }, gr);
  el('rect', { x: -s * 0.2, y: -s * 0.32, width: s * 0.4, height: s * 0.18, rx: s * 0.03, fill: col }, gr);
  for (let r = 0; r < 3; r++) for (let c = 0; c < 3; c++) el('rect', { x: -s * 0.2 + c * s * 0.15, y: -s * 0.04 + r * s * 0.14, width: s * 0.09, height: s * 0.08, rx: s * 0.02, fill: col }, gr); return gr; }
function iconSearch(p, s, col) { const gr = g(p);
  el('circle', { cx: -s * 0.08, cy: -s * 0.08, r: s * 0.26, fill: 'none', stroke: col, 'stroke-width': sw(s, 0.1) }, gr);
  el('path', { d: `M${s * 0.12} ${s * 0.12} L${s * 0.4} ${s * 0.4}`, stroke: col, 'stroke-width': sw(s, 0.13), 'stroke-linecap': 'round' }, gr); return gr; }
function iconCycle(p, s, col) { const gr = g(p); const r = s * 0.32;
  el('path', { d: `M${r} 0 A${r} ${r} 0 0 1 ${-r * 0.7} ${r * 0.7}`, fill: 'none', stroke: col, 'stroke-width': sw(s, 0.1), 'stroke-linecap': 'round' }, gr);
  el('path', { d: `M${-r} 0 A${r} ${r} 0 0 1 ${r * 0.7} ${-r * 0.7}`, fill: 'none', stroke: col, 'stroke-width': sw(s, 0.1), 'stroke-linecap': 'round' }, gr);
  el('path', { d: `M${r * 0.7 - s * 0.14} ${-r * 0.7 - s * 0.08} L${r * 0.7 + s * 0.04} ${-r * 0.7} L${r * 0.7 - s * 0.06} ${-r * 0.7 + s * 0.16}`, fill: 'none', stroke: col, 'stroke-width': sw(s, 0.09), 'stroke-linejoin': 'round' }, gr);
  el('path', { d: `M${-r * 0.7 + s * 0.14} ${r * 0.7 + s * 0.08} L${-r * 0.7 - s * 0.04} ${r * 0.7} L${-r * 0.7 + s * 0.06} ${r * 0.7 - s * 0.16}`, fill: 'none', stroke: col, 'stroke-width': sw(s, 0.09), 'stroke-linejoin': 'round' }, gr); return gr; }
function iconQuestion(p, s, col) { const gr = g(p); iconChat(gr, s, col); T(gr, 0, s * 0.12, '?', { size: s * 0.5, weight: 800, fill: C.ground, anchor: 'middle' }); return gr; }
function iconGavel(p, s, col) { const gr = g(p, { transform: 'rotate(-35)' });
  el('rect', { x: -s * 0.3, y: -s * 0.34, width: s * 0.6, height: s * 0.24, rx: s * 0.05, fill: col }, gr);
  el('rect', { x: -s * 0.05, y: -s * 0.12, width: s * 0.1, height: s * 0.56, rx: s * 0.04, fill: col }, gr); return gr; }
function iconCert(p, s, col) { const gr = g(p);
  el('rect', { x: -s * 0.4, y: -s * 0.36, width: s * 0.8, height: s * 0.6, rx: s * 0.04, fill: 'none', stroke: col, 'stroke-width': sw(s) }, gr);
  for (let i = 0; i < 2; i++) el('rect', { x: -s * 0.26, y: -s * 0.2 + i * s * 0.14, width: s * (0.5 - i * 0.14), height: s * 0.06, rx: s * 0.03, fill: col }, gr);
  el('circle', { cx: s * 0.18, cy: s * 0.24, r: s * 0.14, fill: col }, gr);
  el('path', { d: `M${s * 0.1} ${s * 0.34} L${s * 0.06} ${s * 0.5} L${s * 0.18} ${s * 0.44} L${s * 0.3} ${s * 0.5} L${s * 0.26} ${s * 0.34}`, fill: col }, gr); return gr; }
function iconFlip(p, s, col) { const gr = g(p);
  el('rect', { x: -s * 0.36, y: -s * 0.44, width: s * 0.72, height: s * 0.56, rx: s * 0.04, fill: 'none', stroke: col, 'stroke-width': sw(s) }, gr);
  el('path', { d: `M0 ${s * 0.12} V${s * 0.3} M0 ${s * 0.18} L${-s * 0.26} ${s * 0.46} M0 ${s * 0.18} L${s * 0.26} ${s * 0.46}`, stroke: col, 'stroke-width': sw(s), 'stroke-linecap': 'round' }, gr);
  el('path', { d: `M${-s * 0.22} ${-s * 0.06} L${-s * 0.06} ${-s * 0.2} L${s * 0.06} ${-s * 0.1} L${s * 0.22} ${-s * 0.3}`, fill: 'none', stroke: col, 'stroke-width': sw(s, 0.08), 'stroke-linejoin': 'round' }, gr); return gr; }
function iconList(p, s, col) { const gr = g(p);
  for (let i = 0; i < 3; i++) { el('circle', { cx: -s * 0.32, cy: -s * 0.26 + i * s * 0.26, r: s * 0.06, fill: col }, gr); el('rect', { x: -s * 0.18, y: -s * 0.3 + i * s * 0.26, width: s * 0.58, height: s * 0.08, rx: s * 0.04, fill: col }, gr); } return gr; }
function iconWave(p, s, col) { const gr = g(p);
  [0.2, 0.5, 0.9, 0.6, 1, 0.45, 0.75, 0.3].forEach((h, i) => el('rect', { x: -s * 0.44 + i * s * 0.12, y: -s * 0.4 * h, width: s * 0.06, height: s * 0.8 * h, rx: s * 0.03, fill: col }, gr)); return gr; }
function iconDoor(p, s, col) { const gr = g(p);
  el('rect', { x: -s * 0.28, y: -s * 0.46, width: s * 0.56, height: s * 0.92, rx: s * 0.03, fill: 'none', stroke: col, 'stroke-width': sw(s) }, gr);
  el('circle', { cx: s * 0.14, cy: s * 0.04, r: s * 0.05, fill: col }, gr); return gr; }
function iconLink(p, s, col) { const gr = g(p, { transform: 'rotate(-35)' });
  el('rect', { x: -s * 0.46, y: -s * 0.14, width: s * 0.52, height: s * 0.28, rx: s * 0.14, fill: 'none', stroke: col, 'stroke-width': sw(s) }, gr);
  el('rect', { x: -s * 0.06, y: -s * 0.14, width: s * 0.52, height: s * 0.28, rx: s * 0.14, fill: 'none', stroke: col, 'stroke-width': sw(s) }, gr); return gr; }
function iconTruck(p, s, col) { const gr = g(p);
  el('rect', { x: -s * 0.46, y: -s * 0.28, width: s * 0.58, height: s * 0.46, rx: s * 0.04, fill: col }, gr);
  el('path', { d: `M${s * 0.14} ${-s * 0.12} H${s * 0.32} L${s * 0.46} ${s * 0.04} V${s * 0.18} H${s * 0.14} Z`, fill: col }, gr);
  for (const x of [-0.28, 0.28]) el('circle', { cx: s * x, cy: s * 0.24, r: s * 0.1, fill: C.ground, stroke: col, 'stroke-width': sw(s, 0.07) }, gr); return gr; }
function iconBriefcase(p, s, col) { const gr = g(p);
  el('rect', { x: -s * 0.44, y: -s * 0.2, width: s * 0.88, height: s * 0.6, rx: s * 0.07, fill: col }, gr);
  el('path', { d: `M${-s * 0.14} ${-s * 0.2} V${-s * 0.34} H${s * 0.14} V${-s * 0.2}`, fill: 'none', stroke: col, 'stroke-width': sw(s), 'stroke-linejoin': 'round' }, gr); return gr; }
function iconContract(p, s, col) { const gr = iconDoc(p, s, col); el('path', { d: `M${-s * 0.18} ${s * 0.32} q${s * 0.06} ${-s * 0.1} ${s * 0.12} 0 t${s * 0.12} 0`, fill: 'none', stroke: col, 'stroke-width': sw(s, 0.06) }, gr); return gr; }
const ICON = { betrieb: iconBuilding, privat: iconPerson, unklar: iconUnknown };
function ikon(p, name, x, y, s, col) { const gr = g(p, { transform: `translate(${x} ${y})` }); ({ building: iconBuilding, person: iconPerson, unknown: iconUnknown, spark: iconSpark, translate: iconTranslate, chat: iconChat, institution: iconInstitution, check: iconCheck, cross: iconCross, key: iconKey, mail: iconMail, sealed: (q, z, c) => iconMail(q, z, c, true), calendar: iconCalendar, clock: iconClock, book: iconBook, para: iconPara, euro: iconEuro, phone: iconPhone, doc: iconDoc, folder: iconFolder, warn: iconWarn, pen: iconPen, globe: iconGlobe, megaphone: iconMegaphone, group: iconGroup, pulse: iconPulse, id: iconId, calc: iconCalc, search: iconSearch, cycle: iconCycle, question: iconQuestion, gavel: iconGavel, cert: iconCert, flip: iconFlip, list: iconList, wave: iconWave, door: iconDoor, link: iconLink, truck: iconTruck, briefcase: iconBriefcase, contract: iconContract })[name](gr, s, col); return gr; }

// Kategorie-Marker wie auf der Website: Fakt Quadrat, Auslegung Raute, Unsicher Halbkreis, Lücke gestrichelter Kreis
const MARKFARBE = { fakt: C.blue, auslegung: C.purple, unsicher: C.amber, luecke: C.red };
const MARKWORT = { fakt: { de: 'FAKT', en: 'FACT' }, auslegung: { de: 'AUSLEGUNG', en: 'INTERPRETATION' }, unsicher: { de: 'UNSICHER', en: 'UNCERTAIN' }, luecke: { de: 'LÜCKE', en: 'GAP' } };
function markerShape(p, kind, s) {
  if (kind === 'fakt') return el('rect', { x: -s / 2, y: -s / 2, width: s, height: s, fill: C.blue }, p);
  if (kind === 'auslegung') return el('rect', { x: -s * 0.38, y: -s * 0.38, width: s * 0.76, height: s * 0.76, fill: C.purple, transform: 'rotate(45)' }, p);
  if (kind === 'unsicher') { const gr = g(p); el('circle', { r: s * 0.5, fill: 'none', stroke: C.amber, 'stroke-width': s * 0.12 }, gr); el('path', { d: `M0 ${-s * 0.5} A${s * 0.5} ${s * 0.5} 0 0 0 0 ${s * 0.5} Z`, fill: C.amber }, gr); return gr; }
  return el('circle', { r: s * 0.46, fill: 'none', stroke: C.red, 'stroke-width': s * 0.14, 'stroke-dasharray': `${s * 0.24} ${s * 0.16}` }, p);
}
// Statuslampe (grün, bernstein, rot) mit Ring
function lampe(p, x, y, r, col) { const gr = g(p, { transform: `translate(${x} ${y})` }); const glow = el('circle', { r: r * 4, fill: col === C.red ? 'url(#gRed)' : col === C.green ? 'url(#gGreen)' : 'url(#gAmber)' }, gr); const c = el('circle', { r, fill: col }, gr); el('circle', { r: r + 5, fill: 'none', stroke: col, 'stroke-width': 2, opacity: 0.5 }, gr); return { g: gr, glow, c }; }

// ================= Papier, Etiketten, Karten =================
// Blatt mit Kopfzeile; Mitte 0,0. Gibt Gruppe und die linke Innenkante zurück.
function blatt(p, o = {}) {
  const w = o.w || 480, h = o.h || 640, x0 = -w / 2, y0 = -h / 2, pad = o.pad || 40;
  const gr = g(p);
  if (o.back !== false) el('rect', { x: x0 + 14, y: y0 + 10, width: w, height: h, rx: 6, fill: C.paperBack }, gr);
  const sheet = el('rect', { x: x0, y: y0, width: w, height: h, rx: 6, fill: C.paper, filter: o.schatten === false ? '' : 'url(#shadow)' }, gr);
  let y = y0 + pad;
  if (o.kicker) { T(gr, x0 + pad, y + 8, o.kicker, { mono: 1, size: o.kSize || 15, fill: C.pMuted, ls: '0.08em' }); if (o.datum) T(gr, -x0 - pad, y + 8, o.datum, { mono: 1, size: o.kSize || 15, fill: C.pMuted, anchor: 'end', ls: '0.06em' }); el('rect', { x: x0 + pad, y: y + 22, width: w - 2 * pad, height: 1.5, fill: C.pLine }, gr); y += 40; }
  let titel = null;
  if (o.titel) { y += (o.tSize || 34) * 0.9; titel = TB(gr, x0 + pad, y, o.titel, { size: o.tSize || 34, weight: 800, fill: C.pInk, maxW: w - 2 * pad, lh: (o.tSize || 34) * 1.15 }); y += (titel.zeilen - 1) * (o.tSize || 34) * 1.15 + 18; }
  return { g: gr, sheet, x0, y0, w, h, pad, left: x0 + pad, right: -x0 - pad, y, titel };
}
// Platzhalterzeilen auf Papier
function linien(p, x, y, w, n, gap = 20, col = C.pBar, hgt = 9) { const out = []; for (let i = 0; i < n; i++) out.push(el('rect', { x, y: y + i * gap, width: w * (i === n - 1 ? 0.62 : 0.86 + ((i * 37) % 14) / 100), height: hgt, rx: hgt / 2, fill: col }, p)); return out; }
// Etikett (Pille) mit optionalem Symbol; Mitte 0,0; o.col Rand und Symbol, o.fill Grund, o.gestrichelt
function pille(p, text, o = {}) {
  const gr = g(p); const size = o.size || 22, h = o.h || size * 2.3, col = o.col || C.muted;
  const r = el('rect', { x: 0, y: -h / 2, width: 10, height: h, rx: h / 2, fill: o.fill || C.raised, stroke: col, 'stroke-width': o.sw || 2.5 }, gr);
  if (o.gestrichelt) r.setAttribute('stroke-dasharray', '9 6');
  let x = h * 0.42;
  if (o.icon) { const ic = g(gr, { transform: `translate(${x + size * 0.55} 0)` }); (typeof o.icon === 'function' ? o.icon : (q, s, c) => ikon(q, o.icon, 0, 0, s, c))(ic, size * 1.15, o.iconCol || col); x += size * 1.5; }
  if (o.marke) { const m = g(gr, { transform: `translate(${x + size * 0.45} 0)` }); markerShape(m, o.marke, size * 0.75); x += size * 1.25; }
  const tx = T(gr, x, size * 0.36, text, { mono: o.mono !== false, size, fill: o.tcol || C.ink, weight: o.weight, ls: o.ls || (o.mono !== false ? '0.06em' : null) });
  const w = x + breite(tx) + h * 0.42; r.setAttribute('width', w.toFixed(1));
  gr.w = w; gr.h = h;
  const inner = g(p); inner.appendChild(r); while (gr.firstChild) inner.appendChild(gr.firstChild); // Reihenfolge erhalten
  p.removeChild(gr); const outer = g(p); const z = g(outer, { transform: `translate(${(-w / 2).toFixed(1)} 0)` }); z.appendChild(inner); outer.w = w; outer.h = h; return outer;
}
// Dunkle Karte (Bildschirmwelt)
function karte(p, x, y, w, h, o = {}) { const gr = g(p); el('rect', { x, y, width: w, height: h, rx: o.rx || 18, fill: o.fill || C.raised, stroke: o.stroke || C.edge, 'stroke-width': o.sw || 3, filter: o.schatten === false ? '' : 'url(#shadowS)', 'stroke-dasharray': o.gestrichelt ? '12 8' : '' }, gr); return gr; }
// Stempel (schräg), z. B. ERFUNDEN
function stempel(p, text, col = C.amber, size = 26) { const gr = g(p); const tx = T(gr, 0, size * 0.36, text, { mono: 1, size, fill: col, anchor: 'middle', ls: '0.14em' }); const w = breite(tx) + size * 1.4; el('rect', { x: -w / 2, y: -size * 0.95, width: w, height: size * 1.9, rx: 6, fill: 'none', stroke: col, 'stroke-width': 3 }, gr); gr.w = w; return gr; }
// Kachel mit Nummer
function kachel(p, text, col = C.blue, s = 72) { const gr = g(p); el('rect', { x: -s / 2, y: -s / 2, width: s, height: s, rx: s * 0.2, fill: col }, gr); T(gr, 0, s * 0.18, text, { size: s * 0.53, weight: 800, anchor: 'middle', fill: '#fff' }); return gr; }
// Häkchenkästchen auf Papier
function kaestchen(p, x, y, s = 22) { const gr = g(p, { transform: `translate(${x} ${y})` }); el('rect', { x: -s / 2, y: -s / 2, width: s, height: s, rx: 4, fill: 'none', stroke: C.pMuted, 'stroke-width': 2 }, gr); const h = g(gr); iconCheck(h, s * 1.1, C.blueDeep); return { g: gr, haken: h }; }

// ================= Figuren (ohne Gesicht; Rolle über Silhouette, Kleidung, Werkzeug) =================
function kopfHaar(head, haar) {
  if (haar === 'short') el('path', { d: 'M -33 4 A 33 33 0 0 1 31 -10 Q 12 -24 -6 -18 Q -24 -12 -33 4 Z', fill: HAIR }, head);
  if (haar === 'bun') { el('circle', { cx: -26, cy: -28, r: 15, fill: HAIR }, head); el('path', { d: 'M -33 8 A 33 33 0 0 1 29 -14 Q 2 -28 -20 -12 Q -30 -2 -33 8 Z', fill: HAIR }, head); }
  if (haar === 'long') { el('path', { d: 'M -36 34 Q -44 -10 -24 -28 Q 0 -44 26 -26 Q 40 -12 34 6 Q 14 -18 -6 -16 Q -22 -8 -22 30 Z', fill: HAIR }, head); }
  if (haar === 'curly') { for (const [x, y, r] of [[-22, -20, 14], [-4, -30, 15], [16, -26, 14], [28, -10, 11], [-30, -2, 11]]) el('circle', { cx: x, cy: y, r, fill: HAIR }, head); }
}
function seated(p, x, y, o) {
  const gr = g(p, { transform: `translate(${x} ${y})` });
  el('rect', { x: -88, y: -150, width: 16, height: 154, rx: 8, fill: '#17223a' }, gr);
  el('rect', { x: -92, y: 2, width: 116, height: 16, rx: 8, fill: '#17223a' }, gr);
  el('rect', { x: -40, y: 18, width: 12, height: 52, fill: '#131c30' }, gr);
  el('rect', { x: -76, y: 66, width: 84, height: 8, rx: 4, fill: '#131c30' }, gr);
  el('rect', { x: -22, y: -16, width: 122, height: 32, rx: 16, fill: PANTS }, gr);
  el('rect', { x: 80, y: -4, width: 30, height: 74, rx: 15, fill: PANTS }, gr);
  el('ellipse', { cx: 106, cy: 70, rx: 24, ry: 9, fill: SHOE }, gr);
  el('path', { d: 'M -50 6 L -45 -122 Q -41 -152 -12 -152 L 14 -152 Q 43 -152 43 -122 L 41 6 Z', fill: o.shirt }, gr);
  el('path', { d: 'M -14 -152 L 0 -132 L 14 -152 Z', fill: o.collar || '#d9e0ee', opacity: 0.85 }, gr);
  const head = g(gr);
  el('circle', { cx: 0, cy: 0, r: 33, fill: SKIN }, head);
  kopfHaar(head, o.hair);
  const arm = g(gr);
  el('line', { x1: 0, y1: 0, x2: 26, y2: 52, stroke: o.shirt, 'stroke-width': 26, 'stroke-linecap': 'round' }, arm);
  const fore = g(arm);
  el('line', { x1: 0, y1: 0, x2: 70, y2: -4, stroke: o.shirt, 'stroke-width': 22, 'stroke-linecap': 'round' }, fore);
  el('circle', { cx: 77, cy: -4, r: 12, fill: SKIN }, fore);
  const fig = { g: gr, head, arm, fore, x, y };
  pose(fig, 0, 0, 0); return fig;
}
function pose(fig, armA, foreA, headA) {
  fig.arm.setAttribute('transform', `translate(16 -124) rotate(${armA.toFixed(2)})`);
  fig.fore.setAttribute('transform', `translate(26 52) rotate(${foreA.toFixed(2)})`);
  fig.head.setAttribute('transform', `translate(0 -190) rotate(${headA.toFixed(2)})`);
}
// Stehende Figur. o: jacke, helm, streifen, haar, kappe, telefon (in der linken Hand), blatt (in der rechten Hand)
// Arme: Winkel in Grad, 0 = hängt gerade nach unten; positiv dreht im Uhrzeigersinn (Arm nach links vorne).
function stehend(p, x, y, o = {}) {
  const gr = g(p, { transform: `translate(${x} ${y}) scale(${o.skala || 1})` });
  const beinL = g(gr, { transform: 'translate(-14 -154)' }), beinR = g(gr, { transform: 'translate(14 -154)' });
  for (const b of [beinL, beinR]) { el('rect', { x: -11, y: 0, width: 21, height: 154, rx: 10, fill: o.hose || PANTS }, b); el('ellipse', { cx: -2, cy: 151, rx: 21, ry: 8, fill: SHOE }, b); }
  const armR = g(gr); const foreR = g(armR);
  el('line', { x1: 0, y1: 0, x2: 0, y2: 66, stroke: o.jacke, 'stroke-width': 24, 'stroke-linecap': 'round' }, armR);
  el('line', { x1: 0, y1: 0, x2: 0, y2: 52, stroke: o.jacke, 'stroke-width': 20, 'stroke-linecap': 'round' }, foreR);
  el('circle', { cx: 0, cy: 60, r: 12, fill: SKIN }, foreR);
  let blattG = null; if (o.blatt) { blattG = g(foreR, { transform: 'translate(10 78) rotate(-8)' }); el('rect', { x: -26, y: -34, width: 52, height: 68, rx: 3, fill: C.paper }, blattG); linien(blattG, -18, -22, 36, 4, 12, C.pBar2, 5); }
  el('path', { d: 'M -47 -142 L -45 -268 Q -43 -298 -14 -298 L 14 -298 Q 43 -298 45 -268 L 47 -142 Z', fill: o.jacke }, gr);
  if (o.streifen) { el('rect', { x: -46, y: -216, width: 92, height: 9, fill: '#cfd6e3', opacity: 0.7 }, gr); el('rect', { x: -46, y: -188, width: 92, height: 9, fill: '#cfd6e3', opacity: 0.7 }, gr); }
  if (o.kragen) el('path', { d: 'M -16 -298 L 0 -276 L 16 -298 Z', fill: o.kragen, opacity: 0.9 }, gr);
  const head = g(gr, { transform: 'translate(0 -336)' });
  el('circle', { r: 32, fill: SKIN }, head);
  if (o.helm) { el('path', { d: 'M -35 -2 A 35 35 0 0 1 35 -2 Z', fill: o.helmFarbe || '#e9eef8' }, head); el('rect', { x: -52, y: -7, width: 74, height: 9, rx: 4.5, fill: o.helmFarbe || '#e9eef8' }, head); }
  else if (o.kappe) { el('path', { d: 'M -32 -6 A 32 32 0 0 1 32 -6 Z', fill: o.kappe }, head); el('rect', { x: -56, y: -10, width: 40, height: 8, rx: 4, fill: o.kappe }, head); }
  else kopfHaar(head, o.haar || 'short');
  const armL = g(gr); const foreL = g(armL);
  el('line', { x1: 0, y1: 0, x2: 0, y2: 66, stroke: o.jacke, 'stroke-width': 24, 'stroke-linecap': 'round' }, armL);
  el('line', { x1: 0, y1: 0, x2: 0, y2: 52, stroke: o.jacke, 'stroke-width': 20, 'stroke-linecap': 'round' }, foreL);
  el('circle', { cx: 0, cy: 60, r: 11, fill: SKIN }, foreL);
  let glow = null, dim = null;
  if (o.telefon) {
    const phone = g(foreL, { transform: 'translate(-4 86) rotate(180)' });
    glow = el('circle', { r: 110, fill: 'url(#gBlue)' }, phone);
    el('rect', { x: -18, y: -31, width: 36, height: 62, rx: 7, fill: '#0f1626', stroke: '#3a4d75', 'stroke-width': 2.5 }, phone);
    el('rect', { x: -14, y: -26, width: 28, height: 50, rx: 4, fill: '#dfe7f7' }, phone);
    const ic = g(phone, { transform: 'translate(0 -4) rotate(180)' }); iconChat(ic, 18, C.blueDeep);
    dim = el('rect', { x: -14, y: -26, width: 28, height: 50, rx: 4, fill: '#0f1626' }, phone);
  }
  const fig = { g: gr, head, armL, foreL, armR, foreR, beinL, beinR, glow, dim, blatt: blattG, x, y, s: o.skala || 1 };
  arme(fig, o.telefon ? 18 : -6, o.telefon ? 131 : 0, -6, o.blatt ? -60 : 0, 0); return fig;
}
function arme(fig, aL, fL, aR, fR, kopf = 0) {
  fig.armL.setAttribute('transform', `translate(-30 -276) rotate(${aL.toFixed(2)})`); fig.foreL.setAttribute('transform', `translate(0 66) rotate(${fL.toFixed(2)})`);
  fig.armR.setAttribute('transform', `translate(30 -276) rotate(${aR.toFixed(2)})`); fig.foreR.setAttribute('transform', `translate(0 66) rotate(${fR.toFixed(2)})`);
  fig.head.setAttribute('transform', `translate(0 -336) rotate(${kopf.toFixed(2)})`);
}
// Gehen: Phase in Schritten, Ausschlag 0..1
function gehen(fig, phase, amp = 1) { const a = Math.sin(phase * Math.PI) * 18 * amp; fig.beinL.setAttribute('transform', `translate(-14 -154) rotate(${a.toFixed(2)})`); fig.beinR.setAttribute('transform', `translate(14 -154) rotate(${(-a).toFixed(2)})`); }
function stelle(fig, x, y, s, spiegel = false) { fig.g.setAttribute('transform', `translate(${x.toFixed(2)} ${y.toFixed(2)}) scale(${(spiegel ? -1 : 1) * (s || fig.s)} ${s || fig.s})`); }

// ================= Möbel und Räume =================
function tisch(p, x0, x1, y = 700) { el('rect', { x: x0, y, width: x1 - x0, height: 22, rx: 6, fill: C.desk }, p); el('rect', { x: x0 + 16, y: y + 22, width: 14, height: 126, fill: '#16203a' }, p); el('rect', { x: x1 - 30, y: y + 22, width: 14, height: 126, fill: '#16203a' }, p); }
function monitor(p, x, y, w, h, glyph) {
  const gr = g(p);
  const glow = el('ellipse', { cx: x + w / 2, cy: y + h / 2, rx: w * 1.15, ry: h * 1.35, fill: 'url(#gBlue)' }, gr);
  el('rect', { x: x + w / 2 - 6, y: y + h, width: 12, height: 26, fill: '#26344f' }, gr);
  el('rect', { x: x + w / 2 - 36, y: y + h + 22, width: 72, height: 6, rx: 3, fill: '#26344f' }, gr);
  el('rect', { x, y, width: w, height: h, rx: 10, fill: '#0f1626', stroke: C.edge, 'stroke-width': 4 }, gr);
  const screen = g(gr);
  el('rect', { x: x + 10, y: y + 10, width: w - 20, height: h - 20, rx: 6, fill: '#e3e9f5' }, screen);
  el('rect', { x: x + 10, y: y + 10, width: w - 20, height: 15, rx: 6, fill: '#c6d0e4' }, screen);
  for (let i = 0; i < 3; i++) el('circle', { cx: x + 20 + i * 9, cy: y + 17.5, r: 2.6, fill: '#8d99b2' }, screen);
  if (glyph) { const gl = g(screen, { transform: `translate(${x + 34} ${y + h / 2 + 8})` }); glyph(gl, 30, C.blueDeep); }
  const bars = [0.62, 0.48, 0.55].map((f, i) => el('rect', { x: x + 58, y: y + h / 2 - 8 + i * 13, width: (w - 76) * f, height: 7, rx: 3.5, fill: '#b8c3d9' }, screen));
  const dim = el('rect', { x: x + 10, y: y + 10, width: w - 20, height: h - 20, rx: 6, fill: '#0f1626' }, gr);
  return { g: gr, glow, dim, screen, bars, x, y, w, h };
}
function bildschirm(m, k) { O(m.dim, 0.78 * (1 - k)); O(m.glow, 0.15 + 0.85 * k); }
function raum(p, x, y, w, h, label) { el('rect', { x, y, width: w, height: h, rx: 22, fill: C.wall }, p); el('rect', { x, y: y + h - 14, width: w, height: 14, rx: 5, fill: C.floor }, p); if (label) T(p, x + 30, y + 44, label, { mono: 1, size: 18, fill: C.dim, ls: '0.1em' }); }
function ordnerRegal(p, x, y, n = 11) { el('rect', { x, y: y + 76, width: n * 32 + 20, height: 8, rx: 4, fill: '#1c2943' }, p); for (let i = 0; i < n; i++) el('rect', { x: x + 12 + i * 32, y: y + (i % 3) * 6, width: 24, height: 76 - (i % 3) * 6, rx: 3, fill: i === 6 ? '#3a4d75' : (i % 2 ? '#1f2c47' : '#24324f') }, p); }
function fenster2(p, x, y, w = 250, h = 160) { el('rect', { x, y, width: w, height: h, rx: 8, fill: '#0a111f', stroke: '#1f2c47', 'stroke-width': 6 }, p); el('rect', { x: x + w / 2 - 3, y, width: 6, height: h, fill: '#1f2c47' }, p); }
function tuer(p, x, y, w = 176, h = 378) { const gr = g(p); el('rect', { x, y, width: w, height: h, rx: 6, fill: '#0c1424', stroke: '#1f2c47', 'stroke-width': 6 }, gr); el('circle', { cx: x + w - 28, cy: y + h / 2, r: 7, fill: '#2a3858' }, gr); return gr; }
function schrank(p, x, y, w = 200, h = 300) { const gr = g(p); el('rect', { x, y, width: w, height: h, rx: 6, fill: '#121c30', stroke: '#22304c', 'stroke-width': 4 }, gr); const laden = []; for (let i = 0; i < 3; i++) { const l = g(gr); el('rect', { x: x + 12, y: y + 14 + i * (h - 28) / 3, width: w - 24, height: (h - 28) / 3 - 10, rx: 4, fill: '#18243c', stroke: '#2a3858', 'stroke-width': 2 }, l); el('rect', { x: x + w / 2 - 22, y: y + 14 + i * (h - 28) / 3 + ((h - 28) / 3 - 10) / 2 - 4, width: 44, height: 8, rx: 4, fill: '#3a4d75' }, l); laden.push(l); } return { g: gr, laden }; }

// ================= Einblendungen =================
const KOEPFE = [], MARKEN = [], HINWEISE = [];
let HUDDIM = 0; const dimmen = (v) => { HUDDIM = Math.max(HUDDIM, clamp(v)); };
// Kopfzeile oben links: Kicker und Titel, sichtbar von ab bis bis
function kopf(ab, bis, kicker, titel) {
  const gr = g(HUD); O(gr, 0);
  T(gr, 96, 104, kicker, { mono: 1, size: 24, fill: C.blue, ls: '0.14em' });
  if (titel) T(gr, 94, 166, titel, { size: 60, weight: 800 });
  KOEPFE.push({ g: gr, ab, bis });
}
// Marker unten links mit Quellenleiste; quelle optional ({de, en}); bis = Ende des Absatzes
function marke(ab, bis, art, quelle) {
  const gr = g(HUD); O(gr, 0);
  let bandTop = 1024;
  if (quelle) {
    const band = g(gr);
    const bg = el('rect', { x: 0, y: 952, width: W, height: 72, fill: 'rgba(18,27,47,0.96)' }, band);
    const ln = el('rect', { x: 0, y: 952, width: W, height: 1.5, fill: 'rgba(226,232,246,0.14)' }, band);
    const pre = L({ de: 'Quelle: ', en: 'Source: ' });
    const tx = TB(band, 96, 998, pre + L(quelle), { mono: 1, size: 22, fill: C.muted, maxW: 1728, lh: 30 });
    if (tx.zeilen > 1) { const extra = (tx.zeilen - 1) * 30; bg.setAttribute('y', 952 - extra); bg.setAttribute('height', 72 + extra); ln.setAttribute('y', 952 - extra); tx.setAttribute('y', 998 - extra); [...tx.childNodes].forEach((n) => n.setAttribute && n.getAttribute('dy') === '0' && 0); bandTop = 952 - extra; }
    else bandTop = 952;
  }
  const chip = g(gr);
  const cy = bandTop - 51;
  const r = el('rect', { x: 96, y: cy - 27, width: 10, height: 54, rx: 27, fill: 'rgba(18,27,47,0.94)', stroke: 'rgba(226,232,246,0.16)', 'stroke-width': 1.5 }, chip);
  const m = g(chip, { transform: `translate(128 ${cy})` }); markerShape(m, art, 18);
  const tx = T(chip, 150, cy + 9, MARKWORT[art], { mono: 1, size: 24, fill: MARKFARBE[art], ls: '0.12em' });
  r.setAttribute('width', (breite(tx) + 88).toFixed(0));
  MARKEN.push({ g: gr, chip, ab, bis, art });
}
// Freie Einblendung im HUD (z. B. Hinweiszeile im Einstieg)
function hinweis(ab, bis, baue) { const gr = g(HUD); O(gr, 0); baue(gr); HINWEISE.push({ g: gr, ab, bis }); return gr; }
let OBEN_RECHTS = null;
function hudGrund() { OBEN_RECHTS = T(HUD, 1824, 102, { de: 'KI-GENERIERT · SYNTHETISCHE STIMME', en: 'AI-GENERATED · SYNTHETIC VOICE' }, { mono: 1, size: 18, fill: C.muted, anchor: 'end', ls: '0.12em' }); }
function hudZeichnen(t) {
  for (const k of KOEPFE) { const a = fenster(t, k.ab, 0.45, k.bis, 0.35); O(k.g, a * (1 - 0.9 * HUDDIM)); tr(k.g, 0, (1 - P(t, k.ab, 0.45, E.out)) * 12); }
  for (const m of MARKEN) { const a = fenster(t, m.ab, 0.4, m.bis, 0.35); O(m.g, a); tr(m.chip, (1 - P(t, m.ab, 0.4, E.out)) * -20, 0); }
  for (const h of HINWEISE) O(h.g, fenster(t, h.ab, 0.4, h.bis, 0.4));
  if (OBEN_RECHTS) O(OBEN_RECHTS, 1 - 0.6 * HUDDIM);
}

// Ton-Cues für die Tonebene des Composers (03.11.2026): klang(t, name, {dauer, laut}) sammelt Geräuschstellen
const KLANG = []; window.KLANG = KLANG;
function klang(t, name, o = {}) { if (isFinite(t)) KLANG.push({ t, name, dauer: o.dauer || 0, laut: o.laut || 1 }); }

// ================= Ablauf =================
const AKTE = [];
function akt(def) { AKTE.push(def); return def; }
let NACHLAUF = 0, ENDE = DAUER;
function aufbauen() { hudGrund(); for (const a of AKTE) { a.buehnen = a.buehnen || []; a.bauen(); } SCHNITT.sort((a, b) => a.ab - b.ab); ENDE = DAUER + NACHLAUF; window.ENDE = ENDE; }
function render(t) {
  HUDDIM = 0;
  compose(t);
  for (const a of AKTE) if (a.buehnen.some((b) => b.vis)) a.zeichnen(t);
  hudZeichnen(t);
  O(FADE, Math.max(1 - P(t, 0, 0.6, E.out), P(t, ENDE - 0.8, 0.8, E.in)));
}
window.render = render;

// Markenzeichen von Scutoria (Schild mit Kreuzlinien, aus site/public/scutum-mark.svg); Mitte 0,0, Breite etwa s
function zeichen(p, s, col = C.blue, strich = 1.8) {
  const gr = g(p, { transform: `scale(${(s / 24).toFixed(4)}) translate(-12 -12)` });
  const a = { fill: 'none', stroke: col, 'stroke-width': strich, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' };
  el('path', { d: 'M12 2.5l6.5 3.2v11.6L12 21.5l-6.5-4.2V5.7L12 2.5z', ...a }, gr); el('path', { d: 'M12 6v12', ...a }, gr); el('path', { d: 'M8.5 12h7', ...a }, gr);
  return gr;
}

// Belegter Absatz: nimmt den nächsten Eintrag aus window.MARKEN_DATEN (erzeugt von marken.py), sucht den Absatzanfang
// als Wortanker (schiebt die Lesestelle weiter) und das Ende vor dem nächsten Absatz; setzt Marker und Quellenleiste.
let MARK_I = 0;
function belegt(opt = {}) {
  const d = (window.MARKEN_DATEN || [])[MARK_I++];
  if (!d) { ANKER_FEHLT.push('kein Eintrag in MARKEN_DATEN'); return { s: 0, e: 0, art: 'fakt' }; }
  const a = cue(d.start);
  let e = DAUER;
  if (L(d.weiter)) { const n = cue(d.weiter, { halten: true }); e = Math.min(stilleVor(n.s) + 0.6, n.s - 0.05); }
  if (opt.bis) e = opt.bis;
  marke(a.s - 0.15, e, d.art, d.quelle);
  return { s: a.s, e, art: d.art };
}
// Anfang eines Absatzes (Index wie in marken.py) ohne die Lesestelle zu verschieben
function absatz(i) { return cue((window.ABSAETZE || [])[i] || '', { halten: true }).s; }
// Spricht die Stimme gerade? 0..1, weich an den Wortgrenzen (für Wellenformen)
function spricht(t) { let lo = 0, hi = WORT.length - 1; while (lo < hi) { const m = (lo + hi + 1) >> 1; if (WORT[m].s <= t) lo = m; else hi = m - 1; } const w = WORT[lo]; if (!w) return 0; return t >= w.s - 0.04 && t <= w.e + 0.06 ? 1 : clamp(1 - (t - w.e) / 0.25); }

// Freies Angebot in der Mitte des Videos (Entscheidung Stefan, 30. Oktober 2026; VORLAGE-PARALLEL.md, Abschnitt 3a):
// Kapsel rechts oben unter „SYNTHETISCHE STIMME“, rechtsbündig an x 1824, Kicker „FREI AUF SCUTORIA.COM“, darunter der Pfad,
// Symbol und blauer Rand. Einmal je Video, am Wortanker, etwa 7 Sekunden.
function freiesAngebot(ab, pfad, o = {}) {
  const dauer = o.dauer || 7;
  return hinweis(ab, ab + dauer, (gr) => {
    const kick = T(gr, 0, 0, { de: 'FREI AUF SCUTORIA.COM', en: 'FREE ON SCUTORIA.COM' }, { mono: 1, size: 18, fill: C.blue, ls: '0.12em' });
    const pt = T(gr, 0, 0, pfad, { mono: 1, size: 22, fill: C.ink });
    const w = Math.max(breite(kick), breite(pt)) + 100, h = 84, x0 = 1824 - w, y0 = 126;
    const r = el('rect', { x: x0, y: y0, width: w, height: h, rx: 20, fill: 'rgba(18,27,47,0.94)', stroke: C.blue, 'stroke-width': 2.5 });
    gr.insertBefore(r, gr.firstChild);
    ikon(gr, o.icon || 'doc', x0 + 38, y0 + h / 2, 34, C.blue);
    kick.setAttribute('x', x0 + 72); kick.setAttribute('y', y0 + 34);
    pt.setAttribute('x', x0 + 72); pt.setAttribute('y', y0 + 64);
  });
}
