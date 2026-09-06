"""Google Cloud Text-to-Speech ile sahne seslendirmesi üretir.

Kullanım:
    python3 generate_tts.py <script.txt> <cikti_dizini> <ses_adi>

Kanal sesleri:  Audrey Hepburn = Enceladus,  Diana = Algieba
(her kanalın sesi ayrışma için farklı tutulur)

Ses adı kısa verilir (Enceladus); Chirp3-HD tam adına burada çevrilir.
Bunlar Gemini TTS'teki seslerin aynısı — kanal sesi değişmiyor, yalnızca
fatura AI Studio ön ödemeli bakiyesinden Google Cloud kredisine taşındı.

Çıktı: scene_N.wav (16-bit PCM, 24 kHz mono) — Cloud TTS LINEAR16'yı
RIFF başlıklı gönderdiği için yanıt doğrudan dosyaya yazılır.
"""
import base64
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
import wave

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import cloud_token  # noqa: E402

URL = "https://texttospeech.googleapis.com/v1/text:synthesize"
LANG = "en-US"
RATE = 24000
MAX_CHARS = 4800  # Cloud TTS istek basina 5000 bayt siniri


def voice_name(voice):
    """Kisa ses adini (Algieba) Chirp3-HD tam adina cevirir."""
    return voice if voice.startswith(LANG) else f"{LANG}-Chirp3-HD-{voice}"


def scenes_from(path):
    text = open(path, encoding="utf-8").read()
    return {int(n): c.strip() for n, c in
            re.findall(r"\[SCENE(\d+)\]\s*\n(.*?)\n\[/SCENE\1\]", text, re.S)}


def _chunks(text):
    """Sinirin ustundeki metni cumle sinirindan boler."""
    if len(text.encode()) <= MAX_CHARS:
        return [text]
    out, cur = [], ""
    for sentence in re.findall(r"[^.!?]*[.!?]|\S+$", text):
        if len((cur + sentence).encode()) > MAX_CHARS and cur:
            out.append(cur.strip())
            cur = sentence
        else:
            cur += sentence
    if cur.strip():
        out.append(cur.strip())
    return out


def _synth_one(text, voice, retries=3):
    body = json.dumps({
        "input": {"text": text},
        "voice": {"languageCode": LANG, "name": voice_name(voice)},
        "audioConfig": {"audioEncoding": "LINEAR16", "sampleRateHertz": RATE},
    }).encode()
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                URL, data=body, method="POST",
                headers={"Authorization": f"Bearer {cloud_token()}",
                         "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=180) as resp:
                return base64.b64decode(json.loads(resp.read())["audioContent"])
        except urllib.error.HTTPError as exc:
            print(f"  deneme {attempt + 1} basarisiz: {exc.code} "
                  f"{exc.read().decode()[:200]}", flush=True)
            time.sleep(5)
        except Exception as exc:
            print(f"  deneme {attempt + 1} basarisiz: {exc}", flush=True)
            time.sleep(5)
    raise RuntimeError("TTS basarisiz")


def synth(text, voice, out_path):
    """Sahneyi seslendirip WAV yazar, suresini (sn) doner."""
    pcm = b""
    for chunk in _chunks(text):
        raw = _synth_one(chunk, voice)
        # LINEAR16 RIFF basligiyla geliyor; parcalari birlestirmek icin
        # basliklari soyup ham PCM'i topluyoruz.
        if raw[:4] == b"RIFF":
            idx = raw.find(b"data")
            raw = raw[idx + 8:] if idx != -1 else raw[44:]
        pcm += raw
    with wave.open(out_path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(RATE)
        wf.writeframes(pcm)
    return len(pcm) / 2 / RATE


if __name__ == "__main__":
    script, out_dir, voice = sys.argv[1], sys.argv[2], sys.argv[3]
    os.makedirs(out_dir, exist_ok=True)
    total = 0.0
    for num, text in sorted(scenes_from(script).items()):
        dur = synth(text, voice, os.path.join(out_dir, f"scene_{num}.wav"))
        total += dur
        print(f"Scene {num}: OK ({dur:.1f}s)", flush=True)
    print(f"\nTOPLAM: {total:.1f} sn (~{total / 60:.1f} dk)")
