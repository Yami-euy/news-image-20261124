# Renderer for THE TUESDAY GLOBE — Tuesday 24 November 2026.
# Draws the whole front page with Pillow. Fonts are bundled in the repo
# (fonts/) and loaded from there first, so the program does not depend on
# the sandbox having any system font installed.
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

import stories

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (26, 26, 26)
RED = (164, 30, 34)
BLUE = (31, 78, 121)
MUTED = (107, 101, 88)
RULE = (178, 170, 148)
LAND = (186, 197, 168)
LAND_EDGE = (118, 128, 102)
GREEN = (32, 116, 58)
LIGHT = (238, 233, 218)

_FONT_DIR = Path(__file__).resolve().parent / "fonts"

# (bundled file, system fallback path)
_SERIF = ("DejaVuSerif.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf")
_SERIFB = ("DejaVuSerif-Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf")
_SANS = ("DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
_SANSB = ("DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
_SERIFI = ("LiberationSerif-Italic.ttf", "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf")

_cache = {}


def font(spec, size):
    """Load a font: bundled copy first, system path second, default last."""
    key = (spec, size)
    if key in _cache:
        return _cache[key]
    bundled = _FONT_DIR / spec[0]
    f = None
    for path in (bundled, Path(spec[1])):
        try:
            f = ImageFont.truetype(str(path), size)
            break
        except Exception:
            continue
    if f is None:
        try:
            f = ImageFont.load_default(size)
        except Exception:
            f = ImageFont.load_default()
    _cache[key] = f
    return f


def wrap(d, text, fnt, width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, text, fnt, x, y, width, fill=INK, leading=None):
    """Draw a wrapped paragraph; return the y just below it."""
    leading = leading or int(fnt.size * 1.32)
    for line in wrap(d, text, fnt, width):
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# Simplified continent outlines, (lon, lat). Drawn, not traced from any
# other entry: these are my own coarse shapes.
NORTH_AMERICA = [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69),
                 (-85, 66), (-80, 73), (-70, 62), (-65, 60), (-55, 47),
                 (-60, 45), (-70, 42), (-75, 35), (-80, 32), (-81, 26),
                 (-84, 30), (-90, 21), (-97, 26), (-105, 20), (-110, 23),
                 (-115, 30), (-125, 40), (-125, 49), (-135, 58), (-155, 58),
                 (-165, 60), (-168, 66)]
GREENLAND = [(-58, 64), (-45, 60), (-40, 64), (-32, 68), (-25, 70),
             (-20, 74), (-30, 76), (-45, 76), (-58, 74), (-58, 64)]
SOUTH_AMERICA = [(-80, 9), (-77, 4), (-75, -5), (-81, -6), (-80, -15),
                 (-72, -18), (-70, -23), (-70, -30), (-72, -37), (-73, -44),
                 (-70, -52), (-66, -55), (-65, -45), (-62, -41), (-58, -35),
                 (-52, -32), (-48, -28), (-41, -23), (-35, -9), (-35, -6),
                 (-44, 2), (-50, 0), (-55, 6), (-62, 9), (-72, 11),
                 (-77, 8), (-80, 9)]
AFRICA = [(-6, 35), (-10, 31), (-15, 27), (-17, 21), (-17, 15), (-15, 11),
          (-12, 8), (-8, 5), (-4, 5), (2, 6), (6, 4), (9, 4), (9, -1),
          (12, -6), (13, -10), (12, -18), (14, -22), (16, -28), (20, -35),
          (26, -34), (32, -29), (35, -24), (40, -16), (40, -10), (42, -4),
          (46, -1), (51, 2), (51, 11), (44, 11), (40, 15), (38, 18),
          (37, 22), (34, 27), (32, 31), (25, 32), (19, 33), (11, 34),
          (10, 37), (5, 37), (-6, 35)]
EURASIA = [(-10, 36), (-9, 43), (-2, 48), (-4, 49), (0, 51), (3, 53),
           (8, 57), (10, 59), (5, 60), (5, 62), (10, 64), (18, 69),
           (25, 71), (32, 70), (40, 68), (50, 69), (60, 69), (70, 72),
           (75, 73), (80, 73), (90, 75), (100, 76), (110, 74), (120, 73),
           (130, 72), (140, 72), (150, 70), (158, 69), (162, 66), (170, 66),
           (178, 65), (178, 62), (170, 60), (162, 60), (158, 56), (156, 52),
           (150, 60), (142, 55), (140, 50), (135, 44), (130, 42), (127, 40),
           (122, 39), (120, 35), (122, 31), (120, 28), (118, 25), (112, 22),
           (108, 18), (105, 10), (104, 9), (100, 8), (98, 12), (94, 16),
           (92, 21), (89, 22), (86, 20), (82, 17), (80, 13), (77, 8),
           (75, 12), (72, 20), (68, 23), (66, 25), (62, 25), (58, 25),
           (54, 26), (52, 28), (50, 29), (48, 30), (48, 24), (44, 17),
           (42, 15), (40, 12), (38, 20), (36, 22), (34, 28), (33, 31),
           (30, 36), (27, 36), (23, 36), (19, 40), (15, 44), (12, 44),
           (8, 44), (3, 43), (-1, 38), (-9, 37), (-10, 36)]
AUSTRALIA = [(113, -22), (114, -30), (115, -35), (118, -35), (124, -33),
             (129, -32), (132, -32), (135, -35), (138, -35), (140, -38),
             (145, -38), (150, -37), (153, -32), (153, -27), (150, -22),
             (146, -19), (142, -11), (142, -15), (136, -12), (132, -11),
             (130, -13), (126, -14), (122, -17), (118, -20), (113, -22)]
BRITAIN = [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53),
           (1, 51), (-5, 50)]
