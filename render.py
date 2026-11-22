#!/usr/bin/env python3
"""Render the front page for Sunday 22 November 2026.

Deterministic: no time, no randomness, no metadata. Pillow only at
build time; the graded program (main.py) only copies the PNG.
Run: python3 render.py  -> writes entry.png (1024x1024) next to this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 241, 222)
INK = (26, 26, 26)
RED = (176, 42, 32)
BLUE = (31, 68, 120)
TEAL = (18, 110, 105)
GOLD = (198, 142, 32)
GREY = (110, 105, 90)
LIGHT = (232, 224, 198)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap, returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def tag(draw, x, y, label, fill):
    f = font(SANS_B, 11)
    w = draw.textlength(label, font=f) + 12
    draw.rounded_rectangle([x, y, x + w, y + 17], radius=3, fill=fill)
    draw.text((x + 6, y + 2), label, font=f, fill=(255, 255, 255))
    return w


# ---------------------------------------------------------------- icons
def draw_icon(draw, box, kind, bg):
    """Small flat illustration inside box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=bg)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    if kind == "cop":
        # conference table + flags + sun
        draw.ellipse([x1 - 52, y0 + 8, x1 - 16, y0 + 44], fill=(240, 190, 60))
        draw.rectangle([x0 + 12, y1 - 34, x1 - 12, y1 - 12], fill=(31, 68, 120))
        for i, c in enumerate([(176, 42, 32), (18, 110, 105), (198, 142, 32),
                               (31, 68, 120), (120, 60, 140)]):
            fx = x0 + 18 + i * 26
            draw.rectangle([fx, y1 - 62, fx + 16, y1 - 36], fill=c)
    elif kind == "bahrain":
        # refinery towers + smoke + ship
        for i in range(3):
            tx = x0 + 16 + i * 30
            draw.rectangle([tx, y0 + 34, tx + 14, y1 - 26], fill=(70, 70, 78))
            draw.ellipse([tx - 2, y0 + 12, tx + 16, y0 + 30], fill=(90, 90, 96))
        draw.rectangle([x0 + 10, y1 - 26, x1 - 10, y1 - 12], fill=(40, 60, 90))
        draw.polygon([(x0 + 20, y1 - 26), (x0 + 44, y1 - 44),
                      (x0 + 68, y1 - 26)], fill=(200, 210, 220))
    elif kind == "drone":
        # night sky, drone, burning building
        draw.ellipse([x1 - 46, y0 + 8, x1 - 14, y0 + 40], fill=(240, 210, 120))
        draw.rectangle([x0 + 14, y1 - 52, x0 + 62, y1 - 12], fill=(60, 55, 50))
        draw.polygon([(x0 + 22, y1 - 52), (x0 + 38, y1 - 78),
                      (x0 + 54, y1 - 52)], fill=(230, 110, 30))
        draw.line([cx - 26, y0 + 26, cx + 26, y0 + 26], fill=(220, 220, 220), width=3)
        draw.line([cx, y0 + 14, cx, y0 + 38], fill=(220, 220, 220), width=3)
        draw.ellipse([cx - 6, y0 + 20, cx + 6, y0 + 32], fill=(220, 220, 220))
    elif kind == "ship":
        draw.rectangle([x0 + 6, y1 - 30, x1 - 6, y1 - 14], fill=(40, 60, 90))
        draw.polygon([(x0 + 12, y1 - 30), (x0 + 24, y1 - 52),
                      (x0 + 36, y1 - 30)], fill=(200, 210, 220))
        draw.ellipse([x0 + 26, y0 + 8, x0 + 42, y0 + 24], fill=(230, 110, 30))
        draw.ellipse([x0 + 32, y0 + 16, x0 + 44, y0 + 28], fill=(240, 150, 60))
    elif kind == "nato":
        draw.rectangle([x0 + 14, y0 + 14, x1 - 14, y1 - 14], fill=(31, 68, 120))
        draw.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], fill=(240, 240, 240))
        draw.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(31, 68, 120))
    elif kind == "korea":
        draw.rectangle([x0 + 16, y0 + 16, x1 - 16, y1 - 16], fill=(255, 255, 255))
        draw.rectangle([x0 + 16, y0 + 16, x1 - 16, y0 + 30], fill=(31, 68, 120))
        draw.text((cx - 8, y0 + 34), "AI", font=font(SANS_B, 20),
                  fill=(176, 42, 32))
    elif kind == "vote":
        draw.rectangle([x0 + 20, y0 + 20, x1 - 20, y1 - 14], fill=(255, 255, 255))
        draw.rectangle([x0 + 20, y0 + 20, x1 - 20, y0 + 32], fill=(176, 42, 32))
        draw.line([x0 + 26, cy + 2, x0 + 36, cy + 12], fill=(18, 110, 105), width=3)
        draw.line([x0 + 36, cy + 12, x0 + 48, cy - 4], fill=(18, 110, 105), width=3)
    elif kind == "fire":
        draw.polygon([(cx, y0 + 10), (cx + 24, y0 + 44), (cx + 12, y0 + 44),
                      (cx + 26, y1 - 16), (cx - 26, y1 - 16), (cx - 12, y0 + 44),
                      (cx - 24, y0 + 44)], fill=(230, 110, 30))
        draw.ellipse([cx - 10, y0 + 40, cx + 10, y0 + 60], fill=(240, 190, 60))
    elif kind == "trade":
        draw.rectangle([x0 + 6, y1 - 30, x1 - 6, y1 - 12], fill=(31, 68, 120))
        for i, h in enumerate([12, 20, 15, 24]):
            bx = x0 + 8 + i * 9
            draw.rectangle([bx, y1 - 30 - h, bx + 6, y1 - 30], fill=(198, 142, 32))
    elif kind == "space":
        draw.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=(198, 142, 32))
        draw.ellipse([cx - 26, cy - 6, cx + 26, cy + 6], fill=(220, 220, 220))
        draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(26, 26, 26))
    elif kind == "race":
        draw.rectangle([x0 + 8, y1 - 30, x1 - 8, y1 - 14], fill=(26, 26, 26))
        draw.ellipse([x0 + 16, y1 - 20, x0 + 28, y1 - 8], fill=(240, 240, 240))
        draw.ellipse([x0 + 32, y1 - 20, x0 + 44, y1 - 8], fill=(240, 240, 240))
        draw.rectangle([x0 + 18, y0 + 24, x0 + 42, y0 + 38], fill=(176, 42, 32))
    elif kind == "cricket":
        draw.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=(18, 110, 105))
        draw.rectangle([cx - 4, y0 + 14, cx + 4, y1 - 14], fill=(240, 210, 120))
        draw.ellipse([cx - 14, y0 + 14, cx + 14, y0 + 42], fill=(240, 210, 120))
    elif kind == "soccer":
        draw.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=(255, 255, 255))
        draw.polygon([(cx, cy - 12), (cx + 11, cy - 4), (cx + 7, cy + 10),
                      (cx - 7, cy + 10), (cx - 11, cy - 4)], fill=(26, 26, 26))


