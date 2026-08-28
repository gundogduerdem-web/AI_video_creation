"""ASS altyazı üretir: kelime kelime altın sarısına dönen karaoke stili.

Kanal standardı: siyah bant + okunmamış kelimeler soluk altın, okunan
kelimeler parlak altın.

Kullanım:
    python3 subtitles.py <metin> <timings.json> <cikti.ass> [--vertical]

--vertical  Shorts için 1080x1920 düzen (satır başına 4 kelime, bant üstte
            kalacak şekilde alt marj büyük).
"""
import json
import sys

GOLD_BRIGHT = "&H0023B9E8&"   # #E8B923, BGR sirasi
GOLD_DIM = "&H00125D74&"

HEADER = """[Script Info]
ScriptType: v4.00+
PlayResX: {w}
PlayResY: {h}

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,{fs},&H0023B9E8,&H0023B9E8,&H00000000,&H00000000,1,0,0,0,100,100,0,0,1,0,0,2,{ml},{mr},{mv},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def fmt(t):
    return f"{int(t // 3600)}:{int((t % 3600) // 60):02d}:{t % 60:05.2f}"


def align(original, stt):
    """Orijinal (gosterilecek) kelimeleri STT zamanlarina oransal esler.

    STT bazen 1-3 kelime kacirir; oransal indeks eslemesi bu kucuk
    farklara dayaniklidir ve kelime kelime esleme denemesinden daha
    saglam sonuc verir.
    """
    n, m = len(original), len(stt)
    if m == 0:
        return [(w, 0.0, 0.0) for w in original]
    out = []
    for i, w in enumerate(original):
        idx = round(i * (m - 1) / (n - 1)) if n > 1 else 0
        idx = max(0, min(m - 1, idx))
        out.append((w, stt[idx]["start"], stt[idx]["end"]))
    return out


def build(word_times, chunk_size, layout):
    lines = [HEADER.format(**layout)]
    for i in range(0, len(word_times), chunk_size):
        chunk = word_times[i:i + chunk_size]
        for idx, (_, start, end) in enumerate(chunk):
            parts = ["{\\c" + (GOLD_BRIGHT if j <= idx else GOLD_DIM) + "}" + w
                     for j, (w, _, _) in enumerate(chunk)]
            if end <= start:
                end = start + 0.15
            lines.append(
                f"Dialogue: 0,{fmt(start)},{fmt(end)},Default,,0,0,0,,{' '.join(parts)}")
    return "\n".join(lines)


if __name__ == "__main__":
    text, timings_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    vertical = "--vertical" in sys.argv

    layout = (dict(w=1080, h=1920, fs=64, ml=40, mr=40, mv=360) if vertical
              else dict(w=1920, h=1080, fs=64, ml=80, mr=80, mv=90))
    chunk = 4 if vertical else 6

    original = text.split()
    stt = json.load(open(timings_path, encoding="utf-8"))
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(build(align(original, stt), chunk, layout))
    print(f"{len(original)} kelime, {len(stt)} STT -> {out_path}")
