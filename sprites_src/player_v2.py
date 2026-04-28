"""
player_v2.py — 48x48 hand-crafted pixel art warrior
Output: player_v2_sheet.png (384x48, 8 frames: 4 idle + 4 walk)
        player_v2_preview.png (same, 4x scaled NEAREST)

Character: stocky fantasy warrior, front-facing.
  - Red-orange hair + full beard
  - Blue tunic with white undershirt
  - Brown leather belt with gold buckle
  - Deep red pants
  - Dark brown boots
  - Large war hammer in left hand (head at shoulder height)

Palette: dark near-black outline K=(18,12,8), 3-4 shades per part
Background: magenta (255,0,255) = transparent
"""

from PIL import Image
import os, copy

W, H = 48, 48
OUT_DIR = "/home/leo/dev/game-1/sprites_src"

# ── Palette ────────────────────────────────────────────────────────────────────
MG  = (255,   0, 255)   # magenta = transparent background
K   = ( 18,  12,   8)   # dark near-black outline

# Skin
S0  = (248, 192, 140)   # skin highlight
S1  = (220, 155,  95)   # skin base
S2  = (175, 108,  55)   # skin shadow
S3  = (125,  68,  25)   # skin deep shadow

# Hair / Beard  (red-orange family)
HR0 = (255, 145,  50)   # hair highlight
HR1 = (215,  90,  20)   # hair base
HR2 = (160,  52,   8)   # hair shadow
HR3 = (100,  28,   4)   # hair deep

# Eyes
EP  = ( 25,  15,  10)   # pupil / dark
EB  = ( 15,  10,   8)   # brow

# Tunic (blue)
T0  = (145, 190, 255)   # tunic highlight
T1  = ( 65, 125, 220)   # tunic base
T2  = ( 35,  80, 170)   # tunic shadow
T3  = ( 18,  45, 115)   # tunic deep

# White undershirt
WH  = (245, 240, 230)   # shirt highlight
WS  = (195, 190, 180)   # shirt shadow

# Belt (brown leather + gold buckle)
BL0 = (185, 145,  65)   # leather highlight
BL1 = (130,  90,  30)   # leather base
BL2 = ( 80,  50,  10)   # leather shadow
GD0 = (255, 215,  60)   # gold highlight
GD1 = (200, 160,  20)   # gold base
GD2 = (130,  95,   5)   # gold shadow

# Pants (deep red)
R0  = (235, 100,  70)   # pants highlight
R1  = (185,  55,  32)   # pants base
R2  = (130,  22,  10)   # pants shadow
R3  = ( 80,   8,   3)   # pants deep

# Boots (dark brown)
BO0 = (145, 100,  58)   # boot highlight
BO1 = ( 95,  60,  28)   # boot base
BO2 = ( 55,  32,  10)   # boot shadow
BO3 = ( 22,  12,   3)   # boot sole / deep

# Hammer head (steel)
HH0 = (220, 225, 235)   # hammer highlight
HH1 = (160, 165, 180)   # hammer base
HH2 = ( 95, 100, 115)   # hammer shadow
HH3 = ( 45,  50,  65)   # hammer deep

# Hammer handle (wood)
HW0 = (195, 150,  85)   # handle highlight
HW1 = (145, 100,  42)   # handle base
HW2 = ( 88,  55,  15)   # handle shadow

# Hammer ribbon (red)
RV  = (190,  35,  22)   # ribbon
RVD = (110,  14,   8)   # ribbon dark

# ── Drawing helpers ────────────────────────────────────────────────────────────

def new_frame():
    img = Image.new("RGB", (W, H), MG)
    return img

def px(img, x, y, c):
    if 0 <= x < W and 0 <= y < H:
        img.putpixel((x, y), c)

def hline(img, x0, x1, y, c):
    for x in range(x0, x1 + 1):
        px(img, x, y, c)

def vline(img, x, y0, y1, c):
    for y in range(y0, y1 + 1):
        px(img, x, y, c)

def rect(img, x0, y0, x1, y1, c):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            px(img, x, y, c)

