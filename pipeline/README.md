# Üretim Pipeline'ı

Bu dizin, kanal videolarının uçtan uca üretim zincirini içerir. **Kod repoda,
kimlik bilgileri dışarıda.** Çalışma ortamı (container) sıfırlandığında yalnızca
kimlik bilgilerini yeniden oluşturmak yeterlidir; script'leri baştan yazmak
gerekmez.

> Bu dosya 28 Ağustos 2026'da, geçici çalışma alanının silinmesi ve tüm
> pipeline'ın kaybolması üzerine yazıldı. Aynı şeyin tekrarlanmaması için var.

## Kurulum (sıfırlama sonrası)

Kimlik bilgileri `$PIPELINE_CREDS` altında tutulur (varsayılan:
`<scratchpad>/gcloud_creds`). Gereken dosyalar:

| Dosya | İçerik |
|---|---|
| `desktop_client_id.txt` | OAuth Desktop istemci kimliği |
| `desktop_client_secret.txt` | OAuth Desktop istemci sırrı |
| `gemini_api_key.txt` | Gemini API anahtarı (artık üretimde kullanılmıyor — bkz. "Görsel ve ses Cloud'a taşındı") |
| `youtube_token.json` | YouTube refresh token (Audrey kanalı) |
| `youtube_token_<kanal>.json` | Diğer kanalların YouTube token'ı (`--channel <kanal>` ile seçilir) |
| `oauth_token_full.json` | Drive/Sheets refresh token |
| `speech_token.json` | Speech-to-Text refresh token (**cloud-platform** kapsamı) |