JAPAN = [(130, 31), (132, 33), (134, 34), (137, 35), (139, 35), (140, 38),
         (141, 41), (143, 42), (145, 44), (141, 45), (139, 42), (137, 38),
         (134, 36), (132, 34), (130, 31)]
NEW_GUINEA = [(131, -1), (136, -2), (141, -3), (146, -6), (150, -10),
              (146, -8), (141, -8), (136, -6), (131, -4), (131, -1)]
BORNEO = [(109, 1), (113, 4), (117, 6), (119, 1), (117, -3), (113, -4),
          (110, -2), (109, 1)]
SUMATRA = [(95, 5), (98, 3), (101, 0), (104, -3), (106, -6), (103, -4),
           (100, -1), (97, 2), (95, 5)]
NEW_ZEALAND = [(167, -45), (170, -42), (174, -38), (177, -38), (175, -41),
               (172, -43), (167, -45)]

LANDS = [NORTH_AMERICA, GREENLAND, SOUTH_AMERICA, AFRICA, EURASIA,
         AUSTRALIA, BRITAIN, JAPAN, NEW_GUINEA, BORNEO, SUMATRA, NEW_ZEALAND]

LAT_TOP, LAT_BOT = 83.0, -55.0


def project(lon, lat, box):
    x0, y0, x1, y1 = box
    s = min((x1 - x0) / 360.0, (y1 - y0) / (LAT_TOP - LAT_BOT))
    w_used, h_used = 360.0 * s, (LAT_TOP - LAT_BOT) * s
    ox = x0 + (x1 - x0 - w_used) / 2.0
    oy = y0 + (y1 - y0 - h_used) / 2.0
    return (ox + (lon + 180.0) * s, oy + (LAT_TOP - lat) * s)


def draw_map(d, box):
    for land in LANDS:
        pts = [project(lon, lat, box) for lon, lat in land]
        d.polygon(pts, fill=LAND, outline=LAND_EDGE)


def draw_pin(d, box, number, lon, lat):
    x, y = project(lon, lat, box)
    r = 9
    d.ellipse([x - r, y - r, x + r, y + r], fill=RED, outline=(255, 255, 255), width=1)
    f = font(_SANSB, 10)
    tw = d.textlength(str(number), font=f)
    d.text((x - tw / 2, y - 7), str(number), font=f, fill=(255, 255, 255))


