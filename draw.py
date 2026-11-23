"""Render the 23 November 2026 world-news card (1024x1024) to entry.png.

Composition is fixed by the design brief: header, six 452x248 cards in a
two-column grid, footer. Icons are drawn at 4x and downsampled so the
small shapes stay clean at final size.
"""

from __future__ import annotations

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (11, 18, 32)
CARD = (21, 31, 49)
BORDER = (38, 52, 76)
TEXT = (242, 245, 250)
MUTED = (154, 169, 194)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

CARD_W, CARD_H = 452, 248
COLS = (48, 524)
ROWS = (164, 428, 692)
ICON = 96
ICON_SCALE = 4
TEXT_X = 140
TEXT_W = 290


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont, max_w: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_font(
    draw: ImageDraw.ImageDraw,
    text: str,
    base: ImageFont.FreeTypeFont,
    max_w: int,
    floor: int = 22,
) -> ImageFont.FreeTypeFont:
    """Largest size at or below the base size whose width fits max_w."""
    size = base.size
    while size > floor and draw.textlength(text, font=font(BOLD, size)) > max_w:
        size -= 1
    return font(BOLD, size)


# ---------------------------------------------------------------- icons ----
# Each icon draws into a 96*ICON_SCALE square and is pasted at the icon box.

S = ICON * ICON_SCALE


def _sc(v: float) -> int:
    return round(v * ICON_SCALE)


def icon_ship() -> Image.Image:
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    grey = (150, 160, 178)
    hull = (86, 104, 134)
    orange = (250, 158, 78)
    # hull, long and low in frame
    d.polygon(
        [(_sc(4), _sc(72)), (_sc(92), _sc(72)), (_sc(84), _sc(84)), (_sc(14), _sc(84))],
        fill=hull,
    )
    d.line([(_sc(4), _sc(72)), (_sc(92), _sc(72))], fill=(120, 140, 172), width=_sc(1.5))
    # small bridge tower, aft
    d.rectangle([_sc(62), _sc(54), _sc(74), _sc(72)], fill=hull)
    d.rectangle([_sc(65), _sc(58), _sc(71), _sc(62)], fill=(190, 205, 226))
    # three flames on the deck
    for cx in (24, 40, 56):
        d.polygon(
            [
                (_sc(cx), _sc(70)),
                (_sc(cx + 5), _sc(58)),
                (_sc(cx + 7), _sc(66)),
                (_sc(cx + 9), _sc(52)),
                (_sc(cx + 11), _sc(70)),
            ],
            fill=orange,
        )
        d.polygon(
            [(_sc(cx + 3), _sc(70)), (_sc(cx + 6), _sc(62)), (_sc(cx + 9), _sc(70))],
            fill=(255, 205, 120),
        )
    # grey smoke curl rising from the deck
    pts = [(_sc(44), _sc(54)), (_sc(38), _sc(46)), (_sc(32), _sc(38)), (_sc(36), _sc(29)),
           (_sc(48), _sc(22)), (_sc(58), _sc(17)), (_sc(62), _sc(12))]
    widths = (6, 6, 5, 5, 4, 3)
    for (x0, y0), (x1, y1), w in zip(pts, pts[1:], widths):
        d.line([(x0, y0), (x1, y1)], fill=grey, width=w, joint="curve")
    d.ellipse([_sc(56), _sc(6), _sc(70), _sc(20)], fill=(176, 186, 202))
    return img.resize((ICON, ICON), Image.LANCZOS)


def icon_barrel() -> Image.Image:
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    green = (120, 200, 140)
    body = (92, 112, 142)
    d.rounded_rectangle(
        [_sc(14), _sc(26), _sc(56), _sc(84)], radius=_sc(9), fill=body
    )
    for y in (42, 68):
        d.line([(_sc(14), _sc(y)), (_sc(56), _sc(y))], fill=(150, 170, 200), width=_sc(3))
    d.ellipse([_sc(24), _sc(20), _sc(46), _sc(32)], fill=(70, 88, 114))
    # green arrow rising to the right, past the barrel
    d.line(
        [(_sc(44), _sc(78)), (_sc(60), _sc(58)), (_sc(70), _sc(44)), (_sc(84), _sc(24))],
        fill=green,
        width=_sc(5),
        joint="curve",
    )
    d.polygon(
        [(_sc(88), _sc(18)), (_sc(72), _sc(24)), (_sc(84), _sc(36))],
        fill=green,
    )
    return img.resize((ICON, ICON), Image.LANCZOS)


