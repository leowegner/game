// Mega Thonk - a 2D pixel-art survivors-like

const SPRITE_LIST = [
  "player",
  "enemy_goblin", "enemy_bat", "enemy_knight", "enemy_mage",
  "enemy_charger", "enemy_slime", "enemy_bomber", "enemy_boss",
  "fx_hammer", "fx_orb", "fx_bolt", "fx_lightning", "fx_shockwave", "fx_aura",
  "pickup_gem_small", "pickup_gem_large", "pickup_heart",
  "tile_grass", "tile_crypt", "tile_lava", "tile_ice",
  "prop_rock", "prop_tree", "prop_pillar", "prop_shard",
  "ui_heart", "ui_frame", "ui_badge", "ui_banner",
];

// ---------- Asset loader: loads PNGs, keys out magenta to transparent ----------

const sprites = {};

function loadSprite(name) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => {
      const c = document.createElement("canvas");
      const isTile = name.startsWith("tile_");
      if (isTile) {
        // Sample a center crop and force-mirror the edges so it tiles seamlessly.
        const SRC = Math.min(img.width, img.height);
        const CROP = Math.floor(SRC * 0.55);
        const offX = Math.floor((img.width - CROP) / 2);
        const offY = Math.floor((img.height - CROP) / 2);
        c.width = 256;
        c.height = 256;
        const tctx = c.getContext("2d");
        tctx.imageSmoothingEnabled = true;
        // Draw 4 mirrored quadrants so the edges line up perfectly.
        tctx.save();
        tctx.drawImage(img, offX, offY, CROP, CROP, 0, 0, 128, 128);
        tctx.translate(256, 0);
        tctx.scale(-1, 1);
        tctx.drawImage(img, offX, offY, CROP, CROP, 0, 0, 128, 128);
        tctx.restore();
        tctx.save();
        tctx.translate(0, 256);
        tctx.scale(1, -1);
        tctx.drawImage(img, offX, offY, CROP, CROP, 0, 0, 128, 128);
        tctx.translate(256, 0);
        tctx.scale(-1, 1);
        tctx.drawImage(img, offX, offY, CROP, CROP, 0, 0, 128, 128);
        tctx.restore();
      } else {
        c.width = img.width;
        c.height = img.height;
        const ctx = c.getContext("2d");
        ctx.drawImage(img, 0, 0);
        const data = ctx.getImageData(0, 0, c.width, c.height);
        const d = data.data;
        // Key out magenta. The AI's "magenta" is fuzzy: bright pink/purple
        // shades around #ff00ff. Detect any pixel that is much more red+blue
        // than green AND highly saturated, then also feather edges.
        for (let i = 0; i < d.length; i += 4) {
          const r = d[i], g = d[i + 1], b = d[i + 2];
          const magentaScore = (r + b) / 2 - g;
          if (magentaScore > 60 && r > 130 && b > 100 && g < 160) {
            d[i + 3] = 0;
          } else if (magentaScore > 30 && r > 150 && b > 120 && g < 180) {
            // Edge feather: partial transparency for borderline pixels.
            d[i + 3] = Math.max(0, d[i + 3] - 180);
          }
        }
        ctx.putImageData(data, 0, 0);
      }
      c.dataUrl = c.toDataURL();
      resolve(c);
    };
    img.onerror = () => reject(new Error("failed to load " + name));
    img.src = `sprites/${name}.png`;
  });
}

async function loadAllSprites(onProgress) {
  let done = 0;
  for (const name of SPRITE_LIST) {
    try {
      sprites[name] = await loadSprite(name);
    } catch (e) {
      console.warn("missing sprite", name);
      // Fallback: a solid colored square.
      const c = document.createElement("canvas");
      c.width = c.height = 64;
      const ctx = c.getContext("2d");
      ctx.fillStyle = "#ff00ff";
      ctx.fillRect(0, 0, 64, 64);
      sprites[name] = c;
    }
    done++;
    if (onProgress) onProgress(done, SPRITE_LIST.length);
  }
}

// ---------- Meta-progression (persists across runs via localStorage) ----------

const META_DEFAULT = {
  gold: 0,
  shop: {},        // { upgradeId: levelsBought }
  runNumber: 0,    // how many runs the player has completed (victories)
};

const meta = loadMeta();

function loadMeta() {
  try {
    const raw = localStorage.getItem("megathonk_meta");
    if (raw) return { ...META_DEFAULT, ...JSON.parse(raw) };
  } catch (e) {}
  return { ...META_DEFAULT, shop: {} };
}

function saveMeta() {
  try { localStorage.setItem("megathonk_meta", JSON.stringify(meta)); } catch (e) {}
}

// Shop upgrade definitions.
// Each: { id, name, desc, icon, tier, maxLevel, costBase, costGrowth, apply(player, level) }
// tier 1 = always available; tier 2 = unlocked after run 1; tier 3 = unlocked after run 2.
// apply is called once at run start for every level purchased.
const SHOP_UPGRADES = [
  // ---- Tier 1 ----
  {
    id: "start_hp",
    name: "Iron Constitution",
    desc: "+25 starting Max HP per level",
    icon: "ui_heart",
    tier: 1,
    maxLevel: 8,
    costBase: 75, costGrowth: 60,
    apply(p, lv) { p.maxHp += lv * 25; p.hp = p.maxHp; },
  },
  {
    id: "start_speed",
    name: "Fleet Feet",
    desc: "+8% move speed per level",
    icon: "ui_badge",
    tier: 1,
    maxLevel: 6,
    costBase: 100, costGrowth: 75,
    apply(p, lv) { p.speed *= Math.pow(1.08, lv); },
  },
  {
    id: "start_damage",
    name: "Brute Force",
    desc: "+12% damage per level",
    icon: "fx_hammer",
    tier: 1,
    maxLevel: 8,
    costBase: 125, costGrowth: 90,
    apply(p, lv) { p.damageMult *= Math.pow(1.12, lv); },
  },
  {
    id: "start_regen",
    name: "Life Tap",
    desc: "+0.4 HP/sec regen per level",
    icon: "pickup_heart",
    tier: 1,
    maxLevel: 6,
    costBase: 90, costGrowth: 70,
    apply(p, lv) { p.regen += lv * 0.4; },
  },
  {
    id: "start_pickup",
    name: "Magnetism",
    desc: "+30% pickup radius per level",
    icon: "pickup_gem_small",
    tier: 1,
    maxLevel: 5,
    costBase: 75, costGrowth: 50,
    apply(p, lv) { p.pickupRadius *= Math.pow(1.30, lv); },
  },
  {
    id: "start_armor",
    name: "Plate Skin",
    desc: "+2 flat armor per level",
    icon: "ui_frame",
    tier: 1,
    maxLevel: 6,
    costBase: 100, costGrowth: 80,
    apply(p, lv) { p.armor += lv * 2; },
  },
  {
    id: "gold_bonus",
    name: "Gold Digger",
    desc: "+1 bonus gold per kill per level",
    icon: "ui_badge",
    tier: 1,
    maxLevel: 5,
    costBase: 150, costGrowth: 125,
    apply(p, lv) { p._goldBonus = (p._goldBonus || 0) + lv; },
  },
  {
    id: "start_area",
    name: "Wide Berth",
    desc: "+10% weapon area per level",
    icon: "fx_shockwave",
    tier: 1,
    maxLevel: 6,
    costBase: 110, costGrowth: 90,
    apply(p, lv) { p.areaMult *= Math.pow(1.10, lv); },
  },
  {
    id: "second_weapon",
    name: "Dual Wielder",
    desc: "Start with Bonk Orbs already equipped",
    icon: "fx_orb",
    tier: 1,
    maxLevel: 1,
    costBase: 250, costGrowth: 0,
    apply(p, lv) { if (lv > 0) givePlayerWeapon(p, "orbs"); },
  },
  {
    id: "xp_boost",
    name: "Scholar",
    desc: "+15% XP gain per level (reach levels faster)",
    icon: "pickup_gem_large",
    tier: 1,
    maxLevel: 5,
    costBase: 140, costGrowth: 100,
    apply(p, lv) { p._xpMult = (p._xpMult || 1) * Math.pow(1.15, lv); },
  },

  // ---- Tier 2 (unlocked after completing run 1) ----
  {
    id: "hp_deep",
    name: "Iron Will",
    desc: "+40 starting Max HP per level",
    icon: "ui_heart",
    tier: 2,
    maxLevel: 6,
    costBase: 300, costGrowth: 200,
    apply(p, lv) { p.maxHp += lv * 40; p.hp = p.maxHp; },
  },
  {
    id: "deaths_edge",
    name: "Death's Edge",
    desc: "+20% damage while below 40% HP, per level",
    icon: "fx_hammer",
    tier: 2,
    maxLevel: 5,
    costBase: 350, costGrowth: 250,
    apply(p, lv) { p._deathsEdge = (p._deathsEdge || 0) + lv * 0.20; },
  },
  {
    id: "third_weapon",
    name: "Arsenal",
    desc: "Start with a third weapon slot unlocked",
    icon: "fx_bolt",
    tier: 2,
    maxLevel: 1,
    costBase: 500, costGrowth: 0,
    apply(p, lv) { if (lv > 0) { p._extraWeaponSlots = (p._extraWeaponSlots || 0) + 1; givePlayerWeapon(p, "bolt"); } },
  },
  {
    id: "swift_bolts",
    name: "Swiftshot",
    desc: "+20% projectile speed & +10% cooldown reduction per level",
    icon: "fx_bolt",
    tier: 2,
    maxLevel: 5,
    costBase: 280, costGrowth: 180,
    apply(p, lv) { p._projSpeedMult = (p._projSpeedMult || 1) * Math.pow(1.20, lv); p.cdMult *= Math.pow(0.90, lv); },
  },
  {
    id: "siege_aura",
    name: "Siege Aura",
    desc: "Enemies in your aura are slowed 15% per level",
    icon: "fx_aura",
    tier: 2,
    maxLevel: 4,
    costBase: 320, costGrowth: 220,
    apply(p, lv) { p._auraSlowStrength = (p._auraSlowStrength || 0) + lv * 0.15; },
  },

  // ---- Tier 3 (unlocked after completing run 2) ----
  {
    id: "last_stand",
    name: "Last Stand",
    desc: "Once per run, survive a killing blow at 1 HP",
    icon: "ui_heart",
    tier: 3,
    maxLevel: 1,
    costBase: 1200, costGrowth: 0,
    apply(p, lv) { if (lv > 0) p._lastStand = true; },
  },
  {
    id: "berserker",
    name: "Berserker",
    desc: "+5% damage per kill in a 4s window, stacks up to 10×",
    icon: "fx_hammer",
    tier: 3,
    maxLevel: 3,
    costBase: 800, costGrowth: 600,
    apply(p, lv) { p._berserkerStacks = 0; p._berserkerTimer = 0; p._berserkerMult = lv * 0.05; },
  },
  {
    id: "master_arms",
    name: "Master of Arms",
    desc: "All weapons start 1 level higher",
    icon: "fx_orb",
    tier: 3,
    maxLevel: 3,
    costBase: 900, costGrowth: 700,
    apply(p, lv) { p._weaponHeadstart = (p._weaponHeadstart || 0) + lv; },
  },
  {
    id: "titan_frame",
    name: "Titan Frame",
    desc: "+60 Max HP and +3 armor per level",
    icon: "ui_frame",
    tier: 3,
    maxLevel: 5,
    costBase: 600, costGrowth: 400,
    apply(p, lv) { p.maxHp += lv * 60; p.hp = p.maxHp; p.armor += lv * 3; },
  },
  {
    id: "gold_tide",
    name: "Gold Tide",
    desc: "+3 bonus gold per kill per level",
    icon: "ui_badge",
    tier: 3,
    maxLevel: 5,
    costBase: 700, costGrowth: 500,
    apply(p, lv) { p._goldBonus = (p._goldBonus || 0) + lv * 3; },
  },
];

