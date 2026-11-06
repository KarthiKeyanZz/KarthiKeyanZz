"""Tiny pixel-art toolkit used by make_art.py: palette, sprites, bitmap font, GIF export."""
import math
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw


def hx(s):
    s = s.lstrip("#")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


# Shared palette -------------------------------------------------------------
NIGHT0, NIGHT1, NIGHT2, NIGHT3 = hx("0b0e1f"), hx("141a35"), hx("1f2750"), hx("2f3a78")
DUSK = hx("4a3a8c")
PINK, PINK_L, PINK_D = hx("ff7eb6"), hx("ffc2dc"), hx("c44b86")
CYAN, CYAN_D = hx("5ee7ff"), hx("2a8fb8")
GOLD, GOLD_D = hx("ffd166"), hx("c98a2b")
PURPLE = hx("9b7bff")
GREEN, RED = hx("5dffa0"), hx("ff5d73")
WHITE, GREY, GREY_D = hx("f4f1ff"), hx("8d90b5"), hx("4a4e78")
INK = hx("0a0a14")
WOOD, WOOD_L, WOOD_D = hx("3a2746"), hx("553a63"), hx("241830")

CHAR_COLORS = {
    "K": INK,
    "H": hx("17151f"), "h": hx("37344f"),            # hair
    "S": hx("b9764e"), "s": hx("8f5636"), "L": hx("d6986c"),  # skin
    "B": hx("4a2f24"),                               # beard
    "N": hx("24346e"), "n": hx("18224d"), "m": hx("3a50ad"),  # navy hoodie
    "W": WHITE, "I": hx("3a2418"), "i": hx("9a6a3e"), "w": hx("ffffff"),
    "M": hx("6e2f2a"), "T": hx("f4f1ff"),
    "C": CYAN, "c": CYAN_D, "P": PINK, "G": GOLD, "g": GOLD_D,
    "D": hx("2a2840"), "d": hx("3e3b5e"), "E": PINK_L, "O": hx("ff9d5c"),
}


def sprite(img, rows, x, y, colors=None, flip=False):
    colors = colors or CHAR_COLORS
    px = img.load()
    w, h = img.size
    for j, row in enumerate(rows):
        if flip:
            row = row[::-1]
        for i, ch in enumerate(row):
            if ch == ".":
                continue
            X, Y = x + i, y + j
            if 0 <= X < w and 0 <= Y < h:
                px[X, Y] = colors[ch]


def put(img, x, y, c):
    if 0 <= x < img.width and 0 <= y < img.height:
        img.putpixel((int(x), int(y)), c)


def rect(img, x0, y0, x1, y1, c):
    ImageDraw.Draw(img).rectangle([x0, y0, x1, y1], fill=c)


def line(img, x0, y0, x1, y1, c):
    ImageDraw.Draw(img).line([x0, y0, x1, y1], fill=c)


def disc(img, cx, cy, r, c):
    ImageDraw.Draw(img).ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)


def mix(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]


def gradient(w, h, stops):
    """Vertical gradient with ordered dithering: stays strictly on the given colors."""
    img = Image.new("RGB", (w, h))
    px = img.load()
    n = len(stops) - 1
    for y in range(h):
        p = y / max(1, h - 1) * n
        i = min(int(p), n - 1)
        f = p - i
        for x in range(w):
            px[x, y] = stops[i + 1] if f > (BAYER[y % 4][x % 4] + .5) / 16 else stops[i]
    return img


