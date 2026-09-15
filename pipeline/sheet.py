"""Drive'daki "AI video scenario sheet" tablosunu okur/yazar.

Her kanalin kendi sekmesi var (sekme adi = kisi adi). Sutunlar:
    A No | B Baslik | C Baslik alternatifleri | D Konu/Konsept | E Hook
    F Senaryo | G Sahne dogrulamasi | H Tekrar-kontrol | I Durum
    J YouTube linki | K Drive QC linki | L Yayin zamani (TR)
    M Thumbnail konsepti | N Etiketler | O Erdem onayi
    P 24s/7g izlenme-CTR | Q Not

Sekme adi yerine kanal slug'i da verilebilir ("diana" -> "Princess Diana");
bkz. channels.json.

Kullanim:
    python3 sheet.py show "Audrey Hepburn" [satir_sayisi]
    python3 sheet.py show diana

Kod icinden:
    from sheet import append_row, read_rows, update_cell, tab_for
"""
import json
import sys
import os
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import SHEET_ID, drive_token  # noqa: E402
from channels import all_channels  # noqa: E402

BASE = f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}"
COLS = ["No", "Baslik", "Baslik alternatifleri", "Konu", "Hook", "Senaryo",
        "Sahne dogrulamasi", "Tekrar-kontrol", "Durum", "YouTube", "Drive QC",
        "Yayin zamani", "Thumbnail", "Etiketler", "Onay", "Izlenme", "Not"]

# Kolon harfi <-> indeks; update_cell cagrilarinda harf elle yazilmasin diye.
COL_LETTER = {name: chr(ord("A") + i) for i, name in enumerate(COLS)}


def tab_for(name):
    """Kanal slug'ini sekme adina cevirir; sekme adi verildiyse aynen dondurur."""
    chans = all_channels()
    if name in chans:
        return chans[name]["sheet_tab"]
    return name


def _req(url, data=None, method="GET"):
    headers = {"Authorization": f"Bearer {drive_token()}",
               "Content-Type": "application/json"}
    req = urllib.request.Request(
        url, data=json.dumps(data).encode() if data else None,
        method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read())


def read_rows(tab, first=1, last=200):
    tab = tab_for(tab)
    rng = urllib.parse.quote(f"'{tab}'!A{first}:Q{last}")
    return _req(f"{BASE}/values/{rng}").get("values", [])


def append_row(tab, row):
    """Tabloya tek satir ekler; eksik sutunlar bos birakilir."""
    tab = tab_for(tab)
    row = list(row) + [""] * (len(COLS) - len(row))
    rng = urllib.parse.quote(f"'{tab}'!A1")
    url = (f"{BASE}/values/{rng}:append"
           "?valueInputOption=RAW&insertDataOption=INSERT_ROWS")
    return _req(url, {"values": [row[:len(COLS)]]}, method="POST")


def update_cell(tab, cell, value):
    """Ornek: update_cell("Audrey Hepburn", "I14", "Yayinda").

    tab yerine kanal slug'i da verilebilir: update_cell("diana", "I14", ...).
    """
    tab = tab_for(tab)
    rng = urllib.parse.quote(f"'{tab}'!{cell}")
    return _req(f"{BASE}/values/{rng}?valueInputOption=RAW",
                {"values": [[value]]}, method="PUT")


if __name__ == "__main__":
    tab = sys.argv[1] if len(sys.argv) > 1 else "Audrey Hepburn"
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    for i, row in enumerate(read_rows(tab, 1, n), 1):
        print(i, [c[:35] for c in row])