function shopUpgradeCost(upg) {
  const owned = meta.shop[upg.id] || 0;
  return upg.costBase + owned * upg.costGrowth;
}

function applyShopBonuses(p) {
  for (const upg of SHOP_UPGRADES) {
    const lv = meta.shop[upg.id] || 0;
    if (lv > 0) upg.apply(p, lv);
  }
  // Master of Arms: level up each starting weapon by the headstart amount.
  if (p._weaponHeadstart > 0) {
    for (const w of p.weapons) {
      for (let i = 0; i < p._weaponHeadstart; i++) {
        const def = WEAPONS[w.id];
        if (w.level < def.maxLevel) { w.level++; def.levelUp(w); }
      }
    }
  }
}

// ---------- Core game state ----------

const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");
ctx.imageSmoothingEnabled = false;

const W = canvas.width;
const H = canvas.height;

const keys = {};
window.addEventListener("keydown", (e) => {
  keys[e.key.toLowerCase()] = true;
  if (e.key === " ") e.preventDefault();
});
window.addEventListener("keyup", (e) => { keys[e.key.toLowerCase()] = false; });

const state = {
  running: false,
  paused: false,
  time: 0,      // seconds elapsed
  kills: 0,
  gold: 0,
  player: null,
  enemies: [],
  projectiles: [],
  pickups: [],
  effects: [],
  damageNumbers: [],
  camera: { x: 0, y: 0 },
  upgradePending: 0,
  biome: "grass",
  bossSpawned: false,
  bossDead: false,
  ended: false,
  shake: 0,
};

const RUN_DURATION = 15 * 60; // 15 min
const WORLD_SIZE = 4000;      // logical arena bounds (soft)

// ---------- Math helpers ----------

function rand(a, b) { return a + Math.random() * (b - a); }
function randInt(a, b) { return Math.floor(rand(a, b + 1)); }
function dist(a, b) { const dx = a.x - b.x, dy = a.y - b.y; return Math.hypot(dx, dy); }
function dist2(a, b) { const dx = a.x - b.x, dy = a.y - b.y; return dx * dx + dy * dy; }
function clamp(v, lo, hi) { return v < lo ? lo : v > hi ? hi : v; }
function lerp(a, b, t) { return a + (b - a) * t; }
function angleTo(from, to) { return Math.atan2(to.y - from.y, to.x - from.x); }

// ---------- Player ----------

function makePlayer() {
  return {
    x: 0, y: 0,
    r: 18,
    hp: 100,
    maxHp: 100,
    speed: 180,           // px/sec
    level: 1,
    xp: 0,
    xpNext: 5,
    // Damage multipliers and utility.
    damageMult: 1.0,
    cdMult: 1.0,           // cooldown multiplier (lower = faster)
    areaMult: 1.0,
    projectileBonus: 0,
    pickupRadius: 60,
    armor: 0,
    regen: 0,              // hp/sec
    luck: 0,
    iframes: 0,
    // Weapons the player has, each with { id, level, cd, timer, ... }.
    weapons: [],
    dir: { x: 0, y: 1 },   // facing direction
    attackAnim: 0,         // melee swing anim timer
    walkCycle: 0,          // 0..1 repeating walk phase
    isMoving: false,
    landSquash: 0,         // squash-stretch on step landing
    tiltAngle: 0,          // body tilt toward movement dir
    breathe: 0,            // idle breathing phase
  };
}

// ---------- Weapons definitions ----------
//
// Each weapon has: id, name, desc, icon, maxLevel, init(w), update(w, dt, player),
// levelUp(w) applies per-level stat bumps.

