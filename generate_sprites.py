import base64
import os
import sys
from pathlib import Path

from openai import OpenAI

ROOT = Path(__file__).parent
SPRITE_DIR = ROOT / "sprites"
SPRITE_DIR.mkdir(exist_ok=True)

def load_key() -> str:
    env = ROOT / ".env"
    for line in env.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        if k.strip() == "OpenAIKey":
            return v.strip().strip('"').strip("'")
    raise SystemExit("OpenAIKey not found in .env")

STYLE = (
    "16-bit pixel art sprite, clean crisp pixels, vibrant saturated colors, "
    "bold dark outline, centered subject, solid flat magenta #ff00ff background, "
    "no shadow, no text, no border, single isolated sprite, top-down view"
)

BOSS_STYLE = (
    "16-bit pixel art boss sprite, large imposing creature, clean crisp pixels, "
    "vibrant saturated colors, bold dark outline, centered, solid flat magenta #ff00ff background, "
    "no text, no border, front view"
)

TILE_STYLE = (
    "16-bit pixel art seamless tileable ground texture, top-down view, "
    "clean crisp pixels, fills entire image edge to edge, no border, no text, no objects"
)

UI_STYLE = (
    "16-bit pixel art game UI icon, clean crisp pixels, vibrant colors, bold outline, "
    "centered, solid flat magenta #ff00ff background, no text"
)

REGEN_TILES = {
    "tile_grass": (
        "16-bit pixel art seamless top-down ground texture of a lush grass field. "
        "Solid uniform green grass covering the ENTIRE image edge to edge with NO empty spaces, "
        "NO dark areas, NO vignette, NO border, NO fade, NO black background. "
        "Dense grass blades, small clovers, tiny flowers, and dirt patches scattered evenly. "
        "Must look like a single tile cut from a larger uniform grass field. Top-down view. "
        "Crisp pixel art, vibrant green colors. No text, no objects, no characters."
    ),
}

SHEETS = {
    "player_sheet": (
        "Pixel art character sprite sheet on a SOLID FLAT MAGENTA #ff00ff background. "
        "A 2x2 grid showing the EXACT SAME warrior hero character in 4 different poses. "
        "The character is a chibi pixel art hero with orange spiky hair, blue tunic, brown belt, "
        "brown boots, holding a large two-handed wooden war hammer with iron head. "
        "Top-left cell: standing idle facing camera, hammer held down at side. "
        "Top-right cell: walking forward, left foot raised, slight body lean. "
        "Bottom-left cell: walking forward, right foot raised, slight body lean other way. "
        "Bottom-right cell: mid swing attack, hammer raised overhead, action pose. "
        "All four poses must use IDENTICAL colors, identical proportions, identical character design, "
        "identical size, each centered in its quadrant. Clean crisp 16-bit pixel art, bold dark outlines, "
        "vibrant saturated colors. Solid magenta background fills all empty space. No text, no labels, no borders between cells."
    ),
}

SPRITES = {
    # Player
    "player": f"{STYLE}. A brave hero warrior with a big hammer, blue tunic, determined face, chibi proportions",
    # Enemies
    "enemy_goblin": f"{STYLE}. A small green goblin monster with pointy ears, angry face, tiny club",
    "enemy_bat": f"{STYLE}. A purple flying bat with spread wings, glowing red eyes, fangs",
    "enemy_knight": f"{STYLE}. A heavy armored skeleton knight with gray plate armor and a rusty sword",
    "enemy_mage": f"{STYLE}. An evil dark mage in a purple robe and hood holding a glowing staff",
    "enemy_charger": f"{STYLE}. A red angry minotaur bull monster with big horns, muscular, charging pose",
    "enemy_slime": f"{STYLE}. A green gooey slime blob monster with cute eyes and a wide smile",
    "enemy_bomber": f"{STYLE}. A round black bomb creature with a lit fuse on top, angry face, tiny legs",
    "enemy_boss": f"{BOSS_STYLE}. A colossal demon overlord with massive horns, glowing red eyes, huge claws, dark armor, menacing",
    # Weapon effects
    "fx_hammer": f"{STYLE}. A large wooden war hammer with iron head, weapon icon, diagonal",
    "fx_orb": f"{STYLE}. A glowing blue magical energy orb with sparkles",
    "fx_bolt": f"{STYLE}. A glowing yellow magical arrow bolt projectile with motion trail",
    "fx_lightning": f"{STYLE}. A jagged bright blue-white lightning bolt zap effect",
    "fx_shockwave": f"{STYLE}. A cyan circular shockwave ring energy pulse effect",
    "fx_aura": f"{STYLE}. A swirling red flame aura circle effect",
    # Pickups
    "pickup_gem_small": f"{STYLE}. A small cyan crystal XP gem, faceted diamond shape, glowing",
    "pickup_gem_large": f"{STYLE}. A large purple crystal XP gem, faceted diamond shape, glowing bright",
    "pickup_heart": f"{STYLE}. A bright red health heart pickup, shiny, glowing",
    # Tiles
    "tile_grass": f"{TILE_STYLE}. Lush green grass field with small flowers and tufts",
    "tile_crypt": f"{TILE_STYLE}. Dark gray cracked stone dungeon floor with moss",
    "tile_lava": f"{TILE_STYLE}. Black volcanic rock floor with glowing orange lava cracks",
    "tile_ice": f"{TILE_STYLE}. Pale blue frozen ice floor with snow patches",
    # Props
    "prop_rock": f"{STYLE}. A gray mossy boulder rock obstacle",
    "prop_tree": f"{STYLE}. A small green pine tree with brown trunk, top-down view",
    "prop_pillar": f"{STYLE}. A broken stone dungeon pillar, cracked",
    "prop_shard": f"{STYLE}. A tall pale blue ice crystal shard sticking up",
    # UI
    "ui_heart": f"{UI_STYLE}. A red heart icon for health bar",
    "ui_frame": f"{UI_STYLE}. An ornate golden square upgrade card frame, empty center",
    "ui_badge": f"{UI_STYLE}. A yellow star level-up badge icon",
    "ui_banner": f"{UI_STYLE}. A red scroll banner ribbon, empty, ornate",
}

def generate(client: OpenAI, name: str, prompt: str) -> None:
    out = SPRITE_DIR / f"{name}.png"
    if out.exists():
        print(f"[skip] {name}")
        return
    print(f"[gen ] {name}...", flush=True)
    resp = client.images.generate(
        model="gpt-image-1-mini",
        prompt=prompt,
        size="1024x1024",
        quality="low",
        n=1,
    )
    b64 = resp.data[0].b64_json
    out.write_bytes(base64.b64decode(b64))
    print(f"[ok  ] {name}")

def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    client = OpenAI(api_key=load_key())
    if mode == "test":
        name = "player"
        generate(client, name, SPRITES[name])
        return
    if mode == "regen-tiles":
        for name, prompt in REGEN_TILES.items():
            (SPRITE_DIR / f"{name}.png").unlink(missing_ok=True)
            generate(client, name, prompt)
        return
    if mode == "sheets":
        for name, prompt in SHEETS.items():
            (SPRITE_DIR / f"{name}.png").unlink(missing_ok=True)
            generate(client, name, prompt)
        return
    for name, prompt in SPRITES.items():
        generate(client, name, prompt)
    print(f"done. {len(SPRITES)} sprites in {SPRITE_DIR}")

if __name__ == "__main__":
    main()
