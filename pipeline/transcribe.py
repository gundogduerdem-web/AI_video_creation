"""Google Speech-to-Text ile kelime düzeyinde zamanlama çıkarır.

Altyazı senkronu için şart: sezgisel (silence-detect) zamanlama denendi ve
0,5-2 sn kayma verdi; gerçek forced alignment ile sorun çözüldü.

Kullanım:
    python3 transcribe.py <ses_dizini> <cikti_dizini> [ilk] [son]

Notlar:
  * **v2 API kullanılır** (`v2/.../recognizers/_:recognize`). v1'in
    `longrunningrecognize` ucu 30 Ağustos 2026'da saatlerce 500/503
    ("An error occurred while checking permissions" / "Policy checks are
    unavailable") verdi; aynı kimlikle v2 sorunsuz çalıştı. v2 senkron
    döner, operation beklemek gerekmez.
  * Inline ses ~60 sn ile sınırlı. Sahneler 55 sn'lik parçalara bölünür;
    kesim noktası hep en sessiz an seçilir, böylece kelime ortasından
    bölünmez.
  * Ağ/servis hataları için 500/502/503/504 yeniden denenir.
  * OAuth şart (API anahtarı desteklenmiyor) ve token **cloud-platform**
    kapsamlı olmalı — Drive kapsamı yetmez, 403 ACCESS_TOKEN_SCOPE_INSUFFICIENT
    verir. Kimlik dosyası: speech_token.json
"""
import array
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request
import wave

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import access_token  # noqa: E402

PROJECT_ID = "gen-lang-client-0486434271"
RATE = 24000
CHUNK_SEC = 55.0
RETRYABLE = (500, 502, 503, 504)


def _open(req, timeout, tries=10):
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as exc:
            if exc.code not in RETRYABLE or attempt == tries - 1:
                raise
            body = exc.read()[:100].decode("utf-8", "replace").replace("\n", " ")
            print(f"    {exc.code} yeniden deneniyor: {body}", flush=True)
            time.sleep(min(5 * (attempt + 1), 30))


def _recognize(pcm, token):
    """Tek parca (<=60 sn) icin v2 senkron tanima."""
    body = json.dumps({
        "config": {
            "explicitDecodingConfig": {
                "encoding": "LINEAR16",
                "sampleRateHertz": RATE,
                "audioChannelCount": 1,
            },
            "languageCodes": ["en-US"],
            "model": "long",
            "features": {"enableWordTimeOffsets": True},
        },
        "content": base64.b64encode(pcm).decode("ascii"),
    }).encode()
    url = (f"https://speech.googleapis.com/v2/projects/{PROJECT_ID}"
           f"/locations/global/recognizers/_:recognize")
    req = urllib.request.Request(
        url, data=body, method="POST",
        headers={"Authorization": f"Bearer {token}",
                 "x-goog-user-project": PROJECT_ID,
                 "Content-Type": "application/json"})
    data = _open(req, 180)

    words = []
    for result in data.get("results", []):
        alts = result.get("alternatives") or [{}]
        for w in alts[0].get("words", []):
            # 0 sn'lik ofset JSON'da hic gonderilmiyor (proto varsayilani).
            words.append({
                "word": w["word"],
                "start": float(w.get("startOffset", "0s").rstrip("s")),
                "end": float(w.get("endOffset", "0s").rstrip("s")),
            })
    return words


def _split_points(pcm, chunk_sec=CHUNK_SEC, search_sec=4.0):
    """Hedef sinirlarin +-search_sec cevresindeki EN SESSIZ ani bulur.

    Kelime ortasindan bolmemek icin; ham ortadan bolme denendi ve sinirdaki
    kelimeyi kaybediyordu. Donen degerler BAYT ofsetidir (16-bit -> 2 bayt);
    ornek sayisiyla karistirilirsa parcalar iki kati uzun olur ve API 400
    verir."""
    samples = array.array("h")
    samples.frombytes(pcm)
    total = len(samples)
    if total <= int(chunk_sec * RATE):
        return []

    frame = int(0.02 * RATE)
    energy = [sum(abs(v) for v in samples[i:i + frame]) // frame
              for i in range(0, total - frame, frame)]

    points, target = [], int(chunk_sec * RATE)
    while target < total - int(5 * RATE):
        lo = max(0, (target - int(search_sec * RATE)) // frame)
        hi = min(len(energy), (target + int(search_sec * RATE)) // frame)
        best = min(range(lo, hi), key=lambda j: energy[j])
        cut = best * frame
        if points and cut <= points[-1]:
            break
        points.append(cut)
        target = cut + int(chunk_sec * RATE)
    return [c * 2 for c in points]  # ornek -> bayt


def transcribe_one(path, token):
    with wave.open(path, "rb") as wf:
        pcm = wf.readframes(wf.getnframes())

    cuts = [0] + _split_points(pcm) + [len(pcm) // 2 * 2]
    words = []
    for a, b in zip(cuts, cuts[1:]):
        offset = a / 2 / RATE
        for w in _recognize(pcm[a:b], token):
            w["start"] += offset
            w["end"] += offset
            words.append(w)
    return words


if __name__ == "__main__":
    audio_dir, out_dir = sys.argv[1], sys.argv[2]
    start = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    end = int(sys.argv[4]) if len(sys.argv) > 4 else 8
    os.makedirs(out_dir, exist_ok=True)

    for i in range(start, end + 1):
        for attempt in range(3):
            try:
                token = access_token("speech_token.json")
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
