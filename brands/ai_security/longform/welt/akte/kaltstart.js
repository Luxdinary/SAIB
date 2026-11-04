// Kaltstart · Beispielfall „Dienstag, 09:12“ (neu für die Langfassung, 03.11.2026). Bühne: der Beispielbetrieb bei Nacht,
// Kamera fährt vom Haus ins Büro; Büro A öffnet den Textassistenten, die Mail des Kunden fliegt als Blatt in den Chat,
// die Zeile mit den Kundendaten färbt sich bernstein; am Ende bleibt die offene Frage „entschieden?“.
// Sprechtext (DE): „Dienstag, neun Uhr zwölf, in einem kleinen Elektrobetrieb. Jemand im Büro öffnet einen Textassistenten,
// um ein Angebot zu entwerfen, und fügt die Mail des Kunden gleich mit ein. Es funktioniert. Entschieden hat das niemand.“
akt({
  name: 'kaltstart',
  bauen() {
    const c = (de, en) => cue({ de, en });
    this.tTag = c('Dienstag', 'Tuesday').s;
    this.tBetrieb = c('Elektrobetrieb', 'electrical business').s;
    this.tBuero = c('Jemand im Büro', 'Somebody in the office').s;
    this.tAssi = c('Textassistenten', 'text assistant').s;
    this.tAngebot = c('Angebot zu entwerfen', 'draft a quote').s;
    this.tMail = c('Mail des Kunden', "customer's email").s;
    this.tGeht = c('Es funktioniert', 'It works').s;
    this.tNie = c('Entschieden hat', 'Nobody decided').s;
    this.tEnde = cue({ de: 'Nutzt Ihre Belegschaft', en: 'Are your staff' }, { halten: true }).s;

    const b = buehne('kaltstart-buero', { seed: 11 });
    this.b = b;
    const B = bauBetrieb(b.cam); this.B = B;
    // Chatfenster über dem Arbeitsplatz von Büro A (Weltkoordinaten)
    this.chat = karte(b.cam, 1210, 280, 470, 230, { fill: '#121b2f', stroke: C.blue, sw: 3 });
    this.chatKopf = T(this.chat, 1236, 318, { de: 'TEXTASSISTENT · NEUER CHAT', en: 'TEXT ASSISTANT · NEW CHAT' }, { mono: 1, size: 16, fill: C.muted, ls: '0.1em' });
    this.chatZ1 = T(this.chat, 1236, 360, '', { size: 19, fill: C.ink });
    this.chatZ2 = g(this.chat);
    this.chatZ2Bg = el('rect', { x: 1228, y: 378, width: 434, height: 40, rx: 8, fill: 'rgba(255,209,102,0.16)', stroke: C.amberLine, 'stroke-width': 2, 'stroke-dasharray': '8 6' }, this.chatZ2);
    T(this.chatZ2, 1244, 405, { de: '+ Mail des Kunden: Name, Preise', en: "+ customer's email: name, prices" }, { size: 21, fill: C.amber });
    this.chatOk = g(this.chat); ikon(this.chatOk, 'spark', 1640, 470, 34, C.blue);
    linien(this.chat, 1236, 450, 300, 2, 18, '#2a3858', 8);
    // die Mail als Blatt
    this.mail = g(b.cam);
    const m = blatt(this.mail, { w: 220, h: 150, pad: 18, kicker: { de: 'E-MAIL · KUNDE', en: 'EMAIL · CUSTOMER' }, kSize: 12 });
    linien(this.mail, m.left, m.y + 34, 170, 3, 18, C.pBar, 7);
    // offene Frage
    this.frage = pille(b.cam, { de: 'entschieden: niemand', en: 'decided: nobody' }, { icon: 'unknown', col: C.amber, gestrichelt: true, size: 24 });
    shot(b, 0);
    this.buehnen = [b];

    klang(this.tAngebot, 'keys_typing', { dauer: 2.4, laut: 0.6 }); klang(this.tMail - 0.2, 'paper_slide'); klang(this.tGeht, 'click_soft'); klang(this.tNie, 'tick');
    kopf(0.3, this.tEnde - 0.4, { de: 'BEISPIELFALL · NACHGESTELLT', en: 'EXAMPLE CASE · RE-ENACTED' }, { de: 'Dienstag, 09:12', en: 'Tuesday, 09:12' });
  },

  zeichnen(t) {
    const B = this.B;
    const k = fahrt(t, BLICK.haus, [
      { t: 0, d: 2.5, f: [1640, 560], z: 0.6, e: E.sine },
      { t: this.tBuero - 0.3, d: 1.8, f: [1350, 520], z: 1.05 },
      { t: this.tNie - 0.2, d: 1.6, f: [1260, 520], z: 1.2 },
    ]);
    kamera(this.b, k.f, k.z);
    // Nacht: nur der Bildschirm von Büro A geht an
    bildschirm(B.monA, P(t, this.tAssi, 0.5, E.out));
    bildschirm(B.monB, 0); bildschirm(B.monC, 0);
    B.telefone.forEach((f) => { O(f.dim, 0.78); O(f.glow, 0.12); });
    betriebLeben(B, t, { tippen: { figA: [this.tAngebot, this.tGeht + 0.6] } });
    // Chatfenster
    const cIn = P(t, this.tAssi + 0.2, 0.5, E.back);
    sk(this.chat, 1445, 395, Math.max(0.01, cIn)); O(this.chat, P(t, this.tAssi + 0.2, 0.25));
    typeText(this.chatZ1, { de: 'Angebot Elektroinstallation entwerfen …', en: 'Draft a quote for the electrical work …' }, t, this.tAngebot, 1.6);
    // Mail fliegt in den Chat
    const fk = P(t, this.tMail - 0.2, 1.0, E.io);
    const pos = bogen([560, 210], [1440, 398], fk, 160);
    tr(this.mail, pos[0], pos[1], lerp(1, 0.35, fk), lerp(-6, 0, fk));
    O(this.mail, Math.min(P(t, this.tMail - 0.3, 0.2), 1 - P(t, this.tMail + 0.75, 0.3)));
    O(this.chatZ2, P(t, this.tMail + 0.7, 0.3));
    this.chatZ2Bg.setAttribute('stroke-dashoffset', (-t * 16).toFixed(1));
    pop(this.chatOk, 1640, 470, t, this.tGeht);
    // offene Frage am Arbeitsplatz
    tr(this.frage, 1180, 250, Math.max(0.01, P(t, this.tNie, 0.45, E.back)) * (1 + 0.06 * puls(t, this.tNie + 0.5, 1.0, 8)));
    O(this.frage, P(t, this.tNie, 0.3));
  },
});