const WEAPONS = {
  hammer: {
    id: "hammer",
    name: "Thonk Hammer",
    desc: "Melee arc in front of you.",
    icon: "fx_hammer",
    maxLevel: 6,
    init(w) {
      w.cd = 0.9;
      w.timer = 0;
      w.damage = 22;
      w.range = 90;
      w.arc = Math.PI * 0.9;
    },
    levelUp(w) {
      w.cd *= 0.90;
      w.damage += 14;
      w.range += 10;
      w.arc += 0.1;
    },
    update(w, dt, p) {
      w.timer -= dt * (1 / p.cdMult);
      if (w.timer <= 0) {
        w.timer = w.cd;
        p.attackAnim = 0.25;
        const range = w.range * p.areaMult;
        const dmg = w.damage * p.damageMult;
        for (const e of state.enemies) {
          if (e.dead) continue;
          const dx = e.x - p.x, dy = e.y - p.y;
          const d = Math.hypot(dx, dy);
          if (d > range + e.r) continue;
          const ang = Math.atan2(dy, dx);
          const facing = Math.atan2(p.dir.y, p.dir.x);
          let diff = Math.abs(ang - facing);
          while (diff > Math.PI) diff = Math.abs(diff - Math.PI * 2);
          if (diff < w.arc / 2) {
            dealDamage(e, dmg, { kx: dx / d, ky: dy / d, knock: 140 });
          }
        }
        spawnEffect("swing", p.x + p.dir.x * 40, p.y + p.dir.y * 40, 0.22, {
          angle: Math.atan2(p.dir.y, p.dir.x),
          range: range,
          arc: w.arc,
        });
      }
    },
  },

  orbs: {
    id: "orbs",
    name: "Bonk Orbs",
    desc: "Orbit around you and smash enemies.",
    icon: "fx_orb",
    maxLevel: 6,
    init(w) {
      w.count = 2;
      w.radius = 85;
      w.rotSpeed = 2.8;
      w.damage = 14;
      w.angle = 0;
      w.hitCd = new Map();
    },
    levelUp(w) {
      w.count++;
      w.damage += 8;
      w.radius += 8;
    },
    update(w, dt, p) {
      w.angle += dt * w.rotSpeed;
      const count = w.count + p.projectileBonus;
      const rad = w.radius * p.areaMult;
      for (let i = 0; i < count; i++) {
        const a = w.angle + (i / count) * Math.PI * 2;
        const ox = p.x + Math.cos(a) * rad;
        const oy = p.y + Math.sin(a) * rad;
        for (const e of state.enemies) {
          if (e.dead) continue;
          const d2 = (e.x - ox) ** 2 + (e.y - oy) ** 2;
          if (d2 < (e.r + 18) ** 2) {
            const key = i + "_" + e.id;
            const now = state.time;
            const last = w.hitCd.get(key) || -1;
            if (now - last > 0.4) {
              w.hitCd.set(key, now);
              dealDamage(e, w.damage * p.damageMult, { kx: 0, ky: 0, knock: 40 });
            }
          }
        }
      }
      w._drawCount = count;
      w._drawRad = rad;
    },
    draw(w, p) {
      const count = w._drawCount || w.count;
      const rad = w._drawRad || w.radius;
      for (let i = 0; i < count; i++) {
        const a = w.angle + (i / count) * Math.PI * 2;
        const ox = p.x + Math.cos(a) * rad;
        const oy = p.y + Math.sin(a) * rad;
        drawSprite(sprites.fx_orb, ox, oy, 38);
      }
    },
  },

  bolt: {
    id: "bolt",
    name: "Seeker Bolts",
    desc: "Auto-fire homing bolts at nearest enemy.",
    icon: "fx_bolt",
    maxLevel: 6,
    init(w) {
      w.cd = 0.7;
      w.timer = 0;
      w.damage = 16;
      w.count = 1;
      w.speed = 420;
    },
    levelUp(w) {
      w.cd *= 0.88;
      w.damage += 10;
      if (w.count < 4) w.count++;
    },
    update(w, dt, p) {
      w.timer -= dt * (1 / p.cdMult);
      if (w.timer <= 0) {
        w.timer = w.cd;
        const targets = findNearestEnemies(p, w.count + p.projectileBonus);
        for (const t of targets) {
          const ang = angleTo(p, t);
          const spd = w.speed * (p._projSpeedMult || 1);
          state.projectiles.push({
            x: p.x, y: p.y, vx: Math.cos(ang) * spd, vy: Math.sin(ang) * spd,
            life: 2.5, damage: w.damage * p.damageMult, sprite: "fx_bolt",
            r: 14, homing: 2.2, target: t,
          });
        }
      }
    },
  },

  lightning: {
    id: "lightning",
    name: "Chain Lightning",
    desc: "Zap the nearest enemies from the sky.",
    icon: "fx_lightning",
    maxLevel: 6,
    init(w) {
      w.cd = 2.2;
      w.timer = 0;
      w.damage = 40;
      w.targets = 2;
    },
    levelUp(w) {
      w.cd *= 0.9;
      w.damage += 25;
      w.targets++;
    },
    update(w, dt, p) {
      w.timer -= dt * (1 / p.cdMult);
      if (w.timer <= 0) {
        w.timer = w.cd;
        const targets = findNearestEnemies(p, w.targets + p.projectileBonus);
        for (const t of targets) {
          dealDamage(t, w.damage * p.damageMult, { kx: 0, ky: 0, knock: 20 });
          spawnEffect("lightning", t.x, t.y, 0.35, {});
        }
      }
    },
  },

  shockwave: {
    id: "shockwave",
    name: "Shockwave",
    desc: "Periodic radial blast around you.",
    icon: "fx_shockwave",
    maxLevel: 6,
    init(w) {
      w.cd = 3.0;
      w.timer = 1.0;
      w.damage = 30;
      w.radius = 160;
    },
    levelUp(w) {
      w.cd *= 0.9;
      w.damage += 20;
      w.radius += 30;
    },
    update(w, dt, p) {
      w.timer -= dt * (1 / p.cdMult);
      if (w.timer <= 0) {
        w.timer = w.cd;
        const rad = w.radius * p.areaMult;
        for (const e of state.enemies) {
          if (e.dead) continue;
          const d = dist(e, p);
          if (d < rad + e.r) {
            const k = d > 0 ? 1 / d : 0;
            dealDamage(e, w.damage * p.damageMult, {
              kx: (e.x - p.x) * k, ky: (e.y - p.y) * k, knock: 220,
            });
          }
        }
        spawnEffect("shockwave", p.x, p.y, 0.45, { radius: rad });
        state.shake = Math.max(state.shake, 6);
      }
    },
  },

  aura: {
    id: "aura",
    name: "Bleed Aura",
    desc: "Constant damage field around you.",
    icon: "fx_aura",
    maxLevel: 6,
    init(w) {
      w.dps = 14;
      w.radius = 110;
    },
    levelUp(w) {
      w.dps += 10;
      w.radius += 14;
    },
    update(w, dt, p) {
      const rad = w.radius * p.areaMult;
      const dmg = w.dps * dt * p.damageMult;
      const slowFactor = p._auraSlowStrength ? Math.max(0.1, 1 - p._auraSlowStrength) : 1;
      for (const e of state.enemies) {
        if (e.dead) continue;
        if (dist2(e, p) < (rad + e.r) ** 2) {
          dealDamage(e, dmg, { kx: 0, ky: 0, knock: 0 }, true);
          e._auraSlow = slowFactor;
        } else {
          e._auraSlow = 1;
        }
      }
    },
    draw(w, p) {
      const rad = w.radius * p.areaMult;
      ctx.save();
      ctx.globalAlpha = 0.22 + Math.sin(state.time * 8) * 0.05;
      ctx.fillStyle = "#ff4a2a";
      ctx.beginPath();
      ctx.arc(p.x - state.camera.x, p.y - state.camera.y, rad, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    },
  },
};

function givePlayerWeapon(p, id) {
  const def = WEAPONS[id];
  const existing = p.weapons.find((w) => w.id === id);
  if (existing) {
    if (existing.level < def.maxLevel) {
      existing.level++;
      def.levelUp(existing);
    }
    return;
  }
  const w = { id, level: 1 };
  def.init(w);
  p.weapons.push(w);
}

// ---------- Passive upgrades ----------

const PASSIVES = {
  maxhp:    { name: "Vitality",    desc: "+20 Max HP, full heal",       icon: "ui_heart",  maxLevel: 5, apply(p) { p.maxHp += 20; p.hp = p.maxHp; } },
  speed:    { name: "Swiftness",   desc: "+10% move speed",             icon: "ui_badge",  maxLevel: 5, apply(p) { p.speed *= 1.10; } },
  damage:   { name: "Power",       desc: "+15% damage",                 icon: "fx_hammer", maxLevel: 8, apply(p) { p.damageMult *= 1.15; } },
  cdr:      { name: "Haste",       desc: "-8% cooldowns",               icon: "fx_bolt",   maxLevel: 6, apply(p) { p.cdMult *= 0.92; } },
  area:     { name: "Expansion",   desc: "+12% area / range",           icon: "fx_shockwave", maxLevel: 6, apply(p) { p.areaMult *= 1.12; } },
  proj:     { name: "Multishot",   desc: "+1 projectile / orb / zap",   icon: "fx_bolt",   maxLevel: 3, apply(p) { p.projectileBonus += 1; } },
  pickup:   { name: "Magnetism",   desc: "+40% pickup radius",          icon: "pickup_gem_small", maxLevel: 5, apply(p) { p.pickupRadius *= 1.40; } },
  armor:    { name: "Armor",       desc: "+2 flat damage reduction",    icon: "ui_frame",  maxLevel: 5, apply(p) { p.armor += 2; } },
  regen:    { name: "Regeneration", desc: "+0.5 HP/sec",                icon: "pickup_heart", maxLevel: 5, apply(p) { p.regen += 0.5; } },
  luck:     { name: "Luck",        desc: "+15% luck",                   icon: "ui_badge",  maxLevel: 5, apply(p) { p.luck += 0.15; } },
};

// Per-player track of passive levels.
const passiveLevels = {};

// ---------- Enemy definitions ----------

const ENEMIES = {
  goblin:  { sprite: "enemy_goblin",  hp: 14,  speed: 80,  dmg: 8,  r: 18, xp: 1, kind: "walker" },
  bat:     { sprite: "enemy_bat",     hp: 8,   speed: 140, dmg: 6,  r: 14, xp: 1, kind: "flyer" },
  knight:  { sprite: "enemy_knight",  hp: 80,  speed: 55,  dmg: 14, r: 22, xp: 3, kind: "walker", armor: 3 },
  mage:    { sprite: "enemy_mage",    hp: 28,  speed: 60,  dmg: 10, r: 18, xp: 3, kind: "caster" },
  charger: { sprite: "enemy_charger", hp: 60,  speed: 70,  dmg: 18, r: 22, xp: 4, kind: "charger" },
  slime:   { sprite: "enemy_slime",   hp: 40,  speed: 55,  dmg: 10, r: 20, xp: 2, kind: "splitter" },
  bomber:  { sprite: "enemy_bomber",  hp: 20,  speed: 95,  dmg: 28, r: 18, xp: 3, kind: "bomber" },
};

// Wave schedule: each entry = { at: minutes, types: [...], rate: spawns/sec, cap: soft }.
// The actual count scales with time.
const WAVES = [
  { at: 0,  types: ["goblin"],                           rate: 1.8, cap: 40 },
  { at: 1,  types: ["goblin", "bat"],                    rate: 2.3, cap: 55 },
  { at: 3,  types: ["goblin", "bat", "knight"],          rate: 2.8, cap: 70 },
  { at: 4,  types: ["bat", "knight", "mage"],            rate: 3.2, cap: 85 },
  { at: 6,  types: ["knight", "mage", "charger"],        rate: 3.6, cap: 100 },
  { at: 7,  types: ["bat", "charger", "slime"],          rate: 4.0, cap: 115 },
  { at: 9,  types: ["mage", "charger", "slime", "bomber"], rate: 4.4, cap: 130 },
  { at: 11, types: ["knight", "charger", "bomber", "bat"], rate: 4.8, cap: 150 },
  { at: 13, types: ["bomber", "charger", "mage", "slime", "knight"], rate: 5.2, cap: 170 },
];

function currentWave() {
  const m = state.time / 60;
  let w = WAVES[0];
  for (const wv of WAVES) if (m >= wv.at) w = wv;
  return w;
}

function timeDifficultyMultiplier() {
  // Enemy HP and damage scale over time within a run.
  const m = state.time / 60;
  return 1 + m * 0.35 + (m * m) * 0.03;
}

// Extra multiplier based on how many runs the player has completed.
// Run 0 = 1.0x, run 1 = 1.5x HP / 1.35x dmg, run 2 = 2.0x HP / 1.7x dmg, etc.
function runHpMultiplier()  { return 1 + meta.runNumber * 0.5; }
function runDmgMultiplier() { return 1 + meta.runNumber * 0.35; }
function runSpawnMultiplier() { return 1 + meta.runNumber * 0.2; }

let nextEnemyId = 1;

function spawnEnemy(type) {
  const def = ENEMIES[type];
  // Spawn just outside a ring around the camera.
  const p = state.player;
  const ang = rand(0, Math.PI * 2);
  const r = rand(650, 780);
  const mul = timeDifficultyMultiplier();
  const hpMul = mul * runHpMultiplier();
  const dmgMul = mul * runDmgMultiplier();
  const e = {
    id: nextEnemyId++,
    type,
    sprite: def.sprite,
    x: p.x + Math.cos(ang) * r,
    y: p.y + Math.sin(ang) * r,
    vx: 0, vy: 0,
    hp: def.hp * hpMul,
    maxHp: def.hp * hpMul,
    dmg: def.dmg * dmgMul,
    speed: def.speed,
    r: def.r,
    xp: def.xp,
    kind: def.kind,
    armor: def.armor || 0,
    dead: false,
    hitFlash: 0,
    contactCd: 0,
    // Per-kind state
    castTimer: rand(1, 3),
    chargeState: "idle", chargeTimer: 0, chargeDir: { x: 0, y: 0 },
    fuseTimer: -1,
  };
  state.enemies.push(e);
}

function spawnBoss() {
  const p = state.player;
  const ang = rand(0, Math.PI * 2);
  const e = {
    id: nextEnemyId++,
    type: "boss",
    sprite: "enemy_boss",
    x: p.x + Math.cos(ang) * 500,
    y: p.y + Math.sin(ang) * 500,
    vx: 0, vy: 0,
    hp: 8000 * timeDifficultyMultiplier() * runHpMultiplier(),
    maxHp: 8000 * timeDifficultyMultiplier() * runHpMultiplier(),
    dmg: 35 + meta.runNumber * 10,
    speed: 90,
    r: 72,
    xp: 500,
    kind: "boss",
    armor: 5,
    dead: false,
    hitFlash: 0,
    contactCd: 0,
    isBoss: true,
    castTimer: 3,
  };
  state.enemies.push(e);
  state.shake = 18;
}

// ---------- Damage & effects ----------

function dealDamage(e, amount, push, quiet) {
  if (e.dead) return;
  const final = Math.max(1, amount - (e.armor || 0));
  e.hp -= final;
  e.hitFlash = 0.12;
  if (push && push.knock) {
    e.vx += push.kx * push.knock;
    e.vy += push.ky * push.knock;
  }
  if (!quiet) {
    state.damageNumbers.push({
      x: e.x + rand(-8, 8), y: e.y - e.r, val: Math.round(final), life: 0.8, vy: -40,
    });
  }
  if (e.hp <= 0) killEnemy(e);
}

function killEnemy(e) {
  e.dead = true;
  state.kills++;
  state.gold += 1 + (state.player._goldBonus || 0);
  // Berserker: gain a stack on kill, reset 4s timer, cap at 10.
  const p = state.player;
  if (p._berserkerMult) {
    p._berserkerStacks = Math.min(10, (p._berserkerStacks || 0) + 1);
    p._berserkerTimer = 4;
  }
  // XP drop.
  if (e.isBoss) {
    // Shower of gems + healing.
    for (let i = 0; i < 40; i++) {
      state.pickups.push(makeGem(e.x + rand(-80, 80), e.y + rand(-80, 80), "large"));
    }
    state.pickups.push(makeHeart(e.x, e.y));
    state.bossDead = true;
    state.shake = 30;
    endRun(true);
    return;
  }
  const kind = Math.random() < 0.04 ? "heart"
    : (e.xp >= 3 || Math.random() < 0.1) ? "large" : "small";
  if (kind === "heart") state.pickups.push(makeHeart(e.x, e.y));
  else state.pickups.push(makeGem(e.x, e.y, kind));
  // Splitter: slime splits into two smaller slimes on death.
  if (e.type === "slime" && e.r > 12) {
    for (let i = 0; i < 2; i++) {
      const child = {
        id: nextEnemyId++,
        type: "slime",
        sprite: "enemy_slime",
        x: e.x + rand(-10, 10),
        y: e.y + rand(-10, 10),
        vx: rand(-60, 60), vy: rand(-60, 60),
        hp: e.maxHp * 0.4,
        maxHp: e.maxHp * 0.4,
        dmg: e.dmg * 0.7,
        speed: e.speed * 1.2,
        r: e.r * 0.65,
        xp: 1,
        kind: "walker",
        armor: 0,
        dead: false, hitFlash: 0, contactCd: 0,
      };
      state.enemies.push(child);
    }
  }
}

function makeGem(x, y, kind) {
  return {
    x, y, kind: "gem", size: kind,
    xp: kind === "large" ? 5 : 1,
    sprite: kind === "large" ? "pickup_gem_large" : "pickup_gem_small",
    r: 14, vy: 0, bob: rand(0, Math.PI * 2),
  };
}

function makeHeart(x, y) {
  return { x, y, kind: "heart", sprite: "pickup_heart", r: 16, heal: 25, bob: rand(0, Math.PI * 2) };
}

function spawnEffect(kind, x, y, life, data) {
  state.effects.push({ kind, x, y, life, maxLife: life, data: data || {} });
}

// ---------- Utility: find nearest enemies ----------

function findNearestEnemies(p, n) {
  const arr = [];
  for (const e of state.enemies) if (!e.dead) arr.push(e);
  arr.sort((a, b) => dist2(a, p) - dist2(b, p));
  return arr.slice(0, n);
}

// ---------- Update loop ----------

let lastTime = performance.now();
let spawnAccum = 0;

function update(dt) {
  if (!state.running || state.paused || state.upgradePending > 0 || state.ended) return;
  state.time += dt;

  // Biome changes every ~4 minutes.
  const biomes = ["grass", "crypt", "lava", "ice"];
  state.biome = biomes[Math.min(biomes.length - 1, Math.floor(state.time / (RUN_DURATION / biomes.length)))];

  const p = state.player;

  // ----- Player movement -----
  let mx = 0, my = 0;
  if (keys["w"] || keys["arrowup"]) my -= 1;
  if (keys["s"] || keys["arrowdown"]) my += 1;
  if (keys["a"] || keys["arrowleft"]) mx -= 1;
  if (keys["d"] || keys["arrowright"]) mx += 1;
  const mag = Math.hypot(mx, my);
  p.isMoving = mag > 0;
  if (p.isMoving) {
    mx /= mag; my /= mag;
    p.dir.x = mx; p.dir.y = my;
    p.x += mx * p.speed * dt;
    p.y += my * p.speed * dt;
    // Walk cycle: advance phase, trigger squash on each step landing.
    const prevCycle = p.walkCycle;
    p.walkCycle = (p.walkCycle + dt * 6.5) % 1;
    // Detect crossing the 0.5 boundary = one foot hits ground.
    if (prevCycle < 0.5 && p.walkCycle >= 0.5) p.landSquash = 0.18;
    if (prevCycle > p.walkCycle) p.landSquash = 0.18; // wrapped past 1.0
    // Tilt toward movement direction.
    p.tiltAngle = lerp(p.tiltAngle, mx * 0.18, 1 - Math.pow(0.01, dt));
  } else {
    p.walkCycle = 0;
    p.tiltAngle = lerp(p.tiltAngle, 0, 1 - Math.pow(0.05, dt));
    p.breathe = (p.breathe + dt * 1.4) % (Math.PI * 2);
  }
  // Decay squash.
  p.landSquash = lerp(p.landSquash, 0, 1 - Math.pow(0.001, dt));
  p.x = clamp(p.x, -WORLD_SIZE, WORLD_SIZE);
  p.y = clamp(p.y, -WORLD_SIZE, WORLD_SIZE);

  // Regen & iframes.
  if (p.regen > 0 && p.hp < p.maxHp) p.hp = Math.min(p.maxHp, p.hp + p.regen * dt);
  if (p.iframes > 0) p.iframes -= dt;
  if (p.attackAnim > 0) p.attackAnim -= dt;

  // Apply transient damage bonuses (Death's Edge, Berserker) into damageMult each tick.
  // We store the base damageMult and recompute each frame so bonuses stack correctly.
  p._baseDamageMult = p._baseDamageMult || p.damageMult;
  let tickDmgMult = p._baseDamageMult;
  if (p._deathsEdge && p.hp / p.maxHp < 0.4) tickDmgMult *= (1 + p._deathsEdge);
  if (p._berserkerStacks > 0 && p._berserkerMult) tickDmgMult *= (1 + p._berserkerStacks * p._berserkerMult);
  p.damageMult = tickDmgMult;

  // ----- Weapons update -----
  for (const w of p.weapons) {
    const def = WEAPONS[w.id];
    def.update(w, dt, p);
  }

  // ----- Spawn enemies -----
  if (!state.bossSpawned) {
    const wave = currentWave();
    spawnAccum += dt * wave.rate * (1 + state.time / 120) * runSpawnMultiplier();
    const cap = wave.cap + Math.floor(state.time / 20);
    while (spawnAccum >= 1 && state.enemies.length < cap) {
      spawnAccum -= 1;
      const type = wave.types[randInt(0, wave.types.length - 1)];
      spawnEnemy(type);
    }
  }

  // Boss at 15 min.
  if (!state.bossSpawned && state.time >= RUN_DURATION) {
    state.bossSpawned = true;
    spawnBoss();
  }

  // ----- Update enemies -----
  for (const e of state.enemies) {
    if (e.dead) continue;
    if (e.hitFlash > 0) e.hitFlash -= dt;
    if (e.contactCd > 0) e.contactCd -= dt;

    // Apply knockback velocity with friction.
    e.x += e.vx * dt;
    e.y += e.vy * dt;
    e.vx *= 0.85;
    e.vy *= 0.85;

    const dx = p.x - e.x, dy = p.y - e.y;
    const d = Math.hypot(dx, dy) || 1;
    const nx = dx / d, ny = dy / d;
    const eSlow = e._auraSlow !== undefined ? e._auraSlow : 1;

    if (e.kind === "caster") {
      // Stop at medium range and fire projectile.
      if (d > 280) {
        e.x += nx * e.speed * eSlow * dt;
        e.y += ny * e.speed * eSlow * dt;
      }
      e.castTimer -= dt;
      if (e.castTimer <= 0) {
        e.castTimer = rand(1.8, 2.8);
        const sp = 220;
        state.projectiles.push({
          x: e.x, y: e.y, vx: nx * sp, vy: ny * sp,
          life: 4, damage: e.dmg * 0.7, hostile: true, r: 10, sprite: "fx_bolt",
        });
      }
    } else if (e.kind === "charger") {
      if (e.chargeState === "idle") {
        e.x += nx * e.speed * eSlow * dt;
        e.y += ny * e.speed * eSlow * dt;
        if (d < 260) {
          e.chargeState = "wind";
          e.chargeTimer = 0.7;
          e.chargeDir.x = nx; e.chargeDir.y = ny;
        }
      } else if (e.chargeState === "wind") {
        e.chargeTimer -= dt;
        if (e.chargeTimer <= 0) { e.chargeState = "dash"; e.chargeTimer = 0.5; }
      } else if (e.chargeState === "dash") {
        e.x += e.chargeDir.x * e.speed * 4 * eSlow * dt;
        e.y += e.chargeDir.y * e.speed * 4 * eSlow * dt;
        e.chargeTimer -= dt;
        if (e.chargeTimer <= 0) { e.chargeState = "idle"; }
      }
    } else if (e.kind === "bomber") {
      e.x += nx * e.speed * eSlow * dt;
      e.y += ny * e.speed * eSlow * dt;
      if (d < 60 && e.fuseTimer < 0) e.fuseTimer = 0.5;
      if (e.fuseTimer >= 0) {
        e.fuseTimer -= dt;
        if (e.fuseTimer <= 0) {
          // Explode.
          spawnEffect("shockwave", e.x, e.y, 0.4, { radius: 90, color: "#ff8a3a" });
          if (dist(p, e) < 100 && p.iframes <= 0) {
            p.hp -= Math.max(1, e.dmg - p.armor);
            p.iframes = 0.4;
            state.shake = 10;
          }
          e.dead = true;
          state.kills++;
        }
      }
    } else if (e.kind === "boss") {
      e.x += nx * e.speed * eSlow * dt;
      e.y += ny * e.speed * eSlow * dt;
      e.castTimer -= dt;
      if (e.castTimer <= 0) {
        e.castTimer = 1.6;
        // Radial burst.
        const count = 10;
        for (let i = 0; i < count; i++) {
          const a = (i / count) * Math.PI * 2;
          state.projectiles.push({
            x: e.x, y: e.y, vx: Math.cos(a) * 180, vy: Math.sin(a) * 180,
            life: 4, damage: 20, hostile: true, r: 12, sprite: "fx_bolt",
          });
        }
      }
    } else {
      // walker / flyer / splitter: chase the player.
      e.x += nx * e.speed * eSlow * dt;
      e.y += ny * e.speed * eSlow * dt;
    }

    // Player contact damage.
    if (d < e.r + p.r && e.contactCd <= 0 && p.iframes <= 0) {
      p.hp -= Math.max(1, e.dmg * 0.25 - p.armor);
      p.iframes = 0.5;
      e.contactCd = 0.5;
      state.shake = Math.max(state.shake, 5);
    }
  }

  // Enemy-enemy separation (cheap): nudge overlapping pairs apart.
  for (let i = 0; i < state.enemies.length; i++) {
    const a = state.enemies[i];
    if (a.dead) continue;
    for (let j = i + 1; j < state.enemies.length; j++) {
      const b = state.enemies[j];
      if (b.dead) continue;
      const dx = b.x - a.x, dy = b.y - a.y;
      const d2v = dx * dx + dy * dy;
      const rr = (a.r + b.r) * 0.9;
      if (d2v < rr * rr && d2v > 0.001) {
        const d2r = Math.sqrt(d2v);
        const push = (rr - d2r) * 0.5;
        const pxn = dx / d2r, pyn = dy / d2r;
        a.x -= pxn * push; a.y -= pyn * push;
        b.x += pxn * push; b.y += pyn * push;
      }
    }
  }

  // ----- Update projectiles -----
  for (const pr of state.projectiles) {
    if (pr.homing && pr.target && !pr.target.dead) {
      const a = angleTo(pr, pr.target);
      const speed = Math.hypot(pr.vx, pr.vy);
      const cvx = Math.cos(a) * speed, cvy = Math.sin(a) * speed;
      pr.vx = lerp(pr.vx, cvx, pr.homing * dt);
      pr.vy = lerp(pr.vy, cvy, pr.homing * dt);
    }
    pr.x += pr.vx * dt;
    pr.y += pr.vy * dt;
    pr.life -= dt;
    if (pr.hostile) {
      if (dist(pr, p) < pr.r + p.r && p.iframes <= 0) {
        p.hp -= Math.max(1, pr.damage - p.armor);
        p.iframes = 0.4;
        pr.life = 0;
        state.shake = Math.max(state.shake, 4);
      }
    } else {
      for (const e of state.enemies) {
        if (e.dead) continue;
        if (dist2(pr, e) < (pr.r + e.r) ** 2) {
          dealDamage(e, pr.damage, { kx: pr.vx * 0.001, ky: pr.vy * 0.001, knock: 60 });
          pr.life = 0;
          break;
        }
      }
    }
  }

  // ----- Pickups -----
  for (const pk of state.pickups) {
    pk.bob += dt * 3;
    const d = dist(pk, p);
    if (d < p.pickupRadius) {
      const ang = angleTo(pk, p);
      const pull = 280 + (p.pickupRadius - d) * 2;
      pk.x += Math.cos(ang) * pull * dt;
      pk.y += Math.sin(ang) * pull * dt;
    }
    if (d < p.r + pk.r) {
      pk.collected = true;
      if (pk.kind === "gem") {
        gainXP(pk.xp);
      } else if (pk.kind === "heart") {
        p.hp = Math.min(p.maxHp, p.hp + pk.heal);
      }
    }
  }

  // ----- Damage numbers -----
  for (const dn of state.damageNumbers) {
    dn.life -= dt;
    dn.y += dn.vy * dt;
    dn.vy += 30 * dt;
  }

  // ----- Cleanup -----
  state.enemies = state.enemies.filter((e) => !e.dead);
  state.projectiles = state.projectiles.filter((pr) => pr.life > 0);
  state.pickups = state.pickups.filter((pk) => !pk.collected);
  state.effects = state.effects.filter((ef) => (ef.life -= dt) > 0);
  state.damageNumbers = state.damageNumbers.filter((dn) => dn.life > 0);

  // Camera follows player with screen shake.
  state.camera.x = p.x - W / 2;
  state.camera.y = p.y - H / 2;
  if (state.shake > 0) {
    state.camera.x += rand(-state.shake, state.shake);
    state.camera.y += rand(-state.shake, state.shake);
    state.shake *= 0.88;
    if (state.shake < 0.2) state.shake = 0;
  }

  // Death.
  if (p.hp <= 0 && !state.ended) {
    if (p._lastStand) {
      p._lastStand = false;
      p.hp = 1;
      p.iframes = 2.0;
      state.shake = 20;
    } else {
      p.hp = 0;
      endRun(false);
    }
  }

  // Berserker: decay stack timer.
  if (p._berserkerStacks > 0) {
    p._berserkerTimer -= dt;
    if (p._berserkerTimer <= 0) {
      p._berserkerStacks = 0;
    }
  }

  updateHUD();
}

// ---------- XP & leveling ----------

function gainXP(amount) {
  const p = state.player;
  p.xp += amount * (p._xpMult || 1);
  while (p.xp >= p.xpNext) {
    p.xp -= p.xpNext;
    p.level++;
    p.xpNext = Math.floor(5 + p.level * 3 + p.level * p.level * 0.4);
    state.upgradePending++;
  }
  if (state.upgradePending > 0) showUpgradeScreen();
}

// ---------- Upgrade draft ----------

function rollUpgradeChoices() {
  const p = state.player;
  const pool = [];

  // Weapons: new ones, or level-ups of existing.
  for (const id of Object.keys(WEAPONS)) {
    const existing = p.weapons.find((w) => w.id === id);
    const def = WEAPONS[id];
    if (!existing) {
      if (p.weapons.length < 5) {
        pool.push({ type: "newWeapon", id, name: def.name, desc: def.desc, icon: def.icon, level: 1 });
      }
    } else if (existing.level < def.maxLevel) {
      pool.push({ type: "weaponUp", id, name: def.name, desc: def.desc + " (+)", icon: def.icon, level: existing.level + 1 });
    }
  }

  // Passives.
  for (const id of Object.keys(PASSIVES)) {
    const def = PASSIVES[id];
    const lv = passiveLevels[id] || 0;
    if (lv < def.maxLevel) {
      pool.push({ type: "passive", id, name: def.name, desc: def.desc, icon: def.icon, level: lv + 1 });
    }
  }

  // Shuffle and take 3.
  for (let i = pool.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [pool[i], pool[j]] = [pool[j], pool[i]];
  }
  return pool.slice(0, 3);
}

function applyChoice(choice) {
  const p = state.player;
  if (choice.type === "newWeapon" || choice.type === "weaponUp") {
    givePlayerWeapon(p, choice.id);
  } else if (choice.type === "passive") {
    passiveLevels[choice.id] = (passiveLevels[choice.id] || 0) + 1;
    PASSIVES[choice.id].apply(p);
  }
}

function showUpgradeScreen() {
  const screen = document.getElementById("upgrade-screen");
  const cards = document.getElementById("upgrade-cards");
  cards.innerHTML = "";
  const choices = rollUpgradeChoices();
  if (choices.length === 0) {
    // No upgrades left: give gold instead.
    state.gold += 10;
    state.upgradePending--;
    if (state.upgradePending > 0) showUpgradeScreen();
    return;
  }
  choices.forEach((c, i) => {
    const card = document.createElement("div");
    card.className = "card";
    const iconCanvas = sprites[c.icon];
    const iconUrl = (iconCanvas && iconCanvas.dataUrl) ? iconCanvas.dataUrl : `sprites/${c.icon}.png`;
    card.innerHTML = `
      <div class="card-icon" style="background-image:url('${iconUrl}')"></div>
      <div class="card-title">${c.name}</div>
      <div class="card-level">${c.type === "newWeapon" ? "NEW" : "LV " + c.level}</div>
      <div class="card-desc">${c.desc}</div>
      <div class="card-key">${i + 1}</div>
    `;
    card.onclick = () => pickChoice(c);
    cards.appendChild(card);
  });
  screen.classList.remove("hidden");
  state.activeChoices = choices;
}

function pickChoice(c) {
  applyChoice(c);
  state.upgradePending--;
  document.getElementById("upgrade-screen").classList.add("hidden");
  if (state.upgradePending > 0) showUpgradeScreen();
}

window.addEventListener("keydown", (e) => {
  if (state.upgradePending > 0 && state.activeChoices) {
    const n = parseInt(e.key, 10);
    if (n >= 1 && n <= state.activeChoices.length) {
      pickChoice(state.activeChoices[n - 1]);
    }
  }
  if (e.key.toLowerCase() === "p" && state.running && !state.ended && state.upgradePending === 0) {
    state.paused = !state.paused;
    if (state.paused) showScreen("pause-screen"); else showScreen(null);
  }
});

// ---------- HUD ----------

function updateHUD() {
  const p = state.player;
  const hp = document.getElementById("hp-fill");
  const hpText = document.getElementById("hp-text");
  const xp = document.getElementById("xp-fill");
  const xpText = document.getElementById("xp-text");
  hp.style.width = (100 * clamp(p.hp / p.maxHp, 0, 1)) + "%";
  hpText.textContent = `${Math.ceil(p.hp)} / ${p.maxHp}`;
  xp.style.width = (100 * clamp(p.xp / p.xpNext, 0, 1)) + "%";
  xpText.textContent = `LV ${p.level}`;
  const mm = Math.floor(state.time / 60).toString().padStart(2, "0");
  const ss = Math.floor(state.time % 60).toString().padStart(2, "0");
  document.getElementById("timer").textContent = `${mm}:${ss}`;
  document.getElementById("kills").textContent = `Kills: ${state.kills}`;
  document.getElementById("gold").textContent = `Gold: ${state.gold}`;
}

// ---------- Rendering ----------

function drawSprite(canvasImg, worldX, worldY, size, opts) {
  if (!canvasImg) return;
  const sx = worldX - state.camera.x - size / 2;
  const sy = worldY - state.camera.y - size / 2;
  if (sx + size < 0 || sy + size < 0 || sx > W || sy > H) return;
  if (opts && opts.flash) {
    ctx.save();
    ctx.drawImage(canvasImg, sx, sy, size, size);
    ctx.globalCompositeOperation = "source-atop";
    ctx.fillStyle = "rgba(255,255,255,0.7)";
    ctx.fillRect(sx, sy, size, size);
    ctx.restore();
  } else {
    ctx.drawImage(canvasImg, sx, sy, size, size);
  }
}

function drawBackground() {
  const tile = sprites["tile_" + state.biome] || sprites.tile_grass;
  if (!tile) return;
  const size = 256;
  const cx = state.camera.x, cy = state.camera.y;
  const x0 = Math.floor(cx / size) * size - cx;
  const y0 = Math.floor(cy / size) * size - cy;
  for (let y = y0; y < H; y += size) {
    for (let x = x0; x < W; x += size) {
      ctx.drawImage(tile, x, y, size, size);
    }
  }
  // Vignette edges toward arena bounds.
  ctx.save();
  ctx.globalAlpha = 0.25;
  ctx.fillStyle = "#000";
  const grad = ctx.createRadialGradient(W / 2, H / 2, Math.min(W, H) * 0.35, W / 2, H / 2, Math.max(W, H) * 0.7);
  grad.addColorStop(0, "rgba(0,0,0,0)");
  grad.addColorStop(1, "rgba(0,0,0,0.55)");
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, W, H);
  ctx.restore();
}

