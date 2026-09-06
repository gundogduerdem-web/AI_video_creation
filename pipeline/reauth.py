"""OAuth token yenileme yardimcisi (4 token, haftalik ritual).

Consent screen "Testing" modunda oldugu icin Google 7 gunluk refresh token
veriyor; her token haftada bir elle yenilenmek zorunda. Bu script o isi
link uretme + kod bozma + kalan sure takibi olarak tek yerde toplar.

Kullanim:
    python3 reauth.py                  # durum tablosu + gereken linkler
    python3 reauth.py links            # dort linki de bas
    python3 reauth.py diana <url>      # onay sonrasi localhost URL'ini ver
    python3 reauth.py 1 <url>          # sirayla numara da olur

Onay sonrasi tarayici "localhost baglanti reddedildi" hatasi verir; adres
cubugundaki URL'in tamami buraya yapistirilir, code= degeri ayiklanir.

Kalici cozum (yapilmadi, bkz. pipeline/README.md): Drive/Sheets/Speech'i
servis hesabina tasiyip consent screen'i restricted scope'tan kurtarmak.
"""
import json
import os
import sys
import time
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import CREDS, consent_url, exchange_code  # noqa: E402

YOUTUBE = ["https://www.googleapis.com/auth/youtube",
           "https://www.googleapis.com/auth/youtube.upload",
           "https://www.googleapis.com/auth/yt-analytics.readonly"]
DRIVE = ["https://www.googleapis.com/auth/drive"]
CLOUD = ["https://www.googleapis.com/auth/cloud-platform"]

# (ad, token dosyasi, scope'lar, aciklama, onayda secilecek hesap)
TOKENS = [
    ("diana", "youtube_token_diana.json", YOUTUBE,
     "Diana kanali", "Diana: Untold Chapters kanali"),
    ("audrey", "youtube_token.json", YOUTUBE,
     "Audrey kanali", "Audrey Hepburn: Untold Stories kanali"),
    ("drive", "oauth_token_full.json", DRIVE,
     "Drive / Sheets", "ana hesap (marka kanali degil)"),
    ("speech", "speech_token.json", CLOUD,
     "Speech-to-Text", "ana hesap (marka kanali degil)"),
]

WARN_HOURS = 48  # bu esigin altinda kalan token "yakinda doluyor" sayilir


def find(key):
    """Ada ya da 1-tabanli sira numarasina gore token tanimini bulur."""
    if key.isdigit() and 1 <= int(key) <= len(TOKENS):
        return TOKENS[int(key) - 1]
    for entry in TOKENS:
        if entry[0] == key:
            return entry
    sys.exit(f"Bilinmeyen token: {key}. Gecerli: " +
             ", ".join(t[0] for t in TOKENS))


def remaining(token_file):
    """Token'in kalan omru (saat). Dosya yoksa None, sure bilinmiyorsa -1."""
    path = os.path.join(CREDS, token_file)
    if not os.path.exists(path):
        return None
    data = json.load(open(path))
    ttl = data.get("refresh_token_expires_in")
    if ttl is None:
        return -1  # uygulama yayinda; refresh token dolmuyor
    obtained = data.get("obtained_at", os.path.getmtime(path))
    return (obtained + ttl - time.time()) / 3600


def extract_code(raw):
    """Tam localhost URL'inden ya da duz koddan authorization code'u alir."""
    if "code=" in raw:
        query = urllib.parse.urlparse(raw.strip()).query
        codes = urllib.parse.parse_qs(query).get("code")
        if not codes:
            sys.exit("URL'de code= parametresi bulunamadi.")
        return codes[0]
    return raw.strip()


def show_status():
    stale = []
    print(f"{'token':8} {'dosya':28} durum")
    print("-" * 62)
    for name, token_file, _, label, _ in TOKENS:
        left = remaining(token_file)
        if left is None:
            state, need = "YOK - alinmasi gerekiyor", True
        elif left < 0 and left != -1:
            state, need = "DOLMUS - yenile", True
        elif left == -1:
            state, need = "suresiz (uygulama yayinda)", False
        else:
            state = f"{left / 24:.1f} gun kaldi"
            need = left < WARN_HOURS
            if need:
                state += "  <-- yakinda doluyor"
        print(f"{name:8} {token_file:28} {state}   ({label})")
        if need:
            stale.append(name)
    return stale


def show_links(names):
    for name, _, scopes, label, account in TOKENS:
        if names and name not in names:
            continue
        print(f"\n### {name} — {label}")
        print(f"Onay ekraninda sec: {account}")
        print(consent_url(scopes))


def main():
    args = sys.argv[1:]
    if not args:
        stale = show_status()
        if stale:
            print("\nYenilenmesi gerekenler icin linkler:")
            show_links(stale)
            print("\nHer link icin: onayla -> localhost hatasindaki URL'i kopyala ->")
            print("  python3 reauth.py <ad> '<url>'")
        else:
            print("\nHepsi taze, yapilacak bir sey yok.")
        return
    if args[0] == "links":
        show_links(args[1:])
        return
    if args[0] == "status":
        show_status()
        return
    name, token_file, _, label, _ = find(args[0])
    if len(args) < 2:
        sys.exit(f"Kullanim: python3 reauth.py {name} '<localhost URL veya code>'")
    data = exchange_code(extract_code(args[1]), token_file)
    ttl = data.get("refresh_token_expires_in")
    age = "suresiz" if ttl is None else f"{ttl / 86400:.1f} gun"
    print(f"{label} -> {token_file} yazildi (gecerlilik: {age})")


if __name__ == "__main__":
    main()
