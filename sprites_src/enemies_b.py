"""
enemies_b.py — 4 enemy spritesheets, 48x48 pixel art, hand-crafted via drawing primitives.
Each output: 384x48 (8 frames: 4 idle + 4 walk), magenta transparent background.
Enemies: enemy_mage, enemy_charger, enemy_bomber, enemy_boss
"""
from PIL import Image
import os

W, H = 48, 48
_ = (255, 0, 255)   # transparent / magenta bg
K  = (18, 12, 8)    # outline (dark)
K2 = (40, 25, 15)   # soft inner line

OUT = "/home/leo/dev/game-1/sprites_src"
os.makedirs(OUT, exist_ok=True)

# ── Drawing helpers ────────────────────────────────────────────────────────────

def new_frame():
    return Image.new("RGB", (W, H), _)

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

def orect(img, x0, y0, x1, y1, fill, border=K):
    rect(img, x0, y0, x1, y1, fill)
    hline(img, x0, x1, y0, border)
    hline(img, x0, x1, y1, border)
    vline(img, x0, y0, y1, border)
    vline(img, x1, y0, y1, border)

def circle(img, cx, cy, rx, ry, c):
    for dy in range(-ry, ry + 1):
        for dx in range(-rx, rx + 1):
            if (dx / rx) ** 2 + (dy / ry) ** 2 <= 1.0:
                px(img, cx + dx, cy + dy, c)

def save_sheet(frames, name):
    sheet = Image.new("RGB", (W * 8, H), _)
    for i, f in enumerate(frames):
        sheet.paste(f, (i * W, 0))
    preview = sheet.resize((W * 8 * 4, H * 4), Image.NEAREST)
    sheet.save(f"{OUT}/{name}_sheet.png")
    preview.save(f"{OUT}/{name}_preview.png")
    print(f"Saved {name}_sheet.png ({W*8}×{H})  +  {name}_preview.png ({W*8*4}×{H*4})")

# ══════════════════════════════════════════════════════════════════════════════
# ENEMY_MAGE  —  robed spellcaster, pointed hat, white beard, glowing blue orb
# ══════════════════════════════════════════════════════════════════════════════

# Mage palette
MG_RP0 = (120,  60, 160)   # robe highlight
MG_RP1 = ( 80,  30, 120)   # robe base
MG_RP2 = ( 50,  15,  85)   # robe shadow
MG_RP3 = ( 25,   6,  48)   # robe deep
MG_HP0 = ( 55,  20,  95)   # hat highlight
MG_HP1 = ( 35,  10,  70)   # hat base
MG_HP2 = ( 18,   4,  42)   # hat shadow
MG_BD0 = (240, 235, 220)   # beard / white highlight
MG_BD1 = (200, 195, 180)   # beard base
MG_BD2 = (150, 145, 135)   # beard shadow
MG_SK0 = (230, 175, 120)   # skin hi
MG_SK1 = (200, 140,  85)   # skin base
MG_SK2 = (155,  95,  50)   # skin shadow
MG_EY  = ( 80, 210, 255)   # glowing eye blue
MG_OR0 = (100, 180, 255)   # orb highlight
MG_OR1 = ( 50, 120, 220)   # orb base
MG_OR2 = ( 20,  65, 160)   # orb shadow
MG_OG  = (160, 230, 255)   # orb glow
MG_ST0 = (190, 145,  65)   # staff highlight
MG_ST1 = (140, 100,  35)   # staff base
MG_ST2 = ( 85,  58,  12)   # staff shadow


