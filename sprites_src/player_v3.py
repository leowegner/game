"""
Player v3 spritesheet — 48×48 pixel art, hand-crafted via drawing primitives
Medium-build fantasy warrior, front-facing. Spiky orange-red hair. Short chin-strap beard.
Dark navy hooded tunic. Brown pants. Leather boots. Large two-handed hammer on shoulder (diagonal).
Tan skin, gold/yellow belt.

Output:
  player_v3_sheet.png   — 8 frames × 48px (384×48)  4 idle + 4 walk
  player_v3_preview.png — same, 4× NEAREST scale (1536×192)
"""

from PIL import Image
import os

W, H = 48, 48

# ── Palette ───────────────────────────────────────────────────────────────────
MAG = (255,   0, 255)   # magenta = transparent bg

K   = ( 18,  12,   8)   # outline near-black

# Skin — tan
S0  = (235, 185, 130)   # highlight
S1  = (205, 150,  90)   # base
S2  = (160, 105,  55)   # shadow
S3  = (110,  65,  25)   # deep shadow

# Hair — orange-red spiky
HR0 = (255, 145,  55)   # highlight
HR1 = (220,  90,  25)   # base
HR2 = (165,  55,  10)   # shadow
HR3 = ( 95,  28,   4)   # deep

# Stubble / chin-strap
CB0 = (180,  80,  30)   # light stubble
CB1 = (130,  50,  15)   # dark stubble

# Eyes
EP  = ( 30,  20,  10)   # pupil
EW  = (235, 225, 210)   # white

# Tunic — dark navy
T0  = ( 80, 100, 175)   # highlight
T1  = ( 40,  60, 140)   # base
T2  = ( 22,  38, 100)   # shadow
T3  = ( 10,  18,  60)   # deep shadow

# Hood accent
HD0 = ( 60,  80, 155)   # hood mid
HD1 = ( 30,  50, 115)   # hood dark

# White undershirt
WH  = (240, 235, 225)
WS  = (190, 185, 175)

# Belt — gold/yellow
BL0 = (255, 215,  60)   # highlight
BL1 = (210, 165,  20)   # base
BL2 = (150, 110,   5)   # shadow
BLK = ( 35,  25,   5)   # buckle dark

# Pants — brown
P0  = (175, 120,  65)   # highlight
P1  = (130,  80,  35)   # base
P2  = ( 85,  48,  15)   # shadow
P3  = ( 50,  25,   5)   # deep shadow

# Boots — leather dark brown
BO0 = (120,  80,  45)   # highlight
BO1 = ( 80,  50,  22)   # base
BO2 = ( 48,  28,   8)   # shadow
BO3 = ( 20,  10,   2)   # sole

# Hammer head — grey steel
HH0 = (220, 225, 235)   # highlight
HH1 = (160, 165, 180)   # mid
HH2 = ( 95, 100, 118)   # shadow
HH3 = ( 45,  50,  65)   # deep

# Hammer handle — dark wood
HW0 = (175, 120,  55)   # highlight
HW1 = (120,  72,  22)   # base
HW2 = ( 70,  38,   8)   # shadow

# Handle wrap / band
RV  = (185,  30,  20)   # red wrap
RVD = (110,  12,   8)   # wrap dark

# Bare left arm (holding hammer)
MA0 = (220, 170, 110)   # highlight
MA1 = (190, 135,  75)   # mid

# ── Helpers ───────────────────────────────────────────────────────────────────

def new_frame():
    img = Image.new("RGB", (W, H), MAG)
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
        hline(img, x0, x1, y, c)

def outline(img, x0, y0, x1, y1):
    """Draw K-coloured border around a rect."""
    hline(img, x0, x1, y0, K)
    hline(img, x0, x1, y1, K)
    vline(img, x0, y0, y1, K)
    vline(img, x1, y0, y1, K)


# ── Build one frame ───────────────────────────────────────────────────────────
#
# Coordinate layout (all approximate, before body_dy):
#   y 2-6   : spiky hair
#   y 6-14  : head / face
#   y 14-16 : chin-strap / neck
#   y 17-28 : torso + arms
#   y 28-29 : belt
#   y 30-42 : legs (thigh + shin)
#   y 43-47 : boots
#
# Hammer: diagonal from bottom-left to top-right shoulder.
#   Handle runs from about (10,38) to (32,14)
#   Head sits at top-right end, roughly (28,5)-(42,15)

