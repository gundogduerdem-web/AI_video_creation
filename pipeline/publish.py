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
        "status": {"privacyStatus": "private", "selfDeclaredMadeForKids": False},
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


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "upload":
        upload(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else None)
    elif cmd == "schedule":
        schedule(sys.argv[2], sys.argv[3])
    elif cmd == "drive":
        drive_upload(sys.argv[2])
    elif cmd == "status":
        status()
    else:
        print(__doc__)
