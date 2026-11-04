// Gemeinsame Bausteine für „Was tun Sie? Zwei Fälle“: Gabel A/B/C (bauGabel) und der Fall-Akt mit vier Bühnen (fallAkt).
// Je Video eine Datei mit den Fall-Daten (faelle.js für Video 01, faelle-02.js für Video 02); dort steht auch QUELLEN_F
// (Quellenleiste der Marker, Schlüssel aus den Marken der Fälle). Geladen vor den Fall-Dateien (plan: welt_libs).

// Gabel A/B/C auf einer Bühne; gibt Wege, Karten und Endpunkte zurück
function bauGabel(b, optionen) {
  const start = [300, 560];
  const ziele = [[1180, 300], [1180, 560], [1180, 820]];
  const out = { start, ziele, wege: [], karten: [], enden: [] };
  const s = g(b.cam, { transform: `translate(${start[0]} ${start[1]})` });
  el('circle', { r: 120, fill: 'url(#gBlue)' }, s);
  el('circle', { r: 46, fill: C.surface, stroke: C.blue, 'stroke-width': 4 }, s);
  ikon(s, 'person', 0, 0, 46, C.ink);
  out.startG = s;
  ziele.forEach(([x, y], i) => {
    const w = el('path', { d: catmull([start, [620, 560 + (y - 560) * 0.35], [x - 120, y]]), fill: 'none', stroke: '#33466e', 'stroke-width': 7, 'stroke-linecap': 'round' }, b.cam);
    const wA = el('path', { d: w.getAttribute('d'), fill: 'none', stroke: C.blue, 'stroke-width': 8, 'stroke-linecap': 'round' }, b.cam);
    out.wege.push({ w, wA });
    const kg = g(b.cam);
    karte(kg, x - 100, y - 76, 660, 152, { fill: C.raised, stroke: C.edge, sw: 3 });
    const kach = kachel(kg, 'ABC'[i], C.blue, 74); tr(kach, x - 20, y);
    TB(kg, x + 40, y - 18, optionen[i], { size: 28, weight: 600, maxW: 500, lh: 34 });
    const strich = el('rect', { x: x - 110, y: y - 3, width: 680, height: 6, rx: 3, fill: C.red }, kg);
    O(strich, 0);
    out.karten.push({ g: kg, x, y, strich });
    const ende = g(b.cam, { transform: `translate(${x - 120} ${y})` });
    out.enden.push(ende);
  });
  return out;
}

