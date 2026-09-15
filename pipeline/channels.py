"""Kanal kaydi: her kanalin sheet sekmesi, YouTube token dosyasi ve sesi.

Kanal eklemek KOD isi degil, veri isidir: `channels.json`'a bir giris yazilir.
Tek kanal varsayimi pipeline'in her yerinden kalkti; kanal ya `--channel`
bayragiyla ya `PIPELINE_CHANNEL` ortam degiskeniyle verilir, hicbiri yoksa
`audrey` kullanilir (mevcut davranis korunuyor).

Kullanim:
    python3 channels.py              # kanallari ve kurulum durumunu listele
    python3 channels.py <slug>       # tek kanalin kaydini yazdir

Kod icinden:
    from channels import resolve, all_channels
    ch = resolve("diana")            # dict; slug alani da icinde
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REGISTRY = os.path.join(HERE, "channels.json")
DEFAULT = "audrey"

# channels.json'da bulunmasi gereken alanlar; eksigi olan kayit sessizce
# yanlis kanala yazmasin diye yuklenirken hata verir.
REQUIRED = ("name", "sheet_tab", "youtube_token", "ready")


def all_channels():
    with open(REGISTRY, encoding="utf-8") as fh:
        data = json.load(fh)
    for slug, ch in data.items():
        missing = [f for f in REQUIRED if f not in ch]
        if missing:
            raise ValueError(f"channels.json: '{slug}' kaydinda eksik alan: {missing}")
        ch["slug"] = slug
    return data


def resolve(slug=None):
    """Slug -> kanal kaydi. Slug verilmezse PIPELINE_CHANNEL, o da yoksa DEFAULT."""
    chans = all_channels()
    slug = slug or os.environ.get("PIPELINE_CHANNEL") or DEFAULT
    if slug not in chans:
        raise SystemExit(
            f"bilinmeyen kanal: '{slug}'. Tanimli olanlar: {', '.join(sorted(chans))}")
    return chans[slug]


def take_channel_arg(argv):
    """argv icinden --channel <slug> (ya da --channel=<slug>) cikarir.

    Mevcut script'lerin konumsal argumanlarini bozmamak icin bayrak
    argv'den silinir ve geri kalan liste aynen dondurulur.
    """
    out, slug = [], None
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--channel" and i + 1 < len(argv):
            slug = argv[i + 1]
            i += 2
            continue
        if a.startswith("--channel="):
            slug = a.split("=", 1)[1]
            i += 1
            continue
        out.append(a)
        i += 1
    return out, slug


def require_ready(ch):
    """Kurulumu bitmemis kanala yayin yapilmasini engeller.

    Neden: dogrulanmamis bir YouTube kanalinda ozel thumbnail yuklenemiyor
    (403) ve 15 dakikayi asan video kabul edilmiyor. Thumbnail CTR
    omurgasi oldugu icin strateji karari, dogrulama bitene kadar o kanalda
    YAYIN YAPILMAMASI (uretim yapilabilir). Bkz. CONTENT_STRATEGY.md.
    """
    if not ch.get("ready"):
        raise SystemExit(
            f"'{ch['slug']}' kanali henuz kurulu degil: {ch.get('notes', '')}\n"
            f"Gereken: kanal olusturulmus + OAuth onayi ({ch['youtube_token']}) "
            f"+ telefon dogrulamasi. Uretim yapilabilir, yayin yapilamaz.")


def _creds_dir():
    from common import CREDS
    return CREDS


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(json.dumps(resolve(sys.argv[1]), ensure_ascii=False, indent=1))
        raise SystemExit
    creds = _creds_dir()
    print(f"{'slug':10s} {'kanal':22s} {'ses':11s} {'token':28s} durum")
    for slug, ch in sorted(all_channels().items()):
        has = os.path.exists(os.path.join(creds, ch["youtube_token"]))
        state = "hazir" if ch["ready"] and has else (
            "token yok" if ch["ready"] else "kurulum bekliyor")
        print(f"{slug:10s} {ch['name']:22s} {str(ch['voice']):11s} "
              f"{ch['youtube_token']:28s} {state}")
