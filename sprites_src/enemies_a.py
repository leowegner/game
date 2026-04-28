"""
Enemy spritesheets — 48x48 pixel art, hand-crafted via drawing primitives.
Same style as player: dark outline K=(18,12,8), 3-4 shades per part,
magenta (255,0,255) transparent background.

Enemies: goblin, slime, bat, knight
Each: 8 frames (4 idle + 4 walk) → 384×48 horizontal spritesheet
"""
from PIL import Image
import os

W, H = 48, 48
OUT = "/home/leo/dev/game-1/sprites_src"

# ── Shared palette ────────────────────────────────────────────────────────────
MAG = (255,   0, 255)   # transparent / background
K   = ( 18,  12,   8)   # outline (universal dark)

# ── Drawing helpers ───────────────────────────────────────────────────────────

def new_frame():
    return Image.new("RGB", (W, H), MAG)

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
    """Filled rectangle with border outline."""
    rect(img, x0, y0, x1, y1, fill)
    hline(img, x0, x1, y0, border)
    hline(img, x0, x1, y1, border)
    vline(img, x0, y0, y1, border)
    vline(img, x1, y0, y1, border)

def ellipse(img, cx, cy, rx, ry, c):
    for dy in range(-ry, ry + 1):
        for dx in range(-rx, rx + 1):
            if (dx / rx) ** 2 + (dy / ry) ** 2 <= 1.0:
                px(img, cx + dx, cy + dy, c)

def save_sheet(frames, name):
    sheet = Image.new("RGB", (W * 8, H), MAG)
    for i, f in enumerate(frames):
        sheet.paste(f, (i * W, 0))
    preview = sheet.resize((W * 8 * 4, H * 4), Image.NEAREST)
    sheet.save(f"{OUT}/{name}_sheet.png")
    preview.save(f"{OUT}/{name}_preview.png")
    print(f"Saved {name}_sheet.png ({W*8}×{H})  +  {name}_preview.png ({W*8*4}×{H*4})")

# ═══════════════════════════════════════════════════════════════════════════════
#  GOBLIN
# ═══════════════════════════════════════════════════════════════════════════════
# Palette
GS0 = (160, 210,  90)   # skin highlight
GS1 = (110, 170,  50)   # skin base
GS2 = ( 65, 120,  25)   # skin shadow
GS3 = ( 30,  65,   8)   # skin deep
ER  = (210,  40,  30)   # beady red eye
LC0 = (160, 110,  55)   # loincloth highlight
LC1 = (110,  70,  25)   # loincloth base
LC2 = ( 65,  38,   8)   # loincloth shadow
CL0 = (220, 215, 195)   # claw highlight
CL1 = (160, 155, 135)   # claw mid

