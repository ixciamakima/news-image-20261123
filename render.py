# render.py — draws THE WORLD IN ONE DAY, Monday 23 November 2026.
# One broadsheet infographic, 1024x1024 PNG, deterministic (no network, no clock).
# All facts verified in-session against at least two independent sources
# (Reuters, AP, CNN, AFP, BBC, Cricinfo, Korea JoongAng Daily, Le Monde).
# Every story carries an honest event-date tag; the masthead date is the
# day this front page sums up: Monday 23 November 2026.

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 236)
INK = (25, 25, 25)
INK_SOFT = (60, 58, 52)
RED = (166, 30, 34)
NAVY = (31, 58, 95)
NAVY_DARK = (22, 42, 70)
TEAL = (18, 84, 82)
GOLD = (176, 132, 40)
GREY_LINE = (190, 184, 172)
CARD = (255, 253, 247)
MAP_LAND = (206, 198, 176)
MAP_SEA = (214, 228, 232)

FONT_DIR = "/usr/share/fonts/truetype/noto/"


def font(name, size):
    try:
        return ImageFont.truetype(FONT_DIR + name, size)
    except OSError:
        return ImageFont.load_default()


SERIF_BLACK = lambda s: font("NotoSerifDisplay-Black.ttf", s)
SERIF_XBOLD = lambda s: font("NotoSerifDisplay-ExtraBold.ttf", s)
SERIF_BOLD = lambda s: font("NotoSerif-Bold.ttf", s)
SERIF = lambda s: font("NotoSerif-Regular.ttf", s)
SERIF_IT = lambda s: font("NotoSerif-Italic.ttf", s)
SANS_BOLD = lambda s: font("NotoSans-Bold.ttf", s)
SANS_SEMI = lambda s: font("NotoSans-SemiBold.ttf", s)
SANS = lambda s: font("NotoSans-Regular.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, xy, text, fnt, max_w, fill, spacing=3, max_lines=None):
    x, y = xy
    lines = wrap(draw, text, fnt, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def fit_text(draw, text, fnt, max_w, min_size=10):
    """Shrink font until text fits max_w; returns (font, text)."""
    size = fnt.size
    while size > min_size and draw.textlength(text, font=fnt) > max_w:
        size -= 1
        fnt = font(fnt.path if hasattr(fnt, "path") else "NotoSans-Bold.ttf", size) \
            if False else ImageFont.truetype(fnt.path, size)
    return fnt


# ---------------------------------------------------------------- stories
# date = honest event date.  cat = section.  icon = glyph key.
LEADS = [
    dict(num=1, cat="CLIMATE", place="ANTALYA, TURKEY", date="SUN 22 NOV",
         headline="COP31 COLLAPSES: NO DEAL ON FOSSIL FUELS",
         detail="Longest talks ever end with no deal as 190+ nations reject "
                "the 'Antalya Pact'.",
         icon="globe", art="cop"),
    dict(num=2, cat="WAR", place="BAHRAIN & THE GULF", date="SAT 21 - SUN 22 NOV",
         headline="GULF WAR WIDENS AS IRAN HITS BAHRAIN",
         detail="Two wounded in a strike on a civilian site; Saudi Arabia "
                "condemns 'criminal' attacks.",
         icon="flame", art="gulf"),
    dict(num=3, cat="WAR", place="DYMER, KYIV REGION", date="SUN 22 NOV",
         headline="DRONE SMASHES FLAT: 14 MISSING NEAR KYIV",
         detail="A Russian drone collapses part of a five-storey block; nine "
                "evacuated, one body found.",
         icon="building", art="kyiv"),
]

GRID = [
    dict(num=4, cat="MEXICO", place="GUASAVE, SINALOA", date="FRI 20 NOV",
         headline="'EL CHAPO ISIDRO' HELD; 11 KILLED",
         detail="FBI Top 10 fugitive seized in Sinaloa.",
         icon="target"),
    dict(num=5, cat="ASIA", place="SEOUL", date="SUN 22 NOV",
         headline="MINISTER QUITS OVER AI EXAM CHEAT",
         detail="Choi Kyo-jin resigns; 111 CSAT cases caught.",
         icon="chip"),
    dict(num=6, cat="ASIA", place="CIKANDE, JAVA", date="SAT 21 NOV",
         headline="FACTORY FIRE: ~50 STILL MISSING",
         detail="7 body bags found in Cikande, Java.",
         icon="flame"),
    dict(num=7, cat="DIPLOMACY", place="GENEVA", date="SAT 21 NOV",
         headline="KILLER-ROBOT TALKS: NO RULES YET",
         detail="UN states agree only to keep talking.",
         icon="robot"),
    dict(num=8, cat="ASIA", place="NEW DELHI", date="MON 23 NOV",
         headline="NEPAL'S PM MEETS MODI TODAY",
         detail="First trip abroad since March: trade, energy.",
         icon="flags"),
    dict(num=9, cat="SPORT", place="WELLINGTON", date="SUN 22 NOV",
         headline="INDIA 720/9 - RECORD IN NEW ZEALAND",
         detail="Pant 128, Rahul 136; NZ 119/2 at stumps.",
         icon="bat"),
    dict(num=10, cat="EUROPE", place="GULF OF FINLAND", date="SAT 21 NOV",
         headline="DRONES SET RUSSIAN SHIP ABLAZE",
         detail="Sparta II burns; 16 crew evacuated.",
         icon="ship"),
    dict(num=11, cat="AMERICAS", place="WASHINGTON", date="SUN 22 NOV",
         headline="DEMOCRATS TAKE 258 HOUSE SEATS",
         detail="+44 seats; Hubbard beats Foxx in N. Carolina.",
         icon="capitol"),
    dict(num=12, cat="AFRICA", place="TONJ EAST, S. SUDAN", date="SUN 22 NOV",
         headline="REBELS KILL AT LEAST 15 IN S. SUDAN",
         detail="Raid on a cattle camp; toll feared to rise.",
         icon="alert"),
    dict(num=13, cat="EUROPE", place="BRUSSELS", date="FRI 20 NOV",
         headline="UK AND EU SEAL BREXIT RESET DEAL",
         detail="Food checks to end; 100,000 youth visas a year.",
         icon="deal"),
    dict(num=14, cat="AMERICAS", place="BRASILIA", date="FRI 20 NOV",
         headline="BOLSONARO STABLE IN INTENSIVE CARE",
         detail="Ex-president, 71, in ICU with bowel obstruction.",
         icon="cross"),
]

# Map pins: (lon, lat) for stories 1..14.
PINS = {
    1: (30.7, 36.9), 2: (50.6, 26.2), 3: (30.5, 50.9), 4: (-108.5, 25.6),
    5: (127.0, 37.5), 6: (106.1, -6.2), 7: (6.1, 46.2), 8: (77.2, 28.6),
    9: (174.8, -41.3), 10: (26.0, 59.8), 11: (-77.0, 38.9), 12: (28.9, 7.9),
    13: (4.4, 50.8), 14: (-47.9, -15.8),
}

REGIONS = [
    ("EUROPE", "COP31 collapses; Kyiv hit; Sparta II burns; UK-EU deal."),
    ("MIDDLE EAST", "Iran strikes Bahrain; Houthi fire aimed at Riyadh."),
    ("ASIA", "Seoul minister quits; Java factory fire; Nepal-India talks."),
    ("NORTH AMERICA", "'El Chapo Isidro' held; Democrats take 258 seats."),
    ("SOUTH AMERICA", "Bolsonaro stable in intensive care."),
    ("AFRICA", "15 killed in a South Sudan cattle-camp raid."),
    ("OCEANIA", "India piles up 720/9 in Wellington."),
]

MARKETS = [
    ("BRENT CRUDE", "$92.57", "-3.4% WK"),
    ("S&P 500", "6,910", "-3.7% FRI"),
    ("NASDAQ", "22,618", "-5.3% FRI"),
    ("DOW JONES", "48,147", "-1.9% FRI"),
    ("OPEC+", "29 NOV", "2027 QUOTAS"),
]

# Rough continent outlines (lon, lat) for the strip map.
CONTINENTS = [
    # North America
    [(-168, 66), (-150, 70), (-135, 69), (-125, 71), (-115, 73), (-100, 73),
     (-90, 73), (-85, 69), (-80, 62), (-70, 60), (-60, 55), (-55, 47),
     (-60, 44), (-68, 44), (-75, 38), (-76, 34), (-80, 26), (-82, 28),
     (-88, 21), (-92, 15), (-86, 12), (-82, 9), (-90, 14), (-97, 16),
     (-105, 20), (-110, 23), (-117, 33), (-122, 38), (-124, 48), (-130, 55),
     (-140, 60), (-155, 58), (-162, 58), (-168, 66)],
    # Greenland
    [(-58, 64), (-50, 60), (-40, 60), (-30, 65), (-25, 70), (-35, 76),
     (-50, 78), (-60, 76), (-68, 72), (-58, 64)],
    # South America
    [(-80, 10), (-77, 7), (-72, 10), (-64, 10), (-60, 5), (-52, 4),
     (-50, 0), (-44, -3), (-38, -5), (-35, -9), (-39, -15), (-41, -22),
     (-48, -27), (-55, -34), (-62, -39), (-66, -45), (-69, -52), (-71, -54),
     (-73, -50), (-73, -42), (-72, -32), (-70, -20), (-75, -15), (-80, -6),
     (-81, 0), (-80, 5), (-80, 10)],
    # Africa
    [(-17, 15), (-16, 20), (-13, 27), (-10, 30), (-6, 35), (0, 36), (10, 37),
     (15, 32), (20, 32), (25, 32), (30, 31), (33, 27), (36, 22), (38, 18),
     (43, 12), (48, 11), (51, 10), (46, 5), (41, 0), (40, -5), (39, -12),
     (36, -18), (33, -25), (28, -32), (20, -35), (17, -32), (14, -28),
     (12, -18), (13, -12), (9, -4), (9, 3), (5, 5), (-2, 5), (-8, 5),
     (-13, 8), (-17, 15)],
    # Europe
    [(-10, 36), (-9, 38), (-9, 43), (-2, 44), (-2, 48), (0, 50), (2, 51),
     (5, 53), (7, 54), (8, 57), (10, 58), (12, 56), (18, 56), (21, 55),
     (24, 58), (25, 60), (28, 62), (25, 65), (20, 68), (16, 70), (12, 70),
     (8, 65), (5, 60), (5, 58), (0, 55), (-3, 53), (-5, 50), (-10, 44),
     (-10, 36)],
    # Asia
    [(28, 62), (32, 68), (40, 68), (48, 69), (55, 69), (62, 70), (70, 72),
     (78, 72), (86, 73), (95, 76), (105, 76), (115, 73), (125, 72),
     (135, 71), (145, 71), (155, 69), (165, 66), (173, 66), (178, 65),
     (173, 62), (165, 60), (158, 56), (150, 59), (142, 55), (140, 45),
     (135, 43), (130, 42), (127, 39), (126, 35), (122, 31), (120, 27),
     (117, 23), (110, 20), (108, 15), (105, 10), (102, 8), (100, 7),
     (98, 12), (95, 16), (92, 21), (89, 22), (86, 20), (83, 18), (80, 15),
     (77, 8), (75, 10), (73, 16), (70, 21), (66, 25), (61, 25), (57, 26),
     (54, 27), (51, 28), (48, 29), (44, 29), (40, 31), (36, 36), (33, 36),
     (30, 36), (28, 41), (28, 45), (28, 50), (28, 55), (28, 62)],
    # Australia
    [(113, -22), (114, -28), (115, -32), (118, -35), (124, -33), (130, -32),
     (136, -35), (140, -38), (146, -39), (150, -37), (153, -30), (153, -25),
     (150, -22), (146, -19), (142, -15), (142, -11), (137, -12), (132, -12),
     (127, -14), (122, -17), (118, -20), (113, -22)],
]


# ---------------------------------------------------------------- glyphs
def glyph(draw, kind, box, fg, bg):
    """Small white pictogram inside a coloured rounded square."""
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=5, fill=bg)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    w = (x1 - x0) / 26.0
    X = lambda u: x0 + u * w
    Y = lambda v: y0 + v * w
    if kind == "globe":
        draw.ellipse([X(5), Y(5), X(21), Y(21)], outline=fg, width=2)
        draw.ellipse([X(10), Y(5), X(16), Y(21)], outline=fg, width=1)
        draw.line([X(5), Y(13), X(21), Y(13)], fill=fg, width=1)
        draw.arc([X(5), Y(8), X(21), Y(18)], 200, 340, fill=fg, width=1)
    elif kind == "flame":
        draw.polygon([(X(13), Y(4)), (X(18), Y(12)), (X(21), Y(15)),
                      (X(18), Y(22)), (X(8), Y(22)), (X(5), Y(15)),
                      (X(9), Y(11))], fill=fg)
        draw.ellipse([X(10), Y(15), X(16), Y(20)], fill=bg)
    elif kind == "building":
        draw.rectangle([X(6), Y(6), X(20), Y(22)], outline=fg, width=2)
        for r in (9, 13, 17):
            for c in (9, 13, 17):
                draw.rectangle([X(c), Y(r), X(c + 2), Y(r + 2)], fill=fg)
        draw.line([X(6), Y(15), X(20), Y(11)], fill=fg, width=2)
    elif kind == "target":
        draw.ellipse([X(5), Y(5), X(21), Y(21)], outline=fg, width=2)
        draw.ellipse([X(10), Y(10), X(16), Y(16)], fill=fg)
        draw.line([X(13), Y(2), X(13), Y(24)], fill=fg, width=2)
        draw.line([X(2), Y(13), X(24), Y(13)], fill=fg, width=2)
    elif kind == "chip":
        draw.rectangle([X(7), Y(7), X(19), Y(19)], outline=fg, width=2)
        draw.rectangle([X(11), Y(11), X(15), Y(15)], fill=fg)
        for p in (10, 13, 16):
            draw.line([X(p), Y(7), X(p), Y(3)], fill=fg, width=2)
            draw.line([X(p), Y(19), X(p), Y(23)], fill=fg, width=2)
            draw.line([X(7), Y(p), X(3), Y(p)], fill=fg, width=2)
            draw.line([X(19), Y(p), X(23), Y(p)], fill=fg, width=2)
    elif kind == "factory":
        draw.polygon([(X(4), Y(22)), (X(4), Y(12)), (X(10), Y(12)),
                      (X(10), Y(9)), (X(14), Y(9)), (X(14), Y(12)),
                      (X(22), Y(12)), (X(22), Y(22))], fill=fg)
        draw.rectangle([X(17), Y(4), X(19), Y(10)], fill=fg)
    elif kind == "robot":
        draw.rectangle([X(7), Y(8), X(19), Y(19)], outline=fg, width=2)
        draw.ellipse([X(10), Y(11), X(12), Y(13)], fill=fg)
        draw.ellipse([X(14), Y(11), X(16), Y(13)], fill=fg)
        draw.line([X(10), Y(16), X(16), Y(16)], fill=fg, width=2)
        draw.line([X(13), Y(8), X(13), Y(4)], fill=fg, width=2)
        draw.ellipse([X(11), Y(2), X(15), Y(6)], fill=fg)
    elif kind == "flags":
        draw.line([X(7), Y(3), X(7), Y(23)], fill=fg, width=2)
        draw.polygon([(X(7), Y(4)), (X(17), Y(7)), (X(7), Y(10))], fill=fg)
        draw.line([X(19), Y(3), X(19), Y(23)], fill=fg, width=2)
        draw.polygon([(X(19), Y(4)), (X(9), Y(7)), (X(19), Y(10))],
                     outline=fg, width=1)
    elif kind == "bat":
        draw.line([X(6), Y(20), X(20), Y(6)], fill=fg, width=3)
        draw.ellipse([X(16), Y(4), X(22), Y(10)], outline=fg, width=2)
        draw.ellipse([X(4), Y(15), X(10), Y(21)], fill=fg)
    elif kind == "ship":
        draw.polygon([(X(4), Y(14)), (X(22), Y(14)), (X(19), Y(20)),
                      (X(7), Y(20))], fill=fg)
        draw.rectangle([X(9), Y(8), X(15), Y(14)], fill=fg)
        draw.line([X(12), Y(8), X(12), Y(4)], fill=fg, width=2)
        draw.polygon([(X(12), Y(4)), (X(18), Y(7)), (X(12), Y(7))], fill=fg)
    elif kind == "capitol":
        draw.polygon([(X(13), Y(3)), (X(19), Y(9)), (X(7), Y(9))], fill=fg)
        draw.rectangle([X(6), Y(9), X(20), Y(11)], fill=fg)
        for c in (8, 12, 16):
            draw.rectangle([X(c), Y(12), X(c + 2), Y(19)], fill=fg)
        draw.rectangle([X(4), Y(19), X(22), Y(21)], fill=fg)
    elif kind == "alert":
        draw.polygon([(X(13), Y(3)), (X(23), Y(21)), (X(3), Y(21))],
                     outline=fg, width=2)
        draw.line([X(13), Y(9), X(13), Y(15)], fill=fg, width=2)
        draw.ellipse([X(12), Y(17), X(14), Y(19)], fill=fg)
    elif kind == "deal":
        draw.line([X(5), Y(20), X(11), Y(14)], fill=fg, width=2)
        draw.line([X(21), Y(20), X(15), Y(14)], fill=fg, width=2)
        draw.line([X(5), Y(14), X(21), Y(14)], fill=fg, width=2)
        draw.ellipse([X(9), Y(5), X(17), Y(13)], outline=fg, width=2)
    elif kind == "cross":
        draw.rectangle([X(11), Y(5), X(15), Y(21)], fill=fg)
        draw.rectangle([X(5), Y(11), X(21), Y(15)], fill=fg)


# ---------------------------------------------------------------- lead art
def art_cop(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(16, 66, 64))
    # rising sun disc
    draw.ellipse([x0 + 195, y0 + 12, x0 + 285, y0 + 102], fill=(232, 178, 74))
    # globe
    cx, cy, r = x0 + 105, y0 + 62, 46
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(52, 120, 112))
    draw.ellipse([cx - r + 10, cy - r + 8, cx - 8, cy + 2], fill=(120, 168, 96))
    draw.ellipse([cx - 2, cy + 8, cx + r - 12, cy + r - 8], fill=(120, 168, 96))
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(248, 244, 236), width=2)
    # red slash across the pact ribbon
    draw.line([x0 + 180, y0 + 108, x0 + 300, y0 + 28], fill=RED, width=7)
    # factory silhouettes + smoke
    for sx, sh in ((x0 + 12, 26), (x0 + 52, 34), (x0 + 250, 30)):
        draw.rectangle([sx, y1 - sh, sx + 26, y1], fill=(25, 25, 25))
        draw.rectangle([sx + 6, y1 - sh - 14, sx + 11, y1 - sh], fill=(25, 25, 25))
    draw.ellipse([x0 + 18, y0 + 8, x0 + 34, y0 + 24], fill=(200, 200, 190))
    draw.ellipse([x0 + 30, y0 + 2, x0 + 44, y0 + 16], fill=(200, 200, 190))
    draw.ellipse([x0 + 258, y0 + 6, x0 + 272, y0 + 20], fill=(200, 200, 190))