# ---------------------------------------------------------------- stories
HEROES = [
    ("COP31", "ONGOING", RED, "cop", (18, 90, 110),
     "COP31: NO DEAL YET",
     "Final draft drops 'fossil fuels'; plenary slips into day 2 of overtime.",
     "Reuters"),
    ("BAHRAIN", "CLAIM", (150, 90, 40), "bahrain", (30, 45, 70),
     "BAHRAIN SEEKS UN ACTION",
     "Bahrain says Iran hit a civilian site; IRGC claims US bases hit.",
     "Reuters / AFP"),
    ("UKRAINE", "REPORTED", TEAL, "drone", (20, 25, 45),
     "186 DRONES OVERNIGHT",
     "161 downed; drone hits a flat in Dymer, Kyiv, 14 missing.",
     "Ukraine Air Force / Reuters"),
]

SMALL = [
    ("4", "REPORTED", "ship", (30, 60, 90), "Sparta II still burning off Finland", "Reuters"),
    ("5", "CONFIRMED", "nato", (200, 220, 235), "NATO: defend every inch of Poland", "NATO"),
    ("6", "CONFIRMED", "korea", (235, 225, 210), "S Korea minister quits over AI-cheating row", "KBS"),
    ("7", "CONFIRMED", "vote", (225, 235, 220), "Hong Kong turnout 98.79% in poll", "SCMP"),
    ("8", "REPORTED", "fire", (40, 40, 40), "Cikande factory fire, search ongoing", "Reuters"),
    ("9", "CONFIRMED", "trade", (210, 225, 240), "EU-Indonesia trade deal after 10 years", "Reuters"),
    ("10", "CONFIRMED", "space", (20, 25, 45), "BepiColombo enters Mercury orbit", "ESA"),
    ("11", "CONFIRMED", "race", (25, 25, 25), "Verstappen wins Las Vegas GP", "F1"),
    ("12", "CONFIRMED", "cricket", (225, 240, 225), "India 720/9 vs New Zealand", "Reuters"),
    ("13", "CONFIRMED", "soccer", (240, 240, 240), "Leeds stun Chelsea 4-1 away", "Reuters"),
]

