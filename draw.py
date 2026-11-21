#!/usr/bin/env python3
"""Draw the news-image-20261121 front page: 'THE DAILY GLOBE', Saturday 21 November 2026.

Deterministic, no network, no external images. All art is drawn in code.
Run: python3 draw.py [output.png]   (default: entry.png next to this file)
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (26, 26, 26)
RED = (139, 26, 26)
GOLD = (198, 154, 52)
GREY = (110, 105, 95)
RULE = (60, 55, 48)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = f"{FONT_DIR}/DejaVuSerif-Bold.ttf"
SERIF = f"{FONT_DIR}/DejaVuSerif.ttf"
SANS_B = f"{FONT_DIR}/DejaVuSans-Bold.ttf"
SANS = f"{FONT_DIR}/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill=INK, leading=None):
    """Draw lines; returns y after the last line."""
    lh = leading or int(fnt.size * 1.18)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def hline(draw, x0, x1, y, width=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- art panels
def art_power_plant(d, x, y, w, h):
    """Hartha power station at dusk: orange sky, cooling towers, flames, smoke."""
    # sky bands
    bands = [(226, 122, 54), (232, 148, 66), (238, 178, 88), (244, 205, 120)]
    bh = h // 4
    for i, c in enumerate(bands):
        d.rectangle([x, y + i * bh, x + w, y + (i + 1) * bh], fill=c)
    # ground
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(52, 44, 38))
    # cooling towers (dark silhouettes, kept inside the art box)
    for tx, tw, th in [(x + 60, 120, 95), (x + 210, 140, 110), (x + 380, 110, 90)]:
        top = y + h - 26 - th
        d.polygon([(tx, top + 14), (tx + tw, top + 14), (tx + tw - 14, y + h - 26),
                   (tx + 14, y + h - 26)], fill=(58, 48, 42))
        d.ellipse([tx - 6, top - 6, tx + tw + 6, top + 16], fill=(58, 48, 42))
    # chimney with smoke (kept inside the art box)
    cx = x + w - 130
    d.rectangle([cx, y + 30, cx + 26, y + h - 26], fill=(58, 48, 42))
    for i, r in enumerate([11, 14, 17, 20]):
        d.ellipse([cx - 4 + i * 22, y + 26 - i * 10, cx + 22 + i * 22, y + 26 - i * 10 + 2 * r],
                  fill=(120, 112, 104))
    # flames at the base of the middle tower
    fx = x + 250
    for (dx, fh, col) in [(-30, 46, (220, 60, 20)), (0, 62, (245, 130, 30)), (30, 44, (255, 190, 60))]:
        d.polygon([(fx + dx - 16, y + h - 26), (fx + dx, y + h - 26 - fh),
                   (fx + dx + 16, y + h - 26)], fill=col)


def art_quake(d, x, y, w, h):
    """Andes mountains + red seismograph trace."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 226, 232))
    d.polygon([(x, y + h), (x + 90, y + 30), (x + 190, y + h)], fill=(96, 116, 130))
    d.polygon([(x + 150, y + h), (x + 300, y + 12), (x + 430, y + h)], fill=(70, 90, 104))
    d.polygon([(x + 340, y + h), (x + 430, y + 44), (x + w, y + h)], fill=(96, 116, 130))
    # snow caps
    d.polygon([(x + 82, y + 40), (x + 90, y + 30), (x + 98, y + 40), (x + 90, y + 48)], fill=(255, 255, 255))
    d.polygon([(x + 292, y + 22), (x + 300, y + 12), (x + 308, y + 22), (x + 300, y + 30)], fill=(255, 255, 255))
    # seismograph zigzag
    pts = []
    px = x + 10
    py = y + h - 34
    pts.append((px, py))
    for i, amp in enumerate([0, 26, -30, 44, -52, 30, -18, 8, 0]):
        px += (w - 20) / 8
        pts.append((px, py - amp))
    d.line(pts, fill=(178, 34, 34), width=4)


