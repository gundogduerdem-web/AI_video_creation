#!/usr/bin/env python3
"""Ambient (cozy jazz / doga sesi) kanali icin uzun video uretir.

Girdi: bir klasor dolusu kisa muzik parcasi (Gemini/Lyria, Suno vb.),
opsiyonel bir ortam sesi yatagi (somine catirtisi, ruzgar, yagmur) ve
kisa/kusursuz donen bir gorsel dongu (video ya da sabit gorsel).

Cikti: hedef sureye (orn. 3 saat) uzatilmis tek bir mp4 + YouTube
bolum (chapter) listesi.

Akis:
  1. Her parca ayri ayri ses seviyesine gore normalize edilir (loudnorm).
  2. Parcalar acrossfade ile ust uste bindirilerek tek miks yapilir.
  3. Miks hedef sureye kadar dondurulur.
  4. Ortam sesi yatagi altina dusuk seviyede, kesintisiz dosenir.
  5. Gorsel dongu ayni sureye kadar dondurulup sesle birlestirilir.

Ornek:
  python3 scripts/build_ambience.py \\
      --music-dir music/winter_cabin \\
      --bed audio/fireplace.wav --bed-gain -18 \\
      --loop-video visuals/cabin_loop.mp4 \\
      --duration 3h \\
      --out out/winter_cabin_3h.mp4 \\
      --chapters out/winter_cabin_chapters.txt

ffmpeg ve ffprobe PATH uzerinde olmali.
"""
import argparse
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile

AUDIO_EXTS = (".mp3", ".wav", ".m4a", ".flac", ".aac", ".ogg", ".opus")

# Ambient icerikte YouTube'un -14 LUFS hedefinden daha sessiz kalmak
# tercih edilir; uyku/calisma izleyicisi ani seviye degisimine duyarli.
LOUDNORM = "loudnorm=I=-20:TP=-2:LRA=11"
SAMPLE_RATE = 48000

# YouTube bolum kurallari: en az 3 bolum, ilki 0:00, her biri >= 10 sn.
MIN_CHAPTERS = 3
MIN_CHAPTER_SECONDS = 10


def parse_duration(text):
    """'3h', '90m', '45s', '1:30:00' ya da saniye sayisini saniyeye cevirir."""
    text = text.strip().lower()
    if re.fullmatch(r"\d+(\.\d+)?", text):
        return float(text)

    if ":" in text:
        parts = [float(p) for p in text.split(":")]
        if len(parts) > 3:
            raise ValueError(f"gecersiz sure: {text}")
        seconds = 0.0
        for part in parts:
            seconds = seconds * 60 + part
        return seconds

    match = re.fullmatch(r"(?:(\d+(?:\.\d+)?)h)?(?:(\d+(?:\.\d+)?)m)?(?:(\d+(?:\.\d+)?)s)?", text)
    if not match or not any(match.groups()):
        raise ValueError(f"gecersiz sure: {text}")
    hours, minutes, seconds = (float(g) if g else 0.0 for g in match.groups())
    return hours * 3600 + minutes * 60 + seconds


def format_timestamp(seconds):
    seconds = int(seconds)
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def run(cmd, dry_run):
    if dry_run:
        print(" ".join(shlex_quote(part) for part in cmd))
        return
    subprocess.run(cmd, check=True)


def shlex_quote(value):
    if re.fullmatch(r"[A-Za-z0-9_@%+=:,./-]+", value):
        return value
    return "'" + value.replace("'", "'\\''") + "'"


def probe_duration(path):
    result = subprocess.run(
        [
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "json", path,
        ],
        check=True, capture_output=True, text=True,
    )
    return float(json.loads(result.stdout)["format"]["duration"])


def collect_tracks(music_dir, shuffle, seed):
    if not os.path.isdir(music_dir):
        raise SystemExit(f"Hata: muzik klasoru yok: {music_dir}")

    tracks = sorted(
        os.path.join(music_dir, name)
        for name in os.listdir(music_dir)
        if name.lower().endswith(AUDIO_EXTS)
    )
    if not tracks:
        raise SystemExit(f"Hata: {music_dir} icinde ses dosyasi bulunamadi")

    if shuffle:
        random.Random(seed).shuffle(tracks)
    return tracks


def normalize_tracks(tracks, work_dir, dry_run):
    """Her parcayi ayni seviye/format'a getirir; acrossfade bunu gerektirir."""
    normalized = []
    for index, track in enumerate(tracks):
        target = os.path.join(work_dir, f"norm_{index:03d}.wav")
        run(
            [
                "ffmpeg", "-y", "-v", "error", "-i", track,
                "-af", LOUDNORM,
                "-ar", str(SAMPLE_RATE), "-ac", "2", "-c:a", "pcm_s16le",
                target,
            ],
            dry_run,
        )
        normalized.append(target)
    return normalized