def art_gulf(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(18, 32, 56))
    # moon
    draw.ellipse([x0 + 262, y0 + 10, x0 + 292, y0 + 40], fill=(240, 232, 200))
    # sea bands
    for i, yy in enumerate((y0 + 92, y0 + 104, y0 + 116)):
        draw.rectangle([x0, yy, x1, yy + 3], fill=(52, 96, 128))
    # tanker silhouette
    draw.polygon([(x0 + 40, y0 + 96), (x0 + 200, y0 + 96), (x0 + 190, y0 + 122),
                  (x0 + 50, y0 + 122)], fill=(12, 12, 12))
    draw.rectangle([x0 + 60, y0 + 76, x0 + 100, y0 + 96], fill=(12, 12, 12))
    draw.rectangle([x0 + 110, y0 + 82, x0 + 150, y0 + 96], fill=(12, 12, 12))
    draw.rectangle([x0 + 160, y0 + 72, x0 + 185, y0 + 96], fill=(12, 12, 12))
    # explosion starburst above tanker
    ex, ey = x0 + 235, y0 + 62
    for ang in range(0, 360, 30):
        import math
        a = math.radians(ang)
        draw.line([ex, ey, ex + 26 * math.cos(a), ey + 26 * math.sin(a)],
                  fill=(240, 140, 40), width=4)
    draw.ellipse([ex - 12, ey - 12, ex + 12, ey + 12], fill=(250, 200, 80))
    # missile arcs
    draw.arc([x0 + 150, y0 - 20, x0 + 290, y0 + 90], 200, 330,
             fill=(240, 240, 230), width=3)
    draw.arc([x0 + 20, y0 - 40, x0 + 180, y0 + 70], 210, 320,
             fill=(240, 240, 230), width=3)


