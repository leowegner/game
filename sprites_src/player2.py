"""
Player spritesheet — 48x48 pixel art, hand-crafted via drawing primitives
Detailed SNES-RPG style: stocky warrior, red beard, blue tunic, red pants, big hammer
Output: player2_sheet.png — 8 frames horizontal (4 idle + 4 walk), 384x48
"""
from PIL import Image, ImageDraw
import os

W, H = 48, 48

# ── Palette ───────────────────────────────────────────────────────────────────
_ = (255, 0, 255)   # transparent

K  = ( 18,  12,   8)   # outline
K2 = ( 40,  25,  15)   # soft inner line

S0 = (240, 175, 120)   # skin highlight
S1 = (215, 140,  85)   # skin base
S2 = (175, 100,  50)   # skin shadow
S3 = (130,  65,  25)   # skin deep

HR0= (240, 120,  40)   # hair/beard highlight
HR1= (200,  75,  20)   # hair/beard base
HR2= (150,  45,  10)   # hair/beard shadow
HR3= ( 95,  25,   5)   # hair/beard deep

EW = (240, 230, 215)   # eye white
EP = ( 30,  20,  10)   # pupil

T0 = (130, 175, 240)   # tunic highlight
T1 = ( 60, 115, 210)   # tunic mid
T2 = ( 35,  75, 165)   # tunic shadow
T3 = ( 20,  45, 115)   # tunic deep

WH = (240, 235, 225)   # white shirt
WS = (190, 185, 175)   # shirt shadow

BL0= (200, 160,  70)   # belt highlight
BL1= (155, 115,  30)   # belt base
BL2= (105,  70,  10)   # belt shadow
BLK= ( 30,  20,  10)   # buckle

R0 = (230,  90,  60)   # pants highlight
R1 = (185,  50,  28)   # pants base
R2 = (135,  25,  12)   # pants shadow
R3 = ( 85,  12,   4)   # pants deep

BO0= (140,  95,  55)   # boot highlight
BO1= ( 95,  60,  28)   # boot base
BO2= ( 60,  35,  12)   # boot shadow
BO3= ( 30,  16,   4)   # boot sole

HH0= (215, 220, 230)   # hammerhead highlight
HH1= (155, 160, 175)   # hammerhead mid
HH2= ( 90,  95, 110)   # hammerhead shadow
HH3= ( 45,  50,  65)   # hammerhead dark
HW0= (190, 145,  80)   # handle highlight
HW1= (140,  95,  40)   # handle base
HW2= ( 85,  55,  15)   # handle shadow
RV = (185,  30,  20)   # ribbon red
RVD= (110,  12,   8)   # ribbon dark

MA0= (230, 160, 100)   # bare arm highlight
MA1= (200, 125,  68)   # bare arm mid

# ── Drawing helpers ───────────────────────────────────────────────────────────

def new_frame():
    img = Image.new("RGB", (W, H), _)
    return img

def px(img, x, y, c):
    if 0 <= x < W and 0 <= y < H:
        img.putpixel((x, y), c)

def hline(img, x0, x1, y, c):
    for x in range(x0, x1+1):
        px(img, x, y, c)

def vline(img, x, y0, y1, c):
    for y in range(y0, y1+1):
        px(img, x, y, c)

def rect(img, x0, y0, x1, y1, c):
    for y in range(y0, y1+1):
        hline(img, x0, x1, y, c)

def outline_rect(img, x0, y0, x1, y1, fill, border):
    rect(img, x0, y0, x1, y1, fill)
    hline(img, x0, x1, y0, border)
    hline(img, x0, x1, y1, border)
    vline(img, x0, y0, y1, border)
    vline(img, x1, y0, y1, border)

def draw_ellipse_fill(img, cx, cy, rx, ry, c):
    for dy in range(-ry, ry+1):
        for dx in range(-rx, rx+1):
            if (dx/rx)**2 + (dy/ry)**2 <= 1.0:
                px(img, cx+dx, cy+dy, c)

# ── Build one idle frame ──────────────────────────────────────────────────────