function draw() {
  drawBackground();

  // Pickups (below entities).
  for (const pk of state.pickups) {
    const bob = Math.sin(pk.bob) * 3;
    drawSprite(sprites[pk.sprite], pk.x, pk.y + bob, pk.kind === "heart" ? 28 : 22);
  }

  // Player weapon draws (ground fx like aura under player).
  const p = state.player;
  for (const w of p.weapons) {
    const def = WEAPONS[w.id];
    if (def.draw) def.draw(w, p);
  }

  // Enemies.
  const sorted = state.enemies.slice().sort((a, b) => a.y - b.y);
  for (const e of sorted) {
    const size = e.r * 2.5;
    let bobY = 0;
    if (e.kind === "flyer") bobY = Math.sin(state.time * 6 + e.id) * 4;
    drawSprite(sprites[e.sprite], e.x, e.y + bobY, size, { flash: e.hitFlash > 0 });
    // Health bar for bosses and elites.
    if (e.isBoss || e.maxHp > 200) {
      const bw = Math.max(60, size * 1.2);
      const bx = e.x - state.camera.x - bw / 2;
      const by = e.y - state.camera.y - size / 2 - 14;
      ctx.fillStyle = "#000";
      ctx.fillRect(bx - 1, by - 1, bw + 2, 8);
      ctx.fillStyle = "#d43a3a";
      ctx.fillRect(bx, by, bw * clamp(e.hp / e.maxHp, 0, 1), 6);
    }
  }

  // ---------- Procedural player animation ----------
  const pSize = 64;
  const psx = p.x - state.camera.x;
  const psy = p.y - state.camera.y;
  const spr = sprites.player;
  if (spr) {
    // --- Compute animation values ---
    // Vertical body bob while walking (sine over walk cycle).
    const bobY = p.isMoving ? Math.sin(p.walkCycle * Math.PI * 2) * 3.5 : Math.sin(p.breathe) * 1.2;
    // Leg scissor offset: bottom half shifts left/right alternately.
    const legOffset = p.isMoving ? Math.sin(p.walkCycle * Math.PI * 2) * 5 : 0;
    // Squash-stretch: wider + shorter on landing, taller on airtime.
    const squash = p.landSquash;
    const scaleX = 1 + squash * 0.25;
    const scaleY = 1 - squash * 0.18;
    // Attack lunge: lean forward in facing direction during swing.
    const lungeX = p.attackAnim > 0 ? p.dir.x * (p.attackAnim / 0.25) * 6 : 0;
    const lungeY = p.attackAnim > 0 ? p.dir.y * (p.attackAnim / 0.25) * 6 : 0;
    // Iframe flash: blink by alternating alpha.
    const alpha = (p.iframes > 0 && Math.floor(p.iframes * 18) % 2 === 0) ? 0.35 : 1;

    const half = pSize / 2;
    // Top half: rows 0..49% of sprite height (head + torso).
    const topH = Math.floor(pSize * 0.52);
    // Bottom half: rows 50%..100% (legs + feet).
    const botH = pSize - topH;
    const srcTopH = Math.floor(spr.height * 0.52);
    const srcBotH = spr.height - srcTopH;

    ctx.save();
    ctx.globalAlpha = alpha;

    // --- Bottom half (legs) ---
    // Draw legs offset left/right and slightly squashed.
    ctx.save();
    ctx.translate(psx + lungeX + legOffset, psy + bobY + lungeY);
    if (p.dir.x < 0) ctx.scale(-1, 1);
    ctx.rotate(p.tiltAngle);
    ctx.scale(scaleX, scaleY);
    ctx.drawImage(
      spr,
      0, srcTopH, spr.width, srcBotH,       // source: bottom half
      -half, topH - half, pSize, botH        // dest: bottom portion
    );
    ctx.restore();

    // --- Top half (head + torso) ---
    // Floats up/down with bob, tilts with movement.
    ctx.save();
    ctx.translate(psx + lungeX, psy + bobY + lungeY - squash * 4);
    if (p.dir.x < 0) ctx.scale(-1, 1);
    ctx.rotate(p.tiltAngle * 0.6);
    ctx.scale(scaleX * 0.97, scaleY * 1.04);
    ctx.drawImage(
      spr,
      0, 0, spr.width, srcTopH,             // source: top half
      -half, -half, pSize, topH             // dest: top portion
    );
    ctx.restore();

    ctx.restore(); // globalAlpha
  }

  // Tiny facing pip — direction indicator always visible.
  ctx.save();
  ctx.fillStyle = "#ffd86b";
  ctx.globalAlpha = 0.85;
  ctx.beginPath();
  ctx.arc(psx + p.dir.x * 26, psy + p.dir.y * 26 + 4, 3.5, 0, Math.PI * 2);
  ctx.fill();
  ctx.restore();

  // Hammer swing visual: animate the hammer sprite sweeping through the arc.
  if (p.attackAnim > 0) {
    const hammerDef = p.weapons.find((w) => w.id === "hammer");
    if (hammerDef && sprites.fx_hammer) {
      const range = hammerDef.range * p.areaMult;
      const facing = Math.atan2(p.dir.y, p.dir.x);
      const t = 1 - p.attackAnim / 0.25;     // 0 -> 1 over the swing
      const arc = hammerDef.arc;
      const swingAngle = -arc / 2 + arc * t;
      ctx.save();
      ctx.translate(psx, psy);
      ctx.rotate(facing);
      // Slash trail behind the hammer head.
      ctx.globalAlpha = 0.45 * (1 - t * 0.7);
      ctx.strokeStyle = "#ffe070";
      ctx.lineWidth = 8;
      ctx.beginPath();
      ctx.arc(0, 0, range * 0.8, -arc / 2, swingAngle);
      ctx.stroke();
      // Draw the hammer sprite at the current swing position.
      ctx.globalAlpha = 1;
      ctx.rotate(swingAngle);
      ctx.translate(range * 0.7, 0);
      ctx.rotate(Math.PI / 2 + swingAngle * 0.3);
      const hsize = 56;
      ctx.drawImage(sprites.fx_hammer, -hsize / 2, -hsize / 2, hsize, hsize);
      ctx.restore();
    }
  }

  // Projectiles.
  for (const pr of state.projectiles) {
    drawSprite(sprites[pr.sprite] || sprites.fx_bolt, pr.x, pr.y, 24);
  }

  // Effects.
  for (const ef of state.effects) {
    const t = 1 - ef.life / ef.maxLife;
    if (ef.kind === "shockwave") {
      const r = (ef.data.radius || 100) * t;
      ctx.save();
      ctx.globalAlpha = 1 - t;
      ctx.strokeStyle = ef.data.color || "#7ad0ff";
      ctx.lineWidth = 6;
      ctx.beginPath();
      ctx.arc(ef.x - state.camera.x, ef.y - state.camera.y, r, 0, Math.PI * 2);
      ctx.stroke();
      ctx.restore();
    } else if (ef.kind === "lightning") {
      drawSprite(sprites.fx_lightning, ef.x, ef.y - 10 + t * 20, 56);
    } else if (ef.kind === "swing") {
      // Already drawn via attackAnim above.
    }
  }

  // Damage numbers.
  for (const dn of state.damageNumbers) {
    const a = clamp(dn.life / 0.8, 0, 1);
    ctx.save();
    ctx.globalAlpha = a;
    ctx.fillStyle = "#fff";
    ctx.strokeStyle = "#000";
    ctx.lineWidth = 3;
    ctx.font = "bold 18px Courier New";
    ctx.textAlign = "center";
    const tx = dn.x - state.camera.x;
    const ty = dn.y - state.camera.y;
    ctx.strokeText(dn.val, tx, ty);
    ctx.fillText(dn.val, tx, ty);
    ctx.restore();
  }
}

