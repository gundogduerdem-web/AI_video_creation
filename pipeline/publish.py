"""YouTube'a private yükleme, thumbnail, zamanlama ve Drive QC kopyası.

Kullanım:
    # video + thumbnail yükle (private, zamanlamasız)
    python3 publish.py upload <video.mp4> <seo.json> <thumb.jpg>

    # yayın zamanı ata (TR saatini UTC'ye çevirerek ver: TR = UTC+3)
    python3 publish.py schedule <video_id> 2026-08-28T19:00:00Z

    # Drive'a kalite kontrol kopyası
    python3 publish.py drive <dosya.mp4>

    # kanaldaki private/zamanlı videoları listele
    python3 publish.py status

    # token hangi kanala ait, telefon doğrulaması geçmiş mi?
    python3 publish.py whoami

Çoklu kanal: her komut sona eklenen `--channel <ad>` ile başka bir kanala
yönlendirilir; token dosyası `youtube_token_<ad>.json` olur. Bayrak yoksa
Audrey kanalının `youtube_token.json` dosyası kullanılır.

    python3 publish.py whoami --channel diana
    python3 publish.py upload video.mp4 seo.json thumb.jpg --channel diana

seo.json:  {"title": ..., "description": ..., "tags": [...]}

Kanal standardı (CONTENT_STRATEGY.md): dil en-US, konum ABD,
çocuklar için değil, kategori 27 (Education).
HİÇBİR video Erdem'in açık onayı olmadan public/scheduled yapılmaz.
"""
import json
import os
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DRIVE_PARENT, US_LOCATION, drive_token, youtube_token  # noqa: E402


