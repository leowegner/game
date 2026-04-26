#!/usr/bin/env python3
"""Generate the 1024x500 Play Store feature graphic.

Composition: dark gradient background (matches game), title text on left,
player + a few enemies on right, scattered XP gems for atmosphere.
"""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPR = os.path.join(ROOT, "sprites")
OUT = os.path.join(ROOT, "store", "feature-graphic.png")
W, H = 1024, 500


def key_magenta(img):
    img = img.convert("RGBA")
    px = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            mscore = (r + b) / 2 - g
            if mscore > 60 and r > 130 and b > 100 and g < 160:
                px[x, y] = (0, 0, 0, 0)
            elif mscore > 30 and r > 150 and b > 120 and g < 180:
                px[x, y] = (r, g, b, max(0, a - 180))
    return img


def gradient_bg():
    bg = Image.new("RGBA", (W, H), (10, 6, 18, 255))
    px = bg.load()
    cx, cy = W * 0.62, H * 0.5
    max_r = (W * 0.7)
    inner = (74, 36, 110)
    outer = (10, 6, 18)
    for y in range(H):
        for x in range(W):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            t = min(1.0, d / max_r)
            r = int(inner[0] * (1 - t) + outer[0] * t)
            g = int(inner[1] * (1 - t) + outer[1] * t)
            b = int(inner[2] * (1 - t) + outer[2] * t)
            px[x, y] = (r, g, b, 255)
    return bg


def find_font(size):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def paste_sprite(canvas, name, cx, cy, height, alpha=255, glow=False):
    s = key_magenta(Image.open(os.path.join(SPR, f"{name}.png")))
    aspect = s.width / s.height
    h = height
    w = int(h * aspect)
    s = s.resize((w, h), Image.NEAREST)
    if alpha != 255:
        a = s.split()[3].point(lambda v: int(v * alpha / 255))
        s.putalpha(a)
    x, y = int(cx - w / 2), int(cy - h / 2)
    if glow:
        halo = s.filter(ImageFilter.GaussianBlur(radius=10))
        warm = Image.new("RGBA", halo.size, (255, 180, 120, 0))
        halo = Image.composite(warm, halo, halo.split()[3].point(lambda v: 180 if v > 30 else 0))
        canvas.alpha_composite(halo, (x, y))
    canvas.alpha_composite(s, (x, y))


def main():
    canvas = gradient_bg()

    # Tile the grass on the bottom 25% as a faint footer band.
    tile = Image.open(os.path.join(SPR, "tile_grass.png")).convert("RGBA").resize((128, 128), Image.NEAREST)
    band_h = int(H * 0.28)
    for x in range(0, W, 128):
        for y in range(H - band_h, H, 128):
            canvas.alpha_composite(tile, (x, y))
    # Darken the band so text on top still pops.
    overlay = Image.new("RGBA", (W, band_h), (10, 6, 18, 140))
    canvas.alpha_composite(overlay, (0, H - band_h))

    # Right side: hero plus enemies as a little battle scene.
    paste_sprite(canvas, "enemy_bomber", 700, 300, 110, alpha=220)
    paste_sprite(canvas, "enemy_goblin", 870, 350, 130, alpha=230)
    paste_sprite(canvas, "enemy_bat", 940, 200, 90, alpha=220)
    paste_sprite(canvas, "enemy_mage", 620, 380, 130, alpha=230)
    paste_sprite(canvas, "player", 780, 280, 220, glow=True)
    # Scatter a few gems.
    paste_sprite(canvas, "pickup_gem_small", 600, 240, 36)
    paste_sprite(canvas, "pickup_gem_large", 980, 380, 44)
    paste_sprite(canvas, "pickup_heart", 660, 180, 36)

    # Title on the left.
    draw = ImageDraw.Draw(canvas)
    title_font = find_font(96)
    sub_font = find_font(36)
    # Soft text-shadow.
    title = "MEGA THONK"
    sub = "Pixel survivors. Tiny screen. Big damage."
    for dx, dy in [(-3, 0), (3, 0), (0, -3), (0, 3), (4, 4)]:
        draw.text((40 + dx, 130 + dy), title, font=title_font, fill=(0, 0, 0, 200))
    draw.text((40, 130), title, font=title_font, fill=(255, 220, 130, 255))
    for dx, dy in [(2, 2)]:
        draw.text((42 + dx, 250 + dy), sub, font=sub_font, fill=(0, 0, 0, 200))
    draw.text((42, 250), sub, font=sub_font, fill=(220, 200, 240, 255))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    canvas.convert("RGB").save(OUT, format="PNG")
    print("OK", OUT)


if __name__ == "__main__":
    main()
