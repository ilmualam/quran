"""1200x630 social cards (Open Graph / X) in the site's green, one per page. Only (re)drawn when missing or when the text changes."""
import os, hashlib

SCR = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(SCR)
OUT = f"{REPO}/assets/og"
BOLD = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"
REG = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"


def _wrap(d, text, font, width):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    return lines + [cur]


def card(name, title, sub):
    """Writes assets/og/<name>.jpg; returns its site path. Skips work when the stamped text hash already matches."""
    os.makedirs(OUT, exist_ok=True)
    path, stamp = f"{OUT}/{name}.jpg", f"{OUT}/.{name}.sha"
    h = hashlib.sha1(f"v2|{title}|{sub}".encode()).hexdigest()
    if os.path.exists(path) and os.path.exists(stamp) and open(stamp).read() == h:
        return f"assets/og/{name}.jpg"
    if not os.path.exists(BOLD):  # fonts missing on this machine (e.g. CI): keep whatever card is committed
        return f"assets/og/{name}.jpg" if os.path.exists(path) else None
    from PIL import Image, ImageDraw, ImageFont
    W, H = 1200, 630
    im = Image.new("RGB", (W, H))
    px = im.load()
    a, b = (26, 112, 56), (8, 40, 6)
    for y in range(H):
        for x in range(0, W):
            t = (x / W * .55 + y / H * .45)
            px[x, y] = tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))
    d = ImageDraw.Draw(im, "RGBA")
    for cx, cy, r in ((1080, 90, 210), (1150, 560, 150), (90, 600, 90)):  # soft hexagon echoes of the logo
        pts = [(cx + r * c, cy + r * s) for c, s in ((1, 0), (.5, .866), (-.5, .866), (-1, 0), (-.5, -.866), (.5, -.866))]
        d.polygon(pts, outline=(255, 255, 255, 34), width=10)
    logo = Image.open(f"{REPO}/assets/icons/icon-192.png").convert("RGBA").resize((96, 96), Image.LANCZOS)
    plate = Image.new("RGBA", (124, 124), (0, 0, 0, 0))
    ImageDraw.Draw(plate).rounded_rectangle((0, 0, 123, 123), 28, fill=(255, 255, 255, 255))
    plate.alpha_composite(logo, (14, 14))
    im.paste(plate, (72, 64), plate)
    d.text((222, 84), "Al-Quran Online", font=ImageFont.truetype(BOLD, 38), fill=(255, 255, 255))
    d.text((222, 134), "quran.ilmualam.com", font=ImageFont.truetype(REG, 28), fill=(191, 240, 207))
    size = 70
    while True:
        f = ImageFont.truetype(BOLD, size)
        lines = _wrap(d, title, f, W - 150)
        if len(lines) <= 3 or size <= 46:
            break
        size -= 4
    y = 236
    for ln in lines:
        d.text((72, y), ln, font=f, fill=(255, 255, 255))
        y += int(size * 1.18)
    fs = ImageFont.truetype(REG, 31)
    for ln in _wrap(d, sub, fs, W - 150)[:2]:
        d.text((72, y + 14), ln, font=fs, fill=(216, 240, 223))
        y += 42
    d.rounded_rectangle((72, 548, 72 + 330, 592), 22, fill=(255, 255, 255, 38))
    d.text((94, 556), "Percuma · Tanpa akaun", font=ImageFont.truetype(REG, 24), fill=(255, 255, 255))
    im.save(path, "JPEG", quality=84, optimize=True, progressive=True)
    open(stamp, "w").write(h)
    return f"assets/og/{name}.jpg"


PIN = f"{REPO}/assets/pin"


def pin(name, kicker, title, sub):
    """Writes assets/pin/<name>.jpg, a 1000x1500 (2:3) Pinterest pin in the same style as card(). Same skip-if-unchanged stamp."""
    os.makedirs(PIN, exist_ok=True)
    path, stamp = f"{PIN}/{name}.jpg", f"{PIN}/.{name}.sha"
    h = hashlib.sha1(f"p1|{kicker}|{title}|{sub}".encode()).hexdigest()
    if os.path.exists(path) and os.path.exists(stamp) and open(stamp).read() == h:
        return f"assets/pin/{name}.jpg"
    if not os.path.exists(BOLD):
        return f"assets/pin/{name}.jpg" if os.path.exists(path) else None
    from PIL import Image, ImageDraw, ImageFont
    W, H = 1000, 1500
    im = Image.new("RGB", (W, H))
    px = im.load()
    a, b = (26, 112, 56), (8, 40, 6)
    for y in range(H):
        for x in range(W):
            t = x / W * .35 + y / H * .65
            px[x, y] = tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))
    d = ImageDraw.Draw(im, "RGBA")
    for cx, cy, r in ((900, 140, 260), (980, 1320, 200), (60, 1420, 120)):
        pts = [(cx + r * c, cy + r * s) for c, s in ((1, 0), (.5, .866), (-.5, .866), (-1, 0), (-.5, -.866), (.5, -.866))]
        d.polygon(pts, outline=(255, 255, 255, 34), width=12)
    logo = Image.open(f"{REPO}/assets/icons/icon-192.png").convert("RGBA").resize((104, 104), Image.LANCZOS)
    plate = Image.new("RGBA", (136, 136), (0, 0, 0, 0))
    ImageDraw.Draw(plate).rounded_rectangle((0, 0, 135, 135), 30, fill=(255, 255, 255, 255))
    plate.alpha_composite(logo, (16, 16))
    im.paste(plate, (72, 80), plate)
    d.text((232, 98), "Al-Quran Online", font=ImageFont.truetype(BOLD, 42), fill=(255, 255, 255))
    d.text((232, 152), "quran.ilmualam.com", font=ImageFont.truetype(REG, 30), fill=(191, 240, 207))
    fk = ImageFont.truetype(BOLD, 30)
    kw = d.textlength(kicker.upper(), font=fk)
    d.rounded_rectangle((72, 300, 72 + kw + 48, 356), 28, fill=(227, 193, 90, 255))
    d.text((96, 310), kicker.upper(), font=fk, fill=(12, 56, 8))
    size = 96
    while True:
        f = ImageFont.truetype(BOLD, size)
        lines = _wrap(d, title, f, W - 144)
        if len(lines) <= 5 or size <= 60:
            break
        size -= 6
    y = 410
    for ln in lines:
        d.text((72, y), ln, font=f, fill=(255, 255, 255))
        y += int(size * 1.16)
    fs = ImageFont.truetype(REG, 40)
    y += 30
    for ln in _wrap(d, sub, fs, W - 144)[:6]:
        d.text((72, y), ln, font=fs, fill=(216, 240, 223))
        y += 56
    d.rounded_rectangle((72, 1330, W - 72, 1420), 45, fill=(255, 255, 255, 255))
    fc = ImageFont.truetype(BOLD, 36)
    cta = "Baca percuma di quran.ilmualam.com"
    d.text(((W - d.textlength(cta, font=fc)) / 2, 1355), cta, font=fc, fill=(12, 56, 8))
    im.save(path, "JPEG", quality=80, optimize=True, progressive=True)
    open(stamp, "w").write(h)
    return f"assets/pin/{name}.jpg"
