#!/usr/bin/env python3
"""Generates every animated banner in assets/. All art is original and drawn in code.

    python3 scripts/make_art.py            # build everything
    python3 scripts/make_art.py hero       # build one piece

Needs Pillow and ImageMagick (`magick`).
"""
import math
import random
import sys
from pathlib import Path

from PIL import Image

from pixel import *  # noqa: F401,F403

OUT = Path(__file__).resolve().parent.parent / "assets"

# Character ------------------------------------------------------------------
HEAD = [
    "...........K.....K..........",
    ".......KK.KHK...KHKK.K......",
    ".....KKHHKHHHKKKHHHHKHK.....",
    "....KHHHHHHhhHHHHHHhHHHK....",
    "...KHHHHHhhhhHHHHhhhhHHHK...",
    "..KHHHHhhhHHHHHHhhHHHHHHHK..",
    ".KHHHHHHHHHHHHHHHHHHHHHHHHK.",
    ".KHHHHHHHHHHHHHHHHHHHHHHHHK.",
    ".KHHHHHHHSHHHHHSSHHHHHHHHHK.",
    ".KHHHHSSSSHHHSSSSSHHHSHHHHK.",
    ".KHHSSSSSSSHSSSSSSSSSSSSHHK.",
    ".KHSSSSSSSSSSSSSSSSSSSSSHHK.",
    ".KHSSSSSSSSSSSSSSSSSSSSSHHK.",
    "KsKSSSSSSSSSSSSSSSSSSSSSSKsK",
    "KsKSSSSSSSSSSSSSSSSSSSSSSKsK",
    "KsKSSSSSSSSSSSSSSSSSSSSSSKsK",
    ".KKSSSSSSSSSSSSSSSSSSSSSSKK.",
    "..KSSSSSSSSSSSSSSSSSSSSSSK..",
    "..KSLSSSSSSSSSSSSSSSSSSLSK..",
    "..KBSSSSSSSSSssSSSSSSSSSBK..",
    "..KBSSSSSSSSSSSSSSSSSSSSBK..",
    "..KBBSSSSBBBBBBBBBBSSSSBBK..",
    "...KBBSSSBBSSSSSSBBSSSBBK...",
    "...KBBBSSSSSSSSSSSSSSBBBK...",
    "....KBBBBSSBBBBBBSSBBBBK....",
    ".....KKBBBBBBBBBBBBBBKK.....",
    ".......KKKKKKKKKKKKKK.......",
]

EYE = [
    ".KKKKK",
    "KKKKKK",
    "WwwIIK",
    "WwIIIW",
    "WIIiiW",
    ".WWWW.",
]
EYE_GOLD = [
    ".KKKKK",
    "KKKKKK",
    "WwwGGK",
    "WwGGGW",
    "WGGggW",
    ".WWWW.",
]
EYE_SHUT = [
    "......",
    "......",
    "......",
    "K....K",
    ".KKKK.",
    "......",
]
EYE_HAPPY = [
    "......",
    "..KK..",
    ".KKKK.",
    "KK..KK",
    "K....K",
    "......",
]
EYE_DOWN = [
    "......",
    ".KKKKK",
    "KKKKKK",
    "WIIIIK",
    "WIIiiW",
    ".WWWW.",
]

BODY = [
    "..........KssssssK..........",
    ".......KKKnKssssKnKKK.......",
    ".....KKNNNNnKKKKnNNNNKK.....",
    "....KNNNNNNNnnnnNNNNNNNK....",
    "...KNNmNNNNNWNNWNNNNNmNNK...",
    "...KNNmNNNNNWNNWNNNNNmNNK...",
    "..KNNNmNNNNNNNNNNNNNNmNNNK..",
    "..KNNNmNNNNNNNNNNNNNNmNNNK..",
    "..KNNNmNNNNNNNNNNNNNNmNNNK..",
    "..KNNNmNNNNNNNNNNNNNNmNNNK..",
    "..KNNNmNNNNNNNNNNNNNNmNNNK..",
    "..KNNNmNNNNNNNNNNNNNNmNNNK..",
]


BLUSH = hx("d9705f")


