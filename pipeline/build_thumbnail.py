"""Thumbnail üretir: renkli yakın plan kare + isim + merak metni.

Kullanım:
    python3 build_thumbnail.py <taban_gorsel> <cikti.jpg> "ISIM" "MERAK METNI" [taraf]

taraf: metnin hangi yarıya yaslanacağı — "left" (varsayılan) veya "right".
Yüzün olduğu tarafa yazma; kompozisyonu kapatır.

Kanal standardı (CONTENT_STRATEGY.md):
  * renkli, yakın plan, tek kare (B&W split-frame artık varsayılan değil)
  * konunun ismi mutlaka yer alır — 60+ kitlede tanınırlık odaklı tıklama
  * Anton font; isim küçük/beyaz üstte, merak metni büyük/altın (#E8B923) altta
  * siyah kontur + drop shadow
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1280, 720
GOLD = "#E8B923"
OUTLINE = 8
FONT = os.environ.get(
    "ANTON_FONT",
    "/tmp/claude-0/-home-user-AI-video-creation/"
    "6eb5ab10-2a79-5396-b283-79b467dc27e8/scratchpad/fonts/Anton-Regular.ttf")


def wrap(draw, text, font, max_w):
    """Metni verilen genislige gore satirlara boler."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit(draw, text, max_w, max_h, start, min_size=34):
    """Metni kutuya sigdiran en buyuk punto + satirlari doner."""
    for size in range(start, min_size - 1, -2):
        font = ImageFont.truetype(FONT, size)
        lines = wrap(draw, text, font, max_w)
        line_h = int(size * 1.06)
        if len(lines) * line_h <= max_h:
            return font, lines, line_h
    font = ImageFont.truetype(FONT, min_size)
    return font, wrap(draw, text, font, max_w), int(min_size * 1.06)


def stroked(draw, xy, text, font, fill):
    draw.text(xy, text, font=font, fill=fill,
              stroke_width=OUTLINE, stroke_fill="black")


def build(base_path, out_path, name, hook, side="left"):
    im = Image.open(base_path).convert("RGB").resize((W, H), Image.LANCZOS)

    # Metin tarafini hafifce karart: kontur tek basina okunurlugu tasimiyor.
    shade = Image.new("L", (W, H), 0)
    ImageDraw.Draw(shade).rectangle(
        [0, 0, int(W * 0.60), H] if side == "left" else [int(W * 0.40), 0, W, H],
        fill=140)
    im = Image.composite(Image.new("RGB", (W, H), "black"), im,
                         shade.filter(ImageFilter.GaussianBlur(90)))

    draw = ImageDraw.Draw(im)
    margin = 52
    box_w = int(W * 0.54) - margin
    x = margin if side == "left" else W - margin - box_w

    name_font = ImageFont.truetype(FONT, 54)
    stroked(draw, (x, margin), name.upper(), name_font, "white")

    hook_font, lines, line_h = fit(draw, hook.upper(), box_w, int(H * 0.52), 104)
    y = H - margin - len(lines) * line_h
    for line in lines:
        stroked(draw, (x, y), line, hook_font, GOLD)
        y += line_h

    im.save(out_path, "JPEG", quality=92)
    kb = os.path.getsize(out_path) // 1024
    print(f"{out_path} ({W}x{H}, {kb} KB, {len(lines)} satir, {hook_font.size}pt)")


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4],
          sys.argv[5] if len(sys.argv) > 5 else "left")
