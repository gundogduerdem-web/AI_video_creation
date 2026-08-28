"""Google Speech-to-Text ile kelime düzeyinde zamanlama çıkarır.

Altyazı senkronu için şart: sezgisel (silence-detect) zamanlama denendi ve
0,5-2 sn kayma verdi; gerçek forced alignment ile sorun çözüldü.

Kullanım:
    python3 transcribe.py <ses_dizini> <cikti_dizini> [ilk] [son]

Notlar:
  * Inline ses için ~60 sn sınırı var; uzun sahneler otomatik ikiye bölünüp
    ikinci yarının zaman damgaları kaydırılarak birleştirilir.
  * Ağ kopmaları oluyor — her sahne 3 kez denenir.
  * Servis hesabı yerine OAuth kullanılır (API anahtarı desteklenmiyor).
"""
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request
import wave

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import drive_token  # noqa: E402

PROJECT_ID = "gen-lang-client-0486434271"


def _call(pcm, token):
    body = json.dumps({
        "config": {
            "encoding": "LINEAR16",
            "sampleRateHertz": 24000,
            "languageCode": "en-US",
            "enableWordTimeOffsets": True,
        },
        "audio": {"content": base64.b64encode(pcm).decode("ascii")},
    }).encode()
    headers = {"Authorization": f"Bearer {token}",
               "x-goog-user-project": PROJECT_ID,
               "Content-Type": "application/json"}
    req = urllib.request.Request(
        "https://speech.googleapis.com/v1/speech:longrunningrecognize",
        data=body, method="POST", headers=headers)
    with urllib.request.urlopen(req, timeout=60) as resp:
        op = json.loads(resp.read())["name"]

    for _ in range(60):
        time.sleep(3)
        poll = urllib.request.Request(
            f"https://speech.googleapis.com/v1/operations/{op}",
            headers={"Authorization": f"Bearer {token}",
                     "x-goog-user-project": PROJECT_ID})
        with urllib.request.urlopen(poll, timeout=30) as resp:
            status = json.loads(resp.read())
        if status.get("done"):
            break
    else:
        raise TimeoutError("STT islemi zaman asimina ugradi")

    if "error" in status:
        raise RuntimeError(str(status["error"]))

    words = []
    for result in status.get("response", {}).get("results", []):
        for w in result["alternatives"][0].get("words", []):
            words.append({
                "word": w["word"],
                "start": float(w["startTime"].rstrip("s")),
                "end": float(w["endTime"].rstrip("s")),
            })
    return words


def transcribe_one(path, token):
    with wave.open(path, "rb") as wf:
        frames, rate = wf.getnframes(), wf.getframerate()
        pcm = wf.readframes(frames)
    try:
        return _call(pcm, token)
    except urllib.error.HTTPError as exc:
        if exc.code != 400 or b"duration limit" not in exc.read():
            raise
    # 60 sn sinirini asan sahne: ortadan ikiye bol, ikinci yariyi kaydir
    mid = frames // 2
    offset = mid / rate
    first = _call(pcm[:mid * 2], token)
    second = _call(pcm[mid * 2:], token)
    for w in second:
        w["start"] += offset
        w["end"] += offset
    return first + second


if __name__ == "__main__":
    audio_dir, out_dir = sys.argv[1], sys.argv[2]
    start = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    end = int(sys.argv[4]) if len(sys.argv) > 4 else 8
    os.makedirs(out_dir, exist_ok=True)

    for i in range(start, end + 1):
        for attempt in range(3):
            try:
                token = drive_token()  # cloud-platform kapsamli kullanici tokeni
                words = transcribe_one(os.path.join(audio_dir, f"scene_{i}.wav"), token)
                with open(os.path.join(out_dir, f"scene_{i}.json"), "w",
                          encoding="utf-8") as fh:
                    json.dump(words, fh, ensure_ascii=False, indent=2)
                print(f"Scene {i}: {len(words)} kelime zamanlandi", flush=True)
                break
            except Exception as exc:
                print(f"Scene {i} deneme {attempt + 1}: {exc}", flush=True)
                time.sleep(8)
        else:
            raise RuntimeError(f"Scene {i} zamanlanamadi")
