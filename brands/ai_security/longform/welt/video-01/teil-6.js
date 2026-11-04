// Teil 6 · Was es nicht ist. Absätze 43 bis 47 des Skripts.
// Bühnen: was die Dokumente zeigen → Handbuch, 17 Punkte, 8 offen → Weisungsbereich (Fakt) → Betriebsrat (Unsicher) → neun Bereiche, kein amtlicher Katalog.
akt({
  name: 'nicht',
  bauen() {
    const c = (de, en) => cue({ de, en }).s;
    const K = { de: '6 · WAS ES NICHT IST', en: '6 · WHAT IT IS NOT' };
    this.tKeine = c('Es ist keine Rechtsberatung', 'It is not legal advice');
    this.tKein = c('kein Dokument behauptet', 'no document claims');
    this.tZ = [c('was Sie entschieden haben', 'what you decided'), c('seit wann', 'since when'), c('für welche Tools', 'for which tools'), c('wer davon weiß', 'who knows')];
    this.tHB = c('Das Handbuch des Toolkits', 'The handbook of the toolkit');
    this.t17 = c('siebzehn Punkte|17 Punkte', 'seventeen points|17 points');
    this.tAcht = c('Acht bleiben offen|8 bleiben offen', 'Eight remain open|8 remain open');
    this.tO = [c('Welche Behörde in Österreich', 'Which authority supervises in Austria'), c('Wie oft die Einweisung', 'How often the briefing'), c('Ob eine Richtlinie eine', 'Whether a policy is'), c('freie Mitarbeit', 'freelancers')];
    const F = belegt(); this.tF = F.s;
    this.tAuftr = c('Auftragnehmer und Dienstleister', 'contractors and service providers');
    this.tWeis = c('Weisungsbereich', 'organisational remit');
    this.tVertrag = c('Vertragsrecht', 'contract law');
    this.tNicht = c('nicht erhoben', 'did not survey');
    const U = belegt(); this.tU = U.s;
    this.tBR = c('des Betriebsrats', 'of a works council');
    this.tArb = c('nationales Arbeitsrecht', 'national labour law');
    this.tFach = c('mit einer Fachperson', 'with a specialist');
    this.tVor = c('vor der Beschaffung', 'before procurement');
    this.tDanach = c('nicht danach', 'not after');
    this.tNeun = c('Und die neun Regelbereiche', 'And the nine areas');
    this.tAmtl = c('kein amtlicher Katalog', 'not an official catalogue');
    this.tZus = c('zusammenlegen', 'merge');
    this.tErg = c('ergänzen', 'add areas');
    this.tEnt = c('Ihr Betrieb entscheidet', 'Your business decides');
    this.tZeigen = c('Die Dokumente zeigen, was er', 'The documents show what it');
    this.tEnde = cue({ de: 'Für den ersten Schritt', en: 'For the first step' }, { halten: true }).s;

    // ---------- 1 was die Dokumente zeigen ----------
    const b1 = buehne('nicht-dokumente', { seed: 101, regalDeckkraft: 0.6 }); this.b1 = b1;
    const c1 = b1.cam;
    this.stapel = g(c1);
    ['D7', 'D6', 'D5', 'D4', 'D3', 'D2', 'D1'].forEach((d, i) => { const gr = g(this.stapel, { transform: `translate(${(i - 3) * 22} ${(i - 3) * -10}) rotate(${(i - 3) * 2.2})` }); el('rect', { x: -150, y: -200, width: 300, height: 400, rx: 6, fill: i % 2 ? C.paperBack : C.paper, filter: i === 6 ? 'url(#shadow)' : '' }, gr); T(gr, -120, -160, d, { mono: 1, size: 18, fill: C.pMuted }); if (i === 6) linien(gr, -120, -120, 220, 9, 28, C.pBar2, 10); });
    this.keineRB = pille(c1, { de: 'Keine Rechtsberatung', en: 'No legal advice' }, { icon: 'para', col: C.muted, size: 28 });
    this.keineZ = pille(c1, { de: 'keine Zusage, dass eine Vorschrift erfüllt ist', en: 'no claim that a rule is met' }, { icon: 'cross', col: C.muted, gestrichelt: true, size: 24 });
    const FAC = [['list', { de: 'was Sie entschieden haben', en: 'what you decided' }], ['calendar', { de: 'seit wann', en: 'since when' }], ['spark', { de: 'für welche Tools', en: 'for which tools' }], ['group', { de: 'wer davon weiß', en: 'who knows' }]];
    this.fac = FAC.map(([ic, txt]) => pille(c1, txt, { icon: ic, col: C.blue, size: 28, mono: false, weight: 800 }));
    this.FPOS = [[520, 360], [1400, 360], [520, 760], [1400, 760]];
    this.facL = this.FPOS.map(([x, y]) => el('line', { x1: 960, y1: 560, x2: x, y2: y, stroke: C.blue, 'stroke-width': 3, 'stroke-dasharray': '8 7' }, c1));
    this.facL.forEach((l) => c1.insertBefore(l, this.stapel));
    shot(b1, this.tKeine - 0.6, { typ: 'schwarz', d: 1.0 });

    // ---------- 2 Handbuch, 17 Punkte, 8 offen ----------
    const b2 = buehne('nicht-handbuch', { seed: 103, regalDeckkraft: 0.6 }); this.b2 = b2;
    const c2 = b2.cam;
    this.hb = g(c2);
    karte(this.hb, 160, 250, 760, 620, { fill: C.surface, stroke: C.edge });
    { const ic = g(this.hb, { transform: 'translate(220 312)' }); iconBook(ic, 50, C.ink); }
    T(this.hb, 262, 302, { de: 'HANDBUCH · ABSCHNITT 8', en: 'HANDBOOK · SECTION 8' }, { mono: 1, size: 20, fill: C.muted, ls: '0.1em' });
    T(this.hb, 262, 334, { de: 'Stand 23. Oktober 2026', en: 'As of 23 October 2026' }, { size: 22, weight: 700 });
    // Handbuch Abschnitt 8: offen sind 8.4, 8.5, 8.6, 8.9, 8.10, 8.11, 8.12 und 8.17; 8.7 und 8.8 sind mit Nein beantwortet; sieben erledigt
    // (Gegenprüfung V1 vom 23.10.2026, produkte/PRUEFPAKET-2026-10-23/umsetzung/V1-gegenpruefung-ki-richtlinien.md)
    const OFFEN = new Set([4, 5, 6, 9, 10, 11, 12, 17]), NEIN = new Set([7, 8]);
    this.punkte = Array.from({ length: 17 }, (_, i) => {
      const nr = i + 1, gr = g(c2); const x = 230 + (i % 6) * 112, y = 420 + Math.floor(i / 6) * 120; const off = OFFEN.has(nr), nein = NEIN.has(nr);
      const r = el('rect', { x: x - 44, y: y - 40, width: 88, height: 80, rx: 12, fill: off ? 'rgba(255,209,102,0.08)' : C.raised, stroke: off ? C.amber : C.edge, 'stroke-width': 2.5 }, gr);
      if (off) r.setAttribute('stroke-dasharray', '8 6');
      const ic = g(gr, { transform: `translate(${x} ${y - 6})` }); (off ? iconUnknown : nein ? iconCross : iconCheck)(ic, 30, off ? C.amber : nein ? C.muted : C.green);
      T(gr, x, y + 30, '8.' + nr, { mono: 1, size: 15, fill: C.muted, anchor: 'middle' });
      return { g: gr, off, x, y };
    });
    this.zaehl = pille(c2, { de: '17 Punkte · 8 offen', en: '17 points · 8 open' }, { col: C.amber, size: 26 });
    const OP = [['institution', { de: 'Aufsicht in Österreich', en: 'Supervision in Austria' }], ['clock', { de: 'Rhythmus der Einweisung, Aufbewahrung', en: 'Briefing rhythm, retention' }], ['gavel', { de: 'Richtlinie als Geheimhaltungsmaßnahme', en: 'Policy as a step to keep secrets' }], ['briefcase', { de: 'Bindung freier Mitarbeit und Dienstleister', en: 'Binding freelancers and contractors' }]];
    this.op = OP.map(([ic, txt], i) => { const gr = g(c2); karte(gr, 1000, 270 + i * 150, 780, 120, { fill: C.surface, stroke: C.amber, gestrichelt: true }); const k = g(gr, { transform: `translate(1060 ${330 + i * 150})` }); ikon(k, ic, 0, 0, 46, C.amber); TB(gr, 1110, 322 + i * 150, txt, { size: 27, weight: 800, maxW: 640, lh: 31 }); return gr; });
    shot(b2, this.tHB - 0.4, { typ: 'blende', d: 0.7 });

    // ---------- 3 Weisungsbereich ----------
    const b3 = buehne('nicht-weisung', { seed: 107, regalDeckkraft: 0.6 }); this.b3 = b3;
    const c3 = b3.cam;
    this.bereich = el('ellipse', { cx: 760, cy: 560, rx: 520, ry: 300, fill: 'rgba(79,140,255,0.06)', stroke: C.blue, 'stroke-width': 3, 'stroke-dasharray': '14 10' }, c3);
    this.bereichLab = T(c3, 760, 300, { de: 'WEISUNGSBEREICH', en: 'ORGANISATIONAL REMIT' }, { mono: 1, size: 22, fill: C.blue, anchor: 'middle', ls: '0.12em' });
    this.haus3 = g(c3, { transform: 'translate(500 560)' }); iconBuilding(this.haus3, 120, C.ink); T(this.haus3, 0, 104, { de: 'Betrieb', en: 'Business' }, { size: 24, weight: 700, anchor: 'middle' });
    this.leute = [[680, 470], [740, 640], [620, 660]].map(([x, y]) => { const gr = g(c3, { transform: `translate(${x} ${y})` }); iconPerson(gr, 60, C.muted); return gr; });
    this.extern = [['briefcase', 960, 450, { de: 'Auftragnehmer', en: 'Contractors' }], ['truck', 1000, 660, { de: 'Dienstleister', en: 'Service providers' }]].map(([ic, x, y, lab]) => { const gr = g(c3, { transform: `translate(${x} ${y})` }); ikon(gr, ic, 0, 0, 70, C.blue); T(gr, 0, 66, lab, { size: 22, weight: 700, anchor: 'middle' }); return gr; });
    this.art4 = pille(c3, { de: 'Art. 4 KI-VO erfasst sie', en: 'Art. 4 AI Act covers them' }, { icon: 'book', col: C.blue, size: 22 });
    this.vertrag = g(c3, { transform: 'translate(1560 560)' });
    el('rect', { x: -150, y: -110, width: 300, height: 220, rx: 14, fill: C.surface, stroke: C.amber, 'stroke-width': 3, 'stroke-dasharray': '11 8' }, this.vertrag);
    ikon(this.vertrag, 'contract', 0, -36, 64, C.amber);
    T(this.vertrag, 0, 44, { de: 'Vertragsrecht', en: 'Contract law' }, { size: 28, weight: 800, anchor: 'middle' });
    T(this.vertrag, 0, 80, { de: 'NICHT ERHOBEN', en: 'NOT SURVEYED' }, { mono: 1, size: 18, fill: C.amber, anchor: 'middle', ls: '0.1em' });
    this.vLinie = el('path', { d: 'M 1060 560 C 1220 560 1260 560 1410 560', fill: 'none', stroke: C.amber, 'stroke-width': 4, 'stroke-dasharray': '10 8' }, c3);
    shot(b3, this.tF - 0.4, { typ: 'blende', d: 0.7 });

    // ---------- 4 Betriebsrat ----------
    const b4 = buehne('nicht-betriebsrat', { seed: 109, regalDeckkraft: 0.6 }); this.b4 = b4;
    const c4 = b4.cam;
    this.tool4 = g(c4, { transform: 'translate(420 470)' }); el('circle', { r: 110, fill: 'url(#gBlue)' }, this.tool4); el('rect', { x: -80, y: -60, width: 160, height: 120, rx: 14, fill: '#e3e9f5' }, this.tool4); iconSpark(this.tool4, 60, C.blueDeep); T(this.tool4, 0, 100, { de: 'KI-TOOL', en: 'AI TOOL' }, { mono: 1, size: 20, fill: C.muted, anchor: 'middle', ls: '0.1em' });
    this.pfeil4 = el('path', { d: 'M 540 470 L 820 470', fill: 'none', stroke: C.amber, 'stroke-width': 5, 'stroke-dasharray': '12 9' }, c4);
    this.br = g(c4, { transform: 'translate(1000 470)' }); iconGroup(this.br, 120, C.ink); T(this.br, 0, 100, { de: 'Betriebsrat', en: 'Works council' }, { size: 28, weight: 800, anchor: 'middle' });
    this.brQ = g(c4, { transform: 'translate(1080 400)' }); iconUnknown(this.brQ, 60, C.amber);
    this.arb = pille(c4, { de: 'nationales Arbeitsrecht', en: 'national labour law' }, { icon: 'para', col: C.amber, size: 24 });
    this.zeit4 = g(c4);
    el('rect', { x: 300, y: 790, width: 1300, height: 4, rx: 2, fill: C.line }, this.zeit4);
    this.m1 = g(this.zeit4, { transform: 'translate(700 792)' }); el('circle', { r: 34, fill: C.raised, stroke: C.blue, 'stroke-width': 3 }, this.m1); iconPerson(this.m1, 40, C.ink); T(this.m1, 0, -50, { de: 'mit Fachperson klären', en: 'clarify with a specialist' }, { size: 24, weight: 800, anchor: 'middle' });
    this.m2 = g(this.zeit4, { transform: 'translate(1250 792)' }); el('circle', { r: 34, fill: C.raised, stroke: C.edge, 'stroke-width': 3 }, this.m2); iconDoc(this.m2, 40, C.ink); T(this.m2, 0, -50, { de: 'Beschaffung', en: 'Procurement' }, { size: 24, weight: 800, anchor: 'middle' });
    this.danach = g(this.zeit4, { transform: 'translate(1500 792)' }); el('circle', { r: 24, fill: 'none', stroke: C.red, 'stroke-width': 3, 'stroke-dasharray': '6 5' }, this.danach); iconCross(this.danach, 30, C.red); T(this.danach, 0, 58, { de: 'nicht danach', en: 'not after' }, { mono: 1, size: 18, fill: C.red, anchor: 'middle' });
    shot(b4, this.tU - 0.4, { typ: 'blende', d: 0.7 });

    // ---------- 5 neun Bereiche, kein amtlicher Katalog ----------
    const b5 = buehne('nicht-katalog', { seed: 113, regalDeckkraft: 0.6 }); this.b5 = b5;
    const c5 = b5.cam;
    this.k9 = Array.from({ length: 9 }, (_, i) => { const gr = g(c5); el('rect', { x: -70, y: -50, width: 140, height: 100, rx: 12, fill: '#eef2f8', stroke: '#d3dae6', 'stroke-width': 2 }, gr); T(gr, 0, 10, '§ ' + (i + 1), { mono: 1, size: 26, fill: C.blueDeep, anchor: 'middle' }); return gr; });
    this.kPlus = g(c5); el('rect', { x: -70, y: -50, width: 140, height: 100, rx: 12, fill: C.blueSoft, stroke: C.blue, 'stroke-width': 3 }, this.kPlus); T(this.kPlus, 0, 14, '+', { size: 46, weight: 800, fill: C.blueDeep, anchor: 'middle' });
    this.amtl = g(c5, { transform: 'translate(1460 330)' }); el('rect', { x: -170, y: -50, width: 340, height: 100, rx: 10, fill: 'none', stroke: C.dim, 'stroke-width': 3, 'stroke-dasharray': '12 9' }, this.amtl); T(this.amtl, 0, -6, { de: 'AMTLICHER KATALOG', en: 'OFFICIAL CATALOGUE' }, { mono: 1, size: 20, fill: C.dim, anchor: 'middle', ls: '0.1em' }); T(this.amtl, 0, 30, { de: 'nein', en: 'no' }, { size: 28, weight: 800, fill: C.muted, anchor: 'middle' });
    this.haus5 = g(c5, { transform: 'translate(1460 620)' }); el('circle', { r: 110, fill: 'url(#gPaper)' }, this.haus5); iconBuilding(this.haus5, 110, C.blue); T(this.haus5, 0, 100, { de: 'Ihr Betrieb entscheidet', en: 'Your business decides' }, { size: 30, weight: 800, anchor: 'middle' });
    this.zeigt = pille(c5, { de: 'Die Dokumente zeigen die Entscheidung', en: 'The documents show the decision' }, { icon: 'doc', col: C.blue, size: 24 });
    shot(b5, this.tNeun - 0.4, { typ: 'blende', d: 0.7 });
    this.buehnen = [b1, b2, b3, b4, b5];

    // ---------- Einblendungen ----------
    kopf(this.tKeine, this.tHB - 0.3, K, { de: 'Was die Dokumente zeigen', en: 'What the documents show' });
    kopf(this.tHB, this.tF - 0.3, K, { de: 'Was offen bleibt', en: 'What remains open' });
    kopf(this.tF, this.tU - 0.3, K, { de: 'Auftragnehmer und Dienstleister', en: 'Contractors and service providers' });
    kopf(this.tU, this.tNeun - 0.3, K, { de: 'Offen: Betriebsrat', en: 'Open: works council' });
    kopf(this.tNeun, this.tEnde - 0.3, K, { de: 'Kein amtlicher Katalog', en: 'Not an official catalogue' });
  },

  zeichnen(t) {
    if (this.b1.vis) {
      kamera(this.b1, [960, 540], 1);
      const si = P(t, this.tKeine - 0.3, 0.8, E.out); tr(this.stapel, 960, 560 + (1 - si) * 40, 0.9); O(this.stapel, si);
      rein(this.keineRB, 960, 250, t, this.tKeine + 0.3, 0.45, this.tZ[0] - 0.3);
      rein(this.keineZ, 960, 880, t, this.tKein, 0.45, this.tZ[0] - 0.3);
      this.fac.forEach((f, i) => rein(f, this.FPOS[i][0], this.FPOS[i][1], t, this.tZ[i], 0.45));
      this.facL.forEach((l, i) => O(l, P(t, this.tZ[i] + 0.1, 0.4)));
    }
    if (this.b2.vis) {
      kamera(this.b2, [960, 540], 1);
      const hi = P(t, this.tHB - 0.2, 0.6, E.out); O(this.hb, hi); tr(this.hb, 0, (1 - hi) * 30);
      this.punkte.forEach((p, i) => { const k = P(t, this.t17 + i * 0.06, 0.35, E.back); sk(p.g, p.x, p.y, Math.max(0.01, k)); O(p.g, P(t, this.t17 + i * 0.06, 0.2) * (p.off ? 1 : 1 - 0.5 * P(t, this.tAcht + 0.4, 0.5))); });
      rein(this.zaehl, 540, 840, t, this.tAcht, 0.45);
      this.op.forEach((o, i) => { const k = P(t, this.tO[i] - 0.1, 0.5, E.out); O(o, k); tr(o, (1 - k) * 40, 0); });
    }
    if (this.b3.vis) {
      kamera(this.b3, [960, 540], 1);
      zeichne(this.bereich, P(t, this.tWeis - 0.6, 1.0)); O(this.bereichLab, P(t, this.tWeis - 0.2, 0.4));
      O(this.haus3, P(t, this.tF, 0.5)); this.leute.forEach((l, i) => O(l, P(t, this.tF + 0.3 + i * 0.15, 0.3)));
      this.extern.forEach((e, i) => { const k = P(t, this.tAuftr + i * 0.4, 0.6, E.out); e.setAttribute('transform', `translate(${[960, 1000][i] + (1 - k) * 300} ${[450, 660][i]})`); O(e, k); });
      rein(this.art4, 760, 812, t, this.tWeis + 0.3, 0.45);
      zeichne(this.vLinie, P(t, this.tVertrag - 0.3, 0.6)); this.vLinie.setAttribute('stroke-dasharray', P(t, this.tVertrag + 0.3, 0.01) > 0 ? '10 8' : this.vLinie.getAttribute('stroke-dasharray'));
      const vk = P(t, this.tVertrag, 0.45, E.back); this.vertrag.setAttribute('transform', `translate(1560 560) scale(${Math.max(0.01, vk).toFixed(3)})`); O(this.vertrag, P(t, this.tVertrag, 0.2));
    }
    if (this.b4.vis) {
      kamera(this.b4, [960, 540], 1);
      O(this.tool4, P(t, this.tU, 0.5)); zeichne(this.pfeil4, P(t, this.tU + 0.4, 0.6)); this.pfeil4.setAttribute('stroke-dasharray', P(t, this.tU + 1.0, 0.01) > 0 ? '12 9' : this.pfeil4.getAttribute('stroke-dasharray')); this.pfeil4.setAttribute('stroke-dashoffset', (-t * 30).toFixed(1));
      O(this.br, P(t, this.tBR - 0.2, 0.5)); const q = P(t, this.tBR + 0.2, 0.45, E.back); this.brQ.setAttribute('transform', `translate(1080 400) scale(${Math.max(0.01, q).toFixed(3)})`); O(this.brQ, P(t, this.tBR + 0.2, 0.2));
      rein(this.arb, 1000, 640, t, this.tArb, 0.45);
      O(this.zeit4, P(t, this.tFach - 0.3, 0.5));
      O(this.m1, P(t, this.tFach, 0.4)); O(this.m2, P(t, this.tVor, 0.4));
      const d = P(t, this.tDanach, 0.45, E.back); this.danach.setAttribute('transform', `translate(1500 792) scale(${Math.max(0.01, d).toFixed(3)})`); O(this.danach, P(t, this.tDanach, 0.2));
    }
    if (this.b5.vis) {
      kamera(this.b5, [960, 540], 1);
      const merge = P(t, this.tZus, 0.8, E.io);
      this.k9.forEach((k, i) => {
        let x = 480 + (i % 3) * 170, y = 380 + Math.floor(i / 3) * 130;
        if (i === 8) x = lerp(x, 480 + 170, merge);
        if (i === 7) setText(k.lastChild, merge > 0.6 ? '§ 8 + 9' : '§ 8');
        tr(k, x, y, 1, 0); O(k, P(t, this.tNeun + i * 0.07, 0.3) * (i === 8 ? 1 - 0.9 * merge : 1));
      });
      const pk = P(t, this.tErg, 0.45, E.back); tr(this.kPlus, 480 + 340, 380 + 2 * 130, Math.max(0.01, pk)); O(this.kPlus, P(t, this.tErg, 0.2));
      O(this.amtl, P(t, this.tAmtl - 0.1, 0.4));
      rein(this.haus5, 1460, 620, t, this.tEnt - 0.1, 0.5);
      rein(this.zeigt, 1460, 880, t, this.tZeigen, 0.45);
    }
  },
});