def head(img, x, y, eye=EYE, mouth="smile", phones=True, look=0):
    sprite(img, HEAD, x, y)
    # eyebrows
    for i in range(6):
        put(img, x + 5 + i, y + 10 + (1 if i < 1 else 0), INK)
        put(img, x + 17 + i, y + 10 + (1 if i > 4 else 0), INK)
    sprite(img, eye, x + 5 + look, y + 12)
    sprite(img, eye, x + 17 + look, y + 12)
    for bx in (4, 5, 6, 21, 22, 23):
        put(img, x + bx, y + 18, BLUSH)
    my = y + 22
    if mouth == "smile":
        for i, dy in enumerate((0, 1, 1, 1, 1, 0)):
            put(img, x + 11 + i, my + dy, CHAR_COLORS["M"])
    elif mouth == "open":
        sprite(img, ["MMMMMM", "MPPPPM", ".MMMM."], x + 11, my)
    elif mouth == "flat":
        for i in range(4):
            put(img, x + 12 + i, my + 1, CHAR_COLORS["M"])
    if phones:
        for i in range(28):
            yy = 11 - 5.5 * math.sqrt(max(0, 1 - ((i - 13.5) / 14.5) ** 2))
            put(img, x + i, y + int(yy), CYAN)
        cup = ["CCC", "CPC", "CPC", "CPC", "CPC", "CPC", "CCC"]
        sprite(img, cup, x - 2, y + 11)
        sprite(img, cup, x + 27, y + 11)


CAT = [
    "..K...K...........",
    ".KOK.KOK..........",
    ".KOOKOOOKKKKKKKK..",
    "KOOOOOOOOOOOOOOOK.",
    "KOKKOKKOOgOOgOOOOK",
    "KOOOOOOOOgOOgOOOOK",
    "KOOEOOOOOOOOOOOOOK",
    ".KOOOOOOOOOOOOOOK.",
    "..KKKKKKKKKKKKKK..",
]

PETAL = [[(0, 0), (1, 0), (0, 1)], [(0, 0), (1, 1)], [(0, 0), (0, 1), (1, 1)], [(0, 0), (1, 0)]]


def petals(img, t, n_frames, seed, count, region, drift=-1):
    """Falling sakura. Whole-number wraps per loop keep the GIF seamless."""
    x0, y0, x1, y1 = region
    W, H = x1 - x0, y1 - y0
    r = random.Random(seed)
    for _ in range(count):
        px0, py0 = r.uniform(0, W), r.uniform(0, H)
        turns = r.choice((1, 1, 2))
        ph = r.random()
        col = r.choice((PINK, PINK_L, PINK_L, PINK_D))
        p = t / n_frames * turns
        x = x0 + (px0 + drift * p * W) % W + 2 * math.sin(2 * math.pi * (p * 2 + ph))
        y = y0 + (py0 + p * H) % H
        for dx, dy in PETAL[(int(p * 12 + ph * 4)) % 4]:
            put(img, x + dx, y + dy, col)


def stars(img, t, period, seed, count, region):
    x0, y0, x1, y1 = region
    r = random.Random(seed)
    for _ in range(count):
        x, y, ph = r.randint(x0, x1), r.randint(y0, y1), r.random()
        v = wave(t, period, 0, 1, ph)
        put(img, x, y, WHITE if v > .75 else GREY if v > .35 else GREY_D)
        if v > .93 and r.random() < .5:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                put(img, x + dx, y + dy, GREY)


