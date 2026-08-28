"""Gemini TTS ile sahne seslendirmesi üretir (senkron — batch desteklemiyor).

Kullanım:
    python3 generate_tts.py <script.txt> <cikti_dizini> <ses_adi>

Kanal sesleri:  Audrey Hepburn = Enceladus,  Diana = Algieba
(her kanalın sesi ayrışma için farklı tutulur)

Çıktı: scene_N.wav (16-bit PCM, 24 kHz mono)
"""
import base64
import json
import os
import re
import sys
import time
import urllib.request
import wave

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import gemini_key  # noqa: E402

MODEL = "gemini-2.5-flash-preview-tts"


def scenes_from(path):
    text = open(path, encoding="utf-8").read()
    return {int(n): c.strip() for n, c in
            re.findall(r"\[SCENE(\d+)\]\s*\n(.*?)\n\[/SCENE\1\]", text, re.S)}


def synth(text, voice, out_path, retries=3):
    key = gemini_key()
    url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
           f"{MODEL}:generateContent?key={key}")
    body = json.dumps({
        "contents": [{"parts": [{"text": text}]}],
        "generationConfig": {
            "responseModalities": ["AUDIO"],
            "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}},
        },
    }).encode()
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                url, data=body, headers={"Content-Type": "application/json"}, method="POST")
            with urllib.request.urlopen(req, timeout=150) as resp:
                data = json.loads(resp.read())
            pcm = base64.b64decode(
                data["candidates"][0]["content"]["parts"][0]["inlineData"]["data"])
            with wave.open(out_path, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(24000)
                wf.writeframes(pcm)
            return len(pcm) / 2 / 24000
        except Exception as exc:
            print(f"  deneme {attempt + 1} basarisiz: {exc}", flush=True)
            time.sleep(5)
    raise RuntimeError(f"TTS basarisiz: {out_path}")


if __name__ == "__main__":
    script, out_dir, voice = sys.argv[1], sys.argv[2], sys.argv[3]
    os.makedirs(out_dir, exist_ok=True)
    total = 0.0
    for num, text in sorted(scenes_from(script).items()):
        dur = synth(text, voice, os.path.join(out_dir, f"scene_{num}.wav"))
        total += dur
        print(f"Scene {num}: OK ({dur:.1f}s)", flush=True)
    print(f"\nTOPLAM: {total:.1f} sn (~{total / 60:.1f} dk)")
