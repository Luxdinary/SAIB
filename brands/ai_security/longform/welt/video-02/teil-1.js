// Teil 1 · Einstieg (Fassung 2): „Hat Ihr Kunde einen Sicherheitsfragebogen geschickt?“, Vorstellung, was das Video zeigt (Absätze 0 und 1).
// Bühnen: der Beispielbetrieb bei Nacht (ein Umschlag kommt, wird zum Fragebogen, Termin, leerer Raum „IT-Abteilung“), Vorschau (drei Fragen des Videos).
// „Hier ist Scutoria“ und der KI-Hinweis stehen seit Fassung 2 am Schluss (teil-7.js); der Bildschirmtext unten links steht ab Sekunde 0.
akt({
  name: 'einstieg',
  bauen() {
    // ---------- Wortanker ----------
    const c = (de, en) => cue({ de, en }).s;
    this.tHook = c('Hat Ihr Kunde einen', 'Has your customer');   // Langfassung: vor dem Einstieg läuft der Kaltstart
    this.tFrage = c('Sicherheitsfragebogen', 'security questionnaire');
    this.tTermin = c('Ein Termin', 'A deadline');
    this.tKeineIT = c('keine IT-Abteilung|keine IT Abteilung', 'no IT department');
    this.tWarum = c('Warum er kommt', 'Why it comes');
    this.tNoch = c('noch nicht, mit Termin', 'not yet, with a date');
    this.tVoll = c('vollständige Antwort', 'complete answer');
    this.tSelbst = c('Selbstauskunft', 'self-declaration');
    this.tEnde = cue({ de: 'Die Lage ist in', en: 'The situation is the' }, { halten: true }).s;

    // ---------- Bühne 1: der Betrieb bei Nacht, ein Fragebogen kommt ----------
    const b1 = buehne('einstieg-betrieb', { seed: 3 }); this.b1 = b1;
    const B = bauBetrieb(b1.cam); this.B = B;
    // leerer Raum „IT-Abteilung“ über dem Haus
    this.itRaum = g(b1.cam);
    this.itRahmen = el('rect', { x: 2440, y: -40, width: 620, height: 190, rx: 18, fill: 'rgba(255,209,102,0.03)', stroke: C.amberLine, 'stroke-width': 5, 'stroke-dasharray': '18 12' }, this.itRaum);
    T(this.itRaum, 2750, 40, { de: 'IT-ABTEILUNG', en: 'IT DEPARTMENT' }, { mono: 1, size: 48, fill: C.amber, anchor: 'middle', ls: '0.1em' });
    T(this.itRaum, 2750, 118, { de: 'keine', en: 'none' }, { size: 50, weight: 800, fill: C.amber, anchor: 'middle' });
    this.itLinie = el('path', { d: 'M 2750 150 V 228', stroke: C.amberLine, 'stroke-width': 4, 'stroke-dasharray': '10 8' }, b1.cam);
    // Umschlag und Fragebogen
    this.umschlag = g(b1.cam);
    el('rect', { x: -64, y: -42, width: 128, height: 84, rx: 6, fill: C.paper, filter: 'url(#shadowS)' }, this.umschlag);
    el('path', { d: 'M -60 -38 L 0 6 L 60 -38', fill: 'none', stroke: C.pMuted, 'stroke-width': 4, 'stroke-linejoin': 'round' }, this.umschlag);
    this.bogen = g(b1.cam);
    const fb = blatt(this.bogen, { w: 520, h: 600, kicker: { de: 'FRAGEBOGEN · INFORMATIONSSICHERHEIT', en: 'QUESTIONNAIRE · INFORMATION SECURITY' }, kSize: 14, pad: 32 });
    this.bogenZeilen = [];
    for (let i = 0; i < 7; i++) {
      const y = fb.y + 26 + i * 54, zg = g(fb.g);
      el('rect', { x: fb.left, y: y - 6, width: 24, height: 24, rx: 4, fill: 'none', stroke: C.pBar2, 'stroke-width': 2 }, zg);
      el('rect', { x: fb.left + 40, y, width: 200 + ((i * 53) % 110), height: 11, rx: 5.5, fill: C.pBar }, zg);
      el('rect', { x: fb.right - 110, y: y - 8, width: 110, height: 28, rx: 6, fill: 'none', stroke: C.pLine, 'stroke-width': 2 }, zg);
      this.bogenZeilen.push(zg);
    }
    this.terminP = terminPille(this.bogen, { de: 'Termin', en: 'Deadline' }, 44);
    tr(this.terminP, 150, 330);
    shot(b1, this.tHook - 0.5, { typ: 'blende', d: 0.8 });

    // ---------- Bühne 3: Vorschau auf die drei Fragen ----------
    const b3 = buehne('einstieg-vorschau', { seed: 7, regalDeckkraft: 0.6 }); this.b3 = b3;
    const v = b3.cam;
    this.feld = [380, 960, 1540].map((x) => { const gr = g(v); el('rect', { x: x - 270, y: 290, width: 540, height: 470, rx: 22, fill: C.surface, stroke: C.edge, 'stroke-width': 3 }, gr); return gr; });
    // 1 Warum er kommt: Kunde schickt an Lieferant
    this.vKunde = kundeHaus(this.feld[0], 250, 650, 0.5, { label: null });
    this.vKlein = kleinHaus(this.feld[0], 520, 650, 0.62, { label: null });
    T(this.feld[0], 250, 700, { de: 'KUNDE', en: 'CUSTOMER' }, { mono: 1, size: 24, fill: C.muted, anchor: 'middle', ls: '0.1em' });
    T(this.feld[0], 520, 700, { de: 'SIE', en: 'YOU' }, { mono: 1, size: 24, fill: C.muted, anchor: 'middle', ls: '0.1em' });
    this.vBlatt = g(this.feld[0]); el('rect', { x: -26, y: -34, width: 52, height: 68, rx: 4, fill: C.paper }, this.vBlatt); linien(this.vBlatt, -16, -20, 32, 4, 12, C.pBar2, 5);
    this.vT = [T(v, 380, 350, { de: 'Warum er kommt', en: 'Why it comes' }, { size: 32, weight: 800, anchor: 'middle' })];
    // 2 Noch nicht, mit Termin: vollständig
    this.vNoch = antwort(v, 'termin', { size: 28 }); tr(this.vNoch, 960, 500);
    this.vVoll = pille(v, { de: 'vollständige Antwort', en: 'complete answer' }, { icon: 'check', col: C.blue, size: 28, mono: false, weight: 800 }); tr(this.vVoll, 960, 610);
    this.vT.push(T(v, 960, 350, { de: 'Was als Antwort zählt', en: 'What counts as an answer' }, { size: 32, weight: 800, anchor: 'middle' }));
    // 3 Selbstauskunft
    this.vSa = g(v);
    const sa = blatt(this.vSa, { w: 300, h: 330, kicker: { de: 'SELBSTAUSKUNFT', en: 'SELF-DECLARATION' }, kSize: 13, pad: 24 });
    this.vSaZeilen = [C.green, C.amber, C.amber].map((col, i) => { const zg = g(sa.g); const y = sa.y + 30 + i * 62; el('circle', { cx: sa.left + 12, cy: y, r: 12, fill: i === 2 ? 'none' : col, stroke: col, 'stroke-width': 3, 'stroke-dasharray': i === 2 ? '6 4' : '' }, zg); el('rect', { x: sa.left + 38, y: y - 6, width: 150, height: 12, rx: 6, fill: C.pBar }, zg); T(zg, sa.right, y + 6, '2026-11', { mono: 1, size: 14, fill: C.pMuted, anchor: 'end' }); return zg; });
    this.vT.push(T(v, 1540, 350, { de: 'Wie sie aussieht', en: 'What it looks like' }, { size: 32, weight: 800, anchor: 'middle' }));
    shot(b3, this.tWarum - 0.35, { typ: 'blende', d: 0.7 });
    this.buehnen = [b1, b3];

    // ---------- Einblendungen ----------
    kopf(this.tHook - 0.2, this.tWarum - 0.4, { de: 'SCUTORIA · SICHERHEITSFRAGEBOGEN', en: 'SCUTORIA · SECURITY QUESTIONNAIRE' }, { de: 'Ein Sicherheitsfragebogen?', en: 'A security questionnaire?' });
    kopf(this.tWarum, this.tEnde - 0.3, { de: 'IN DIESEM VIDEO', en: 'IN THIS VIDEO' }, '');
    hinweis(0, this.tEnde - 0.2, (gr) => {
      el('rect', { x: 96, y: 990, width: 56, height: 2, fill: C.blue }, gr);
      T(gr, 96, 1030, { de: 'Synthetische Stimme · Quellen am Bildschirm · Keine Rechtsberatung', en: 'Synthetic voice · Sources on screen · No legal advice' }, { mono: 1, size: 24, fill: C.muted, ls: '0.04em' });
    });
  },

  zeichnen(t) {
    const B = this.B;
    // ---------- Bühne 1 ----------
    if (this.b1.vis) {
      const k = fahrt(t, { f: [1720, 450], z: 0.58 }, [{ t: this.tHook - 0.5, d: Math.max(3, this.tWarum - this.tHook), f: [1680, 420], z: 0.62, e: E.sine }]); // der Auftakt ist kurz: Totale mit leichter Drift
      kamera(this.b1, k.f, k.z);
      const an = [0, 0.15, 0.3].map((d) => P(t, this.tHook + 0.5 + d, 0.5, E.out));
      B.monitore.forEach((m, i) => bildschirm(m, 0.25 + 0.75 * an[i]));
      // Umschlag fliegt auf einem Bogen zum Schreibtisch von Büro A
      const fk = P(t, this.tFrage - 0.7, 1.3, E.io);
      const pos = bogen([-260, 120], [1062, 680], fk, 160);
      const auf = P(t, this.tFrage + 0.5, 0.8, E.out);
      tr(this.umschlag, pos[0], pos[1], 1 - 0.5 * auf, lerp(-18, 0, fk)); O(this.umschlag, Math.min(P(t, this.tFrage - 0.7, 0.2), 1 - auf));
      // Fragebogen faltet sich auf und steigt über den Schreibtisch
      const bp = lerp2([1062, 660], [1180, 360], auf);
      tr(this.bogen, bp[0], bp[1] + 4 * Math.sin(t * 0.9), lerp(0.08, 0.95, auf), lerp(-6, -2, auf)); O(this.bogen, P(t, this.tFrage + 0.5, 0.3));
      this.bogenZeilen.forEach((z, i) => O(z, P(t, this.tFrage + 1.0 + i * 0.1, 0.25)));
      { const kk = P(t, this.tTermin, 0.45, E.back); tr(this.terminP, 150, 330, Math.max(0.01, kk) * (1 + 0.06 * puls(t, this.tTermin + 0.5, 1, 8))); O(this.terminP, P(t, this.tTermin, 0.2)); }
      // Büro A schaut zum Blatt; leerer Raum „IT-Abteilung“
      betriebLeben(B, t, { tippen: { figA: [this.tHook + 0.5, this.tFrage + 0.4], figB: [this.tHook + 0.8, 99], figC: [this.tHook + 1.1, 99] } });
      const ik = P(t, this.tKeineIT + 0.1, 0.6, E.out);
      O(this.itRaum, ik); tr(this.itRaum, 0, (1 - ik) * -30); zeichne(this.itLinie, P(t, this.tKeineIT + 0.5, 0.5));
      this.itRahmen.setAttribute('stroke-dashoffset', (-t * 16).toFixed(1));
    }
    // ---------- Bühne 3 ----------
    if (this.b3.vis) {
      kamera(this.b3, [960, 540], 1);
      const ein = [this.tWarum, this.tNoch - 0.2, this.tSelbst - 0.3];
      this.feld.forEach((f, i) => { const k = P(t, ein[i] - 0.1, 0.6, E.out); O(f, k); tr(f, 0, (1 - k) * 30); O(this.vT[i], k); tr(this.vT[i], 0, (1 - k) * 30); });
      // Blatt pendelt vom Kunden zum Lieferanten
      const zyk = clamp((t - this.tWarum - 0.5) / 2.2) ; const kk = E.io(zyk);
      const p = bogen([250, 470], [520, 520], kk, 90); tr(this.vBlatt, p[0], p[1], 0.9, lerp(-10, 6, kk)); O(this.vBlatt, Math.min(P(t, this.tWarum + 0.4, 0.2), 1));
      pop(this.vNoch, 960, 500, t, this.tNoch); tr(this.vNoch, 960, 500, Math.max(0.01, P(t, this.tNoch, 0.45, E.back)));
      tr(this.vVoll, 960, 610, Math.max(0.01, P(t, this.tVoll, 0.45, E.back))); O(this.vVoll, P(t, this.tVoll, 0.2));
      const sk = P(t, this.tSelbst - 0.2, 0.6, E.out); tr(this.vSa, 1540, 560 + (1 - sk) * 30, 1, lerp(4, 1.5, sk)); O(this.vSa, sk);
      this.vSaZeilen.forEach((z, i) => O(z, P(t, this.tSelbst + 0.3 + i * 0.25, 0.3)));
    }
  },
});