def icon_asean() -> Image.Image:
    import math

    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cooler = (120, 170, 235)
    warmer = (236, 88, 76)
    cx, cy, ring_r, dot = 52.0, 48.0, 40.0, 3.6
    for i in range(10):
        a = math.radians(i * 36)
        x = cx + ring_r * math.cos(a)
        y = cy + ring_r * math.sin(a)
        d.ellipse(
            [_sc(x - dot), _sc(y - dot), _sc(x + dot), _sc(y + dot)], fill=cooler
        )
    ox, oy, orr = 5.5, 58.0, 3.9
    d.ellipse([_sc(ox - orr), _sc(oy - orr), _sc(ox + orr), _sc(oy + orr)], fill=warmer)
    return img.resize((ICON, ICON), Image.LANCZOS)


def icon_flood() -> Image.Image:
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    blue = (120, 170, 235)
    rock = (78, 96, 124)
    d.polygon(
        [(_sc(6), _sc(64)), (_sc(36), _sc(20)), (_sc(66), _sc(64))], fill=rock
    )
    d.polygon(
        [(_sc(28), _sc(31)), (_sc(36), _sc(20)), (_sc(45), _sc(32)),
         (_sc(40), _sc(35)), (_sc(36), _sc(30)), (_sc(31), _sc(36))],
        fill=(240, 245, 252),
    )
    # wave line crossing beneath the peak
    for dx in (0, 28, 56):
        d.arc(
            [_sc(2 + dx), _sc(64), _sc(30 + dx), _sc(80)],
            start=195,
            end=345,
            fill=blue,
            width=_sc(3.2),
        )
    # banknote, right
    d.rounded_rectangle([_sc(64), _sc(40), _sc(92), _sc(58)], radius=_sc(2), fill=(52, 80, 122))
    d.rounded_rectangle(
        [_sc(64), _sc(40), _sc(92), _sc(58)], radius=_sc(2), outline=blue, width=_sc(1.6)
    )
    d.ellipse([_sc(73), _sc(44.5), _sc(83), _sc(54.5)], outline=blue, width=_sc(1.4))
    return img.resize((ICON, ICON), Image.LANCZOS)


def icon_chip() -> Image.Image:
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    blue = (120, 170, 235)
    body = (46, 74, 116)
    d.rounded_rectangle([_sc(20), _sc(24), _sc(68), _sc(72)], radius=_sc(6), fill=body)
    d.rounded_rectangle(
        [_sc(20), _sc(24), _sc(68), _sc(72)], radius=_sc(6), outline=blue, width=_sc(2)
    )
    d.rounded_rectangle([_sc(32), _sc(36), _sc(56), _sc(60)], radius=_sc(3), outline=blue, width=_sc(1.5))
    # 12 pins, three per side
    for i in range(3):
        p = 28 + i * 13
        d.line([(_sc(20), _sc(p)), (_sc(12), _sc(p))], fill=blue, width=_sc(3))       # left
        d.line([(_sc(68), _sc(p)), (_sc(76), _sc(p))], fill=blue, width=_sc(3))       # right
        d.line([(_sc(p), _sc(24)), (_sc(p), _sc(16))], fill=blue, width=_sc(3))       # top
        d.line([(_sc(p), _sc(72)), (_sc(p), _sc(80))], fill=blue, width=_sc(3))       # bottom
    # faint circuit trace going right
    d.line(
        [(_sc(76), _sc(56)), (_sc(84), _sc(56)), (_sc(84), _sc(44)), (_sc(94), _sc(44))],
        fill=(84, 116, 162),
        width=_sc(1.6),
        joint="curve",
    )
    d.ellipse([_sc(91), _sc(41.5), _sc(96), _sc(46.5)], fill=(84, 116, 162))
    return img.resize((ICON, ICON), Image.LANCZOS)


def icon_globe() -> Image.Image:
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    green = (120, 200, 140)
    sea = (110, 160, 220)
    d.ellipse([_sc(10), _sc(12), _sc(82), _sc(84)], outline=sea, width=_sc(3))
    # two latitude arcs
    for top, bottom in ((26, 44), (52, 70)):
        d.arc([_sc(10), _sc(top), _sc(82), _sc(bottom)], start=0, end=180, fill=sea, width=_sc(2))
    # one longitude arc
    d.arc([_sc(34), _sc(12), _sc(58), _sc(84)], start=90, end=270, fill=sea, width=_sc(2))
    # small leaf, lower right
    d.polygon(
        [(_sc(74), _sc(84)), (_sc(94), _sc(64)), (_sc(92), _sc(80)), (_sc(80), _sc(88))],
        fill=green,
    )
    d.line([(_sc(76), _sc(86)), (_sc(92), _sc(70))], fill=(86, 160, 108), width=_sc(1.6))
    return img.resize((ICON, ICON), Image.LANCZOS)


