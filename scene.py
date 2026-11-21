"""The VELMORA poster composition, drawn procedurally on a 1024x1024 canvas.

Layout (top to bottom), leading the eye name -> landmark -> horizon:
  sky gradient (indigo dusk to peach horizon) + early stars
  low golden sun on the horizon
  the floating island: rock, skyline and the glass lighthouse, its beam
  a hot-air balloon and a few birds for scale
  a sea of clouds the island floats above
  a cream footer band carrying the place name, a gold rule and the tagline

Everything is deterministic: star and window positions come from fixed
arithmetic, never from an unseeded random source.
"""

from palette import (
    INDIGO, INDIGO_DEEP, VIOLET, PEACH, PEACH_SOFT, GOLD, GOLD_BRIGHT,
    CREAM, CREAM_SHADOW, CLOUD_LILAC, TEAL, TEAL_DEEP, ROCK, ROCK_LIT,
)
from font import draw_text, draw_text_centred

W = 1024
H = 1024
FOOTER_Y = 800


def _stars(canvas):
    """Early stars in the top of the sky, fixed seeded positions."""
    import random
    rng = random.Random(20261121)
    for _ in range(70):
        x = rng.randrange(W)
        y = rng.randrange(290)
        if rng.random() < 0.3:
            canvas.disc(x, y, 2, CREAM)
        else:
            canvas.set(x, y, CREAM)


def _sun(canvas):
    cx, cy, r = 805, 455, 78
    canvas.disc(cx, cy, r, GOLD)
    canvas.disc(cx, cy - 10, 52, GOLD_BRIGHT)


def _balloon(canvas, cx, cy):
    """A small striped hot-air balloon drifting left of the island."""
    canvas.disc(cx, cy, 38, GOLD)
    canvas.ellipse(cx - 20, cy, 11, 38, INDIGO)
    canvas.ellipse(cx + 20, cy, 11, 38, INDIGO)
    canvas.disc(cx, cy - 9, 13, GOLD_BRIGHT)
    # ropes + basket
    canvas.polygon([(cx - 13, cy + 33), (cx - 9, cy + 33),
                    (cx - 11, cy + 50), (cx - 15, cy + 50)], INDIGO)
    canvas.polygon([(cx + 13, cy + 33), (cx + 9, cy + 33),
                    (cx + 11, cy + 50), (cx + 15, cy + 50)], INDIGO)
    canvas.fill_rect(cx - 13, cy + 50, cx + 13, cy + 64, INDIGO)


def _bird(canvas, x, y, s):
    canvas.polygon([(x, y), (x + 7 * s, y - 5 * s),
                    (x + 14 * s, y), (x + 7 * s, y - 1 * s)], INDIGO)