// ---------- Game lifecycle ----------

function startRun() {
  state.running = true;
  state.paused = false;
  state.ended = false;
  state.time = 0;
  state.kills = 0;
  state.gold = 0;
  state.enemies = [];
  state.projectiles = [];
  state.pickups = [];
  state.effects = [];
  state.damageNumbers = [];
  state.upgradePending = 0;
  state.bossSpawned = false;
  state.bossDead = false;
  spawnAccum = 0;
  for (const k in passiveLevels) delete passiveLevels[k];
  state.player = makePlayer();
  givePlayerWeapon(state.player, "hammer");
  applyShopBonuses(state.player);
  showScreen(null);
  document.getElementById("hud").classList.remove("hidden");
  updateHUD();
}

function endRun(won) {
  state.ended = true;
  state.running = false;
  // Bank gold into meta. Victories advance the run number.
  meta.gold += state.gold;
  if (won) {
    meta.runNumber = (meta.runNumber || 0) + 1;
  }
  saveMeta();
  const title = document.getElementById("end-title");
  const stats = document.getElementById("end-stats");
  title.textContent = won ? "VICTORY!" : "YOU DIED";
  title.style.color = won ? "#7aff8a" : "#ff6b6b";
  const mm = Math.floor(state.time / 60).toString().padStart(2, "0");
  const ss = Math.floor(state.time % 60).toString().padStart(2, "0");
  stats.innerHTML = `
    <div>Time survived: <b>${mm}:${ss}</b></div>
    <div>Kills: <b>${state.kills}</b></div>
    <div>Level reached: <b>${state.player.level}</b></div>
    <div>Gold earned: <b>+${state.gold}</b> ◈</div>
    <div>Total gold: <b>${meta.gold}</b> ◈</div>
  `;
  document.getElementById("hud").classList.add("hidden");
  showScreen("end-screen");
}

