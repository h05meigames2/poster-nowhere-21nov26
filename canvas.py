"""A tiny pure-stdlib raster canvas + PNG encoder.

No PIL, no numpy: the make.fun sandbox runs main.py with the Python
standard library only, so the PNG is written by hand (zlib + struct +
CRC32) and every shape is drawn with row spans, which keeps the render
fast even at 1024x1024.
"""

import struct
import zlib

from palette import blend


class Canvas:
    def __init__(self, width, height):
        self.w = width
        self.h = height
        self.px = bytearray(width * height * 3)

    # -- low level -----------------------------------------------------
    def set(self, x, y, colour):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(colour)

    def hspan(self, y, x0, x1, colour):
        """Fill a horizontal run of pixels on one row (clipped)."""
        if y < 0 or y >= self.h:
            return
        x0 = max(0, x0)
        x1 = min(self.w, x1)
        if x1 <= x0:
            return
        i = (y * self.w + x0) * 3
        self.px[i:i + 3 * (x1 - x0)] = bytes(colour) * (x1 - x0)

    def fill_rect(self, x0, y0, x1, y1, colour):
        x0 = max(0, x0)
        y0 = max(0, y0)
        x1 = min(self.w, x1)
        y1 = min(self.h, y1)
        for y in range(y0, y1):
            self.hspan(y, x0, x1, colour)

    def blend_hspan(self, y, x0, x1, colour, alpha):
        if y < 0 or y >= self.h or alpha <= 0:
            return
        x0 = max(0, x0)
        x1 = min(self.w, x1)
        for x in range(x0, x1):
            i = (y * self.w + x) * 3
            bg = (self.px[i], self.px[i + 1], self.px[i + 2])
            self.px[i:i + 3] = bytes(blend(bg, colour, alpha))

    # -- gradients -----------------------------------------------------
    def vertical_gradient(self, y0, y1, stops):
        """Fill rows y0..y1 with a multi-stop vertical gradient.

        stops: list of (position 0..1, colour) sorted by position.
        """
        for y in range(max(0, y0), min(self.h, y1)):
            t = (y - y0) / max(1, (y1 - y0 - 1))
            colour = stops[0][1]
            for j in range(len(stops) - 1):
                p0, c0 = stops[j]
                p1, c1 = stops[j + 1]
                if p0 <= t <= p1:
                    lt = 0.0 if p1 == p0 else (t - p0) / (p1 - p0)
                    colour = tuple(
                        int(c0[k] + (c1[k] - c0[k]) * lt) for k in range(3)
                    )
                    break
            else:
                colour = stops[-1][1]
            self.hspan(y, 0, self.w, colour)

    # -- shapes --------------------------------------------------------
    def disc(self, cx, cy, r, colour):
        """Filled circle, drawn as per-row spans."""
        r2 = r * r
        for y in range(cy - r, cy + r + 1):
            dy = y - cy
            dx = int((r2 - dy * dy) ** 0.5) if r2 >= dy * dy else 0
            self.hspan(y, cx - dx, cx + dx + 1, colour)

    def ellipse(self, cx, cy, rx, ry, colour):
        for y in range(cy - ry, cy + ry + 1):
            dy = (y - cy) / ry
            if abs(dy) > 1:
                continue
            dx = int(rx * (1 - dy * dy) ** 0.5)
            self.hspan(y, cx - dx, cx + dx + 1, colour)

    def blend_ellipse(self, cx, cy, rx, ry, colour, alpha):
        for y in range(cy - ry, cy + ry + 1):
            dy = (y - cy) / ry
            if abs(dy) > 1:
                continue
            dx = int(rx * (1 - dy * dy) ** 0.5)
            self.blend_hspan(y, cx - dx, cx + dx + 1, colour, alpha)

    def polygon(self, points, colour):
        """Filled polygon via a scanline fill (points: list of (x, y))."""
        if len(points) < 3:
            return
        ys = [p[1] for p in points]
        for y in range(max(0, min(ys)), min(self.h, max(ys) + 1)):
            xs = []
            n = len(points)
            for i in range(n):
                x0, y0 = points[i]
                x1, y1 = points[(i + 1) % n]
                if y0 == y1:
                    continue
                if (y0 <= y < y1) or (y1 <= y < y0):
                    xs.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
            if len(xs) >= 2:
                xs.sort()
                for j in range(0, len(xs) - 1, 2):
                    self.hspan(y, int(xs[j]), int(xs[j + 1]) + 1, colour)

    def blend_polygon(self, points, colour, alpha):
        if len(points) < 3 or alpha <= 0:
            return
        ys = [p[1] for p in points]
        for y in range(max(0, min(ys)), min(self.h, max(ys) + 1)):
            xs = []
            n = len(points)
            for i in range(n):
                x0, y0 = points[i]
                x1, y1 = points[(i + 1) % n]
                if y0 == y1:
                    continue
                if (y0 <= y < y1) or (y1 <= y < y0):
                    xs.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
            if len(xs) >= 2:
                xs.sort()
                for j in range(0, len(xs) - 1, 2):
                    self.blend_hspan(y, int(xs[j]), int(xs[j + 1]) + 1,
                                     colour, alpha)

    # -- PNG output ----------------------------------------------------
    def to_png(self):
        def chunk(kind, data):
            out = struct.pack(">I", len(data)) + kind + data
            out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
            return out

        ihdr = struct.pack(">IIBBBBB", self.w, self.h, 8, 2, 0, 0, 0)
        raw = bytearray()
        stride = self.w * 3
        for y in range(self.h):
            raw.append(0)  # filter: None
            raw += self.px[y * stride:(y + 1) * stride]
        idat = zlib.compress(bytes(raw), 9)
        png = b"\x89PNG\r\n\x1a\n"
        png += chunk(b"IHDR", ihdr)
        png += chunk(b"IDAT", idat)
        png += chunk(b"IEND", b"")
        return png