def build_mage(float_dy=0, orb_glow=False):
    """float_dy: -1,0,+1 to simulate hovering; orb_glow: brighten orb"""
    img = new_frame()
    fy = float_dy  # body float offset

    # ── STAFF (left side, x=7..9, y=10..40) ──────────────────────────────────
    vline(img,  8, 12 + fy, 40 + fy, MG_ST0)
    vline(img,  9, 12 + fy, 40 + fy, MG_ST1)
    vline(img, 10, 12 + fy, 40 + fy, MG_ST2)
    vline(img,  7, 12 + fy, 40 + fy, K)
    vline(img, 11, 12 + fy, 40 + fy, K)
    # Staff knob top
    hline(img, 6, 12, 11 + fy, K)
    hline(img, 6, 12, 10 + fy, MG_ST0)
    px(img, 9, 10 + fy, MG_ST1)

    # ── ORB (floating at staff tip, x=3..10, y=5..11+fy) ─────────────────────
    ox, oy = 9, 6 + fy
    orb_c = MG_OG if orb_glow else MG_OR0
    circle(img, ox, oy, 4, 4, MG_OR2)
    circle(img, ox, oy, 3, 3, MG_OR1)
    circle(img, ox, oy, 2, 2, orb_c)
    px(img, ox - 1, oy - 1, MG_OR0)
    # orb glow ring
    hline(img, ox - 4, ox + 4, oy, K)
    hline(img, ox - 4, ox + 4, oy - 4, K)
    hline(img, ox - 4, ox + 4, oy + 4, K)
    vline(img, ox - 4, oy - 4, oy + 4, K)
    vline(img, ox + 4, oy - 4, oy + 4, K)
    # inner glow edge
    hline(img, ox - 3, ox + 3, oy - 3, MG_OR2)
    hline(img, ox - 3, ox + 3, oy + 3, MG_OR2)
    vline(img, ox - 3, oy - 3, oy + 3, MG_OR2)
    vline(img, ox + 3, oy - 3, oy + 3, MG_OR2)

    # ── POINTED HAT (center ~x=22, y=3..12+fy) ───────────────────────────────
    # Brim: y=12+fy, x=16..33
    hline(img, 16, 33, 12 + fy,     MG_HP1)
    hline(img, 16, 33, 11 + fy,     K)
    hline(img, 15, 34, 13 + fy,     MG_HP0)
    hline(img, 15, 34, 14 + fy,     K)
    # Cone: widens from tip down
    # tip at x=24, y=3+fy
    for row in range(0, 9):
        yx = 3 + row + fy
        half = row // 2
        lx = 24 - half
        rx = 24 + half
        hline(img, lx, rx, yx, MG_HP1)
        px(img, lx,     yx, MG_HP2)
        if rx > lx:
            px(img, rx, yx, MG_HP2)
        px(img, lx + 1, yx, MG_HP0)
        # outline sides
        px(img, lx - 1, yx, K)
        px(img, rx + 1, yx, K)
    # Hat tip outline
    px(img, 24, 2 + fy, K)
    # Brim sides outline
    px(img, 14, 13 + fy, K)
    px(img, 35, 13 + fy, K)

    # ── HEAD/FACE (x=18..30, y=14..21+fy) ────────────────────────────────────
    head_top = 15 + fy
    head_bot = 22 + fy
    rect(img, 18, head_top, 30, head_bot, MG_SK1)
    hline(img, 19, 29, head_top, MG_SK0)
    vline(img, 18, head_top, head_bot, MG_SK2)
    vline(img, 30, head_top, head_bot, MG_SK2)
    hline(img, 18, 30, head_bot, MG_SK2)
    # head outline
    hline(img, 17, 31, head_top - 1, K)
    hline(img, 17, 31, head_bot + 1, K)
    vline(img, 17, head_top, head_bot, K)
    vline(img, 31, head_top, head_bot, K)
    # Eyes — glowing blue
    ey = head_top + 3
    px(img, 21, ey, MG_EY); px(img, 22, ey, MG_EY)
    px(img, 27, ey, MG_EY); px(img, 28, ey, MG_EY)
    hline(img, 20, 23, ey - 1, K)
    hline(img, 26, 29, ey - 1, K)
    # Nose
    px(img, 24, ey + 2, MG_SK2)

    # ── BEARD (white, wide, x=16..32, y=21..28+fy) ───────────────────────────
    bt = head_bot
    bb = bt + 7
    rect(img, 16, bt, 32, bb + fy - fy, MG_BD1)  # stays at head_bot
    bb = bt + 7
    rect(img, 16, bt, 32, bb, MG_BD1)
    hline(img, 17, 31, bt, MG_BD0)
    hline(img, 16, 32, bb, MG_BD2)
    vline(img, 16, bt, bb, MG_BD2)
    vline(img, 32, bt, bb, MG_BD2)
    # Beard texture strokes
    for tx in range(18, 32, 3):
        px(img, tx,     bt + 2, MG_BD2)
        px(img, tx + 1, bt + 4, MG_BD2)
    # Tapered bottom
    hline(img, 18, 30, bb + 1, MG_BD2)
    hline(img, 20, 28, bb + 2, MG_BD2)
    hline(img, 15, 33, bt - 1, K)
    hline(img, 15, 33, bb + 3, K)
    vline(img, 14, bt, bb + 2, K)
    vline(img, 34, bt, bb + 2, K)

    # ── ROBE BODY (x=14..35, y=30..43+fy) ────────────────────────────────────
    robe_top = bb + 4
    robe_bot = 43 + fy
    rect(img, 15, robe_top, 34, robe_bot, MG_RP1)
    vline(img, 16, robe_top + 1, robe_bot - 1, MG_RP0)
    vline(img, 33, robe_top + 1, robe_bot - 1, MG_RP2)
    vline(img, 34, robe_top + 1, robe_bot - 1, MG_RP3)
    # Center fold
    vline(img, 24, robe_top + 2, robe_bot - 2, MG_RP2)
    vline(img, 25, robe_top + 2, robe_bot - 2, MG_RP0)
    # Robe widens at base
    hline(img, 13, 35, robe_bot,     MG_RP2)
    hline(img, 12, 36, robe_bot + 1, MG_RP3)
    hline(img, 11, 37, robe_bot + 1, K)
    # Outline
    hline(img, 14, 35, robe_top - 1, K)
    vline(img, 14, robe_top, robe_bot, K)
    vline(img, 35, robe_top, robe_bot, K)

    # ── ROBE SLEEVES ──────────────────────────────────────────────────────────
    # Left sleeve: robe arm reaching down left at x=9..15
    sl_top = robe_top + 2
    sl_bot = sl_top + 8
    rect(img, 10, sl_top, 15, sl_bot, MG_RP1)
    vline(img, 11, sl_top + 1, sl_bot - 1, MG_RP0)
    hline(img, 9, 15, sl_top - 1, K)
    hline(img, 9, 15, sl_bot + 1, K)
    vline(img, 9, sl_top, sl_bot, K)
    # Right sleeve: raised/outstretched at x=34..41
    sr_top = robe_top
    sr_bot = sr_top + 9
    rect(img, 34, sr_top, 41, sr_bot, MG_RP1)
    vline(img, 35, sr_top + 1, sr_bot - 1, MG_RP0)
    vline(img, 40, sr_top + 1, sr_bot - 1, MG_RP2)
    hline(img, 33, 42, sr_top - 1, K)
    hline(img, 33, 42, sr_bot + 1, K)
    vline(img, 42, sr_top, sr_bot, K)

    # ── FEET (hovering — just show hem, no feet on ground) ────────────────────
    # Robe hem bottom shadow line is at robe_bot+1 above

    return img


def mage_frames():
    # Idle: gentle float cycle
    idle = [
        build_mage(float_dy=0,  orb_glow=False),
        build_mage(float_dy=-1, orb_glow=True),
        build_mage(float_dy=-2, orb_glow=False),
        build_mage(float_dy=-1, orb_glow=True),
    ]
    # Walk: same float but bigger oscillation
    walk = [
        build_mage(float_dy=0,  orb_glow=True),
        build_mage(float_dy=-2, orb_glow=False),
        build_mage(float_dy=-3, orb_glow=True),
        build_mage(float_dy=-1, orb_glow=False),
    ]
    return idle + walk


# ══════════════════════════════════════════════════════════════════════════════
# ENEMY_CHARGER  —  bull/armored ram, wide front, horns, heavy stomp walk
# ══════════════════════════════════════════════════════════════════════════════

CH_HD0 = (200, 130,  60)   # hide highlight
CH_HD1 = (160,  90,  35)   # hide base
CH_HD2 = (110,  55,  15)   # hide shadow
CH_HD3 = ( 65,  28,   5)   # hide deep
CH_AR0 = (190, 140,  70)   # armor plate highlight
CH_AR1 = (140,  95,  35)   # armor plate
CH_AR2 = ( 90,  55,  12)   # armor shadow
CH_HR0 = (240, 235, 220)   # horn highlight
CH_HR1 = (210, 185, 120)   # horn base
CH_HR2 = (150, 120,  60)   # horn shadow
CH_EY  = ( 30,  12,   5)   # eye
CH_BL  = ( 40,  30,  20)   # hoof
CH_NS  = (180, 100,  50)   # nostril
CH_SP  = (230, 200, 150)   # snort puff