function loop(now) {
  const dt = Math.min(0.05, (now - lastTime) / 1000);
  lastTime = now;
  update(dt);
  if (state.running || state.ended) draw();
  requestAnimationFrame(loop);
}

// ---------- Screen management ----------

function showScreen(id) {
  const all = ["home-screen", "shop-screen", "end-screen", "pause-screen"];
  for (const s of all) {
    document.getElementById(s).classList.toggle("hidden", s !== id);
  }
}

function showHome() {
  state.running = false;
  document.getElementById("hud").classList.add("hidden");
  renderHomepage();
  showScreen("home-screen");
}

// ---------- Homepage ----------

function renderHomepage() {
  document.getElementById("home-gold").textContent = meta.gold;
  const runEl = document.getElementById("home-run-number");
  if (runEl) {
    const n = meta.runNumber || 0;
    runEl.textContent = n === 0 ? "Run 1 — Good luck!" : `Run ${n + 1} — ${n} completion${n > 1 ? "s" : ""}`;
  }
  // Show active shop bonuses.
  const bonusEl = document.getElementById("meta-bonuses");
  const lines = [];
  for (const upg of SHOP_UPGRADES) {
    const lv = meta.shop[upg.id] || 0;
    if (lv > 0) lines.push(`▸ ${upg.name} Lv${lv}`);
  }
  bonusEl.innerHTML = lines.length
    ? "<b>Active bonuses:</b><br>" + lines.join("<br>")
    : "";
  // Draw animated preview on the small canvas.
  startPreviewAnim();
}

