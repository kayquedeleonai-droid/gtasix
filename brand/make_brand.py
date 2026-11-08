"""Gera foto de perfil e capa do canal GTAVI | MISSION PASSED.

Uso: python3 brand/make_brand.py
Fundos em brand/source (gerados na Magnific), saídas em brand/output.
"""
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).parent
SRC, OUT, FONTS = ROOT / "source", ROOT / "output", ROOT / "fonts"
OUT.mkdir(exist_ok=True)

WHITE = (255, 255, 255)
GOLD = (255, 196, 40)
PINK = (255, 62, 165)
BLACK = (10, 6, 20)


def font(name, size):
    return ImageFont.truetype(str(FONTS / name), size)


def cover(img, w, h):
    s = max(w / img.width, h / img.height)
    img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    x, y = (img.width - w) // 2, (img.height - h) // 2
    return img.crop((x, y, x + w, y + h))


def star_points(cx, cy, r_out, r_in, rot=-90):
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 36)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def shadow_layer(size, draw_fn, blur, offset=(0, 0), color=(0, 0, 0, 200)):
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    mask = Image.new("L", size, 0)
    draw_fn(ImageDraw.Draw(mask), offset)
    mask = mask.filter(ImageFilter.GaussianBlur(blur))
    layer.paste(Image.new("RGBA", size, color), (0, 0), mask)
    return layer


def text_block(base, text, f, center_x, top, fill, stroke, stroke_w, shadow=12, glow=None):
    """Texto estilo 'mission passed': preenchimento, contorno grosso e sombra."""
    d = ImageDraw.Draw(base)
    bbox = d.textbbox((0, 0), text, font=f, stroke_width=stroke_w)
    x = center_x - (bbox[2] - bbox[0]) / 2 - bbox[0]
    y = top - bbox[1]

    def draw(dr, off, sw=stroke_w):
        dr.text((x + off[0], y + off[1]), text, font=f, fill=255, stroke_width=sw, stroke_fill=255)

    if glow:
        base.alpha_composite(shadow_layer(base.size, lambda dr, o: draw(dr, o, stroke_w * 3), 28, color=glow))
    base.alpha_composite(shadow_layer(base.size, draw, shadow, offset=(0, shadow), color=(0, 0, 0, 220)))
    d.text((x, y), text, font=f, fill=fill, stroke_width=stroke_w, stroke_fill=stroke)
    return bbox[3] - bbox[1]


def stars_row(base, cx, cy, n, r, gap, glow=(255, 220, 120, 210)):
    total = (n - 1) * gap
    xs = [cx - total / 2 + i * gap for i in range(n)]

    def draw(dr, off):
        for sx in xs:
            dr.polygon(star_points(sx + off[0], cy + off[1], r * 1.25, r * 0.6), fill=255)

    base.alpha_composite(shadow_layer(base.size, draw, r * 0.6, color=glow))
    d = ImageDraw.Draw(base)
    for sx in xs:
        d.polygon(star_points(sx, cy, r + 6, (r + 6) * 0.45), fill=BLACK)
        d.polygon(star_points(sx, cy, r, r * 0.45), fill=WHITE)


def banner():
    W, H = 2560, 1440
    img = cover(Image.open(SRC / "banner_bg.png").convert("RGB"), W, H).convert("RGBA")
    # vinheta escura no centro para o texto ler bem sobre o sol
    band = Image.new("L", (W, H), 0)
    ImageDraw.Draw(band).ellipse((W / 2 - 900, H / 2 - 300, W / 2 + 900, H / 2 + 300), fill=150)
    band = band.filter(ImageFilter.GaussianBlur(120))
    img.paste(Image.new("RGBA", (W, H), (25, 8, 45, 255)), (0, 0), band)

    cx = W / 2
    stars_row(img, cx, 536, 5, 20, 62)
    text_block(img, "GTA VI", font("Anton.woff", 168), cx, 566, WHITE, BLACK, 10, glow=(255, 62, 165, 150))
    text_block(img, "MISSION PASSED", font("Anton.woff", 84), cx, 760, GOLD, BLACK, 7)
    text_block(img, "CURIOSIDADES  •  SEGREDOS  •  MELHORES MOMENTOS", font("BebasNeue.woff", 42), cx, 874, WHITE, BLACK, 4, shadow=6)
    img.convert("RGB").save(OUT / "capa_youtube_2560x1440.png", optimize=True)

    # prévia com a área segura (o que aparece em todos os aparelhos)
    prev = img.copy()
    ImageDraw.Draw(prev).rectangle((507, 508, 2053, 931), outline=(0, 255, 120, 255), width=6)
    prev.convert("RGB").resize((1280, 720)).save(OUT / "_previa_area_segura.jpg", quality=90)


def profile(src_name, out_name):
    S = 800
    img = cover(Image.open(SRC / src_name).convert("RGB"), S, S).convert("RGBA")
    shade = Image.new("L", (S, S), 0)
    ImageDraw.Draw(shade).ellipse((120, 330, 680, 600), fill=140)
    shade = shade.filter(ImageFilter.GaussianBlur(50))
    img.paste(Image.new("RGBA", (S, S), (25, 8, 45, 255)), (0, 0), shade)
    text_block(img, "GTA VI", font("Anton.woff", 210), S / 2, 355, WHITE, BLACK, 10, shadow=10, glow=(255, 62, 165, 140))
    img.convert("RGB").save(OUT / out_name, optimize=True)
    prev = img.copy()
    m = Image.new("L", (S, S), 0)
    ImageDraw.Draw(m).ellipse((0, 0, S, S), fill=255)
    circ = Image.new("RGBA", (S, S), (33, 33, 33, 255))
    circ.paste(prev, (0, 0), m)
    circ.convert("RGB").save(OUT / ("_previa_circulo_" + out_name.replace(".png", ".jpg")), quality=90)


if __name__ == "__main__":
    banner()
    profile("logo_bg_a.png", "perfil_A_800x800.png")
    profile("logo_bg_b.png", "perfil_B_800x800.png")
    print("ok:", sorted(p.name for p in OUT.iterdir()))
