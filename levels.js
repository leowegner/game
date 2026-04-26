// 50-level progression with enemies and shop tiers
// Each level has enemy definitions and shopTier gating

const LEVELS = {
  1: {
    shopTier: 1,
    difficulty: 2,
    enemies: [
      { name: "Goblin Rusher", type: "melee", hp: 15, speed: 2.5, damage: 3, description: "Fast melee attacker. Weak to crowd control." },
      { name: "Bone Archer", type: "ranged", hp: 12, speed: 1.2, damage: 2, description: "Skeleton archer. Projectiles travel slowly." }
    ]
  },
  2: {
    shopTier: 1,
    difficulty: 4,
    enemies: [
      { name: "Armored Sentinel", type: "tank", hp: 40, speed: 0.8, damage: 4, description: "Heavily armored knight. High health, reduced knockback." },
      { name: "Fire Cultist", type: "caster", hp: 18, speed: 1.5, damage: 3, description: "Mage casting AoE fire. Vulnerable while casting." }
    ]
  },
  3: {
    shopTier: 1,
    difficulty: 6,
    enemies: [
      { name: "Skeletal Knight", type: "melee", hp: 45, speed: 2.0, damage: 12, description: "Heavy undead warrior. Charges every 2 seconds." },
      { name: "Death Caster", type: "caster", hp: 25, speed: 1.5, damage: 8, description: "Ranged magic user. Slows enemies on hit." }
    ]
  },
  4: {
    shopTier: 1,
    difficulty: 7,
    enemies: [
      { name: "Flame Wraith", type: "swarm", hp: 18, speed: 3.5, damage: 6, description: "Fast fire spirit. Spawns in packs. Leaves burning ground." },
      { name: "Magma Golem", type: "tank", hp: 80, speed: 1.2, damage: 15, description: "Heavy lava tank. Releases lava pools. Takes 30% less ranged damage." }
    ]
  },
  5: {
    shopTier: 1,
    difficulty: 6,
    enemies: [
      { name: "Inferno Knight", type: "melee", hp: 120, speed: 4.5, damage: 18, description: "Fast rusher that ignites enemies on hit with DoT." },
      { name: "Blizzard Mage", type: "caster", hp: 60, speed: 2.0, damage: 22, description: "Ice shards in spread pattern. Slows enemies 40% for 2s." }
    ]
  },
  6: {
    shopTier: 1,
    difficulty: 7,
    enemies: [
      { name: "Void Warden", type: "tank", hp: 200, speed: 2.5, damage: 16, description: "Cosmic barrier tank. Absorbs 30% damage, reflects 10% back." },
      { name: "Spectral Lancer", type: "ranged", hp: 70, speed: 3.5, damage: 20, description: "Ghost warrior. Throws ethereal spears. Brief invulnerability at low HP." }
    ]
  },
  7: {
    shopTier: 1,
    difficulty: 6,
    enemies: [
      { name: "Void Wraith", type: "caster", hp: 45, speed: 2.5, damage: 12, description: "Teleporting caster. Creates void zones." },
      { name: "Crystalline Sentinel", type: "tank", hp: 120, speed: 1.2, damage: 8, description: "Reflective armor tank. Punishes careless attacks." }
    ]
  },
  8: {
    shopTier: 1,
    difficulty: 8,
    enemies: [
      { name: "Plague Swarm", type: "swarm", hp: 8, speed: 3.5, damage: 3, description: "Fast cluster dealing poison. Deaths release miasma clouds." },
      { name: "Corrupted Arbiter", type: "boss", hp: 200, speed: 2.0, damage: 15, description: "Two-phase fight: minion summoning then berserk with area damage." }
    ]
  },
  9: {
    shopTier: 1,
    difficulty: 8,
    enemies: [
      { name: "Void Sentinel", type: "tank", hp: 450, speed: 0.8, damage: 35, description: "Heavy construct. Absorbs 40% damage, regenerates 5 HP/s while still." },
      { name: "Chaos Caster", type: "caster", hp: 280, speed: 1.2, damage: 50, description: "Explosive orbs in patterns. AoE impact with damaging zones." }
    ]
  },
  10: {
    shopTier: 1,
    difficulty: 9,
    enemies: [
      { name: "Rift Summoner", type: "boss", hp: 600, speed: 1.0, damage: 45, description: "Boss caster. Opens rifts summoning 3-5 minions. Can teleport." },
      { name: "Temporal Devourer", type: "swarm", hp: 150, speed: 2.2, damage: 25, description: "Fast horde spawning in 4-6. Explodes on death with knockback." }
    ]
  },
  11: {
    shopTier: 2,
    difficulty: 9,
    enemies: [
      { name: "Spectre", type: "ranged", hp: 35, speed: 110, damage: 12, description: "Phases in/out every 1.5s. Takes 50% reduced damage while phased." },
      { name: "Dullahan", type: "tank", hp: 120, speed: 65, damage: 22, description: "High armor (30-50% reduction). Ground slam AoE every 3s with knockback." }
    ]
  },
  12: {
    shopTier: 2,
    difficulty: 10,
    enemies: [
      { name: "Flame Wraith", type: "caster", hp: 45, speed: 100, damage: 16, description: "Fires 3 fireballs every 2s creating persistent damage zones." },
      { name: "Soul Devourer", type: "support", hp: 95, speed: 75, damage: 20, description: "Buffs nearby enemies. Drains player mana on contact." }
    ]
  },
  13: {
    shopTier: 2,
    difficulty: 10,
    enemies: [
      { name: "Wraith", type: "phantom", hp: 32, speed: 110, damage: 11, description: "Phases in/out every 3s. Becomes invisible with damaging aura." },
      { name: "Frostbound Guardian", type: "tank", hp: 95, speed: 40, damage: 14, description: "Freezes survivors for 1.5s. Slows nearby enemies 30%." }
    ]
  },
  14: {
    shopTier: 2,
    difficulty: 11,
    enemies: [
      { name: "Void Seeker", type: "ranged", hp: 50, speed: 100, damage: 18, description: "Fires 3-way dark projectiles. Leaves persistent void zones." },
      { name: "Umbral Parasite", type: "swarm", hp: 22, speed: 120, damage: 8, description: "Drains 5% current HP per hit. Spawns 2 copies when damaged." }
    ]
  },
  15: {
    shopTier: 2,
    difficulty: 10,
    enemies: [
      { name: "Infernal Wraith", type: "caster", hp: 65, speed: 90, damage: 20, description: "Phases between attacks. Casts homing fire projectiles ignoring armor." },
      { name: "Magma Titan", type: "tank", hp: 140, speed: 35, damage: 22, description: "Colossal molten creature. Lava pools with projectile reflection." }
    ]
  },
  16: {
    shopTier: 2,
    difficulty: 11,
    enemies: [
      { name: "Dimensional Rift", type: "caster", hp: 75, speed: 85, damage: 24, description: "Creates wormholes. Fires splitting projectiles with reality damage." },
      { name: "Void Leviathan", type: "charger", hp: 160, speed: 70, damage: 26, description: "Massive tentacled entity. Gravitational pull, applies stat debuffs." }
    ]
  },
  17: {
    shopTier: 2,
    difficulty: 11,
    enemies: [
      { name: "Wraith", type: "ranged", hp: 45, speed: 110, damage: 11, description: "Spectral unit with pierce projectiles ignoring obstacles." },
      { name: "Thornvine", type: "tank", hp: 85, speed: 35, damage: 12, description: "Stationary plant with self-healing and radius damage aura." }
    ]
  },
  18: {
    shopTier: 2,
    difficulty: 12,
    enemies: [
      { name: "Golem", type: "tank", hp: 180, speed: 40, damage: 16, description: "Massive stone tank with earthquake charge attacks." },
      { name: "Harpy", type: "support", hp: 35, speed: 130, damage: 13, description: "Aerial buffer that enhances nearby enemies and spawns minions." }
    ]
  },
  19: {
    shopTier: 3,
    difficulty: 11,
    enemies: [
      { name: "Spectral Wraith", type: "specter", hp: 50, speed: 105, damage: 14, description: "Phasing mechanic with armor-piercing damage." },
      { name: "Void Sentinel", type: "void_guardian", hp: 130, speed: 60, damage: 18, description: "Projectile reflection and damaging aura." }
    ]
  },
  20: {
    shopTier: 3,
    difficulty: 12,
    enemies: [
      { name: "Rift Summoner", type: "summoner", hp: 140, speed: 55, damage: 20, description: "Spawns void minions through dimensional rifts." },
      { name: "Calamity Elemental", type: "calamity", hp: 180, speed: 45, damage: 28, description: "Explosive splash damage and hazard field creation." }
    ]
  },
  21: {
    shopTier: 3,
    difficulty: 12,
    enemies: [
      { name: "Spectral Wraith", type: "ranged", hp: 35, speed: 110, damage: 12, description: "Phases through obstacles. Attacks from distance." },
      { name: "Crystal Sentinel", type: "tank", hp: 120, speed: 40, damage: 16, description: "Heavily armored. Reflects damage back. Gains strength when damaged." }
    ]
  },
  22: {
    shopTier: 3,
    difficulty: 13,
    enemies: [
      { name: "Temporal Anomaly", type: "caster", hp: 45, speed: 95, damage: 14, description: "Warps space-time with unpredictable attacks and teleportation." },
      { name: "Void Swarm Cluster", type: "swarm", hp: 25, speed: 130, damage: 8, description: "Fast-moving swarm. Multiplies when grouped." }
    ]
  },
  23: {
    shopTier: 3,
    difficulty: 12,
    enemies: [
      { name: "Wraith", type: "ranged", hp: 35, speed: 120, damage: 12, description: "Spectral attacker with high speed. Phases through obstacles." },
      { name: "Spiked Crusher", type: "tank", hp: 140, speed: 35, damage: 22, description: "Massive tank with reflective spikes. Reflects 20% melee damage." }
    ]
  },
  24: {
    shopTier: 3,
    difficulty: 13,
    enemies: [
      { name: "Void Crawler", type: "swarm", hp: 55, speed: 65, damage: 16, description: "Tentacled aberration. Summons 2-3 void tentacles on attack." },
      { name: "Plague Spreader", type: "ranged", hp: 45, speed: 75, damage: 14, description: "Infectious caster. Applies lingering damage aura (3 ticks, -2 hp/s)." }
    ]
  },
  25: {
    shopTier: 3,
    difficulty: 13,
    enemies: [
      { name: "Spectral Wraith", type: "ethereal", hp: 45, speed: 120, damage: 16, description: "Phases through obstacles. Leaves slowing orbs." },
      { name: "Crystalline Golem", type: "tank", hp: 140, speed: 40, damage: 22, description: "High armor. Shatters into projectiles on death." }
    ]
  },
  26: {
    shopTier: 3,
    difficulty: 14,
    enemies: [
      { name: "Plague Swarm", type: "swarm", hp: 8, speed: 160, damage: 4, description: "Spawns in groups. Creates poison clouds with DoT." },
      { name: "Abyssal Sentinel", type: "caster", hp: 95, speed: 75, damage: 28, description: "Summons shadow minions. Casts void projectiles." }
    ]
  },
  27: {
    shopTier: 4,
    difficulty: 13,
    enemies: [
      { name: "Wraith", type: "ranged", hp: 60, speed: 100, damage: 16, description: "Teleports every 4s. Fires projectiles." },
      { name: "Void Tentacle", type: "tank", hp: 95, speed: 45, damage: 20, description: "Ground slam every 6s creating void zones." }
    ]
  },
  28: {
    shopTier: 4,
    difficulty: 14,
    enemies: [
      { name: "Infernal Revenant", type: "flyer", hp: 110, speed: 110, damage: 24, description: "Gains stacking buffs from kills. Leaves burn trails." },
      { name: "Crystalline Swarm Queen", type: "caster", hp: 85, speed: 80, damage: 18, description: "Spawns 2 drones every 5 seconds." }
    ]
  },
  29: {
    shopTier: 4,
    difficulty: 14,
    enemies: [
      { name: "Plague Swarm", type: "swarm", hp: 35, speed: 110, damage: 9, description: "Splits into smaller units when damaged. High mobility." },
      { name: "Void Sentinel", type: "tank", hp: 120, speed: 65, damage: 22, description: "Protective void field reducing ranged damage. Casts void orbs." }
    ]
  },
  30: {
    shopTier: 4,
    difficulty: 15,
    enemies: [
      { name: "Chrono Reaver", type: "melee", hp: 95, speed: 75, damage: 26, description: "Blinks between targets with evasion. Leaves temporal trails." },
      { name: "Binding Tentacle Mass", type: "boss", hp: 140, speed: 45, damage: 12, description: "Multiple tentacles bind/slow players. Heals other enemies." }
    ]
  },
  31: {
    shopTier: 4,
    difficulty: 14,
    enemies: [
      { name: "Temporal Disruptor", type: "caster", hp: 70, speed: 80, damage: 20, description: "Freezes time in zones. Applies stacking slow debuffs." },
      { name: "Void Leech", type: "support", hp: 85, speed: 70, damage: 16, description: "Drains health from allies to self-heal and boost damage." }
    ]
  },
  32: {
    shopTier: 4,
    difficulty: 15,
    enemies: [
      { name: "Infernal Colossus", type: "boss", hp: 300, speed: 50, damage: 32, description: "Extreme armor (6). Leaves burning ground DoT." },
      { name: "Ethereal Specter", type: "swarm", hp: 60, speed: 155, damage: 18, description: "Becomes invulnerable during dash. Spawns in groups." }
    ]
  },
  33: {
    shopTier: 5,
    difficulty: 15,
    enemies: [
      { name: "Temporal Echo", type: "caster", hp: 65, speed: 95, damage: 22, description: "Spawns ghost clones dealing 50% damage." },
      { name: "Gravity Well", type: "tank", hp: 180, speed: 40, damage: 18, description: "Attracts enemies and projectiles with pull mechanic." }
    ]
  },
  34: {
    shopTier: 5,
    difficulty: 16,
    enemies: [
      { name: "Infernal Warden", type: "tank", hp: 150, speed: 50, damage: 26, description: "Leaves burning damage trails. Creates persistent fire zones." },
      { name: "Void Ripper", type: "swarm", hp: 55, speed: 130, damage: 20, description: "Swift void predator spawning rift fragments." }
    ]
  },
  35: {
    shopTier: 5,
    difficulty: 15,
    enemies: [
      { name: "Ethereal Lich King", type: "boss", hp: 180, speed: 50, damage: 35, description: "Phases between realms. Casts death curses with armor penetration." },
      { name: "Temporal Nexus Weaver", type: "caster", hp: 65, speed: 95, damage: 24, description: "Creates temporal rifts. Spawns 2-3 time anomalies every 7s." }
    ]
  },
  36: {
    shopTier: 5,
    difficulty: 16,
    enemies: [
      { name: "Void Leviathan", type: "boss", hp: 200, speed: 45, damage: 40, description: "Tentacle attacks with large AoE. Gains +2% damage per 5 seconds." },
      { name: "Stellar Sentinel Swarm", type: "swarm", hp: 20, speed: 140, damage: 8, description: "Fast stars spawning in groups. Reflects projectiles at high speed." }
    ]
  },
  37: {
    shopTier: 5,
    difficulty: 16,
    enemies: [
      { name: "Chrono Weaver", type: "caster", hp: 75, speed: 85, damage: 26, description: "Creates temporal rifts with crowd control slowdown." },
      { name: "Verdant Guardian", type: "tank", hp: 160, speed: 45, damage: 24, description: "Nature-themed heavy tank with self-healing and root." }
    ]
  },
  38: {
    shopTier: 5,
    difficulty: 17,
    enemies: [
      { name: "Nexus Architect", type: "caster", hp: 90, speed: 70, damage: 22, description: "Spawns explosive pylons for area control." },
      { name: "Void Devourer", type: "boss", hp: 220, speed: 60, damage: 32, description: "Consumes nearby enemies to heal and grow stronger." }
    ]
  },
  39: {
    shopTier: 5,
    difficulty: 16,
    enemies: [
      { name: "Chrono Wraith", type: "phantom", hp: 85, speed: 95, damage: 28, description: "Rewinds 2 seconds when taking major damage." },
      { name: "Molten Tyrant", type: "boss", hp: 250, speed: 50, damage: 30, description: "Leaves persistent trails. Gains scaling damage. Erupts with AoE every 6s." }
    ]
  },
  40: {
    shopTier: 5,
    difficulty: 17,
    enemies: [
      { name: "Entropy Swarm", type: "swarm", hp: 25, speed: 120, damage: 12, description: "Multiplies exponentially on death (spawns 2 per death)." },
      { name: "Apex Reaver", type: "boss", hp: 280, speed: 100, damage: 36, description: "Adaptive damage reduction up to 50%. Dash attacks every 5s." }
    ]
  },
  41: {
    shopTier: 6,
    difficulty: 17,
    enemies: [
      { name: "Void Wraith", type: "caster", hp: 80, speed: 100, damage: 26, description: "Teleports every 3s. Fires void projectiles. +20% damage while phased." },
      { name: "Crystalline Colossus", type: "tank", hp: 260, speed: 50, damage: 28, description: "Bounces 40% projectile damage back. Gains +15% armor per hit (stacks 10x)." }
    ]
  },
  42: {
    shopTier: 6,
    difficulty: 18,
    enemies: [
      { name: "Abyssal Leviathan", type: "boss", hp: 220, speed: 45, damage: 32, description: "Creates damaging whirlpools every 5s (120px radius). Takes 20% reduced ranged damage." },
      { name: "Starlight Sentinel", type: "support", hp: 95, speed: 70, damage: 24, description: "Marks players giving all enemies +25% damage. Stuns nearby enemies every 7s." }
    ]
  },
  43: {
    shopTier: 6,
    difficulty: 17,
    enemies: [
      { name: "Temporal Wraith", type: "caster", hp: 90, speed: 90, damage: 28, description: "Slows targets and creates temporal rifts." },
      { name: "Void Leviathan", type: "boss", hp: 180, speed: 60, damage: 28, description: "Life-draining tank that grows stronger over time." }
    ]
  },
  44: {
    shopTier: 6,
    difficulty: 18,
    enemies: [
      { name: "Ethereal Siphon", type: "caster", hp: 100, speed: 85, damage: 30, description: "Energy-draining enemy that weakens offensive capabilities of up to 3 targets." },
      { name: "Primordial Colossus", type: "boss", hp: 200, speed: 55, damage: 40, description: "40% damage reduction. Area stomp attacks." }
    ]
  },
  45: {
    shopTier: 6,
    difficulty: 18,
    enemies: [
      { name: "Void Singularity", type: "tank", hp: 180, speed: 60, damage: 26, description: "Gravitational vortex AoE mechanics." },
      { name: "Chrono Assassin", type: "caster", hp: 75, speed: 120, damage: 32, description: "Time-bending blinks and slow effects." }
    ]
  },
  46: {
    shopTier: 6,
    difficulty: 19,
    enemies: [
      { name: "Paradox Breaker", type: "caster", hp: 110, speed: 95, damage: 34, description: "Exponential splitting mechanic." },
      { name: "Abyss Reaper", type: "boss", hp: 300, speed: 75, damage: 40, description: "Boss-class melee with contextual damage scaling." }
    ]
  },
  47: {
    shopTier: 6,
    difficulty: 18,
    enemies: [
      { name: "Void Leech", type: "ranged", hp: 105, speed: 90, damage: 28, description: "Parasitic swarm with lifesteal mechanics." },
      { name: "Chrono Wraith", type: "caster", hp: 95, speed: 100, damage: 26, description: "Summons temporal clones with movement slows." }
    ]
  },
  48: {
    shopTier: 6,
    difficulty: 19,
    enemies: [
      { name: "Ascendant Sorcerer", type: "caster", hp: 130, speed: 95, damage: 36, description: "Progressive evolution with spell casting and homing projectiles." },
      { name: "Apex Predator", type: "melee", hp: 240, speed: 110, damage: 38, description: "True damage and momentum scaling with hunt mode burst." }
    ]
  },
  49: {
    shopTier: 6,
    difficulty: 19,
    enemies: [
      { name: "Chronos Weaver", type: "caster", hp: 120, speed: 90, damage: 34, description: "Reality-bending mage with time-slow aura and temporal anchors." },
      { name: "Void Leviathan", type: "boss", hp: 200, speed: 60, damage: 32, description: "Colossal tank spawning void rifts with pulling mechanics." }
    ]
  },
  50: {
    shopTier: 6,
    difficulty: 20,
    enemies: [
      { name: "The Architect", type: "boss", hp: 400, speed: 70, damage: 45, description: "Ultimate mega-boss with phase invulnerability and echo clones at 50%/25% HP." },
      { name: "Primordial Flame", type: "caster", hp: 180, speed: 80, damage: 38, description: "Inferno elemental with spreading burn zones and meteor attacks." }
    ]
  }
};

// Helper to get shop-gated levels by run progression
function getUnlockedLevels(runNumber) {
  // Mirror TIER_UNLOCK in script.js: [_, 0, 0, 1, 2, 3, 4, 5] — runs needed per tier.
  const TIER_UNLOCK = [0, 0, 0, 1, 2, 3, 4, 5];
  let maxTier = 1;
  for (let t = 1; t <= 6; t++) if (runNumber >= TIER_UNLOCK[t]) maxTier = t;
  return Object.entries(LEVELS)
    .filter(([, data]) => data.shopTier <= maxTier)
    .map(([k]) => parseInt(k));
}