def outline_rect(img, x0, y0, x1, y1, fill, border=K):
    rect(img, x0, y0, x1, y1, fill)
    hline(img, x0, x1, y0, border)
    hline(img, x0, x1, y1, border)
    vline(img, x0, y0, y1, border)
    vline(img, x1, y0, y1, border)

def shift_cols(img, x_cols, dy):
    """Shift specific columns of img down by dy pixels (positive=down)."""
    for x in x_cols:
        col = [img.getpixel((x, y)) for y in range(H)]
        for y in range(H):
            src = y - dy
            if 0 <= src < H:
                img.putpixel((x, y), col[src])
            else:
                img.putpixel((x, y), MG)

# ── Layout constants (all Y coords relative to top of 48px frame) ─────────────
#
# Head top:    y=2   (hair starts)
# Head:        y=2..12   (~10px tall including hair)
# Neck:        y=13..14
# Torso:       y=15..27  (~12px)
# Belt:        y=28..30
# Legs:        y=31..42  (~12px)
# Boots:       y=43..47  (~5px)

# The character is centered horizontally.  Body center x ≈ 24.
# Hammer is to the LEFT of the character (x ≈ 3..14).

# ── Draw hammer (drawn first so body layers over handle) ──────────────────────

def draw_hammer(img, body_dy):
    # Handle: x=9..11, y=14..38 (extends from head level to below belt)
    hy0 = 12 + body_dy
    hy1 = 38 + body_dy
    vline(img, 10, hy0, hy1, HW0)
    vline(img, 11, hy0, hy1, HW1)
    vline(img, 12, hy0, hy1, HW2)
    vline(img,  9, hy0, hy1, K)
    vline(img, 13, hy0, hy1, K)

    # Hammer head: x=2..13, y=2..12 (sits at shoulder / head height)
    hx0, hx1 = 2, 13
    hhy0 = 2 + body_dy
    hhy1 = 12 + body_dy

    # Main body mid-tone
    rect(img, hx0+1, hhy0+1, hx1-1, hhy1-1, HH1)
    # Top highlight strip
    hline(img, hx0+1, hx1-1, hhy0+1, HH0)
    hline(img, hx0+1, hx0+3, hhy0+1, HH0)
    rect(img, hx0+1, hhy0+1, hx0+4, hhy0+3, HH0)  # top-left corner bright
    # Right shadow
    vline(img, hx1-1, hhy0+1, hhy1-1, HH2)
    vline(img, hx1-2, hhy0+2, hhy1-1, HH2)
    # Bottom deep shadow
    hline(img, hx0+1, hx1-1, hhy1-1, HH3)
    hline(img, hx0+2, hx1-2, hhy1-2, HH2)
    # Red ribbon band (decorative wrap)
    hline(img, hx0+1, hx1-1, hhy0+4, RV)
    hline(img, hx0+1, hx1-1, hhy0+5, RVD)
    hline(img, hx0+1, hx1-1, hhy0+6, RV)
    # Outline
    hline(img, hx0, hx1, hhy0, K)
    hline(img, hx0, hx1, hhy1, K)
    vline(img, hx0, hhy0, hhy1, K)
    vline(img, hx1, hhy0, hhy1, K)

# ── Draw head ─────────────────────────────────────────────────────────────────

