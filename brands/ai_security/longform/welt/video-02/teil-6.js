// Teil 6 · Was das Toolkit nicht ist (Absätze 32 bis 35).
// Bühnen: Grenzen (keine Rechtsberatung, kein Audit, kein Zertifikat; was die Dokumente zeigen) → die vier Marker
// → 23 Punkte, 13 offen → kein Zertifikat, sondern Selbstauskunft; der Betrieb entscheidet.
akt({
  name: 'nicht',
  bauen() {
    const c = (de, en, o) => cue({ de, en }, o).s;
    const K = { de: '6 · WAS DAS TOOLKIT NICHT IST', en: '6 · WHAT THE TOOLKIT IS NOT' };
    // ---------- Wortanker ----------
    this.tWas = c('Was dieses Toolkit', 'What this toolkit');
    this.tX = [c('keine Rechtsberatung', 'not legal advice'), c('kein Audit', 'not an audit'), c('kein Zertifikat', 'not a certificate')];
    this.tBeh = c('kein Dokument behauptet', 'no document claims');
    this.tSicher = c('sicher ist', 'is secure');
    this.tGesetz = c('ein Gesetz erfüllt', 'complies with a law');
    this.tZeigen = c('Die Dokumente zeigen', 'The documents show');
    this.tDatum = c('an einem Datum', 'on a given date');
    this.tBis = c('bis wann', 'by when');
    this.tWer = c('wer dafür einsteht', 'who answers for it');
    this.tJede = c('Jede Aussage', 'Every statement');
    this.tVier = c('vier Markern', 'four markers');
    this.tM = [c('Fakt', 'Fact'), c('Auslegung', 'Interpretation'), c('Unsicher', 'Uncertain'), c('Lücke', 'Gap')];
    // Erklärungen je Marker: in Sprechreihenfolge nach dem jeweiligen Wort (halten, damit die nächste Marker-Suche nicht überspringt)
    this.tEntsch = c('Sie entscheiden', 'you decide');
    this.tAbsicht = c('absichtlich offen', 'open on purpose');
    const Q9 = quelle(); this.tQ9 = Q9.s;
    this.tDrei = c('dreiundzwanzig Punkte', 'twenty-three points|twenty three points');
    this.tDreizehn = c('dreizehn', 'thirteen');
    this.tAbs6 = c('Abschnitt sechs', 'section six');
    this.tBek = c('Bekommen Sie damit', 'Does it give you');
    this.tNein = c('Nein', 'No');
    this.tSA = c('Selbstauskunft mit Nachweisen', 'self-declaration with evidence');
    this.tVers = c('Versicherer', 'insurers');
    this.tWahr = c('welche Antwort wahr', 'which answer is true');
    this.tEntscheidet = c('entscheidet Ihr Betrieb', 'your business decides');
    this.tSchreibt = c('schreibt sie auf', 'writes it down');
    this.tEnde = cue({ de: 'Wenn Sie anfangen wollen', en: 'If you want to start' }, { halten: true }).s;

    // ---------- Bühne 1: Grenzen ----------
    const b1 = buehne('nicht-grenzen', { seed: 97, regalDeckkraft: 0.55 }); this.b1 = b1;
    const k1 = b1.cam;
    this.tk = g(k1);
    { const b0 = blatt(this.tk, { w: 300, h: 380, kicker: { de: 'HANDBUCH', en: 'HANDBOOK' }, kSize: 13, pad: 26 }); linien(b0.g, b0.left, b0.y + 10, 240, 8, 32, C.pBar, 10); tr(b0.g, -80, -30, 1, -4);
      const b1b = blatt(this.tk, { w: 300, h: 380, kicker: { de: 'D1 · SELBSTAUSKUNFT', en: 'D1 · SELF-DECLARATION' }, kSize: 13, pad: 26 }); linien(b1b.g, b1b.left, b1b.y + 10, 240, 8, 32, C.pBar, 10); tr(b1b.g, 60, 20, 1, 3); }
    this.tkLab = T(k1, 420, 820, { de: 'Sicherheitsnachweis-Toolkit', en: 'Security Evidence Toolkit' }, { size: 30, weight: 800, anchor: 'middle' });
    this.nicht = [['para', { de: 'Rechtsberatung', en: 'Legal advice' }], ['search', { de: 'Audit', en: 'Audit' }], ['cert', { de: 'Zertifikat', en: 'Certificate' }]].map(([ic, w0]) => { const gr = g(k1); const p = pille(gr, w0, { icon: ic, col: C.muted, size: 32, mono: false, weight: 800 }); const s = streich(gr, p.w, C.red); return { g: gr, s }; });
    this.behaupt = [{ de: '„Ihr Betrieb ist sicher“', en: '"your business is secure"' }, { de: '„erfüllt das Gesetz“', en: '"complies with the law"' }].map((w0) => { const gr = g(k1); const p = pille(gr, w0, { col: C.dim, size: 26, gestrichelt: true, mono: false, weight: 700 }); const s = streich(gr, p.w, C.red); return { g: gr, s }; });
    this.behLab = T(k1, 1290, 560, { de: 'kein Dokument behauptet', en: 'no document claims' }, { mono: 1, size: 22, fill: C.muted, anchor: 'middle', ls: '0.06em' });
    this.zeigt = [['calendar', { de: 'was an einem Datum vorliegt', en: 'what is in place on a date' }], ['clock', { de: 'was bis wann geschieht', en: 'what happens by when' }], ['person', { de: 'wer dafür einsteht', en: 'who answers for it' }]].map(([ic, w0]) => pille(k1, w0, { icon: ic, col: C.blue, size: 26 }));
    shot(b1, this.tWas - 0.5, { typ: 'schwarz', d: 0.9 });

    // ---------- Bühne 2: vier Marker ----------
    const b2 = buehne('nicht-marker', { seed: 101, regalDeckkraft: 0.5 }); this.b2 = b2;
    const k2 = b2.cam;
    this.hb = g(k2); ikon(this.hb, 'book', 0, 0, 70, C.blue); T(this.hb, 0, 70, { de: 'im Handbuch', en: 'in the handbook' }, { mono: 1, size: 22, fill: C.muted, anchor: 'middle', ls: '0.06em' });
    const ERKL = { fakt: { de: 'am Original gelesen, mit Abrufdatum', en: 'read at the original, with retrieval date' }, auslegung: { de: 'unsere Schlussfolgerung, streitbar', en: 'our conclusion, open to argument' },
      unsicher: { de: 'Quellen widersprechen sich, Lage offen', en: 'sources contradict, law is open' }, luecke: { de: 'keine Quelle: Sie entscheiden', en: 'no source: you decide' } };
    this.kacheln = ['fakt', 'auslegung', 'unsicher', 'luecke'].map((art, i) => {
      const x = 360 + i * 400, gr = g(k2, { transform: `translate(${x} 560)` });
      el('rect', { x: -170, y: -190, width: 340, height: 380, rx: 20, fill: C.surface, stroke: C.edge, 'stroke-width': 3 }, gr);
      const form = g(gr, { transform: 'translate(0 -80)' }); el('circle', { r: 90, fill: art === 'fakt' ? 'url(#gBlue)' : art === 'auslegung' ? 'url(#gPurple)' : art === 'unsicher' ? 'url(#gAmber)' : 'url(#gRed)' }, form); markerShape(form, art, 96);
      T(gr, 0, 70, MARKWORT[art], { mono: 1, size: 30, fill: MARKFARBE[art], anchor: 'middle', ls: '0.12em' });
      const ek = TB(gr, -140, 118, ERKL[art], { size: 24, weight: 700, maxW: 280, lh: 29, fill: C.ink });
      return { g: gr, form, ek, x, art };
    });
    this.feldOffen = g(k2); el('rect', { x: -120, y: -24, width: 240, height: 48, rx: 8, fill: 'none', stroke: C.red, 'stroke-width': 3, 'stroke-dasharray': '10 7' }, this.feldOffen); T(this.feldOffen, 0, 8, { de: 'Feld bleibt offen', en: 'field stays open' }, { mono: 1, size: 20, fill: C.red, anchor: 'middle' });
    shot(b2, this.tJede - 0.4, { typ: 'blende', d: 0.7 });

    // ---------- Bühne 3: 23 Punkte, 13 offen ----------
    const b3 = buehne('nicht-punkte', { seed: 103, regalDeckkraft: 0.5 }); this.b3 = b3;
    const k3 = b3.cam;
    this.punkte = Array.from({ length: 23 }, (_, i) => {
      const offen = [0, 2, 3, 5, 7, 8, 10, 12, 14, 15, 17, 19, 21].includes(i); // 13 offen, 10 geklärt; welche Punkte es sind, zeigt das Bild nicht (Anordnung nur zur Darstellung)
      const x = 300 + (i % 6) * 110, y = 360 + Math.floor(i / 6) * 110, gr = g(k3, { transform: `translate(${x} ${y})` });
      const c0 = el('circle', { r: 36, fill: offen ? 'rgba(255,209,102,0.06)' : '#22385d', stroke: offen ? C.amberLine : C.blue, 'stroke-width': 4, 'stroke-dasharray': offen ? '9 7' : '' }, gr);
      return { g: gr, offen, c: c0, x, y };
    });
    this.zahl23 = T(k3, 1300, 420, { de: '23 Punkte', en: '23 points' }, { size: 64, weight: 800 });
    this.stand = T(k3, 1300, 470, { de: 'Stand 23. Oktober 2026', en: 'as of 23 October 2026' }, { mono: 1, size: 24, fill: C.muted });
    this.zahl13 = T(k3, 1300, 580, { de: '13 offen', en: '13 open' }, { size: 64, weight: 800, fill: C.amber });
    this.abs6 = pille(k3, { de: 'Handbuch, Abschnitt 6', en: 'Handbook, section 6' }, { icon: 'book', col: C.blue, size: 26 });
    shot(b3, this.tQ9 - 0.4, { typ: 'blende', d: 0.7 });

    // ---------- Bühne 4: kein Zertifikat; der Betrieb entscheidet ----------
    const b4 = buehne('nicht-entscheidet', { seed: 107, regalDeckkraft: 0.5 }); this.b4 = b4;
    const k4 = b4.cam;
    this.zert = g(k4); { el('circle', { r: 110, fill: 'none', stroke: C.dim, 'stroke-width': 4, 'stroke-dasharray': '12 9' }, this.zert); iconCert(this.zert, 120, C.muted); }
    this.zertS = el('path', { d: 'M -100 -100 L 100 100', stroke: C.red, 'stroke-width': 8, 'stroke-linecap': 'round' }, this.zert);
    this.zertLab = TB(k4, 200, 700, { de: 'Zertifikat oder Gütesiegel?', en: 'A certificate or a label?' }, { size: 30, weight: 800, maxW: 340, lh: 36, fill: C.muted });
    this.nein = T(k4, 330, 400, { de: 'Nein.', en: 'No.' }, { size: 80, weight: 800, anchor: 'middle' });
    this.sa = g(k4);
    { const s0 = blatt(this.sa, { w: 340, h: 440, kicker: { de: 'SELBSTAUSKUNFT', en: 'SELF-DECLARATION' }, kSize: 14, pad: 28 }); this.saZ = [C.green, C.amber, C.amber, C.green].map((col, i) => { const zg = g(s0.g); const y = s0.y + 30 + i * 56; el('circle', { cx: s0.left + 12, cy: y, r: 12, fill: i === 2 ? 'none' : col, stroke: col, 'stroke-width': 3, 'stroke-dasharray': i === 2 ? '6 4' : '' }, zg); el('rect', { x: s0.left + 36, y: y - 6, width: 180, height: 12, rx: 6, fill: C.pBar }, zg); return zg; }); this.saSlot = [s0.left, s0.y + 30 + 4 * 56]; }
    this.saOrdner = nachweisOrdner(k4, { w: 300, h: 210 });
    this.empf = [kundeHaus(k4, 1500, 470, 0.42, { label: null }), null];
    this.versG = g(k4); { el('circle', { r: 70, fill: C.surface, stroke: C.edge, 'stroke-width': 3 }, this.versG); iconBriefcase(this.versG, 70, C.muted); }
    this.empfL = [T(k4, 1500, 506, { de: 'KUNDEN', en: 'CUSTOMERS' }, { mono: 1, size: 22, fill: C.muted, anchor: 'middle', ls: '0.1em' }), T(k4, 1720, 506, { de: 'VERSICHERER', en: 'INSURERS' }, { mono: 1, size: 22, fill: C.muted, anchor: 'middle', ls: '0.1em' })];
    this.zuerstP = pille(k4, { de: 'verlangen das zuerst', en: 'ask for this first' }, { col: C.blue, size: 22 });
    this.inhaberin = seated(k4, 1480, 860, BESETZUNG.inhaberin);
    tisch(k4, 1420, 1760, 790);
    this.wahrP = pille(k4, { de: 'Ihr Betrieb entscheidet, was wahr ist', en: 'your business decides what is true' }, { icon: 'person', col: C.blue, size: 24 });
    this.schreibP = antwort(k4, 'termin', { size: 22 });
    shot(b4, this.tBek - 0.4, { typ: 'blende', d: 0.7 });
    this.buehnen = [b1, b2, b3, b4];

    // ---------- Einblendungen ----------
    kopf(this.tWas, this.tJede - 0.3, K, { de: 'Was es nicht ist', en: 'What it is not' });
    kopf(this.tJede, this.tQ9 - 0.3, K, { de: 'Vier Marker', en: 'Four markers' });
    kopf(this.tQ9, this.tBek - 0.3, K, { de: 'Offene Punkte, mit Stand', en: 'Open points, with status' });
    kopf(this.tBek, this.tEnde - 0.3, K, { de: 'Ihr Betrieb entscheidet', en: 'Your business decides' });
  },

  zeichnen(t) {
    // ---------- Bühne 1 ----------
    if (this.b1.vis) {
      kamera(this.b1, [960, 540], 1);
      const tk = P(t, this.tWas, 0.7, E.out); tr(this.tk, 420, 500 + (1 - tk) * 24, 1); O(this.tk, tk); O(this.tkLab, tk);
      this.nicht.forEach((n, i) => { const t0 = this.tX[i]; tr(n.g, 1290, 270 + i * 90, Math.max(0.01, P(t, t0 - 0.1, 0.45, E.back))); O(n.g, P(t, t0 - 0.1, 0.2)); zeichne(n.s, P(t, t0 + 0.35, 0.35)); });
      O(this.behLab, P(t, this.tBeh, 0.4));
      this.behaupt.forEach((b, i) => { const t0 = i === 0 ? this.tSicher : this.tGesetz; tr(b.g, 1290, 620 + i * 76, 1); O(b.g, P(t, t0 - 0.3, 0.3) * 0.9); zeichne(b.s, P(t, t0 + 0.1, 0.35)); });
      const ab = P(t, this.tZeigen - 0.2, 0.5);
      [this.tDatum, this.tBis, this.tWer].forEach((tt, i) => { const p = this.zeigt[i]; tr(p, 400 + i * 560, 900, Math.max(0.01, P(t, tt - 0.1, 0.45, E.back))); O(p, P(t, tt - 0.1, 0.2)); });
      O(this.tkLab, tk * (1 - 0.0 * ab));
    }
    // ---------- Bühne 2 ----------
    if (this.b2.vis) {
      kamera(this.b2, [960, 540], 1);
      tr(this.hb, 960, 250, Math.max(0.01, P(t, this.tJede, 0.45, E.back))); O(this.hb, P(t, this.tJede, 0.2));
      this.kacheln.forEach((k, i) => {
        const t0 = this.tM[i] - 0.15, a = P(t, t0, 0.5, E.out);
        tr(k.g, k.x, 560 + (1 - a) * 30, 1); O(k.g, Math.max(P(t, this.tVier, 0.4) * 0.25, a));
        const f = P(t, t0, 0.5, E.back); k.form.setAttribute('transform', `translate(0 -80) scale(${Math.max(0.01, f).toFixed(3)})`);
        O(k.ek, P(t, t0 + 0.6, 0.4));
      });
      tr(this.feldOffen, 1560, 860, Math.max(0.01, P(t, this.tAbsicht - 0.2, 0.45, E.back))); O(this.feldOffen, P(t, this.tAbsicht - 0.2, 0.2));
    }
    // ---------- Bühne 3 ----------
    if (this.b3.vis) {
      kamera(this.b3, [960, 540], 1);
      this.punkte.forEach((p, i) => { const t0 = this.tDrei - 0.4 + i * 0.05, k = P(t, t0, 0.35, E.back); sk(p.g, 0, 0, 1); p.g.setAttribute('transform', `translate(${p.x} ${p.y}) scale(${Math.max(0.01, k).toFixed(3)})`); O(p.g, P(t, t0, 0.15) * (p.offen || t < this.tDreizehn ? 1 : 1 - 0.55 * P(t, this.tDreizehn, 0.4)));
        if (p.offen) p.c.setAttribute('stroke-width', t > this.tDreizehn ? 5 : 4); });
      O(this.zahl23, P(t, this.tDrei, 0.4)); O(this.stand, P(t, this.tDrei + 0.5, 0.4)); O(this.zahl13, P(t, this.tDreizehn, 0.4));
      tr(this.abs6, 1440, 700, Math.max(0.01, P(t, this.tAbs6, 0.45, E.back))); O(this.abs6, P(t, this.tAbs6, 0.2));
    }
    // ---------- Bühne 4 ----------
    if (this.b4.vis) {
      kamera(this.b4, [960, 540], 1);
      const zw = P(t, this.tWahr - 0.3, 0.8, E.io);
      const zk = P(t, this.tBek, 0.5, E.out); tr(this.zert, 330, 600, 1); O(this.zert, zk * (1 - 0.6 * zw)); O(this.zertLab, zk * (1 - zw)); zeichne(this.zertS, P(t, this.tNein, 0.35));
      O(this.nein, P(t, this.tNein, 0.3) * (1 - zw));
      const sk0 = P(t, this.tSA - 0.2, 0.6, E.out); tr(this.sa, lerp(860, 900, sk0), 520 + (1 - sk0) * 24, 1, -2); O(this.sa, sk0);
      tr(this.saOrdner.g, 900, 860, 0.7); O(this.saOrdner.g, P(t, this.tSA + 0.6, 0.4) * (1 - zw));
      const ek = P(t, this.tVers - 0.6, 0.5); O(this.empf[0].g, ek * (1 - zw)); tr(this.versG, 1720, 400, Math.max(0.01, P(t, this.tVers - 0.2, 0.45, E.back))); O(this.versG, P(t, this.tVers - 0.2, 0.2) * (1 - zw)); O(this.empfL[0], ek * (1 - zw)); O(this.empfL[1], P(t, this.tVers, 0.3) * (1 - zw));
      tr(this.zuerstP, 1610, 580, Math.max(0.01, P(t, this.tVers + 0.4, 0.45, E.back))); O(this.zuerstP, P(t, this.tVers + 0.4, 0.2) * (1 - zw));
      // der Betrieb entscheidet; das Toolkit schreibt die Antwort mit Termin auf
      O(this.inhaberin.g, zw); pose(this.inhaberin, -40 * P(t, this.tSchreibt - 0.3, 0.4), tippen(t, this.tSchreibt, this.tSchreibt + 2, 0, 6), 2 * Math.sin(t));
      tr(this.wahrP, 1500, 330, Math.max(0.01, P(t, this.tEntscheidet - 0.2, 0.45, E.back))); O(this.wahrP, P(t, this.tEntscheidet - 0.2, 0.2));
      const sp = P(t, this.tSchreibt, 0.9, E.io); const pp = bogen([1500, 600], [900 - 170 + 28 + 120, 520 + this.saSlot[1]], sp, 80);
      tr(this.schreibP, pp[0], pp[1], lerp(1, 0.9, sp)); O(this.schreibP, P(t, this.tSchreibt, 0.2));
    }
  },
});
