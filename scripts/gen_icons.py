#!/usr/bin/env python3
"""Generate Android app icons + Play Store icon from sprites/player.png.

Mirrors the magenta-keying logic in script.js so the output looks like the
in-game sprite. Produces:
  - mipmap-*/ic_launcher.png and ic_launcher_round.png (legacy + adaptive bg)
  - mipmap-*/ic_launcher_foreground.png (adaptive foreground)
  - playstore-icon.png (512x512 for the Play Store listing)
"""
import os
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "sprites", "player.png")
RES = os.path.join(ROOT, "android", "app", "src", "main", "res")
OUT_PLAY = os.path.join(ROOT, "store", "playstore-icon.png")

# Density buckets and the launcher icon sizes Android expects per bucket.
DENSITIES = {
    "mdpi":    48,
    "hdpi":    72,
    "xhdpi":   96,
    "xxhdpi":  144,
    "xxxhdpi": 192,
}
# Adaptive icon foreground: 108dp at each density.
ADAPTIVE_FG = {
    "mdpi":    108,
    "hdpi":    162,
    "xhdpi":   216,
    "xxhdpi":  324,
    "xxxhdpi": 432,
}

BG_INNER = (52, 28, 84, 255)   # deep purple (matches game chrome)
BG_OUTER = (10, 6, 18, 255)    # near-black


def key_magenta(img):
    """Same magenta keying as script.js loadSprite()."""
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


def radial_bg(size):
    """Cheap radial gradient: inner -> outer."""
    bg = Image.new("RGBA", (size, size), BG_OUTER)
    cx = cy = size / 2
    max_r = (size / 2) * 1.05
    px = bg.load()
    for y in range(size):
        for x in range(size):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            t = min(1.0, d / max_r)
            r = int(BG_INNER[0] * (1 - t) + BG_OUTER[0] * t)
            g = int(BG_INNER[1] * (1 - t) + BG_OUTER[1] * t)
            b = int(BG_INNER[2] * (1 - t) + BG_OUTER[2] * t)
            px[x, y] = (r, g, b, 255)
    return bg


def compose(size, sprite, padding_ratio=0.18, glow=True):
    """Sprite over radial bg, with optional soft glow."""
    bg = radial_bg(size)
    pad = int(size * padding_ratio)
    target = size - pad * 2
    sized = sprite.resize((target, target), Image.NEAREST)
    if glow:
        # Soft glow halo behind the sprite.
        halo = sized.copy()
        halo = halo.filter(ImageFilter.GaussianBlur(radius=size * 0.04))
        # Tint halo warm.
        rgba = halo.split()
        warm = Image.new("RGBA", halo.size, (255, 180, 120, 0))
        halo = Image.composite(warm, halo, rgba[3].point(lambda v: 200 if v > 30 else 0))
        bg.alpha_composite(halo, (pad, pad))
    bg.alpha_composite(sized, (pad, pad))
    return bg


def compose_foreground(size, sprite):
    """Adaptive icon foreground: transparent bg, sprite centered in safe zone.

    Android crops adaptive icons; the visible region is the inner 66% of the
    foreground. We size the sprite to ~52% of the canvas so it sits comfortably
    inside any mask shape.
    """
    fg = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    target = int(size * 0.52)
    sized = sprite.resize((target, target), Image.NEAREST)
    off = (size - target) // 2
    fg.alpha_composite(sized, (off, off))
    return fg


def round_mask(size):
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size - 1, size - 1), fill=255)
    return mask


def main():
    sprite = key_magenta(Image.open(SRC))

    for bucket, sz in DENSITIES.items():
        out_dir = os.path.join(RES, f"mipmap-{bucket}")
        os.makedirs(out_dir, exist_ok=True)
        legacy = compose(sz, sprite, padding_ratio=0.14)
        legacy.save(os.path.join(out_dir, "ic_launcher.png"))

        rounded = legacy.copy()
        mask = round_mask(sz)
        rounded.putalpha(mask)
        rounded.save(os.path.join(out_dir, "ic_launcher_round.png"))

        fg_size = ADAPTIVE_FG[bucket]
        fg = compose_foreground(fg_size, sprite)
        fg.save(os.path.join(out_dir, "ic_launcher_foreground.png"))

    # Play Store listing icon (must be 512x512, opaque).
    os.makedirs(os.path.dirname(OUT_PLAY), exist_ok=True)
    play = compose(512, sprite, padding_ratio=0.16)
    play.convert("RGB").save(OUT_PLAY, format="PNG")
    print("OK")


if __name__ == "__main__":
    main()
