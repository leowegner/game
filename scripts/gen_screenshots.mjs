// Drive the real game in headless Chromium and capture landscape screenshots.
// Output: store/screenshots/landing.png, run-early.png, run-mid.png,
// run-late.png, upgrade.png, shop.png.
import { chromium } from "playwright";
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const OUT_DIR = path.join(ROOT, "store", "screenshots");
fs.mkdirSync(OUT_DIR, { recursive: true });

// Tiny static file server rooted at the project so the game can fetch sprites.
function serve(rootDir) {
  return new Promise((resolve) => {
    const server = http.createServer((req, res) => {
      const url = decodeURIComponent(req.url.split("?")[0]);
      const safe = path.normalize(url).replace(/^(\.\.[\/\\])+/, "");
      const fsPath = path.join(rootDir, safe === "/" ? "index.html" : safe);
      fs.readFile(fsPath, (err, data) => {
        if (err) {
          res.writeHead(404);
          res.end("404");
          return;
        }
        const ext = path.extname(fsPath).toLowerCase();
        const mime = {
          ".html": "text/html",
          ".js":   "application/javascript",
          ".css":  "text/css",
          ".png":  "image/png",
          ".json": "application/json",
        }[ext] || "application/octet-stream";
        res.writeHead(200, { "Content-Type": mime });
        res.end(data);
      });
    });
    // Bind to 127.0.0.1 with port 0 = OS picks a free port.
    server.listen(0, "127.0.0.1", () => resolve(server));
  });
}

const W = 1280, H = 720;

async function snapCanvas(page, name) {
  // Read the canvas backing buffer directly so we get its native resolution
  // (1280x720) instead of the CSS-scaled size that locator.screenshot returns.
  const dataUrl = await page.evaluate(() => document.getElementById("game").toDataURL("image/png"));
  const b64 = dataUrl.split(",", 2)[1];
  fs.writeFileSync(path.join(OUT_DIR, name), Buffer.from(b64, "base64"));
}

async function snapPage(page, name) {
  await page.screenshot({ path: path.join(OUT_DIR, name), fullPage: false });
}

async function waitForGameReady(page) {
  await page.waitForFunction(() => {
    const btn = document.getElementById("start-btn");
    return btn && !btn.disabled;
  }, { timeout: 60000 });
}

(async () => {
  const server = await serve(ROOT);
  const port = server.address().port;
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  await page.goto(`http://127.0.0.1:${port}/index.html`, { waitUntil: "domcontentloaded" });

  // Expose game internals to window. The game declares them with `const` at
  // top-level, which doesn't add to window, so we re-evaluate them here.
  await page.evaluate(() => {
    // eslint-disable-next-line no-eval
    window.__game = (0, eval)("({ get state(){return state}, gainXP, givePlayerWeapon })");
  });

  // Landing screen with sprites loaded.
  await waitForGameReady(page);
  await page.waitForTimeout(400);
  await snapPage(page, "01-landing.png");

  // Shop screen.
  await page.click("#shop-btn");
  await page.waitForTimeout(400);
  await snapPage(page, "02-shop.png");
  await page.click("#shop-close-btn");
  await page.waitForTimeout(200);

  // Start a run.
  await page.click("#start-btn");
  await page.waitForFunction(() => window.__game.state && window.__game.state.running, { timeout: 5000 }).catch(() => {});

  // Drive movement so the camera pans and enemies don't pile on the player.
  const cycle = [["d"], ["d", "s"], ["s"], ["s", "a"], ["a"], ["a", "w"], ["w"], ["w", "d"]];
  let i = 0;
  let prev = [];
  const press = async (keys) => { for (const k of keys) await page.keyboard.down(k); };
  const release = async (keys) => { for (const k of keys) await page.keyboard.up(k); };
  const step = async (durationMs) => {
    await release(prev);
    prev = cycle[i++ % cycle.length];
    await press(prev);
    await page.waitForTimeout(durationMs);
  };

  // Run-early: warp ~60s in so spawn rate is interesting, give the player a
  // second weapon for visual variety, and make them invincible so they don't
  // die in the warped state.
  await page.evaluate(() => {
    const g = window.__game;
    if (g.state) {
      g.state.time = 60;
      if (g.state.player) {
        g.state.player.iframes = 99999;
        g.givePlayerWeapon(g.state.player, "orbs");
      }
    }
  });
  for (let t = 0; t < 6; t++) await step(700);
  for (let k = 0; k < 5; k++) {
    const open = await page.locator("#upgrade-screen:not(.hidden)").count();
    if (!open) break;
    await page.keyboard.press("1");
    await page.waitForTimeout(120);
  }
  await snapCanvas(page, "03-run-early.png");

  // Force a level-up overlay. Pause the game first so XP doesn't roll new
  // levels under us between snap and dismiss.
  await page.evaluate(() => {
    // Push level threshold met: bump xpNext low and feed enough XP for one tick.
    const p = window.__game.state.player;
    p.xp = p.xpNext - 1;
    window.__game.gainXP(2);
  });
  await page.waitForSelector("#upgrade-screen:not(.hidden)", { timeout: 3000 });
  await page.waitForTimeout(300);
  await snapPage(page, "04-upgrade.png");

  // Drain level-up stack.
  for (let k = 0; k < 8; k++) {
    const open = await page.locator("#upgrade-screen:not(.hidden)").count();
    if (!open) break;
    await page.keyboard.press("1");
    await page.waitForTimeout(120);
  }

  // Run-mid: bump time to push spawn waves up (but keep player invincible).
  await page.evaluate(() => {
    if (window.__game.state) {
      window.__game.state.time = 240;
      if (window.__game.state.player) window.__game.state.player.iframes = 99999;
    }
  });
  for (let t = 0; t < 8; t++) await step(700);
  // Avoid catching a level-up overlay if one popped.
  for (let k = 0; k < 5; k++) {
    const open = await page.locator("#upgrade-screen:not(.hidden)").count();
    if (!open) break;
    await page.keyboard.press("1");
    await page.waitForTimeout(120);
  }
  await snapCanvas(page, "05-run-mid.png");

  // Run-late: heavier combat, and add a few weapon levels for visual flair.
  await page.evaluate(() => {
    if (window.__game.state && window.__game.state.player) {
      ["orbs", "bolt", "lightning", "shockwave"].forEach((id) => {
        for (let n = 0; n < 3; n++) window.__game.givePlayerWeapon(window.__game.state.player, id);
      });
    }
    if (window.__game.state) {
      window.__game.state.time = 480;
      if (window.__game.state.player) window.__game.state.player.iframes = 99999;
    }
  });
  for (let t = 0; t < 8; t++) await step(700);
  for (let k = 0; k < 5; k++) {
    const open = await page.locator("#upgrade-screen:not(.hidden)").count();
    if (!open) break;
    await page.keyboard.press("1");
    await page.waitForTimeout(120);
  }
  await snapCanvas(page, "06-run-late.png");

  await release(prev);
  await browser.close();
  server.close();
  console.log("OK");
})();