def build_frame(leg_dy_left=0, leg_dy_right=0, body_dy=0):
    img = new_frame()

    bd = body_dy   # shorthand

    # ──────────────────────────────────────────────────────────────────────────
    # HAMMER (drawn first so body overlaps the handle)
    # Diagonal handle: bottom-left (10,40) → top-right (32,16)
    # We trace a 2-px-wide diagonal line then place the head.
    # ──────────────────────────────────────────────────────────────────────────

    # Handle — 22-px diagonal, stepping 1 right per row going up
    # Parameterise by column offset from base point
    h_base_x, h_base_y = 10, 40 + bd
    h_tip_x,  h_tip_y  = 31, 17 + bd
    steps = abs(h_tip_y - h_base_y)   # 23 rows
    for i in range(steps + 1):
        t  = i / steps
        cx = int(h_base_x + t * (h_tip_x - h_base_x))
        cy = h_base_y - i
        # 2-px wide
        px(img, cx,     cy, HW0)
        px(img, cx + 1, cy, HW1)
        px(img, cx - 1, cy, K)
        px(img, cx + 2, cy, K)

    # Red wrap bands near handle middle
    wrap_y = h_base_y - 10
    for wy in range(wrap_y - 1, wrap_y + 3):
        t  = (h_base_y - wy) / steps
        cx = int(h_base_x + t * (h_tip_x - h_base_x))
        px(img, cx,     wy, RV)
        px(img, cx + 1, wy, RVD)

    # Hammer head — wide block at top end, tilted
    # Placed as a filled region around (h_tip_x, h_tip_y)
    # Head box: 14 wide, 8 tall, offset slightly to follow diagonal
    hh_cx = h_tip_x + 2
    hh_cy = h_tip_y - 2 + bd
    # Main steel face (front face of hammer)
    rect(img, hh_cx - 6, hh_cy - 4, hh_cx + 7, hh_cy + 4, HH1)
    # Highlight stripe top-left
    rect(img, hh_cx - 5, hh_cy - 3, hh_cx - 1, hh_cy - 1, HH0)
    # Shadow stripe bottom-right
    rect(img, hh_cx + 2, hh_cy,     hh_cx + 6, hh_cy + 3, HH2)
    hline(img, hh_cx - 6, hh_cx + 7, hh_cy + 3, HH3)
    hline(img, hh_cx - 6, hh_cx + 7, hh_cy + 4, HH3)
    # Outline
    outline(img, hh_cx - 6, hh_cy - 4, hh_cx + 7, hh_cy + 4)
    # Metal band across centre
    hline(img, hh_cx - 5, hh_cx + 6, hh_cy,     HH2)
    hline(img, hh_cx - 5, hh_cx + 6, hh_cy - 1, HH0)

    # Spike / poll on back side of head (left side)
    rect(img, hh_cx - 9, hh_cy - 1, hh_cx - 7, hh_cy + 1, HH1)
    hline(img, hh_cx - 9, hh_cx - 7, hh_cy - 2, K)
    hline(img, hh_cx - 9, hh_cx - 7, hh_cy + 2, K)
    vline(img, hh_cx - 10, hh_cy - 1, hh_cy + 1, K)

    # ──────────────────────────────────────────────────────────────────────────
    # HEAD
    # ──────────────────────────────────────────────────────────────────────────

    head_top = 5 + bd
    face_top = head_top + 3
    face_bot = face_top + 8     # y ~16

    # Face base
    rect(img, 18, face_top, 31, face_bot, S1)
    # Highlight — forehead
    hline(img, 19, 30, face_top,     S0)
    hline(img, 19, 30, face_top + 1, S0)
    # Side shadows
    vline(img, 18, face_top, face_bot, S2)
    vline(img, 31, face_top, face_bot, S2)
    # Bottom shadow
    hline(img, 18, 31, face_bot,     S3)
    hline(img, 18, 31, face_bot - 1, S2)

    # Face outline
    hline(img, 18, 31, face_top - 1, K)
    hline(img, 18, 31, face_bot + 1, K)
    vline(img, 17, face_top, face_bot, K)
    vline(img, 32, face_top, face_bot, K)

    # Eyes  (y = face_top + 3)
    ey = face_top + 3
    hline(img, 20, 22, ey, EW)
    px(img,  21, ey, EP)
    hline(img, 20, 22, ey - 1, K)   # brow left
    hline(img, 26, 28, ey, EW)
    px(img,  27, ey, EP)
    hline(img, 26, 28, ey - 1, K)   # brow right

    # Nose
    px(img, 23, face_top + 5, S3)
    px(img, 25, face_top + 5, S3)

    # Mouth — subtle smile line
    hline(img, 22, 28, face_bot - 1, S3)
    px(img, 21, face_bot - 2, S3)
    px(img, 29, face_bot - 2, S3)

    # ──────────────────────────────────────────────────────────────────────────
    # SPIKY HAIR
    # Spikes along top of head, orange-red
    # ──────────────────────────────────────────────────────────────────────────

    ht = face_top - 1   # hair starts just above face_top

    # Wide hair base covering top of head
    rect(img, 17, ht,     32, ht + 2, HR1)
    hline(img, 18, 31,    ht,         HR0)   # highlight along base

    # 5 spikes — varying heights, roughly at x positions 17, 20, 23, 26, 29
    spike_data = [
        # (base_x, width, spike_height, tip_shade)
        (17, 3, 4, HR2),
        (20, 3, 5, HR1),
        (23, 3, 6, HR0),
        (26, 3, 5, HR1),
        (29, 3, 4, HR2),
    ]
    for (sx, sw, sh, tip_c) in spike_data:
        for row in range(sh):
            shrink = row // 2
            x0 = sx + shrink
            x1 = sx + sw - 1 - shrink
            if x0 > x1:
                x0 = x1 = (sx + sw // 2)
            y  = ht - row
            shade = HR1 if row < sh // 2 else HR2
            hline(img, x0, x1, y, shade)
            if row == sh - 1:
                hline(img, x0, x1, y, tip_c)
            # highlight left edge
            px(img, x0, y, HR0)
        # outline left and right of spike
        for row in range(sh):
            shrink = row // 2
            x0 = sx + shrink
            x1 = sx + sw - 1 - shrink
            y  = ht - row
            px(img, x0 - 1, y, K)
            px(img, x1 + 1, y, K)
        # cap
        cap_shrink = (sh - 1) // 2
        cx0 = sx + cap_shrink
        cx1 = sx + sw - 1 - cap_shrink
        hline(img, cx0, cx1, ht - sh, K)

    # Hair back / sides (behind head outline)
    rect(img, 16, ht, 17, ht + 1, HR2)
    rect(img, 32, ht, 33, ht + 1, HR2)
    hline(img, 16, 33, ht - 1, K)    # top hair outline

    # Hood rim — dark navy framing the face
    vline(img, 16, face_top - 2, face_bot,     HD1)
    vline(img, 33, face_top - 2, face_bot,     HD1)
    hline(img, 16, 33, face_top - 2, HD0)
    # Outline over hood rim
    vline(img, 15, face_top - 2, face_bot,     K)
    vline(img, 34, face_top - 2, face_bot,     K)

    # ──────────────────────────────────────────────────────────────────────────
    # CHIN-STRAP / STUBBLE (NOT a full beard — just along jaw line)
    # ──────────────────────────────────────────────────────────────────────────

    jaw_y = face_bot   # y ~ 16+bd
    # Thin line along jaw sides
    px(img, 18, jaw_y,     CB1)
    px(img, 18, jaw_y - 1, CB0)
    px(img, 31, jaw_y,     CB1)
    px(img, 31, jaw_y - 1, CB0)
    # Chin centre strip (2 rows, 3 wide)
    hline(img, 22, 27, jaw_y,     CB0)
    hline(img, 22, 27, jaw_y - 1, CB1)
    # Tiny dots for stubble texture on cheeks
    px(img, 19, jaw_y - 2, CB1)
    px(img, 29, jaw_y - 2, CB1)
    px(img, 20, jaw_y - 1, CB0)
    px(img, 28, jaw_y - 1, CB0)

    # ──────────────────────────────────────────────────────────────────────────
    # NECK
    # ──────────────────────────────────────────────────────────────────────────

    neck_top = face_bot + 2
    neck_bot = neck_top + 1
    rect(img, 22, neck_top, 27, neck_bot, S2)
    vline(img, 21, neck_top, neck_bot, K)
    vline(img, 28, neck_top, neck_bot, K)
    hline(img, 22, 27, neck_top - 1, K)

    # ──────────────────────────────────────────────────────────────────────────
    # TORSO — dark navy hooded tunic / vest
    # ──────────────────────────────────────────────────────────────────────────

    torso_top = neck_bot + 1
    torso_bot = torso_top + 10   # y ~ 30

    # Tunic body
    rect(img, 19, torso_top, 32, torso_bot, T1)
    # Highlight left stripe
    vline(img, 20, torso_top + 1, torso_bot - 1, T0)
    # Shadow right
    vline(img, 31, torso_top + 1, torso_bot - 1, T2)
    vline(img, 32, torso_top + 1, torso_bot - 1, T3)
    # White shirt / tunic centre opening
    rect(img, 23, torso_top + 1, 28, torso_bot - 1, WH)
    rect(img, 24, torso_top + 2, 27, torso_bot - 2, WS)

    # Hood drape over shoulders (wider dark panels)
    rect(img, 14, torso_top, 19, torso_top + 5, HD1)
    vline(img, 15, torso_top, torso_top + 5, HD0)
    rect(img, 32, torso_top, 37, torso_top + 5, HD1)
    vline(img, 36, torso_top, torso_top + 5, HD0)

    # Torso outline
    hline(img, 14, 37, torso_top - 1, K)
    hline(img, 14, 37, torso_bot + 1, K)
    vline(img, 13, torso_top, torso_bot, K)
    vline(img, 38, torso_top, torso_bot, K)

    # ──────────────────────────────────────────────────────────────────────────
    # LEFT ARM — bare, gripping hammer handle (at left side)
    # ──────────────────────────────────────────────────────────────────────────

    la_top = torso_top + 1
    la_bot = torso_top + 8
    rect(img, 13, la_top, 17, la_bot, MA1)
    vline(img, 14, la_top, la_bot, MA0)
    # hand / fist (slightly wider at bottom)
    rect(img, 12, la_bot - 1, 17, la_bot + 2, S1)
    hline(img, 12, 17, la_bot - 2, K)
    hline(img, 12, 17, la_bot + 3, K)
    vline(img, 11, la_bot - 1, la_bot + 2, K)
    vline(img, 18, la_bot - 1, la_bot + 2, K)
    # grip outline
    vline(img, 12, la_top, la_bot - 2, K)
    vline(img, 18, la_top, la_bot - 2, K)

    # ──────────────────────────────────────────────────────────────────────────
    # RIGHT ARM — tunic sleeve
    # ──────────────────────────────────────────────────────────────────────────

    ra_top = torso_top + 1
    ra_bot = torso_top + 8
    rect(img, 34, ra_top, 38, ra_bot, T1)
    vline(img, 35, ra_top + 1, ra_bot - 1, T0)
    vline(img, 37, ra_top + 1, ra_bot - 1, T2)
    # cuff
    hline(img, 34, 38, ra_bot, T2)
    # hand
    rect(img, 34, ra_bot + 1, 38, ra_bot + 3, S1)
    hline(img, 34, 38, ra_bot + 4, K)
    vline(img, 33, ra_top, ra_bot + 3, K)
    vline(img, 39, ra_top, ra_bot + 3, K)
    hline(img, 34, 38, ra_top - 1, K)

    # ──────────────────────────────────────────────────────────────────────────
    # BELT — gold/yellow
    # ──────────────────────────────────────────────────────────────────────────

    belt_y = torso_bot + 1
    rect(img, 16, belt_y,     35, belt_y + 2, BL1)
    hline(img, 17, 34, belt_y,     BL0)
    hline(img, 17, 34, belt_y + 2, BL2)
    # Buckle centre
    rect(img, 23, belt_y,     26, belt_y + 2, BLK)
    px(img, 24, belt_y + 1, BL0)
    px(img, 25, belt_y + 1, BL0)
    # Belt outline
    hline(img, 16, 35, belt_y - 1, K)
    hline(img, 16, 35, belt_y + 3, K)
    vline(img, 15, belt_y, belt_y + 2, K)
    vline(img, 36, belt_y, belt_y + 2, K)

    # ──────────────────────────────────────────────────────────────────────────
    # LEGS — brown pants
    # ──────────────────────────────────────────────────────────────────────────

    leg_top = belt_y + 4

    def draw_leg(lx, dy):
        lt = leg_top + dy
        # thigh
        rect(img, lx,     lt,      lx + 4, lt + 5, P1)
        vline(img, lx + 1, lt,     lt + 5, P0)
        vline(img, lx + 3, lt,     lt + 5, P2)
        vline(img, lx + 4, lt,     lt + 5, P3)
        # shin
        rect(img, lx,     lt + 6,  lx + 4, lt + 11, P1)
        vline(img, lx + 1, lt + 6, lt + 11, P0)
        vline(img, lx + 3, lt + 6, lt + 11, P2)
        # leg outline
        hline(img, lx, lx + 4, lt - 1, K)
        vline(img, lx - 1, lt, lt + 11, K)
        vline(img, lx + 5, lt, lt + 11, K)
        hline(img, lx, lx + 4, lt + 12, K)
        # boot
        bx0 = lx - 1
        bx1 = lx + 5
        by0 = lt + 12
        rect(img, bx0, by0,     bx1, by0 + 2, BO1)
        hline(img, bx0, bx1,    by0, BO0)
        # toe extension forward
        rect(img, bx0 - 1, by0 + 1, bx1 + 1, by0 + 3, BO1)
        hline(img, bx0 - 1, bx1 + 1, by0 + 1, BO0)
        hline(img, bx0 - 1, bx1 + 1, by0 + 3, BO2)
        # sole
        hline(img, bx0 - 1, bx1 + 1, by0 + 4, BO3)
        hline(img, bx0 - 1, bx1 + 1, by0 + 5, BO3)
        # boot outline
        hline(img, bx0 - 1, bx1 + 1, by0 - 1, K)
        vline(img, bx0 - 2, by0, by0 + 5, K)
        vline(img, bx1 + 2, by0, by0 + 5, K)
        hline(img, bx0 - 1, bx1 + 1, by0 + 6, K)

    draw_leg(18, leg_dy_left)
    draw_leg(26, leg_dy_right)

    return img


# ── Generate frames ───────────────────────────────────────────────────────────

# Idle: body bobs dy = [0, -1, -1, 0]
idle_frames = [
    build_frame(0, 0,  0),
    build_frame(0, 0, -1),
    build_frame(0, 0, -1),
    build_frame(0, 0,  0),
]

# Walk: legs alternate, body bobs on frames 0 and 2
walk_frames = [
    build_frame(-3,  3, -1),   # left leg forward, body up
    build_frame(-1,  1,  0),   # mid-step
    build_frame( 3, -3, -1),   # right leg forward, body up
    build_frame( 1, -1,  0),   # mid-step
]

# ── Assemble spritesheet ──────────────────────────────────────────────────────

all_frames = idle_frames + walk_frames
sheet = Image.new("RGB", (W * 8, H), MAG)
for i, frame in enumerate(all_frames):
    sheet.paste(frame, (i * W, 0))

preview = sheet.resize((W * 8 * 4, H * 4), Image.NEAREST)

out_dir = "/home/leo/dev/game-1/sprites_src"
os.makedirs(out_dir, exist_ok=True)
sheet_path   = f"{out_dir}/player_v3_sheet.png"
preview_path = f"{out_dir}/player_v3_preview.png"
sheet.save(sheet_path)
preview.save(preview_path)
print(f"Saved {sheet_path}   ({W * 8}×{H})")
print(f"Saved {preview_path} ({W * 8 * 4}×{H * 4}) — 4× zoom")
