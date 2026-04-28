"""
Slime enemy — 32x32 pixel art, 4 idle frames + 4 walk frames
Spritesheet: 256x32
Magenta = transparent
"""
from PIL import Image
import os

_ = (255, 0, 255)
K = (15, 10, 5)       # outline
G = (60, 160, 40)     # green base
GL = (100, 210, 70)   # green light
GLL= (150, 235, 120)  # highlight
GD = (30, 100, 20)    # green dark
GDD= (15, 60, 10)     # very dark
W = (240, 240, 240)   # eye white
P = (20, 10, 60)      # pupil
T = (200, 60, 80)     # tongue
TD = (150, 30, 50)    # tongue dark

# 32x32 base slime frame
BASE = [
    [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_,_,_,K,K,K,K,K,K,K,K,_,_,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_,K,K,G,G,GL,GLL,GLL,GL,G,G,K,K,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,K,G,GL,GL,G,G,GL,GL,G,G,GL,GL,G,K,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,K,G,GL,G,G,G,G,G,G,G,G,G,G,GL,G,K,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,K,G,G,G,K,K,G,G,G,G,G,G,K,K,G,G,G,K,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,K,G,G,K,W,W,K,G,G,G,G,K,W,W,K,G,G,K,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,K,G,G,K,W,P,W,K,G,G,K,W,P,W,K,G,G,K,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,K,G,G,K,W,W,K,G,G,G,G,K,W,W,K,G,G,K,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,K,G,G,G,K,K,G,G,G,G,G,G,K,K,G,G,G,K,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,K,GD,G,G,G,G,G,K,K,K,G,G,G,G,G,GD,K,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,K,GD,G,G,G,G,K,T,T,T,K,G,G,G,G,GD,K,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,K,GD,GD,G,G,G,K,TD,T,TD,K,G,G,G,GD,GD,K,_,_,_,_,_,_],
    [_,_,_,_,_,_,K,GD,GD,GD,G,G,G,G,K,K,G,G,G,G,GD,GD,GD,K,_,_,_,_,_,_,_],
    [_,_,_,_,_,K,GD,GD,GDD,GD,GD,G,G,G,G,G,G,G,G,GD,GD,GDD,GD,GD,K,_,_,_,_,_,_],
    [_,_,_,_,K,GD,GDD,GDD,GDD,GD,GD,GD,G,G,G,G,G,G,GD,GD,GDD,GDD,GDD,GD,K,_,_,_,_,_,_],
    [_,_,_,K,GDD,GDD,GDD,GDD,GDD,GDD,GD,GD,GD,GD,GD,GD,GD,GD,GD,GD,GDD,GDD,GDD,GDD,GDD,K,_,_,_,_,_],
    [_,_,_,K,GDD,GDD,GDD,GDD,GDD,GDD,GDD,GDD,GDD,GDD,GDD,GDD,GDD,GDD,GDD,GDD,GDD,GDD,GDD,GDD,GDD,K,_,_,_,_,_],
    [_,_,_,_,K,K,K,K,K,K,K,K,K,K,K,K,K,K,K,K,K,K,K,K,K,K,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
]

def grid_to_img(grid):
    img = Image.new("RGB", (32, 32), (255, 0, 255))
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            img.putpixel((x, y), c)
    return img

def squish(grid, amount):
    """Squish vertically — compress rows toward bottom to simulate bounce"""
    result = [[_]*32 for _ in range(32)]
    for y, row in enumerate(grid):
        ny = int(y + (y / 32) * amount)
        if 0 <= ny < 32:
            result[ny] = list(row)
    return result

def stretch(grid, amount):
    """Stretch vertically — spread rows upward"""
    result = [[_]*32 for _ in range(32)]
    for y, row in enumerate(grid):
        ny = int(y - (y / 32) * amount)
        if 0 <= ny < 32:
            result[ny] = list(row)
    return result

def bob(grid, dy):
    result = [[_]*32 for _ in range(32)]
    for y, row in enumerate(grid):
        ny = y + dy
        if 0 <= ny < 32:
            result[ny] = list(row)
    return result

# Idle: bounce squish cycle
idle_frames = [
    grid_to_img(BASE),
    grid_to_img(squish(BASE, 1)),
    grid_to_img(bob(BASE, -1)),
    grid_to_img(squish(BASE, 1)),
]

# Walk: side wobble + slight squish
walk_frames = [
    grid_to_img(bob(BASE, -1)),
    grid_to_img(squish(BASE, 2)),
    grid_to_img(bob(BASE, -1)),
    grid_to_img(squish(BASE, 1)),
]

sheet = Image.new("RGB", (32 * 8, 32), (255, 0, 255))
for i, frame in enumerate(idle_frames + walk_frames):
    sheet.paste(frame, (i * 32, 0))

os.makedirs("/home/leo/dev/game-1/sprites_src", exist_ok=True)
out = "/home/leo/dev/game-1/sprites_src/slime_sheet_preview.png"
sheet.save(out)
print(f"Saved {out} — {os.path.getsize(out)} bytes")
