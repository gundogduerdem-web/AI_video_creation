"""Uzun videonun sahne-1 hook'undan dikey Shorts teaser'ı üretir (≤60 sn).

Kullanım:
    python3 build_short.py <is_adi> <sahne1_metni.txt> <timings.json> \
                           <sahne1_ses.wav> <dikey_gorsel.png> [kesim_sn]

Öğrenilmiş kurallar:
  * Kaynak görsel olarak yatay sahne görselinin dikey kırpımı KULLANILMAZ —
    kompozisyona göre ana karakteri kadraj dışında bırakıyor. Bunun yerine
    Shorts için zaten üretilen natif 9:16 thumbnail görseli kullanılır
    (ek maliyet yok).
  * Kesim noktası kelime zamanlamalarından bulunan DOĞAL BİR CÜMLE SONU
    olmalı; tercihen merak bırakan bir cümlede (yarım cümle bırakma).
  * Son 3,5 saniyede "WATCH THE FULL STORY / LINK IN DESCRIPTION" bindirmesi.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FPS = 25

# Yonlendirme bindirmesi. Shorts'ta aciklama katlanmis geldigi icin tek basina
# "link in description" zayif kaliyor; bu yuzden kapanis kartindan once ustte
# erken bir kue de gosteriliyor. Ust bant (y=120) secildi: altyazi bandiyla da,
# YouTube'un kendi alt arayuzuyle de (baslik/kanal/related link) cakismiyor.
CUE_SEC = 10.0     # erken kue kac saniye once basliyor
CARD_SEC = 4.0     # kapanis karti kac saniye once basliyor
CUE_TEXT = "FULL STORY ON THIS CHANNEL"
# Kanal "advanced features"e gecip Shorts'a Related video baglarsa bu satir
# "TAP THE LINK BELOW" olarak degistirilir (baglanti o zaman oynaticida gorunur).
CARD_TEXT = "LINK IN DESCRIPTION"


def sentence_ends(text_path, timings_path, limit=60.0):
    """Kesime uygun cümle sonlarını (saniye, önizleme) olarak döndürür."""
    words = json.load(open(timings_path, encoding="utf-8"))
    orig = open(text_path, encoding="utf-8").read().split()
    n, m = len(orig), len(words)
    out = []
    for i, w in enumerate(orig):
        if w.endswith("."):
            t = words[min(round(i * (m - 1) / (n - 1)), m - 1)]["end"]
            if t < limit:
                out.append((t, " ".join(orig[max(0, i - 7):i + 1])))
    return out


def build(name, text_path, timings_path, audio_path, image_path, cut):
    work = os.environ.get("PIPELINE_WORK", ".")
    os.chdir(work)
    os.makedirs("shorts", exist_ok=True)

    words = json.load(open(timings_path, encoding="utf-8"))
    orig = open(text_path, encoding="utf-8").read().split()
    n, m = len(orig), len(words)
    keep = [w for i, w in enumerate(orig)
            if words[min(round(i * (m - 1) / (n - 1)), m - 1)]["end"] <= cut]
    kept_text = " ".join(keep)
    kept_timings = [w for w in words if w["end"] <= cut]

    tim_out = f"shorts/{name}_timings.json"
    json.dump(kept_timings, open(tim_out, "w"), ensure_ascii=False)
    print(f"kesim {cut}s -> {len(keep)}/{n} kelime")

    wav = f"shorts/{name}.wav"
    subprocess.run(["ffmpeg", "-y", "-i", audio_path, "-t", str(cut),
                    "-c", "copy", wav, "-loglevel", "error"], check=True)
    dur = float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", wav], capture_output=True, text=True).stdout.strip())

    ass = f"shorts/{name}.ass"
    subprocess.run(["python3", os.path.join(HERE, "subtitles.py"),
                    kept_text, tim_out, ass, "--vertical"], check=True)

    frames = int(dur * FPS) + 5
    cue_at = f"{max(0.0, dur - CUE_SEC):.2f}"      # erken, kucuk hatirlatma
    card_at = f"{max(0.0, dur - CARD_SEC):.2f}"    # kapanis karti
    vf = (f"[0:v]scale=1080:1920:flags=lanczos,"
          f"zoompan=z='min(zoom+0.00009,1.10)':d={frames}"
          f":x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps={FPS},"
          f"drawbox=x=0:y=1380:w=1080:h=260:color=black@1.0:t=fill,"
          f"ass={ass},"
          # erken kue: ustte, koyu plaka uzerinde (goruntu acik olsa da okunur)
          f"drawbox=x=0:y=120:w=1080:h=86:color=black@0.55:t=fill"
          f":enable='between(t,{cue_at},{card_at})',"
          f"drawtext=fontfile={FONT}:text='{CUE_TEXT}':fontcolor=0xE8B923"
          f":fontsize=46:x=(w-text_w)/2:y=142"
          f":enable='between(t,{cue_at},{card_at})',"
          # kapanis karti
          f"drawtext=fontfile={FONT}:text='WATCH THE FULL STORY':fontcolor=0xE8B923"
          f":fontsize=58:x=(w-text_w)/2:y=300:enable='gte(t,{card_at})',"
          f"drawtext=fontfile={FONT}:text='{CARD_TEXT}':fontcolor=white"
          f":fontsize=40:x=(w-text_w)/2:y=390:enable='gte(t,{card_at})'[v]")

    out = f"shorts/{name}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loop", "1", "-i", image_path, "-i", wav,
                    "-filter_complex", vf, "-map", "[v]", "-map", "1:a",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "18",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", out, "-loglevel", "error"], check=True)
    print(f"SHORT: {out} ({dur:.2f}s)")
    return out


if __name__ == "__main__":
    name, text_p, tim_p, aud_p, img_p = sys.argv[1:6]
    if len(sys.argv) > 6:
        build(name, text_p, tim_p, aud_p, img_p, float(sys.argv[6]))
    else:
        print("Uygun kesim noktalari (saniye | cumle sonu):")
        for t, preview in sentence_ends(text_p, tim_p):
            print(f"  {t:6.1f}  ...{preview}")
        print("\nBirini secip son argüman olarak ver (biraz üstüne ekle, ör. 50.4 -> 50.6)")
