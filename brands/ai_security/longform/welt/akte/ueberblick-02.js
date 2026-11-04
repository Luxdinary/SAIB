// Überblick Video 02 · die sieben Kapitel als Stationen auf einem Weg (neu für die Langfassung, 03.11.2026; nach akte/ueberblick.js von Video 01). Die Kamera fährt den
// Weg ab, jede Station leuchtet bei ihrem Wort auf; der Kopf „IN DIESEM VIDEO“ kommt aus teil-1.js.
// Sprechtext (DE): „Wir gehen so vor: was meistens schiefgeht, die fünf Schritte, die Quellen hinter der Antwort „noch nicht“, zwei Fälle,
// in denen Sie entscheiden, der Beispielbetrieb, was das alles nicht ist, und am Ende das freie Memo.“
akt({
  name: 'ueberblick-02',
  bauen() {
    const c = (de, en) => cue({ de, en }).s;
    this.tStart = c('Wir gehen so vor', 'We go like this');
    const anker = [['was meistens schiefgeht', 'what usually goes wrong'], ['die fünf Schritte', 'the five steps'], ['Quellen hinter', 'sources behind'],
      ['zwei Fälle', 'two cases'], ['der Beispielbetrieb', 'the example business'], ['das alles nicht ist', 'all of this is not'], ['freie Memo', 'free memo']];
    this.tS = anker.map(([de, en]) => c(de, en));
    const namen = [{ de: 'Was schiefgeht', en: 'What goes wrong' }, { de: 'Fünf Schritte', en: 'Five steps' }, { de: 'Die Quellen', en: 'The sources' },
      { de: 'Was tun Sie?', en: 'What do you do?' }, { de: 'Beispielbetrieb', en: 'Example business' }, { de: 'Was es nicht ist', en: 'What it is not' },
      { de: 'Memo und Toolkit', en: 'Memo and toolkit' }];
    const icons = ['warn', 'list', 'para', 'question', 'briefcase', 'doc', 'mail'];

    const b = buehne('ueberblick', { seed: 5, regalDeckkraft: 0.55 });
    this.b = b;
    this.pts = namen.map((_, i) => [260 + i * 420, 560 + (i % 2 ? -70 : 40)]);
    this.weg = el('path', { d: catmull([[60, 600], ...this.pts, [3000, 520]]), fill: 'none', stroke: '#33466e', 'stroke-width': 7, 'stroke-linecap': 'round' }, b.cam);
    this.wegAktiv = el('path', { d: catmull([[60, 600], ...this.pts, [3000, 520]]), fill: 'none', stroke: C.blue, 'stroke-width': 7, 'stroke-linecap': 'round' }, b.cam);
    this.st = this.pts.map(([x, y], i) => {
      const n = g(b.cam, { transform: `translate(${x} ${y})` });
      const glow = el('circle', { r: 150, fill: 'url(#gBlue)' }, n);
      const ring = el('circle', { r: 56, fill: C.surface, stroke: C.line, 'stroke-width': 4 }, n);
      const ic = ikon(n, icons[i], 0, 0, 52, C.muted);
      const num = T(n, 0, -84, String(i + 1), { mono: 1, size: 26, anchor: 'middle', fill: C.muted });
      const lab = T(n, 0, 112, namen[i], { size: 34, weight: 800, anchor: 'middle', fill: C.ink });
      return { g: n, glow, ring, ic, num, lab };
    });
    this.tS.forEach((ts) => klang(ts - 0.05, 'swipe', { laut: 0.5 }));
    shot(b, this.tStart - 0.35, { typ: 'schieben', d: 0.8, dir: 1 });
    this.buehnen = [b];
  },

  zeichnen(t) {
    // Kamera folgt der jeweils aktiven Station
    const shots = this.tS.map((ts, i) => ({ t: ts - 0.3, d: 0.9, f: [this.pts[i][0] + 220, 560], z: 0.92 }));
    const k = fahrt(t, { f: [this.pts[0][0] + 400, 560], z: 0.62 }, [{ t: this.tStart, d: 1.2, f: [this.pts[0][0] + 520, 560], z: 0.66 }, ...shots,
      { t: this.tS[6] + 0.35, d: 0.9, f: [1520, 560], z: 0.5 }]);
    kamera(this.b, k.f, k.z);
    zeichne(this.weg, P(t, this.tStart - 0.2, 1.4));
    const n = this.tS.filter((ts) => t >= ts - 0.1).length;
    zeichne(this.wegAktiv, n === 0 ? 0 : clamp((n - 0.5) / 7.2));
    this.st.forEach((s, i) => {
      const an = P(t, this.tS[i] - 0.1, 0.4, E.back);
      const vorbei = i < n - 1 ? 1 : 0;
      s.ring.setAttribute('stroke', an > 0.5 ? C.blue : C.line);
      s.ring.setAttribute('fill', an > 0.5 && !vorbei ? C.blue : C.surface);
      sk(s.ic, 0, 0, 1 + 0.15 * puls(t, this.tS[i], 0.8, 9));
      O(s.glow, an * (1 - 0.7 * vorbei));
      O(s.lab, 0.25 + 0.75 * an); O(s.num, 0.4 + 0.6 * an);
    });
  },
});
