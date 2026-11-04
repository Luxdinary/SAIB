// Teil 3a · Fünf Schritte zu einer ehrlichen Antwort, Überblick, Schritt 1 und Schritt 2 (Absätze 7 bis 11).
// Bühnen: Weg mit fünf Stationen → Kunde mit zehn Bereichen und seinen Lieferanten (Fakt Art. 21, Auslegung, Fakt Art. 32 DSGVO)
// → die vier Antworten mit Beispielantwort (Lücke, Termin, Person).
akt({
  name: 'loesung-1',
  bauen() {
    const c = (de, en, o) => cue({ de, en }, o).s;
    // ---------- Wortanker ----------
    this.tWas = c('Was der Betrieb tut', 'What the business does');
    this.tFuenf = c('fünf Schritten', 'five steps');
    this.tOhne = c('ohne Toolkit', 'without any toolkit');
    this.tSchneller = c('nur schneller', 'only makes them faster');
    const F1 = belegt(); this.tS1 = F1.s;
    this.tWer = c('fragt und warum', 'is asking and why'); // „wer“ und „who“ hat belegt() schon gelesen
    this.tErfasst = c('erfasst', 'covered by');
    this.tZehn = c('zehn Bereichen', 'ten areas');
    this.tLiefer = c('Sicherheit der Lieferkette', 'supply chain security');
    this.tUnmittel = c('unmittelbaren Anbietern', 'direct suppliers');
    this.tPraxis = c('Cybersicherheitspraxis', 'cybersecurity practices', { halten: true }); // im Englischen umgekehrte Reihenfolge
    this.tBer = c('berücksichtigen', 'into account'); this.tLupe = Math.min(this.tPraxis, this.tBer);
    const A1 = belegt(); this.tA1 = A1.s;
    this.tIstFB = c('der Fragebogen', 'the questionnaire'); // „Das ist“ hat belegt() schon gelesen
    this.tBillig = c('billigste Weg', 'cheapest way');
    this.tHundert = c('hunderte Lieferanten', 'hundreds of suppliers');
    this.tFolgen = c('zehn Bereichen des Kunden', 'own ten areas');
    this.tAntw = c('Ihre Antworten können', 'your answers can');
    this.tBindet = c('bindet den Kunden', 'binds the customer');
    this.tVertrag = c('der Vertrag', 'the contract');
    this.tDSGVO = c('die DSGVO selbst', 'the GDPR itself');
    const F2 = belegt(); this.tF2 = F2.s;
    this.tTOM = c('technischen und organisatorischen', 'technical and organisational');
    this.tWieder = c('rasch wiederherzustellen', 'ability to restore');
    this.tUeber = c('regelmäßigen Überprüfung', 'regularly testing');
    const Q3 = quelle(); this.tS2 = Q3.s;
    this.tVier = c('vier Antworten', 'four answers');
    this.tAn = [c('Vorhanden', 'In place'), c('Teilweise', 'Partly'), c('Noch nicht, mit Termin', 'Not yet, with a date'), c('Nicht anwendbar', 'Not applicable')];
    this.tNichts = c('Nichts anderes', 'Nothing else');
    this.tKeinJa = c('Kein Ja', 'Not yes');
    this.tLeeres = c('kein leeres Feld', 'not a blank');
    this.tBsp = c('Eine Antwort wie', 'An answer like');
    this.tQuartal = c('Ende des Quartals', 'end of the quarter');
    this.tVerantw = c('verantwortlich', 'responsible');
    this.tVollst = c('ist vollständig', 'is complete');
    this.tLuecke = c('eine Lücke', 'a gap');
    this.tTermin = c('einen Termin', 'a date');
    this.tPerson = c('eine Person', 'a person');
    this.tEnde = cue({ de: 'Schritt drei', en: 'Step three' }, { halten: true }).s;

    // ---------- Bühne W: der Weg ----------
    const bW = buehne('loesung-weg', { seed: 29, regalDeckkraft: 0.6 }); this.bW = bW;
    this.Wg = bauWeg5(bW.cam);
    this.tk = pille(bW.cam, { de: 'Toolkit: nur schneller', en: 'Toolkit: only faster' }, { icon: 'book', col: C.blue, gestrichelt: true, size: 26 });
    this.ohneP = pille(bW.cam, { de: 'alle fünf ohne Toolkit', en: 'all five without a toolkit' }, { icon: 'check', col: C.muted, size: 26 });
    shot(bW, this.tWas - 0.5, { typ: 'schwarz', d: 0.9 });

    // ---------- Bühne K: der Kunde, seine zehn Bereiche, seine Lieferanten ----------
    const bK = buehne('loesung-kunde', { seed: 31, regalDeckkraft: 0.5 }); this.bK = bK;
    const kc = bK.cam;
    this.kunde = kundeHaus(kc, 560, 800, 0.62, { label: null });
    this.kundeLab = T(kc, 560, 852, { de: 'KUNDE · NIS2', en: 'CUSTOMER · NIS2' }, { mono: 1, size: 26, fill: C.muted, anchor: 'middle', ls: '0.1em' });
    this.ring = el('ellipse', { cx: 560, cy: 520, rx: 360, ry: 300, fill: 'none', stroke: C.blue, 'stroke-width': 6 }, kc);
    this.ringP = pille(kc, { de: 'bindet den Kunden', en: 'binds the customer' }, { icon: 'link', col: C.blue, size: 26 });
    this.kacheln = 'abcdefghij'.split('').map((ch, i) => {
      const th = (180 + i * 20) * Math.PI / 180, x = 560 + 320 * Math.cos(th), y = 560 + 320 * Math.sin(th);
      const gr = g(kc, { transform: `translate(${x.toFixed(1)} ${y.toFixed(1)})` });
      const glow = el('circle', { r: 80, fill: 'url(#gBlue)' }, gr);
      const r = el('rect', { x: -34, y: -34, width: 68, height: 68, rx: 12, fill: C.raised, stroke: C.line, 'stroke-width': 3 }, gr);
      const tx = T(gr, 0, 10, ch, { mono: 1, size: 30, fill: C.muted, anchor: 'middle' });
      return { g: gr, glow, r, tx, x, y };
    });
    this.dP = pille(kc, { de: 'd · Lieferkette', en: 'd · supply chain' }, { col: C.blue, size: 26 });
    // Lieferanten: unser Betrieb und weitere
    this.liefer = [[1220, 560, 0.3], [1400, 520, 0.28], [1620, 520, 0.28], [1800, 560, 0.3], [1260, 760, 0.32], [1780, 760, 0.32]].map(([x, y, s]) => ({ h: kleinHaus(kc, x, y, s, { label: null }), x, y, s }));
    this.unser = kleinHaus(kc, 1500, 820, 0.55, { label: null });
    this.unserLab = T(kc, 1500, 862, { de: 'IHR BETRIEB', en: 'YOUR BUSINESS' }, { mono: 1, size: 26, fill: C.ink, anchor: 'middle', ls: '0.1em' });
    const d = this.kacheln[3];
    this.lLinien = [...this.liefer.map((l) => [l.x, l.y - 260 * l.s]), [1500, 820 - 260 * 0.55]].map(([x, y], i) => el('path', { d: `M ${d.x + 30} ${d.y} C ${d.x + 400} ${d.y - 120} ${x - 200} ${y - 160} ${x} ${y - 6}`, fill: 'none', stroke: C.blue, 'stroke-width': i === 6 ? 5 : 3, 'stroke-linecap': 'round', opacity: 0.9 }, kc));
    this.lupe = g(kc); el('circle', { r: 70, fill: 'url(#gBlue)' }, this.lupe); iconSearch(this.lupe, 110, C.blue);
    // Fragebogen mit den zehn Bereichen
    this.kfb = g(kc);
    const kb = blatt(this.kfb, { w: 440, h: 600, kicker: { de: 'FRAGEBOGEN', en: 'QUESTIONNAIRE' }, kSize: 15, pad: 30 });
    this.kfbZeilen = 'abcdefghij'.split('').map((ch, i) => { const y = kb.y + 18 + i * 44, zg = g(kb.g); const lt = T(zg, kb.left, y + 8, ch, { mono: 1, size: 22, fill: C.pMuted }); el('rect', { x: kb.left + 30, y: y - 4, width: 160 + ((i * 47) % 80), height: 11, rx: 5.5, fill: C.pBar }, zg); const an = el('rect', { x: kb.right - 90, y: y - 6, width: 90, height: 14, rx: 7, fill: C.blue }, zg); return { lt, an }; });
    // Kopien an hunderte Lieferanten
    this.viele = [];
    for (let r = 0; r < 3; r++) for (let k = 0; k < 15; k++) { const x = 1190 + k * 44 + (r % 2) * 18, y = 260 + r * 48; const gr = g(kc, { transform: `translate(${x} ${y})` }); el('path', { d: 'M -12 0 L 0 -10 L 12 0 V 12 H -12 Z', fill: '#2a3d62' }, gr); this.viele.push({ g: gr, x, y }); }
    this.kopien = Array.from({ length: 18 }, (_, i) => { const gr = g(kc); el('rect', { x: -9, y: -12, width: 18, height: 24, rx: 2, fill: C.paper }, gr); return { g: gr, ziel: this.viele[(i * 7) % this.viele.length] }; });
    this.vertragK = belegKarte(kc, 'contract', { de: 'Vertrag', en: 'Contract' }, { w: 220, h: 66, size: 24 });
    this.dsgvoK = belegKarte(kc, 'para', { de: 'DSGVO', en: 'GDPR' }, { w: 200, h: 66, size: 24 });
    this.bindL = [el('path', { d: 'M 1410 672 Q 1450 690 1462 740', fill: 'none', stroke: C.blue, 'stroke-width': 4 }, kc), el('path', { d: 'M 1690 672 Q 1560 690 1545 740', fill: 'none', stroke: C.blue, 'stroke-width': 4 }, kc)];
    // Art. 32 DSGVO
    this.art32 = g(kc);
    const ab = blatt(this.art32, { w: 660, h: 470, kicker: { de: 'DSGVO · ARTIKEL 32 ABSATZ 1', en: 'GDPR · ARTICLE 32(1)' }, kSize: 15, pad: 36, titel: { de: 'Geeignete Maßnahmen', en: 'Appropriate measures' }, tSize: 36 });
    this.a32 = [['doc', { de: 'technisch und organisatorisch', en: 'technical and organisational' }], ['cycle', { de: 'rasch wiederherstellen', en: 'restore in a timely manner' }], ['calendar', { de: 'regelmäßig überprüfen', en: 'test regularly' }]].map(([ic, txt], i) => {
      const y = ab.y + 40 + i * 92, zg = g(ab.g);
      const hl = el('rect', { x: ab.left - 14, y: y - 40, width: ab.w - 2 * ab.pad + 28, height: 72, rx: 10, fill: C.blueSoft }, zg);
      ikon(zg, ic, ab.left + 22, y - 4, 40, C.blueDeep); T(zg, ab.left + 60, y + 8, txt, { size: 30, weight: 800, fill: C.pInk });
      return { g: zg, hl };
    });
    shot(bK, this.tS1 + 0.9, { typ: 'kreis', d: 1.3, p: weg5Punkt(0) });
    shot(bW, this.tS2 - 1.1, { typ: 'kreisRaus', d: 1.0, p: weg5Punkt(0) });

    // ---------- Bühne A: die vier Antworten ----------
    const bA = buehne('loesung-antworten', { seed: 37, regalDeckkraft: 0.5 }); this.bA = bA;
    const ac = bA.cam;
    this.frage = karte(ac, 200, 250, 640, 110, { fill: C.surface });
    T(this.frage, 232, 290, { de: 'FRAGE · BEISPIEL', en: 'QUESTION · EXAMPLE' }, { mono: 1, size: 18, fill: C.blue, ls: '0.1em' });
    T(this.frage, 232, 336, { de: 'MFA bei der Cloud-Konsole?', en: 'MFA on the cloud console?' }, { size: 32, weight: 800 });
    this.antw = ['vorhanden', 'teilweise', 'termin', 'na'].map((a) => antwort(ac, a, { size: 30 }));
    this.wahl = el('rect', { x: 0, y: 0, width: 10, height: 86, rx: 43, fill: 'none', stroke: C.blue, 'stroke-width': 4 }, ac);
    this.falsch = g(ac);
    this.jaX = g(this.falsch); { const kk = karte(this.jaX, -110, -40, 220, 80, { fill: C.raised }); kaestchen(kk, -64, 0, 28); T(kk, -30, 12, { de: 'Ja', en: 'Yes' }, { size: 34, weight: 800 }); }
    this.jaStrich = streich(this.jaX, 220, C.red);
    this.leerX = g(this.falsch); el('rect', { x: -110, y: -40, width: 220, height: 80, rx: 14, fill: 'none', stroke: C.dim, 'stroke-width': 3, 'stroke-dasharray': '10 8' }, this.leerX); T(this.leerX, 0, 12, { de: 'leer', en: 'blank' }, { mono: 1, size: 26, fill: C.dim, anchor: 'middle' });
    this.leerStrich = streich(this.leerX, 220, C.red);
    this.bsp = g(ac);
    const bs = blatt(this.bsp, { w: 760, h: 250, kicker: { de: 'ANTWORT · BEISPIEL', en: 'ANSWER · EXAMPLE' }, kSize: 15, pad: 34, back: false });
    this.bspZ1 = T(bs.g, bs.left, bs.y + 34, '', { size: 32, weight: 800, fill: C.pInk });
    this.bspZ2 = T(bs.g, bs.left, bs.y + 88, '', { size: 26, weight: 700, fill: C.pInk });
    this.bspRand = el('rect', { x: -388, y: -133, width: 776, height: 266, rx: 12, fill: 'none', stroke: C.blue, 'stroke-width': 5 }, this.bsp);
    this.tags = [pille(ac, { de: 'Lücke', en: 'Gap' }, { icon: 'unknown', col: C.amber, gestrichelt: true, size: 26 }), terminPille(ac, { de: 'Termin', en: 'Date' }, 26), pille(ac, { de: 'Person', en: 'Person' }, { icon: 'person', col: C.blue, size: 26 })];
    this.vollP = pille(ac, { de: 'vollständig', en: 'complete' }, { icon: 'check', col: C.blue, size: 28, mono: false, weight: 800 });
    shot(bA, this.tS2 + 0.5, { typ: 'kreis', d: 1.2, p: weg5Punkt(1) });
    this.buehnen = [bW, bK, bA];

    // ---------- Einblendungen ----------
    const K = { de: '2 · FÜNF SCHRITTE', en: '2 · FIVE STEPS' };
    kopf(this.tWas, this.tS1 + 0.6, K, { de: 'Was der Betrieb tut', en: 'What the business does' });
    kopf(this.tS1 + 0.9, this.tA1 - 0.3, { de: 'SCHRITT 1', en: 'STEP 1' }, { de: 'Verstehen, wer fragt', en: 'Who is asking, and why' });
    kopf(this.tA1, this.tF2 - 0.3, { de: 'SCHRITT 1', en: 'STEP 1' }, { de: 'Das ist der Fragebogen', en: 'That is the questionnaire' });
    kopf(this.tF2, this.tS2 - 1.2, { de: 'SCHRITT 1', en: 'STEP 1' }, { de: 'Artikel 32 DSGVO', en: 'Article 32 GDPR' });
    kopf(this.tS2 - 1.0, this.tS2 + 0.3, K, { de: 'Was der Betrieb tut', en: 'What the business does' });
    kopf(this.tS2 + 0.5, this.tEnde - 1.2, { de: 'SCHRITT 2', en: 'STEP 2' }, { de: 'Vier Antworten', en: 'Four answers' });
  },

  zeichnen(t) {
    // ---------- Bühne W ----------
    if (this.bW.vis) {
      kamera(this.bW, WEG5_BLICK.f, WEG5_BLICK.z);
      const zurueck = t > this.tS2 - 2; // nach Schritt 1
      const da = this.Wg.nodes.map((_, i) => P(t, this.tFuenf + 0.3 + i * 0.14, 0.4, E.back));
      const puls = t < this.tSchneller ? -1 : clamp((t - this.tSchneller - 0.1) / 0.9);
      weg5Zeichnen(this.Wg, t, { strecke: P(t, this.tFuenf - 0.2, 1.2), puls: puls >= 1 ? -1 : puls, da, aktiv: zurueck ? 1 : (t > this.tS1 - 0.2 ? 0 : -1), aktivK: zurueck ? P(t, this.tS2 - 0.2, 0.4) : P(t, this.tS1 - 0.2, 0.4), erledigt: zurueck ? 1 : 0, nah: t > this.tOhne && t < this.tSchneller ? -1 : -1 });
      this.Wg.nodes.forEach((n, i) => O(n.glow, (t > this.tOhne && t < this.tSchneller + 0.2 ? 0.35 * P(t, this.tOhne + i * 0.1, 0.3) : 0) + (i === (zurueck ? 1 : 0) && t > (zurueck ? this.tS2 - 0.2 : this.tS1 - 0.2) ? 0.9 : 0)));
      tr(this.ohneP, 1810, 400, Math.max(0.01, P(t, this.tOhne, 0.45, E.back))); O(this.ohneP, Math.min(P(t, this.tOhne, 0.2), 1 - P(t, this.tSchneller - 0.2, 0.3)));
      tr(this.tk, 1810, 400, Math.max(0.01, P(t, this.tSchneller - 0.1, 0.45, E.back))); O(this.tk, Math.min(P(t, this.tSchneller - 0.1, 0.2), 1 - P(t, this.tS1 - 0.4, 0.4)));
    }
    // ---------- Bühne K ----------
    if (this.bK.vis) {
      kamera(this.bK, [960, 540], 1);
      const aus = P(t, this.tF2 - 0.3, 0.8); // Art. 32 rückt nach vorn, der Rest tritt zurück
      const ki = P(t, this.tS1 + 1.0, 0.6, E.out);
      O(this.kunde.g, ki * (1 - 0.6 * aus)); O(this.kundeLab, P(t, this.tErfasst, 0.5) * (1 - 0.6 * aus));
      this.kunde.fenster.forEach((f, i) => f.setAttribute('fill', (i * 5 + Math.floor(t * 0.6)) % 7 === 0 ? '#3a5584' : (i % 4 === 1 ? '#2a3d62' : '#1a2742')));
      this.kacheln.forEach((k, i) => {
        const t0 = this.tZehn - 0.2 + i * 0.09, a = P(t, t0, 0.4, E.back);
        const folg = puls(t, this.tFolgen + i * 0.16, 0.6, 9);
        sk(k.g, k.x, k.y, 1); tr(k.g, k.x, k.y, Math.max(0.01, a) * (1 + 0.12 * folg));
        O(k.g, P(t, t0, 0.2) * (1 - 0.6 * aus));
        const istD = i === 3 && t > this.tLiefer - 0.1;
        k.r.setAttribute('fill', istD ? C.blue : C.raised); k.r.setAttribute('stroke', istD || folg > 0.2 ? C.blue : C.line); k.tx.setAttribute('fill', istD ? '#fff' : C.muted);
        O(k.glow, istD ? 0.8 : 0);
      });
      tr(this.dP, 560, 400, Math.max(0.01, P(t, this.tLiefer + 0.2, 0.45, E.back))); O(this.dP, Math.min(P(t, this.tLiefer + 0.2, 0.2), 1 - P(t, this.tIstFB, 0.4)));
      const bind = P(t, this.tBindet, 0.5);
      this.liefer.forEach((l, i) => { O(l.h.g, P(t, this.tUnmittel + 0.1 + i * 0.08, 0.4) * (1 - 0.8 * bind) * (1 - aus)); });
      O(this.unser.g, P(t, this.tLiefer + 0.3, 0.5) * (1 - 0.5 * aus)); O(this.unserLab, P(t, this.tLiefer + 0.3, 0.5) * (1 - 0.5 * aus));
      this.lLinien.forEach((l, i) => { zeichne(l, P(t, i === 6 ? this.tLiefer + 0.3 : this.tUnmittel + 0.1 + i * 0.08, 0.7)); O(l, (i === 6 ? 1 : 1 - 0.85 * bind) * (1 - P(t, this.tIstFB, 0.6) * 0.6) * (1 - aus)); });
      // Lupe: der Kunde prüft die Praxis der Lieferanten, dann wird sie zum Fragebogen
      const lk = P(t, this.tLupe - 0.3, 1.2, E.io); const lp = bogen([700, 420], [1500, 560], lk, 120);
      tr(this.lupe, lp[0] + 10 * Math.sin(t * 2), lp[1] + 6 * Math.cos(t * 1.7), 1, 0); O(this.lupe, Math.min(P(t, this.tLupe - 0.3, 0.3), 1 - P(t, this.tIstFB - 0.1, 0.4)));
      const fbk = P(t, this.tIstFB - 0.1, 0.9, E.io); const fp = lerp2([1500, 560], [1062, 600], fbk);
      tr(this.kfb, fp[0], fp[1], lerp(0.2, 0.56, fbk), lerp(8, -1.5, fbk)); O(this.kfb, P(t, this.tIstFB - 0.1, 0.3) * (1 - aus));
      this.kfbZeilen.forEach((z, i) => { const on = puls(t, this.tFolgen + i * 0.16, 0.6, 9); z.lt.setAttribute('fill', t > this.tFolgen + i * 0.16 ? C.blueDeep : C.pMuted); O(z.an, P(t, this.tAntw + 0.1 + i * 0.12, 0.25)); });
      // hunderte Lieferanten bekommen Kopien
      this.viele.forEach((v, i) => O(v.g, P(t, this.tHundert - 0.2 + (i % 15) * 0.03 + Math.floor(i / 15) * 0.1, 0.3) * (1 - 0.8 * bind) * (1 - aus)));
      this.kopien.forEach((k, i) => { const t0 = this.tBillig + i * 0.12, kk = P(t, t0, 1.0, E.io); const p = bogen([600, 480], [k.ziel.x, k.ziel.y], kk, 140); tr(k.g, p[0], p[1], 1, kk * 20); O(k.g, Math.min(P(t, t0, 0.15), 1 - P(t, t0 + 0.95, 0.2))); });
      // bindet den Kunden, nicht Sie; Vertrag und DSGVO beim Lieferanten
      zeichne(this.ring, bind); O(this.ring, 1 - aus);
      tr(this.ringP, 980, 236, Math.max(0.01, P(t, this.tBindet + 0.2, 0.45, E.back))); O(this.ringP, P(t, this.tBindet + 0.2, 0.2) * (1 - aus));
      const vk = P(t, this.tVertrag - 0.1, 0.6, E.out), dk = P(t, this.tDSGVO - 0.1, 0.6, E.out);
      tr(this.vertragK, lerp(1260, 1300, vk), 640, 1, lerp(-6, -2, vk)); O(this.vertragK, vk * (1 - aus));
      tr(this.dsgvoK, lerp(1830, 1790, dk), 640, 1, lerp(6, 2, dk)); O(this.dsgvoK, dk * (1 - aus));
      zeichne(this.bindL[0], P(t, this.tVertrag + 0.4, 0.5)); zeichne(this.bindL[1], P(t, this.tDSGVO + 0.4, 0.5)); O(this.bindL[0], 1 - aus); O(this.bindL[1], 1 - aus);
      // Art. 32 DSGVO
      const ak = P(t, this.tF2 - 0.2, 0.8, E.out); tr(this.art32, lerp(1500, 1260, ak), 560 + (1 - ak) * 30, 1, lerp(3, 1, ak)); O(this.art32, ak);
      this.a32.forEach((z, i) => { const t0 = [this.tTOM, this.tWieder, this.tUeber][i]; O(z.g, 0.25 + 0.75 * P(t, t0 - 0.1, 0.35)); O(z.hl, i > 0 ? P(t, t0, 0.4) : 0); });
    }
    // ---------- Bühne A ----------
    if (this.bA.vis) {
      kamera(this.bA, [960, 540], 1);
      O(this.frage, P(t, this.tS2 + 0.8, 0.5));
      const Y = [440, 530, 620, 710];
      this.antw.forEach((p, i) => { const t0 = this.tAn[i] - 0.1, k = P(t, t0, 0.45, E.back); tr(p, 520, Y[i], Math.max(0.01, k)); O(p, Math.min(P(t, t0, 0.2), i === 2 || t < this.tBsp ? 1 : 1 - 0.5 * P(t, this.tBsp, 0.4))); });
      const wk = P(t, this.tBsp - 0.1, 0.4, E.out); const ww = this.antw[2].w + 24;
      this.wahl.setAttribute('x', (520 - ww / 2).toFixed(1)); this.wahl.setAttribute('y', (Y[2] - 43).toFixed(1)); this.wahl.setAttribute('width', ww.toFixed(1)); O(this.wahl, wk);
      // nichts anderes: „Ja“ und leeres Feld werden gestrichen und fallen weg
      const fx = (t0) => P(t, t0 + 0.4, 0.8, E.in);
      tr(this.jaX, 1360, 440 + 300 * fx(this.tKeinJa), 1, 20 * fx(this.tKeinJa)); O(this.jaX, Math.min(P(t, this.tNichts - 0.1, 0.3), 1 - fx(this.tKeinJa)));
      zeichne(this.jaStrich, P(t, this.tKeinJa, 0.35));
      tr(this.leerX, 1660, 440 + 300 * fx(this.tLeeres), 1, -20 * fx(this.tLeeres)); O(this.leerX, Math.min(P(t, this.tNichts - 0.1, 0.3), 1 - fx(this.tLeeres)));
      zeichne(this.leerStrich, P(t, this.tLeeres, 0.35));
      // Beispielantwort tippt sich
      const bk = P(t, this.tBsp, 0.6, E.out); tr(this.bsp, 1340, 600 + (1 - bk) * 30, 1, lerp(2, 0.6, bk)); O(this.bsp, bk);
      typeText(this.bspZ1, { de: 'Noch nicht · bis Ende des Quartals', en: 'Not yet · by the end of the quarter' }, t, this.tBsp + 0.5, Math.max(0.8, this.tVerantw - this.tBsp - 0.7));
      typeText(this.bspZ2, { de: 'verantwortlich: Büroleitung mit IT-Dienstleister', en: 'responsible: office manager with the IT provider' }, t, this.tVerantw, 1.6);
      zeichne(this.bspRand, P(t, this.tVollst, 0.6));
      tr(this.vollP, 1340, 452, Math.max(0.01, P(t, this.tVollst + 0.2, 0.45, E.back))); O(this.vollP, P(t, this.tVollst + 0.2, 0.2));
      const TX = [1080, 1340, 1600];
      this.tags.forEach((p, i) => { const t0 = [this.tLuecke, this.tTermin, this.tPerson][i], k = P(t, t0, 0.45, E.back); tr(p, TX[i], 790, Math.max(0.01, k)); O(p, P(t, t0, 0.2)); });
    }
  },
});