def icon_house() -> Image.Image:
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    grey = (74, 84, 102)
    flame = (233, 120, 90)
    core = (250, 186, 128)
    # square body plus triangular roof, dark grey
    d.rectangle([_sc(16), _sc(52), _sc(76), _sc(86)], fill=grey)
    d.polygon(
        [(_sc(10), _sc(54)), (_sc(46), _sc(20)), (_sc(82), _sc(54))], fill=grey
    )
    # right side of the house replaced by an orange flame
    d.polygon(
        [
            (_sc(54), _sc(86)),
            (_sc(50), _sc(72)),
            (_sc(56), _sc(62)),
            (_sc(60), _sc(66)),
            (_sc(58), _sc(50)),
            (_sc(66), _sc(56)),
            (_sc(70), _sc(34)),
            (_sc(76), _sc(52)),
            (_sc(84), _sc(48)),
            (_sc(86), _sc(64)),
            (_sc(80), _sc(78)),
            (_sc(72), _sc(88)),
        ],
        fill=flame,
    )
    d.polygon(
        [(_sc(66), _sc(86)), (_sc(63), _sc(74)), (_sc(69), _sc(68)), (_sc(72), _sc(80))],
        fill=core,
    )
    return img.resize((ICON, ICON), Image.LANCZOS)


CARDS = [
    ("OFF FINLAND", "Cargo ship still burning", "Russia-linked", (233, 120, 90), icon_ship),
    ("GLOBAL MARKETS", "Brent crude at $124.77", "India imports +60%", (120, 200, 140), icon_barrel),
    ("NAYPYIDAW", "Myanmar rejects ASEAN ruling", "army-backed", (233, 120, 90), icon_asean),
    ("NEW DELHI", "Nepal asks for $2bn in flood aid", "$2bn", (120, 170, 235), icon_flood),
    ("SINGAPORE", "Chip-smuggling network uncovered", "Nvidia servers", (120, 170, 235), icon_chip),
    ("NARAIL, BANGLADESH", "Houses burned as unrest spreads", "30 homes", (233, 120, 90), icon_house),
]


# ---------------------------------------------------------------- card -----

def draw_card(img: Image.Image, x: int, y: int) -> None:
    """Card fill plus 2px rounded border, rendered at 4x then downsampled."""
    k = 4
    tile = Image.new("RGBA", (CARD_W * k, CARD_H * k), (0, 0, 0, 0))
    d = ImageDraw.Draw(tile)
    d.rounded_rectangle(
        [0, 0, CARD_W * k - 1, CARD_H * k - 1],
        radius=14 * k,
        fill=CARD,
        outline=BORDER,
        width=2 * k,
    )
    flat = tile.resize((CARD_W, CARD_H), Image.LANCZOS)
    img.paste(flat, (x, y), flat)


def render() -> Image.Image:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # header
    d.text((48, 40), "23 NOVEMBER 2026", font=font(BOLD, 56), fill=TEXT, anchor="lt")
    x = 48
    sub = font(REG, 20)
    for ch in "THE WORLD, ONE PICTURE":
        d.text((x, 104), ch, font=sub, fill=MUTED, anchor="lt")
        x += d.textlength(ch, font=sub) + 3
    d.line([(48, 140), (976, 140)], fill=BORDER, width=2)

    card_no = font(BOLD, 18)
    head = font(BOLD, 26)
    fig = font(BOLD, 34)
    fig_room = CARD_W - TEXT_X - 24

    for i, (place, headline, figure, accent, icon_fn) in enumerate(CARDS):
        cx = COLS[i % 2]
        cy = ROWS[i // 2]
        draw_card(img, cx, cy)
        ic = icon_fn()
        img.paste(ic, (cx + 24, cy + 28), ic)
        tx = cx + TEXT_X
        d.text((tx, cy + 30), place, font=card_no, fill=MUTED, anchor="lt")
        lines = wrap(d, headline, head, TEXT_W)
        for n, line in enumerate(lines[:2]):
            d.text((tx, cy + 58 + n * 33), line, font=head, fill=TEXT, anchor="lt")
        d.text(
            (tx, cy + 150),
            figure,
            font=fit_font(d, figure, fig, fig_room),
            fill=accent,
            anchor="lt",
        )

    # footer
    d.text(
        (976, 976),
        "make.fun \u00b7 news-image 23 November 2026",
        font=font(REG, 18),
        fill=MUTED,
        anchor="rt",
    )
    return img


if __name__ == "__main__":
    out = render()
    out.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png", out.size)
