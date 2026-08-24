# Kanal Portföyü — İçerik Stratejisi

## ÇOKLU KANAL GENİŞLEMESİ (güncel büyük karar)

Tek kanalın başarı ihtimali düşük olduğu için portföy yaklaşımına geçildi.
**5 kanal:** Audrey Hepburn (mevcut) + Princess Diana + Jacqueline Kennedy +
Louis Armstrong + Kenny Rogers (hepsi Erdem tarafından seçildi/onaylandı).
Seçim kriterleri: vefat etmiş, 65+ ABD kitlesinde çok tanınır, agresif
estate/lisans temsilcisi yok (Elvis, Einstein, James Dean, Sinatra, CMG
temsilcileri — Billie Holiday, Buddy Holly, Hank Williams, Chuck Berry —
ABG temsilcileri — Whitney Houston — ve Ray Charles vakfı elendi).

**Merkezi kayıt:** Drive'daki "AI video scenario sheet"
(ID: 1LaEweSHZb4L_Y-AhnuRxiz7o7qSONKsxYSXhdWTBLBo) — Dashboard + kanal
başına bir sekme. Her video için: başlık (+alternatifler), konu, hook,
tam senaryo, doğrulamalar, tekrar-kontrol notu, durum, YouTube/Drive
linkleri, yayın zamanı, thumbnail konsepti, etiketler, Erdem onayı,
izlenme verisi.