def art_bitcoin(d, x, y, w, h):
    """Dark chart, red falling line, gold coin."""
    d.rectangle([x, y, x + w, y + h], fill=(18, 28, 44))
    # grid
    for gy in range(y + 18, y + h - 10, 22):
        d.line([(x + 8, gy), (x + w - 8, gy)], fill=(38, 52, 72), width=1)
    # falling line
    pts = [(x + 12, y + 22), (x + 90, y + 34), (x + 170, y + 30), (x + 250, y + 58),
           (x + 330, y + 52), (x + 410, y + 82), (x + w - 14, y + h - 22)]
    d.line(pts, fill=(226, 62, 62), width=4)
    for p in pts[1:-1]:
        d.ellipse([p[0] - 4, p[1] - 4, p[0] + 4, p[1] + 4], fill=(226, 62, 62))
    # gold coin
    cx, cy, r = x + w - 62, y + 34, 26
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(212, 160, 44), outline=(150, 106, 20), width=2)
    d.text((cx - 8, cy - 17), "B", font=font(SANS_B, 30), fill=(24, 24, 24))


def art_liquor(d, x, y, w, h):
    """Hospital cross + bottle with warning."""
    d.rectangle([x, y, x + w, y + h], fill=(222, 235, 228))
    # hospital cross
    cx, cy = x + w // 2, y + h // 2 - 6
    d.rectangle([cx - 34, cy - 12, cx + 34, cy + 12], fill=(34, 120, 80))
    d.rectangle([cx - 12, cy - 34, cx + 12, cy + 34], fill=(34, 120, 80))
    # small bottle at the corner
    bx, by = x + 14, y + h - 52
    d.rectangle([bx + 8, by - 8, bx + 22, by], fill=(90, 90, 90))
    d.rectangle([bx, by, bx + 30, by + 44], fill=(120, 60, 60))
    d.polygon([(bx + 15, by + 8), (bx + 26, by + 26), (bx + 4, by + 26)], fill=(255, 220, 60))
    d.text((bx + 12, by + 14), "!", font=font(SANS_B, 14), fill=(0, 0, 0))


def art_haiti(d, x, y, w, h):
    """Helmet + explosion starburst on olive ground."""
    d.rectangle([x, y, x + w, y + h], fill=(196, 198, 158))
    cx, cy = x + w // 2, y + h // 2 + 8
    # starburst (small, behind the helmet)
    for ang in range(0, 360, 30):
        import math
        r1, r2 = 30, 44
        a = math.radians(ang)
        d.line([(cx + r1 * math.cos(a), cy - 6 + r1 * math.sin(a)),
                (cx + r2 * math.cos(a), cy - 6 + r2 * math.sin(a))], fill=(214, 150, 40), width=4)
    # helmet
    d.pieslice([cx - 52, cy - 46, cx + 52, cy + 30], 180, 360, fill=(74, 92, 52))
    d.rectangle([cx - 62, cy - 2, cx + 62, cy + 8], fill=(58, 74, 40))


def art_kryvyi(d, x, y, w, h):
    """City skyline at dusk with an explosion burst."""
    d.rectangle([x, y, x + w, y + h], fill=(38, 48, 74))
    # buildings
    import random
    rng = random.Random(7)
    bx = x
    while bx < x + w - 20:
        bw = rng.randint(22, 44)
        bh = rng.randint(28, 62)
        d.rectangle([bx, y + h - bh, bx + bw, y + h], fill=(22, 28, 46))
        bx += bw + 4
    # explosion
    ex, ey = x + w - 70, y + 34
    for (dx, dy, r, col) in [(0, 0, 26, (255, 190, 60)), (-16, 8, 16, (240, 120, 40)),
                             (16, 10, 14, (240, 120, 40)), (0, -14, 12, (255, 220, 120))]:
        d.ellipse([ex + dx - r, ey + dy - r, ex + dx + r, ey + dy + r], fill=col)
    # siren light
    d.ellipse([x + 16, y + 14, x + 34, y + 32], fill=(226, 62, 62))