let previewAnimId = null;
let previewT = 0;

function startPreviewAnim() {
  if (previewAnimId) cancelAnimationFrame(previewAnimId);
  previewT = 0;
  const pc = document.getElementById("preview-canvas");
  const pctx = pc.getContext("2d");
  pctx.imageSmoothingEnabled = false;

  function frame() {
    previewAnimId = requestAnimationFrame(frame);
    previewT += 0.016;
    pctx.clearRect(0, 0, pc.width, pc.height);
    // Grass background tiles.
    const tile = sprites.tile_grass;
    if (tile) {
      for (let y = 0; y < pc.height; y += 128)
        for (let x = 0; x < pc.width; x += 128)
          pctx.drawImage(tile, x, y, 128, 128);
    }
    // Animate a few enemies walking in a circle for the preview.
    const cx = pc.width / 2, cy = pc.height / 2 + 30;
    const enemyTypes = ["enemy_goblin", "enemy_bat", "enemy_slime", "enemy_bomber", "enemy_mage"];
    for (let i = 0; i < enemyTypes.length; i++) {
      const ang = (i / enemyTypes.length) * Math.PI * 2 + previewT * 0.6;
      const r = 110;
      const ex = cx + Math.cos(ang) * r;
      const ey = cy + Math.sin(ang) * r * 0.5;
      const spr = sprites[enemyTypes[i]];
      if (spr) {
        const bob = Math.sin(previewT * 6 + i) * 3;
        const sz = 44;
        pctx.save();
        if (Math.cos(ang) < 0) pctx.scale(-1, 1);
        pctx.drawImage(spr, (Math.cos(ang) < 0 ? -ex : ex) - sz / 2, ey + bob - sz / 2, sz, sz);
        pctx.restore();
      }
    }
    // Player in center with bob and breathing.
    const spr = sprites.player;
    if (spr) {
      const breathe = Math.sin(previewT * 1.4) * 1.5;
      const bob = Math.sin(previewT * 3) * 2;
      const sz = 80;
      pctx.drawImage(spr, cx - sz / 2, cy - sz / 2 + breathe + bob - 30, sz, sz);
    }
    // Title text overlay.
    pctx.save();
    pctx.fillStyle = "rgba(10,6,18,0.45)";
    pctx.fillRect(0, 0, pc.width, 60);
    pctx.fillStyle = "#ffd86b";
    pctx.font = "bold 18px 'Courier New', monospace";
    pctx.textAlign = "center";
    pctx.textBaseline = "middle";
    pctx.fillText("SURVIVE 15 MINUTES", pc.width / 2, 30);
    pctx.restore();
  }
  frame();
}

