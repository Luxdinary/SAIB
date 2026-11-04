// Kaltstart Video 02 · „Freitag, 16:40“ (neu für die Langfassung, 03.11.2026). Bühne: der Beispielbetrieb, Kamera fährt vom Haus
// ins Büro; der Fragebogen kommt als Blatt an, die Uhr steht auf Freitag 16:40, die Rückgabe am Mittwoch bekommt ihre Kapsel;
// dann schwenkt die Kamera zur Baustelle, wo die externe IT-Betreuung steht und erst nächste Woche zu erreichen ist.
// Sprechtext (DE): „Freitag, sechzehn Uhr vierzig. Ein größerer Kunde schickt einen Fragebogen zur Informationssicherheit.
// Rückgabe bis Mittwoch. Die IT-Betreuung ist erst nächste Woche wieder erreichbar.“
akt({
  name: 'kaltstart-02',
  bauen() {
    const c = (de, en) => cue({ de, en }).s;
    this.tFr = c('Freitag', 'Friday');
    this.tUhr = c('Uhr vierzig', 'to five');
    this.tKunde = c('größerer Kunde', 'larger customer');
    this.tFB = c('Fragebogen zur', 'questionnaire on');
    this.tRueck = c('Rückgabe', 'Due back');
    this.tMi = c('Mittwoch', 'Wednesday');
    this.tIT = c('Die IT-Betreuung|Die IT Betreuung', 'The IT provider');
    this.tNaechste = c('nächste Woche', 'next week');
    this.tEnde = cue({ de: 'Hat Ihr Kunde einen', en: 'Has your customer' }, { halten: true }).s;

    const b = buehne('kaltstart-fragebogen', { seed: 12 });
    this.b = b;
    const B = bauBetrieb(b.cam); this.B = B;
    // Baustelle mit der externen IT-Betreuung rechts neben dem Haus (wie in Kapitel 1)
    el('rect', { x: 3330, y: 852, width: 900, height: 10, rx: 5, fill: '#1c2943' }, b.cam);
    baustelle(b.cam, 3900, 856);
    this.itFig = itBetreuung(b.cam, 3640, 852, 1);
    this.itLab = pille(b.cam, { de: 'IT-Betreuung · extern', en: 'IT provider · external' }, { icon: 'briefcase', col: C.muted, size: 24 });
    this.itWeg = pille(b.cam, { de: 'erst nächste Woche erreichbar', en: 'not available until next week' }, { icon: 'calendar', col: C.amber, gestrichelt: true, size: 24 });
    // die Uhr, die Mail als Blatt, die Rückgabe
    this.uhr = pille(b.cam, { de: 'Freitag · 16:40', en: 'Friday · 16:40' }, { icon: 'clock', col: C.blue, size: 26 });
    this.mail = g(b.cam);
    const m = blatt(this.mail, { w: 240, h: 170, pad: 18, kicker: { de: 'FRAGEBOGEN · KUNDE', en: 'QUESTIONNAIRE · CUSTOMER' }, kSize: 12 });
    linien(this.mail, m.left, m.y + 34, 190, 4, 20, C.pBar, 7);
    this.rueck = terminPille(b.cam, { de: 'Rückgabe: Mittwoch', en: 'Due back: Wednesday' }, 26);
    shot(b, 0);
    this.buehnen = [b];

    klang(this.tFB - 0.2, 'paper_slide'); klang(this.tUhr, 'clock_tick', { dauer: 1.2, laut: 0.5 });
    klang(this.tMi, 'pop'); klang(this.tIT, 'swipe', { laut: 0.5 }); klang(this.tNaechste, 'tick');
    kopf(0.3, this.tEnde - 0.4, { de: 'BEISPIELFALL · NACHGESTELLT', en: 'EXAMPLE CASE · RE-ENACTED' }, { de: 'Freitag, 16:40', en: 'Friday, 16:40' });
  },

  zeichnen(t) {
    const B = this.B;
    const k = fahrt(t, BLICK.haus, [
      { t: 0, d: 2.5, f: [1640, 560], z: 0.6, e: E.sine },
      { t: this.tKunde - 0.3, d: 1.8, f: [1250, 540], z: 1.0 },
      { t: this.tIT - 0.3, d: 1.8, f: [3560, 620], z: 1.05 },
      { t: this.tNaechste + 1.6, d: 1.6, f: [1900, 560], z: 0.62, e: E.sine },
    ]);
    kamera(this.b, k.f, k.z);
    B.monitore.forEach((mo, i) => bildschirm(mo, i === 0 ? P(t, this.tKunde, 0.5, E.out) : 0.1));
    B.telefone.forEach((f) => { O(f.dim, 0.78); O(f.glow, 0.12); });
    betriebLeben(B, t, { tippen: { figA: [this.tFB + 0.4, this.tRueck] } });
    // Uhr über dem Haus
    tr(this.uhr, 1000, 195, Math.max(0.01, P(t, this.tFr, 0.45, E.back)) * (1 + 0.05 * puls(t, this.tUhr, 1.0, 8))); O(this.uhr, P(t, this.tFr, 0.3));
    // Mail fliegt vom linken Rand zum Schreibtisch von Büro A und bleibt dort stehen
    const fk = P(t, this.tFB - 0.3, 1.1, E.io);
    const pos = bogen([420, 230], [1180, 470], fk, 150);
    tr(this.mail, pos[0], pos[1], lerp(1, 0.55, fk), lerp(-8, -2, fk)); O(this.mail, P(t, this.tFB - 0.35, 0.25));
    // Rückgabe am Mittwoch
    tr(this.rueck, 1180, 330, Math.max(0.01, P(t, this.tMi - 0.2, 0.45, E.back))); O(this.rueck, P(t, this.tRueck, 0.3));
    // IT-Betreuung auf der Baustelle: tippt, ist aber nicht erreichbar
    arme(this.itFig, -6, 0, 30 + 2 * Math.sin(t * 9), 72 + tippen(t, this.tIT, this.tNaechste, 0, 4), 6 + 3 * Math.sin(t * 0.8));
    tr(this.itLab, 3640, 930, 1); O(this.itLab, P(t, this.tIT - 0.2, 0.4));
    tr(this.itWeg, 3640, 1000, Math.max(0.01, P(t, this.tNaechste - 0.2, 0.45, E.back))); O(this.itWeg, P(t, this.tNaechste - 0.2, 0.25));
  },
});
