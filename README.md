# AI Video Creation Pipeline

YouTube kanalı için AI destekli video üretim otomasyonu. Üç aşamalı bir hat:

1. **Script → Google Sheets** *(bu repo, hazır)*: Claude'un yazdığı script en
   fazla 12 sahneye (her biri en fazla 999 karakter) bölünmüş halde, görsel
   üretme promptları, title, description ve tag'lerle birlikte JSON olarak
   make.com webhook'una gönderilir; make.com bunu Google Sheets'e bir satır
   olarak işler.
2. **Görsel + script → Fliki → Drive** *(planlanıyor)*: Drive'daki `eg1`,
   `eg2`, ... klasörlerindeki görseller ile sheet'teki ilgili satırın
   script'leri Fliki'ye gönderilip video üretilecek, çıktı Drive'a
   kaydedilecek.
3. **Publish time → YouTube'a yayın** *(planlanıyor)*: Sheet'te publish time'ı
   gelen videolar otomatik yayınlanacak.

Bu repo şu an sadece 1. aşamayı içeriyor.

## Video JSON şeması

`send_video.py` aşağıdaki yapıda bir JSON dosyası bekler (bkz.
`examples/example_video.json`):

```json
{
  "video_code": "eg1",
  "title": "...",
  "description": "...",
  "tags": ["tag1", "tag2"],
  "publish_time": "",
  "scenes": [
    { "script": "sahne 1 metni (en fazla 999 karakter)", "image_prompt": "görsel üretme prompt'u" }
  ]
}
```

- `video_code`: Drive'daki `eg1`, `eg2`, ... klasör adıyla eşleşir; görselleri
  doğru videoya bağlamak için kullanılır.
- `scenes`: en fazla 12 öğe, her `script` alanı en fazla 999 karakter.
- `tags`: liste ya da virgülle ayrılmış tek string olabilir.

## Kullanım

```bash
# Sadece payload'u görmek için (webhook'a göndermeden)
python3 scripts/send_video.py examples/example_video.json --dry-run

# make.com webhook'una gönder
export MAKE_WEBHOOK_URL="https://hook.eu1.make.com/xxxxxxxx"
python3 scripts/send_video.py examples/example_video.json
```

`send_video.py`, sheet satırına düz (flat) sütunlar olarak yazılabilmesi için
JSON'u şu alanlara dönüştürür:

```
video_code, title, description, tags, publish_time,
scene_1..scene_12, prompt_1..prompt_12
```

make.com tarafında **Custom Webhook** → **Google Sheets: Add a Row** modülü bu
alanları ilgili sütunlara eşleyecek şekilde kurulmalı (12 sahneden azı
kullanılırsa kalan `scene_N`/`prompt_N` alanları boş string olarak gönderilir).

## Sahne bölme yardımcı aracı (opsiyonel)

Script zaten sahnelere ayrılmış şekilde yazılıyor olsa da, tek parça gelen bir
script'i 999 karakter sınırına göre otomatik bölmek için:

```bash
python3 scripts/split_script.py my_script.txt > scenes.json
```

Bu, cümle sınırlarını koruyarak sahnelere böler ve `{"scenes": [...]}` formatında
JSON çıktı verir (`image_prompt` alanları boş bırakılır, elle doldurulmalı).

## Sonraki adımlar

- make.com senaryosunda webhook URL'ini oluşturup `MAKE_WEBHOOK_URL` olarak
  paylaş, Google Sheets modülünü yukarıdaki sütun şemasına göre kur.
- Drive klasör yapısı (`eg1`, `eg2`, ...) ve Fliki entegrasyonu netleşince
  2. otomasyon için ayrı bir script eklenecek.
- Publish time bazlı YouTube yayınlama otomasyonu 3. aşamada eklenecek.

## Ambient kanal hattı (cozy jazz / doğa sesleri)

Hikaye kanallarından ayrı, ffmpeg tabanlı ikinci bir hat. Fliki kullanılmaz.
`scripts/build_ambience.py`, kısa müzik parçalarını + bir ortam sesi yatağını +
kısa bir görsel döngüyü alıp saatlerce süren tek bir mp4 üretir.

```bash
python3 scripts/build_ambience.py \
    --music-dir music/winter_cabin \
    --bed audio/fireplace.wav --bed-gain -18 \
    --loop-video visuals/cabin_loop.mp4 \
    --duration 3h \
    --out out/winter_cabin_3h.mp4 \
    --chapters out/winter_cabin_chapters.txt
```

Yaptığı işler sırayla: her parçayı `loudnorm` ile aynı seviyeye getirir
(-20 LUFS — ambient içerikte YouTube'un -14 hedefinden daha sessiz kalmak
tercih edilir), parçaları 6 saniyelik `acrossfade` ile birleştirir, miksi hedef
süreye kadar döndürür, ortam sesini altına kesintisiz döşer ve görsel döngüyü
yeniden kodlamadan (`-c:v copy`) sesle birleştirir. `--chapters` verilirse
YouTube bölüm listesini de yazar.

Notlar:

- **Ortam sesi yatağı (`--bed`) önemli.** Şömine çatırtısı ya da rüzgar,
  parçaların altında kesintisiz akınca video bir çalma listesi gibi değil tek
  bir mekân gibi duyuluyor. Parça geçişlerini de gizler.
- **Yeterli parça üretin.** Miks hedef süreden kısaysa döngü noktasında sert
  bir kesme duyulur (`-stream_loop` crossfade yapmaz). 3 saatlik video için
  ~35-40 parça üretip miksi hedefe yaklaştırmak en temizi.
- **`--loop-video` asıl kullanım, `--still` yedektir.** Sabit görsel hem
  izleyici için monoton hem de YouTube'un "inauthentic content" politikası
  açısından riskli; kar, ateş, buhar gibi hareketli katmanlar taşıyan kısa bir
  döngü tercih edilmeli.
- `--dry-run` çalıştırmadan üretilecek ffmpeg komutlarını yazdırır.
- ffmpeg ve ffprobe PATH üzerinde olmalı.