def build_crossfade_filter(count, crossfade):
    """acrossfade zinciri: [0][1] -> [a1], [a1][2] -> [a2], ..."""
    if count == 1:
        return None, "0:a"

    steps = []
    previous = "[0:a]"
    for index in range(1, count):
        label = f"[a{index}]"
        steps.append(
            f"{previous}[{index}:a]acrossfade=d={crossfade}:c1=tri:c2=tri{label}"
        )
        previous = label
    return ";".join(steps), previous.strip("[]")


def concat_with_crossfade(normalized, crossfade, work_dir, dry_run):
    target = os.path.join(work_dir, "mix.wav")
    filter_complex, out_label = build_crossfade_filter(len(normalized), crossfade)

    cmd = ["ffmpeg", "-y", "-v", "error"]
    for path in normalized:
        cmd += ["-i", path]
    if filter_complex:
        cmd += ["-filter_complex", filter_complex, "-map", f"[{out_label}]"]
    else:
        cmd += ["-map", out_label]
    cmd += ["-ar", str(SAMPLE_RATE), "-ac", "2", "-c:a", "pcm_s16le", target]

    run(cmd, dry_run)
    return target


def build_audio(mix_path, bed, bed_gain, duration, work_dir, audio_bitrate, dry_run):
    """Miksi hedef sureye dondurur ve varsa ortam sesi yatagini altina serer."""
    target = os.path.join(work_dir, "audio.m4a")

    cmd = ["ffmpeg", "-y", "-v", "error", "-stream_loop", "-1", "-i", mix_path]
    if bed:
        cmd += ["-stream_loop", "-1", "-i", bed]
        # normalize=0: amix'in girdi sayisina gore sesi kismasini engeller,
        # boylece muzik seviyesi korunur ve yatak gercekten "altta" kalir.
        cmd += [
            "-filter_complex",
            f"[1:a]volume={bed_gain}dB,aresample={SAMPLE_RATE}[bed];"
            f"[0:a][bed]amix=inputs=2:duration=first:normalize=0[out]",
            "-map", "[out]",
        ]
    else:
        cmd += ["-map", "0:a"]

    cmd += [
        "-t", f"{duration:.3f}",
        "-ar", str(SAMPLE_RATE), "-ac", "2",
        "-c:a", "aac", "-b:a", audio_bitrate,
        target,
    ]
    run(cmd, dry_run)
    return target


def mux(video_source, still, audio_path, duration, out_path, reencode_video, still_fps, dry_run):
    out_dir = os.path.dirname(os.path.abspath(out_path))
    if out_dir and not dry_run:
        os.makedirs(out_dir, exist_ok=True)

    cmd = ["ffmpeg", "-y", "-v", "error"]
    if still:
        cmd += ["-loop", "1", "-framerate", str(still_fps), "-i", still]
        video_args = [
            "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p",
            "-r", str(still_fps), "-g", str(still_fps * 10), "-crf", "20",
        ]
    else:
        cmd += ["-stream_loop", "-1", "-i", video_source]
        if reencode_video:
            video_args = ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "veryfast"]
        else:
            # Dongu videosu tek basina dogru kodlanmissa yeniden kodlamaya
            # gerek yok; 3 saatlik 4K encode'dan kacinmak icin varsayilan bu.
            video_args = ["-c:v", "copy"]

    cmd += ["-i", audio_path]
    cmd += ["-map", "0:v:0", "-map", "1:a:0"]
    cmd += video_args
    cmd += ["-c:a", "copy", "-t", f"{duration:.3f}", "-movflags", "+faststart", "-shortest", out_path]
    run(cmd, dry_run)


