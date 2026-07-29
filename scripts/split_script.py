#!/usr/bin/env python3
"""Ham script metnini en fazla 999 karakterlik sahnelere böler.

Normal akışta sahneler zaten 999 karakter sınırına uyacak şekilde
yazılır; bu araç, elle yazılmış ya da tek parça halinde gelen script'leri
send_video.py'a vermeden önce sahnelere bölmek için kullanılan bir
yedek/yardımcı araçtır.
"""
import argparse
import json
import re
import sys

MAX_SCENE_CHARS = 999
MAX_SCENES = 12


def split_into_scenes(text, max_chars=MAX_SCENE_CHARS, max_scenes=MAX_SCENES):
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    scenes = []
    current = ""

    for sentence in sentences:
        candidate = f"{current} {sentence}".strip() if current else sentence
        if len(candidate) <= max_chars:
            current = candidate
            continue

        if current:
            scenes.append(current)
            current = ""

        while len(sentence) > max_chars:
            scenes.append(sentence[:max_chars])
            sentence = sentence[max_chars:]
        current = sentence

    if current:
        scenes.append(current)

    if len(scenes) > max_scenes:
        raise ValueError(
            f"Script {len(scenes)} sahneye bölündü ama en fazla {max_scenes} sahne olmalı. "
            "Script'i kısalt ya da sahne/karakter sınırını gözden geçir."
        )
    return scenes


def main():
    parser = argparse.ArgumentParser(description="Script metnini sahnelere böler")
    parser.add_argument("input", help="Script metni içeren .txt dosyası ('-' ile stdin)")
    parser.add_argument("--max-chars", type=int, default=MAX_SCENE_CHARS)
    parser.add_argument("--max-scenes", type=int, default=MAX_SCENES)
    args = parser.parse_args()

    text = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    scenes = split_into_scenes(text, args.max_chars, args.max_scenes)

    for i, scene in enumerate(scenes, start=1):
        print(f"--- Sahne {i} ({len(scene)} karakter) ---", file=sys.stderr)
        print(scene, file=sys.stderr)
        print(file=sys.stderr)

    print(json.dumps({"scenes": [{"script": s, "image_prompt": ""} for s in scenes]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
