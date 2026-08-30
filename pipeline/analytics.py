"""YouTube Analytics API v2 sorgulari (kanal teshisi icin).

Kullanim:
    python3 analytics.py sources <video_id> [gun]     # trafik kaynagi kirilimi
    python3 analytics.py daily <video_id> [gun]       # gunluk izlenme
    python3 analytics.py retention <video_id>         # tutunma egrisi
    python3 analytics.py channel [gun]                # kanal geneli gunluk
    python3 analytics.py top [gun]                    # videoya gore ozet

NOT: Gosterim (impressions) ve CTR **API'de yok** — yalnizca Studio arayuzunde.
Bu yuzden "kac kisiye gosterildi" sorusu API'den cevaplanamaz; en yakin vekil
trafik kaynagi kirilimidir (browse/suggested payi dusukse dagitim yok demektir).

Kimlik: youtube_token.json (yt-analytics.readonly kapsami sart).
"""
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import youtube_token  # noqa: E402

BASE = "https://youtubeanalytics.googleapis.com/v2/reports"


def query(**params):
    params.setdefault("ids", "channel==MINE")
    url = f"{BASE}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(
        url, headers={"Authorization": f"Bearer {youtube_token()}"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read())


def _span(days):
    return (str(date.today() - timedelta(days=days)), str(date.today()))


def show(data, title):
    print(f"\n--- {title} ---")
    cols = [h["name"] for h in data["columnHeaders"]]
    print(" | ".join(cols))
    for row in data.get("rows", []):
        print(" | ".join(str(c) for c in row))
    if not data.get("rows"):
        print("(veri yok)")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "sources":
        vid = sys.argv[2]
        start, end = _span(int(sys.argv[3]) if len(sys.argv) > 3 else 30)
        show(query(startDate=start, endDate=end, metrics="views,estimatedMinutesWatched",
                   dimensions="insightTrafficSourceType", filters=f"video=={vid}",
                   sort="-views"), f"{vid} trafik kaynagi")
    elif cmd == "daily":
        vid = sys.argv[2]
        start, end = _span(int(sys.argv[3]) if len(sys.argv) > 3 else 30)
        show(query(startDate=start, endDate=end, metrics="views,averageViewDuration",
                   dimensions="day", filters=f"video=={vid}"), f"{vid} gunluk")
    elif cmd == "retention":
        vid = sys.argv[2]
        start, end = _span(90)
        show(query(startDate=start, endDate=end, metrics="audienceWatchRatio",
                   dimensions="elapsedVideoTimeRatio", filters=f"video=={vid}"),
             f"{vid} tutunma")
    elif cmd == "channel":
        start, end = _span(int(sys.argv[2]) if len(sys.argv) > 2 else 30)
        show(query(startDate=start, endDate=end,
                   metrics="views,estimatedMinutesWatched,subscribersGained",
                   dimensions="day"), "kanal gunluk")
    elif cmd == "top":
        start, end = _span(int(sys.argv[2]) if len(sys.argv) > 2 else 30)
        show(query(startDate=start, endDate=end,
                   metrics="views,estimatedMinutesWatched,averageViewPercentage,"
                           "subscribersGained",
                   dimensions="video", sort="-views", maxResults=25), "video ozeti")
    else:
        print(__doc__)
