#!/usr/bin/env python3
"""Video script JSON'unu make.com webhook'una POST eder.

Girdi: video_code, title, description, tags ve en fazla 12 sahneden
(her biri en fazla 999 karakter script + görsel üretme prompt'u) oluşan
bir JSON dosyası. Örnek için examples/example_video.json dosyasına bak.

make.com tarafında Custom Webhook -> Google Sheets "Add a Row" modülü
aşağıdaki düz (flat) alanları sütunlara eşleyecek şekilde kurulmalı:
  video_code, title, description, tags, publish_time,
  scene_1..scene_12, prompt_1..prompt_12
"""
import argparse
import json
import os
import sys
from urllib import error as urlerror
from urllib import request as urlrequest

MAX_SCENE_CHARS = 999
MAX_SCENES = 12


def load_video(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate(video):
    errors = []
    for field in ("video_code", "title", "description", "tags", "scenes"):
        if field not in video:
            errors.append(f"eksik alan: {field}")
    if errors:
        raise ValueError("\n".join(errors))

    scenes = video["scenes"]
    if len(scenes) > MAX_SCENES:
        errors.append(f"{len(scenes)} sahne var, en fazla {MAX_SCENES} olmalı")

    for i, scene in enumerate(scenes, start=1):
        script = scene.get("script", "")
        if len(script) > MAX_SCENE_CHARS:
            errors.append(
                f"sahne {i}: {len(script)} karakter, limit {MAX_SCENE_CHARS} karakter"
            )
        if not scene.get("image_prompt"):
            errors.append(f"sahne {i}: image_prompt eksik")

    if errors:
        raise ValueError("\n".join(errors))


def flatten(video):
    tags = video["tags"]
    payload = {
        "video_code": video["video_code"],
        "title": video["title"],
        "description": video["description"],
        "tags": ", ".join(tags) if isinstance(tags, list) else tags,
        "publish_time": video.get("publish_time", ""),
    }
    scenes = video["scenes"]
    for i in range(1, MAX_SCENES + 1):
        scene = scenes[i - 1] if i <= len(scenes) else {}
        payload[f"scene_{i}"] = scene.get("script", "")
        payload[f"prompt_{i}"] = scene.get("image_prompt", "")
    return payload


def send(payload, webhook_url):
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urlrequest.Request(
        webhook_url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlrequest.urlopen(req) as resp:
        return resp.status, resp.read().decode("utf-8")


def main():
    parser = argparse.ArgumentParser(
        description="Video script JSON'unu make.com webhook'una gönderir"
    )
    parser.add_argument("video_json", help="Video verisini içeren JSON dosyası")
    parser.add_argument(
        "--webhook-url",
        default=os.environ.get("MAKE_WEBHOOK_URL"),
        help="make.com webhook URL (veya MAKE_WEBHOOK_URL env değişkeni)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Webhook'a göndermeden sadece oluşturulan payload'u yazdır",
    )
    args = parser.parse_args()

    video = load_video(args.video_json)
    validate(video)
    payload = flatten(video)

    if args.dry_run or not args.webhook_url:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        if not args.webhook_url and not args.dry_run:
            print(
                "\nUyarı: --webhook-url verilmedi ya da MAKE_WEBHOOK_URL ayarlanmadı, "
                "sadece payload gösterildi, gönderim yapılmadı.",
                file=sys.stderr,
            )
        return

    try:
        status, body = send(payload, args.webhook_url)
    except urlerror.HTTPError as e:
        print(f"Webhook hatası: HTTP {e.code}\n{e.read().decode('utf-8', 'ignore')}", file=sys.stderr)
        sys.exit(1)
    except urlerror.URLError as e:
        print(f"Webhook'a ulaşılamadı: {e.reason}", file=sys.stderr)
        sys.exit(1)

    print(f"Webhook yanıtı: {status}")
    print(body)


if __name__ == "__main__":
    main()