def draw_head(img, body_dy):
    ht = 2 + body_dy   # top of hair
    # Centre of head: x=16..31  (16px wide)

    # ── Hair (top + sides) ────────────────────────────────────────────────────
    # Top hair bulk: y=ht..ht+3
    hline(img, 16, 31, ht,   HR3)           # very top outline merged with hair
    hline(img, 16, 31, ht+1, HR2)
    hline(img, 17, 30, ht+2, HR1)
    hline(img, 18, 29, ht+3, HR0)           # highlight inside

    # Side hair bumps (add a bit of volume)
    # Left side
    px(img, 15, ht+1, HR2)
    px(img, 15, ht+2, HR1)
    px(img, 14, ht+2, HR2)
    # Right side
    px(img, 32, ht+1, HR2)
    px(img, 32, ht+2, HR1)
    px(img, 33, ht+2, HR2)

    # ── Face ─────────────────────────────────────────────────────────────────
    ft = ht + 4    # face top (below hair)
    fb = ft + 7    # face bottom (y=13 at body_dy=0)

    # Face base fill
    rect(img, 17, ft, 30, fb, S1)
    # Highlights
    hline(img, 18, 29, ft,   S0)
    hline(img, 18, 29, ft+1, S0)
    vline(img, 18, ft, fb,   S0)   # left highlight strip
    # Shadow right/bottom
    vline(img, 29, ft+1, fb, S2)
    vline(img, 30, ft+1, fb, S2)
    hline(img, 18, 30, fb,   S3)
    hline(img, 18, 30, fb-1, S2)

    # Head outline (sides + top continuity)
    vline(img, 16, ft, fb, K)
    vline(img, 31, ft, fb, K)

    # ── Eyes ─────────────────────────────────────────────────────────────────
    ey = ft + 3
    # Brows
    hline(img, 19, 21, ey-1, EB)
    hline(img, 26, 28, ey-1, EB)
    # Eye whites (3px wide)
    hline(img, 19, 21, ey, S0)
    hline(img, 26, 28, ey, S0)
    # Pupils (center of each eye)
    px(img, 20, ey, EP)
    px(img, 27, ey, EP)
    # Lower lash line
    hline(img, 19, 21, ey+1, K)
    hline(img, 26, 28, ey+1, K)

    # ── Nose (small dot pair) ─────────────────────────────────────────────────
    px(img, 22, ft+5, S3)
    px(img, 25, ft+5, S3)

    # ── Mouth / warrior expression (thin frown) ───────────────────────────────
    mx = 24
    my = ft + 6
    hline(img, mx-2, mx+2, my, K)   # straight line
    px(img, mx-2, my-1, K)          # downward corners
    px(img, mx+2, my-1, K)

    # ── Beard (covers lower half of face) ────────────────────────────────────
    bt = fb - 2      # beard starts 2px before face bottom (overlaps)
    bb = fb + 5      # beard extends below face

    # Beard bulk
    rect(img, 16, bt, 31, bb, HR1)
    # Upper transition blended with face
    hline(img, 17, 30, bt,   HR0)
    hline(img, 17, 30, bt+1, HR1)
    # Lower beard shading
    hline(img, 16, 31, bb,   HR3)
    hline(img, 16, 31, bb-1, HR2)
    # Side shadow
    vline(img, 16, bt, bb, HR2)
    vline(img, 31, bt, bb, HR2)
    # Center highlight ridge
    vline(img, 23, bt, bb-1, HR0)
    vline(img, 24, bt, bb-1, HR0)
    # Texture strand lines
    for x in (18, 21, 25, 28):
        px(img, x, bt+2, HR2)
        px(img, x, bt+3, HR3)
        px(img, x, bt+4, HR2)
    # Beard outline (bottom + sides)
    hline(img, 15, 32, bb+1, K)
    vline(img, 15, bt, bb, K)
    vline(img, 32, bt, bb, K)

    # ── Neck ─────────────────────────────────────────────────────────────────
    nt = bb + 2
    nb = nt + 1
    rect(img, 21, nt, 26, nb, S2)
    vline(img, 20, nt, nb, K)
    vline(img, 27, nt, nb, K)
    hline(img, 21, 26, nb+1, K)

# ── Draw torso / arms ─────────────────────────────────────────────────────────