def build_charger(head_dy=0, leg_left_dy=0, leg_right_dy=0):
    img = new_frame()

    # ── TAIL (rear, x=37..41, y=20..32) ──────────────────────────────────────
    vline(img, 38, 22, 30, CH_HD2)
    vline(img, 39, 22, 30, CH_HD1)
    hline(img, 38, 42, 31, CH_HD2)
    hline(img, 38, 42, 32, CH_HD3)
    vline(img, 37, 22, 32, K)
    vline(img, 43, 28, 32, K)

    # ── BODY (wide rectangle, low) x=10..40, y=20..34 ────────────────────────
    bx0, bx1 = 9, 40
    by0, by1 = 19, 34
    rect(img, bx0, by0, bx1, by1, CH_HD1)
    hline(img, bx0 + 1, bx1 - 1, by0, CH_HD0)
    hline(img, bx0 + 1, bx1 - 1, by0 + 1, CH_HD0)
    hline(img, bx0 + 1, bx1 - 1, by1, CH_HD2)
    hline(img, bx0 + 1, bx1 - 1, by1 - 1, CH_HD2)
    vline(img, bx0, by0, by1, CH_HD2)
    vline(img, bx1, by0, by1, CH_HD2)
    # Body outline
    hline(img, bx0 - 1, bx1 + 1, by0 - 1, K)
    hline(img, bx0 - 1, bx1 + 1, by1 + 1, K)
    vline(img, bx0 - 1, by0, by1, K)
    vline(img, bx1 + 1, by0, by1, K)

    # ── ARMOR PLATE on back (x=18..38, y=19..26) ─────────────────────────────
    rect(img, 18, 19, 38, 26, CH_AR1)
    hline(img, 19, 37, 19, CH_AR0)
    hline(img, 19, 37, 20, CH_AR0)
    hline(img, 19, 37, 26, CH_AR2)
    vline(img, 18, 19, 26, CH_AR2)
    vline(img, 38, 19, 26, CH_AR2)
    # rivets
    for rx in [21, 27, 33]:
        px(img, rx, 22, K)
        px(img, rx, 23, CH_AR0)
    hline(img, 17, 39, 18, K)
    hline(img, 17, 39, 27, K)
    vline(img, 17, 19, 26, K)
    vline(img, 39, 19, 26, K)

    # ── HEAD (wide, low, pushed forward left side) x=3..18, y=18+head_dy..30+head_dy
    hx0, hx1 = 3, 19
    hy0 = 18 + head_dy
    hy1 = 30 + head_dy
    rect(img, hx0, hy0, hx1, hy1, CH_HD1)
    hline(img, hx0 + 1, hx1 - 1, hy0, CH_HD0)
    hline(img, hx0 + 1, hx1 - 1, hy0 + 1, CH_HD0)
    vline(img, hx0, hy0, hy1, CH_HD2)
    hline(img, hx0 + 1, hx1 - 1, hy1, CH_HD3)
    hline(img, hx0 + 1, hx1 - 1, hy1 - 1, CH_HD2)
    # Snout (front of head): x=3..6, y=hy0+3..hy1-2
    rect(img, 2, hy0 + 3, 6, hy1 - 3, CH_HD2)
    hline(img, 2, 6, hy0 + 2, K)
    hline(img, 2, 6, hy1 - 2, K)
    vline(img, 1, hy0 + 3, hy1 - 3, K)
    # Nostrils
    px(img, 2, hy0 + 4, K)
    px(img, 2, hy0 + 5, CH_NS)
    px(img, 4, hy1 - 4, K)
    px(img, 4, hy1 - 5, CH_NS)
    # Eye
    px(img, 15, hy0 + 3, K)
    px(img, 16, hy0 + 3, CH_EY)
    px(img, 15, hy0 + 2, K); px(img, 16, hy0 + 2, K)
    # Head outline
    hline(img, hx0 - 1, hx1 + 1, hy0 - 1, K)
    hline(img, hx0 - 1, hx1 + 1, hy1 + 1, K)
    vline(img, hx0 - 1, hy0, hy1, K)
    vline(img, hx1 + 1, hy0, hy1, K)

    # ── HORNS (on top of head, curved upward) ─────────────────────────────────
    # Left horn
    hh = hy0 - 1
    px(img,  7, hh,     CH_HR1); px(img,  6, hh - 1, CH_HR1)
    px(img,  5, hh - 2, CH_HR0); px(img,  4, hh - 3, CH_HR1)
    px(img,  3, hh - 4, CH_HR2); px(img,  2, hh - 5, K)
    px(img,  6, hh,     K);      px(img,  5, hh - 1, K)
    px(img,  4, hh - 2, K);      px(img,  3, hh - 3, K)
    # Right horn
    px(img, 13, hh,     CH_HR1); px(img, 14, hh - 1, CH_HR1)
    px(img, 15, hh - 2, CH_HR0); px(img, 16, hh - 3, CH_HR1)
    px(img, 17, hh - 4, CH_HR2); px(img, 18, hh - 5, K)
    px(img, 14, hh,     K);      px(img, 15, hh - 1, K)
    px(img, 16, hh - 2, K);      px(img, 17, hh - 3, K)

    # ── SNORT PUFF (front of head) ────────────────────────────────────────────
    # Always show faint breath
    px(img, 0, hy0 + 3, CH_SP)
    px(img, 0, hy0 + 5, CH_SP)

    # ── LEGS (4 legs, pairs) ──────────────────────────────────────────────────
    # Front pair x=11..14 and x=16..19, rear pair x=29..32 and x=34..37
    def draw_leg(lx, dy, front=True):
        leg_top = by1 + 1
        lt = leg_top + dy
        # Upper leg
        rect(img, lx, lt, lx + 3, lt + 5, CH_HD1)
        vline(img, lx + 1, lt, lt + 5, CH_HD0)
        vline(img, lx + 3, lt, lt + 5, CH_HD2)
        # Lower leg / hoof
        rect(img, lx, lt + 6, lx + 3, lt + 9, CH_HD2)
        hline(img, lx, lx + 3, lt + 9, CH_BL)
        hline(img, lx, lx + 3, lt + 10, CH_BL)
        # outline
        hline(img, lx - 1, lx + 4, lt - 1, K)
        vline(img, lx - 1, lt, lt + 10, K)
        vline(img, lx + 4, lt, lt + 10, K)
        hline(img, lx - 1, lx + 4, lt + 11, K)

    draw_leg(10, leg_left_dy,  front=True)
    draw_leg(16, leg_right_dy, front=True)
    draw_leg(29, leg_right_dy, front=False)
    draw_leg(35, leg_left_dy,  front=False)

    return img