def build_frame(leg_dy_left=0, leg_dy_right=0, body_dy=0):
    img = new_frame()

    # ── HAMMER (left side, held at shoulder height) ───────────────────────────
    # Handle: vertical, x=7, y=9..30
    hy0, hy1 = 9 + body_dy, 30 + body_dy
    vline(img, 8, hy0, hy1, HW0)
    vline(img, 9, hy0, hy1, HW1)
    vline(img, 10, hy0, hy1, HW2)
    # outline
    vline(img, 7, hy0, hy1, K)
    vline(img, 11, hy0, hy1, K)

    # Hammer head: x=3..12, y=3..12 + body_dy
    hx0, hx1 = 3, 13
    hhy0, hhy1 = 3 + body_dy, 13 + body_dy
    # main body
    rect(img, hx0+1, hhy0+1, hx1-1, hhy1-1, HH1)
    # highlight top-left
    rect(img, hx0+1, hhy0+1, hx0+3, hhy0+3, HH0)
    # shadow right
    rect(img, hx1-3, hhy0+1, hx1-1, hhy1-1, HH2)
    # shadow bottom
    rect(img, hx0+1, hhy1-2, hx1-1, hhy1-1, HH3)
    # red ribbon band across middle
    hline(img, hx0+1, hx1-1, hhy0+4, RV)
    hline(img, hx0+1, hx1-1, hhy0+5, RVD)
    hline(img, hx0+1, hx1-1, hhy0+6, RV)
    # outline
    hline(img, hx0, hx1, hhy0, K)
    hline(img, hx0, hx1, hhy1, K)
    vline(img, hx0, hhy0, hhy1, K)
    vline(img, hx1, hhy0, hhy1, K)

    # ── HEAD ─────────────────────────────────────────────────────────────────
    # Hair top: x=16..31, y=4..7 + body_dy
    head_top = 4 + body_dy
    # Hair back/sides (dark)
    rect(img, 16, head_top, 31, head_top+1, HR2)
    hline(img, 16, 31, head_top, HR3)
    # Hair middle rows
    rect(img, 15, head_top+1, 32, head_top+3, HR1)
    hline(img, 17, 30, head_top+1, HR0)  # highlight strip

    # Face: x=17..30, y=7..14 + body_dy
    face_top = head_top + 3
    face_bot = face_top + 8
    rect(img, 17, face_top, 30, face_bot, S1)
    # Highlight strip
    hline(img, 18, 29, face_top, S0)
    hline(img, 18, 29, face_top+1, S0)
    # Shadow sides
    vline(img, 17, face_top, face_bot, S2)
    vline(img, 30, face_top, face_bot, S2)
    # Shadow bottom
    hline(img, 17, 30, face_bot, S3)
    hline(img, 17, 30, face_bot-1, S2)

    # Eyes: y = face_top+3
    ey = face_top + 3
    # left eye x=19..21
    hline(img, 19, 21, ey, EW)
    px(img, 20, ey, EP)
    hline(img, 19, 21, ey-1, K)  # brow
    # right eye x=26..28
    hline(img, 26, 28, ey, EW)
    px(img, 27, ey, EP)
    hline(img, 26, 28, ey-1, K)  # brow

    # Nose: center
    px(img, 23, face_top+5, S3)
    px(img, 24, face_top+5, S3)

    # Head outline
    hline(img, 16, 31, head_top-1, K)
    hline(img, 16, 31, face_bot+1, K)
    vline(img, 15, head_top, face_bot, K)
    vline(img, 32, head_top, face_bot, K)

    # ── BEARD ────────────────────────────────────────────────────────────────
    beard_top = face_bot - 1
    beard_bot = beard_top + 5
    # Full beard covering lower face
    rect(img, 16, beard_top, 31, beard_bot, HR1)
    # Highlight top
    hline(img, 17, 30, beard_top, HR0)
    # Shadow sides and bottom
    vline(img, 16, beard_top, beard_bot, HR2)
    vline(img, 31, beard_top, beard_bot, HR2)
    hline(img, 16, 31, beard_bot, HR3)
    hline(img, 16, 31, beard_bot-1, HR2)
    # Texture lines
    for x in range(17, 31, 3):
        px(img, x, beard_top+2, HR2)
        px(img, x+1, beard_top+3, HR3)

    # ── NECK ─────────────────────────────────────────────────────────────────
    neck_top = beard_bot + 1
    neck_bot = neck_top + 1
    rect(img, 21, neck_top, 26, neck_bot, S2)
    vline(img, 20, neck_top, neck_bot, K)
    vline(img, 27, neck_top, neck_bot, K)

    # ── BODY / TORSO ─────────────────────────────────────────────────────────
    torso_top = neck_bot + 1 + body_dy
    torso_bot = torso_top + 10

    # Bare arm (left, hammer side): x=13..17, y=torso_top..torso_top+7
    arm_top = torso_top
    arm_bot = torso_top + 8
    rect(img, 13, arm_top, 17, arm_bot, MA1)
    vline(img, 14, arm_top, arm_bot, MA0)
    vline(img, 13, arm_top, arm_bot, K)
    vline(img, 17, arm_top, arm_bot, K)
    hline(img, 13, 17, arm_top, K)
    hline(img, 13, 17, arm_bot, K)

    # Tunic body: x=18..33
    rect(img, 18, torso_top, 33, torso_bot, T1)
    # Highlight left stripe
    vline(img, 19, torso_top+1, torso_bot-1, T0)
    # Shadow right stripe
    vline(img, 32, torso_top+1, torso_bot-1, T2)
    vline(img, 33, torso_top+1, torso_bot-1, T3)
    # White shirt center
    rect(img, 22, torso_top+1, 29, torso_bot-1, WH)
    rect(img, 23, torso_top+2, 28, torso_bot-2, WS)
    # Right arm (tunic sleeve)
    rect(img, 34, arm_top, 38, arm_bot, T1)
    vline(img, 35, arm_top+1, arm_bot-1, T0)
    vline(img, 37, arm_top+1, arm_bot-1, T2)
    vline(img, 34, arm_top, arm_bot, K)
    vline(img, 38, arm_top, arm_bot, K)
    hline(img, 34, 38, arm_top, K)
    hline(img, 34, 38, arm_bot, K)

    # Torso outline
    hline(img, 13, 38, torso_top-1, K)
    hline(img, 13, 38, torso_bot+1, K)
    vline(img, 12, torso_top, torso_bot, K)
    vline(img, 39, torso_top, torso_bot, K)

    # ── BELT ─────────────────────────────────────────────────────────────────
    belt_y = torso_bot + 1
    rect(img, 16, belt_y, 35, belt_y+2, BL1)
    hline(img, 17, 34, belt_y, BL0)
    hline(img, 17, 34, belt_y+2, BL2)
    # buckle center
    rect(img, 23, belt_y, 25, belt_y+2, BLK)
    px(img, 24, belt_y+1, BL0)
    hline(img, 16, 35, belt_y-1, K)
    hline(img, 16, 35, belt_y+3, K)
    vline(img, 15, belt_y, belt_y+2, K)
    vline(img, 36, belt_y, belt_y+2, K)

    # ── LEGS ─────────────────────────────────────────────────────────────────
    leg_top = belt_y + 4

    def draw_leg(img, lx, dy):
        lt = leg_top + dy
        # thigh
        rect(img, lx, lt, lx+4, lt+6, R1)
        vline(img, lx+1, lt, lt+6, R0)
        vline(img, lx+3, lt, lt+6, R2)
        vline(img, lx+4, lt, lt+6, R3)
        # shin
        rect(img, lx, lt+7, lx+4, lt+12, R1)
        vline(img, lx+1, lt+7, lt+12, R0)
        vline(img, lx+3, lt+7, lt+12, R2)
        # outline
        hline(img, lx, lx+4, lt-1, K)
        vline(img, lx-1, lt, lt+12, K)
        vline(img, lx+5, lt, lt+12, K)
        hline(img, lx, lx+4, lt+13, K)
        # boot
        bx0, bx1 = lx-1, lx+6
        by0 = lt+13
        rect(img, bx0+1, by0, bx1-1, by0+3, BO1)
        hline(img, bx0+1, bx1-1, by0, BO0)
        # toe extension
        rect(img, bx0, by0+2, bx1, by0+4, BO1)
        hline(img, bx0, bx1, by0+1, BO0)
        hline(img, bx0, bx1, by0+4, BO2)
        # sole
        hline(img, bx0, bx1, by0+5, BO3)
        hline(img, bx0, bx1, by0+6, BO3)
        # boot outline
        hline(img, bx0, bx1, by0-1, K)
        vline(img, bx0-1, by0, by0+6, K)
        vline(img, bx1+1, by0, by0+6, K)
        hline(img, bx0, bx1, by0+7, K)

    draw_leg(img, 17, leg_dy_left)
    draw_leg(img, 26, leg_dy_right)

    return img