# ---------------------------------------------------------------- front page
def build(out_path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    d.rectangle([0, 0, W, 118], fill=RED)
    title = "THE DAILY GLOBE"
    tf = font(SERIF_B, 62)
    d.text(((W - d.textlength(title, font=tf)) / 2, 12), title, font=tf, fill=(255, 250, 240))
    date = "SATURDAY  21  NOVEMBER  2026"
    df = font(SANS_B, 27)
    d.text(((W - d.textlength(date, font=df)) / 2, 80), date, font=df, fill=(255, 214, 150))
    d.rectangle([0, 118, W, 124], fill=GOLD)

    # ---- lead: Basra fire
    lx, lw = 28, 968
    ly = 138
    d.text((lx, ly), "IRAQ  ·  DISASTER", font=font(SANS_B, 19), fill=RED)
    art_power_plant(d, lx, ly + 30, lw, 148)
    hy = ly + 30 + 148 + 12
    head = "Fire kills four at Basra power station"
    hf = font(SERIF_B, 40)
    d.text((lx, hy), head, font=hf, fill=INK)
    cy = hy + 52
    cap = ("At least four people were killed and 30 injured in a fire at the Hartha "
           "power station north of Basra. Fire crews brought the blaze under control, "
           "but officials fear the toll may rise.")
    text_block(d, lx, cy, wrap(d, cap, font(SANS, 21), lw), font(SANS, 21), leading=26)
    hline(d, 28, 996, 470)

    # ---- row 2: Peru | Bitcoin
    ry = 482
    # Peru (left)
    art_quake(d, 28, ry, 472, 96)
    text_block(d, 28, ry + 106,
               wrap(d, "Magnitude 6.9 quake shakes Peru's Andes", font(SERIF_B, 28), 472),
               font(SERIF_B, 28), leading=32)
    text_block(d, 28, ry + 106 + 64,
               wrap(d, "Felt in the capital, Lima. No casualties or damage reported.",
                    font(SANS, 19), 472), font(SANS, 19), leading=23)
    # Bitcoin (right)
    art_bitcoin(d, 524, ry, 472, 96)
    text_block(d, 524, ry + 106,
               wrap(d, "Bitcoin breaks below $60,000", font(SERIF_B, 28), 472),
               font(SERIF_B, 28), leading=32)
    text_block(d, 524, ry + 106 + 34,
               wrap(d, "Lowest since September 2024; about $2.4bn in leveraged bets "
                       "wiped out in a day.", font(SANS, 19), 472),
               font(SANS, 19), leading=23)
    hline(d, 28, 996, 714)

    # ---- row 3: Manipur | Haiti | Kryvyi Rih
    ty = 726
    cols = [
        (28, art_liquor, "Toxic liquor toll hits 13 in Manipur",
         "346 in hospital; methanol suspected in the spurious brew."),
        (366, art_haiti, "Three Salvadoran troops killed in Haiti",
         "Soldiers hit by explosives in Port-au-Prince."),
        (704, art_kryvyi, "Kryvyi Rih: 2 dead, 42 hurt overnight",
         "Attack followed Friday's mass barrage on Kyiv."),
    ]
    for (cx, art, headline, caption) in cols:
        art(d, cx, ty, 292, 82)
        hlines = wrap(d, headline, font(SERIF_B, 23), 292)
        y = text_block(d, cx, ty + 90, hlines, font(SERIF_B, 23), leading=27)
        text_block(d, cx, y + 4, wrap(d, caption, font(SANS, 17), 292),
                   font(SANS, 17), leading=21)

    # ---- ticker
    d.rectangle([0, 940, W, 974], fill=(26, 26, 26))
    tick = ("Houthi missiles at Riyadh intercepted  ·  Palisades arsonist convicted  ·  "
            "Indonesia forest fires")
    tf2 = font(SANS_B, 17)
    tw = d.textlength(tick, font=tf2)
    d.text(((W - tw) / 2, 948), tick, font=tf2, fill=(255, 255, 255))

    # ---- footer
    foot = "Drawn from reports published on 21 November 2026  ·  Sources: Reuters, USGS, PTI, CoinGecko"
    ff = font(SANS, 15)
    d.text(((W - d.textlength(foot, font=ff)) / 2, 986), foot, font=ff, fill=GREY)

    img.save(out_path, "PNG")
    print(f"wrote {out_path} {img.size}")


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else "entry.png")