# 5x7 bitmap font ------------------------------------------------------------
_F = """
A 01110 10001 10001 11111 10001 10001 10001
B 11110 10001 10001 11110 10001 10001 11110
C 01111 10000 10000 10000 10000 10000 01111
D 11110 10001 10001 10001 10001 10001 11110
E 11111 10000 10000 11110 10000 10000 11111
F 11111 10000 10000 11110 10000 10000 10000
G 01111 10000 10000 10011 10001 10001 01111
H 10001 10001 10001 11111 10001 10001 10001
I 11111 00100 00100 00100 00100 00100 11111
J 00111 00010 00010 00010 00010 10010 01100
K 10001 10010 10100 11000 10100 10010 10001
L 10000 10000 10000 10000 10000 10000 11111
M 10001 11011 10101 10101 10001 10001 10001
N 10001 11001 10101 10101 10011 10001 10001
O 01110 10001 10001 10001 10001 10001 01110
P 11110 10001 10001 11110 10000 10000 10000
Q 01110 10001 10001 10001 10101 10010 01101
R 11110 10001 10001 11110 10100 10010 10001
S 01111 10000 10000 01110 00001 00001 11110
T 11111 00100 00100 00100 00100 00100 00100
U 10001 10001 10001 10001 10001 10001 01110
V 10001 10001 10001 10001 10001 01010 00100
W 10001 10001 10001 10101 10101 11011 10001
X 10001 10001 01010 00100 01010 10001 10001
Y 10001 10001 01010 00100 00100 00100 00100
Z 11111 00001 00010 00100 01000 10000 11111
0 01110 10011 10101 10101 10101 11001 01110
1 00100 01100 00100 00100 00100 00100 01110
2 01110 10001 00001 00110 01000 10000 11111
3 11110 00001 00001 01110 00001 00001 11110
4 00010 00110 01010 10010 11111 00010 00010
5 11111 10000 11110 00001 00001 10001 01110
6 01110 10000 10000 11110 10001 10001 01110
7 11111 00001 00010 00100 01000 01000 01000
8 01110 10001 10001 01110 10001 10001 01110
9 01110 10001 10001 01111 00001 00001 01110
& 01100 10010 10100 01000 10101 10010 01101
/ 00001 00001 00010 00100 01000 10000 10000
. 00000 00000 00000 00000 00000 01100 01100
, 00000 00000 00000 00000 01100 00100 01000
! 00100 00100 00100 00100 00100 00000 00100
? 01110 10001 00001 00110 00100 00000 00100
- 00000 00000 00000 11111 00000 00000 00000
+ 00000 00100 00100 11111 00100 00100 00000
: 00000 01100 01100 00000 01100 01100 00000
> 01000 00100 00010 00001 00010 00100 01000
_ 00000 00000 00000 00000 00000 00000 11111
* 00000 00100 10101 01110 10101 00100 00000
"""
FONT = {ln.split()[0]: ln.split()[1:] for ln in _F.strip().splitlines()}


def text_w(s, scale=1):
    return len(s) * 6 * scale - scale


def text(img, s, x, y, c, scale=1, shadow=None, grad=None):
    """Draw text. `c` may be a color or a function (x, y) -> color for shimmer effects."""
    for k, ch in enumerate(s.upper()):
        gl = FONT.get(ch)
        if gl:
            for j, row in enumerate(gl):
                for i, b in enumerate(row):
                    if b != "1":
                        continue
                    for a in range(scale):
                        for e in range(scale):
                            X = x + k * 6 * scale + i * scale + a
                            Y = y + j * scale + e
                            if shadow:
                                put(img, X + scale, Y + scale, shadow)
    for k, ch in enumerate(s.upper()):
        gl = FONT.get(ch)
        if gl:
            for j, row in enumerate(gl):
                for i, b in enumerate(row):
                    if b != "1":
                        continue
                    for a in range(scale):
                        for e in range(scale):
                            X = x + k * 6 * scale + i * scale + a
                            Y = y + j * scale + e
                            put(img, X, Y, c(X, Y) if callable(c) else c)


def wave(t, period, lo=-1.0, hi=1.0, phase=0.0):
    return lo + (hi - lo) * (0.5 + 0.5 * math.sin(2 * math.pi * (t / period + phase)))


def save_gif(frames, path, scale=4, ms=100):
    """Upscale with nearest-neighbour, share one palette, then let ImageMagick shrink deltas."""
    path = Path(path)
    w, h = frames[0].size
    sheet = Image.new("RGB", (w, h * len(frames)))
    for i, f in enumerate(frames):
        sheet.paste(f, (0, i * h))
    colors = sheet.getcolors(1 << 20)
    if colors and len(colors) <= 256:
        pal = [c for _, rgb in colors for c in rgb]
        ref = Image.new("P", (1, 1))
        ref.putpalette(pal + [0] * (768 - len(pal)))
    else:
        ref = sheet.quantize(256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    big = [
        f.quantize(palette=ref, dither=Image.Dither.NONE).resize((w * scale, h * scale), Image.NEAREST)
        for f in frames
    ]
    tmp = path.with_suffix(".tmp.gif")
    big[0].save(tmp, save_all=True, append_images=big[1:], duration=ms, loop=0, optimize=False, disposal=1)
    subprocess.run(
        ["magick", str(tmp), "-layers", "OptimizeTransparency", "-loop", "0", str(path)],
        check=True,
    )
    tmp.unlink()
    print(f"{path.name:24s} {w * scale}x{h * scale}  {len(frames):3d}f  {path.stat().st_size / 1024:7.1f} KB")