def charger_frames():
    idle = [
        build_charger(head_dy=0, leg_left_dy=0, leg_right_dy=0),
        build_charger(head_dy=-1, leg_left_dy=0, leg_right_dy=0),  # head bob
        build_charger(head_dy=0, leg_left_dy=0, leg_right_dy=0),
        build_charger(head_dy=-1, leg_left_dy=0, leg_right_dy=0),
    ]
    walk = [
        build_charger(head_dy=0,  leg_left_dy=-3, leg_right_dy=0),
        build_charger(head_dy=-1, leg_left_dy=-1, leg_right_dy=-1),
        build_charger(head_dy=0,  leg_left_dy=0, leg_right_dy=-3),
        build_charger(head_dy=-1, leg_left_dy=-1, leg_right_dy=-1),
    ]
    return idle + walk


# ══════════════════════════════════════════════════════════════════════════════
# ENEMY_BOMBER  —  small goblin, ragged clothes, big bomb, lit fuse
# ══════════════════════════════════════════════════════════════════════════════

BM_SK0 = ( 80, 160,  50)   # goblin skin highlight (green)
BM_SK1 = ( 55, 125,  30)   # goblin skin base
BM_SK2 = ( 30,  85,  12)   # goblin skin shadow
BM_SK3 = ( 14,  55,   4)   # goblin skin deep
BM_EY  = (240, 215,  40)   # yellow eye
BM_EP  = (  8,   4,   2)   # pupil
BM_CL0 = (160,  90,  40)   # clothes highlight (ragged brown)
BM_CL1 = (115,  60,  20)   # clothes base
BM_CL2 = ( 70,  32,   8)   # clothes shadow
BM_BM0 = ( 30,  30,  35)   # bomb highlight
BM_BM1 = ( 18,  18,  22)   # bomb base
BM_BM2 = (  8,   8,  12)   # bomb shadow
BM_FS0 = (255, 180,  30)   # fuse glow orange
BM_FS1 = (220,  90,  10)   # fuse base
BM_FS2 = (150,  50,   4)   # fuse shadow
BM_TE  = (200, 160,  80)   # teeth


def build_bomber(leg_left_dy=0, leg_right_dy=0, body_dy=0, fuse_bright=False):
    img = new_frame()
    bd = body_dy

    # ── BOMB (carried in front, x=5..15, y=25+bd..35+bd) ─────────────────────
    bx, by = 10, 31 + bd
    circle(img, bx, by, 5, 5, BM_BM2)
    circle(img, bx, by, 4, 4, BM_BM1)
    circle(img, bx, by, 2, 2, BM_BM0)
    px(img, bx - 2, by - 2, BM_BM0)
    # Bomb outline ring
    hline(img, bx - 5, bx + 5, by - 5, K)
    hline(img, bx - 5, bx + 5, by + 5, K)
    vline(img, bx - 5, by - 5, by + 5, K)
    vline(img, bx + 5, by - 5, by + 5, K)
    # Fuse cord (squiggly from top of bomb)
    px(img, bx, by - 5, K)
    px(img, bx, by - 6, BM_FS2)
    px(img, bx + 1, by - 7, BM_FS1)
    px(img, bx, by - 8, BM_FS1)
    px(img, bx + 1, by - 9, BM_FS0 if fuse_bright else BM_FS1)
    # Fuse spark at tip
    if fuse_bright:
        px(img, bx + 1, by - 10, BM_FS0)
        px(img, bx,     by - 10, BM_FS0)
        px(img, bx + 2, by - 9,  BM_FS0)

    # ── HEAD (x=19..31, y=5+bd..16+bd) ──────────────────────────────────────
    head_top = 5 + bd
    head_bot = 16 + bd
    rect(img, 19, head_top, 31, head_bot, BM_SK1)
    hline(img, 20, 30, head_top, BM_SK0)
    hline(img, 20, 30, head_top + 1, BM_SK0)
    vline(img, 19, head_top, head_bot, BM_SK2)
    vline(img, 31, head_top, head_bot, BM_SK2)
    hline(img, 19, 31, head_bot, BM_SK3)
    # Big pointy ears
    px(img, 18, head_top + 2, BM_SK1)
    px(img, 17, head_top + 1, BM_SK2)
    px(img, 16, head_top,     K)
    px(img, 32, head_top + 2, BM_SK1)
    px(img, 33, head_top + 1, BM_SK2)
    px(img, 34, head_top,     K)
    # Eyes — large yellow
    ey = head_top + 4
    rect(img, 21, ey, 23, ey + 1, BM_EY)
    px(img, 22, ey, BM_EP)
    rect(img, 27, ey, 29, ey + 1, BM_EY)
    px(img, 28, ey, BM_EP)
    hline(img, 20, 24, ey - 1, K)
    hline(img, 26, 30, ey - 1, K)
    # Huge grin
    hline(img, 21, 29, head_bot - 2, K)
    hline(img, 21, 29, head_bot - 1, BM_SK3)
    # Teeth
    px(img, 22, head_bot - 2, BM_TE)
    px(img, 24, head_bot - 2, BM_TE)
    px(img, 26, head_bot - 2, BM_TE)
    px(img, 28, head_bot - 2, BM_TE)
    # Nose (big bulbous)
    hline(img, 23, 26, ey + 3, BM_SK2)
    px(img, 22, ey + 3, K)
    px(img, 27, ey + 3, K)
    # Head outline
    hline(img, 18, 32, head_top - 1, K)
    hline(img, 18, 32, head_bot + 1, K)
    vline(img, 18, head_top, head_bot, K)
    vline(img, 32, head_top, head_bot, K)

    # ── BODY (ragged shirt+pants, x=17..33, y=17+bd..30+bd) ─────────────────
    torso_top = head_bot + 1
    torso_bot = torso_top + 10
    rect(img, 18, torso_top, 32, torso_bot, BM_CL1)
    vline(img, 19, torso_top + 1, torso_bot - 1, BM_CL0)
    vline(img, 31, torso_top + 1, torso_bot - 1, BM_CL2)
    # Ragged bottom hem (uneven)
    for rx in range(18, 33, 2):
        px(img, rx, torso_bot + 1, BM_CL2)
    # Left arm (holding bomb side): x=12..18
    rect(img, 13, torso_top, 18, torso_top + 9, BM_SK1)
    vline(img, 14, torso_top + 1, torso_top + 8, BM_SK0)
    hline(img, 12, 18, torso_top - 1, K)
    hline(img, 12, 18, torso_top + 10, K)
    vline(img, 12, torso_top, torso_top + 9, K)
    # Right arm (raised): x=32..38
    rect(img, 32, torso_top - 2, 37, torso_top + 6, BM_SK1)
    vline(img, 33, torso_top - 1, torso_top + 5, BM_SK0)
    vline(img, 36, torso_top - 1, torso_top + 5, BM_SK2)
    hline(img, 31, 38, torso_top - 3, K)
    hline(img, 31, 38, torso_top + 7, K)
    vline(img, 31, torso_top - 2, torso_top + 6, K)
    vline(img, 38, torso_top - 2, torso_top + 6, K)
    # Body outline
    hline(img, 17, 33, torso_top - 1, K)
    hline(img, 17, 33, torso_bot + 1, K)
    vline(img, 17, torso_top, torso_bot, K)
    vline(img, 33, torso_top, torso_bot, K)

    # ── LEGS (short stumpy, x=19..24 left, x=26..31 right) ──────────────────
    leg_top = torso_bot + 2
    def draw_bleg(lx, dy):
        lt = leg_top + dy
        rect(img, lx, lt, lx + 4, lt + 5, BM_CL2)
        vline(img, lx + 1, lt, lt + 5, BM_CL1)
        # boot
        rect(img, lx - 1, lt + 6, lx + 5, lt + 8, K)
        rect(img, lx,     lt + 6, lx + 4, lt + 7, BM_SK3)
        hline(img, lx - 1, lx + 5, lt - 1, K)
        hline(img, lx - 1, lx + 5, lt + 9, K)
        vline(img, lx - 1, lt, lt + 8, K)
        vline(img, lx + 5, lt, lt + 8, K)

    draw_bleg(19, leg_left_dy)
    draw_bleg(26, leg_right_dy)

    return img


