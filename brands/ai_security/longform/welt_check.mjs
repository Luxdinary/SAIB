// Loads a built chapter project in headless Chrome and reports missing word anchors and script errors of the world.
// Usage: node brands/ai_security/longform/welt_check.mjs <project_dir>
import { createRequire } from "node:module";
import { pathToFileURL } from "node:url";
import path from "node:path";
import fs from "node:fs";
const base = path.join(process.env.LOCALAPPDATA || "", "npm-cache", "_npx");
let pp = process.env.FN_PUPPETEER;
for (const d of !pp && fs.existsSync(base) ? fs.readdirSync(base) : []) { const p = path.join(base, d, "node_modules", "puppeteer-core"); if (fs.existsSync(p)) { pp = p; break; } }
const puppeteer = createRequire(import.meta.url)(pp);
const browser = await puppeteer.launch({ executablePath: process.env.FN_CHROME || "C:/Program Files/Google/Chrome/Application/chrome.exe", headless: true, args: ["--allow-file-access-from-files"] });
const page = await browser.newPage();
const errs = [];
page.on("pageerror", (e) => errs.push("pageerror: " + e.message));
page.on("console", (m) => { if (/welt|Error|error/.test(m.text())) errs.push("console: " + m.text()); });
await page.setViewport({ width: 1920, height: 1080 });
await page.goto(pathToFileURL(path.join(process.argv[2], "index.html")).href);
await new Promise((r) => setTimeout(r, 1500));
const info = await page.evaluate(() => ({
  fehlt: window.ANKER_FEHLT || [], akte: (typeof AKTE !== "undefined" ? AKTE.map((a) => a.name) : []), ende: window.ENDE,
  // events of the whole world timeline (global seconds) for the sound cues
  schnitte: (typeof SCHNITT !== "undefined" ? SCHNITT.map((s) => ({ t: s.ab, typ: (s.ueber || {}).typ || "schnitt" })) : []),
  koepfe: (typeof KOEPFE !== "undefined" ? KOEPFE.map((k) => k.ab) : []),
  marken: (typeof MARKEN !== "undefined" ? MARKEN.map((m) => ({ t: m.ab, art: m.art })) : []),
  klang: window.KLANG || [],
}));
console.log(JSON.stringify({ ...info, errors: errs }, null, 1));
await browser.close();