def draw_torso(img, body_dy):
    tt = 15 + body_dy   # torso top
    tb = 26 + body_dy   # torso bottom

    # ── Left arm (bare skin — hammer hand) ────────────────────────────────────
    # x=13..17, hangs alongside torso
    at = tt
    ab = tt + 9
    rect(img, 13, at, 16, ab, S1)
    vline(img, 14, at, ab, S0)
    vline(img, 13, at, ab, K)
    vline(img, 17, at, ab, K)
    hline(img, 13, 17, at, K)
    hline(img, 13, 17, ab+1, K)
    # Fist / grip (slightly darker)
    rect(img, 13, ab-2, 16, ab, S2)
    hline(img, 13, 16, ab-3, K)

    # ── Tunic body ────────────────────────────────────────────────────────────
    rect(img, 18, tt, 33, tb, T1)
    # Left highlight stripe
    vline(img, 19, tt+1, tb-1, T0)
    # Right shadow stripes
    vline(img, 32, tt+1, tb-1, T2)
    vline(img, 33, tt+1, tb-1, T3)
    # Center white undershirt V-neck
    rect(img, 22, tt+1, 27, tb-1, WH)
    vline(img, 22, tt+1, tb-1, WS)
    vline(img, 27, tt+1, tb-1, WS)
    # Shirt crease lines
    hline(img, 23, 26, tt+3, WS)
    hline(img, 23, 26, tt+6, WS)
    # V-neck cut detail
    px(img, 23, tt+1, T1)
    px(img, 26, tt+1, T1)

    # ── Right arm (tunic sleeve) ───────────────────────────────────────────────
    rect(img, 34, at, 38, ab, T1)
    vline(img, 35, at+1, ab-1, T0)
    vline(img, 37, at+1, ab-1, T2)
    vline(img, 34, at, ab, K)
    vline(img, 38, at, ab, K)
    hline(img, 34, 38, at, K)
    hline(img, 34, 38, ab+1, K)
    # Cuff at bottom of sleeve
    hline(img, 34, 38, ab-1, T3)
    # Fist / hand peek
    rect(img, 34, ab, 38, ab+2, S1)
    hline(img, 34, 38, ab+3, K)

    # ── Torso outline ─────────────────────────────────────────────────────────
    hline(img, 13, 38, tt-1, K)
    hline(img, 18, 33, tb+1, K)
    vline(img, 12, tt, tb, K)
    vline(img, 39, tt, tb, K)

# ── Draw belt ─────────────────────────────────────────────────────────────────

def draw_belt(img, body_dy):
    by = 27 + body_dy
    # Belt strap
    rect(img, 16, by, 35, by+2, BL1)
    hline(img, 17, 34, by,   BL0)
    hline(img, 17, 34, by+2, BL2)
    # Gold buckle (center, 3px wide)
    rect(img, 22, by, 25, by+2, GD1)
    hline(img, 22, 25, by,   GD0)
    hline(img, 22, 25, by+2, GD2)
    px(img, 23, by+1, GD0)   # buckle prong highlight
    # Belt outline
    hline(img, 15, 36, by-1, K)
    hline(img, 15, 36, by+3, K)
    vline(img, 15, by, by+2, K)
    vline(img, 36, by, by+2, K)
    # Belt loop lines
    px(img, 19, by+1, BL2)
    px(img, 30, by+1, BL2)

# ── Draw one leg ──────────────────────────────────────────────────────────────

def draw_leg(img, lx, top, dy):
    """Draw a single leg+boot. lx=left x, top=top y, dy=vertical shift."""
    lt = top + dy
    lw = 5   # leg width

    # Thigh
    rect(img, lx, lt, lx+lw-1, lt+6, R1)
    vline(img, lx+1, lt, lt+6, R0)
    vline(img, lx+lw-2, lt, lt+6, R2)
    vline(img, lx+lw-1, lt, lt+6, R3)

    # Shin (slightly narrower feel via shading)
    rect(img, lx, lt+7, lx+lw-1, lt+12, R1)
    vline(img, lx+1, lt+7, lt+12, R0)
    vline(img, lx+lw-2, lt+7, lt+12, R2)
    vline(img, lx+lw-1, lt+7, lt+12, R3)

    # Leg outline
    vline(img, lx-1, lt, lt+12, K)
    vline(img, lx+lw, lt, lt+12, K)
    hline(img, lx, lx+lw-1, lt-1, K)
    hline(img, lx, lx+lw-1, lt+13, K)

    # Boot
    bx0 = lx - 1
    bx1 = lx + lw + 1   # boot wider than leg
    by0 = lt + 13

    # Boot upper
    rect(img, bx0+1, by0, bx1-1, by0+2, BO1)
    hline(img, bx0+1, bx1-1, by0, BO0)
    # Boot toe extension
    rect(img, bx0, by0+2, bx1, by0+4, BO1)
    hline(img, bx0, bx1, by0+2, BO0)
    hline(img, bx0, bx1, by0+4, BO2)
    # Sole
    hline(img, bx0, bx1, by0+5, BO3)
    hline(img, bx0, bx1, by0+6, BO3)
    # Boot outline
    hline(img, bx0, bx1, by0-1, K)
    vline(img, bx0-1, by0, by0+6, K)
    vline(img, bx1+1, by0, by0+6, K)
    hline(img, bx0-1, bx1+1, by0+7, K)
    # Boot crease line
    hline(img, bx0, bx1, by0+1, BO2)