def build_chapters(tracks, durations, crossfade, total_duration):
    """Parca baslangiclarini YouTube bolum listesine cevirir.

    Crossfade parcalari ust uste bindirdigi icin her parca, kendinden
    onceki her gecis kadar one kayar. Miks hedef sureden kisaysa dongu
    boyunca tekrar eder.
    """
    cycle = sum(durations) - crossfade * (len(durations) - 1)
    if cycle <= 0:
        return []

    lines = []
    offset = 0.0
    while offset < total_duration:
        position = 0.0
        for index, (track, length) in enumerate(zip(tracks, durations)):
            start = offset + position
            if start >= total_duration:
                break
            title = os.path.splitext(os.path.basename(track))[0].replace("_", " ").strip()
            lines.append((start, title or f"Track {index + 1}"))
            position += length - (crossfade if index < len(durations) - 1 else 0)
        offset += cycle

    # Cok kisa araliklar YouTube tarafindan reddedilir; birlestirip atlariz.
    filtered = []
    for start, title in lines:
        if filtered and start - filtered[-1][0] < MIN_CHAPTER_SECONDS:
            continue
        filtered.append((start, title))

    if len(filtered) < MIN_CHAPTERS:
        return []

    filtered[0] = (0.0, filtered[0][1])
    return [f"{format_timestamp(start)} {title}" for start, title in filtered]


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--music-dir", required=True, help="Kisa muzik parcalarinin bulundugu klasor")
    parser.add_argument("--duration", required=True, help="Hedef sure: 3h, 90m, 1:30:00 ya da saniye")
    parser.add_argument("--out", required=True, help="Cikti mp4 yolu")

    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--loop-video", help="Kusursuz donen kisa video (asil kullanim)")
    source.add_argument("--still", help="Sabit gorsel (yedek; dongu videosu yoksa)")

    parser.add_argument("--bed", help="Altta kesintisiz calacak ortam sesi (somine, ruzgar, yagmur)")
    parser.add_argument("--bed-gain", type=float, default=-18.0, help="Ortam sesi seviyesi, dB (varsayilan: -18)")
    parser.add_argument("--crossfade", type=float, default=6.0, help="Parca gecis suresi, saniye (varsayilan: 6)")
    parser.add_argument("--chapters", help="YouTube bolum listesinin yazilacagi dosya")
    parser.add_argument("--shuffle", action="store_true", help="Parca sirasini karistir")
    parser.add_argument("--seed", type=int, default=0, help="Karistirma tohumu (tekrarlanabilirlik icin)")
    parser.add_argument("--audio-bitrate", default="256k", help="AAC bitrate (varsayilan: 256k)")
    parser.add_argument("--still-fps", type=int, default=5, help="Sabit gorsel modunda kare hizi (varsayilan: 5)")
    parser.add_argument("--reencode-video", action="store_true", help="Dongu videosunu kopyalamak yerine yeniden kodla")
    parser.add_argument("--keep-temp", action="store_true", help="Ara dosyalari silme (hata ayiklama)")
    parser.add_argument("--dry-run", action="store_true", help="Calistirmadan ffmpeg komutlarini yazdir")
    args = parser.parse_args()

    if not args.dry_run:
        for binary in ("ffmpeg", "ffprobe"):
            if not shutil.which(binary):
                raise SystemExit(f"Hata: {binary} PATH uzerinde bulunamadi")

    duration = parse_duration(args.duration)
    tracks = collect_tracks(args.music_dir, args.shuffle, args.seed)

    if args.bed and not os.path.isfile(args.bed):
        raise SystemExit(f"Hata: ortam sesi dosyasi yok: {args.bed}")
    visual = args.loop_video or args.still
    if not args.dry_run and not os.path.isfile(visual):
        raise SystemExit(f"Hata: gorsel dosyasi yok: {visual}")

    print(f"{len(tracks)} parca bulundu, hedef sure {format_timestamp(duration)}", file=sys.stderr)

    work_dir = tempfile.mkdtemp(prefix="ambience_")
    try:
        normalized = normalize_tracks(tracks, work_dir, args.dry_run)
        mix_path = concat_with_crossfade(normalized, args.crossfade, work_dir, args.dry_run)
        audio_path = build_audio(
            mix_path, args.bed, args.bed_gain, duration, work_dir, args.audio_bitrate, args.dry_run
        )
        mux(
            args.loop_video, args.still, audio_path, duration, args.out,
            args.reencode_video, args.still_fps, args.dry_run,
        )

        if args.chapters:
            durations = [8 * 60.0] * len(tracks) if args.dry_run else [probe_duration(t) for t in tracks]
            lines = build_chapters(tracks, durations, args.crossfade, duration)
            if not lines:
                print("Uyari: bolum listesi olusturulamadi (yeterli bolum yok)", file=sys.stderr)
            elif args.dry_run:
                print("\n# chapters (dry-run, parca sureleri tahmini)\n" + "\n".join(lines[:5]) + "\n...")
            else:
                with open(args.chapters, "w", encoding="utf-8") as f:
                    f.write("\n".join(lines) + "\n")
                print(f"{len(lines)} bolum yazildi: {args.chapters}", file=sys.stderr)

        if not args.dry_run:
            print(f"Tamam: {args.out}", file=sys.stderr)
    finally:
        if args.keep_temp:
            print(f"Ara dosyalar: {work_dir}", file=sys.stderr)
        else:
            shutil.rmtree(work_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