# ── Generate frames ───────────────────────────────────────────────────────────

# Idle: gentle bob
idle_frames = [
    build_frame(0, 0, 0),
    build_frame(0, 0, -1),
    build_frame(0, 0, 0),
    build_frame(0, 0, 1),
]

# Walk: legs alternate, body bobs
walk_frames = [
    build_frame(-3,  3, -1),  # left leg forward
    build_frame(-1,  1,  0),  # mid
    build_frame( 3, -3, -1),  # right leg forward
    build_frame( 1, -1,  0),  # mid back
]

# ── Assemble spritesheet ──────────────────────────────────────────────────────
sheet = Image.new("RGB", (W * 8, H), _)
for i, frame in enumerate(idle_frames + walk_frames):
    sheet.paste(frame, (i * W, 0))

# 4× zoom preview
preview = sheet.resize((W * 8 * 4, H * 4), Image.NEAREST)

out_dir = "/home/leo/dev/game-1/sprites_src"
os.makedirs(out_dir, exist_ok=True)
sheet.save(f"{out_dir}/player2_sheet.png")
preview.save(f"{out_dir}/player2_preview.png")
print(f"Saved {out_dir}/player2_sheet.png  ({W*8}×{H})")
print(f"Saved {out_dir}/player2_preview.png  ({W*8*4}×{H*4}) — zoom 4×")