def build_goblin(body_dy=0, leg_dy_l=0, leg_dy_r=0):
    img = new_frame()

    # Goblin stands ~35px tall, centered around x=17..30
    # Body is hunched — head pushed forward
    base_y = 38   # feet y

    # -- HEAD (big, pushed forward/down for hunch) --
    head_cx = 21
    head_top = 8 + body_dy
    head_bot = 18 + body_dy
    # skull
    rect(img, head_cx-5, head_top, head_cx+5, head_bot, GS1)
    # highlight
    rect(img, head_cx-3, head_top, head_cx+1, head_top+2, GS0)
    # shadow sides
    vline(img, head_cx-5, head_top, head_bot, GS2)
    vline(img, head_cx+5, head_top, head_bot, GS2)
    hline(img, head_cx-5, head_cx+5, head_bot, GS3)
    # outline
    hline(img, head_cx-5, head_cx+5, head_top-1, K)
    hline(img, head_cx-5, head_cx+5, head_bot+1, K)
    vline(img, head_cx-6, head_top, head_bot, K)
    vline(img, head_cx+6, head_top, head_bot, K)

    # -- BIG POINTY EARS --
    # left ear: points further left and slightly up
    ear_y = head_top + 2
    # left ear triangle
    px(img, head_cx-7, ear_y,   GS1)
    px(img, head_cx-8, ear_y+1, GS1)
    px(img, head_cx-9, ear_y+2, GS2)
    px(img, head_cx-7, ear_y+1, GS2)
    px(img, head_cx-8, ear_y,   K)
    px(img, head_cx-9, ear_y+1, K)
    px(img, head_cx-10,ear_y+2, K)
    px(img, head_cx-8, ear_y+3, K)
    # right ear
    px(img, head_cx+7, ear_y,   GS1)
    px(img, head_cx+8, ear_y+1, GS1)
    px(img, head_cx+9, ear_y+2, GS2)
    px(img, head_cx+7, ear_y+1, GS2)
    px(img, head_cx+8, ear_y,   K)
    px(img, head_cx+9, ear_y+1, K)
    px(img, head_cx+10,ear_y+2, K)
    px(img, head_cx+8, ear_y+3, K)

    # -- EYES (beady red, close together) --
    ey = head_top + 5
    px(img, head_cx-2, ey, ER)
    px(img, head_cx+2, ey, ER)
    # brow dots
    px(img, head_cx-2, ey-1, K)
    px(img, head_cx+2, ey-1, K)

    # -- NOSE (pointy) --
    px(img, head_cx,   head_top+7, GS2)
    px(img, head_cx,   head_top+8, GS3)
    px(img, head_cx-1, head_top+8, GS3)

    # -- BODY (hunched, short torso) --
    torso_top = head_bot + 1
    torso_bot = torso_top + 7
    torso_cx  = 22   # shifted right from head (hunch lean)
    rect(img, torso_cx-4, torso_top, torso_cx+5, torso_bot, GS1)
    vline(img, torso_cx-3, torso_top, torso_bot, GS0)
    vline(img, torso_cx+4, torso_top, torso_bot, GS2)
    hline(img, torso_cx-4, torso_cx+5, torso_bot, GS3)
    hline(img, torso_cx-4, torso_cx+5, torso_top-1, K)
    hline(img, torso_cx-4, torso_cx+5, torso_bot+1, K)
    vline(img, torso_cx-5, torso_top, torso_bot, K)
    vline(img, torso_cx+6, torso_top, torso_bot, K)

    # -- LOINCLOTH --
    lc_top = torso_bot
    lc_bot = lc_top + 5
    rect(img, torso_cx-3, lc_top, torso_cx+4, lc_bot, LC1)
    hline(img, torso_cx-3, torso_cx+4, lc_top, LC0)
    hline(img, torso_cx-3, torso_cx+4, lc_bot, LC2)
    # ragged bottom edge
    px(img, torso_cx-3, lc_bot+1, LC2)
    px(img, torso_cx-1, lc_bot+1, LC2)
    px(img, torso_cx+1, lc_bot+1, LC2)
    px(img, torso_cx+3, lc_bot+1, LC2)
    hline(img, torso_cx-4, torso_cx+5, lc_top-1, K)
    hline(img, torso_cx-4, torso_cx+5, lc_bot+1, K)
    vline(img, torso_cx-4, lc_top, lc_bot, K)
    vline(img, torso_cx+5, lc_top, lc_bot, K)

    # -- ARMS with claws --
    arm_y = torso_top + 1
    # left arm
    rect(img, torso_cx-7, arm_y, torso_cx-5, arm_y+5, GS1)
    vline(img, torso_cx-6, arm_y, arm_y+5, GS0)
    vline(img, torso_cx-8, arm_y, arm_y+5, K)
    vline(img, torso_cx-4, arm_y, arm_y+5, K)
    hline(img, torso_cx-8, torso_cx-4, arm_y-1, K)
    # left claw
    px(img, torso_cx-8, arm_y+6, CL1)
    px(img, torso_cx-7, arm_y+7, CL0)
    px(img, torso_cx-6, arm_y+6, CL1)
    px(img, torso_cx-5, arm_y+7, CL0)
    px(img, torso_cx-8, arm_y+8, K)
    px(img, torso_cx-6, arm_y+8, K)
    # right arm
    rect(img, torso_cx+6, arm_y, torso_cx+8, arm_y+5, GS1)
    vline(img, torso_cx+7, arm_y, arm_y+5, GS0)
    vline(img, torso_cx+5, arm_y, arm_y+5, K)
    vline(img, torso_cx+9, arm_y, arm_y+5, K)
    hline(img, torso_cx+5, torso_cx+9, arm_y-1, K)
    # right claw
    px(img, torso_cx+7, arm_y+6, CL1)
    px(img, torso_cx+8, arm_y+7, CL0)
    px(img, torso_cx+6, arm_y+6, CL1)
    px(img, torso_cx+9, arm_y+7, CL0)
    px(img, torso_cx+7, arm_y+8, K)
    px(img, torso_cx+9, arm_y+8, K)

    # -- LEGS (short, stubby) --
    leg_top = lc_bot + 2
    def draw_goblin_leg(lx, dy):
        lt = leg_top + dy
        rect(img, lx, lt, lx+3, lt+4, GS1)
        vline(img, lx+1, lt, lt+4, GS0)
        vline(img, lx+3, lt, lt+4, GS2)
        # foot (flat, clawed)
        rect(img, lx-1, lt+5, lx+4, lt+6, GS2)
        px(img, lx-1, lt+7, K)
        px(img, lx+1, lt+7, K)
        px(img, lx+3, lt+7, K)
        hline(img, lx-1, lx+4, lt-1, K)
        vline(img, lx-2, lt, lt+6, K)
        vline(img, lx+5, lt, lt+6, K)
        hline(img, lx-1, lx+4, lt+7, K)

    draw_goblin_leg(torso_cx-4, leg_dy_l)
    draw_goblin_leg(torso_cx+1, leg_dy_r)

    return img