def bomber_frames():
    idle = [
        build_bomber(0, 0, 0,  fuse_bright=False),
        build_bomber(0, 0, -1, fuse_bright=True),
        build_bomber(0, 0, 0,  fuse_bright=False),
        build_bomber(0, 0, -1, fuse_bright=True),
    ]
    walk = [
        build_bomber(-3,  2, -1, fuse_bright=True),
        build_bomber(-1,  0,  0, fuse_bright=False),
        build_bomber( 2, -3, -1, fuse_bright=True),
        build_bomber( 0, -1,  0, fuse_bright=False),
    ]
    return idle + walk


# ══════════════════════════════════════════════════════════════════════════════
# ENEMY_BOSS  —  64×64 dark knight/demon, ~58px tall, crescent axe, wide wings
# ══════════════════════════════════════════════════════════════════════════════

BW, BH = 64, 64   # boss-only frame size

BS_AR0 = (100, 108, 128)   # armor highlight
BS_AR1 = ( 55,  60,  78)   # armor base
BS_AR2 = ( 28,  32,  50)   # armor shadow
BS_AR3 = ( 12,  12,  24)   # armor deep
BS_AR4 = (  5,   5,  12)   # armor darkest
BS_EY  = (255,  30,  20)   # glowing red eye
BS_EG  = (160,   8,   4)   # eye glow dim
BS_AX0 = (215, 225, 240)   # axe blade highlight
BS_AX1 = (148, 158, 178)   # axe blade mid
BS_AX2 = ( 80,  90, 115)   # axe blade shadow
BS_AX3 = ( 38,  44,  62)   # axe dark
BS_HN0 = ( 72,  78,  98)   # horn highlight
BS_HN1 = ( 42,  46,  68)   # horn base
BS_HN2 = ( 18,  20,  36)   # horn shadow
BS_WG0 = ( 70,  22,  22)   # wing edge highlight
BS_WG1 = ( 45,  12,  12)   # wing membrane lit
BS_WG2 = ( 22,   6,   6)   # wing membrane base
BS_WG3 = ( 10,   2,   2)   # wing deep shadow


def _bpx(img, x, y, c):
    if 0 <= x < BW and 0 <= y < BH:
        img.putpixel((x, y), c)

def _bhline(img, x0, x1, y, c):
    for x in range(x0, x1 + 1):
        _bpx(img, x, y, c)

def _bvline(img, x, y0, y1, c):
    for y in range(y0, y1 + 1):
        _bpx(img, x, y, c)

def _brect(img, x0, y0, x1, y1, c):
    for y in range(y0, y1 + 1):
        _bhline(img, x0, x1, y, c)

def _bcircle(img, cx, cy, rx, ry, c):
    for dy in range(-ry, ry + 1):
        for dx in range(-rx, rx + 1):
            if (dx / max(rx, 1)) ** 2 + (dy / max(ry, 1)) ** 2 <= 1.0:
                _bpx(img, cx + dx, cy + dy, c)

def new_boss_frame():
    return Image.new("RGB", (BW, BH), _)

def save_boss_sheet(frames, name):
    sheet = Image.new("RGB", (BW * 8, BH), _)
    for i, f in enumerate(frames):
        sheet.paste(f, (i * BW, 0))
    preview = sheet.resize((BW * 8 * 4, BH * 4), Image.NEAREST)
    sheet.save(f"{OUT}/{name}_sheet.png")
    preview.save(f"{OUT}/{name}_preview.png")
    print(f"Saved {name}_sheet.png ({BW*8}x{BH})  +  {name}_preview.png ({BW*8*4}x{BH*4})")