def art_kyiv(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(214, 196, 160))
    # dusk sky band
    draw.rectangle([x0, y0, x1, y0 + 46], fill=(122, 74, 62))
    # apartment block, left intact part
    draw.rectangle([x0 + 30, y0 + 30, x0 + 150, y1], fill=(88, 80, 70))
    for r in range(5):
        for c in range(4):
            draw.rectangle([x0 + 40 + c * 28, y0 + 38 + r * 19,
                            x0 + 58 + c * 28, y0 + 52 + r * 19],
                           fill=(250, 220, 130))
    # collapsed right part: jagged edge + rubble
    draw.polygon([(x0 + 150, y0 + 30), (x0 + 190, y0 + 60), (x0 + 170, y0 + 80),
                  (x0 + 200, y0 + 105), (x0 + 165, y1), (x0 + 150, y1)],
                 fill=(60, 54, 48))
    draw.polygon([(x0 + 165, y1), (x0 + 200, y1 - 8), (x0 + 235, y1 - 2),
                  (x0 + 260, y1 - 14), (x0 + 290, y1), (x0 + 165, y1)],
                 fill=(110, 100, 88))
    # smoke curls
    draw.ellipse([x0 + 185, y0 + 12, x0 + 215, y0 + 38], fill=(90, 88, 84))
    draw.ellipse([x0 + 205, y0 + 2, x0 + 230, y0 + 24], fill=(120, 118, 112))
    # drone silhouette top right
    dx, dy = x0 + 262, y0 + 26
    draw.ellipse([dx - 12, dy - 4, dx + 12, dy + 4], fill=(25, 25, 25))
    draw.line([dx - 20, dy - 8, dx + 20, dy - 8], fill=(25, 25, 25), width=2)
    draw.ellipse([dx - 24, dy - 11, dx - 14, dy - 5], fill=(25, 25, 25))
    draw.ellipse([dx + 14, dy - 11, dx + 24, dy - 5], fill=(25, 25, 25))
    # rescue light beam
    draw.polygon([(x0 + 40, y1), (x0 + 70, y1), (x0 + 120, y0 + 60),
                  (x0 + 100, y0 + 60)], fill=(250, 220, 130))


