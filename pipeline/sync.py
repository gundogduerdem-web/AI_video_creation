"""Sheet'i yayin takviminin KAYNAGI yapar: L kolonundaki saati YouTube'a isler.

Neden gerekli: yayin iki yerde yaziliyor — YouTube'un `publishAt` alani ve
sheet'in "Yayin zamani" kolonu. Bu ikisi sessizce ayrisabiliyor; 13 Eylul
2026'da bir video sheet'te "Yayinda" yazarken YouTube'da private +
publishAt=yarin duruyordu. Bu komut iki tarafi karsilastirir ve farki
raporlar; --apply ile sheet'teki saati YouTube'a yazar.

Yayini YouTube yapar: publishAt saati geldiginde video kendi kendine public
olur, yani bu script'in ya da konteynerin o an ayakta olmasi gerekmez.
Buradaki is, saatin gercekten islenmis oldugunu garanti etmek.

ONAY KAPISI KORUNUR: bir satira saat islenmesi icin O ("Onay") kolonunda
onay yazmasi sart. Onaysiz satir asla zamanlanmaz, --apply verilse bile.

Kullanim:
    python3 sync.py [--channel <slug>]            # karsilastir, yazma
    python3 sync.py --apply [--channel <slug>]    # sheet -> YouTube
    python3 sync.py --fix-status                  # public olanlarin Durum'unu duzelt
    python3 sync.py --all                         # tum kurulu kanallar

Sheet'e yazilan kanonik saat formati (ikisi de okunur):
    2026-09-16 00:00 (Carsamba gecesi) = 2026-09-15 21:00 UTC
    2026-09-16 00:00        <- saat dilimi yazilmazsa TR (UTC+3) sayilir
"""
import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from channels import all_channels, resolve, take_channel_arg  # noqa: E402
from common import youtube_token  # noqa: E402
from publish import schedule  # noqa: E402
from sheet import COLS, read_rows, update_cell  # noqa: E402

I_STATUS = COLS.index("Durum")
I_YT = COLS.index("YouTube")
I_WHEN = COLS.index("Yayin zamani")
I_OK = COLS.index("Onay")

TR = timezone(timedelta(hours=3))
UTC_RE = re.compile(r"(\d{4})-(\d{2})-(\d{2})[ T](\d{2}):(\d{2})\s*(?:UTC|Z)")
ANY_RE = re.compile(r"(\d{4})-(\d{2})-(\d{2})[ T](\d{2}):(\d{2})")
ID_RE = re.compile(r"(?:watch\?v=|shorts/|youtu\.be/)([A-Za-z0-9_-]{11})")


def parse_when(text):
    """Sheet hucresinden UTC datetime cikarir; okunamazsa None.

    Once acik UTC damgasi aranir ("= 2026-09-15 21:00 UTC"), cunku hucrede
    hem TR hem UTC yazili oluyor ve dogru olan UTC. Yoksa ilk tarih TR
    kabul edilip UTC'ye cevrilir.
    """
    if not text:
        return None
    m = UTC_RE.search(text)
    if m:
        y, mo, d, h, mi = (int(x) for x in m.groups())
        return datetime(y, mo, d, h, mi, tzinfo=timezone.utc)
    m = ANY_RE.search(text)
    if m:
        y, mo, d, h, mi = (int(x) for x in m.groups())
        return datetime(y, mo, d, h, mi, tzinfo=TR).astimezone(timezone.utc)
    return None


def approved(text):
    """O kolonu onay iceriyor mu. 'Onay bekliyor' onay DEGILDIR."""
    t = (text or "").lower()
    return t.startswith("onayl") and "bekliyor" not in t


def video_states(ids, token_file):
    out = {}
    token = youtube_token(token_file)
    for i in range(0, len(ids), 50):
        url = ("https://www.googleapis.com/youtube/v3/videos"
               f"?part=status&id={','.join(ids[i:i + 50])}")
        with urllib.request.urlopen(urllib.request.Request(
                url, headers={"Authorization": f"Bearer {token}"}), timeout=30) as resp:
            for v in json.loads(resp.read())["items"]:
                out[v["id"]] = v["status"]
    return out


def _is_published_text(text):
    t = (text or "").lower()
    return "yayında" in t or "yayinda" in t


def sync(ch, apply=False, fix_status=False, now=None):
    now = now or datetime.now(timezone.utc)
    tab = ch["sheet_tab"]
    rows = read_rows(tab, 1, 400)
    plan = []
    for n, row in enumerate(rows, 1):
        row = list(row) + [""] * (len(COLS) - len(row))
        m = ID_RE.search(row[I_YT] or "")
        if not m:
            continue
        plan.append({"row": n, "vid": m.group(1), "no": row[0],
                     "title": (row[1] or "")[:42],
                     "want": parse_when(row[I_WHEN]),
                     "ok": approved(row[I_OK]),
                     "sheet_status": row[I_STATUS]})
    if not plan:
        print(f"[{ch['slug']}] sheet'te YouTube linki olan satir yok")
        return []
    states = video_states([p["vid"] for p in plan], ch["youtube_token"])

    acted = []
    print(f"[{ch['slug']}] {len(plan)} satir, {len(states)} video bulundu")
    for p in plan:
        st = states.get(p["vid"])
        if st is None:
            print(f"  satir {p['row']:>3} {p['no']:>4} | {p['vid']} | "
                  f"BU KANALDA YOK (yanlis kanal ya da silinmis)")
            continue
        priv = st["privacyStatus"]
        has = st.get("publishAt")
        cur = datetime.fromisoformat(has.replace("Z", "+00:00")) if has else None
        want = p["want"]

        if priv == "public":
            verdict = "yayinda"
            if not _is_published_text(p["sheet_status"]):
                verdict = "yayinda — sheet'te 'Yayında' yazmiyor"
                if fix_status:
                    update_cell(ch["sheet_tab"],
                                f"{chr(ord('A') + I_STATUS)}{p['row']}", "Yayında")
                    verdict += " -> duzeltildi"
        elif want is None:
            verdict = "sheet'te saat yok/okunamadi"
        elif cur == want:
            verdict = "eslesiyor"
        elif not p["ok"]:
            verdict = f"ONAY YOK — {want:%Y-%m-%d %H:%M}Z islenmedi"
        elif cur is None and want <= now:
            verdict = f"KACIRILMIS — saat {want:%Y-%m-%d %H:%M}Z gecti, hala private"
        else:
            verdict = f"FARKLI — youtube={has or 'YOK'} sheet={want:%Y-%m-%d %H:%M}Z"
            if apply:
                schedule(p["vid"], want.strftime("%Y-%m-%dT%H:%M:%SZ"),
                         ch["youtube_token"])
                acted.append(p["vid"])
                verdict += " -> islendi"
        print(f"  satir {p['row']:>3} {p['no']:>4} | {p['vid']} | "
              f"{priv:7s} | {p['title']:42s} | {verdict}")
    return acted


if __name__ == "__main__":
    argv, slug = take_channel_arg(sys.argv[1:])
    apply = "--apply" in argv
    fix = "--fix-status" in argv
    if "--all" in argv:
        targets = [c for c in all_channels().values() if c["ready"]]
    else:
        targets = [resolve(slug)]
    for ch in targets:
        if not ch["ready"]:
            print(f"[{ch['slug']}] kurulum bekliyor, atlandi")
            continue
        sync(ch, apply=apply, fix_status=fix)