function fallAkt(F) {
  return akt({
    name: F.name,
    bauen() {
      const c = (p) => cue(p).s;
      this.t = {};
      for (const [k, p] of F.anker) this.t[k] = c(p);
      this.tEnde = cue(F.ende, { halten: true }).s;
      const T0 = this.t;

      // ---------- Bühne 1: der Fall im Betrieb ----------
      const b1 = buehne(F.name + '-fall', { seed: F.seed });
      this.b1 = b1;
      const B = bauBetrieb(b1.cam); this.B = B;
      this.obj = g(b1.cam);
      const o = blatt(this.obj, { w: 420, h: 330, pad: 28, kicker: F.objekt.kicker, kSize: 14, titel: F.objekt.titel, tSize: 26 });
      this.objZeilen = F.objekt.zeilen.map((z, i) => {
        const zg = g(this.obj);
        const bg = el('rect', { x: o.left - 10, y: o.y + 6 + i * 44, width: o.right - o.left + 20, height: 38, rx: 6, fill: 'rgba(255,209,102,0.0)' }, zg);
        T(zg, o.left, o.y + 32 + i * 44, z.text, { size: 21, fill: C.pInk });
        return { g: zg, bg, at: z.at, heikel: z.heikel };
      });
      this.pillen = (F.pillen || []).map((p) => ({ g: pille(b1.cam, p.text, { icon: p.icon, col: C.amber, gestrichelt: true, size: 22 }), x: p.x, y: p.y, at: p.at }));
      shot(b1, T0.start - 0.4, F.ueber || { typ: 'schwarz', d: 0.9 });

      // ---------- Bühne 2: die Wahl ----------
      const b2 = buehne(F.name + '-wahl', { seed: F.seed + 1, regalDeckkraft: 0.5 });
      this.b2 = b2;
      this.gabel = bauGabel(b2, F.optionen);
      this.denk = g(b2.front);
      el('rect', { x: 600, y: 980, width: 720, height: 12, rx: 6, fill: 'rgba(255,209,102,0.2)' }, this.denk);
      this.denkBar = el('rect', { x: 600, y: 980, width: 720, height: 12, rx: 6, fill: C.amber }, this.denk);
      shot(b2, T0.wahl - 0.35, { typ: 'blende', d: 0.7 });

      // ---------- Bühne 3: die Folge ----------
      const b3 = buehne(F.name + '-folge', { seed: F.seed + 2, regalDeckkraft: 0.45 });
      this.b3 = b3;
      const n = F.folge.length;
      this.fPts = F.folge.map((_, i) => [260 + i * (1400 / (n - 1)), 600]);
      this.fWeg = el('path', { d: catmull([[120, 600], ...this.fPts]), fill: 'none', stroke: '#33466e', 'stroke-width': 7, 'stroke-linecap': 'round' }, b3.cam);
      this.fItems = F.folge.map((f, i) => {
        const [x, y] = this.fPts[i];
        const gr = g(b3.cam);
        const last = i === n - 1;
        const col = last ? C.red : f.ton === 'amber' ? C.amber : C.muted;
        const ring = el('circle', { cx: x, cy: y, r: last ? 26 : 18, fill: last ? C.red : C.surface, stroke: col, 'stroke-width': 4, 'stroke-dasharray': f.ton === 'amber' ? '7 5' : '' }, gr);
        if (f.zeit) T(gr, x, y - 54, f.zeit, { mono: 1, size: 26, fill: col, anchor: 'middle' });
        TB(gr, x - 150, y + 64, f.text, { size: 26, weight: 600, maxW: 300, lh: 32, fill: last ? C.red : C.ink });
        if (last) lampe(gr, x, y, 14, C.red);
        return { g: gr, at: f.at, ring };
      });
      shot(b3, T0.folge - 0.35, { typ: 'kreis', d: 1.1, p: [this.gabel.ziele[F.falsch][0] - 120, this.gabel.ziele[F.falsch][1]] });

      // ---------- Bühne 4: der Schritt ----------
      const b4 = buehne(F.name + '-schritt', { seed: F.seed + 3, regalDeckkraft: 0.5 });
      this.b4 = b4;
      this.gabel2 = bauGabel(b4, F.optionen);
      this.ziel = g(b4.cam, { transform: `translate(${this.gabel2.ziele[2][0] + 610} ${this.gabel2.ziele[2][1]})` });
      lampe(this.ziel, 0, 0, 16, C.green);
      this.notizen = F.gruende.map((gr0, i) => {
        const z = this.gabel2.ziele[gr0.option];
        const p = pille(b4.cam, gr0.text, { col: C.red, size: 20 });
        return { g: p, x: z[0] + 230, y: z[1] + 98, at: gr0.at };
      });
      this.zielText = g(b4.cam);
      TB(this.zielText, this.gabel2.ziele[2][0] + 580, this.gabel2.ziele[2][1] + 70, F.schritt.sub, { size: 24, maxW: 420, lh: 30, fill: C.ink });
      shot(b4, T0.schritt - 0.35, { typ: 'schieben', d: 0.8, dir: -1 });
      this.buehnen = [b1, b2, b3, b4];

      // ---------- Ton ----------
      klang(T0.objekt - 0.1, 'paper_slide');
      for (const k of ['opt0', 'opt1', 'opt2']) klang(T0[k], 'pop', { laut: 0.7 });
      klang(T0.denk, 'clock_tick', { dauer: F.denkSek || 2.5, laut: 0.5 });
      F.folge.forEach((f, i) => klang(T0[f.at], i === F.folge.length - 1 ? 'thud_low' : 'tick', { laut: i === F.folge.length - 1 ? 0.8 : 0.5 }));
      klang(T0.grund0, 'strike'); klang(T0.grund1, 'strike'); klang(T0.schritt + 0.9, 'chime_soft');
      // ---------- Einblendungen ----------
      kopf(T0.start - 0.2, T0.wahl - 0.4, F.kopf.kicker, F.kopf.titel);
      kopf(T0.wahl, T0.folge - 0.4, { de: '4 · WAS TUN SIE?', en: '4 · WHAT DO YOU DO?' }, F.kopf.frage);
      kopf(T0.folge, T0.schritt - 0.4, F.kopf.folgeKicker, F.kopf.folgeTitel);
      kopf(T0.schritt, this.tEnde - 0.3, { de: '4 · DER EINE SCHRITT', en: '4 · THE ONE STEP' }, F.schritt.titel);
      for (const m of F.marken || []) {                       // ab/bis sind Schlüssel aus F.anker (Anker sind nur vorwärts auffindbar)
        const ab = T0[m.ab] - 0.15, bis = m.bis ? T0[m.bis] - 0.1 : this.tEnde - 0.2, q = m.quelle ? QUELLEN_F[m.quelle] : null;
        if (m.art) marke(ab, bis, m.art, q); else leiste(ab, bis, q);   // ohne Art nur die Quellenleiste (leiste() steht in bausteine.js)
      }
    },

    zeichnen(t) {
      const T0 = this.t, B = this.B;
      if (this.b1.vis) {
        const k = fahrt(t, BLICK.haus, [{ t: T0.start - 0.4, d: 2.2, f: F.blick.f, z: F.blick.z, e: E.sine }, { t: T0.objekt - 0.2, d: 1.2, f: F.blickNah.f, z: F.blickNah.z }]);
        kamera(this.b1, k.f, k.z);
        B.monitore.forEach((m, i) => bildschirm(m, i === 0 ? P(t, T0.start, 0.4) : 0.1));
        B.telefone.forEach((f) => { O(f.dim, 0.78); O(f.glow, 0.12); });
        betriebLeben(B, t, { tippen: F.tippen ? { [F.tippen]: [T0.objekt, T0.wahl] } : {} });
        const ok = P(t, T0.objekt - 0.1, 0.9, E.io);
        const pos = bogen(F.objekt.von, F.objekt.nach, ok, 140);
        tr(this.obj, pos[0], pos[1], lerp(0.5, 1, ok), lerp(-8, -2, ok)); O(this.obj, P(t, T0.objekt - 0.15, 0.25));
        this.objZeilen.forEach((z) => {
          const a = P(t, T0[z.at] - 0.1, 0.3);
          O(z.g, 0.25 + 0.75 * a);
          z.bg.setAttribute('fill', z.heikel ? `rgba(255,209,102,${(0.32 * P(t, T0[z.at] + 0.2, 0.4)).toFixed(3)})` : 'rgba(255,209,102,0)');
        });
        this.pillen.forEach((p) => { tr(p.g, p.x, p.y, Math.max(0.01, P(t, T0[p.at], 0.45, E.back))); O(p.g, P(t, T0[p.at], 0.25)); });
      }
      const gabel = (G, wahl, schritt) => {
        G.wege.forEach((w, i) => {
          const an = wahl ? P(t, T0['opt' + i] - 0.2, 0.7) : 1;
          zeichne(w.w, an);
          const blau = schritt && i === 2 ? P(t, T0.schritt + 0.2, 1.0) : 0;
          zeichne(w.wA, blau); O(w.wA, blau > 0 ? 1 : 0);
          O(w.w, schritt && i !== 2 ? 0.35 : 1);
        });
        G.karten.forEach((kc, i) => {
          const an = wahl ? P(t, T0['opt' + i], 0.45, E.out) : 1;
          tr(kc.g, (1 - an) * 40, 0); O(kc.g, schritt && i !== 2 ? 0.5 + 0.5 * (1 - P(t, T0['grund' + i] || T0.schritt + 1, 0.4)) : an);
          if (schritt && i !== 2) { O(kc.strich, P(t, T0['grund' + i] || T0.schritt + 1, 0.35)); }
        });
      };
      if (this.b2.vis) {
        kamera(this.b2, [960, 560], 0.92);
        gabel(this.gabel, true, false);
        const dk = P(t, T0.denk, F.denkSek || 2.5, E.lin);
        this.denkBar.setAttribute('width', (720 * (1 - dk)).toFixed(1));
        O(this.denk, fenster(t, T0.denk - 0.1, 0.3, T0.denk + (F.denkSek || 2.5) + 0.3, 0.3));
      }
      if (this.b3.vis) {
        const mitte = (this.fPts[0][0] + this.fPts[this.fPts.length - 1][0]) / 2;
        const k = fahrt(t, { f: [mitte - 120, 640], z: 0.95 }, [{ t: T0.folge, d: Math.max(2, T0.schritt - T0.folge), f: [mitte, 620], z: 0.86, e: E.sine }]);
        kamera(this.b3, k.f, k.z);
        const n = this.fItems.filter((it) => t >= T0[it.at] - 0.1).length;
        zeichne(this.fWeg, n === 0 ? 0.05 : clamp((n - 0.3) / (this.fItems.length - 0.3)));
        this.fItems.forEach((it) => { const a = P(t, T0[it.at] - 0.1, 0.45, E.out); O(it.g, a); });
      }
      if (this.b4.vis) {
        kamera(this.b4, [1240, 560], 0.82);
        gabel(this.gabel2, false, true);
        const zk = P(t, T0.schritt + 0.9, 0.5, E.back);
        sk(this.ziel, this.gabel2.ziele[2][0] + 610, this.gabel2.ziele[2][1], Math.max(0.01, zk)); O(this.ziel, zk);
        this.notizen.forEach((nz) => { tr(nz.g, nz.x, nz.y, Math.max(0.01, P(t, T0[nz.at], 0.4, E.back))); O(nz.g, P(t, T0[nz.at], 0.25)); });
        rein(this.zielText, 0, 0, t, T0.schritt + 1.2, 0.6, this.tEnde - 0.2, 20);
      }
    },
  });
}