function stopPreviewAnim() {
  if (previewAnimId) { cancelAnimationFrame(previewAnimId); previewAnimId = null; }
}

// ---------- Shop ----------

function renderShop() {
  document.getElementById("shop-gold-display").textContent = meta.gold;
  const container = document.getElementById("shop-items");
  container.innerHTML = "";

  const TIER_LABELS = ["", "Tier I", "Tier II", "Tier III"];
  const TIER_UNLOCK = [0, 0, 1, 2]; // runs needed to unlock each tier

  let currentTier = 0;
  for (const upg of SHOP_UPGRADES) {
    // Inject a tier header when we enter a new tier.
    if (upg.tier !== currentTier) {
      currentTier = upg.tier;
      const runsNeeded = TIER_UNLOCK[currentTier];
      const unlocked = meta.runNumber >= runsNeeded;
      const header = document.createElement("div");
      header.className = "shop-tier-header" + (unlocked ? "" : " locked");
      header.innerHTML = unlocked
        ? `<span>${TIER_LABELS[currentTier]}</span>`
        : `<span>${TIER_LABELS[currentTier]} — Complete run ${runsNeeded} to unlock</span>`;
      container.appendChild(header);
    }

    const runsNeeded = TIER_UNLOCK[upg.tier];
    const tierUnlocked = meta.runNumber >= runsNeeded;
    const owned = meta.shop[upg.id] || 0;
    const maxed = owned >= upg.maxLevel;
    const cost = maxed ? 0 : shopUpgradeCost(upg);
    const canAfford = meta.gold >= cost;
    const iconCanvas = sprites[upg.icon];
    const iconUrl = iconCanvas?.dataUrl ?? `sprites/${upg.icon}.png`;

    const el = document.createElement("div");
    if (!tierUnlocked) {
      el.className = "shop-item tier-locked";
      el.innerHTML = `
        <div class="shop-item-icon" style="background-image:url('${iconUrl}'); filter:grayscale(1) opacity(0.4)"></div>
        <div class="shop-item-name" style="opacity:0.4">${upg.name}</div>
        <div class="shop-item-desc" style="opacity:0.3">${upg.desc}</div>
        <div class="shop-item-cost" style="opacity:0.4">🔒 Locked</div>
      `;
    } else {
      el.className = "shop-item" + (maxed ? " maxed" : !canAfford ? " cant-afford" : "");
      el.innerHTML = `
        ${maxed ? '<div class="shop-item-badge">MAX</div>' : ""}
        <div class="shop-item-icon" style="background-image:url('${iconUrl}')"></div>
        <div class="shop-item-name">${upg.name}</div>
        <div class="shop-item-desc">${upg.desc}</div>
        <div class="shop-item-level">${owned > 0 ? `Lv ${owned} / ${upg.maxLevel}` : `Max Lv ${upg.maxLevel}`}</div>
        <div class="shop-item-cost">
          <span class="gold-coin">◈</span>
          <span>${maxed ? "MAXED" : cost}</span>
        </div>
      `;
      if (!maxed && canAfford) {
        el.onclick = () => buyShopItem(upg);
      }
    }
    container.appendChild(el);
  }
}

function buyShopItem(upg) {
  const owned = meta.shop[upg.id] || 0;
  if (owned >= upg.maxLevel) return;
  const cost = shopUpgradeCost(upg);
  if (meta.gold < cost) return;
  meta.gold -= cost;
  meta.shop[upg.id] = owned + 1;
  saveMeta();
  renderShop();
  renderHomepage();
}

// ---------- Boot ----------

async function boot() {
  const loadingMsg = document.getElementById("loading-msg");
  const startBtn = document.getElementById("start-btn");
  startBtn.disabled = true;

  await loadAllSprites((done, total) => {
    loadingMsg.textContent = `Loading sprites... ${done}/${total}`;
  });
  loadingMsg.classList.add("hidden");

  // Wire buttons.
  startBtn.disabled = false;
  startBtn.textContent = "START RUN";
  startBtn.onclick = () => { stopPreviewAnim(); startRun(); };

  document.getElementById("shop-btn").onclick = () => {
    showScreen("shop-screen");
    renderShop();
  };
  document.getElementById("shop-close-btn").onclick = () => {
    showScreen("home-screen");
    renderHomepage();
  };
  document.getElementById("restart-btn").onclick = () => { stopPreviewAnim(); startRun(); };
  document.getElementById("home-btn").onclick = showHome;
  document.getElementById("pause-home-btn").onclick = () => {
    state.paused = false;
    showHome();
  };

  // Show homepage.
  showHome();

  // Start game loop (runs in background, only draws when in-game).
  state.player = makePlayer();
  state.camera.x = -W / 2;
  state.camera.y = -H / 2;
  requestAnimationFrame((t) => { lastTime = t; loop(t); });
}

boot();