goblin_idle = [
    build_goblin(0,  0,  0),
    build_goblin(-1, 0,  0),
    build_goblin(0,  0,  0),
    build_goblin(1,  0,  0),
]
goblin_walk = [
    build_goblin(-1, -2,  2),
    build_goblin(0,  -1,  1),
    build_goblin(-1,  2, -2),
    build_goblin(0,   1, -1),
]
save_sheet(goblin_idle + goblin_walk, "enemy_goblin")


# ═══════════════════════════════════════════════════════════════════════════════
#  SLIME
# ═══════════════════════════════════════════════════════════════════════════════
SL0 = (150, 255, 100)   # slime highlight
SL1 = ( 60, 195,  50)   # slime base
SL2 = ( 20, 130,  25)   # slime shadow
SL3 = (  5,  75,  10)   # slime deep
SE  = ( 10,  30,  10)   # eye dot

def build_slime(squish=0, lean=0):
    """
    squish: 0=normal, positive=squished down (wider, shorter)
    lean: -1 left, 0 center, 1 right (for walk)
    """
    img = new_frame()
    cx = 24 + lean
    # Body height: 22 normally, squish reduces height and adds width
    bh = 22 - squish * 2
    bw = 14 + squish * 2
    top = 20 + squish
    bot = top + bh
    # main blob body (ellipse approximated via pixel rows)
    ry = bh // 2
    rx = bw // 2
    cy = top + ry
    ellipse(img, cx, cy, rx, ry, SL1)
    # highlight top-left quadrant
    ellipse(img, cx - rx//3, cy - ry//3, max(1, rx//2), max(1, ry//2), SL0)
    # shadow bottom
    for dy in range(0, ry + 1):
        frac = dy / ry
        if frac > 0.4:
            x_span = int(rx * (1 - (frac - 0.4) / 0.6) ** 0.5)
            if x_span > 0:
                hline(img, cx - x_span, cx + x_span, cy + dy, SL2)
    # deep shadow at very bottom
    for dy in range(int(ry * 0.7), ry + 1):
        frac = dy / ry
        x_span = int(rx * (1 - frac ** 2) ** 0.5) if frac < 1 else 0
        if x_span > 0:
            hline(img, cx - x_span + 1, cx + x_span - 1, cy + dy, SL3)
    # outline
    for dy in range(-ry, ry + 1):
        x_span = int(rx * (1 - (dy / ry) ** 2) ** 0.5)
        if x_span >= 0:
            px(img, cx - x_span - 1, cy + dy, K)
            px(img, cx + x_span + 1, cy + dy, K)
    for dx in range(-rx, rx + 1):
        y_span = int(ry * (1 - (dx / rx) ** 2) ** 0.5)
        if y_span >= 0:
            px(img, cx + dx, cy - y_span - 1, K)
            px(img, cx + dx, cy + y_span + 1, K)

    # Eyes: two round dots in upper half
    ey = cy - ry // 3
    # left eye
    px(img, cx - 4, ey - 1, SE)
    px(img, cx - 5, ey,     SE)
    px(img, cx - 4, ey,     SE)
    px(img, cx - 3, ey,     SE)
    px(img, cx - 4, ey + 1, SE)
    # right eye
    px(img, cx + 4, ey - 1, SE)
    px(img, cx + 5, ey,     SE)
    px(img, cx + 4, ey,     SE)
    px(img, cx + 3, ey,     SE)
    px(img, cx + 4, ey + 1, SE)
    # shine dots
    px(img, cx - 3, ey - 1, SL0)
    px(img, cx + 5, ey - 1, SL0)

    # Ground puddle line at base
    hline(img, cx - rx + 1, cx + rx - 1, bot, SL3)

    return img


slime_idle = [
    build_slime(0, 0),
    build_slime(2, 0),
    build_slime(2, 0),
    build_slime(0, 0),
]
slime_walk = [
    build_slime(0,  0),
    build_slime(2, -1),
    build_slime(0,  0),
    build_slime(2,  1),
]
save_sheet(slime_idle + slime_walk, "enemy_slime")


# ═══════════════════════════════════════════════════════════════════════════════
#  BAT
# ═══════════════════════════════════════════════════════════════════════════════
BP0 = (145, 110, 175)   # wing highlight
BP1 = ( 90,  55, 130)   # wing base (dark purple)
BP2 = ( 50,  20,  80)   # wing shadow
BP3 = ( 20,   5,  40)   # wing deep
BB0 = (110,  90, 130)   # body highlight
BB1 = ( 65,  45,  95)   # body base
BB2 = ( 35,  20,  60)   # body shadow
BE  = (210,  30,  20)   # red eyes
BT  = (210, 170, 200)   # teeth/belly

def build_bat(wing_up=0, fly_dy=0):
    """
    wing_up: pixels wings raised above neutral (negative = lower)
    fly_dy: vertical offset for flying animation
    """
    img = new_frame()
    cx = 24
    body_top = 20 + fly_dy
    body_bot = body_top + 12

    # Wings spread wide
    # Left wing: from body left side out
    wing_root_y = body_top + 4
    wing_tip_y  = wing_root_y - 6 - wing_up
    # left wing shape: triangle-ish membrane
    # outer span x = cx - 18
    for wx in range(cx - 18, cx - 4):
        t = (wx - (cx - 18)) / 14.0     # 0 at tip, 1 at body
        top_y = int(wing_tip_y + t * (wing_root_y - wing_tip_y - 4))
        bot_y = wing_root_y + 3
        if top_y <= bot_y:
            vline(img, wx, top_y, bot_y, BP1)
            px(img, wx, top_y, BP0)
            px(img, wx, bot_y, BP2)
    # right wing
    for wx in range(cx + 5, cx + 19):
        t = (cx + 18 - wx) / 14.0
        top_y = int(wing_tip_y + t * (wing_root_y - wing_tip_y - 4))
        bot_y = wing_root_y + 3
        if top_y <= bot_y:
            vline(img, wx, top_y, bot_y, BP1)
            px(img, wx, top_y, BP0)
            px(img, wx, bot_y, BP2)
    # Wing membrane details (darker veins)
    for wx in range(cx - 16, cx - 5, 4):
        py_v = int(wing_tip_y + 2 + (wx - (cx - 16)) * 0.5)
        px(img, wx, py_v, BP3)
    for wx in range(cx + 6, cx + 17, 4):
        py_v = int(wing_tip_y + 2 + (cx + 16 - wx) * 0.5)
        px(img, wx, py_v, BP3)
    # wing outlines
    for wx in range(cx - 18, cx - 4):
        t = (wx - (cx - 18)) / 14.0
        top_y = int(wing_tip_y + t * (wing_root_y - wing_tip_y - 4))
        px(img, wx, top_y - 1, K)
    px(img, cx - 18, wing_root_y + 2, K)
    for wx in range(cx + 5, cx + 19):
        t = (cx + 18 - wx) / 14.0
        top_y = int(wing_tip_y + t * (wing_root_y - wing_tip_y - 4))
        px(img, wx, top_y - 1, K)
    px(img, cx + 18, wing_root_y + 2, K)

    # Body: small round-ish oval
    ellipse(img, cx, body_top + 6, 5, 6, BB1)
    ellipse(img, cx - 1, body_top + 4, 3, 3, BB0)  # highlight
    # belly (lighter patch)
    ellipse(img, cx, body_top + 8, 3, 3, BT)
    # body outline
    for dy in range(-6, 7):
        x_s = int(5 * (1 - (dy / 6) ** 2) ** 0.5)
        px(img, cx - x_s - 1, body_top + 6 + dy, K)
        px(img, cx + x_s + 1, body_top + 6 + dy, K)
    for dx in range(-5, 6):
        y_s = int(6 * (1 - (dx / 5) ** 2) ** 0.5)
        px(img, cx + dx, body_top + 6 - y_s - 1, K)
        px(img, cx + dx, body_top + 6 + y_s + 1, K)

    # Eyes: red glowing
    ey = body_top + 4
    px(img, cx - 2, ey, BE)
    px(img, cx + 2, ey, BE)
    px(img, cx - 2, ey + 1, BE)
    px(img, cx + 2, ey + 1, BE)

    # Ears (small pointy triangles on head top)
    head_top = body_top
    px(img, cx - 3, head_top - 1, BB1)
    px(img, cx - 2, head_top - 2, BB2)
    px(img, cx - 3, head_top - 3, K)
    px(img, cx - 2, head_top - 3, K)
    px(img, cx - 1, head_top - 2, K)
    px(img, cx + 3, head_top - 1, BB1)
    px(img, cx + 2, head_top - 2, BB2)
    px(img, cx + 3, head_top - 3, K)
    px(img, cx + 2, head_top - 3, K)
    px(img, cx + 1, head_top - 2, K)

    # Tiny fangs at bottom of body
    fang_y = body_bot - 1
    px(img, cx - 1, fang_y, BT)
    px(img, cx + 1, fang_y, BT)
    px(img, cx - 1, fang_y + 1, K)
    px(img, cx + 1, fang_y + 1, K)

    return img


bat_idle = [
    build_bat( 3,  0),
    build_bat( 5,  1),
    build_bat( 3,  0),
    build_bat(-2, -1),
]
bat_walk = [   # "walk" = flying forward
    build_bat( 4,  0),
    build_bat( 6,  1),
    build_bat( 2, -1),
    build_bat(-1,  0),
]
save_sheet(bat_idle + bat_walk, "enemy_bat")


# ═══════════════════════════════════════════════════════════════════════════════
#  KNIGHT
# ═══════════════════════════════════════════════════════════════════════════════
AR0 = (230, 235, 245)   # armor highlight
AR1 = (170, 175, 195)   # armor base (silver)
AR2 = (100, 105, 125)   # armor shadow
AR3 = ( 45,  50,  70)   # armor deep
PL0 = (200, 160,  50)   # plume highlight (gold-red)
PL1 = (185,  40,  30)   # plume base (red)
PL2 = (120,  18,  10)   # plume shadow
VS  = ( 15,  10,   5)   # visor slit (very dark)
SW0 = (245, 245, 250)   # sword highlight
SW1 = (185, 185, 200)   # sword blade
SW2 = (100, 100, 120)   # sword shadow
GD0 = (230, 185,  60)   # guard gold highlight
GD1 = (170, 125,  20)   # guard gold base
GD2 = (100,  65,   5)   # guard gold shadow
HN  = (120,  90,  40)   # handle brown
HN2 = ( 70,  50,  20)   # handle dark

def build_knight(body_dy=0, leg_dy_l=0, leg_dy_r=0):
    img = new_frame()
    cx = 24

    # -- SWORD (left side, held upright) --
    sw_x = 10
    sw_top = 4 + body_dy
    sw_bot = 28 + body_dy
    # blade
    vline(img, sw_x,     sw_top, sw_bot, SW1)
    vline(img, sw_x + 1, sw_top, sw_bot, SW0)
    vline(img, sw_x + 2, sw_top, sw_bot, SW2)
    # tip
    px(img, sw_x + 1, sw_top - 1, SW0)
    px(img, sw_x, sw_top - 1, K)
    px(img, sw_x + 2, sw_top - 1, K)
    px(img, sw_x + 1, sw_top - 2, K)
    # outline
    vline(img, sw_x - 1, sw_top, sw_bot, K)
    vline(img, sw_x + 3, sw_top, sw_bot, K)
    # guard (crossguard)
    gd_y = sw_bot - 10
    rect(img, sw_x - 3, gd_y, sw_x + 5, gd_y + 2, GD1)
    hline(img, sw_x - 3, sw_x + 5, gd_y,     GD0)
    hline(img, sw_x - 3, sw_x + 5, gd_y + 2, GD2)
    hline(img, sw_x - 4, sw_x + 6, gd_y - 1, K)
    hline(img, sw_x - 4, sw_x + 6, gd_y + 3, K)
    vline(img, sw_x - 4, gd_y, gd_y + 2, K)
    vline(img, sw_x + 6, gd_y, gd_y + 2, K)
    # handle
    rect(img, sw_x, sw_bot - 8, sw_x + 2, gd_y - 1, HN)
    vline(img, sw_x + 1, sw_bot - 8, gd_y - 1, HN2)
    # pommel
    rect(img, sw_x - 1, sw_bot - 9, sw_x + 3, sw_bot - 8, GD1)
    hline(img, sw_x - 2, sw_x + 4, sw_bot - 10, K)
    hline(img, sw_x - 2, sw_x + 4, sw_bot - 7,  K)

    # -- HELMET --
    helm_top = 4 + body_dy
    helm_bot = 13 + body_dy
    helm_l   = cx - 7
    helm_r   = cx + 7
    # main helm body
    rect(img, helm_l, helm_top, helm_r, helm_bot, AR1)
    # highlight left
    vline(img, helm_l + 1, helm_top + 1, helm_bot - 1, AR0)
    hline(img, helm_l + 1, helm_r - 1,  helm_top + 1, AR0)
    # shadow right/bottom
    vline(img, helm_r - 1, helm_top + 1, helm_bot - 1, AR2)
    vline(img, helm_r,     helm_top + 1, helm_bot - 1, AR3)
    hline(img, helm_l, helm_r, helm_bot - 1, AR2)
    # cheek guards (wider at bottom)
    rect(img, helm_l - 1, helm_top + 4, helm_r + 1, helm_bot, AR2)
    vline(img, helm_l - 1, helm_top + 4, helm_bot, AR3)
    vline(img, helm_r + 1, helm_top + 4, helm_bot, AR3)
    # outline
    hline(img, helm_l - 1, helm_r + 1, helm_top - 1, K)
    hline(img, helm_l - 1, helm_r + 1, helm_bot + 1, K)
    vline(img, helm_l - 2, helm_top,   helm_bot,     K)
    vline(img, helm_r + 2, helm_top,   helm_bot,     K)

    # Visor slit: narrow horizontal dark band
    vis_y = helm_top + 6
    hline(img, helm_l + 1, helm_r - 1, vis_y,     VS)
    hline(img, helm_l + 1, helm_r - 1, vis_y + 1, VS)
    # eyes glow slightly through visor
    px(img, cx - 2, vis_y,     (60, 20, 10))
    px(img, cx + 2, vis_y,     (60, 20, 10))

    # -- RED PLUME on top --
    plume_base = helm_top - 1
    # plume body curves left and up
    for i in range(8):
        px_x = cx + 1 - i // 2
        px_y = plume_base - 1 - i
        px(img, px_x,     px_y, PL1)
        px(img, px_x - 1, px_y, PL0)
        px(img, px_x + 1, px_y, PL2)
        px(img, px_x,     px_y - 1, K)  # top outline
        if i == 0:
            px(img, px_x - 1, px_y, K)  # left outline at base
    # plume outline right side
    for i in range(8):
        px_x = cx + 1 - i // 2 + 1
        px_y = plume_base - 1 - i
        px(img, px_x + 1, px_y, K)

    # -- GORGET / NECK piece --
    neck_top = helm_bot + 1
    neck_bot = neck_top + 3
    rect(img, cx - 4, neck_top, cx + 4, neck_bot, AR2)
    hline(img, cx - 3, cx + 3, neck_top, AR1)
    hline(img, cx - 4, cx + 4, neck_top - 1, K)
    hline(img, cx - 4, cx + 4, neck_bot + 1, K)
    vline(img, cx - 5, neck_top, neck_bot, K)
    vline(img, cx + 5, neck_top, neck_bot, K)

    # -- TORSO (plate cuirass) --
    torso_top = neck_bot + 1
    torso_bot = torso_top + 11
    # main plate
    rect(img, cx - 7, torso_top, cx + 8, torso_bot, AR1)
    # highlight column
    vline(img, cx - 5, torso_top + 1, torso_bot - 1, AR0)
    # shadow edges
    vline(img, cx + 6, torso_top + 1, torso_bot - 1, AR2)
    vline(img, cx + 7, torso_top + 1, torso_bot - 1, AR3)
    vline(img, cx - 6, torso_top + 1, torso_bot - 1, AR3)
    # center ridge (breastplate line)
    vline(img, cx, torso_top + 2, torso_bot - 1, AR2)
    hline(img, cx - 3, cx + 3, torso_top + 2, AR0)  # pectoral highlight
    # torso outline
    hline(img, cx - 7, cx + 8, torso_top - 1, K)
    hline(img, cx - 7, cx + 8, torso_bot + 1, K)
    vline(img, cx - 8, torso_top, torso_bot, K)
    vline(img, cx + 9, torso_top, torso_bot, K)

    # -- PAULDRONS (shoulder armor) --
    # left
    rect(img, cx - 11, torso_top, cx - 7, torso_top + 5, AR1)
    hline(img, cx - 10, cx - 7, torso_top, AR0)
    vline(img, cx - 10, torso_top, torso_top + 5, AR0)
    hline(img, cx - 11, cx - 7, torso_top - 1, K)
    hline(img, cx - 11, cx - 7, torso_top + 6, K)
    vline(img, cx - 12, torso_top, torso_top + 5, K)
    # right
    rect(img, cx + 8, torso_top, cx + 12, torso_top + 5, AR1)
    hline(img, cx + 8, cx + 11, torso_top, AR0)
    vline(img, cx + 11, torso_top, torso_top + 5, AR0)
    hline(img, cx + 8, cx + 12, torso_top - 1, K)
    hline(img, cx + 8, cx + 12, torso_top + 6, K)
    vline(img, cx + 13, torso_top, torso_top + 5, K)

    # -- ARMS (vambraces) --
    arm_top = torso_top + 3
    arm_bot = arm_top + 8
    # left arm
    rect(img, cx - 12, arm_top, cx - 8, arm_bot, AR1)
    vline(img, cx - 11, arm_top, arm_bot, AR0)
    vline(img, cx - 9,  arm_top, arm_bot, AR2)
    vline(img, cx - 13, arm_top, arm_bot, K)
    vline(img, cx - 7,  arm_top, arm_bot, K)
    hline(img, cx - 13, cx - 7, arm_top - 1, K)
    hline(img, cx - 13, cx - 7, arm_bot + 1, K)
    # gauntlet left
    rect(img, cx - 12, arm_bot + 1, cx - 7, arm_bot + 4, AR2)
    hline(img, cx - 12, cx - 7, arm_bot,     K)
    hline(img, cx - 12, cx - 7, arm_bot + 5, K)
    vline(img, cx - 13, arm_bot + 1, arm_bot + 4, K)
    vline(img, cx - 6,  arm_bot + 1, arm_bot + 4, K)
    # right arm
    rect(img, cx + 9, arm_top, cx + 13, arm_bot, AR1)
    vline(img, cx + 12, arm_top, arm_bot, AR0)
    vline(img, cx + 10, arm_top, arm_bot, AR2)
    vline(img, cx + 8,  arm_top, arm_bot, K)
    vline(img, cx + 14, arm_top, arm_bot, K)
    hline(img, cx + 8, cx + 14, arm_top - 1, K)
    hline(img, cx + 8, cx + 14, arm_bot + 1, K)
    # gauntlet right
    rect(img, cx + 8, arm_bot + 1, cx + 13, arm_bot + 4, AR2)
    hline(img, cx + 8, cx + 13, arm_bot,     K)
    hline(img, cx + 8, cx + 13, arm_bot + 5, K)
    vline(img, cx + 7,  arm_bot + 1, arm_bot + 4, K)
    vline(img, cx + 14, arm_bot + 1, arm_bot + 4, K)

    # -- TASSET / HIP SKIRT (plate strips) --
    belt_y = torso_bot + 1
    rect(img, cx - 7, belt_y, cx + 8, belt_y + 3, AR2)
    hline(img, cx - 6, cx + 7, belt_y, AR1)
    # vertical plate divisions
    for tx in range(cx - 5, cx + 8, 4):
        vline(img, tx, belt_y, belt_y + 3, AR3)
    hline(img, cx - 7, cx + 8, belt_y - 1, K)
    hline(img, cx - 7, cx + 8, belt_y + 4, K)
    vline(img, cx - 8, belt_y, belt_y + 3, K)
    vline(img, cx + 9, belt_y, belt_y + 3, K)

    # -- LEGS (greaves) --
    leg_top_y = belt_y + 4

    def draw_knight_leg(lx, dy):
        lt = leg_top_y + dy
        # thigh plate
        rect(img, lx, lt, lx + 5, lt + 6, AR1)
        vline(img, lx + 1, lt, lt + 6, AR0)
        vline(img, lx + 4, lt, lt + 6, AR2)
        vline(img, lx + 5, lt, lt + 6, AR3)
        # knee cap
        rect(img, lx, lt + 7, lx + 5, lt + 9, AR2)
        hline(img, lx + 1, lx + 4, lt + 7, AR0)
        # greave (shin)
        rect(img, lx, lt + 10, lx + 5, lt + 15, AR1)
        vline(img, lx + 1, lt + 10, lt + 15, AR0)
        vline(img, lx + 4, lt + 10, lt + 15, AR2)
        # outline
        hline(img, lx - 1, lx + 6, lt - 1,  K)
        vline(img, lx - 1, lt, lt + 15, K)
        vline(img, lx + 6, lt, lt + 15, K)
        hline(img, lx - 1, lx + 6, lt + 16, K)
        # sabatons (foot armor)
        rect(img, lx - 1, lt + 16, lx + 7, lt + 18, AR2)
        hline(img, lx,     lx + 6, lt + 16, AR1)
        hline(img, lx - 2, lx + 8, lt + 15, K)
        hline(img, lx - 2, lx + 8, lt + 19, K)
        vline(img, lx - 2, lt + 16, lt + 18, K)
        vline(img, lx + 8, lt + 16, lt + 18, K)

    draw_knight_leg(cx - 7, leg_dy_l)
    draw_knight_leg(cx + 1, leg_dy_r)

    return img


knight_idle = [
    build_knight(0,  0,  0),
    build_knight(-1, 0,  0),
    build_knight(0,  0,  0),
    build_knight(1,  0,  0),
]
knight_walk = [
    build_knight(-1, -3,  3),
    build_knight(0,  -1,  1),
    build_knight(-1,  3, -3),
    build_knight(0,   1, -1),
]
save_sheet(knight_idle + knight_walk, "enemy_knight")

print("\nAll done! Files written to:", OUT)