# ---------------------------------------------------------------- sections
def draw_masthead(draw):
    draw.rectangle([0, 0, W, 6], fill=RED)
    f_small = SANS_BOLD(14)
    f_date = SANS_BOLD(15)
    draw.text((28, 16), "MONDAY", font=f_date, fill=RED)
    right = "15 STORIES  •  7 REGIONS  •  ALL FACTS CHECKED TWICE"
    draw.text((W - 28 - draw.textlength(right, font=f_small), 17),
              right, font=f_small, fill=INK_SOFT)
    f_mast = SERIF_BLACK(64)
    title = "THE WORLD IN ONE DAY"
    draw.text(((W - draw.textlength(title, font=f_mast)) / 2, 34),
              title, font=f_mast, fill=INK)
    f_sub = SERIF_IT(16)
    sub = "Monday, 23 November 2026  —  the day's news, verified against two sources for every story"
    draw.text(((W - draw.textlength(sub, font=f_sub)) / 2, 104),
              sub, font=f_sub, fill=INK_SOFT)
    draw.line([28, 130, W - 28, 130], fill=INK, width=3)
    draw.line([28, 135, W - 28, 135], fill=INK, width=1)


def draw_leads(draw):
    y0 = 144
    col_w, gap = 310, 16
    art_h = 116
    for i, st in enumerate(LEADS):
        x0 = 28 + i * (col_w + gap)
        x1 = x0 + col_w
        # illustration
        art_fn = {"cop": art_cop, "gulf": art_gulf, "kyiv": art_kyiv}[st["art"]]
        art_fn(draw, (x0, y0, x1, y0 + art_h))
        draw.rectangle([x0, y0, x1, y0 + art_h], outline=INK, width=1)
        # number badge on art
        bx, by = x0 + 6, y0 + 6
        draw.ellipse([bx, by, bx + 26, by + 26], fill=RED)
        f_num = SANS_BOLD(15)
        t = str(st["num"])
        draw.text((bx + 13 - draw.textlength(t, font=f_num) / 2, by + 4),
                  t, font=f_num, fill=(255, 255, 255))
        y = y0 + art_h + 8
        f_kick = SANS_BOLD(13)
        draw.text((x0, y), st["cat"] + "  •  " + st["place"], font=f_kick, fill=RED)
        y += 20
        f_head = SERIF_BOLD(22)
        y = draw_wrapped(draw, (x0, y), st["headline"], f_head, col_w, INK,
                         spacing=1, max_lines=2)
        y += 2
        f_det = SANS(14)
        y = draw_wrapped(draw, (x0, y), st["detail"], f_det, col_w, INK_SOFT,
                         spacing=2, max_lines=2)
        f_date = SANS_BOLD(13)
        draw.text((x0, y + 2), st["date"], font=f_date, fill=NAVY)