**Erdem'in Drive'ında** OAuth istemcisinin JSON yedeği duruyor — client id ve
secret oradan alınır (Google secret'ı yalnızca oluşturma anında gösterir).

Token'ları yenilemek için:

```python
from common import consent_url, exchange_code
print(consent_url([
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/yt-analytics.readonly"]))
# linki Erdem açar, "localhost" hatasındaki code= değerini verir:
exchange_code("4/0A...", "youtube_token.json")
```

Drive için aynı akış, tek kapsam: `https://www.googleapis.com/auth/drive`
(bu kapsam Sheets API'sine de yetiyor).

⚠️ YouTube onayında **doğru kanal** seçilmeli — marka kanalları hesap
seçiciyle ayrı satır olarak çıkar. Token'ın gerçekten hangi kanala
bağlandığını doğrulamak için:

```bash
python3 publish.py whoami --channel diana
```

Bu komut kanal adını, ID'sini ve `longUploadsStatus` alanını yazar.
`allowed` = kanal telefonla doğrulanmış (özel thumbnail ve 15 dk üstü
video açık); `eligible` = henüz doğrulanmamış.

## 💳 Görsel ve ses Cloud'a taşındı (6 Eylül 2026)

Görsel üretimi ve seslendirme, AI Studio ucundan (`generativelanguage`,
API anahtarı) **Google Cloud** uçlarına taşındı:

| | Önce | Sonra |
|---|---|---|
| Görsel | Gemini Batch API (%50 indirim) | **Vertex AI** `gemini-2.5-flash-image`, senkron |
| Ses | Gemini TTS, ses adı `Algieba` | **Cloud TTS** `en-US-Chirp3-HD-Algieba` |
| Kimlik | `gemini_api_key.txt` | `speech_token.json` (cloud-platform kapsamı) |

**Sebep:** AI Studio'nun ön ödemeli bakiyesi ile projedeki Google Cloud
kredisi **ayrı kasalar**. Ön ödemeli bakiye boşaldığında her iki servis de
`429 RESOURCE_EXHAUSTED: prepayment credits are depleted` veriyor, ama
projede kullanılmayı bekleyen Cloud kredisi duruyordu. Cloud uçları o
krediden ödeniyor.

Kanal sesi değişmedi — Chirp3-HD sesleri Gemini TTS'tekilerin aynısı
(Enceladus, Algieba). Batch API'nin %50 indirimi kayboldu: Vertex'te batch
GCS giriş/çıkış zorunlu kılıyor, 8 görsel için karmaşıklığa değmiyor.

**Projede açık olması gereken API'ler:** `aiplatform.googleapis.com`,
`texttospeech.googleapis.com`, `speech.googleapis.com`. Kapalıysa hata
"credits depleted" değil, "API has not been used in project ... or it is
disabled" olur — karıştırma.

Vertex tarafında dakikalık istek sınırı var; `generate_images.py` 429
alınca 10 sn bekleyip 3 kez deniyor, ısrarlı başarısızlıkta `--retry N`
ile tek sahne yeniden üretilir.

## 🖼️ Thumbnail

```bash
python3 build_thumbnail.py <taban.png> <cikti.jpg> "Princess Diana" "merak metni" left
```

Renkli yakın plan kare + isim (beyaz, üstte) + merak metni (altın #E8B923,
altta), Anton font, siyah kontur. Son argüman metnin hangi yarıya
yaslanacağı — yüzün olduğu tarafa yazma.

Gereken: `pip install Pillow` ve Anton fontu. Font yolu `ANTON_FONT`
ortam değişkeniyle verilir; kurulumda
`https://raw.githubusercontent.com/google/fonts/main/ofl/anton/Anton-Regular.ttf`
adresinden indirilir.

## ⏳ Token'lar 7 günde doluyor (6 Eylül 2026'da tespit edildi)

Google, OAuth consent screen'i **"Testing"** modunda olan projelere
**7 günlük** refresh token veriyor — token yanıtındaki
`refresh_token_expires_in: 604799` bunun göstergesi. Dört token da
(iki YouTube kanalı + Drive/Sheets + Speech) haftada bir düşüyor ve elle
yeniden onay gerektiriyor. Bu, container sıfırlamasından ayrı bir
sorundur; "kimlik bilgileri yine gitmiş" durumunun asıl sebebi çoğunlukla
budur.

**Haftalık yenileme:**

```bash
python3 reauth.py                      # kalan süreleri yazar + gereken linkleri basar
python3 reauth.py diana '<localhost URL>'   # onay sonrası URL'i olduğu gibi ver
```

`reauth.py` linkleri üretir, hangi onay ekranında hangi hesabın
seçileceğini söyler, `code=` değerini URL'den kendisi ayıklar ve doğru
token dosyasına yazar.

**Kalıcı çözüm (henüz yapılmadı, Erdem 7 günlük ile devam etme kararı
verdi):** Consent screen'i "In production" yapmak sorunu bitirir, ama
`auth/drive` **restricted** bir kapsam olduğu için Google CASA güvenlik
değerlendirmesi istiyor (ücretli, yıllık). Bunu aşmanın yolu Drive/Sheets
ve Speech-to-Text'i **servis hesabına** taşımak: servis hesabının consent
screen'i ve süre sınırı yoktur, geriye yalnızca iki YouTube token'ı kalır
ve projede restricted kapsam kalmadığı için publish sorunsuz geçer.
Gereken: servis hesabı JSON anahtarı + "AI Videos" klasörünün ve senaryo
sheet'inin o hesapla paylaşılması.

## Akış

```bash
# 1) Görseller (Vertex AI, senkron)
python3 generate_images.py prompts.json $WORK/imgs

# 2) Seslendirme (senkron; Audrey=Enceladus, Diana=Algieba)
python3 generate_tts.py script.txt $WORK/audio Enceladus

# 3) Kelime zamanlaması (gerçek forced alignment)
python3 transcribe.py $WORK/audio $WORK/timings

# 4) Derleme: 8 görsel -> 24 kadraj -> altyazı -> tek dosya
./build_video.sh isim script.txt $WORK/imgs $WORK/audio $WORK/timings

# 5) Shorts (önce kesim noktalarını listeler, sonra seçileni verirsin)
python3 build_short.py isim s1.txt timings/scene_1.json audio/scene_1.wav dikey.png
python3 build_short.py isim s1.txt timings/scene_1.json audio/scene_1.wav dikey.png 50.6

# 6) Senaryo tablosu (Drive'daki AI video scenario sheet)
python3 sheet.py "Audrey Hepburn"          # son satırları göster
# kod içinden: from sheet import append_row, update_cell

# 7) Yayın
python3 publish.py upload isim.mp4 seo.json thumb.jpg
python3 publish.py drive isim.mp4          # kalite kontrol kopyası
python3 publish.py schedule <video_id> 2026-08-28T19:00:00Z
python3 publish.py status                  # zamanlamaları doğrula
```

`$WORK` = `$PIPELINE_WORK` (varsayılan scratchpad).

## Üretimde öğrenilen kurallar

Bunlar deneyerek bulundu; tekrar tökezlememek için buradalar. Format
kararlarının gerekçesi `../CONTENT_STRATEGY.md` içinde.

**Görsel güvenlik filtresi.** Yasaklı sembolleri olumsuz biçimde bile anma —
"no swastikas, no political symbols" ifadesi `IMAGE_SAFETY` engeline yol açtı
(8 görselden 6'sı reddedildi). Düşman/asker figürleri milliyet belirtmeden,
yüzü görünmeyen/uzak/silüet tanımlanır. "bombed buildings" gibi savaş hasarı
ifadeleri de engellenebiliyor.

**Aspect ratio.** `generationConfig.imageConfig.aspectRatio` verilmezse kare
(1024×1024) döner; 16:9 istemek için açıkça belirtilmeli.

**Batch timeout yanıltıcı.** İstek timeout görünse bile iş oluşmuş olabilir —
`generate_images.py` bu durumda batch listesinden işi bulup devam eder.

**Speech-to-Text.** API anahtarı desteklemiyor, OAuth şart ve token
**cloud-platform** kapsamlı olmalı — Drive kapsamı yetmiyor
(`403 ACCESS_TOKEN_SCOPE_INSUFFICIENT`). Ayrı `speech_token.json` tutulur.
**v2 API kullanılıyor:** v1'in `longrunningrecognize` ucu 30 Ağustos 2026'da
saatlerce `500 An error occurred while checking permissions` /
`503 Policy checks are unavailable` verdi; aynı kimlikle v2 sorunsuz çalıştı
(üstelik senkron, operation beklemiyor). v2'de alan adları `startOffset` /
`endOffset` ve **0 saniyelik ofset JSON'da hiç gönderilmiyor** — `.get(...,
"0s")` şart. Inline ses ~60 sn ile sınırlı; sahneler 55 sn'lik parçalara
bölünüyor ve kesim noktası enerji taraması ile **en sessiz ana** kaydırılıyor
(ortadan bölmek sınırdaki kelimeyi kaybediyordu). Bölme noktaları **bayt**
ofsetidir; örnek sayısıyla karıştırılırsa parçalar iki kat uzun olur ve API
400 verir.

**Süre hedefi ölçümle doğrulanır.** Anlatım hızı **~18,4 karakter/saniye**
(ölçüldü). 12-13 dakika için sahne başına **1690-1749** karakter gerekir;
eski 1450-1499 aralığı ~11 dakika veriyordu. TTS bitince `TOPLAM` satırındaki
süre kontrol edilir.

**Shorts kaynak görseli.** Yatay sahne görselinin dikey kırpımı ana karakteri
kadraj dışında bırakabiliyor; Shorts için natif 9:16 üretilen thumbnail
görseli kullanılır. Kesim noktası doğal bir cümle sonu olmalı.

**Shorts kapağı 9:16 kalır.** YouTube kapakları 16:9 tuvale oturttuğu için
dikey kapak bazı yüzeylerde yanlarda boşlukla görünebilir; Erdem mevcut halini
inceleyip onayladı (28 Ağu 2026). Shorts kapakları dikey üretilmeye devam eder.

**Thumbnail.** Üretilen kare çoğu zaman fazla geniş oluyor; kanal kuralı
(renkli, yakın plan, tek kare) için ffmpeg ile yüz merkezli kırpılıyor.
Yeni kanallarda telefon doğrulaması yoksa thumbnail yüklenemiyor (403).

**`cd` + arka plan.** `cd X && cmd &` tüm zinciri alt kabuğa alır; sonraki
komut eski dizinde çalışır. Script'ler bu yüzden mutlak yol kullanır.
