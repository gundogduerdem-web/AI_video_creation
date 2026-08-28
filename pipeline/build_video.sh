#!/bin/bash
# Uzun video derleyici: 8 gorsel -> 24 kadraj -> altyazi -> tek dosya.
#
# Kullanim:
#   ./build_video.sh <is_adi> <script.txt> <gorsel_dizini> <ses_dizini> <timing_dizini>
#
# Neden 3 kadraj: analytics teshisi (25 Agu 2026) izleyicinin yarisinin ilk
# 25 saniyede gittigini gosterdi; tek gorselin ~90 sn ekranda kalmasi gorsel
# monotonluk yaratiyordu. Her gorselden 3 kadraj cikarilinca gorsel basina
# sure ~28 sn'ye iniyor, gorsel maliyeti 8'de kaliyor.
set -e

NAME=$1; SCRIPT=$2; IMG_DIR=$3; AUD_DIR=$4; TIM_DIR=$5
[ -z "$TIM_DIR" ] && { echo "kullanim: $0 <is_adi> <script> <gorsel> <ses> <timing>"; exit 1; }

HERE="$(cd "$(dirname "$0")" && pwd)"
W=${PIPELINE_WORK:-.}
cd "$W"
mkdir -p "${NAME}_segs" "${NAME}_clips" "${NAME}_subs" "${NAME}_final" "${NAME}_texts"

FPS=25
CROP_A="2688:1536:0:0"        # tam kare (genis plan)
CROP_B="2150:1229:269:154"    # %80 merkez (orta plan)
CROP_C="1666:952:511:120"     # %62 ust-merkez (yakin plan; yuzler ust yarida)

python3 - "$SCRIPT" "${NAME}_texts" <<'PY'
import re, sys, os
text = open(sys.argv[1], encoding='utf-8').read()
for n, c in re.findall(r'\[SCENE(\d+)\]\s*\n(.*?)\n\[/SCENE\1\]', text, re.S):
    open(os.path.join(sys.argv[2], f'scene_{n}.txt'), 'w', encoding='utf-8').write(c.strip())
PY

for i in $(seq 1 8); do
  AUD="$AUD_DIR/scene_${i}.wav"
  IMG="$IMG_DIR/scene_${i}.png"
  DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$AUD")
  read T1 T2 T3 <<< $(python3 -c "d=float('$DUR');a=d/3;print(f'{a:.3f} {a:.3f} {d-2*a:.3f}')")

  for v in 1 2 3; do
    case $v in
      1) SEG=$T1; CROP=$CROP_A; Z="min(zoom+0.00009,1.08)";;
      2) SEG=$T2; CROP=$CROP_B; Z="if(lte(zoom,1.0),1.08,max(1.001,zoom-0.00009))";;
      3) SEG=$T3; CROP=$CROP_C; Z="min(zoom+0.00009,1.08)";;
    esac
    FRAMES=$(python3 -c "print(int(float('$SEG') * $FPS) + 5)")
    ffmpeg -y -loop 1 -i "$IMG" -filter_complex \
      "[0:v]scale=2688:1536:flags=lanczos,crop=${CROP},zoompan=z='${Z}':d=${FRAMES}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=${FPS}[v]" \
      -map "[v]" -t "$SEG" -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p \
      "${NAME}_segs/s${i}_v${v}.mp4" -loglevel error
  done

  rm -f "${NAME}_segs/list_${i}.txt"
  for v in 1 2 3; do echo "file 's${i}_v${v}.mp4'" >> "${NAME}_segs/list_${i}.txt"; done
  ffmpeg -y -f concat -safe 0 -i "${NAME}_segs/list_${i}.txt" -c copy \
    "${NAME}_segs/scene_${i}_v.mp4" -loglevel error
  ffmpeg -y -i "${NAME}_segs/scene_${i}_v.mp4" -i "$AUD" -map 0:v -map 1:a \
    -c:v copy -c:a aac -b:a 192k -shortest "${NAME}_clips/scene_${i}.mp4" -loglevel error
  echo "clip $i hazir (3 kadraj, ${DUR}s)"
done

for i in $(seq 1 8); do
  python3 "$HERE/subtitles.py" "$(cat "${NAME}_texts/scene_${i}.txt")" \
    "$TIM_DIR/scene_${i}.json" "${NAME}_subs/scene_${i}.ass"
  ffmpeg -y -i "${NAME}_clips/scene_${i}.mp4" \
    -vf "drawbox=x=0:y=920:w=1920:h=160:color=black@1.0:t=fill,ass=${NAME}_subs/scene_${i}.ass" \
    -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -c:a copy \
    "${NAME}_final/scene_${i}.mp4" -loglevel error
  echo "clip $i altyazili"
done

rm -f "${NAME}_concat.txt"
for i in $(seq 1 8); do echo "file '${NAME}_final/scene_${i}.mp4'" >> "${NAME}_concat.txt"; done
ffmpeg -y -f concat -safe 0 -i "${NAME}_concat.txt" -c copy "${NAME}.mp4" -loglevel error
echo "SON VIDEO: ${NAME}.mp4"
ffprobe -v error -show_entries format=duration -of csv=p=0 "${NAME}.mp4"
