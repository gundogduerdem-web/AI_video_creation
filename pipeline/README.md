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
| `gemini_api_key.txt` | Gemini API anahtarı |
| `youtube_token.json` | YouTube refresh token (Audrey kanalı) |
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
seçiciyle ayrı satır olarak çıkar.

## Akış

```bash
# 1) Görseller (Batch API, %50 indirim)
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

**Süre hedefi ölçümle doğrulanır.** Anlatım hızı sabit değil: ölçülen
aralık **16,7-21,0 karakter/saniye** (içeriğe göre değişiyor). 12-13 dakika
için sahne başına **1690-1749** karakter iyi bir başlangıç, ama karakter
sayısı süreyi garanti etmez — TTS bitince `TOPLAM` satırındaki süre mutlaka
kontrol edilir.

**TTS metni tekrarlayabiliyor.** V9'da model 8. sahnenin metnini baştan sona
iki kez okudu: 1746 karakter için 177 saniye. Sessizce geçse videonun sonunda
aynı paragraf iki kez duyulacaktı. `generate_tts.py` artık her sahnede
karakter/saniye oranını kontrol ediyor (12-26 aralığı dışı hata sayılır) ve
tekrar deniyor. Aynı belirti kesilme durumunda da yakalanır.

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