def rule(d, x0, x1, y, width=1):
    d.line([(x0, y), (x1, y)], fill=RULE, width=width)


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx, mx1 = 28, 996  # margins

    # ---- Masthead ----
    f_mast = font(_SERIFB, 56)
    t = stories.MASTHEAD
    d.text(((W - d.textlength(t, font=f_mast)) / 2, 12), t, font=f_mast, fill=INK)
    d.line([(mx, 82), (mx1, 82)], fill=INK, width=3)
    f_date = font(_SANSB, 15)
    d.text((mx, 88), stories.DATELINE, font=f_date, fill=RED)
    f_tag = font(_SANS, 12)
    tw = d.textlength(stories.TAGLINE, font=f_tag)
    d.text((mx1 - tw, 89), stories.TAGLINE, font=f_tag, fill=MUTED)
    rule(d, mx, mx1, 112, 1)

    # ---- Stat strip ----
    f_stat = font(_SANSB, 13)
    d.text((mx, 120), stories.STATS, font=f_stat, fill=BLUE)
    rule(d, mx, mx1, 142, 1)

    # ---- Lead story + chart ----
    lead = stories.LEAD
    f_kick = font(_SANSB, 13)
    d.text((mx, 152), lead["kicker"], font=f_kick, fill=RED)
    f_head = font(_SERIFB, 40)
    y = para(d, lead["headline"], f_head, mx, 172, 600, leading=44)
    f_sub = font(_SERIFI, 16)
    y = para(d, lead["subhead"], f_sub, mx, y + 2, 600, fill=MUTED, leading=21)
    f_body = font(_SANS, 14)
    para(d, lead["body"], f_body, mx, y + 8, 600, leading=19)

    # Chart box
    cx0, cx1, cy0, cy1 = 656, 996, 150, 316
    d.rectangle([cx0, cy0, cx1, cy1], outline=RULE, width=1)
    f_ct = font(_SANSB, 13)
    d.text((cx0 + 12, cy0 + 8), stories.CHART["title"], font=f_ct, fill=RED)
    bars = stories.CHART["bars"]
    maxv = max(v for _, v in bars)
    bx0, bx1 = cx0 + 92, cx1 - 64
    by = cy0 + 32
    f_bl = font(_SANSB, 12)
    f_bv = font(_SANS, 12)
    for name, val in bars:
        d.text((cx0 + 12, by), name, font=f_bl, fill=INK)
        bw = (bx1 - bx0) * val / maxv
        d.rectangle([bx0, by + 1, bx0 + bw, by + 13], fill=GREEN)
        d.text((bx0 + bw + 6, by), "+%.2f%%" % val, font=f_bv, fill=GREEN)
        by += 24
    f_cn = font(_SANS, 11)
    d.text((cx0 + 12, cy1 - 18),
           "Best day for the Nasdaq since April 2025.",
           font=f_cn, fill=MUTED)

    rule(d, mx, mx1, 326, 1)

    # ---- Two secondary stories ----
    col_w = 472
    f_sk = font(_SANSB, 12)
    f_sh = font(_SERIFB, 21)
    f_sb = font(_SANS, 13)
    for i, s in enumerate(stories.SECONDARY):
        x = mx + i * (col_w + 24)
        d.text((x, 336), s["kicker"], font=f_sk, fill=RED)
        y = para(d, s["headline"], f_sh, x, 356, col_w, leading=25)
        para(d, s["body"], f_sb, x, y + 4, col_w, leading=17)

    rule(d, mx, mx1, 458, 1)

    # ---- World map + ALSO ----
    f_sec = font(_SANSB, 13)
    d.text((mx, 468), "WHERE THE NEWS HAPPENED", font=f_sec, fill=RED)
    map_box = (mx, 490, 648, 640)
    draw_map(d, map_box)
    for num, _label, lon, lat in stories.PINS:
        draw_pin(d, map_box, num, lon, lat)
    f_leg = font(_SANS, 10)
    legend = ("1 Zaporizhzhia  2 Washington  3 Brussels  4 Tallinn  5 Warsaw  "
              "6 Singapore")
    legend2 = ("7 Seoul  8 Cikande  9 Piura  10 Rio Grande do Sul  11 Gaza  "
               "12 Khartoum")
    d.text((mx, 646), legend, font=f_leg, fill=MUTED)
    d.text((mx, 660), legend2, font=f_leg, fill=MUTED)

    ax0, ax1 = 664, 996
    d.text((ax0, 468), "ALSO ON TUESDAY", font=f_sec, fill=RED)
    f_ai = font(_SANS, 12)
    y = 492
    for item in stories.ALSO:
        d.rectangle([ax0, y + 4, ax0 + 6, y + 10], fill=RED)
        y = para(d, item, f_ai, ax0 + 14, y, ax1 - ax0 - 14, leading=15)
        y += 6

    rule(d, mx, mx1, 682, 1)

    # ---- Region grid: 4 columns x 2 rows ----
    col_w = 234
    gap = 10
    row_h = 132
    f_rh = font(_SANSB, 13)
    f_ri = font(_SANS, 11)
    for i, (region, items) in enumerate(stories.REGIONS):
        col, row = i % 4, i // 4
        x = mx + col * (col_w + gap)
        y = 692 + row * (row_h + 6)
        d.text((x, y), region, font=f_rh, fill=RED)
        d.line([(x, y + 18), (x + col_w, y + 18)], fill=RULE, width=1)
        yy = y + 24
        for item in items:
            d.rectangle([x, yy + 4, x + 5, yy + 9], fill=BLUE)
            yy = para(d, item, f_ri, x + 11, yy, col_w - 11, leading=14)
            yy += 4

    rule(d, mx, mx1, 962, 1)

    # ---- Footer ----
    f_ft = font(_SANS, 11)
    d.text((mx, 970), stories.FOOTER, font=f_ft, fill=MUTED)
    f_nt = font(_SANSB, 11)
    note = "Tuesday 24 November 2026 — the whole day, in one page."
    tw = d.textlength(note, font=f_nt)
    d.text((mx1 - tw, 988), note, font=f_nt, fill=INK)

    return img


if __name__ == "__main__":
    out = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out, exist_ok=True)
    render().save(os.path.join(out, "entry.png"))
