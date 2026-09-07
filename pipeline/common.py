"""Ortak yardımcılar: kimlik bilgileri, OAuth token yenileme, yollar.

Kimlik bilgileri ASLA repoda tutulmaz. Bu modül onları
`$PIPELINE_CREDS` (varsayılan: <scratchpad>/gcloud_creds) altında arar:

    desktop_client_id.txt       OAuth Desktop istemci kimliği
    desktop_client_secret.txt   OAuth Desktop istemci sırrı
    youtube_token.json          YouTube refresh token (kanal başına)
    oauth_token_full.json       Drive/Sheets refresh token
    gemini_api_key.txt          Gemini API anahtarı

Konteyner sıfırlanırsa: bu dosyaları yeniden oluşturmak yeterli,
kodun tamamı repoda durur. Kurulum için bkz. pipeline/README.md
"""
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request

CREDS = os.environ.get(
    "PIPELINE_CREDS",
    "/tmp/claude-0/-home-user-AI-video-creation/"
    "7cf1db21-c849-5360-ab3c-cb73ab4434ba/scratchpad/gcloud_creds",
)
WORK = os.environ.get(
    "PIPELINE_WORK",
    "/tmp/claude-0/-home-user-AI-video-creation/"
    "7cf1db21-c849-5360-ab3c-cb73ab4434ba/scratchpad",
)

PROJECT_ID = "gen-lang-client-0486434271"
SHEET_ID = "1LaEweSHZb4L_Y-AhnuRxiz7o7qSONKsxYSXhdWTBLBo"
DRIVE_PARENT = "1X2emDeckCcXm6LWDqFG5bj-uvZLZv9kT"  # "AI Videos" klasörü
US_LOCATION = {"latitude": 39.8283, "longitude": -98.5795}


def _read(name):
    with open(os.path.join(CREDS, name), encoding="utf-8") as fh:
        return fh.read().strip()


def gemini_key():
    return _read("gemini_api_key.txt")


def access_token(token_file):
    """Refresh token dosyasından taze bir access token üretir."""
    refresh = json.load(open(os.path.join(CREDS, token_file)))["refresh_token"]
    body = urllib.parse.urlencode({
        "grant_type": "refresh_token",
        "refresh_token": refresh,
        "client_id": _read("desktop_client_id.txt"),
        "client_secret": _read("desktop_client_secret.txt"),
    }).encode()
    req = urllib.request.Request(
        "https://oauth2.googleapis.com/token", data=body, method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())["access_token"]


def vertex_generate(model, body, location="global", timeout=180):
    """Vertex AI üzerinden generateContent çağırır ve parts listesini döndürür.

    Neden Vertex: API anahtarıyla çağrılan generativelanguage.googleapis.com
    AI Studio'nun *prepay* bakiyesinden düşüyor; Cloud projesindeki kredi ona
    uygulanmıyor ve bakiye bitince her istek 429 "prepayment credits are
    depleted" veriyor (7 Eylül 2026'da üretim bu yüzden durdu). Vertex aynı
    modelleri Cloud faturasından işliyor, yani projedeki kredi geçerli.

    Kimlik: speech_token.json (cloud-platform kapsamı) — Speech-to-Text ile
    aynı yetki, ek bir onay gerekmiyor.
    """
    host = ("aiplatform.googleapis.com" if location == "global"
            else f"{location}-aiplatform.googleapis.com")
    url = (f"https://{host}/v1/projects/{PROJECT_ID}/locations/{location}"
           f"/publishers/google/models/{model}:generateContent")
    req = urllib.request.Request(
        url, data=json.dumps(body).encode(), method="POST",
        headers={"Authorization": f"Bearer {access_token('speech_token.json')}",
                 "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read())
    return data["candidates"][0]["content"]["parts"]


def youtube_token(channel="youtube_token.json"):
    return access_token(channel)


def drive_token():
    return access_token("oauth_token_full.json")


def consent_url(scopes):
    """Yetki sıfırlandığında kullanıcıya verilecek onay linki."""
    return "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode({
        "client_id": _read("desktop_client_id.txt"),
        "redirect_uri": "http://localhost",
        "response_type": "code",
        "scope": " ".join(scopes),
        "access_type": "offline",
        "prompt": "consent",
    })


def exchange_code(code, out_file):
    """Onay kodunu refresh token'a çevirip kaydeder."""
    body = urllib.parse.urlencode({
        "code": code,
        "client_id": _read("desktop_client_id.txt"),
        "client_secret": _read("desktop_client_secret.txt"),
        "redirect_uri": "http://localhost",
        "grant_type": "authorization_code",
    }).encode()
    req = urllib.request.Request(
        "https://oauth2.googleapis.com/token", data=body, method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read())
    with open(os.path.join(CREDS, out_file), "w") as fh:
        json.dump(data, fh)
    return data


def request_json(url, token, data=None, method="GET", timeout=60, retries=3):
    """Ağ kopmalarına dayanıklı JSON isteği (STT ve upload'larda gerekli)."""
    last = None
    for attempt in range(retries):
        try:
            headers = {"Authorization": f"Bearer {token}"}
            if data is not None:
                headers["Content-Type"] = "application/json"
            req = urllib.request.Request(
                url, data=json.dumps(data).encode() if data is not None else None,
                method=method, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read()
            return json.loads(raw) if raw else {}
        except (urllib.error.URLError, OSError, json.JSONDecodeError) as exc:
            last = exc
            time.sleep(5 * (attempt + 1))
    raise last