**Yeni karar akışı (Erdem'in talimatı):** Konu + hook + başlığı Claude
en yüksek izlenme potansiyeline göre kendisi seçer, Erdem'e sormaz;
tüm seçimler sheet'e işlenir. Değişmeyen kapılar: final video kalite
kontrolü (Drive QC linki) ve **açık onay olmadan hiçbir video
public/scheduled yapılmaz** (onay sheet'teki "Erdem onayı" kolonuyla
toplu verilebilir).

**Tempo planı:** Lansman fazında kanal başına günde 1 video (algoritma
yer edinme hızlandırması, Erdem'in kararı), kanal başına ilk 3-4 hafta;
sonra haftada 2-3'e inilir. Kanallar 3-4 gün arayla kademeli devreye
alınır (aynı gün toplu açılış "ağ/spam" görünümü riski). Tekrar kontrolü
hem kanal içi hem **kanallar arası** yapılır.

**Operasyonel önkoşullar:** Erdem 4 yeni marka kanalı oluşturur + her
kanal için bir kez OAuth onayı verir (kanal başına ayrı refresh token).

Aşağıdaki bölümler Audrey Hepburn kanalı için yazılmıştır; teknik
standartlar (8 sahne/8 görsel, 1450-1499 kr/sahne, 12-13 dk, Batch API,
zoompan/encode ayarları, YouTube meta, Drive QC akışı) **tüm kanallar
için geçerlidir**.

---

# Audrey Hepburn: Untold Stories — İçerik Stratejisi

> **Bu dosya hakkında:** Bu doküman, Erdem'in ayrı bir Claude.ai projesinde
> (kanal danışmanlığı) birikmiş proje hafızası ile bu repodaki otomasyon
> çalışmasında alınan kararların birleştirilmiş, tek kanonik halidir.
> Kaynaklar arasında **üç noktada bilinçli çelişki/düzeltme/pivot** var,
> hepsi bu repo oturumunda Erdem tarafından açıkça onaylandı:
>
> 1. **Sahne sayısı: 12** (proje hafızasındaki "Exactly 10 sahne" değil).
> 2. **Haftalık kategori kotası/slot sistemi yok** — asker, sporcu, şarkıcı
>    vb. için sabit bir limit uygulanmıyor (proje hafızasındaki "Weekly
>    category rotation" slot sistemi bu repo için geçerli değil).
> 3. **Büyük pivot (güncel karar):** Kanal, çok kişili "hidden moment"
>    belgesel formatından (The Stories History Left Behind) **tek karakter,
>    açıkça kurgusal/dramatize** bir formata geçti — bkz. aşağıdaki
>    "Kanal Kimliği ve Amaç" bölümü. Aşağıdaki "Öncelikli İçerik
>    Kategorileri", "Doygunluk Kontrolü" (çoklu isim seçimi) ve "Backlog"
>    bölümleri **eski format için yazılmıştı, artık aktif olarak
>    kullanılmıyor** — tarihsel referans olarak saklanıyor, silinmedi.
>
> Bunlar dışındaki tüm bilgiler (tamamlanmış prodüksiyonlar, performans
> öğrenmeleri, teknik standartlar, araç zinciri) proje hafızasından olduğu
> gibi aktarılmıştır.

---

## Kanal Kimliği ve Amaç (güncel — pivot sonrası)

**Kanal adı:** Audrey Hepburn: Untold Stories *(eski ad: "The Stories
History Left Behind")*

**Kanal açıklaması:**
"Fictional, dramatized stories inspired by the hidden and untold moments
of Audrey Hepburn's life — many set during World War II, years before the
world knew her name. Each story blends documented history with imagined
detail to explore the emotional truths behind her legend. New stories
every week.

These videos are created using AI-generated visuals and voice, and depict
fictional, dramatized storytelling — not documentary or biographical fact."

Kanal artık **tek bir karakter** üzerine kurulu: **Audrey Hepburn**. İçerik,
çoğunlukla **II. Dünya Savaşı** dönemini (Nazi işgali altındaki Hollanda,
1940-1945) konu alan, **açıkça kurgusal/dramatize edilmiş** hikayelerden
oluşuyor — gerçek biyografik anlatım değil (bkz. yukarıdaki açıklama metni
ve aşağıdaki "İçerik Çerçevesi" bölümü). Hedef kitle İngilizce konuşan 60+
yaş grubu; aktif hedef, bu kitle içindeki **65+ kadın izleyici payını
artırmak**.

İçerik üretim süreci Türkçe yürütülüyor (Claude ile), yayın için İngilizceye
çevriliyor/tamamlanıyor.

**Başarı ölçütleri:** CTR, retention, hedef demografideki büyüme.

### İçerik Çerçevesi (kurgu kuralları)

- İçerik **açıkça kurgu/dramatizasyon olarak sunulur** — başlık/açıklamada
  gizlenmez, video açıklamasının sonunda AI üretimi ve kurgusal olduğu
  açıkça belirtilir (bkz. yukarıdaki kanal açıklaması).
- Gerçek isim/imaj kullanılır (Audrey Hepburn), ama hikaye örgüsü video
  video değişebilir: bazıları gerçek bir olaydan yola çıkıp ağırlıklı kurgu
  içerir (örn. gerçek direniş kuryeliği geçmişi), bazıları tamamen
  kurgusaldır.
- Zaman çizgisi/yaş esnetilebilir: gerçek olaylar Audrey Hepburn'ün genç
  yaşlarında (14-16) geçmiş olsa da, reşit olmayan tasvir kısıtı nedeniyle
  kurgusal versiyonda **yetişkin (20'li yaşlar)** olarak tasvir edilir.
- İkincil karakterler (örn. "Ormandaki Asker"daki yaralı asker) tamamen
  kurgusal/isimsiz olabilir.
- Anlatım tüm hikayelerde 3. şahıs.

---

## Konu Uygunluğu (eski format — artık aktif değil)

> Aşağıdaki bölüm, çok karakterli eski format için yazılmıştı. Kanal artık
> sadece Audrey Hepburn'ü işlediği için bu bölüm aktif olarak kullanılmıyor,
> tarihsel referans olarak saklanıyor.

- Tercihen ~2019 veya öncesinde vefat etmiş figürler.
- 2023 sonrası vefat edenler hariç tutulur ("gizli an" açısı için çok yakın,
  aile/emlak hassasiyeti daha yüksek).
- Konu havuzu **tüm dönemleri kapsar**, belirli bir dekad sınırlaması yok —
  şarkıcı, aktör, aktris, sanatçı, politikacı, First Lady, aktivist, müzik
  ikonu ve ünlüler dahil.
- İçerik her zaman belgelenmiş, doğrulanabilir olaylara dayanır —
  dramatizasyon sadece sahne kurulumu ve makul iç durumlarla sınırlıdır.
- Gerçek kişilere uydurma alıntı atfedilmez. Belgelenmiş söylenti/üçüncü
  şahıs anlatıları, açıkça öyle olduğu belirtilerek kullanılabilir.
- Tüm anlatım 3. şahıs.

---

## Öncelikli İçerik Kategorileri (eski format — artık aktif değil, kota/slot yok)

- Klasik Hollywood / altın çağ aktör ve aktrisleri (evlilik/kayıp temaları) — yüksek öncelik
- Her dönemden TV yıldızları — yüksek öncelik
- Romantik müzik ikonları / şarkıcılar — yüksek öncelik
- First Lady'ler ve politik eşler — yüksek öncelik
- Politikacılar (kişisel dram açısı olanlar) — orta öncelik
- İlişki merkezli asker hikayeleri (hayatta kalanın perspektifi, taktik değil) — orta öncelik
- İstatistik ağırlıklı spor içerikleri / kişisel dram içermeyen saf politika hikayeleri — düşük öncelik

**Not:** Kategoriler arasında sabit bir haftalık kota/slot uygulanmıyor —
hangi kategoriden kaç video üretileceği sabit değil, doygunluk kontrolü ve
elde mevcut iyi açılara göre serbestçe seçiliyor.

**Anahtar prensip:** İlişki/fedakarlık/kırılganlık çerçevesi, ana karakterin
cinsiyetinden veya döneminden daha önemli bir kaldıraçtır — 65+ kadın
segmentinde performansı bu belirliyor.

---

## 🔑 Doygunluk Kontrolü (eski format — artık aktif değil)

> Bu bölüm, çoklu isim havuzundan konu seçimi için yazılmıştı. Kanal artık
> sadece Audrey Hepburn'ü işlediği için (konu seçimi değil, açı/hikaye
> seçimi yapılıyor) aktif olarak kullanılmıyor, tarihsel referans olarak
> saklanıyor.

**Kritik prensip:** Değerlendirme **ismin ne kadar tanınır olduğu değil**,
seçilen **spesifik açı/detayın** başka kanallarda ne kadar işlendiğidir.

**Formül: TANINIR İSİM + AZ İŞLENMİŞ AÇI.** Gerçekten obskür isimler hedef
değildir — isim tanınırlığı, 60+ kitle için thumbnail tıklama davranışını
yönlendiren temel faktördür. Örnek: Audrey Hepburn çok tanınır bir isim, ama
II. Dünya Savaşı direniş kuryeliği az işlenmiş bir açıdır (bu açı zaten tam
prodüksiyon paketiyle tamamlandı, bkz. aşağıdaki "Tamamlanmış Prodüksiyonlar").

**Adımlar:**
1. **Açı doygunluğu kontrolü:** Üretime başlamadan önce, seçilen spesifik
   açının başka kanallarda ne kadar işlendiğini değerlendir. Aşırı doymuşsa,
   ya aynı figürde gerçekten az işlenmiş başka bir açı bul ya da konu
   havuzundaki başka bir tanınır isme geç.
2. **Başlık kuralı kontrolü:** Başlıklar sonucu asla çözmez/ima etmez —
   sadece bir soru/gerilim yaratır. Her başlık önerisinde bu kontrolün
   yapıldığı açıkça Erdem'e belirtilir (Natalie Wood videosunun düşük
   performansının bir nedeni buydu, bkz. aşağıdaki "Önemli Öğrenmeler").
3. **Hook yapısı, konunun tanınırlığına göre değişir:**
   - Az tanınan konu (varsayılan) → **atmosferik/sahne kurulumu** açılış.
   - Yaygın tanınan/doymuş konu → **doğrudan-detay-önce** açılış (şaşırtıcı,
     spesifik bir detayla başlar; atmosfer sonra gelir).
4. **Yayın sonrası kontrol (24-48 saat):** CTR %3'ün altındaysa thumbnail
   revizyonu düşünülür; erken izleyici kaybı yüksekse bir sonraki benzer
   videonun hook'una bu öğrenme yansıtılır.
5. **Performans log'u:** Her video için doygunluk seviyesi, başlık tipi,
   hook tipi, CTR ve retention kaydedilir.

---

## 🔑 Süreç Kuralı: İkincil Figür/Canlı İçeren Hikayeler

Bir hikayenin az işlenmiş açısı, ünlü kişiyle bağlantılı **ikincil bir figür
veya canlı** (bir hayvan, az bilinen bir yakın kişi vb.) içeriyorsa:

- Script'in anlatı odağı ve perspektifi, **tüm 12 sahne boyunca isimli/tanınır
  ünlü kişide kalmalıdır.**
- İkincil figür yalnızca ünlü kişinin karakterine dair bir şey ortaya çıkaran
  **detay/pencere** görevi görür — asla ortak kahraman ya da kendi
  biyografisi anlatının omurgası olan bağımsız bir özne haline gelmemelidir.
- Bir taslak yanlışlıkla ikincil figürün hikayesini anlatmaya kayarsa, sahne
  sahne yeniden yazılarak ünlü kişinin neredeyse her sahne açılış cümlesinin
  öznesi olması sağlanmalıdır.

---

## Tamamlanmış Prodüksiyonlar (Geçmiş)

- Ronald Reagan
- Natalie Wood — **düşük performans:** (1) başlık sonucu ele veriyordu
  (kanal kuralını ihlal), (2) konu doygunluğu yüksekti. Bu iki neden, aşağıdaki
  kalıcı süreç iyileştirmelerini tetikledi (başlık kontrolü, hook tipi
  konunun tanınırlığına göre seçimi, doygunluk kontrolü adımı).
- Elizabeth Taylor
- Tammi Terrell
- Audrey Hepburn (II. Dünya Savaşı direniş kuryeliği açısı)

---

## Aktif Prodüksiyon Standartları (Kanonik)

- **Sahne sayısı: 12** (proje hafızasındaki "10" yerine — bu repoda alınan
  karar). Ayrı outro yok, kapanış Sahne 12'ye katlanır.
- **Sahne başına karakter sayısı:** kesinlikle **970–999 karakter**.
- **Toplam script hedefi:** 12 sahne × bu aralık = **~11.640–11.988 karakter**.
- **Görsel stil:** Siyah-beyaz sinematik belgesel, 35mm film grain, yüksek
  kontrast, 16:9.
- **Thumbnail standardı (güncellendi):** Eski kural (B&W split-frame,
  öncesi/sonrası kontrastı) düşük CTR verdiği için değiştirildi. **Yeni
  kural: video sahnesinin (genelde Sahne 1) renkli, yakın plan bir versiyonu**
  — tek kadraj, geniş/uzak çekim değil, yüzler net ve okunaklı olacak
  kadar yakın. Konunun ismi mutlaka yer alır (60+ kitlede tanınırlık odaklı
  tıklama davranışı); Anton font; isim küçük/beyaz üstte, curiosity-gap
  metni büyük/altın (#E8B923) altta, siyah 8px kontur + drop shadow.
  B&W/split-frame format artık varsayılan değil — istenirse A/B test için
  ayrıca denenebilir ama varsayılan artık **renkli + yakın plan + tek kare**.
- **Politika kısıtı:** Reşit olmayanların fotogerçekçi tasviri yok — bunun
  yerine siluet, sembolik obje ya da çevresel kompozisyon kullanılır.
- **Retention mimarisi:** Kanal intro'su yok; 25–35 saniye civarında pattern
  interrupt; breadcrumb suspense tüm 12 sahne boyunca korunur (hook'lar
  cevap vermez, geciktirir).
- **Prodüksiyon araç zinciri:** Claude (script + promptlar) → Google Flow
  (görsel üretimi) → Fliki (video montajı).
  - Bu repodaki make.com/Google Sheets otomasyonu, bu zincirin **Claude →
    Sheet** kısmını otomatikleştirmeyi hedefliyor; 2. otomasyon (Drive
    görselleri + Fliki) bu zincirin geri kalanını kapsayacak.

---

## "Her Şey Tamam, Hazırım" Komut Sistemi

- **Adım 1:** İçerik Fikirleri — 10 farklı içerik fikri (doygunluk kontrolü ile)
- **Adım 2:** Hook Seçenekleri — 5 alternatif giriş hook'u
- **Adım 3:** Script Yazımı — profesyonel İngilizce script
- **Adım 4:** Görsel Prompt'ları — kilitli karakter tanımları + sahne başı görsel prompt'lar
- **Adım 5:** Kapak Metni — thumbnail (istenirse A/B test formatında)
- **Adım 6:** Yayın Paketi — 5 başlık alternatifi (sonuç-çözme kontrolünden geçirilmiş) + SEO açıklama + etiketler
- **Adım 7:** Kanal adı/açıklaması güncellemesi — video yayına hazır olduğunda, "The Stories History Left Behind" belgesel formatından kurgusal/dramatize içerik formatına geçişi yansıtacak şekilde YouTube kanal adı ve açıklaması güncellenir (bkz. Studio → Customization → Basic info); açıklamada içeriğin kurgusal olduğu açıkça belirtilir.
- **Adım 8:** YouTube'a yükleme otomasyonu — tamamlanan video + başlık + açıklama + etiketlerin YouTube Data API üzerinden otomatik yüklenmesi (private olarak yüklenir, Erdem'in açık onayı olmadan asla public/scheduled yapılmaz).

### Drive kullanım standardı (Video 3'ten itibaren geçerli)
Drive artık pipeline'ın zorunlu bir parçası değil — görseller ve ham
üretim dosyaları Drive'a yüklenmez, sadece local scratchpad'de kalır.
Tek istisna: **kalite kontrolü için final video.**
1. Video derlenip YouTube'a private olarak yüklendikten sonra, aynı final
   video dosyası (görseller değil) tek başına Drive'a yüklenir.
2. Erdem'e hem Drive linki hem YouTube (private) linki paylaşılır; kalite
   kontrolünü Drive üzerinden yapabilir.
3. Erdem onay verdiğinde (video içeriğini/kalitesini onayladığında),
   `send_later` ile **24 saat sonrasına** bir hatırlatma kurulur.
4. 24 saat dolunca bu hatırlatma tetiklenir ve Drive'daki video dosyası
   Drive API ile silinir (YouTube'daki kopyaya dokunulmaz). Bu, video her
   onaylandığında tekrarlanan standart bir adımdır — ayrıca istenmesine
   gerek yoktur.

### Prodüksiyon teknik standardı (Video 3'ten itibaren geçerli)
**Önemli:** Bu standart yalnızca **henüz YouTube'a yüklenmemiş** videolar için
geçerlidir. Zaten YouTube'a yüklenmiş (private dahil) bir video, kalite
sorunu tespit edilse bile geriye dönük olarak değiştirilmez/yeniden
yüklenmez — bu tamamen Erdem'in ayrı kararına bırakılır.
- **Sahne/görsel sayısı:** Video başına **8 sahne / 8 görsel** (Erdem'in kararı, Video 3'ten itibaren).
- **Video süresi (Video 4'ten itibaren):** Hedef **12-13 dakika** — 8 görsel korunur, sahne başına metin uzatılır. Sahne başına karakter aralığı: **1450–1499** (ölçülen anlatım hızı ~15.7 kr/sn ile 8 sahne ≈ 12.3-12.7 dk). Eski 970-999 aralığı Fliki kısıtından geliyordu ve Video 3 ile birlikte emekli edildi. Speech-to-Text'in 60 sn üstü otomatik ses bölme mekanizması uzun sahneleri zaten destekliyor.
- **Konu serbestisi:** Konular tamamen uydurma olabilir (kurgu beyanı her videoda korunur).
- **Görsel üretimi HER ZAMAN Batch API ile:** Görseller istisnasız Gemini **Batch API** üzerinden üretilir (%50 indirim; işlem 24 saate kadar sürebilir, pratikte genelde dakikalar içinde biter). TTS ve Speech-to-Text batch desteklemediği için senkron kalır.
- **Görsel çözünürlüğü:** Gemini görsel üretiminde `generationConfig.imageConfig.aspectRatio: "16:9"` parametresi kullanılır (native 1344x768 çıktı); kare (1024x1024) görseli zorla 16:9'a genişletmek bulanıklığa yol açtığı için kullanılmaz.
- **Ken Burns (zoompan) efekti:** Yavaş ve sınırlı — `scale=2688:1512:flags=lanczos` ile ön ölçekleme, zoom artışı `min(zoom+0.00007,1.12)` (önceki `0.0006` / max `1.3` çok hızlıydı ve sahne sonunda yüzleri kadraj dışına taşırıyordu).
- **Video encode kalitesi:** `-preset slow -crf 18` (önceki `-preset fast`, düşük netlik).

### YouTube video meta verisi standardı (Video 3'ten itibaren geçerli)
- **Location:** United States (U.S.A)
- **Video dili / Language:** English (United States) — `snippet.defaultLanguage` ve `defaultAudioLanguage` = `en-US`
- **Made for kids:** Hayır — `status.selfDeclaredMadeForKids: false`

### Ön-prodüksiyon kontrol listesi (her video için)
1. Doygunluk kontrolü — konu/açı başka kanallarda ne kadar işlenmiş.
2. Başlık kuralı doğrulaması — sonucu çözmediği açıkça teyit edilir.
3. Hook tipi seçimi — atmosferik mi, doğrudan-detay-önce mi.
4. Karakter sayısı doğrulaması — Python regex ile sahne etiketlerinden
   (`[SCENE1]...[/SCENE1]` vb.) her sahnenin güncel aralıkta (Video 4'ten
   itibaren **1450–1499** karakter; öncesinde 970–999 idi) olduğu
   üretime/Erdem'e sunulmadan önce doğrulanır.
5. **Tekrar/benzerlik kontrolü (kritik, kanal riski):** Yeni script/hikaye,
   daha önce üretilmiş videolarla (özellikle olay örgüsü, hook, açılış/kapanış
   yapısı ve görsel sahne kompozisyonları) karşılaştırılıp **belirgin şekilde
   farklı** olduğu doğrulanır. Erdem'in benzer içerik üreten tanıdıkları,
   tekrarlayan/formülsel içerik nedeniyle YouTube'un "reused/duplicative
   content" politikası kapsamında kanal kapatılmasıyla karşılaşmış — bu
   somut, gerçek bir kanal riski. Tek karakter (Audrey Hepburn) + tek dönem
   (II. Dünya Savaşı) formatında bu risk daha yüksek olduğu için, her yeni
   video için: (a) farklı bir olay/açı seçilir (aynı "yaralı asker saklama"
   kalıbı tekrarlanmaz), (b) hook yapısı ve sahne kompozisyonları önceki
   videolardan görsel/yapısal olarak ayrıştırılır, (c) şüpheli bir benzerlik
   varsa üretime geçmeden önce Erdem'e açıkça belirtilir.
   - **Kanalda daha önce işlenmiş konular (bir daha önerilme/kullanılma):**
     Direniş kuryeliği (ayakkabıda/gizlice direniş mesajı taşıma anlatısı) —
     Erdem bu konuyu kanalda daha önce işlemiş.
6. **Kurgu serbestisi:** Hikayeler tamamen uydurma olabilir — gerçek bir
   tarihsel olaya dayanma zorunluluğu yok. (Kanal kimliğindeki "açıkça
   kurgu/dramatizasyon" beyanı her durumda korunur.)

### Oturum iş akışı sırası
Konsept fikri → konu onayı → hook seçimi → karakter sayısı doğrulamalı script
üretimi → görsel promptları (kilitli fiziksel karakter tanımlarıyla) →
thumbnail prompt'u → başlık alternatifleri (sonuç-çözme kontrolü işaretli) →
SEO açıklaması ve etiketler.

### Yayın sonrası
- 24–48 saat performans kontrolü.
- Her video için log: doygunluk seviyesi, başlık tipi, hook tipi, CTR, retention.

### Önemli Kurallar
1. **Karakter Güvenliği:** Belirlenen karakterler dışında tüm isimler hayali.
2. **Onay Sistemi:** Her aşamada onay alma zorunluluğu.
3. **Kurgusal İçerik:** Ana karakter(ler) dışında herkes kurgusal.
4. **Anlatım Stili:** 3. şahıs anlatım, gerçek kişi isimleri açıkça kullanılır.
5. **Anlatı Odağı:** İkincil figür/canlı içeren hikayelerde anlatı odağı tüm
   sahneler boyunca isimli ünlü kişide kalır (bkz. yukarıdaki süreç kuralı).

---

## Hikaye Anlatım Özellikleri

- **3. Şahıs Anlatıcı:** Objektif bir anlatıcı perspektifi.
- **Karakter Tanıtımı:** Gerçek kişilerin isimleri açıkça kullanılır.
- **Betimleme Stili:** Duygu ve düşünceler dışarıdan bir gözlemci gibi,
  belgelenmiş kaynaklara dayanarak aktarılır.
- Örnek: "[Konu kişi] kapıya doğru yürüdü. Yüzünde endişeli bir ifade vardı."

---

## Önemli Öğrenmeler ve Prensipler

- **Doygunluk en büyük risktir:** Natalie Wood seviyesinde ün/konu doygunluğu,
  hikaye ilgi çekici olsa bile "gizli an" önermesini zayıflatıyor. Az tanınan
  figürler ya da gerçekten az işlenmiş mikro-açılar, yoğun işlenmiş
  konulardan tutarlı şekilde daha iyi performans gösteriyor.
- **Başlık sonucu çözerse CTR ölür:** Başlıklar her zaman bir soru/gerilim
  yaratmalı — sonucu asla çözmemeli/ima etmemeli. Her önerilen başlıkta bu
  kontrol açıkça Erdem'e belirtilmeli.
- **Hook yapısı konu tanınırlığına bağlı:** Az tanınan konularda (varsayılan)
  atmosferik/sahne kurulumu uygun; yaygın tanınan/doymuş konularda doğrudan,
  şaşırtıcı bir detayla açılır — atmosfer sonra gelir.
- **Anlatı çerçevesi > ana karakterin demografisi:** İlişki, fedakarlık ve
  kırılganlık çerçevesi, 65+ kadın hedef segmentinde ana karakterin
  cinsiyetinden/döneminden daha çok performansı belirliyor.
- **Thumbnail'da isim:** İsim eklenmesi artık kanal standardı (60+ kitlenin
  tanınırlık odaklı tıklama davranışı nedeniyle).
- **Performans geri bildirim döngüsü:** Yayından 24–48 saat sonra CTR ~%3
  altındaysa thumbnail revizyonu düşünülür; ciddi erken retention düşüşü,
  bir sonraki benzer videonun hook'una yansıtılır.

---

## Ufuktakiler (Otomasyon Planları)

- Güncellenmiş kategori önceliklerine göre haftalık video üretimine devam.
- **Pipeline otomasyonu** (bu repodaki çalışmayla doğrudan örtüşüyor):
  - Claude çıktısını doğrudan Fliki'nin toplu oluşturma (bulk-create) CSV
    formatına dönüştürerek manuel kopyala-yapıştırı ortadan kaldırmak.
  - Görsel üretimi için resmi Gemini/Imagen API'sine geçiş ihtimali.
  - YouTube yükleme API otomasyonu (kota maliyetleri yakın zamanda düştü) —
    otomasyon yolu üzerinde henüz kesin karar verilmedi.
- Zamanla kanal-spesifik kalıpları ortaya çıkarmak için video başına
  performans log'u oluşturmak.

---

## Araçlar ve Kaynaklar

- **Claude:** Script yazımı, görsel prompt üretimi, SEO metni, iş akışı yönetimi.
- **Google Flow:** Görsel promptlarından görsel üretimi (API yok, şu an manuel).
- **Fliki:** Script ve görsellerden video montajı.
- **Python/regex araçları:** Script üretimi sırasında sahne başına karakter
  sayısı doğrulaması (bu repodaki `scripts/send_video.py` ve
  `scripts/split_script.py` bu doğrulamanın webhook/sheet tarafını yapıyor).
- **Anton font:** Kanal standardı thumbnail tipografisi.

---

## Backlog (eski format — artık aktif değil)

> Kanal artık sadece Audrey Hepburn'ü işlediği için bu liste (başka
> isimler için fikir havuzu) aktif olarak kullanılmıyor, tarihsel referans
> olarak saklanıyor.

**27 Club** ("27 Club" çerçevesi kullanılmaz — her figürün bireysel
az-işlenmiş açısı kullanılır):
- Brian Jones (Rolling Stones'tan çıkarılması/güç mücadelesi — düşük doygunluk, yüksek fırsat)
- Jim Morrison (Paris'e taşınması, şöhretten kaçış — orta doygunluk, daha keskin mikro-açı gerekli)
- Amy Winehouse (büyükannesi Cynthia'nın etkisi; veya sessiz hayır işleri)
- Kurt Cobain (sanat öğretmeni Bob Hunter mentörlüğü; Meat Puppets'ı MTV Unplugged'da öne çıkarma motivasyonu; Frances Bean ile ev videoları)

---

## Güncel Prodüksiyon Durumu (aktif)

**Video 1 — "Ormandaki Asker" (The Soldier in the Woods)**
- Konu/açı: Audrey Hepburn (kurgusal, yetişkin), II. Dünya Savaşı, Nazi
  işgali altındaki Hollanda'da yaralı bir müttefik askerini gizlice
  saklaması ve aralarında gelişen ilişki.
- Durum: **Yayında.** Tam prodüksiyon paketi tamamlandı — 12 sahnelik
  script, görseller (Gemini API, watermark'sız), seslendirme (Gemini TTS,
  "Enceladus" sesi), gerçek kelime zamanlamalı altyazı (Google
  Speech-to-Text ile), FFmpeg ile birleştirilmiş final video, thumbnail
  (renkli, yakın plan, tek kare), SEO paketi. Kullanıcı onayıyla public
  yapıldı.
- Seçilen başlık: **"The Man Audrey Hepburn Never Named"**
- Video ve görseller Drive'da `AI Videos/eg2` klasöründe.

**Video 2 — "Açlık Kışı" (The Hunger Winter)**
- Konu/açı: Audrey Hepburn (kurgusal, yetişkin), 1944-45 Hollanda
  Hongerwinter'ı (Nazi ablukası nedeniyle yaşanan gerçek kıtlık); aile
  fedakarlığı ve hayatta kalma — Video 1'den kasıtlı olarak farklı bir
  görsel/duygusal kayıt (gündüz/ev içi, orman/gece yok, ikincil aşk
  karakteri yok; tekrar kontrolü — checklist madde 5 — bu videoda
  uygulandı).
- Durum: **Tam prodüksiyon paketi tamamlandı, YouTube'a private olarak
  yüklendi, kullanıcı onayı bekleniyor.** 12 sahnelik script, görseller
  (Gemini API), seslendirme (Gemini TTS, "Enceladus"), gerçek kelime
  zamanlamalı altyazı (Speech-to-Text), FFmpeg final video (~12.5 dk),
  thumbnail (renkli, yakın plan, tek kare), SEO paketi.
- Seçilen başlık: **"Audrey Hepburn Ate Tulip Bulbs to Survive World War II"**
- Video ve görseller Drive'da `AI Videos/eg3` klasöründe.
- YouTube linki (private): https://youtube.com/watch?v=QyZ7kl8G6Fc
- Sıradaki adım: Kullanıcının video içeriğini onaylaması, ardından
  yayın zamanı belirlenip public/scheduled yapılması.

**Video 3 — "Karanlık Geceler" (The Black Evenings)**
- Konu/açı: Audrey Hepburn (kurgusal, yetişkin), işgal altındaki
  Hollanda'da "zwarte avonden" — perdeleri mühürlü evlerde alkışın
  yasak olduğu gizli dans gösterileri; toplanan paranın direnişe
  akışı. Tekrar kontrolü uygulandı: sahne/sanat/performans kaydı,
  V1'in gece/orman/asker ve V2'nin kıtlık/aile kalıplarından ayrık;
  kanalda daha önce işlenen "direniş kuryeliği" konusuna girilmedi.
- Durum: **İlk 8 sahne/8 görsel + Batch API standardıyla üretildi;
  YouTube'a private yüklendi, kalite onayı bekleniyor.** 8 sahnelik
  script (970-999 kr/sahne), görseller Batch API ile (%50 indirim,
  native 16:9), seslendirme (Enceladus), Speech-to-Text altyazı,
  yavaş zoompan + crf 18 ile FFmpeg final video (~8.4 dk), thumbnail
  (renkli, yakın plan, tek kare), SEO paketi. Yeni YouTube meta
  standardı uygulandı (en-US dil, ABD konumu, çocuklar için değil).
- Seçilen başlık: **"Audrey Hepburn Danced Where Clapping Could Get You Killed"**
- YouTube linki (private): https://youtube.com/watch?v=nE3dK2bMcJI
- Drive QC kopyası: https://drive.google.com/file/d/1J8UOFKhDN3EBY2xzvGsxXbZHU8e49g7t/view
  (görseller Drive'a yüklenmedi — yeni Drive standardı; onaydan 24 saat
  sonra bu kopya silinecek).
- Kalite onayı alındı; Erdem'in talimatıyla **25 Ağustos 2026 TR 22:00**
  (19:00 UTC) için YouTube üzerinden zamanlandı (publishAt).
- Not: Yayın saati deneyi — önceki videolar TR 19:00'da yayınlanmıştı;
  bu video ABD ET 15:00'e denk gelen TR 22:00'de yayınlanarak 24-48 saat
  sonra Analytics'te karşılaştırılacak.
- Drive QC kopyası duruyor (otomatik silme kurulumu onaylanmadı; Erdem
  istediğinde manuel silinecek).