def upload(video, seo_path, thumb=None, token_file="youtube_token.json"):
    token = youtube_token(token_file)
    seo = json.load(open(seo_path, encoding="utf-8"))
    size = os.path.getsize(video)
    meta = {
        "snippet": {
            "title": seo["title"],
            "description": seo["description"],
            "tags": seo["tags"],
            "categoryId": "27",
            "defaultLanguage": "en-US",
            "defaultAudioLanguage": "en-US",
        },
        # containsSyntheticMedia: YouTube'un "altered or synthetic content"
        # beyani. Gercek bir kisiyi ve gercek gorunumlu sahneleri yapay
        # goruntu + yapay sesle canlandirdigimiz icin ZORUNLU; aciklamadaki
        # kurgu ibaresi kaldirilinca tek beyan bu kaliyor.
        "status": {"privacyStatus": "private", "selfDeclaredMadeForKids": False,
                   "containsSyntheticMedia": True},
        "recordingDetails": {"location": US_LOCATION},
    }
    init = urllib.request.Request(
        "https://www.googleapis.com/upload/youtube/v3/videos"
        "?uploadType=resumable&part=snippet,status,recordingDetails",
        data=json.dumps(meta).encode(), method="POST",
        headers={"Authorization": f"Bearer {token}",
                 "Content-Type": "application/json; charset=UTF-8",
                 "X-Upload-Content-Type": "video/mp4",
                 "X-Upload-Content-Length": str(size)})
    with urllib.request.urlopen(init, timeout=30) as resp:
        url = resp.headers.get("Location")
    put = urllib.request.Request(
        url, data=open(video, "rb").read(), method="PUT",
        headers={"Content-Type": "video/mp4", "Content-Length": str(size)})
    with urllib.request.urlopen(put, timeout=1800) as resp:
        vid = json.loads(resp.read())["id"]
    print(f"YOUTUBE (private): https://youtube.com/watch?v={vid}")

    if thumb:
        # Not: kanal telefon dogrulamasi yoksa burasi 403 verir.
        req = urllib.request.Request(
            f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={vid}",
            data=open(thumb, "rb").read(), method="POST",
            headers={"Authorization": f"Bearer {token}", "Content-Type": "image/jpeg"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            resp.read()
        print("Thumbnail: OK")
    return vid


def schedule(vid, publish_at, token_file="youtube_token.json"):
    token = youtube_token(token_file)
    body = json.dumps({"id": vid, "status": {
        "privacyStatus": "private", "publishAt": publish_at,
        "selfDeclaredMadeForKids": False}}).encode()
    req = urllib.request.Request(
        "https://www.googleapis.com/youtube/v3/videos?part=status",
        data=body, method="PUT",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        status = json.loads(resp.read())["status"]
    print(f"{vid} -> publishAt {status.get('publishAt')}")


def drive_upload(path, name=None):
    token = drive_token()
    name = name or os.path.basename(path)
    size = os.path.getsize(path)
    meta = json.dumps({"name": name, "parents": [DRIVE_PARENT]}).encode()
    init = urllib.request.Request(
        "https://www.googleapis.com/upload/drive/v3/files?uploadType=resumable",
        data=meta, method="POST",
        headers={"Authorization": f"Bearer {token}",
                 "Content-Type": "application/json; charset=UTF-8",
                 "X-Upload-Content-Type": "video/mp4",
                 "X-Upload-Content-Length": str(size)})
    with urllib.request.urlopen(init, timeout=30) as resp:
        url = resp.headers.get("Location")
    put = urllib.request.Request(
        url, data=open(path, "rb").read(), method="PUT",
        headers={"Content-Type": "video/mp4", "Content-Length": str(size)})
    with urllib.request.urlopen(put, timeout=1800) as resp:
        fid = json.loads(resp.read())["id"]
    link = f"https://drive.google.com/file/d/{fid}/view"
    print("DRIVE QC:", link)
    return link


def status(token_file="youtube_token.json"):
    token = youtube_token(token_file)
    req = urllib.request.Request(
        "https://www.googleapis.com/youtube/v3/channels?part=contentDetails&mine=true",
        headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        pl = json.loads(resp.read())["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    ids, page = [], None
    while True:
        url = ("https://www.googleapis.com/youtube/v3/playlistItems"
               f"?part=snippet&playlistId={pl}&maxResults=50")
        if page:
            url += f"&pageToken={page}"
        with urllib.request.urlopen(urllib.request.Request(
                url, headers={"Authorization": f"Bearer {token}"}), timeout=30) as resp:
            data = json.loads(resp.read())
        ids += [i["snippet"]["resourceId"]["videoId"] for i in data["items"]]
        page = data.get("nextPageToken")
        if not page:
            break
    for i in range(0, len(ids), 50):
        url = ("https://www.googleapis.com/youtube/v3/videos"
               f"?part=snippet,status&id={','.join(ids[i:i + 50])}")
        with urllib.request.urlopen(urllib.request.Request(
                url, headers={"Authorization": f"Bearer {token}"}), timeout=30) as resp:
            for v in json.loads(resp.read())["items"]:
                st = v["status"]
                if st["privacyStatus"] == "private":
                    print(f"  {v['id']} | publishAt={st.get('publishAt', 'YOK')} "
                          f"| {v['snippet']['title'][:55]}")


def token_file_for(channel):
    """Kanal adını token dosyasına çevirir (Audrey varsayılan kanaldır)."""
    if channel is None or channel == "audrey":
        return "youtube_token.json"
    return f"youtube_token_{channel}.json"


def whoami(token_file="youtube_token.json"):
    """Token'ın hangi kanala ait olduğunu ve doğrulama durumunu yazar.

    longUploadsStatus, telefon doğrulamasının programatik göstergesidir:
    "allowed" = doğrulanmış, "eligible" = doğrulanabilir ama henüz değil.
    """
    token = youtube_token(token_file)
    req = urllib.request.Request(
        "https://www.googleapis.com/youtube/v3/channels"
        "?part=snippet,status&mine=true",
        headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        ch = json.loads(resp.read())["items"][0]
    long_uploads = ch["status"].get("longUploadsStatus", "bilinmiyor")
    print(f"Kanal:   {ch['snippet']['title']}")
    print(f"ID:      {ch['id']}")
    print(f"Token:   {token_file}")
    print(f"Doğrulama (longUploadsStatus): {long_uploads}"
          + ("  -> doğrulanmış" if long_uploads == "allowed"
             else "  -> DOĞRULANMAMIŞ, özel thumbnail yüklenemez"))
    return ch


def _pop_channel(argv):
    """argv'den `--channel <ad>` bayrağını ayıklayıp kanal adını döndürür."""
    if "--channel" not in argv:
        return None
    i = argv.index("--channel")
    if i + 1 >= len(argv):
        sys.exit("--channel bayrağı bir kanal adı bekliyor (örn. --channel diana)")
    channel = argv[i + 1]
    del argv[i:i + 2]
    return channel


if __name__ == "__main__":
    argv = sys.argv[1:]
    token = token_file_for(_pop_channel(argv))
    cmd = argv[0] if argv else None
    if cmd == "upload":
        upload(argv[1], argv[2], argv[3] if len(argv) > 3 else None, token_file=token)
    elif cmd == "schedule":
        schedule(argv[1], argv[2], token_file=token)
    elif cmd == "drive":
        drive_upload(argv[1])
    elif cmd == "status":
        status(token)
    elif cmd == "whoami":
        whoami(token)
    else:
        print(__doc__)