ALSO = [
    ("14", "Nigeria funeral boat capsizes, 24 dead", "REPORTED", "Reuters"),
    ("15", "FBI probes hack of national crime database", "REPORTED", "AP"),
    ("16", "Nvidia faces SEC probe as shares slide", "REPORTED", "Reuters"),
    ("17", "Iran power rationing begins", "REPORTED", "AFP"),
    ("18", "Gaza food-aid van strike, 3 killed, identity disputed", "REPORTED", "Reuters"),
    ("19", "Estonia closes Russia border crossings", "CONFIRMED", "Reuters"),
    ("20", "Denmark expels Russian attache", "REPORTED", "Reuters"),
    ("21", "Houthi missile fired at Saudi Arabia", "REPORTED", "Reuters"),
    ("22", "Iraq Hartha power plant fire, 4 dead", "REPORTED", "Reuters"),
    ("23", "Toxic alcohol in India kills 11", "REPORTED", "AP"),
    ("24", "Florida record flooding on St Johns River", "REPORTED", "AP"),
    ("25", "Argentina approves $50bn LNG project", "CONFIRMED", "Reuters"),
    ("26", "US curbs defence cooperation with Canada", "REPORTED", "Reuters"),
    ("27", "UN: 128 nations to draft autonomous-weapons rules", "CONFIRMED", "AP"),
    ("28", "ICJ Myanmar genocide ruling - 19 Nov", "CONFIRMED", "ICJ"),
    ("29", "Wall Street AI rout - Fri 20 Nov", "REPORTED", "AP"),
    ("30", "Brazil storm kills 3, wrecks thousands of homes", "REPORTED", "AP"),
    ("31", "Tbilisi gas explosion kills 6", "REPORTED", "AP"),
    ("32", "Turkey seizes last independent news channel", "REPORTED", "Reuters"),
    ("33", "Gulf oil near $90 as Hormuz tension rises", "REPORTED", "Reuters"),
    ("34", "Banda quake M6.8 felt in Darwin, no tsunami", "CONFIRMED", "USGS"),
    ("35", "Arsenal held 2-2 by Newcastle", "CONFIRMED", "Reuters"),
]

REGIONS = ["EUROPE", "MIDDLE EAST", "ASIA-PACIFIC", "AMERICAS",
           "AFRICA", "UKRAINE", "GLOBAL"]
REGION_COLORS = [(31, 68, 120), (176, 42, 32), (18, 110, 105),
                 (198, 142, 32), (120, 60, 140), (40, 90, 60), (90, 90, 96)]

UTC_EVENTS = [("02:00", "COP31 draft"), ("06:00", "Plenary slips"),
              ("08:00", "Bahrain to UN"), ("12:00", "Dymer rescue"),
              ("18:00", "HK 98.79%")]


