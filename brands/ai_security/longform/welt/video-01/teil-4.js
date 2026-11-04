// Teil 4 · Verlangt ein Gesetz eine Richtlinie? Absätze 28 bis 36 des Skripts.
// Bühnen: drei Gesetze und die drei nächstliegenden Artikel (Auslegung) → drei Stellen, die eine Richtlinie empfehlen (Fakten),
// ihre Reichweite (Auslegung) → offen: Geheimhaltungsmaßnahme (Unsicher) → offen: Aufsicht (Unsicher).
akt({
  name: 'gesetz',
  bauen() {
    const c = (de, en) => cue({ de, en }).s;
    const K = { de: '3 · VERLANGT EIN GESETZ EINE RICHTLINIE?', en: '3 · DOES A LAW REQUIRE A POLICY?' };
    this.tFrage = c('Jetzt die Frage', 'Now the question');
    this.tVerlangt = c('Verlangt irgendein Gesetz', 'does any law require');
    const A29 = belegt(); this.tA29 = A29.s;
    this.tKIVO = c('die KI-Verordnung noch', 'the AI Act nor');
    this.tDSGVO = c('die DSGVO enthält', 'the GDPR contains');
    this.tAusdr = c('ausdrücklich verpflichtet', 'explicitly requires');
    this.tDreiArt = c('Drei Artikel', 'Three articles');
    this.tArt = [c('Artikel vier der|Artikel 4 der', 'Article four of|Article 4 of'), c('Artikel vierundzwanzig|Artikel 24', 'Article twenty-four|Article 24|Article twenty four'), c('Geschäftsgeheimnis-Richtlinie schützt|Geschäftsgeheimnisrichtlinie schützt', 'Trade Secrets Directive protects')];
    this.tKeiner = c('Keiner sagt', 'None of them says');
    this.tWeg = c('der übliche Weg', 'the usual way');
    this.tPflicht = c('keine eigene Pflicht', 'not a duty of its own');
    this.tWarum = c('Warum dann eine schreiben', 'So why write one');
    this.tDreiSt = c('drei Stellen', 'three bodies');
    const D31 = belegt(); this.tD31 = D31.s;
    this.tWeis = c('Weisungen erteilt', 'instructions should be issued');
    this.tW4 = [c('ob, unter welchen', 'whether, under which'), c('Voraussetzungen', 'conditions'), c('konkreten Zwecken', 'concrete purposes'), c('welche KI-Anwendungen', 'which AI applications')];
    const B32 = belegt(); this.tB32 = B32.s;
    this.tM16 = c('Seine Maßnahme|Maßnahme M16|Maßnahme M', 'Its measure|measure M16|measure M');
    this.tB3 = [c('welche KI-Modelle', 'which AI models'), c('welche Eingaben', 'which inputs'), c('wie Ausgaben', 'how outputs')];
    { const v = cue({ de: 'verbindlich', en: 'bindingly' }, { leise: true, weit: 30 }); this.tVerb = v ? v.s : this.tB3[2] + 1.8; if (v) CUR = v.j; }
    const W33 = belegt(); this.tW33 = W33.s;
    this.tMuster = c('kostenloses Muster', 'free model policy');
    this.tZehn = c('zehn nummerierten|10 nummerierten', 'ten numbered|10 numbered');
    this.tUeber = c('überholt', 'out of date');
    const A34 = belegt(); this.tA34 = A34.s;
    this.tDeAt = c('deutsch und österreichisch', 'German and Austrian');
    this.tKeinR = c('kein Recht', 'not law');
    this.tBinden = c('binden außerhalb', 'bind nobody');
    this.tBeste = c('beste veröffentlichte', 'best published');
    this.tNeun = c('neun Regelbereiche', 'nine areas');
    const U35 = belegt(); this.tU35 = U35.s;
    this.tGericht = c('Gerichtsentscheidung', 'court decision');
    this.tOhne = c('Ohne Regel', 'Without a rule');
    this.tMit = c('mit Regel', 'with a rule');
    this.tEinzel = c('im Einzelfall', 'case by case');
    const U36 = belegt(); this.tU36 = U36.s;
    this.tDE = c('Deutschland hat', 'Germany has');
    this.tKraft = c('in Kraft ist', 'in force since');
    this.tAT = c('Für Österreich', 'For Austria');
    this.tGelten = c('Die Pflichten gelten', 'The duties apply');
    this.tEnde = cue({ de: 'Zwei Fälle zum Mitentscheiden', en: 'Two cases for you' }, { halten: true }).s;
    // Ton (Langfassung 03.11.2026)
    (this.tArt || []).forEach((t) => klang(t, 'pop', { laut: 0.5 })); klang(this.tKeiner, 'thud_low', { laut: 0.5 });
    (this.tW4 || []).forEach((t) => klang(t, 'tick', { laut: 0.5 })); (this.tB3 || []).forEach((t) => klang(t, 'tick', { laut: 0.5 }));
    klang(this.tZehn, 'paper_slide'); klang(this.tUeber, 'strike', { laut: 0.6 }); klang(this.tOhne, 'pop', { laut: 0.5 }); klang(this.tMit, 'pop', { laut: 0.5 });

    // ---------- Bühne 1: drei Gesetze ----------
    const bG = buehne('gesetz-buecher', { seed: 61 }); this.bG = bG;
    const gc = bG.cam;
    this.frage = T(gc, 960, 300, { de: 'Pflicht zur schriftlichen Richtlinie?', en: 'A duty to keep a written policy?' }, { size: 52, weight: 800, anchor: 'middle' });
    const BUCH = [{ de: 'KI-VO', en: 'AI ACT' }, { de: 'DSGVO', en: 'GDPR' }, { de: 'RL 2016/943', en: 'DIR 2016/943' }];
    const BSUB = [{ de: 'VO (EU) 2024/1689', en: 'Reg. (EU) 2024/1689' }, { de: 'VO (EU) 2016/679', en: 'Reg. (EU) 2016/679' }, { de: 'Geschäftsgeheimnisse', en: 'Trade secrets' }];
    this.BX = [500, 960, 1420];
    this.buecher = BUCH.map((b, i) => {
      const gr = g(gc);
      el('rect', { x: -95, y: -120, width: 190, height: 240, rx: 10, fill: '#1c2a47', stroke: C.edge, 'stroke-width': 3 }, gr);
      el('rect', { x: -95, y: -120, width: 30, height: 240, rx: 8, fill: '#2a3c62' }, gr);
      T(gr, 18, -40, b, { mono: 1, size: 24, fill: C.ink, anchor: 'middle', ls: '0.06em' });
      T(gr, 18, -8, BSUB[i], { mono: 1, size: 14, fill: C.muted, anchor: 'middle' });
      el('rect', { x: -40, y: 50, width: 116, height: 6, rx: 3, fill: C.line }, gr);
      el('rect', { x: -40, y: 66, width: 80, height: 6, rx: 3, fill: C.line }, gr);
      return gr;
    });
    this.lupe = g(gc); el('circle', { r: 70, fill: 'url(#gBlue)' }, this.lupe); iconSearch(this.lupe, 110, C.blue);
    this.keinePf = [0, 1].map(() => pille(gc, { de: 'keine Pflicht zur Richtlinie', en: 'no duty to keep a policy' }, { icon: 'cross', col: C.muted, gestrichelt: true, size: 18 }));
    const ART = [
      [{ de: 'Art. 4', en: 'Art. 4' }, { de: 'Maßnahmen für KI-Kompetenz', en: 'measures for AI literacy' }],
      [{ de: 'Art. 24 Abs. 1', en: 'Art. 24(1)' }, { de: 'technische und organisatorische Maßnahmen', en: 'technical and organisational measures' }],
      [{ de: 'Art. 2 Abs. 1 Buchst. c', en: 'Art. 2(1)(c)' }, { de: 'angemessene Geheimhaltungsmaßnahmen', en: 'reasonable steps to keep secrets' }],
    ];
    this.karten = ART.map(([a, txt]) => {
      const gr = g(gc);
      const b = blatt(gr, { w: 420, h: 230, pad: 24, back: false });
      T(b.g, b.left, b.y0 + 46, a, { mono: 1, size: 20, fill: C.blueDeep, ls: '0.04em' });
      TB(b.g, b.left, b.y0 + 88, txt, { size: 24, weight: 800, fill: C.pInk, maxW: 372, lh: 28 });
      const rl = g(b.g); el('rect', { x: b.left - 4, y: b.y0 + 180, width: 200, height: 32, rx: 8, fill: 'none', stroke: C.pMuted, 'stroke-width': 2, 'stroke-dasharray': '7 5' }, rl);
      T(rl, b.left + 8, b.y0 + 202, { de: '„Richtlinie“: —', en: '"policy": —' }, { mono: 1, size: 17, fill: C.pMuted });
      return { g: gr, rl };
    });
    this.rl = g(gc);
    const rb = blatt(this.rl, { w: 300, h: 110, pad: 20, back: false });
    T(rb.g, 0, 8, { de: 'KI-Richtlinie', en: 'AI policy' }, { size: 30, weight: 800, fill: C.pInk, anchor: 'middle' });
    T(rb.g, 0, 38, { de: 'ÜBLICHER WEG', en: 'USUAL WAY' }, { mono: 1, size: 15, fill: C.blueDeep, anchor: 'middle', ls: '0.1em' });
    this.rlLinien = this.BX.map((x) => el('path', { d: `M 960 760 C 960 720 ${x} 720 ${x} 690`, fill: 'none', stroke: C.blue, 'stroke-width': 4, 'stroke-linecap': 'round' }, gc));
    gc.insertBefore(this.rlLinien[0], this.rl); gc.insertBefore(this.rlLinien[1], this.rl); gc.insertBefore(this.rlLinien[2], this.rl);
    this.pflichtP = pille(gc, { de: 'keine eigene Pflicht', en: 'not a duty of its own' }, { col: C.purple, gestrichelt: true, size: 22, marke: 'auslegung' });
    shot(bG, this.tFrage - 0.5, { typ: 'schwarz', d: 0.9 });

    // ---------- Bühne 2: drei Stellen ----------
    const bS = buehne('gesetz-stellen', { seed: 67, regalDeckkraft: 0.6 }); this.bS = bS;
    const sc = bS.cam;
    this.SX = [380, 960, 1540];
    const ST = [[{ de: 'Datenschutzkonferenz', en: 'Data protection conference' }, 'DE'], [{ de: 'BSI', en: 'BSI (Federal Office)' }, 'DE'], [{ de: 'Wirtschaftskammer', en: 'Economic Chamber' }, 'AT']];
    this.stellen = ST.map(([n, land], i) => {
      const gr = g(sc, { transform: `translate(${this.SX[i]} 0)` });
      el('circle', { cx: 0, cy: 290, r: 90, fill: 'url(#gPaper)' }, gr);
      const ic = g(gr, { transform: 'translate(0 285)' }); iconInstitution(ic, 72, C.ink);
      T(gr, 0, 362, n, { size: 26, weight: 800, anchor: 'middle' });
      const lt = g(gr); const p = pille(lt, land, { col: C.blue, size: 20 }); tr(p, 0, 404);
      return { g: gr, land: lt };
    });
    const blattS = (i, kicker, zeilen) => {
      const gr = g(sc);
      const b = blatt(gr, { w: 460, h: 340, kicker, pad: 26, kSize: 13 });
      const z = zeilen.map((txt, k) => { const zg = g(b.g); const y = b.y + 26 + k * 62; el('circle', { cx: b.left + 10, cy: y - 8, r: 7, fill: C.blueDeep }, zg); TB(zg, b.left + 28, y, txt, { size: 22, weight: 700, fill: C.pInk, maxW: 384, lh: 25 }); return zg; });
      return { g: gr, b, z };
    };
    this.s1 = blattS(0, { de: 'WEISUNGEN · ERTEILT UND DOKUMENTIERT', en: 'INSTRUCTIONS · ISSUED AND DOCUMENTED' }, [{ de: 'ob', en: 'whether' }, { de: 'unter welchen Voraussetzungen', en: 'under which conditions' }, { de: 'zu welchen Zwecken', en: 'for which purposes' }, { de: 'welche KI-Anwendungen', en: 'which AI applications' }]);
    this.s2 = blattS(1, { de: 'MASSNAHME M16 · S. 49', en: 'MEASURE M16 · P. 49' }, [{ de: 'Modelle und Anwendungen: wofür', en: 'models and applications: for what' }, { de: 'Eingaben: welche zulässig', en: 'inputs: which are permitted' }, { de: 'Ausgaben: wie weiterverwendet', en: 'outputs: how they are reused' }]);
    this.verb = stempel(this.s2.b.g, { de: 'VERBINDLICH', en: 'BINDING' }, C.blueDeep, 20);
    this.s3 = blattS(2, { de: 'MUSTER · KI-GUIDELINES FÜR KMU', en: 'MODEL · AI GUIDELINES FOR SMEs' }, []);
    this.paras = Array.from({ length: 10 }, (_, k) => { const zg = g(this.s3.b.g); const col = k % 2, row = Math.floor(k / 2); const x = this.s3.b.left + col * 190, y = this.s3.b.y + 24 + row * 44; T(zg, x, y, '§ ' + (k + 1), { mono: 1, size: 18, fill: C.blueDeep }); el('rect', { x: x + 52, y: y - 10, width: 100, height: 9, rx: 4.5, fill: C.pBar2 }, zg); return zg; });
    this.ueber = stempel(this.s3.b.g, { de: 'TEILS ÜBERHOLT', en: 'PARTLY OUT OF DATE' }, C.amberDeep, 18);
    this.ueberDatum = pille(sc, { de: 'seit 8. Juli 2026', en: 'since 8 July 2026' }, { icon: 'calendar', col: C.amber, size: 20 });
    this.grenze = el('rect', { x: 120, y: 200, width: 1680, height: 620, rx: 30, fill: 'none', stroke: C.purple, 'stroke-width': 3, 'stroke-dasharray': '14 10' }, sc);
    this.grenzeLab = pille(sc, { de: 'DE · AT · fachlicher Stand, kein Recht', en: 'DE · AT · professional practice, not law' }, { col: C.purple, size: 22, marke: 'auslegung' });
    this.neun = Array.from({ length: 9 }, (_, i) => { const gr = g(sc); el('rect', { x: -38, y: -24, width: 76, height: 48, rx: 8, fill: C.raised, stroke: C.blue, 'stroke-width': 2 }, gr); T(gr, 0, 8, '§ ' + (i + 1), { mono: 1, size: 18, fill: C.ink, anchor: 'middle' }); return gr; });
    this.neunLinien = this.SX.map((x) => el('path', { d: `M ${x} 800 C ${x} 840 960 830 960 862`, fill: 'none', stroke: C.blue, 'stroke-width': 3, 'stroke-dasharray': '8 6' }, sc));
    this.maske = el('path', { d: 'M -80 -80 H 2000 V 1160 H -80 Z M 150 200 H 1770 Q 1800 200 1800 230 V 790 Q 1800 820 1770 820 H 150 Q 120 820 120 790 V 230 Q 120 200 150 200 Z', fill: C.ground, 'fill-rule': 'evenodd' }, sc);
    this.aussenP = pille(sc, { de: 'außerhalb von DE und AT: bindend für niemanden', en: 'outside DE and AT: binding on nobody' }, { col: C.muted, gestrichelt: true, size: 22 }); tr(this.aussenP, 960, 900);
    shot(bS, this.tWarum - 0.4, { typ: 'blende', d: 0.7 });

    // ---------- Bühne 3: offen, Geheimhaltungsmaßnahme ----------
    const bU = buehne('gesetz-geheimnis', { seed: 19, regalDeckkraft: 0.6 }); this.bU = bU;
    const uc = bU.cam;
    this.tor = g(uc);
    el('rect', { x: 860, y: 380, width: 12, height: 300, rx: 5, fill: C.amber }, this.tor); el('rect', { x: 1048, y: 380, width: 12, height: 300, rx: 5, fill: C.amber }, this.tor); el('rect', { x: 852, y: 368, width: 216, height: 16, rx: 6, fill: C.amber }, this.tor);
    T(this.tor, 960, 340, '3', { mono: 1, size: 30, fill: C.amber, anchor: 'middle' });
    TB(this.tor, 860, 730, { de: 'angemessene Geheimhaltungsmaßnahme?', en: 'a reasonable step to keep it secret?' }, { size: 26, weight: 800, maxW: 300, lh: 31, fill: C.amber });
    this.torQ = g(uc, { transform: 'translate(960 530)' }); iconUnknown(this.torQ, 110, C.amber);
    this.ohne = g(uc, { transform: 'translate(430 530)' });
    el('rect', { x: -120, y: -150, width: 240, height: 300, rx: 10, fill: 'none', stroke: C.dim, 'stroke-width': 3, 'stroke-dasharray': '12 9' }, this.ohne);
    T(this.ohne, 0, 8, '—', { size: 60, weight: 800, fill: C.dim, anchor: 'middle' });
    TB(this.ohne, -120, 200, { de: 'ohne Regel: kein Anhaltspunkt', en: 'without a rule: no evidence' }, { size: 24, weight: 700, maxW: 260, lh: 29, fill: C.muted });
    this.mit = g(uc);
    const mb = blatt(this.mit, { w: 240, h: 300, kicker: { de: 'RICHTLINIE', en: 'POLICY' }, pad: 22, kSize: 13 });
    linien(mb.g, mb.left, mb.y + 6, 180, 7, 26, C.pBar2, 9);
    this.mitLab = TB(uc, 1370, 730, { de: 'mit Regel: Maßnahme zeigbar', en: 'with a rule: a step can be shown' }, { size: 24, weight: 700, maxW: 280, lh: 29 });
    this.gavel = g(uc, { transform: 'translate(1580 300)' }); el('circle', { r: 56, fill: 'none', stroke: C.muted, 'stroke-width': 3, 'stroke-dasharray': '10 8' }, this.gavel); iconGavel(this.gavel, 60, C.muted);
    this.gavelLab = T(uc, 1650, 310, { de: 'nicht gesucht', en: 'not searched' }, { mono: 1, size: 22, fill: C.muted });
    this.einzel = pille(uc, { de: 'Einzelfall', en: 'case by case' }, { marke: 'unsicher', col: C.amber, size: 24 });
    shot(bU, this.tU35 - 0.4, { typ: 'blende', d: 0.7 });

    // ---------- Bühne 4: offen, Aufsicht ----------
    const bA = buehne('gesetz-aufsicht', { seed: 71, regalDeckkraft: 0.6 }); this.bA = bA;
    const ac = bA.cam;
    this.frageA = T(ac, 960, 262, { de: 'Wer beaufsichtigt Artikel 4?', en: 'Who supervises Article 4?' }, { size: 46, weight: 800, anchor: 'middle' });
    this.de = g(ac);
    karte(this.de, 330, 320, 560, 340, { fill: C.surface, stroke: C.blue });
    T(this.de, 370, 380, { de: 'DEUTSCHLAND', en: 'GERMANY' }, { mono: 1, size: 22, fill: C.blue, ls: '0.12em' });
    { const ic = g(this.de, { transform: 'translate(430 480)' }); iconInstitution(ic, 80, C.ink); }
    T(this.de, 500, 468, { de: 'Bundesnetzagentur', en: 'Federal Network Agency' }, { size: 28, weight: 800 });
    T(this.de, 500, 508, { de: 'benannt durch das KI-MIG', en: 'named by the KI-MIG act' }, { size: 22, weight: 600, fill: C.muted });
    this.deKraft = pille(this.de, { de: 'in Kraft seit 29. Juli 2026', en: 'in force since 29 July 2026' }, { icon: 'calendar', col: C.blue, size: 20 });
    tr(this.deKraft, 610, 600);
    this.at = g(ac);
    karte(this.at, 1030, 320, 560, 340, { fill: C.surface, stroke: C.amber, gestrichelt: true });
    T(this.at, 1070, 380, { de: 'ÖSTERREICH', en: 'AUSTRIA' }, { mono: 1, size: 22, fill: C.amber, ls: '0.12em' });
    { const ic = g(this.at, { transform: 'translate(1130 480)' }); el('circle', { r: 50, fill: 'none', stroke: C.amber, 'stroke-width': 3, 'stroke-dasharray': '10 8' }, ic); iconUnknown(ic, 60, C.amber); }
    TB(this.at, 1200, 468, { de: 'keine amtliche Quelle nennt die Behörde', en: 'no official source names the authority' }, { size: 26, weight: 800, maxW: 360, lh: 31 });
    this.atStand = pille(this.at, { de: 'Stand 23. Oktober 2026', en: 'as of 23 October 2026' }, { icon: 'calendar', col: C.amber, size: 20 });
    tr(this.atStand, 1310, 600);
    this.pflichten = g(ac);
    el('rect', { x: 330, y: 700, width: 1260, height: 66, rx: 33, fill: C.blue }, this.pflichten);
    T(this.pflichten, 960, 743, { de: 'Die Pflichten gelten trotzdem', en: 'The duties apply regardless' }, { size: 30, weight: 800, anchor: 'middle', fill: '#fff' });
    shot(bA, this.tU36 - 0.4, { typ: 'blende', d: 0.7 });
    this.buehnen = [bG, bS, bU, bA];

    // ---------- Einblendungen ----------
    kopf(this.tFrage, this.tDreiArt - 0.3, K, '');
    kopf(this.tDreiArt, this.tWarum - 0.3, K, { de: 'Drei Artikel kommen am nächsten', en: 'Three articles come closest' });
    kopf(this.tWarum, this.tA34 - 0.3, K, { de: 'Drei Stellen empfehlen sie', en: 'Three bodies recommend it' });
    kopf(this.tA34, this.tU35 - 0.3, K, { de: 'Fachlicher Stand, kein Recht', en: 'Practice, not law' });
    kopf(this.tU35, this.tU36 - 0.3, K, { de: 'Offen: angemessene Maßnahme?', en: 'Open: a reasonable step?' });
    kopf(this.tU36, this.tEnde - 0.3, K, { de: 'Offen: welche Aufsicht', en: 'Open: which authority' });
  },

  zeichnen(t) {
    if (this.bG.vis) {
      const hoch = P(t, this.tDreiArt - 0.3, 0.8);
      kamera(this.bG, [960, 540], 1);
      O(this.frage, fenster(t, this.tVerlangt - 0.2, 0.5, this.tDreiArt - 0.4, 0.4));
      this.buecher.forEach((b, i) => { const k = P(t, this.tFrage + 0.2 + i * 0.2, 0.5, E.out); tr(b, this.BX[i], lerp(540, 330, hoch) + (1 - k) * 30, lerp(1, 0.8, hoch)); O(b, k); });
      // Lupe sucht in KI-VO und DSGVO
      const l1 = P(t, this.tKIVO - 0.2, 0.7), l2 = P(t, this.tDSGVO - 0.2, 0.7);
      const lx = lerp(lerp(300, this.BX[0], l1), this.BX[1], l2);
      tr(this.lupe, lx + 40, lerp(540, 330, hoch) + 40 + 8 * Math.sin(t * 4), 1); O(this.lupe, fenster(t, this.tKIVO - 0.3, 0.4, this.tDreiArt - 0.3, 0.4));
      this.keinePf.forEach((p, i) => rein(p, this.BX[i], 720, t, i === 0 ? this.tAusdr - 0.4 : this.tAusdr + 0.1, 0.45, this.tDreiArt - 0.3));
      this.karten.forEach((k, i) => { const kk = P(t, this.tArt[i] - 0.1, 0.6, E.out); tr(k.g, this.BX[i], 560 + (1 - kk) * 40, 1, i === 1 ? 0.6 : -0.6); O(k.g, kk * (1 - 0.0)); O(k.rl, P(t, this.tKeiner + i * 0.15, 0.3)); });
      const rk = P(t, this.tWeg - 0.3, 0.6, E.out);
      tr(this.rl, 960, 800 + (1 - rk) * 30); O(this.rl, rk);
      this.rlLinien.forEach((l, i) => zeichne(l, P(t, this.tWeg + 0.2 + i * 0.15, 0.5)));
      rein(this.pflichtP, 1460, 800, t, this.tPflicht, 0.45);
    }
    if (this.bS.vis) {
      kamera(this.bS, [960, 540], 1);
      const st = [this.tD31, this.tB32, this.tW33];
      const reich = P(t, this.tA34 - 0.2, 0.6);
      this.stellen.forEach((s, i) => { const k = P(t, this.tDreiSt + i * 0.25, 0.5, E.out); tr(s.g, this.SX[i], (1 - k) * 30); const akt0 = t > st[i] - 0.3 && t < (st[i + 1] || this.tA34) - 0.3 ? 1 : 0; O(s.g, k * (reich > 0 ? 1 : (st.some((x) => t > x - 0.3) ? (akt0 ? 1 : 0.45) : 1))); O(s.land, P(t, this.tDeAt + i * 0.2, 0.4)); });
      [this.s1, this.s2, this.s3].forEach((s, i) => { const k = P(t, st[i] - 0.1, 0.6, E.out); tr(s.g, this.SX[i], 600 + (1 - k) * 40, lerp(1, 0.86, reich), i === 1 ? 0.5 : -0.5); O(s.g, k); });
      this.s1.z.forEach((z, k) => O(z, P(t, (k === 0 ? this.tW4[0] : this.tW4[k]) + (k === 0 ? 0 : 0) - 0.1, 0.3)));
      this.s2.z.forEach((z, k) => O(z, P(t, this.tB3[k] - 0.1, 0.3)));
      const vb = P(t, this.tVerb, 0.4, E.back); this.verb.setAttribute('transform', `translate(${this.s2.b.right - 70} ${this.s2.b.y0 + this.s2.b.h - 44}) rotate(-6) scale(${Math.max(0.01, vb).toFixed(3)})`); O(this.verb, P(t, this.tVerb, 0.2));
      this.paras.forEach((p, k) => O(p, P(t, this.tZehn + k * 0.08, 0.2)));
      const ub = P(t, this.tUeber - 0.2, 0.4, E.back); this.ueber.setAttribute('transform', `translate(${this.s3.b.right - 110} ${this.s3.b.y0 + this.s3.b.h - 40}) rotate(-5) scale(${Math.max(0.01, ub).toFixed(3)})`); O(this.ueber, P(t, this.tUeber - 0.2, 0.2));
      rein(this.ueberDatum, 1540, 815, t, this.tUeber + 0.2, 0.45, this.tA34 - 0.2);
      zeichne(this.grenze, P(t, this.tDeAt + 0.6, 1.0)); O(this.grenze, reich);
      rein(this.grenzeLab, 1300, 200, t, this.tKeinR - 0.2, 0.45);
      this.neun.forEach((n, i) => { const k = P(t, this.tNeun + i * 0.07, 0.4, E.back); tr(n, 960 + (i - 4) * 92, 880, Math.max(0.01, k)); O(n, P(t, this.tNeun + i * 0.07, 0.2)); });
      this.neunLinien.forEach((l, i) => zeichne(l, P(t, this.tNeun - 0.2, 0.6)));
      // außerhalb: die Welt außerhalb des Rahmens wird dunkler
      const aussen = fenster(t, this.tBinden, 0.5, this.tBeste, 0.5); O(this.maske, 0.55 * aussen); O(this.aussenP, aussen);
    }
    if (this.bU.vis) {
      kamera(this.bU, [960, 540], 1);
      O(this.tor, P(t, this.tU35, 0.5));
      const qk = P(t, this.tU35 + 0.4, 0.45, E.back); this.torQ.setAttribute('transform', `translate(960 530) scale(${Math.max(0.01, qk * (1 + 0.1 * puls(t, this.tEinzel, 1, 8))).toFixed(3)})`); O(this.torQ, P(t, this.tU35 + 0.4, 0.2));
      O(this.gavel, P(t, this.tGericht, 0.4)); O(this.gavelLab, P(t, this.tGericht + 0.3, 0.4));
      O(this.ohne, P(t, this.tOhne, 0.5));
      const mk = P(t, this.tMit - 0.1, 0.8, E.out); tr(this.mit, lerp(1600, 1460, mk), 530, 1, lerp(6, 2, mk)); O(this.mit, mk); O(this.mitLab, P(t, this.tMit + 0.3, 0.4));
      rein(this.einzel, 960, 860, t, this.tEinzel, 0.45);
    }
    if (this.bA.vis) {
      kamera(this.bA, [960, 540], 1);
      O(this.frageA, P(t, this.tU36, 0.5));
      rein(this.de, 0, 0, t, this.tDE - 0.2, 0.6); rein(this.at, 0, 0, t, this.tAT - 0.2, 0.6);
      O(this.deKraft, P(t, this.tKraft - 0.4, 0.4)); O(this.atStand, P(t, this.tAT + 1.2, 0.4));
      const pk = P(t, this.tGelten - 0.1, 0.5, E.out); tr(this.pflichten, 0, (1 - pk) * 20); O(this.pflichten, pk);
    }
  },
});