def skyline(img, seed, base, x0=0, x1=None, tall=26, body=NIGHT1):
    """Static silhouettes. Returns window list so callers can flicker them."""
    x1 = x1 or img.width
    r = random.Random(seed)
    wins, x = [], x0
    while x < x1:
        w, h = r.randint(9, 20), r.randint(8, tall)
        rect(img, x, base - h, x + w - 1, base, body)
        if r.random() < .3:
            rect(img, x + w // 2, base - h - 4, x + w // 2, base - h, body)
            put(img, x + w // 2, base - h - 5, RED)
        for wy in range(base - h + 2, base - 1, 3):
            for wx in range(x + 2, x + w - 2, 3):
                if r.random() < .42:
                    wins.append((wx, wy, r.choice((GOLD, GOLD, CYAN, PINK_L)), r.random()))
        x += w + r.randint(0, 2)
    return wins


def hologram(img, x0, y0, x1, y1, t, kind):
    """Translucent HUD panel: mixes with whatever is behind it."""
    px = img.load()
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            px[x, y] = mix(px[x, y], NIGHT2, .72) if (y + t // 2) % 3 else mix(px[x, y], CYAN_D, .34)
    for x in range(x0, x1 + 1):
        px[x, y0] = px[x, y1] = CYAN
    for y in range(y0, y1 + 1):
        px[x0, y] = px[x1, y] = CYAN
    for a, b in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)):
        px[a, b] = WHITE
    if kind == "code":
        r = random.Random(7)
        rows = [(r.randint(0, 4), r.randint(4, x1 - x0 - 8), r.choice((PINK, CYAN, GOLD, GREEN, WHITE))) for _ in range(16)]
        off = t // 3
        y = y0 + 3
        i = 0
        while y < y1 - 1:
            ind, ln, c = rows[(i + off) % 16]
            for k in range(ln):
                if k % 5 != 4:
                    put(img, x0 + 3 + ind + k, y, c)
            y += 2
            i += 1
    else:
        base = y1 - 3
        n = x1 - x0 - 5
        pts = []
        for i in range(n):
            v = (math.sin((i + t) * 2 * math.pi / 16) * .5 + math.sin((i + t) * 2 * math.pi / 8 + 1) * .3 + 1) / 2
            pts.append(int(v * (y1 - y0 - 15)))
        for i, v in enumerate(pts):
            put(img, x0 + 3 + i, base - v, GREEN)
            if i % 3 == 0:
                for yy in range(base - v + 1, base + 1):
                    put(img, x0 + 3 + i, yy, CYAN_D)
        text(img, "AI", x0 + 3, y0 + 3, PINK)


def hero():
    W, H, N = 240, 96, 48
    bg = gradient(W, H, [NIGHT0, NIGHT1, NIGHT2, NIGHT3, DUSK])
    MX, MY = 187, 41
    disc(bg, MX, MY, 34, hx("3a3a78"))
    disc(bg, MX, MY, 32, hx("6a6aa8"))
    disc(bg, MX, MY, 30, hx("e8e4ff"))
    for cx, cy, r in ((172, 26, 4), (207, 40, 5), (200, 20, 3), (165, 50, 3), (208, 58, 3)):
        disc(bg, cx, cy, r, hx("cfcaf0"))
    far = skyline(bg, 3, 78, tall=30, body=hx("1c2148"))
    near = skyline(bg, 11, 78, tall=17, body=NIGHT0)

    frames = []
    grad_t = [hx("ffffff"), PINK_L, PINK]
    for t in range(N):
        im = bg.copy()
        stars(im, t, N // 2, 5, 46, (0, 0, W - 1, 50))
        for wx, wy, c, ph in far + near:
            if wave(t, N, 0, 1, ph) > .18:
                put(im, wx, wy, c)
        # shooting star, once per loop
        if 6 <= t < 16:
            s = t - 6
            for k in range(7):
                put(im, 150 - s * 9 + k * 2, 4 + s * 3 - k, mix(WHITE, NIGHT2, k / 7))

        # sakura branch
        line(im, 239, 2, 216, 9, WOOD)
        line(im, 239, 3, 216, 10, WOOD)
        line(im, 226, 6, 212, 1, WOOD)
        line(im, 228, 7, 222, 17, WOOD)
        rb = random.Random(2)
        for _ in range(38):
            bx, by = rb.randint(206, 239), rb.randint(0, 19)
            put(im, bx, by, rb.choice((PINK, PINK_L, PINK_D, PINK_L)))
            put(im, bx + 1, by, rb.choice((PINK, PINK_L)))

        # title block
        text(im, "KARTHI KEYAN", 10, 11,
             lambda x, y: WHITE if abs(((x - y) - t * 6) % 288 - 60) < 7 else grad_t[min(2, (y - 11) // 5)],
             scale=2, shadow=hx("3a1f5c"))
        text(im, "BACKEND & AI/ML ENGINEER", 10, 31, CYAN, shadow=NIGHT0)
        text(im, "> LLM + RAG SYSTEMS", 10, 41, GOLD, shadow=NIGHT0)
        if (t // 6) % 2 == 0:
            rect(im, 10 + text_w("> LLM + RAG SYSTEMS") + 3, 41, 10 + text_w("> LLM + RAG SYSTEMS") + 7, 47, GOLD)

        # character
        bob = 1 if (t // 8) % 2 else 0
        hx0, hy0 = MX - 14, 24 + bob
        sprite(im, BODY, hx0, hy0 + 26)
        blink = t % 24 in (15, 16)
        look = -1 if 24 <= t < 34 else 1 if 34 <= t < 40 else 0
        head(im, hx0, hy0, eye=EYE_SHUT if blink else EYE, look=look)

        hologram(im, 134, 50, 160, 73, t, "code")
        hologram(im, 211, 27, 236, 58, t, "chart")

        # desk + laptop
        rect(im, 0, 78, W, 79, PINK)
        rect(im, 0, 80, W, 81, WOOD_L)
        rect(im, 0, 82, W, H, WOOD_D)
        rect(im, MX - 19, 60, MX + 19, 76, hx("3a3f6a"))
        rect(im, MX - 18, 61, MX + 18, 75, hx("262a4e"))
        rect(im, MX - 19, 76, MX + 19, 77, GREY)
        glow = PINK if (t // 12) % 2 else CYAN
        disc(im, MX, 68, 3, glow)
        put(im, MX, 68, WHITE)

        # cat
        sprite(im, CAT, 96, 69)
        tail = int(wave(t, 24, -2, 2))
        for k in range(7):
            yy = 74 - int(k * .6) + (tail * k) // 5
            put(im, 113 + k, yy, CHAR_COLORS["O"])
            put(im, 113 + k, yy + 1, CHAR_COLORS["O"])
            put(im, 113 + k, yy - 1, INK)

        # mug + steam
        rect(im, 62, 71, 69, 77, CYAN_D)
        rect(im, 62, 71, 69, 72, CYAN)
        for yy in (73, 74, 75):
            put(im, 70, yy, CYAN_D)
            put(im, 71, yy, CYAN_D)
        for k in range(2):
            for s in range(6):
                sy = 69 - ((s * 2 + t // 2 + k * 5) % 12)
                put(im, 64 + k * 3 + int(wave(sy, 8, -1, 1)), sy, GREY_D)

        # LED ticker on desk front
        tick = "PYTHON * JAVA * RUST * FASTAPI * SPRING BOOT * KAFKA * "
        unit = text_w(tick) + 1
        off = int(t * unit / N)
        for rep in range(-1, 3):
            text(im, tick, rep * unit - off, 85, hx("a48bc9"))

        petals(im, t, N, 9, 16, (0, 0, W, 78))
        frames.append(im)
    save_gif(frames, OUT / "hero.gif", scale=4, ms=90)


def back_head(img, x, y, rim):
    cx, cy = x + 14, y + 13
    disc(img, cx, cy, 13, INK)
    disc(img, cx, cy, 12, CHAR_COLORS["H"])
    for sx, sy in ((5, 2), (9, 0), (14, -1), (19, 0), (23, 2)):
        for k in range(4):
            put(img, x + sx, y + sy + k, CHAR_COLORS["H"])
            put(img, x + sx + 1, y + sy + k + 1, CHAR_COLORS["H"])
        put(img, x + sx, y + sy - 1, INK)
    for i in range(6, 22):
        put(img, x + i, y + 4 + abs(i - 14) // 4, CHAR_COLORS["h"])
    for i in range(28):
        yy = 12 - 11 * math.sqrt(max(0, 1 - ((i - 13.5) / 14.5) ** 2))
        put(img, x + i, y + int(yy), CYAN)
    cup = ["CCC", "CPC", "CPC", "CPC", "CPC", "CPC", "CCC"]
    sprite(img, cup, x - 2, y + 10)
    sprite(img, cup, x + 27, y + 10)
    for i in range(8, 21):
        put(img, x + i, y + 1 + abs(i - 14) // 5, rim)


def wall(w, h, top, bottom):
    return gradient(w, h, [top, bottom])


def gaming():
    W, H, N = 96, 72, 32
    frames = []
    for t in range(N):
        im = wall(W, H, NIGHT1, hx("2a1f55"))
        rect(im, 0, 0, W, 1, PINK if (t // 8) % 2 else PURPLE)
        rect(im, 10, 4, 85, 46, INK)
        rect(im, 11, 5, 84, 45, hx("2c2c44"))
        # game world
        sx0, sy0, sw, sh = 13, 7, 70, 37
        scene = gradient(sw, sh, [hx("3a2470"), hx("c44b86"), hx("ff9d5c"), hx("ffd166")])
        disc(scene, 48, 22, 8, hx("fff1c4"))
        for off, base, amp, col, per in ((t, 30, 7, hx("7a3a78"), 32), (t * 2, 33, 5, hx("4a2458"), 32)):
            for x in range(sw):
                y = int(base - amp * (.5 + .5 * math.sin((x + off) * 2 * math.pi / per)))
                rect(scene, x, y, x, sh, col)
        rect(scene, 0, 33, sw, sh, hx("2a1630"))
        for cxp in (10, 42):
            cx = (cxp - t * 2) % 64
            rect(scene, cx, 27, cx + 1, 33, INK)
            rect(scene, cx - 2, 29, cx - 2, 30, INK)
            rect(scene, cx + 3, 28, cx + 3, 29, INK)
        # lone rider, simple silhouette
        by = 1 if (t // 2) % 2 else 0
        legs = ["..K.K....K.K..", ".K...K..K...K."] if by else ["...K.K..K.K...", "...K.K..K.K..."]
        sprite(scene, ["......KK......", ".....KKKK.....", "......KK......", ".....KKKK...K.", "KK...KKKK..KK.", ".KKKKKKKKKKKK.", ".KKKKKKKKKKK..", "..KKKKKKKK...."] + legs, 4, 22 + by, {"K": INK})
        for i in range(3):
            sprite(scene, ["P.P", "PPP", ".P."], 2 + i * 5, 2, {"P": RED})
        text(scene, str(1000 + t * 8), 44, 2, WHITE)
        im.paste(scene, (sx0, sy0))
        rect(im, 42, 46, 53, 49, INK)
        # player, seen from behind
        rect(im, 22, 62, 73, 72, CHAR_COLORS["N"])
        rect(im, 16, 66, 79, 72, CHAR_COLORS["N"])
        rect(im, 24, 60, 71, 62, CHAR_COLORS["N"])
        elbow = (t // 4) % 2
        rect(im, 14, 64 + elbow, 22, 72, CHAR_COLORS["n"])
        rect(im, 73, 65 - elbow, 81, 72, CHAR_COLORS["n"])
        rim = (hx("ff9d5c"), hx("ffd166"), PINK)[(t // 6) % 3]
        back_head(im, 34, 38, rim)
        petals(im, t, N, 21, 3, (0, 0, W, 40))
        frames.append(im)
    save_gif(frames, OUT / "gaming.gif", scale=4, ms=90)


def manga():
    W, H, N = 96, 72, 32
    bg = wall(W, H, hx("23193f"), hx("3a2a5e"))
    r = random.Random(4)
    for sy in (8, 34):
        rect(bg, 0, sy + 20, W, sy + 21, WOOD_L)
        x = 1
        while x < W - 3:
            w, h = r.randint(3, 6), r.randint(13, 20)
            c = r.choice((PINK_D, CYAN_D, PURPLE, GOLD_D, hx("3f6fbf"), hx("5f8f6f")))
            rect(bg, x, sy + 20 - h, x + w - 1, sy + 19, c)
            rect(bg, x + 1, sy + 20 - h + 2, x + w - 2, sy + 20 - h + 3, WHITE)
            x += w + r.randint(0, 1)
    frames = []
    for t in range(N):
        im = bg.copy()
        px = im.load()
        for y in range(H):
            for x in range(W):
                d = math.hypot(x - 48, y - 36)
                if d < 36:
                    px[x, y] = mix(px[x, y], hx("120e26"), .55)
        hx0, hy0 = 34, 11 + (1 if (t // 8) % 2 else 0)
        sprite(im, BODY, hx0, hy0 + 26)
        head(im, hx0, hy0, eye=EYE_SHUT if t % 16 in (5, 6) else EYE_DOWN, mouth=None)
        # open manga
        bx, by, bw = 22, 42, 26
        rect(im, bx - 1, by - 1, bx + bw * 2, by + 25, hx("5b2a86"))
        rect(im, bx, by, bx + bw - 1, by + 23, WHITE)
        rect(im, bx + bw + 1, by, bx + bw * 2 - 1, by + 23, WHITE)
        rect(im, bx + bw, by - 1, bx + bw, by + 24, hx("3a1a5c"))
        for px0 in (bx + 2, bx + bw + 3):
            rect(im, px0, by + 2, px0 + 9, by + 10, GREY_D)
            rect(im, px0 + 11, by + 2, px0 + 20, by + 10, hx("c8c6dc"))
            rect(im, px0, by + 12, px0 + 20, by + 21, hx("c8c6dc"))
            for k in range(0, 6, 2):
                line(im, px0 + 2, by + 14 + k, px0 + 18 - k, by + 14 + k, GREY_D)
        # page turning
        ph = t % 16
        if ph < 6:
            turn = int((ph / 5) * bw * 2) - bw
            x0, x1 = sorted((bx + bw, bx + bw + (-turn)))
            rect(im, x0, by - 2, x1, by + 22, hx("e8e4f4"))
            line(im, x0, by - 2, x1, by - 2, GREY)
        # floating reactions
        c = (GOLD, PINK, CYAN)[(t // 8) % 3]
        rise = (t % 16) // 2
        text(im, "!?", 72, 22 - rise, c, shadow=NIGHT0)
        for a in range(4):
            ang = t / N * 2 * math.pi + a * math.pi / 2
            put(im, 14 + 7 * math.cos(ang), 22 + 7 * math.sin(ang), GOLD)
        sprite(im, ["..C..", ".CWC.", ".CWC.", ".CCC.", "C.C.C"], 12, 19 - (t // 8) % 2, {"C": CYAN, "W": WHITE})
        frames.append(im)
    save_gif(frames, OUT / "manga.gif", scale=4, ms=90)


def hue(t, n, off=0.0):
    import colorsys
    r, g, b = colorsys.hsv_to_rgb((t / n + off) % 1, .7, 1)
    return (int(r * 255), int(g * 255), int(b * 255))


def fan(im, cx, cy, r, ang, ring):
    disc(im, cx, cy, r, ring)
    disc(im, cx, cy, r - 1, hx("151528"))
    for k in range(3):
        a = ang + k * 2 * math.pi / 3
        for s in (0, .35):
            line(im, cx, cy, cx + (r - 2) * math.cos(a + s), cy + (r - 2) * math.sin(a + s), hx("5a5a84"))
    disc(im, cx, cy, 2, ring)


def pcbuild():
    W, H, N = 96, 72, 24
    frames = []
    for t in range(N):
        im = wall(W, H, NIGHT1, hx("1c2c58"))
        rect(im, 0, 64, W, H, WOOD_D)
        rect(im, 0, 64, W, 64, PINK)
        # open case
        rect(im, 5, 4, 55, 65, INK)
        rect(im, 6, 5, 54, 64, hx("1a1a2e"))
        rect(im, 8, 7, 52, 62, hx("232340"))
        ang = t * math.radians(30)
        for i, cy in enumerate((16, 31, 46)):
            fan(im, 17, cy, 7, ang, hue(t, N, i * .12))
        # cpu cooler + ram
        rect(im, 30, 11, 41, 22, hx("6a6a94"))
        rect(im, 32, 13, 39, 20, hx("3a3a5c"))
        for i in range(4):
            rect(im, 44 + i * 2, 10, 44 + i * 2, 24, hue(t, N, i * .15))
        # gpu
        rect(im, 28, 32, 51, 41, hx("3a3a5c"))
        rect(im, 28, 32, 51, 33, hue(t, N, .5))
        fan(im, 36, 37, 3, -ang, GREY_D)
        fan(im, 44, 37, 3, -ang, GREY_D)
        # tidy cable runs
        for i, c in enumerate((GOLD_D, RED, CYAN_D)):
            line(im, 28, 47 + i, 40, 47 + i, c)
            line(im, 40, 47 + i, 44, 53 + i, c)
            line(im, 44, 53 + i, 50, 53 + i, c)
        # builder
        hy = 20 + (1 if (t // 6) % 2 else 0)
        sprite(im, BODY[:9], 60, hy + 26)
        head(im, 60, hy, eye=EYE_HAPPY if t % 12 < 3 else EYE, mouth="open" if t % 12 < 3 else "smile", look=-1)
        # screwdriver hand, tapping the case
        tap = int(wave(t, 12, 0, 3))
        rect(im, 56 - tap, 49, 60, 52, CHAR_COLORS["N"])
        rect(im, 53 - tap, 49, 56 - tap, 52, CHAR_COLORS["S"])
        rect(im, 49 - tap, 50, 53 - tap, 51, GREY)
        rect(im, 51 - tap, 49, 53 - tap, 52, GOLD)
        if t % 12 < 3:
            for dx, dy in ((-1, -2), (-3, 0), (-1, 2), (-4, -2), (-4, 2)):
                put(im, 48 + dx, 50 + dy, GOLD)
        frames.append(im)
    save_gif(frames, OUT / "pcbuild.gif", scale=4, ms=90)


def crypto():
    W, H, N = 96, 72, 32
    r = random.Random(12)
    PER = 16
    series, v = [], 22
    for i in range(PER):
        step = r.randint(-5, 6)
        series.append((v, v + step, r.randint(1, 3)))
        v += step
    series[-1] = (series[-1][0], series[0][0], 2)
    lo_v = min(min(o, c) for o, c, _ in series)
    hi_v = max(max(o, c) for o, c, _ in series)
    fit = lambda v: int((v - lo_v) / (hi_v - lo_v) * 26) + 3
    series = [(fit(o), fit(c), w) for o, c, w in series]
    frames = []
    for t in range(N):
        im = wall(W, H, NIGHT0, hx("15234a"))
        rect(im, 3, 3, 62, 49, CYAN_D)
        rect(im, 4, 4, 61, 48, hx("0d1228"))
        for gy in range(10, 48, 8):
            for gx in range(5, 61, 3):
                put(im, gx, gy, NIGHT2)
        off = (t // 2) % PER
        for k in range(14):
            o, c, wk = series[(k + off) % PER]
            x = 6 + k * 4
            col = GREEN if c >= o else RED
            lo, hi = sorted((o, c))
            rect(im, x + 1, 45 - hi - wk, x + 1, 45 - lo + wk, col)
            rect(im, x, 45 - hi, x + 2, 45 - lo, col)
        text(im, "BTC", 41, 7, GOLD, shadow=NIGHT0)
        # chain of blocks with a walking hash
        for i in range(5):
            x = 4 + i * 12
            lit = (t // 4) % 5 == i
            rect(im, x, 55, x + 8, 63, CYAN if lit else NIGHT3)
            rect(im, x + 1, 56, x + 7, 62, hx("0d1228"))
            rect(im, x + 3, 58, x + 5, 60, CYAN if lit else GREY_D)
            if i < 4:
                rect(im, x + 9, 58, x + 11, 59, GOLD if lit else GREY_D)
        # coin
        cw = abs(math.cos(t / N * 4 * math.pi))
        rw = max(1, int(10 * cw))
        cx, cy = 80, 14 + int(wave(t, 16, -1, 1))
        from PIL import ImageDraw
        d = ImageDraw.Draw(im)
        d.ellipse([cx - rw - 1, cy - 11, cx + rw + 1, cy + 11], fill=GOLD_D)
        d.ellipse([cx - rw, cy - 10, cx + rw, cy + 10], fill=GOLD)
        if rw >= 7:
            text(im, "K", cx - 2, cy - 3, GOLD_D)
        # glint
        if t % 16 < 3:
            put(im, cx + 5, cy - 8, WHITE)
            put(im, cx + 6, cy - 7, WHITE)
        hy = 41 + (1 if (t // 8) % 2 else 0)
        head(im, 65, hy, eye=EYE_GOLD, mouth="open")
        rect(im, 67, 68, 91, 72, CHAR_COLORS["N"])
        frames.append(im)
    save_gif(frames, OUT / "crypto.gif", scale=4, ms=90)


def interests():
    W, H, N = 240, 66, 48
    tags = ["AI MODELS", "OPEN SOURCE", "SPACE", "SUPERCOMPUTERS", "PC BUILDING", "GADGETS"]
    bg = gradient(W, H, [NIGHT0, NIGHT1, hx("231a55")])
    rng = random.Random(8)
    TILE = W // 2  # stars repeat every half-width, so 1x and 2x speeds both wrap cleanly
    layers = [(rng.randint(0, TILE - 1), rng.randint(0, H - 1), 1) for _ in range(18)]
    layers += [(rng.randint(0, TILE - 1), rng.randint(0, H - 1), 2) for _ in range(10)]
    frames = []
    for t in range(N):
        im = bg.copy()
        for x, y, sp in layers:
            X = (x - t * sp * TILE // N) % TILE
            put(im, X, y, WHITE if sp == 2 else GREY_D)
            put(im, X + TILE, y, WHITE if sp == 2 else GREY_D)
        # rocket crosses top
        rx = int(t * (W + 40) / N) - 20
        sprite(im, [".....WW...", "..PPWWWCW.", "OPPWWWWWWW", "..PPWWWCW.", ".....WW..."], rx, 3, {"W": WHITE, "P": PINK, "C": CYAN, "O": GOLD})
        for k in range(3):
            put(im, rx - 2 - k * 3 - (t % 2), 5, GOLD if k < 2 else GREY_D)
        # astronaut
        ay = 14 + int(wave(t, 24, -3, 3))
        ax = 7
        rect(im, ax + 2, ay + 26, ax + 25, ay + 42, hx("c8c6dc"))
        rect(im, ax + 7, ay + 29, ax + 20, ay + 37, GREY_D)
        rect(im, ax + 9, ay + 31, ax + 12, ay + 33, (GREEN, RED)[(t // 6) % 2])
        rect(im, ax + 15, ay + 31, ax + 18, ay + 33, CYAN)
        disc(im, ax + 13, ay + 13, 19, GREY)
        disc(im, ax + 13, ay + 13, 18, hx("c8c6dc"))
        disc(im, ax + 13, ay + 13, 16, NIGHT2)
        head(im, ax, ay, phones=False, eye=EYE_SHUT if t % 24 in (9, 10) else EYE)
        put(im, ax + 2, ay + 3, WHITE)
        put(im, ax + 3, ay + 2, WHITE)
        put(im, ax + 4, ay + 1, WHITE)
        # lit tags
        active = (t // 8) % 6
        for i, name in enumerate(tags):
            col, row = i // 3, i % 3
            x, y = 56 + col * 92, 12 + row * 18
            w = 88
            on = i == active
            rect(im, x, y, x + w, y + 14, PINK if on else CYAN_D)
            rect(im, x + 1, y + 1, x + w - 1, y + 13, hx("3a1f5c") if on else NIGHT1)
            text(im, name, x + (w - text_w(name)) // 2 + 1, y + 4, WHITE if on else CYAN)
        frames.append(im)
    save_gif(frames, OUT / "interests.gif", scale=4, ms=100)


CAT_RUN = [[
    "K.K.............",
    "KOKK..........K.",
    "KOOOKKKKKKKKKKOK",
    "KKOOOOOgOOgOOOK.",
    "KOOOOOOgOOgOOK..",
    ".KKOOOOOOOOOOK..",
    "..KOK.KKK.KOK...",
    "...KK......KK...",
], [
    "K.K.............",
    "KOKK..........K.",
    "KOOOKKKKKKKKKKOK",
    "KKOOOOOgOOgOOOK.",
    "KOOOOOOgOOgOOK..",
    ".KKOOOOOOOOOOK..",
    ".KOK..KKK...KOK.",
    "KK...........KK.",
]]


def footer():
    W, H, N = 240, 52, 60
    bg = gradient(W, H, [NIGHT0, NIGHT1, NIGHT2, NIGHT3])
    wins = skyline(bg, 6, 44, tall=16, body=hx("1c2148"))
    frames = []
    a, b = "STAY CURIOUS. STAY CREATIVE.", "NEVER STOP BUILDING!"
    for t in range(N):
        im = bg.copy()
        stars(im, t, N // 2, 15, 26, (0, 0, W - 1, 26))
        for wx, wy, c, ph in wins:
            if wave(t, N, 0, 1, ph) > .2:
                put(im, wx, wy, c)
        text(im, a, 60, 8, CYAN, shadow=NIGHT0)
        text(im, b, 60, 19, lambda x, y: WHITE if abs((x - t * 8) % 480 - 120) < 8 else PINK, shadow=NIGHT0)
        rect(im, 0, 44, W, 45, PINK)
        rect(im, 0, 46, W, H, WOOD_D)
        # wave hello
        head(im, 14, 8 + (t // 10) % 2, eye=EYE_HAPPY if (t // 15) % 2 else EYE, mouth="open" if (t // 15) % 2 else "smile")
        sprite(im, BODY[:8], 14, 34 + (t // 10) % 2)
        hand = int(wave(t, 15, -2, 2))
        rect(im, 45, 20 + hand, 48, 24 + hand, CHAR_COLORS["S"])
        line(im, 44, 34, 46, 25 + hand, CHAR_COLORS["N"])
        line(im, 45, 34, 47, 25 + hand, CHAR_COLORS["N"])
        rect(im, 0, 46, W, H, WOOD_D)
        cx = (t * 4) % W
        for off in (0, -W):
            sprite(im, CAT_RUN[(t // 2) % 2], W - 1 - (cx + off), 37, flip=False)
        petals(im, t, N, 31, 8, (0, 0, W, 44))
        frames.append(im)
    save_gif(frames, OUT / "footer.gif", scale=4, ms=90)


def header(slug, title, accent):
    W, H, N = 240, 15, 32
    frames = []
    tw = text_w(title)
    for t in range(N):
        im = gradient(W, H, [NIGHT0, NIGHT1])
        rect(im, 0, H - 1, W, H - 1, NIGHT3)
        # energy pulse along the base
        p = int(t * (W + 40) / N) - 20
        for k in range(22):
            put(im, p - k, H - 1, mix(accent, NIGHT3, k / 22))
        x0 = (W - tw) // 2
        for side in (-1, 1):
            base = x0 - 12 if side < 0 else x0 + tw + 11
            for k in range(5):
                rect(im, base + side * k * 6, 6, base + side * k * 6 + 2, 8, mix(accent, NIGHT1, k / 5))
        text(im, title, x0, 4, lambda x, y: WHITE if abs((x * 1 - t * 8) % 256 - 40) < 6 else accent, shadow=NIGHT0)
        frames.append(im)
    save_gif(frames, OUT / f"h_{slug}.gif", scale=4, ms=100)


def headers():
    for slug, title, c in (
        ("skills", "SKILLS", CYAN),
        ("problems", "PROBLEMS I SOLVED", PINK),
        ("hobbies", "HOBBIES", GOLD),
        ("interests", "INTERESTS", PURPLE),
        ("snake", "CONTRIBUTIONS", GREEN),
        ("stats", "STATS", CYAN),
    ):
        header(slug, title, c)


PIECES = {
    "hero": hero, "gaming": gaming, "manga": manga, "pcbuild": pcbuild,
    "crypto": crypto, "interests": interests, "footer": footer, "headers": headers,
}


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for name in sys.argv[1:] or PIECES:
        PIECES[name]()
