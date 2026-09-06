"""Vertex AI ile sahne görselleri üretir.

Kullanım:
    python3 generate_images.py <prompts.json> <cikti_dizini> [--retry sahne,sahne]

prompts.json biçimi:
    {"1": "sahne 1 prompt", "2": "...", ...}

Neden Vertex: AI Studio ucu (generativelanguage + API anahtarı) ayrı bir ön
ödemeli bakiyeden ödeniyor ve o bakiye boştu (RESOURCE_EXHAUSTED). Aynı model
Vertex üzerinden Google Cloud faturasına yazılıyor, yani projedeki Cloud
kredisinden. Batch API'nin %50 indirimi Vertex'te GCS giriş/çıkış zorunlu
olduğu için kullanılmıyor; 8 görsel senkron üretiliyor.

Öğrenilmiş kurallar (CONTENT_STRATEGY.md'de de kayıtlı):
  * Yasaklı sembolleri OLUMSUZ biçimde bile anma ("no swastikas" yazmak
    IMAGE_SAFETY engeline yol açtı, 8 görselden 6'sı reddedildi).
  * Düşman/asker figürleri milliyet belirtmeden, yüzü görünmeyen /
    uzak / silüet olarak tanımlanır.
  * "bombed buildings" gibi savaş hasarı ifadeleri de engellenebiliyor;
    nötr karşılıklar kullan ("a street still under repair").
  * aspectRatio mutlaka verilir, yoksa kare döner. 16:9 -> 1344x768.
"""
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import PROJECT, cloud_token  # noqa: E402

MODEL = "gemini-2.5-flash-image"
LOCATION = "global"


def generate(prompt, out_path, aspect="16:9", retries=4, backoff=30):
    """Tek sahne üretir. Basarili ise True, guvenlik engeli ise sebep doner.

    Vertex'in dakikalik istek siniri, arka arkaya uretimde her basarili
    cagrinin sonrakini 429'a dusurmesine yol acti. Geri cekilme bu yuzden
    dakika penceresini asacak kadar uzun ve artan: 30, 60, 90, 120 sn.
    """
    url = (f"https://aiplatform.googleapis.com/v1/projects/{PROJECT}"
           f"/locations/{LOCATION}/publishers/google/models/{MODEL}:generateContent")
    body = json.dumps({
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {"imageConfig": {"aspectRatio": aspect}},
    }).encode()
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                url, data=body, method="POST",
                headers={"Authorization": f"Bearer {cloud_token()}",
                         "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=300) as resp:
                data = json.loads(resp.read())
            cand = (data.get("candidates") or [{}])[0]
            if "content" not in cand:
                return cand.get("finishReason", "BILINMEYEN")
            for part in cand["content"].get("parts", []):
                if "inlineData" in part:
                    with open(out_path, "wb") as fh:
                        fh.write(base64.b64decode(part["inlineData"]["data"]))
                    return True
            return "GORSEL_YOK"
        except urllib.error.HTTPError as exc:
            wait = backoff * (attempt + 1)
            print(f"  deneme {attempt + 1} basarisiz: {exc.code} "
                  f"{exc.read().decode()[:120]} -> {wait} sn bekleniyor", flush=True)
            time.sleep(wait)
        except Exception as exc:
            wait = backoff * (attempt + 1)
            print(f"  deneme {attempt + 1} basarisiz: {exc} -> {wait} sn", flush=True)
            time.sleep(wait)
    return "AG_HATASI"


if __name__ == "__main__":
    prompts = json.load(open(sys.argv[1], encoding="utf-8"))
    out_dir = sys.argv[2]
    if "--retry" in sys.argv:
        wanted = sys.argv[sys.argv.index("--retry") + 1].split(",")
        prompts = {k: v for k, v in prompts.items() if k in wanted}
    os.makedirs(out_dir, exist_ok=True)

    saved, blocked = [], []
    for n, key in enumerate(sorted(prompts, key=int)):
        if n:
            time.sleep(20)   # dakikalik pencereyi arka arkaya doldurmamak icin
        name = f"scene_{key}"
        result = generate(prompts[key], os.path.join(out_dir, f"{name}.png"))
        if result is True:
            saved.append(name)
            print(f"{name}: OK", flush=True)
        else:
            blocked.append((name, result))
            print(f"{name}: ENGELLI ({result})", flush=True)
    print("\nBASARILI:", saved)
    if blocked:
        print("ENGELLI:", blocked)
        print("-> prompt'u notrlestirip --retry ile tekrar calistir")
