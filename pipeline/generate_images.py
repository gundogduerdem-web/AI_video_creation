"""Vertex AI ile sahne görselleri üretir (sıralı, senkron).

Fatura notu: API anahtarıyla çağrılan Batch API artık kullanılmıyor;
gerekçe common.py içindeki vertex_generate'te yazılı. submit/collect
eski batch yolunu koruyor ama varsayılan akış render() üzerinden gider.

Kullanım:
    python3 generate_images.py <prompts.json> <cikti_dizini> [--retry sahne,sahne]
                               [--vertical | --aspect 9:16]

Varsayilan en-boy orani 16:9'dur. Shorts kapak gorseli icin --vertical
VERILMEZSE prompt'ta "vertical 9:16 composition" yazsa bile API 16:9
dondurur; V15'e kadar butun dikey kapaklar bu yuzden yataydi.

prompts.json biçimi:
    {"1": "sahne 1 prompt", "2": "...", ...}

Öğrenilmiş kurallar (CONTENT_STRATEGY.md'de de kayıtlı):
  * Yasaklı sembolleri OLUMSUZ biçimde bile anma ("no swastikas" yazmak
    IMAGE_SAFETY engeline yol açtı, 8 görselden 6'sı reddedildi).
  * Düşman/asker figürleri milliyet belirtmeden, yüzü görünmeyen /
    uzak / silüet olarak tanımlanır.
  * "bombed buildings" gibi savaş hasarı ifadeleri de engellenebiliyor;
    nötr karşılıklar kullan ("a street still under repair").
  * aspect_ratio mutlaka verilir, yoksa kare (1024x1024) döner.
"""
import base64
import json
import os
import sys
import time
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import gemini_key, vertex_generate  # noqa: E402

MODEL = "gemini-2.5-flash-image"


def render(prompts, out_dir, aspect="16:9", retries=3):
    """Prompt'ları Vertex üzerinden tek tek üretir; (kaydedilen, engellenen).

    Batch yerine sıradan çağrılar: Vertex'in toplu işi girdi/çıktı için GCS
    ya da BigQuery istiyor, video başına 8 görsel için bu zahmete değmez.
    Sıralı çalışınca 8 görsel yaklaşık 2-3 dakika sürüyor — eski batch
    yolundan (10-30 dk) belirgin biçimde hızlı.
    """
    os.makedirs(out_dir, exist_ok=True)
    saved, blocked, failed = [], [], []
    for k, prompt in sorted(prompts.items(), key=lambda kv: int(kv[0])):
        name = f"scene_{k}"
        body = {"contents": [{"role": "user", "parts": [{"text": prompt}]}],
                "generationConfig": {"imageConfig": {"aspectRatio": aspect}}}
        for attempt in range(retries):
            try:
                parts = vertex_generate(MODEL, body, timeout=180)
                data = next((p["inlineData"]["data"] for p in parts if "inlineData" in p), None)
                if data is None:
                    # Metin dondu, gorsel yok: IMAGE_SAFETY engeli.
                    blocked.append((name, "".join(p.get("text", "") for p in parts)[:120]))
                else:
                    with open(os.path.join(out_dir, f"{name}.png"), "wb") as fh:
                        fh.write(base64.b64decode(data))
                    saved.append(name)
                    print(f"  {name} OK", flush=True)
                break
            except Exception as exc:
                if attempt == retries - 1:
                    # API hatasi engel DEGILDIR; ayri raporlanir, cunku
                    # "prompt'u notrlestir" tavsiyesi 429'da yanlis yon
                    # gosteriyor (8 Eyl'de bir kez buna harcandi).
                    failed.append((name, str(exc)[:120]))
                    break
                # 429 bu modelde sik; 5-10 sn beklemek yetmiyordu ve
                # V19'da 8 gorselin 3'u ilk turda dustu. Daha uzun bekle.
                time.sleep(20 * (attempt + 1) if "429" in str(exc)
                           else 5 * (attempt + 1))
    return saved, blocked, failed


def submit(prompts, display_name, aspect="16:9"):
    key = gemini_key()
    reqs = [{
        "request": {
            "contents": [{"parts": [{"text": p}]}],
            "generation_config": {"image_config": {"aspect_ratio": aspect}},
        },
        "metadata": {"key": f"scene_{k}"},
    } for k, p in sorted(prompts.items(), key=lambda kv: int(kv[0]))]

    body = json.dumps({"batch": {
        "display_name": display_name,
        "input_config": {"requests": {"requests": reqs}},
    }}).encode()
    url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
           f"{MODEL}:batchGenerateContent?key={key}")
    try:
        req = urllib.request.Request(
            url, data=body, headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=180) as resp:
            return json.loads(resp.read())["name"]
    except Exception:
        # Istek timeout gorunse bile is olusmus olabilir - listeden bul.
        time.sleep(5)
        listing = urllib.request.Request(
            f"https://generativelanguage.googleapis.com/v1beta/batches?key={key}&pageSize=10")
        with urllib.request.urlopen(listing, timeout=60) as resp:
            for b in json.loads(resp.read()).get("operations", []):
                if b.get("metadata", {}).get("displayName") == display_name:
                    return b["name"]
        raise


def collect(op, out_dir, poll=20, limit=80):
    key = gemini_key()
    os.makedirs(out_dir, exist_ok=True)
    for _ in range(limit):
        time.sleep(poll)
        req = urllib.request.Request(
            f"https://generativelanguage.googleapis.com/v1beta/{op}?key={key}")
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read())
        state = data["metadata"]["state"]
        print("state:", state, flush=True)
        if state == "BATCH_STATE_SUCCEEDED":
            saved, blocked = [], []
            for item in data["response"]["inlinedResponses"]["inlinedResponses"]:
                name = item["metadata"]["key"]
                cand = (item.get("response", {}).get("candidates") or [{}])[0]
                if "content" not in cand:
                    blocked.append((name, cand.get("finishReason")))
                    continue
                for part in cand["content"].get("parts", []):
                    if "inlineData" in part:
                        with open(os.path.join(out_dir, f"{name}.png"), "wb") as fh:
                            fh.write(base64.b64decode(part["inlineData"]["data"]))
                        saved.append(name)
                        break
            return saved, blocked
        if state in ("BATCH_STATE_FAILED", "BATCH_STATE_CANCELLED", "BATCH_STATE_EXPIRED"):
            raise RuntimeError(f"batch {state}")
    raise TimeoutError("batch zaman asimi")


if __name__ == "__main__":
    prompts = json.load(open(sys.argv[1], encoding="utf-8"))
    out_dir = sys.argv[2]
    if "--retry" in sys.argv:
        wanted = sys.argv[sys.argv.index("--retry") + 1].split(",")
        prompts = {k: v for k, v in prompts.items() if k in wanted}
    aspect = ("9:16" if "--vertical" in sys.argv else
              sys.argv[sys.argv.index("--aspect") + 1] if "--aspect" in sys.argv
              else "16:9")
    saved, blocked, failed = render(prompts, out_dir, aspect)
    print("BASARILI:", saved)
    if blocked:
        print("ENGELLI (IMAGE_SAFETY):", blocked)
        print("-> prompt'u notrlestirip --retry ile tekrar calistir")
    if failed:
        print("HATA (API):", failed)
        print("-> prompt sorunu degil; --retry ile aynen tekrar dene "
              "(429 genelde es zamanli is fazlaligindan, tek basina calisir)")
