// Review frames of a direction project without a video render (Scutoria Testvideo 11/2026): loads the project in
// headless Chrome, seeks the GSAP timeline and every <video> clip to each time and writes one JPEG per time, captions
// and labels included. Same lookup and clip-window logic as scripts/make_cover.mjs.
// Usage: node brands/ai_security/snap_frames.mjs <project_dir> <out_dir> <t1> <t2> ...
import { createRequire } from "node:module";
import { pathToFileURL } from "node:url";
import path from "node:path";
import fs from "node:fs";

function findPuppeteer() {
  if (process.env.FN_PUPPETEER) return process.env.FN_PUPPETEER;
  const base = path.join(process.env.LOCALAPPDATA || "", "npm-cache", "_npx");
  for (const d of fs.existsSync(base) ? fs.readdirSync(base) : []) {
    const p = path.join(base, d, "node_modules", "puppeteer-core");
    if (fs.existsSync(p)) return p;
  }
  throw new Error("puppeteer-core not found; set FN_PUPPETEER");
}
const require = createRequire(import.meta.url);
const puppeteer = require(findPuppeteer());
const CHROME = process.env.FN_CHROME || "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";

const [dir, outDir, ...times] = process.argv.slice(2);
fs.mkdirSync(outDir, { recursive: true });
const idx = path.join(dir, "index.html");
const browser = await puppeteer.launch({ executablePath: CHROME, headless: true, args: ["--allow-file-access-from-files", "--autoplay-policy=no-user-gesture-required"] });
const page = await browser.newPage();
await page.setViewport({ width: 1080, height: 1920 });
await page.goto(pathToFileURL(idx).href, { waitUntil: "load" });
for (let k = 0; k < 100 && !(await page.evaluate(() => !!(window.__timelines && window.__timelines.main))); k++) await new Promise(r => setTimeout(r, 200));
await page.evaluate(() => document.fonts.ready);
for (const ts of times) {
  await page.evaluate(async (t) => {
    window.__timelines.main.seek(t, false);
    const waits = [];
    for (const v of document.querySelectorAll("video")) {
      const s = Number(v.dataset.start || 0);
      const local = Math.max(0, t - s);
      v.pause();
      waits.push(new Promise(res => { v.addEventListener("seeked", res, { once: true }); setTimeout(res, 3000); }));
      v.currentTime = v.duration ? Math.min(local, v.duration - 0.05) : local;
    }
    await Promise.all(waits);
    for (const c of document.querySelectorAll(".clip[data-start]")) {
      const s = Number(c.dataset.start), d = Number(c.dataset.duration);
      c.style.visibility = (t < s || t > s + d) ? "hidden" : "";
    }
  }, Number(ts));
  await new Promise(r => setTimeout(r, 250));
  const out = path.join(outDir, `t${String(Number(ts).toFixed(1)).padStart(5, "0")}.jpg`);
  await page.screenshot({ path: out, type: "jpeg", quality: 82 });
  console.log(out);
}
await browser.close();