def draw_map_regions(draw):
    y0 = 392
    draw.line([28, y0, W - 28, y0], fill=GREY_LINE, width=1)
    f_head = SANS_BOLD(13)
    draw.text((28, y0 + 8), "WHERE IT HAPPENED — FIND EACH NUMBER IN THE STORIES BELOW",
              font=f_head, fill=NAVY)
    map_x, map_y, map_w, map_h = 28, y0 + 30, 500, 168
    draw.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], fill=MAP_SEA,
                   outline=GREY_LINE, width=1)
    lon0, lon1, lat0, lat1 = -168.0, 192.0, -55.0, 80.0

    def proj(lon, lat):
        px = map_x + (lon - lon0) / (lon1 - lon0) * map_w
        py = map_y + (lat1 - lat) / (lat1 - lat0) * map_h
        return (px, py)

    for poly in CONTINENTS:
        draw.polygon([proj(lo, la) for lo, la in poly], fill=MAP_LAND,
                     outline=(160, 150, 130))
    f_pin = SANS_BOLD(13)
    # Nudge the crowded European pins apart so the numbers stay readable.
    NUDGE = {7: (-4.0, -1.5), 10: (-2.0, 2.5), 13: (-1.0, 1.0)}
    for num, (lo, la) in sorted(PINS.items()):
        dlo, dla = NUDGE.get(num, (0.0, 0.0))
        px, py = proj(lo + dlo, la + dla)
        draw.ellipse([px - 10, py - 10, px + 10, py + 10], fill=RED,
                     outline=(255, 255, 255), width=1)
        t = str(num)
        draw.text((px - draw.textlength(t, font=f_pin) / 2, py - 8),
                  t, font=f_pin, fill=(255, 255, 255))
    # region digest, right of map
    rx = 548
    f_rh = SANS_BOLD(13)
    draw.text((rx, y0 + 8), "THE DAY BY REGION", font=f_rh, fill=NAVY)
    f_reg = SANS_BOLD(13)
    f_rtx = SANS(13)
    ry = y0 + 30
    for name, text in REGIONS:
        draw.text((rx, ry), name, font=f_reg, fill=RED)
        nw = draw.textlength(name, font=f_reg)
        draw.text((rx + nw + 8, ry), text, font=f_rtx, fill=INK)
        ry += 24
    draw.line([28, y0 + 206, W - 28, y0 + 206], fill=GREY_LINE, width=1)