# ── Build one complete frame ───────────────────────────────────────────────────

LEG_TOP = 31   # leg top y at body_dy=0
LEFT_LEG_X  = 17
RIGHT_LEG_X = 26

def build_frame(body_dy=0, left_leg_dy=0, right_leg_dy=0):
    img = new_frame()

    # Hammer is behind body, draw first
    draw_hammer(img, body_dy)
    draw_head(img, body_dy)
    draw_torso(img, body_dy)
    draw_belt(img, body_dy)
    draw_leg(img, LEFT_LEG_X,  LEG_TOP, left_leg_dy)
    draw_leg(img, RIGHT_LEG_X, LEG_TOP, right_leg_dy)

    return img

# ── Helper: shift leg columns for walk animation ───────────────────────────────

def shift_leg_cols(base_img, leg_x, lw, dy):
    """Return a copy of base_img with a leg (cols leg_x..leg_x+lw+2) shifted by dy."""
    img = base_img.copy()
    # Grab all columns of that leg (including boot overhang)
    cols = range(leg_x - 2, leg_x + lw + 3)
    # Save original column data
    col_data = {}
    for x in cols:
        if 0 <= x < W:
            col_data[x] = [img.getpixel((x, y)) for y in range(H)]
    # Rewrite shifted
    for x in cols:
        if x not in col_data:
            continue
        orig = col_data[x]
        for y in range(H):
            src = y - dy
            if 0 <= src < H:
                img.putpixel((x, y), orig[src])
            else:
                img.putpixel((x, y), MG)
    return img

# ── Generate idle frames 0-3 ──────────────────────────────────────────────────
#   Frame 0: neutral
#   Frame 1: body up 1px (bob up)
#   Frame 2: body up 1px (hold)
#   Frame 3: body down 1px (bob down)

idle_frames = [
    build_frame(body_dy= 0),
    build_frame(body_dy=-1),
    build_frame(body_dy=-1),
    build_frame(body_dy= 1),
]

# ── Generate walk frames 4-7 ──────────────────────────────────────────────────
#   Walk legs shift using shift_cols helper
#   body_dy = -1 on frames 4 and 6 (mid-stride "up" bounce)

# Base neutral frame for walk (no body_dy, we shift legs after)
_walk_base = build_frame(body_dy=0)

def walk_frame(body_dy, left_dy, right_dy):
    # Build with body_dy, then manually we'll use the leg y offsets via build_frame
    return build_frame(body_dy=body_dy,
                       left_leg_dy=left_dy,
                       right_leg_dy=right_dy)

walk_frames = [
    walk_frame(body_dy=-1, left_dy=-3, right_dy= 3),   # frame 4: left fwd
    walk_frame(body_dy= 0, left_dy=-1, right_dy= 1),   # frame 5: mid
    walk_frame(body_dy=-1, left_dy= 3, right_dy=-3),   # frame 6: right fwd
    walk_frame(body_dy= 0, left_dy= 1, right_dy=-1),   # frame 7: mid
]

# ── Assemble and save ─────────────────────────────────────────────────────────

all_frames = idle_frames + walk_frames
sheet = Image.new("RGB", (W * 8, H), MG)
for i, frame in enumerate(all_frames):
    sheet.paste(frame, (i * W, 0))

preview = sheet.resize((W * 8 * 4, H * 4), Image.NEAREST)

os.makedirs(OUT_DIR, exist_ok=True)
sheet_path   = f"{OUT_DIR}/player_v2_sheet.png"
preview_path = f"{OUT_DIR}/player_v2_preview.png"
sheet.save(sheet_path)
preview.save(preview_path)
print(f"Saved {sheet_path}  ({W*8}×{H})")
print(f"Saved {preview_path}  ({W*8*4}×{H*4})  [4× zoom]")