def _building(canvas, x, base_y, w, h, roof):
    """One skyline building: body, pointed or domed roof, lit windows."""
    canvas.fill_rect(x, base_y - h, x + w, base_y, INDIGO)
    if roof == "point":
        canvas.polygon([(x, base_y - h), (x + w // 2, base_y - h - 22),
                        (x + w, base_y - h)], INDIGO)
    else:  # dome
        canvas.ellipse(x + w // 2, base_y - h, w // 2, 14, INDIGO)
    for wy in range(base_y - h + 10, base_y - 8, 16):
        for wx in range(x + 6, x + w - 5, 12):
            if (wx * 7 + wy * 13) % 5 < 2:
                canvas.fill_rect(wx, wy, wx + 4, wy + 6, GOLD)


def _lighthouse(canvas, cx, base_y):
    """The glass lighthouse: teal tower, gold lamp, beam across the sky."""
    # beam first (behind the tower, in front of the sky): a short, bright
    # cone from the lamp — strong warm alpha so it reads as light, not
    # a grey stripe, over the dark indigo sky
    beam = (255, 232, 175)
    canvas.blend_polygon(
        [(cx + 10, 234), (720, 200), (720, 280), (cx + 10, 256)],
        beam, 0.70)
    canvas.blend_polygon(
        [(cx - 10, 234), (360, 210), (360, 262), (cx - 10, 256)],
        beam, 0.70)
    # tower
    canvas.polygon([(cx - 22, base_y), (cx - 16, 250),
                    (cx + 16, 250), (cx + 22, base_y)], TEAL_DEEP)
    canvas.polygon([(cx - 16, 250), (cx - 12, 250),
                    (cx - 12, base_y), (cx - 16, base_y)], TEAL)
    for wy in range(280, base_y - 10, 26):
        canvas.fill_rect(cx - 11, wy, cx + 11, wy + 12, GOLD_BRIGHT)
    # lamp room + cap
    canvas.fill_rect(cx - 20, 224, cx + 20, 252, INDIGO)
    canvas.fill_rect(cx - 14, 230, cx + 14, 246, GOLD_BRIGHT)
    canvas.polygon([(cx - 22, 224), (cx, 204), (cx + 22, 224)], GOLD)
    canvas.disc(cx, 200, 5, GOLD_BRIGHT)
    canvas.blend_ellipse(cx, 238, 36, 22, GOLD, 0.25)


def _island(canvas):
    """The floating rock with its skyline, hanging vines and waterfall."""
    # waterfall first (clouds will cover its foot)
    canvas.polygon([(498, 640), (526, 640), (518, 780), (506, 780)],
                   CREAM)
    # rock: wide flat top tapering to a point below
    canvas.polygon([(322, 400), (702, 400), (640, 520),
                    (512, 660), (384, 520)], ROCK)
    # sunlit left edge of the rock
    canvas.polygon([(322, 400), (384, 400), (420, 520),
                    (384, 520)], ROCK_LIT)
    # hanging vines under the rim
    for i, vx in enumerate((360, 420, 470, 560, 620, 670)):
        canvas.polygon([(vx, 400), (vx + 8, 400),
                        (vx + 4, 400 + 26 + (i * 11) % 30)], TEAL_DEEP)
    # skyline on the rim
    base = 400
    specs = [
        (332, 26, 62, "point"), (362, 34, 96, "dome"),
        (400, 24, 54, "point"), (428, 30, 78, "dome"),
        (462, 26, 66, "point"), (566, 26, 70, "dome"),
        (596, 32, 92, "point"), (632, 26, 58, "dome"),
        (662, 30, 84, "point"),
    ]
    for x, w, h, roof in specs:
        _building(canvas, x, base, w, h, roof)
    _lighthouse(canvas, 512, base)


def _islet(canvas, cx, cy, s):
    """A distant tiny floating islet with one spire, for depth."""
    # shallow rock: wide flat top, gentle taper (reads as an islet, not an arrow)
    canvas.polygon([(cx - 44 * s, cy), (cx + 44 * s, cy),
                    (cx + 26 * s, cy + 20 * s), (cx, cy + 30 * s),
                    (cx - 26 * s, cy + 20 * s)], ROCK)
    canvas.fill_rect(cx - 5 * s, cy - 26 * s, cx + 5 * s, cy, INDIGO)
    canvas.polygon([(cx - 6 * s, cy - 26 * s), (cx, cy - 40 * s),
                    (cx + 6 * s, cy - 26 * s)], GOLD)
    canvas.fill_rect(cx - 2 * s, cy - 18 * s, cx + 2 * s, cy - 12 * s, GOLD)


def _cloud(canvas, cx, cy, rx, ry, colour):
    canvas.ellipse(cx, cy, rx, ry, colour)
    canvas.ellipse(cx - rx // 2, cy + ry // 3, rx // 2, ry // 2, colour)
    canvas.ellipse(cx + rx // 2, cy + ry // 3, rx // 2, ry // 2, colour)


def _cloud_sea(canvas):
    """Layered sea of clouds the island floats above."""
    # far lilac shadows
    for cx, cy, rx in ((180, 600, 200), (520, 585, 260), (880, 600, 210)):
        canvas.ellipse(cx, cy, rx, 46, CLOUD_LILAC)
    # main cream banks
    _cloud(canvas, 200, 660, 230, 70, CREAM)
    _cloud(canvas, 540, 640, 280, 80, CREAM)
    _cloud(canvas, 880, 665, 220, 66, CREAM)
    # nearer puffs with soft shadow beneath
    _cloud(canvas, 120, 730, 190, 58, CREAM_SHADOW)
    _cloud(canvas, 130, 716, 190, 56, CREAM)
    _cloud(canvas, 900, 732, 180, 56, CREAM_SHADOW)
    _cloud(canvas, 910, 718, 180, 54, CREAM)
    _cloud(canvas, 512, 745, 260, 62, CREAM_SHADOW)
    _cloud(canvas, 512, 732, 260, 60, CREAM)
    # small overlapping puffs to break the flat middle field
    _cloud(canvas, 330, 700, 130, 40, CREAM_SHADOW)
    _cloud(canvas, 335, 692, 130, 38, CREAM)
    _cloud(canvas, 700, 702, 130, 40, CREAM_SHADOW)
    _cloud(canvas, 695, 694, 130, 38, CREAM)


def _footer(canvas):
    """Cream band: place name, gold rule, tagline."""
    canvas.fill_rect(0, FOOTER_Y, W, H, CREAM)
    canvas.fill_rect(0, FOOTER_Y, W, FOOTER_Y + 6, GOLD)
    name = "VELMORA"
    scale = 16
    name_y = 828
    # warm offset shadow, then the indigo name on top
    draw_text(canvas, 512 - 656 // 2 + 5, name_y + 5, name, scale,
              PEACH, spacing=1)
    draw_text_centred(canvas, 512, name_y, name, scale, INDIGO, spacing=1)
    # gold rule under the name
    canvas.fill_rect(512 - 328, 954, 512 + 328, 959, GOLD)
    # tagline
    draw_text_centred(canvas, 512, 972, "SLEEP ABOVE THE CLOUDS", 5,
                      INDIGO, spacing=1)


def draw_poster(canvas):
    canvas.vertical_gradient(0, FOOTER_Y, [
        (0.0, INDIGO_DEEP),
        (0.30, INDIGO),
        (0.58, VIOLET),
        (0.82, PEACH),
        (1.0, PEACH_SOFT),
    ])
    _stars(canvas)
    _sun(canvas)
    _islet(canvas, 150, 470, 1)
    _islet(canvas, 905, 560, 1)
    _balloon(canvas, 215, 300)
    _bird(canvas, 700, 250, 1)
    _bird(canvas, 760, 285, 1)
    _bird(canvas, 820, 240, 1)
    _island(canvas)
    _cloud_sea(canvas)
    _footer(canvas)
