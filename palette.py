"""Palette for VELMORA — a floating city above the clouds at sunset.

Purposeful, limited palette (5 main colours):
  INDIGO  — night sky top, text, island shadow
  VIOLET  — dusk mid-sky
  PEACH   — horizon glow
  GOLD    — the low sun, lighthouse beam, rules
  CREAM   — the sea of clouds, poster footer band
  TEAL    — one cool accent: the glass lighthouse
"""

INDIGO = (26, 32, 84)
INDIGO_DEEP = (18, 22, 60)
VIOLET = (96, 78, 148)
PEACH = (247, 178, 118)
PEACH_SOFT = (252, 205, 155)
GOLD = (255, 196, 84)
GOLD_BRIGHT = (255, 226, 150)
CREAM = (255, 243, 224)
CREAM_SHADOW = (232, 205, 196)
CLOUD_LILAC = (214, 196, 224)
TEAL = (127, 196, 196)
TEAL_DEEP = (70, 138, 150)
ROCK = (44, 48, 96)
ROCK_LIT = (96, 78, 130)


def lerp(a, b, t):
    """Linear interpolation between two RGB colours; t in [0, 1]."""
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def blend(bg, fg, alpha):
    """Alpha-blend fg over bg; alpha 0.0 (transparent) .. 1.0 (opaque)."""
    return tuple(int(bg[i] + (fg[i] - bg[i]) * alpha) for i in range(3))
