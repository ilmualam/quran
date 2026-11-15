"""Branded 1200x675 featured cards for refreshed posts -> assets/blog/<name>.webp. Arabic is shaped with RAQM using the
site's own Amiri subset (assets/fonts/*.woff2, converted once with fontTools). Usage: from cards import card."""
import math, os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
OUT = f"{REPO}/assets/blog"
B = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"
M = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"
AR = f"{HERE}/.amiri.ttf"
W, H = 1200, 675


def _arabic_font():
    if not os.path.exists(AR):
        from fontTools.ttLib import TTFont
        f = TTFont(f"{REPO}/assets/fonts/amiri-arabic-400-normal.woff2"); f.flavor = None; f.save(AR)
    return AR


def _wrap(d, text, font, width):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= width:
            cur = t
        else:
            lines.append(cur); cur = w
    return lines + [cur]


def card(name, kicker, title, sub, arabic, foot="Mazhab Syafi'i · Dalil Sahih"):
    os.makedirs(OUT, exist_ok=True)
    im = Image.new("RGB", (W, H)); px = im.load()
    for y in range(H):
        for x in range(0, W, 4):
            t = x / W * 0.6 + y / H * 0.4
            c = (int(12 + 19 * t), int(56 + 66 * t), int(8 + 52 * t))
            for k in range(4):
                px[x + k, y] = c
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    for i in range(5):
        for j in range(6):
            cx, cy, r = 880 + i * 80, 40 + j * 120 + (40 if i % 2 else 0), 30
            od.polygon([(cx + r * math.cos(a * math.pi / 4 + math.pi / 8), cy + r * math.sin(a * math.pi / 4 + math.pi / 8)) for a in range(8)], outline=(255, 255, 255, 28), width=2)
    od.rounded_rectangle((50, 50, W - 50, H - 50), radius=28, outline=(201, 162, 39, 255), width=3)
    im = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB"); d = ImageDraw.Draw(im)
    fk, ft, fs = ImageFont.truetype(M, 28), ImageFont.truetype(B, 64), ImageFont.truetype(M, 30)
    fa = ImageFont.truetype(_arabic_font(), 72, layout_engine=ImageFont.Layout.RAQM)
    d.rounded_rectangle((100, 100, 100 + d.textlength(kicker, font=fk) + 40, 146), radius=23, fill=(255, 226, 122))
    d.text((120, 106), kicker, font=fk, fill=(12, 40, 8))
    d.text((W - 100, 96), arabic, font=fa, fill=(255, 236, 170), anchor="ra", direction="rtl", language="ar")
    y = 270
    for line in _wrap(d, title, ft, 820)[:3]:
        d.text((100, y), line, font=ft, fill="white"); y += 78
    y += 8
    for line in _wrap(d, sub, fs, 760)[:2]:
        d.text((100, y), line, font=fs, fill=(220, 240, 225)); y += 42
    d.text((100, H - 108), "ilmualam.com", font=ImageFont.truetype(B, 30), fill=(255, 226, 122))
    d.text((W - 100, H - 106), foot, font=fk, fill=(220, 240, 225), anchor="ra")
    im.save(f"{OUT}/{name}.webp", "WEBP", quality=82, method=6)
    return f"{name}.webp"