def draw_map(draw, x0, y0, x1, y1):
    """Dotted world map: dots inside rough continent blobs."""
    blobs = [  # (cx, cy, rx, ry) in box-relative fractions
        (0.16, 0.30, 0.13, 0.16), (0.30, 0.42, 0.10, 0.13),
        (0.52, 0.28, 0.16, 0.13), (0.62, 0.45, 0.12, 0.15),
        (0.80, 0.38, 0.13, 0.14), (0.88, 0.62, 0.07, 0.10),
    ]
    w, h = x1 - x0, y1 - y0
    step = 9
    for gy in range(y0 + 6, y1 - 4, step):
        for gx in range(x0 + 6, x1 - 4, step):
            fx, fy = (gx - x0) / w, (gy - y0) / h
            inside = any(((fx - cx) / rx) ** 2 + ((fy - cy) / ry) ** 2 <= 1
                         for cx, cy, rx, ry in blobs)
            if inside:
                draw.ellipse([gx - 2, gy - 2, gx + 2, gy + 2], fill=(90, 90, 96))
    pins = [(0.55, 0.30, "Antalya"), (0.60, 0.42, "Bahrain"),
            (0.53, 0.24, "Kyiv"), (0.82, 0.40, "Jakarta")]
    for fx, fy, _name in pins:
        px, py = x0 + int(fx * w), y0 + int(fy * h)
        draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED)
        draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255, 255, 255))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 28  # margin

    # ---- masthead
    d.line([mx, 10, W - mx, 10], fill=INK, width=4)
    f_mast = font(SERIF, 62)
    t = "THE WORLD IN ONE DAY"
    d.text(((W - d.textlength(t, font=f_mast)) / 2, 16), t, font=f_mast, fill=INK)
    f_date = font(SANS_B, 30)
    t2 = "SUNDAY 22 NOVEMBER 2026"
    d.text(((W - d.textlength(t2, font=f_date)) / 2, 84), t2, font=f_date, fill=RED)
    f_sub = font(SANS_B, 15)
    t3 = "35 DATED STORIES  •  7 REGIONS  •  WIRES READ UP TO 11:00 UTC"
    d.text(((W - d.textlength(t3, font=f_sub)) / 2, 118), t3, font=f_sub, fill=GREY)
    d.line([mx, 140, W - mx, 140], fill=INK, width=2)

    # ---- stats strip
    stats = [("35", "STORIES"), ("7", "REGIONS"), ("186", "DRONES"),
             ("161", "DOWNED"), ("98.79%", "HK TURNOUT"), ("2", "TANKERS HIT")]
    sw = (W - 2 * mx) // 6
    for i, (num, lab) in enumerate(stats):
        x = mx + i * sw
        d.text((x + 8, 148), num, font=font(SANS_B, 22), fill=INK)
        d.text((x + 8, 174), lab, font=font(SANS_B, 11), fill=GREY)
        if i:
            d.line([x, 150, x, 190], fill=(200, 192, 168), width=1)
    d.line([mx, 196, W - mx, 196], fill=INK, width=1)

    # ---- 3 hero cards
    hy, hh = 204, 236
    cw = (W - 2 * mx - 16) // 3
    for i, (region, tg, tgcol, kind, bg, head, body, src) in enumerate(HEROES):
        x0 = mx + i * (cw + 8)
        x1 = x0 + cw
        d.rectangle([x0, hy, x1, hy + hh], outline=INK, width=2)
        draw_icon(d, (x0 + 2, hy + 2, x1 - 2, hy + 108), kind, bg)
        tag(d, x0 + 8, hy + 114, tg, tgcol)
        d.text((x0 + 8, hy + 136), region, font=font(SANS_B, 12), fill=GREY)
        f_h = font(SANS_B, 21)
        lines = wrap(d, head, f_h, cw - 16)
        y = hy + 154
        for ln in lines[:2]:
            d.text((x0 + 8, y), ln, font=f_h, fill=INK)
            y += 24
        f_b = font(SANS, 14)
        for ln in wrap(d, body, f_b, cw - 16)[:2]:
            d.text((x0 + 8, y), ln, font=f_b, fill=(60, 58, 50))
            y += 17
        d.text((x0 + 8, hy + hh - 18), "Source: " + src,
               font=font(SANS, 11), fill=GREY)

    # ---- region bar
    ry = 452
    d.text((mx, ry), "REGIONS:", font=font(SANS_B, 13), fill=INK)
    x = mx + 78
    for name, col in zip(REGIONS, REGION_COLORS):
        f = font(SANS_B, 12)
        w = d.textlength(name, font=f) + 16
        d.rounded_rectangle([x, ry - 2, x + w, ry + 16], radius=8, fill=col)
        d.text((x + 8, ry + 1), name, font=f, fill=(255, 255, 255))
        x += w + 6

    # ---- UTC strip
    uy = 482
    d.rectangle([mx, uy, W - mx, uy + 30], fill=(26, 26, 26))
    d.text((mx + 10, uy + 7), "THE DAY IN UTC", font=font(SANS_B, 13),
           fill=(240, 190, 60))
    x = mx + 150
    for tm, ev in UTC_EVENTS:
        d.text((x, uy + 7), tm, font=font(SANS_B, 13), fill=(240, 190, 60))
        x += 50
        d.text((x, uy + 8), ev, font=font(SANS, 12), fill=(240, 240, 235))
        x += d.textlength(ev, font=font(SANS, 12)) + 22

    # ---- 10 small cards, 5 x 2
    sy = 524
    scw = (W - 2 * mx - 32) // 5
    sch = 82
    for i, (num, tg, kind, bg, head, src) in enumerate(SMALL):
        r, c = divmod(i, 5)
        x0 = mx + c * (scw + 8)
        y0 = sy + r * (sch + 6)
        x1, y1 = x0 + scw, y0 + sch
        d.rectangle([x0, y0, x1, y1], outline=(180, 172, 148), width=1)
        draw_icon(d, (x0 + 1, y0 + 1, x0 + 48, y1 - 1), kind, bg)
        d.text((x0 + 54, y0 + 4), num + ".", font=font(SANS_B, 12), fill=RED)
        f_h = font(SANS_B, 13)
        lines = wrap(d, head, f_h, scw - 60)
        y = y0 + 20
        for ln in lines[:3]:
            d.text((x0 + 54, y), ln, font=f_h, fill=INK)
            y += 15
        d.text((x0 + 54, y1 - 15), tg + " - " + src,
               font=font(SANS, 10), fill=GREY)

    # ---- ALSO list, 22 stories in 2 columns
    ay = 700
    d.text((mx, ay), "ALSO ON SUNDAY  —  22 MORE STORIES",
           font=font(SANS_B, 16), fill=INK)
    d.line([mx, ay + 22, W - mx, ay + 22], fill=INK, width=1)
    col_w = (W - 2 * mx - 20) // 2
    for i, (num, head, tg, src) in enumerate(ALSO):
        col, row = divmod(i, 11)
        x0 = mx + col * (col_w + 20)
        y = ay + 28 + row * 17
        d.text((x0, y), num + ".", font=font(SANS_B, 12), fill=RED)
        d.text((x0 + 26, y), head, font=font(SANS, 12), fill=INK)
        tw = d.textlength("[" + tg + "]", font=font(SANS, 10))
        d.text((x0 + col_w - tw, y + 1), "[" + tg + "]",
               font=font(SANS, 10), fill=GREY)

    # ---- bottom: map left, DATE CHECK right
    by = 922
    d.text((mx, by - 2), "WHERE IT HAPPENED", font=font(SANS_B, 12), fill=INK)
    draw_map(d, mx, by + 14, mx + 300, by + 76)
    bx = mx + 330
    d.rectangle([bx, by, W - mx, by + 76], outline=RED, width=3)
    d.text((bx + 10, by + 5), "DATE CHECK", font=font(SANS_B, 15), fill=RED)
    f_dc = font(SANS, 12)
    dc_lines = [
        "Wires read up to 11:00 UTC. Tonight's barrage was 186, not 400.",
        "Left out - not 22 Nov: El Chapo Isidro arrested Fri night; 400-drone",
        "barrage Fri 19-20 Nov; Peru quake Fri; Kryvyi Rih double-tap Fri;",
        "Shenzhen summit Thu 19 Nov. Claims are labelled CLAIM, not fact.",
    ]
    y = by + 25
    for ln in dc_lines:
        d.text((bx + 10, y), ln, font=f_dc, fill=INK)
        y += 12
    d.text((mx, H - 14), "Sources: Reuters, AP, AFP, BBC, NATO, ESA, SCMP, KBS, ICJ, USGS.",
           font=font(SANS, 10), fill=GREY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, format="PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