def build_boss(leg_left_dy=0, leg_right_dy=0, body_dy=0, eye_bright=True):
    img = new_boss_frame()
    bd = body_dy

    # Layout anchors (all coordinates in 64x64 space)
    # Crown of helmet horns: ~y=2
    # Head top: ~y=6+bd, head bot: ~y=17+bd
    # Torso top: ~y=18+bd, torso bot: ~y=36+bd
    # Belt: ~y=37+bd..39+bd
    # Legs: ~y=40+bd..58+bd (boots end at 58)
    # Wings span: y=10+bd..38+bd, x=0..63

    # ── WINGS (behind body, dark membranous, full width) ─────────────────────
    # Left wing: x=0..19, y=10+bd..40+bd
    # Wing shape: wider at top, tapers to tip at bottom-left
    wt = 10 + bd
    wb = 40 + bd
    # Fill main membrane block
    _brect(img,  1, wt,     18, wb,     BS_WG3)
    _brect(img,  2, wt + 1, 16, wb - 1, BS_WG2)
    # Membrane vein lines (radiating from shoulder area near x=19)
    for i, wy in enumerate(range(wt + 1, wb, 4)):
        tip_x = max(1, 16 - i * 2)
        _bhline(img, tip_x, 16, wy, BS_WG1)
    # Leading edge highlight
    _bvline(img, 1, wt + 1, wb - 1, BS_WG0)
    # Wing tip points (lower-left corner jagged)
    _bpx(img, 0, wb - 2, BS_WG2)
    _bpx(img, 0, wb - 4, BS_WG2)
    # Wing outline
    _bvline(img, 0, wt, wb, K)
    _bhline(img, 0, 19, wt - 1, K)
    _bhline(img, 0, 19, wb + 1, K)

    # Right wing: x=44..63, mirror
    _brect(img, 45, wt,     62, wb,     BS_WG3)
    _brect(img, 47, wt + 1, 61, wb - 1, BS_WG2)
    for i, wy in enumerate(range(wt + 1, wb, 4)):
        tip_x = min(62, 47 + i * 2)
        _bhline(img, 47, tip_x, wy, BS_WG1)
    _bvline(img, 62, wt + 1, wb - 1, BS_WG0)
    _bpx(img, 63, wb - 2, BS_WG2)
    _bpx(img, 63, wb - 4, BS_WG2)
    _bvline(img, 63, wt, wb, K)
    _bhline(img, 44, 63, wt - 1, K)
    _bhline(img, 44, 63, wb + 1, K)

    # ── AXE (left side, large crescent, handle runs full height) ─────────────
    # Handle: x=9..11, y=4+bd..54+bd
    ax_hx = 10   # handle center x
    _bvline(img, ax_hx - 1, 4 + bd, 54 + bd, BS_AX1)
    _bvline(img, ax_hx,     4 + bd, 54 + bd, BS_AX0)
    _bvline(img, ax_hx + 1, 4 + bd, 54 + bd, BS_AX2)
    _bvline(img, ax_hx - 2, 4 + bd, 54 + bd, K)
    _bvline(img, ax_hx + 2, 4 + bd, 54 + bd, K)
    # Handle end cap (bottom pommel)
    _brect(img, ax_hx - 3, 53 + bd, ax_hx + 3, 56 + bd, BS_AX2)
    _bhline(img, ax_hx - 3, ax_hx + 3, 53 + bd, BS_AX0)
    _bhline(img, ax_hx - 4, ax_hx + 4, 52 + bd, K)
    _bhline(img, ax_hx - 4, ax_hx + 4, 57 + bd, K)
    _bvline(img, ax_hx - 4, 53 + bd, 56 + bd, K)
    _bvline(img, ax_hx + 4, 53 + bd, 56 + bd, K)

    # Crescent blade: upper arc x=1..14, y=4+bd..30+bd
    # Outer crescent: large filled arc (left-opening crescent)
    blade_t = 4 + bd
    blade_b = 30 + bd
    blade_cx = 14   # right edge (where handle meets)
    blade_cy = (blade_t + blade_b) // 2
    blade_ry = (blade_b - blade_t) // 2
    # Outer filled half-ellipse (left side)
    for dy in range(-blade_ry, blade_ry + 1):
        cy = blade_cy + dy
        # outer radius: 13px
        frac = 1.0 - (dy / blade_ry) ** 2
        outer_x = int(13 * frac ** 0.5)
        # inner radius: 7px (cutout to make crescent)
        inner_x = int(7 * frac ** 0.5)
        lx = blade_cx - outer_x
        rx_outer = blade_cx - 1
        rx_inner = blade_cx - inner_x - 1
        if lx <= rx_inner:
            # outer crescent fill
            _bhline(img, max(0, lx), rx_inner, cy, BS_AX2)
        if rx_inner + 1 <= rx_outer:
            _bhline(img, rx_inner + 1, rx_outer, cy, BS_AX1)
        # highlight on leading (left) edge
        _bpx(img, max(0, lx), cy, BS_AX0)
        _bpx(img, max(0, lx + 1), cy, BS_AX1)
        # shadow near handle
        _bpx(img, rx_outer, cy, BS_AX3)
    # Blade outline
    for dy in range(-blade_ry - 1, blade_ry + 2):
        cy = blade_cy + dy
        frac = max(0.0, 1.0 - (dy / (blade_ry + 1)) ** 2)
        outer_x = int(14 * frac ** 0.5)
        lx = blade_cx - outer_x
        _bpx(img, max(0, lx - 1), cy, K)
    _bhline(img, 1, blade_cx, blade_t - 1, K)
    _bhline(img, 1, blade_cx, blade_b + 1, K)
    # Top spike on axe (crescent upper tip)
    _bpx(img, blade_cx - 1, blade_t - 2, BS_AX0)
    _bpx(img, blade_cx - 2, blade_t - 3, BS_AX1)
    _bpx(img, blade_cx - 1, blade_t - 3, K)
    _bpx(img, blade_cx - 2, blade_t - 4, K)
    # Bottom spike on axe (crescent lower tip)
    _bpx(img, blade_cx - 1, blade_b + 2, BS_AX0)
    _bpx(img, blade_cx - 2, blade_b + 3, BS_AX1)
    _bpx(img, blade_cx - 1, blade_b + 3, K)
    _bpx(img, blade_cx - 2, blade_b + 4, K)

    # ── BODY TORSO (x=20..43, y=18+bd..36+bd) ────────────────────────────────
    torso_top = 18 + bd
    torso_bot = 36 + bd
    _brect(img, 20, torso_top, 43, torso_bot, BS_AR1)
    # Left highlight column
    _bvline(img, 21, torso_top + 1, torso_bot - 1, BS_AR0)
    _bvline(img, 22, torso_top + 1, torso_bot - 1, BS_AR0)
    # Right shadow columns
    _bvline(img, 42, torso_top + 1, torso_bot - 1, BS_AR2)
    _bvline(img, 43, torso_top + 1, torso_bot - 1, BS_AR3)
    # Chest plate (central raised panel)
    _brect(img, 25, torso_top + 2, 38, torso_top + 12, BS_AR2)
    _brect(img, 26, torso_top + 3, 37, torso_top + 11, BS_AR1)
    _bhline(img, 26, 37, torso_top + 3, BS_AR0)
    _bvline(img, 26, torso_top + 3, torso_top + 11, BS_AR0)
    # Ribbed armor lines on chest
    for ry2 in range(torso_top + 5, torso_top + 12, 3):
        _bhline(img, 27, 36, ry2, BS_AR2)
    # Torso outline
    _bhline(img, 19, 44, torso_top - 1, K)
    _bhline(img, 19, 44, torso_bot + 1, K)
    _bvline(img, 19, torso_top, torso_bot, K)
    _bvline(img, 44, torso_top, torso_bot, K)

    # ── PAULDRONS (large spiked shoulder armor) ────────────────────────────────
    # Left pauldron: x=14..22, y=torso_top-4..torso_top+8
    _brect(img, 14, torso_top - 4, 22, torso_top + 8, BS_AR1)
    _bhline(img, 14, 22, torso_top - 4, BS_AR0)
    _bvline(img, 14, torso_top - 4, torso_top + 8, BS_AR0)
    _bvline(img, 22, torso_top - 4, torso_top + 8, BS_AR2)
    # Pauldron spike
    _bpx(img, 16, torso_top - 5, BS_AR1)
    _bpx(img, 17, torso_top - 6, BS_AR0)
    _bpx(img, 16, torso_top - 6, K)
    _bpx(img, 17, torso_top - 7, K)
    # Outline
    _bhline(img, 13, 23, torso_top - 5, K)
    _bhline(img, 13, 23, torso_top + 9, K)
    _bvline(img, 13, torso_top - 4, torso_top + 8, K)
    _bvline(img, 23, torso_top - 4, torso_top + 8, K)

    # Right pauldron: x=41..49, mirror
    _brect(img, 41, torso_top - 4, 49, torso_top + 8, BS_AR1)
    _bhline(img, 41, 49, torso_top - 4, BS_AR0)
    _bvline(img, 41, torso_top - 4, torso_top + 8, BS_AR0)
    _bvline(img, 49, torso_top - 4, torso_top + 8, BS_AR2)
    _bpx(img, 47, torso_top - 5, BS_AR1)
    _bpx(img, 46, torso_top - 6, BS_AR0)
    _bpx(img, 47, torso_top - 6, K)
    _bpx(img, 46, torso_top - 7, K)
    _bhline(img, 40, 50, torso_top - 5, K)
    _bhline(img, 40, 50, torso_top + 9, K)
    _bvline(img, 40, torso_top - 4, torso_top + 8, K)
    _bvline(img, 50, torso_top - 4, torso_top + 8, K)

    # ── ARMS ──────────────────────────────────────────────────────────────────
    # Left arm (holding axe, x=14..19, y=torso_top+8..torso_top+22)
    _brect(img, 14, torso_top + 8, 19, torso_top + 22, BS_AR1)
    _bvline(img, 15, torso_top + 9, torso_top + 21, BS_AR0)
    _bvline(img, 19, torso_top + 9, torso_top + 21, BS_AR2)
    _bhline(img, 13, 20, torso_top + 7, K)
    _bhline(img, 13, 20, torso_top + 23, K)
    _bvline(img, 13, torso_top + 8, torso_top + 22, K)
    _bvline(img, 20, torso_top + 8, torso_top + 22, K)
    # Gauntlet (left hand)
    _brect(img, 13, torso_top + 22, 20, torso_top + 26, BS_AR2)
    _bhline(img, 13, 20, torso_top + 22, BS_AR0)
    _bhline(img, 12, 21, torso_top + 21, K)
    _bhline(img, 12, 21, torso_top + 27, K)
    _bvline(img, 12, torso_top + 22, torso_top + 26, K)
    _bvline(img, 21, torso_top + 22, torso_top + 26, K)

    # Right arm (raised/menacing, x=44..50, y=torso_top+6..torso_top+20)
    _brect(img, 44, torso_top + 6, 50, torso_top + 20, BS_AR1)
    _bvline(img, 45, torso_top + 7, torso_top + 19, BS_AR0)
    _bvline(img, 50, torso_top + 7, torso_top + 19, BS_AR2)
    _bhline(img, 43, 51, torso_top + 5, K)
    _bhline(img, 43, 51, torso_top + 21, K)
    _bvline(img, 43, torso_top + 6, torso_top + 20, K)
    _bvline(img, 51, torso_top + 6, torso_top + 20, K)
    # Gauntlet (right hand, with claw points)
    _brect(img, 43, torso_top + 20, 51, torso_top + 24, BS_AR2)
    _bhline(img, 43, 51, torso_top + 20, BS_AR0)
    # Claw tips
    for cx2 in [44, 46, 48, 50]:
        _bpx(img, cx2, torso_top + 25, BS_AR3)
        _bpx(img, cx2, torso_top + 26, K)
    _bhline(img, 42, 52, torso_top + 19, K)
    _bhline(img, 42, 52, torso_top + 24, K)
    _bvline(img, 42, torso_top + 20, torso_top + 24, K)
    _bvline(img, 52, torso_top + 20, torso_top + 24, K)

    # ── HEAD (large helmeted, x=22..41, y=6+bd..17+bd) ───────────────────────
    head_top = 6 + bd
    head_bot = 17 + bd
    _brect(img, 22, head_top, 41, head_bot, BS_AR1)
    _bhline(img, 23, 40, head_top, BS_AR0)
    _bhline(img, 23, 40, head_top + 1, BS_AR0)
    _bvline(img, 22, head_top, head_bot, BS_AR0)
    _bvline(img, 41, head_top, head_bot, BS_AR2)
    _bhline(img, 22, 41, head_bot, BS_AR2)
    # Chin guard widens slightly
    _brect(img, 21, head_bot - 3, 42, head_bot, BS_AR2)
    _bhline(img, 21, 42, head_bot - 3, BS_AR1)
    _bhline(img, 20, 43, head_bot - 4, K)
    _bhline(img, 20, 43, head_bot + 1, K)
    _bvline(img, 20, head_bot - 3, head_bot, K)
    _bvline(img, 43, head_bot - 3, head_bot, K)
    # Helmet crest ridge (top center)
    _brect(img, 29, head_top - 2, 34, head_top, BS_AR0)
    _bhline(img, 28, 35, head_top - 3, K)
    _bvline(img, 28, head_top - 2, head_top, K)
    _bvline(img, 35, head_top - 2, head_top, K)
    # Visor slit (wide)
    ey = head_top + 5
    _brect(img, 24, ey, 39, ey + 2, K)
    # Glowing red eyes shining through visor
    eye_col = BS_EY if eye_bright else BS_EG
    _bhline(img, 26, 29, ey,     eye_col)
    _bhline(img, 26, 29, ey + 1, eye_col)
    _bhline(img, 34, 37, ey,     eye_col)
    _bhline(img, 34, 37, ey + 1, eye_col)
    # Nasal guard (center divider)
    _bvline(img, 31, head_top + 1, head_bot - 4, BS_AR2)
    _bvline(img, 32, head_top + 1, head_bot - 4, BS_AR0)
    # Helmet outline
    _bhline(img, 21, 42, head_top - 1, K)
    _bhline(img, 21, 42, head_bot + 1, K)
    _bvline(img, 21, head_top, head_bot, K)
    _bvline(img, 42, head_top, head_bot, K)

    # ── HORNS on helmet (large, curving outward) ───────────────────────────────
    # Left horn: base at x=23, y=head_top, curves up-left
    for i in range(7):
        hx2 = 23 - i
        hy2 = head_top - 1 - i
        _bpx(img, hx2,     hy2, BS_HN1)
        _bpx(img, hx2 - 1, hy2, K)
        _bpx(img, hx2,     hy2 - 1, K)
        if i < 3:
            _bpx(img, hx2 + 1, hy2, BS_HN0)
    _bpx(img, 23, head_top - 1, BS_HN0)
    _bpx(img, 17, head_top - 6, BS_HN2)
    # Right horn: base at x=40, curves up-right
    for i in range(7):
        hx2 = 40 + i
        hy2 = head_top - 1 - i
        _bpx(img, hx2,     hy2, BS_HN1)
        _bpx(img, hx2 + 1, hy2, K)
        _bpx(img, hx2,     hy2 - 1, K)
        if i < 3:
            _bpx(img, hx2 - 1, hy2, BS_HN0)
    _bpx(img, 40, head_top - 1, BS_HN0)
    _bpx(img, 46, head_top - 6, BS_HN2)

    # ── BELT / WAIST ARMOR ────────────────────────────────────────────────────
    belt_y = torso_bot + 1
    _brect(img, 20, belt_y, 43, belt_y + 3, BS_AR2)
    _bhline(img, 21, 42, belt_y, BS_AR0)
    # Belt buckle
    _brect(img, 29, belt_y, 34, belt_y + 3, K)
    _bpx(img, 31, belt_y + 1, BS_AR0)
    _bpx(img, 32, belt_y + 1, BS_AR0)
    _bhline(img, 19, 44, belt_y - 1, K)
    _bhline(img, 19, 44, belt_y + 4, K)

    # ── LEGS (heavy armored greaves, x=21..30 left, x=32..41 right) ──────────
    leg_top = belt_y + 5

    def draw_boss_leg(lx, dy):
        lt = leg_top + dy
        # Thigh armor (wide)
        _brect(img, lx, lt, lx + 7, lt + 8, BS_AR1)
        _bvline(img, lx + 1, lt + 1, lt + 7, BS_AR0)
        _bvline(img, lx + 6, lt + 1, lt + 7, BS_AR2)
        _bvline(img, lx + 7, lt + 1, lt + 7, BS_AR3)
        _bhline(img, lx, lx + 7, lt, BS_AR0)
        # Knee armor (raised)
        _brect(img, lx - 1, lt + 8, lx + 8, lt + 11, BS_AR2)
        _bhline(img, lx - 1, lx + 8, lt + 8, BS_AR0)
        # Lower greave
        _brect(img, lx, lt + 12, lx + 7, lt + 18, BS_AR2)
        _bvline(img, lx + 1, lt + 13, lt + 17, BS_AR1)
        _bvline(img, lx + 3, lt + 13, lt + 17, BS_AR3)  # center shin ridge
        _bvline(img, lx + 4, lt + 13, lt + 17, BS_AR0)
        # Heavy boot
        _brect(img, lx - 1, lt + 19, lx + 8, lt + 23, BS_AR3)
        _bhline(img, lx - 1, lx + 8, lt + 19, BS_AR1)
        _bhline(img, lx - 2, lx + 9, lt + 23, K)
        # Boot toe cap extended
        _brect(img, lx - 2, lt + 21, lx - 1, lt + 23, BS_AR4)
        # Outline
        _bhline(img, lx - 2, lx + 9, lt - 1, K)
        _bvline(img, lx - 2, lt, lt + 23, K)
        _bvline(img, lx + 9, lt, lt + 23, K)

    draw_boss_leg(21, leg_left_dy)
    draw_boss_leg(33, leg_right_dy)

    return img


def boss_frames():
    idle = [
        build_boss(0, 0, 0,  eye_bright=True),
        build_boss(0, 0, -1, eye_bright=True),
        build_boss(0, 0, 0,  eye_bright=False),
        build_boss(0, 0, -1, eye_bright=True),
    ]
    walk = [
        build_boss(-3,  2, -1, eye_bright=True),
        build_boss(-1,  0,  0, eye_bright=False),
        build_boss( 2, -3, -1, eye_bright=True),
        build_boss( 0, -1,  0, eye_bright=False),
    ]
    return idle + walk


# ══════════════════════════════════════════════════════════════════════════════
# Main — generate all sheets
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    save_sheet(mage_frames(),    "enemy_mage")
    save_sheet(charger_frames(), "enemy_charger")
    save_sheet(bomber_frames(),  "enemy_bomber")
    save_boss_sheet(boss_frames(), "enemy_boss")
    print("All done.")
