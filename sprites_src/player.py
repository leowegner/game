"""
Player spritesheet — 32x32 pixels per frame, 4 frames idle + 4 frames walk
Output: player.png — a 256x32 horizontal spritesheet (8 frames × 32px)
Magenta (255,0,255) = transparent
"""
from PIL import Image

_ = (255, 0, 255)   # transparent
K = (20, 12, 8)     # outline black
S = (210, 100, 30)  # skin
SD = (160, 65, 15)  # skin shadow
H = (190, 70, 20)   # hair
HD = (130, 40, 10)  # hair dark
B = (50, 100, 200)  # blue tunic
BD = (30, 65, 145)  # tunic shadow
BL = (100, 155, 235)# tunic highlight
P = (80, 50, 30)    # pants brown
PD = (55, 30, 15)   # pants shadow
G = (140, 140, 150) # hammer grey
GD = (80, 80, 90)   # hammer dark
GL = (200, 200, 210)# hammer light
W = (210, 175, 130) # wood handle
WD = (150, 110, 70) # wood dark

# Base frame — standing idle frame 0
# 32 rows, 32 cols
IDLE0 = [
    [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_,_,_,K,K,K,K,K,K,K,K,_,_,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_,_,K,H,H,HD,HD,HD,HD,H,H,K,_,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_,K,H,HD,H,H,H,H,H,H,HD,H,K,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_,K,H,S,S,S,S,S,S,S,S,H,K,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_,K,H,S,SD,S,S,S,S,SD,S,H,K,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_,K,H,S,S,S,S,S,S,S,S,H,K,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_,K,K,S,S,K,S,S,K,S,S,K,K,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_,_,K,S,S,S,S,S,S,S,S,K,_,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_,_,K,K,K,K,K,K,K,K,K,K,_,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,K,K,B,BL,B,B,B,B,B,B,B,BD,K,K,_,_,_,_,_,_,_,_],
    [_,_,_,K,GD,K,_,_,K,B,BL,B,B,B,B,B,B,B,B,B,BD,B,K,_,_,_,_,_,_,_,_,_],
    [_,_,K,GD,G,GD,K,K,B,B,B,B,B,B,B,B,B,B,B,B,B,B,K,_,_,_,_,_,_,_,_],
    [_,_,K,G,GL,G,K,K,B,B,BD,B,B,B,B,B,B,BD,B,B,B,B,K,_,_,_,_,_,_,_,_],
    [_,_,K,GD,G,GD,K,K,B,B,B,B,B,B,B,B,B,B,B,B,B,B,K,_,_,_,_,_,_,_,_],
    [_,_,_,K,W,K,_,_,K,B,B,B,BD,B,B,B,B,BD,B,B,B,B,K,_,_,_,_,_,_,_,_],
    [_,_,_,K,WD,K,_,_,_,K,B,B,B,BD,BD,BD,BD,B,B,B,K,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,K,W,K,_,_,_,_,K,K,K,K,K,K,K,K,K,K,K,_,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,K,P,PD,P,P,_,_,P,P,PD,P,K,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,K,P,P,P,P,PD,_,_,PD,P,P,P,P,K,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,K,P,P,P,P,P,_,_,P,P,P,P,P,K,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,K,PD,P,P,PD,_,_,_,_,PD,P,P,PD,K,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,K,K,K,K,_,_,_,_,K,K,K,K,_,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,K,P,P,K,_,_,_,_,K,P,P,K,_,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,K,P,PD,P,K,_,_,_,_,K,P,PD,P,K,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,K,P,P,PD,K,_,_,_,_,K,PD,P,P,K,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,K,K,K,K,K,_,_,_,_,K,K,K,K,K,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
    [_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_,_],
]

def frame_to_image(grid):
    img = Image.new("RGB", (32, 32), (255, 0, 255))
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            img.putpixel((x, y), col)
    return img

def shift_legs(grid, offsets):
    """offsets: dict of col -> row pixel shift for leg columns (12-13 left, 17-18 right)"""
    result = [list(row) for row in grid]
    # shift specific columns in the leg/boot rows (19-27)
    for col, dy in offsets.items():
        for y in range(18, 32):
            ny = y + dy
            if 0 <= ny < 32:
                result[ny][col] = grid[y][col]
            result[y][col] = _
    return result

def bob(grid, dy):
    """Shift entire sprite up or down by dy pixels"""
    result = [[_]*32 for _ in range(32)]
    for y, row in enumerate(grid):
        ny = y + dy
        if 0 <= ny < 32:
            result[ny] = list(row)
    return result

# Generate 4 idle frames (gentle bob)
idle_frames = []
for i, dy in enumerate([0, -1, -1, 0]):
    idle_frames.append(frame_to_image(bob(IDLE0, dy)))

# Generate 4 walk frames (legs alternating)
WALK_OFFSETS = [
    {9: -2, 10: -2, 11: -2, 12: -2, 18: 2, 19: 2, 20: 2},   # left leg forward
    {9: -1, 10: -1, 18: 1, 19: 1},                             # mid
    {9: 2, 10: 2, 11: 2, 12: 2, 18: -2, 19: -2, 20: -2},      # right leg forward
    {9: 1, 10: 1, 18: -1, 19: -1},                             # mid back
]
walk_frames = []
for offsets in WALK_OFFSETS:
    walk_frames.append(frame_to_image(shift_legs(IDLE0, offsets)))

# Combine into spritesheet: 8 frames × 32px wide, 32px tall
sheet = Image.new("RGB", (32 * 8, 32), (255, 0, 255))
for i, frame in enumerate(idle_frames + walk_frames):
    sheet.paste(frame, (i * 32, 0))

import os
os.makedirs("/home/leo/dev/game-1/sprites_src", exist_ok=True)
sheet.save("/home/leo/dev/game-1/sprites_src/player_sheet_preview.png")
print("Saved player_sheet_preview.png")
print(f"Size: {os.path.getsize('/home/leo/dev/game-1/sprites_src/player_sheet_preview.png')} bytes")
