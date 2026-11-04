// Teil 1 · Einstieg (Fassung 2, Stefan 30.10.2026): beginnt mit einer Frage; Scutoria und KI-Hinweis stehen jetzt am Schluss (teil-7.js).
// Bühnen: der Beispielbetrieb bei Nacht (Geräte gehen an, der Rahmen für die Regel bleibt leer), Vorschau (Schritt 1, Richtlinie leistet / leistet nicht).
akt({
  name: 'einstieg',
  bauen() {
    // ---------- Wortanker ----------
    const c = (de, en) => cue({ de, en });
    this.tStart = 0;
    this.tHook = c('Nutzt Ihre Belegschaft', 'Are your staff').s;   // Langfassung: vor dem Einstieg läuft der Kaltstart
    this.tTools = c('KI-Tools', 'AI tools').s;
    this.tOb = c('ohne dass der Betrieb', 'without the business').s;
    this.tNicht = c('entschieden hat', 'decided anything').s;
    this.tVideo = c('Dieses Video zeigt', 'This video shows').s;
    this.tSchritt = c('welcher Schritt', 'which step').s;
    this.tLeistet = c('was eine Richtlinie', 'what a policy').s;
    this.tNicht2 = c('und was nicht', 'does not do').s;
    this.tEnde = cue({ de: 'Nehmen Sie eine typische', en: 'Take a typical' }, { halten: true }).s;
    // Ton (Langfassung 03.11.2026)
    klang(this.tTools, 'click_soft'); klang(this.tOb, 'pop', { laut: 0.5 }); klang(this.tNicht, 'tick'); klang(this.tLeistet, 'paper_slide', { laut: 0.6 });

    // ---------- Bühne 1: der Betrieb bei Nacht ----------
    const b1 = buehne('einstieg-betrieb', { seed: 3 });
    this.b1 = b1;
    const B = bauBetrieb(b1.cam); this.B = B;
    const geraete = [[B.monA.x + 86, B.monA.y - 64], [B.monB.x + 86, B.monB.y - 64], [B.monC.x + 86, B.monC.y - 64], [2522, 470], [2742, 470]];
    this.funken = geraete.map(([x, y]) => { const f = g(b1.cam); ikon(f, 'spark', 0, 0, 70, C.blue); return { g: f, x, y }; });
    this.frage = pille(b1.cam, { de: 'entschieden?', en: 'decided?' }, { icon: 'unknown', col: C.amber, gestrichelt: true, size: 26 });
    shot(b1, this.tHook - 0.5, { typ: 'blende', d: 0.8 });

    // ---------- Bühne 3: Vorschau ----------
    const b3 = buehne('einstieg-vorschau', { seed: 7, regalDeckkraft: 0.6 });
    this.b3 = b3;
    const pts = [[230, 640], [370, 600], [510, 636], [650, 590], [790, 626], [930, 584]];
    this.vWeg = el('path', { d: catmull([[150, 660], ...pts, [1010, 570]]), fill: 'none', stroke: '#33466e', 'stroke-width': 6, 'stroke-linecap': 'round' }, b3.cam);
    this.vKnoten = pts.map(([x, y], i) => { const n = g(b3.cam, { transform: `translate(${x} ${y})` }); const glow = el('circle', { r: 110, fill: 'url(#gBlue)' }, n); const c0 = el('circle', { r: 20, fill: C.surface, stroke: C.line, 'stroke-width': 3 }, n); const num = T(n, 0, 9, String(i + 1), { mono: 1, size: 24, anchor: 'middle', fill: C.muted }); return { g: n, glow, c: c0, num }; });
    this.vZuerst = pille(b3.cam, { de: 'zuerst', en: 'first' }, { col: C.blue, size: 26 });
    this.vRl = g(b3.cam);
    const rl = blatt(this.vRl, { w: 560, h: 380, kicker: { de: 'KI-NUTZUNGSRICHTLINIE', en: 'AI USAGE POLICY' } });
    const colX = [rl.left, 20];
    this.vSpalten = [0, 1].map((k) => {
      const s = g(rl.g); const x = colX[k];
      const kopfT = T(s, x + 36, rl.y + 26, k === 0 ? { de: 'leistet', en: 'does' } : { de: 'leistet nicht', en: 'does not' }, { size: 26, weight: 800, fill: k === 0 ? C.blueDeep : C.pMuted });
      const ic = g(s, { transform: `translate(${x + 12} ${rl.y + 17})` }); (k === 0 ? iconCheck : (q, z, c0) => el('rect', { x: -z * 0.32, y: -z * 0.06, width: z * 0.64, height: z * 0.12, rx: z * 0.06, fill: c0 }, q))(ic, 26, k === 0 ? C.blueDeep : C.pMuted);
      const ln = linien(s, x, rl.y + 66, 190, 5, 34, k === 0 ? C.blueBar : C.pBar, 11);
      const rahmen = el('rect', { x: x - 14, y: rl.y - 14, width: 228, height: 236, rx: 12, fill: 'none', stroke: k === 0 ? C.blue : C.dim, 'stroke-width': 3, 'stroke-dasharray': k === 0 ? '' : '10 7' }, s);
      return { g: s, rahmen, ln, kopfT };
    });
    shot(b3, this.tVideo - 0.35, { typ: 'blende', d: 0.7 });
    this.buehnen = [b1, b3];

    // ---------- Einblendungen ----------
    kopf(this.tHook - 0.2, this.tVideo - 0.4, { de: 'SCUTORIA · KI-REGELN', en: 'SCUTORIA · AI RULES' }, { de: 'Nutzt Ihre Belegschaft schon KI?', en: 'Are your staff already using AI?' });
    kopf(this.tVideo, this.tEnde - 0.3, { de: 'IN DIESEM VIDEO', en: 'IN THIS VIDEO' }, '');
    hinweis(0, this.tEnde - 0.2, (gr) => {
      el('rect', { x: 96, y: 990, width: 56, height: 2, fill: C.blue }, gr);
      T(gr, 96, 1030, { de: 'Synthetische Stimme · Quellen am Bildschirm · Keine Rechtsberatung', en: 'Synthetic voice · Sources on screen · No legal advice' }, { mono: 1, size: 24, fill: C.muted, ls: '0.04em' });
    });
  },

  zeichnen(t) {
    const B = this.B;
    // ---------- Bühne 1 ----------
    if (this.b1.vis) {
      const k = fahrt(t, { f: [1680, 470], z: 0.58 }, [{ t: this.tHook - 0.5, d: 6, f: [1700, 480], z: 0.62, e: E.sine }, { t: this.tOb - 0.1, d: 1.4, f: [470, 470], z: 1.3 }]);
      kamera(this.b1, k.f, k.z);
      const an = [0, 0.18, 0.36, 0.54, 0.72].map((d) => P(t, this.tTools + d, 0.35, E.out));
      B.monitore.forEach((m, i) => bildschirm(m, an[i]));
      B.telefone.forEach((f, i) => { O(f.dim, 0.78 * (1 - an[3 + i])); O(f.glow, 0.12 + 0.88 * an[3 + i]); });
      this.funken.forEach((f, i) => { const kk = P(t, this.tTools + i * 0.18, 0.45, E.back); tr(f.g, f.x, f.y - 10 * Math.sin(t * 2 + i), Math.max(0.01, kk), t * 20); O(f.g, Math.min(P(t, this.tTools + i * 0.18, 0.2), 1 - P(t, this.tOb, 0.5))); });
      betriebLeben(B, t, { tippen: { figA: [this.tTools, 99], figB: [this.tTools + 0.2, 99], figC: [this.tTools + 0.4, 99] } });
      // leerer Rahmen für die Regel
      const rk = P(t, this.tOb + 0.6, 0.5);
      B.rahmenRect.setAttribute('stroke', rk > 0.5 ? C.amberLine : C.line);
      B.rahmenRect.setAttribute('stroke-dashoffset', (-t * 18).toFixed(1));
      B.rahmenRect.setAttribute('stroke-width', (3 + 2 * rk).toFixed(1));
      const pz = 1 + 0.08 * puls(t, this.tNicht, 1.0, 9);
      pop(this.frage, 0, 0, t, this.tOb + 0.75); tr(this.frage, 445, 290, pz * P(t, this.tOb + 0.75, 0.45, E.back) || 0.01);
    }
    // ---------- Bühne 3 ----------
    if (this.b3.vis) {
      kamera(this.b3, [960, 540], 1);
      zeichne(this.vWeg, P(t, this.tVideo - 0.2, 1.0));
      this.vKnoten.forEach((n, i) => {
        const ap = P(t, this.tVideo + i * 0.12, 0.35, E.back);
        const akt0 = i === 0 ? P(t, this.tSchritt, 0.4) : 0;
        n.c.setAttribute('r', Math.max(0.1, (20 + 16 * akt0) * ap).toFixed(1));
        n.c.setAttribute('fill', akt0 > 0.5 ? C.blue : C.surface); n.c.setAttribute('stroke', akt0 > 0.5 ? C.blue : C.line);
        n.num.setAttribute('fill', akt0 > 0.5 ? '#fff' : C.muted); n.num.setAttribute('font-size', (24 + 8 * akt0).toFixed(1)); n.num.setAttribute('y', (9 + 3 * akt0).toFixed(1));
        O(n.num, ap); O(n.glow, akt0 * 0.9);
      });
      pop(this.vZuerst, 230, 740, t, this.tSchritt + 0.2); tr(this.vZuerst, 230, 730, Math.max(0.01, P(t, this.tSchritt + 0.2, 0.45, E.back)));
      const rIn = P(t, this.tLeistet - 0.3, 0.7, E.out);
      tr(this.vRl, 1400, 600 + (1 - rIn) * 40, 1, lerp(4, 1.5, rIn)); O(this.vRl, rIn);
      this.vSpalten.forEach((s, k) => {
        const on = P(t, k === 0 ? this.tLeistet + 0.4 : this.tNicht2, 0.4);
        O(s.rahmen, on); s.ln.forEach((l, i) => O(l, 0.35 + 0.65 * P(t, (k === 0 ? this.tLeistet + 0.4 : this.tNicht2) + i * 0.08, 0.25)));
      });
    }
  },
});