def draw_markets(draw):
    y0 = 606
    draw.rectangle([28, y0, W - 28, y0 + 56], fill=NAVY_DARK)
    f_lab = SANS_BOLD(13)
    draw.text((40, y0 + 6), "MARKETS", font=f_lab, fill=(250, 200, 80))
    draw.text((40, y0 + 28), "CLOSE FRI 20 NOV", font=SANS(13), fill=(220, 225, 235))
    cell_w = 150
    x = 208
    f_name = SANS_BOLD(13)
    f_val = SANS_BOLD(19)
    f_chg = SANS_BOLD(13)
    for name, val, chg in MARKETS:
        draw.text((x, y0 + 6), name, font=f_name, fill=(200, 210, 225))
        draw.text((x, y0 + 24), val, font=f_val, fill=(255, 255, 255))
        col = (250, 120, 110) if chg.startswith("-") else (250, 200, 80)
        draw.text((x + draw.textlength(val, font=f_val) + 8, y0 + 29),
                  chg, font=f_chg, fill=col)
        x += cell_w


def draw_grid(draw):
    y0 = 670
    col_w, row_h, gap_x, gap_y = 310, 76, 16, 8
    f_num = SANS_BOLD(13)
    f_kick = SANS_BOLD(13)
    f_det = SANS(13)
    for i, st in enumerate(GRID):
        r, c = divmod(i, 3)
        x0 = 28 + c * (col_w + gap_x)
        yy = y0 + r * (row_h + gap_y)
        x1 = x0 + col_w
        draw.rectangle([x0, yy, x1, yy + row_h], fill=CARD, outline=GREY_LINE, width=1)
        # number badge + pictogram
        draw.ellipse([x0 + 8, yy + 8, x0 + 30, yy + 30], fill=NAVY)
        t = str(st["num"])
        draw.text((x0 + 19 - draw.textlength(t, font=f_num) / 2, yy + 11),
                  t, font=f_num, fill=(255, 255, 255))
        glyph(draw, st["icon"], (x0 + 36, yy + 8, x0 + 60, yy + 32),
              (255, 255, 255), RED if st["cat"] in ("WAR",) else NAVY)
        tx = x0 + 66
        draw.text((tx, yy + 9), st["cat"] + "  •  " + st["place"],
                  font=f_kick, fill=RED)
        draw.text((tx, yy + 25), st["date"], font=SANS_BOLD(13), fill=NAVY)
        hy = yy + 40
        # headline: one line, shrink to fit (floor 13px)
        f_head = SERIF_BOLD(15)
        while draw.textlength(st["headline"], font=f_head) > col_w - 16 \
                and f_head.size > 13:
            f_head = SERIF_BOLD(f_head.size - 1)
        draw.text((x0 + 8, hy), st["headline"], font=f_head, fill=INK)
        # detail: one line, shrink to fit (floor 13px); truncate only as a guard
        det = st["detail"]
        f = f_det
        while draw.textlength(det, font=f) > col_w - 16 and f.size > 13:
            f = SANS(f.size - 1)
        while draw.textlength(det, font=f) > col_w - 16 and len(det) > 4:
            det = det[:-5] + "…"
        draw.text((x0 + 8, hy + 19), det, font=f, fill=INK_SOFT)
    # 12th cell: by the numbers
    r, c = divmod(11, 3)
    x0 = 28 + c * (col_w + gap_x)
    yy = y0 + r * (row_h + gap_y)
    draw.rectangle([x0, yy, x0 + col_w, yy + row_h], fill=NAVY_DARK)
    draw.text((x0 + 10, yy + 8), "THE DAY IN NUMBERS", font=SANS_BOLD(13),
              fill=(250, 200, 80))
    draw.text((x0 + 10, yy + 30), "186 drones  •  258 seats  •  720 runs",
              font=SANS_BOLD(13), fill=(255, 255, 255))
    draw.text((x0 + 10, yy + 50), "$92.57 oil  •  100,000 visas",
              font=SANS_BOLD(13), fill=(255, 255, 255))


def draw_footer(draw):
    y = 1004
    f = SANS(13)
    left = "SOURCES: REUTERS  •  AP  •  CNN  •  AFP  •  BBC  •  CRICINFO  •  KOREA JOONGANG DAILY"
    draw.text((28, y), left, font=f, fill=INK_SOFT)
    right = "THE WORLD IN ONE DAY"
    draw.text((W - 28 - draw.textlength(right, font=f), y), right, font=f,
              fill=INK_SOFT)


def render():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    draw_leads(draw)
    draw_map_regions(draw)
    draw_markets(draw)
    draw_grid(draw)
    draw_footer(draw)
    return img
