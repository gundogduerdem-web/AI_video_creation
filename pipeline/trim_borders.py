"""Üretilen karelerdeki düz siyah film çerçevesini kırpar.

Kullanım:
    python3 trim_borders.py <gorsel_dizini> [--dry-run]

Fotoğraf dili ("35mm film", "imperfect framing") modeli bazen kareye düz
siyah bir film kenarlığı çizmeye itiyor. build_video.sh kareyi 2688x1536'ya
ölçekleyip crop'ladığı için bu kenarlık videoda siyah şerit olarak görünür.

Gerçek kenarlık ile karanlık sahne içeriğini ayıran ölçüt **varyans**:
kenarlık düz siyahtır (varyans ~0), karanlık bir koğuş duvarında ise doku
vardır. Kırpma sonrası kare 16:9'a (1.75) merkezden yeniden oturtulur.
"""
import glob
import os
import sys

import numpy as np
from PIL import Image

RATIO = 2688 / 1536          # build_video.sh'in bekledigi oran
DARK = 8                     # ortalama parlaklik esigi (gercek kenarlik tam siyahtir)
FLAT = 2.0                   # standart sapma esigi (duz siyah)
MAX_FRAC = 0.08              # bir kenardan en fazla %8 kirp
                             # (karanlik sahne icerigini kenarlik sanmamak icin)


def border(line_stats):
    """Bastan itibaren kac satir/sutunun duz siyah oldugunu doner."""
    n = 0
    for mean, std in line_stats:
        if mean < DARK and std < FLAT:
            n += 1
        else:
            break
    return n


def trim(path, dry_run=False):
    im = Image.open(path).convert("RGB")
    a = np.asarray(im.convert("L"), dtype=np.float32)
    h, w = a.shape
    cap_w, cap_h = int(w * MAX_FRAC), int(h * MAX_FRAC)

    left = min(border([(a[:, x].mean(), a[:, x].std()) for x in range(cap_w)]), cap_w)
    right = min(border([(a[:, w - 1 - x].mean(), a[:, w - 1 - x].std())
                        for x in range(cap_w)]), cap_w)
    top = min(border([(a[y, :].mean(), a[y, :].std()) for y in range(cap_h)]), cap_h)
    bottom = min(border([(a[h - 1 - y, :].mean(), a[h - 1 - y, :].std())
                         for y in range(cap_h)]), cap_h)

    if max(left, right, top, bottom) < 4:
        print(f"{os.path.basename(path)}: kenarlik yok")
        return False

    box = im.crop((left, top, w - right, h - bottom))
    bw, bh = box.size
    # 16:9'a merkezden oturt
    if bw / bh > RATIO:
        new_w = int(bh * RATIO)
        box = box.crop(((bw - new_w) // 2, 0, (bw - new_w) // 2 + new_w, bh))
    else:
        new_h = int(bw / RATIO)
        box = box.crop((0, (bh - new_h) // 2, bw, (bh - new_h) // 2 + new_h))

    print(f"{os.path.basename(path)}: sol={left} sag={right} ust={top} alt={bottom}"
          f" -> {box.size[0]}x{box.size[1]}" + ("  (dry-run)" if dry_run else ""))
    if not dry_run:
        box.save(path)
    return True


if __name__ == "__main__":
    d = sys.argv[1]
    dry = "--dry-run" in sys.argv
    files = sorted(glob.glob(os.path.join(d, "*.png")),
                   key=lambda p: int("".join(c for c in os.path.basename(p) if c.isdigit())))
    n = sum(trim(f, dry) for f in files)
    print(f"\n{n}/{len(files)} karede kenarlik kirpildi")
