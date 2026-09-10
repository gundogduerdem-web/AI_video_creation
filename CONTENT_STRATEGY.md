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
kanal için bir kez OAuth onayı verir (kanal başına ayrı refresh token)
+ **her kanal için ayrı telefon doğrulaması** yapar.

**Telefon doğrulaması (kritik kurulum engeli):** Yeni bir YouTube kanalı
doğrulanmadan **özel thumbnail yüklenemez** (API `403: doesn't have
permissions to upload and set custom video thumbnails`) ve **15 dakikayı
aşan video yüklenemez**. Yeni 13-15 dk standardı bu sınıra dayanıyor:
V16 15 dk 01 sn ile sınırın **üstünde** ve sorunsuz yüklendi, yani bu
kanal doğrulanmış durumda ve sınır bizi bağlamıyor. Yine de doğrulama
düşerse ilk kırılacak yer burasıdır. Doğrulama **kanal bazındadır** — ana hesabın doğrulanmış
olması marka kanalını kapsamaz. Google bir telefon numarasıyla **yılda
en fazla 2 kanal** doğrulanmasına izin verir; Erdem'in numarası dolduğu
için (kişisel hesap + Audrey kanalı) kalan 4 kanal **2 ek telefon
numarası** gerektirir (numara başına 2 kanal). Sanal/VOIP numaraları
Google genellikle reddeder — gerçek mobil numara gerekir.
Kanal başına yapılacak: Diana kanalına geçiş → Studio → Ayarlar →
Kanal → Özellik uygunluğu → Orta düzey özellikler → telefon doğrulaması.
Thumbnail stratejinin CTR omurgası olduğu için, **doğrulanmamış kanalda
video yayınlanmaz** — üretim yapılabilir, yayın doğrulama sonrasına kalır.

**Kanal anlatıcı sesleri:** Audrey Hepburn = Enceladus (erkek). Diana =
Algieba (erkek, pürüzsüz/derin — Erdem seçti; ayrışma için her kanalın
sesi farklı tutulur). Diğer kanalların sesleri kurulumda seçilecek.

**Yaşayan kişiler kuralı (kritik, tüm kanallar):** Hikayeler vefat etmiş
ana karakter etrafında kurgulanır; ancak o kişinin çevresindeki
**yaşayan gerçek kişilere** (örn. Diana hikayelerinde Charles, William,
Harry, Camilla) uydurma kötü davranış, skandal veya söz atfedilmez —
yaşayanlar ya hiç geçmez ya isimsiz/nötr arka planda kalır; dram,
tamamen kurgusal/isimsiz yan karakterler üzerinden kurulur. Ölüm/kaza
komplo teorileri hiçbir kanalda konu edilmez. (Hukuki zemin: hakaret
ölümle düşer; Diana özelinde Cairns v. Franklin Mint (9th Cir. 2002) —
estate, UK ikametgahı nedeniyle ABD'de ölüm sonrası tanıtım hakkı
ileri süremez.)

Aşağıdaki bölümler Audrey Hepburn kanalı için yazılmıştır; teknik
standartlar (8 sahne/8 görsel, 1570-1630 kr/sahne, 13-15 dk, Vertex AI,
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

### 📊 ANALYTICS TEŞHİSİ (25 Ağu 2026) — format kararlarının veri temeli

YouTube Analytics API'den çekilen gerçek veri (Audrey kanalı, 1 Haz–25 Ağu):

- **Terk eğrisi (uzun videolar):** 0:08'de %95 → **0:25'te %57** → 0:42'de %41
  → 1:24'te %27 → sonunda %9-12. İzleyicinin yarısı **ilk 25 saniyede**
  gidiyor. 13 dk videonun ortalama izlenmesi 90-150 sn (%12-20).
- **Trafik:** izlenmelerin **%79'u Shorts akışından**; ana sayfa/Browse
  önerisi yok denecek kadar az, uzun videoya tek anlamlı kaynak %10
  "ilgili video". Yani düşük dağıtımın sebebi CTR değil, **retention**.
- **Shorts retention: %67-105** (100 üstü = tekrar izleme), video başına
  700-1000 izlenme. Kanalın çalışan tek yüzeyi.
- **Kitle hedeflemesi doğru:** %88'i 55+ (65+: %67,7 / 55-64: %20,5).
  Not: 65+ içinde erkek %43,9, kadın %23,8 — kadın payı hedefin altında.
- API'de CTR/gösterim metrikleri yok (Studio'ya özel), teşhis retention
  ve trafik kaynağı üzerinden yapıldı.

**Bu teşhise dayanan üç format kararı (Erdem onayladı, 25 Ağu):**

1. **Görsel yoğunluğu:** Sahne metinleri ve 8 sahne yapısı korunur, ama
   **her sahne için 3 görsel varyasyonu** üretilir (geniş → orta → yakın
   plan). Video başına **24 görsel**; görsel başına ekran süresi ~90 sn
   yerine **~28 sn**. Görsel monotonluk retention'ın ana düşmanı.
2. **İlk 25 saniye kuralı:** Sahne 1, hook cümlesinden sonra **derhal
   somut bir sahneye** girer (isim, saat, mekan, eylem) — atmosferik
   betimleme sonraya bırakılır; sahne 1 bir merak sözüyle biter.
   **Kurgu beyanı sahne 2'den çıkarılıp sahne 8'in sonuna taşınır**
   (eskiden tam terk noktasında "bu hikaye uydurma" deniyordu).
   Şeffaflık korunur: beyan hem videonun sonunda hem açıklamada var.
3. **Shorts frekansı:** Shorts artık sadece teaser değil, kanalın birincil
   büyüme yüzeyi olarak ele alınır; hafta sonu 3 slotluk sınır esnetilir.

### Kanal temizliği (25 Ağu 2026) — Audrey kanalı "yumuşak sıfırlama"

Erdem kanalı silip sıfırdan açmayı düşündü; **silinmedi.** Gerekçe: (a) kanal
zaten telefon doğrulamalı ve elde yedek numara yok — silmek doğrulanmış tek
varlığı kaybettirirdi, silinen kanalın doğrulama slotunu serbest bıraktığına
dair kaynak da yok; (b) sorun kanal kimliği değil retention (bkz. analytics
teşhisi); (c) korunacak birikim yok (30 abone, 72 saat izlenme).

Bunun yerine **28 eski format videosu "liste dışı" (unlisted)** yapıldı —
Elvis, Michael Jackson, Sinatra, Prince, Nixon, Marvin Gaye, Johnny Cash,
Janis Joplin, Oppenheimer vb. Amaç: YouTube'un kanal için tuttuğu konu/kitle
profilini Audrey'ye sadeleştirmek (eski videolar yeni Audrey içeriğini
yanlış kitleye gösterilmesine yol açıyordu). Bedeli: kanalın toplam
izlenmesinin %97'si (5.516/5.668) halka kapalı hale geldi.

Kanalda halka açık kalan: 4 Audrey videosu + 4 private/zamanlı Audrey
içeriği. **İşlem geri alınabilir** — videolar silinmedi, yedek liste
`unlist_backup.json` (scratchpad, oturuma bağlı) ve bu kayıt üzerinden
tek komutla public'e döndürülebilir.

### Kanal teşhisi #2 (30 Ağustos 2026) — liste dışı kararı geri alındı

Erdem'in sorusu ("bir video 96 izlenme aldı, sonrakiler 3-5, neden?")
üzerine yapılan ikinci analiz. Analytics 2 gün gecikmeli olduğu için veri
28 Ağustos'ta bitiyor.

**96 izlenme bir başarı değil, başarısız olan testti.** Video (nE3dK2bMcJI)
25 Ağustos'ta yayınlandı, ilk iki günde 7 izlenme aldı. 27-28 Ağustos'ta
YouTube feed'lerde denedi: 76 izlenme geldi, **ortalama izlenme süresi 14
saniye** (8,5 dk videonun %3,6'sı), izleyenlerin 83'ünün 82'si abone değil.
Algoritma dağıtımı kesti; sonraki videolar test bile edilmedi.

| | 25-35 sn sonra kalan | 50-70 sn sonra kalan |
|---|---|---|
| nE3dK2bMcJI (eski format) | %27,8 | %5,6 |
| V4 KGP1_ccCZ9A (yeni format) | %45,2 | %35,5 |

**Yeni retention formatı çalışıyor** (açılış tutunması ~6 kat iyi, ortalama
izlenme yüzdesi %3,6 → %17,9) ama kanalın dağıtımı zaten çökmüşken geldiği
için kendini kanıtlayacak gösterimi alamadı.

**Ana sayfa (BROWSE_FEATURES) trafiği 1-28 Ağustos boyunca tam sıfır.**
Kanal geneli: SHORTS 1128 izlenme, RELATED_VIDEO 158, SUBSCRIBER 152,
YT_SEARCH 63. Shorts'tan uzun videoya giden trafik (SHORTS_CONTENT_LINKS)
ayda **2 izlenme**.

**İlk 72 saat karşılaştırması (yaş farkı giderilmiş):** eski çok-kişili
format medyan **35** izlenme, yeni tek-kişili format medyan **7**. Eski
formatın avantajı muhtemelen içerik kalitesi değil **komşuluk yüzeyi**:
Prince/Marvin Gaye/Janis Joplin videolarının yanında önerilebiliyordu.
Tek kişilik kanalın oturabileceği yer çok dar.

**Düzeltme:** 28 Ağustos'ta 28 videoyu liste dışına alma önerisi (bkz. bir
önceki bölüm) veriye dayanmıyordu ve yanlıştı — o videolar 30-149 izlenme
taşıyordu, tutunmaları (%16-27) yeni videolardan iyiydi ve kanalın önerilen-
video yüzeyinin tamamıydı. **30 Ağustos 2026'da 28 videonun tamamı Erdem'in
onayıyla tekrar public yapıldı.**

**Açık soru (Erdem'e sunuldu):** tek kişi = tek kanal modeli, 5 kanallık
genişleme planının temeli. Bu bulgu o modele karşı bir kanıt; alternatif,
her kanalı bir kişi yerine bir temaya oturtmak.

### Yayın saati standardı (5 Eylül 2026, Erdem'in kararı)

**Varsayılan yayın saati: 00:00 (TR) = 21:00 UTC.** Uzun video da Shorts da
bu slotu kullanır. Erdem ayrı bir saat vermedikçe her yayın buraya konur,
sorulmaz.

**Çakışma sorun değil.** Aynı saatte birden fazla içerik (uzun + Shorts,
ya da iki Shorts) yayınlanabilir. Claude'un daha önce üç kez uyguladığı
"çakışmayı önlemek için Shorts'u öne al" davranışı **iptal edildi**;
saatler bu gerekçeyle kaydırılmaz.

Not: TR = UTC+3, yani 00:00 TR bir **önceki günün 21:00 UTC**'sidir.
Zamanlama yazılırken bu kayma hesaba katılmalı (`publishAt` UTC ister).

### Monetizasyon eşikleri ve Shorts kararı (1 Eylül 2026)

Erdem'in itirazı: "Shorts'tan para kazanmam için çok uzun bir izlenme süresi
gerekiyor, bu hedef gerçekçi değil." İtiraz doğru; ölçüldü.

**YouTube Partner Program eşikleri:** 1.000 abone **ve** ya 12 ayda 4.000
izlenme saati ya da 90 günde 10 milyon Shorts izlenmesi. İkisi **hiçbir zaman
birleşmiyor** ve **Shorts izlenme süresi 4.000 saate sayılmıyor.**
⚠️ **1 Şubat 2027'de eşik ikiye katlanıyor** (8.000 saat / 20 milyon Shorts).

**Kanalın konumu (1 Eylül 2026, son 365 gün):**

| Eşik | Gereken | Mevcut | Fark |
|---|---|---|---|
| Abone | 1.000 | 31 | 32× |
| İzlenme saati | 4.000 | 86,4 | 46× |
| Shorts izlenme (90 gün) | 10.000.000 | 5.766 | 1.735× |

**Shorts monetizasyon yolu kapalı.** 1.735 kat fark kapatılabilir değil.

**Claude'un önceki "Shorts'u ana ürün yap" önerisi eksik gerekçeliydi ve
düzeltildi.** Gerekçe "kanalın izlenmesinin %74'ü Shorts'tan geliyor" idi;
doğru ama varış noktası yok: Shorts'tan uzun videoya giden trafik ayda **2
izlenme**, ve 5.766 Shorts izlenmesine karşılık bir yılda **+34 abone**.
Shorts dağıtım üretiyor, gelire giden yolu beslemiyor.

**Tek monetize edilebilir yol uzun video izlenme saati.** Bugünkü tutunmayla
(12 dk videoda ~%20 = izlenme başına ~2,4 dk) 4.000 saat ≈ yılda **100.000
uzun video izlenmesi**; haftada 2 video ile video başına ~960 izlenme
gerekiyor. Mevcut: video başına 1-40. Tutunma %40'a çıkarsa gereken izlenme
50.000'e iniyor — tutunma, izlenme kadar değerli bir kaldıraç.

**Claude'un dürüst değerlendirmesi kayda geçti:** mevcut gidişatla 5 ay içinde
(Şubat 2027 öncesi) eşiğe ulaşmak gerçekçi değil ve bunu değiştirecek
kanıtlanmış bir yöntem elde yok.

**ERDEM'İN KARARI (1 Eylül 2026): Shorts üretimi DURDURULMAYACAK, mevcut
format aynen sürdürülecek.** Yukarıdaki analiz kararı değiştirmedi; karar
bilgi tam olarak verildikten sonra alındı. Shorts her videoda üretilmeye ve
planlanmaya devam eder.

### Prodüksiyon teknik standardı (Video 3'ten itibaren geçerli)
**Önemli:** Bu standart yalnızca **henüz YouTube'a yüklenmemiş** videolar için
geçerlidir. Zaten YouTube'a yüklenmiş (private dahil) bir video, kalite
sorunu tespit edilse bile geriye dönük olarak değiştirilmez/yeniden
yüklenmez — bu tamamen Erdem'in ayrı kararına bırakılır.
- **Sahne/görsel sayısı:** Video başına **8 sahne / 8 görsel** (Erdem'in kararı, Video 3'ten itibaren).
- **Video süresi (Video 17'den itibaren):** Hedef **13-15 dakika** (Erdem'in kararı, 7 Eyl 2026) — 8 görsel korunur, sahne başına metin uzatılır. Sahne başına karakter aralığı: **1570–1630**.
  - **Neden değişti (7 Eyl 2026, Video 16):** Üretim Vertex AI'a taşındı (fatura gerekçesi aşağıda) ve Vertex TTS belirgin biçimde daha yavaş okuyor: ölçülen aralık **14,6–16,0 kr/sn**, önceki yolda 16,7–21,0 idi. Aynı karakter sayısı V15'te 12,8 dk, V16'da 15,0 dk verdi. Erdem 15 dk'yı kabul edip standardı 13-15 dk'ya çekti. Yeni aralık ölçüme dayanıyor: 8 × 1570 = 13,1 dk (en hızlı okuma), 8 × 1630 = 14,9 dk (en yavaş okuma) — iki uç da hedefin içinde.
  - **Önceki hedef (Video 4–16):** 12-13 dakika, sahne başına 1690–1749 karakter. Eski 970-999 aralığı Fliki kısıtından geliyordu ve Video 3 ile birlikte emekli edildi. Speech-to-Text'in 60 sn üstü otomatik ses bölme mekanizması uzun sahneleri zaten destekliyor.
  - **Düzeltme (30 Ağu 2026, Video 8):** Önceki 1450–1499 aralığı ~15,7 kr/sn varsayımına dayanıyordu; gerçek ölçüm **~18,4 kr/sn** çıktı. Bu yüzden V4–V7 hedefin altında kaldı (V7: 11 dk 02 sn, 11.867 karakter). Yeni aralık ölçüme dayanıyor: 8 × ~1720 kr ≈ **12 dk**. Süre, TTS bittiğinde `TOPLAM` satırından doğrulanır; 12 dk altındaysa metin uzatılıp TTS tekrar üretilir. **Yayınlanmış videolar geriye dönük düzeltilmez.**
- **Konu serbestisi:** Konular tamamen uydurma olabilir (kurgu beyanı her videoda korunur).
- **Görsel üretimi Vertex AI ile, sıralı (7 Eyl 2026'dan itibaren):** Görseller `gemini-2.5-flash-image` ile Vertex üzerinden tek tek üretilir; 8 görsel ~1 dakika sürüyor. **Eski Batch API yolu (%50 indirim) terk edildi:** API anahtarı AI Studio'nun prepay bakiyesinden düşüyor ve o bakiye 7 Eyl 2026'da bitip tüm üretimi durdurdu, üstelik batch pratikte 10-30 dk sürüyordu ve V15'te bir kapak işi zaman aşımına uğradı. Vertex Cloud faturasından işlediği için projedeki kredi geçerli. Vertex'in kendi toplu işi girdi/çıktı için GCS/BigQuery istediğinden 8 görsel için kullanılmıyor. TTS ve Speech-to-Text zaten senkron.
- **Görsel çözünürlüğü:** Gemini görsel üretiminde `generationConfig.imageConfig.aspectRatio: "16:9"` parametresi kullanılır (native 1344x768 çıktı); kare (1024x1024) görseli zorla 16:9'a genişletmek bulanıklığa yol açtığı için kullanılmaz.
- **Ken Burns (zoompan) efekti:** Yavaş ve sınırlı — `scale=2688:1512:flags=lanczos` ile ön ölçekleme, zoom artışı `min(zoom+0.00007,1.12)` (önceki `0.0006` / max `1.3` çok hızlıydı ve sahne sonunda yüzleri kadraj dışına taşırıyordu).
- **Video encode kalitesi:** `-preset slow -crf 18` (önceki `-preset fast`, düşük netlik).
- **Kadraj çoğaltma (Erdem'in kararı, maliyet nedeniyle):** Görsel sayısı **8'de sabit** kalır; görsel monotonluğu, her görselden **ffmpeg ile 3 farklı kadraj** çıkararak kırılır (tam kare → %80 merkez → %62 üst-merkez kesit, her birinde yön değiştiren yavaş zoom). Ekranda 24 plan, maliyette 8 görsel. Sınırı bilinmeli: aynı görselin üç kadrajı, üç farklı görsel kadar zengin değildir — bunu telafi etmek için görsel prompt'ları derinlikli kompozisyon, tek güçlü ışık kaynağı ve ön plan bulanıklığı içerecek şekilde yazılır (yakın plana girildiğinde kadrajda detay olsun diye).
- **Görsel güvenlik filtresi (öğrenilmiş kural):** Prompt'larda yasaklı sembolleri **olumsuz biçimde bile anmayın** — "no swastikas, no political symbols" ifadesi `IMAGE_SAFETY` engeline yol açtı (8 görselden 6'sı reddedildi). Ayrıca düşman/asker karakterleri **milliyet belirtmeden**, yüzü görünmeyen/uzak/silüet figürler olarak tanımlanır. Nötrleştirilmiş prompt'larla 6/6 geçti.

### Shorts standardı (her uzun video için)
- Her uzun videonun **1 Shorts teaser'ı** üretilir: sahne 1 (hook) sesi +
  görseli, **maksimum 60 saniye**, dikey 1080x1920 (merkez 9:16 kırpma +
  yavaş zoompan), aynı altın karaoke altyazı (dikey stil), son 3.5 saniyede
  "WATCH THE FULL STORY / LINK IN DESCRIPTION" bindirmesi.
- **Açıklamanın ilk satırı:** `CLICK TO WATCH THE FULL VIDEO 👉 <ana video linki>`
  + kısa kurgu beyanı + #Shorts etiketleri.
- **Thumbnail:** dikey **9:16**, renkli, vurucu yakın plan (`generate_images.py --vertical`; oran açıkça verilmezse API 16:9 döner ve V15'te bu yüzden bir kapak yatay çıktı). YouTube'un thumbnail sistemi 16:9 tabanlı olduğu için dikey kapak bazı yüzeylerde yanlarda boşlukla gösterilebilir; Erdem 28 Ağu 2026'da mevcut Shorts kapaklarını inceleyip **iyi göründüğünü onayladı** ve dikey formatta devam kararı verdi. 16:9'a çevrilmeyecek.
- **Shorts görseli (öğrenilmiş kural):** Yatay sahne görselinin merkezden dikey kırpılması, kompozisyona göre ana karakteri kadraj dışında bırakabiliyor. Bu yüzden Short, **natif 9:16 üretilen dikey thumbnail görseliyle** derlenir (tek görsel + yavaş zoom) — hem yüz merkezde kalır hem ek maliyet olmaz, çünkü o görsel zaten thumbnail için üretiliyor.
- **Süre:** Sahne 1 anlatımı 60 sn'yi aşarsa, kelime zamanlamalarından **doğal bir cümle sonu** bulunup orada kesilir (yarım cümle bırakılmaz); tercihen merak bırakan bir cümlede.
- Shorts, ana videosu public olmadan public yapılmaz; yayın onay kapısı
  uzun videolarla aynıdır.
- **Shorts yayın takvimi (kalıcı kural, Erdem'in talimatı):** Her uzun
  videonun Shorts'u üretilir ve Shorts'lar yalnızca **hafta sonu
  akşamları — Cuma, Cumartesi, Pazar TR 22:00** — yayınlanır. Haftanın
  birikmiş Shorts sayısına bakılarak üç akşama **olabildiğince eşit**
  dağıtılır (örn. 3 Short → her akşama 1; 5 Short → 2+2+1). Hangi Short'un
  hangi akşama gideceğine Claude karar verir ve sheet'e işler.

### Video sonu çapraz tanıtım standardı
- **Gelecek uzun videolara** son ~15-20 saniyelik outro eklenir: kanalın
  diğer videolarını öneren anlatım + görsel ("More untold stories on the
  channel" + önceki videoların thumbnail kompozisyonu), YouTube end-screen
  alanına uygun düzen (son 20 saniyede sağ/orta alan boş bırakılır).
- **Kısıt:** YouTube Data API end-screen/kart eklemeyi desteklemiyor —
  end-screen'ler Studio'dan manuel eklenir (Erdem; video başına ~2 dk:
  Studio → İçerik → video → Düzenleyici → Son ekran). Baked outro bu
  manuel adımı güçlendirir ama onun yerine geçer.

### YouTube video meta verisi standardı (Video 3'ten itibaren geçerli)
- **Location:** United States (U.S.A)
- **Video dili / Language:** English (United States) — `snippet.defaultLanguage` ve `defaultAudioLanguage` = `en-US`
- **Made for kids:** Hayır — `status.selfDeclaredMadeForKids: false`

### Ön-prodüksiyon kontrol listesi (her video için)
1. Doygunluk kontrolü — konu/açı başka kanallarda ne kadar işlenmiş.
2. Başlık kuralı doğrulaması — sonucu çözmediği açıkça teyit edilir.
3. Hook tipi seçimi — atmosferik mi, doğrudan-detay-önce mi.
4. Karakter sayısı doğrulaması — Python regex ile sahne etiketlerinden
   (`[SCENE1]...[/SCENE1]` vb.) her sahnenin güncel aralıkta (Video 17'den
   itibaren **1570–1630** karakter; V8-V16 1690–1749, V4-V7 1450–1499,
   öncesinde 970–999 idi) olduğu üretime/Erdem'e sunulmadan önce doğrulanır.
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

## Analitik Teşhis #3 — CTR ve izleme süresi düşüşü (7 Eyl 2026)

Erdem'in Studio'dan bildirdiği tetikleyici: V15 125 izlenme aldı ama **CTR
%1,5** ve **ortalama izleme 1:45** — ikisi de düşüş.

**Ölçülebilenler (Analytics API):**

| Video | Abone-değil ort. izleme | Açılış cümlesi türü |
|---|---|---|
| V8 Four Hours | **4:34** | somut sahne |
| V12 Lost Part | **3:28** | somut sahne |
| V13 Platform | **3:13** | somut sahne |
| V14 Bicycle | **2:04** | hikâye hakkında yorum |
| V15 Correction | **1:45** (Studio) | hikâye hakkında yorum |

Düşüş tek yönlü ve V15'te başlamıyor — V14'te başlıyor.

**Tutunma (çalışma süresinin oranı olarak):** ilk %5'te (~40 sn) izleyicinin
%31-52'si gitmiş oluyor (V12 %68,5 kalıyor, V14 %57,9, V13 %48,3). Bu **iyi
performans gösteren videolarda da** böyle, yani yapısal. V14 ortada çöküyor:
%30 noktasında yalnızca %10,5 kalıyor (V12 %25,8, V13 %31,0).

**Trafik:** neredeyse tamamı RELATED_VIDEO (V12 119'un 100'ü, V13 43'ün 27'si,
V14 22'nin 16'sı). **BROWSE_FEATURES hiç yok** — YouTube bu videoları ana
akışa koymuyor. Önerilen-video yüzeyi doğası gereği düşük CTR'lı bir yüzeydir;
%1,5'i ana akış CTR'ıyla kıyaslamak yanlış olur.

**Elenen açıklama:** başlık uzunluğu. V11 89 karakter → 3:06; V15 86 karakter
→ 1:45. Korelasyon yok, bu bir sebep değil.

**Küçük resim (168 px yan sütun boyutunda test edildi):** V15'te karedeki en
parlak nesne **lamba**, yüz değil; koyu balıkçı yaka koyu arka planla
birleşiyor ve göz lambaya gidiyor. Ortalama parlaklık V14 70,7 / V15 59,6 /
**V16 37,3** — V16 açık ara en karanlığı ve aynı riski taşıyor.

**Kanıt gücü:** açılış cümlesi ayrımı n=5'e dayanıyor, yani güçlü bir işaret
ama kanıtlanmış değil. İzlenmeler 22-119 aralığında, gürültü yüksek.
Impressions/CTR **API'de yok**, yalnızca Studio'da. V15/V16 verisi API'ye
2-3 günde düşer; teşhis o zaman doğrulanmalı.

**Kararlar:** açılış cümlesi hikâyenin kendisiyle başlar, hikâye hakkında
yorumla değil ("This story runs backwards", "This is not a story about
Audrey Hepburn" gibi meta girişler kullanılmaz). Küçük resimde **yüz karedeki
en parlak öğe** olmalı.

### Meta cümle ölçümü (7 Eyl 2026) ve V16 testi

"Meta cümle" = hikâyeyi anlatmak yerine hikâyenin kendisinden/kurgusundan söz
eden cümle. Sahne 1'de ilk meta cümlenin **saniyesi** ölçüldüğünde sıralama
izleme süresiyle birebir örtüşüyor:

| Video | Sahne 1'de ilk meta cümle | Abone-değil ort. izleme |
|---|---|---|
| V12 | yok | **3:28** |
| V13 | yok | **3:13** |
| V16 | 0:25 | ? |
| V14 | 0:00 | **2:04** |
| V15 | 0:00 | **1:45** |

**V16 kasıtsız bir test durumu.** Teşhisten önce yazıldı; somut açılıyor ama
0:25'te "This story is made out of those fourteen fragments, and the reason to
tell it that way is…" ile kendi kurgusuna dönüyor — yani tutunmanın en çok
sızdığı ilk 40 saniyenin ortasında. Hipotez doğruysa V16'nın ortalama izleme
süresi **2:04 ile 3:13 arasına** düşmeli.

**Düşürülebilir tahmin:** V16 > 2:04 çıkarsa hipotez destek görür; 2:04'ün
altına düşerse meta-cümle açıklaması yanlıştır ve düşüşün sebebi başka yerde
aranmalıdır. Veri API'ye 9-10 Eyl civarında düşer. **V16'nın kapağı 7 Eyl'de
değiştirildi; bu CTR'ı etkiler ama izleme süresini değil, dolayısıyla test
bozulmaz.** V16 bu yüzden geriye dönük düzeltilmeyecek — düzeltmek testi yok
ederdi.

**Video 17'den itibaren kural:** sahne 1'de meta cümle **hiç** bulunmaz.
Hikâyenin nasıl anlatıldığına dair her açıklama 2. sahneye ya da sonrasına
taşınır. Anlatı yapısı (ters kronoloji, topluluk anlatımı vb.) serbest —
yasak olan onu **izleyiciye duyurmak**.

**Kapak prompt'unda "night" yazılmaz — "dusk" yazılır (7 Eyl 2026'da ölçüldü).**
V16'nın kapağı düzeltilirken önce ışık talimatı güçlendirildi ama sahne gece
kaldı; üretilen üç varyant da mevcuttan **daha karanlık** çıktı (YAVG 25-31,
mevcut 37,3). Sorun ışık tarifi değil, sahne tarifiydi: "night" modeli her
durumda karanlığa çekiyor ve "bright exposure / face is the brightest element"
talimatlarını eziyor. Sahne alacakaranlığa alınınca aynı ışık talimatlarıyla
73,6 çıktı; hafif kırpma ile **87,3**. Kanalın en iyi izleme süresine sahip
kapağı olan V14 de zaten "dusk" tarifinden geliyordu (70,7) — yani parlaklık
farkı baştan beri gece/alacakaranlık ayrımından kaynaklanıyormuş.

Kapak üretim kuralı: sahne **dusk/twilight**, ışık kaynağı **kadraj dışında**
(arka planda yüzden parlak lamba/pencere bırakılmaz), yüz kadraja hâkim.
Sonuç **168 px genişliğinde** (öneri sütunu boyutu) gözden geçirilir ve YAVG
ölçülür; hedef bant **70-90**.

---

### Arama talebi testi — zaten yapılmış (8 Eyl 2026)

V18 gerçek + aranabilir bir konuyla kurgulanacaktı. Senaryo yazıldıktan sonra
katalog kontrol edilince iki şey çıktı ve test iptal edildi.

**1. Konu zaten işlenmiş.** 23-28 Ağustos bloğu tam olarak bu alanı kaplıyor:
"The Man Audrey Hepburn Never Named" (amcası Otto), "Ate Tulip Bulbs to
Survive World War II", "Danced Where Clapping Could Get You Killed" (kara
akşamlar), "The Three Minutes That Ended Her Real Dream" (bale), "A German
Officer Slept Below Her Bedroom", ve Shorts "Hid What the Nazis Were Hunting"
(direniş). V18 taslağının 8 sahnesinden 5'i bunlarla birebir örtüşüyordu.
**Ders: senaryo yazmadan önce katalog taranır.**

**2. Test zaten yapılmış.** O blok kurgu içerikliydi ama başlıkları gerçek ve
aranabilir konulardı — ve arama sıralamasını belirleyen şey içeriğin doğruluğu
değil, başlık/metadata ve etkileşimdir. Ölçüm:

| | İzlenme | Arama | Arama payı | Browse |
|---|---|---|---|---|
| Aranabilir gerçek-konu başlığı (Tulip Bulbs) | 14 | 2 | %14,3 | 0 |
| Uydurma premise başlıkları (6 video) | 595 | 21 | %3,5 | 0 |

**Sonuç:** aranabilir başlık mekanizma olarak çalışıyor (arama payı 4 katına
çıkıyor) ama mutlak katkısı 2 izlenme, ve o video toplamda 40 kat daha az
izlenme aldı. 39 aboneyle baş terimlerde yerleşik kanallarla yarışılamıyor.
Kanalın çalışan tek yüzeyi önerilen video; arama bir kaldıraç değil.

**Karar:** konu değişimi bir büyüme kaldıracı olarak elendi. Kalan kaldıraç
tutunma ve CTR — yani önerilen videoyu besleyen iki şey.

---

### CTR teşhisi — üç ölçülmüş kusur (8 Eyl 2026)

İzleme süresi ve CTR ayrı kaldıraçlar; 7 Eyl teşhisi yalnızca birincisini
ele alıyordu. CTR tarafında ölçülen üç kusur:

**1. Kanca tıklama anında görünmüyor.** Son 8 uzun videonun 8'inde başlık
iki cümleli ve ~60 karakterde kırpılıyor, yani ödülü taşıyan ikinci cümle
karar anında hiç görünmüyor:

| Görünen | Kesilen |
|---|---|
| A Roman Street Watched Audrey Hepburn for Four Months. All F | ourteen of Them Were Wrong. |
| A Journalist Invented a Story About Audrey Hepburn. She Wait | ed 11 Years to Correct It. |
| Audrey Hepburn's Wartime Bicycle Was Found 45 Years Later. S | he Refused to Take It Back. |
| For 22 Years Audrey Hepburn Stood on the Same Platform on th | e Same Day. Nobody Knew. |

Not: başlık uzunluğu 7 Eyl'de **izleme süresi** için elenmişti (V11 89
karakterle 3:06 aldı). CTR için durum farklı — mesele uzunluk değil,
kancanın kırpılan yarıda kalması.

**2. Yedi ardışık kapak birbirinin aynı.** V10-V16'nın hepsi tek başına,
sakin ifadeli, üç-çeyrek profil bir yüz. Öneri sütununda ayırt edilemiyorlar,
üstelik trafiğimizin çoğu kendi videolarımızın birbirini önermesinden geldiği
için izleyici aynı videoyu tekrar görüyor sanıyor.

**3. Kapaklar neredeyse gri.** Ölçülen doygunluk (0-255): V10 14,2 · V11 13,5
· V12 11,9 · V13 8,3 · V14 25,6 · V15 **4,1** · V16 13,6. Yedisinin altısı
15'in altında. Erdem'in CTR şikâyeti V15 içindi ve V15 setin en düşüğü.

**Kurallar (Video 18'den itibaren):**
* Kanca ilk **~55 karaktere** yazılır; başlık kırpıldığında da tam anlaşılır.
* Kapakta çeşitlilik: her seferinde tek sakin yüz değil — iki kişi, tepki,
  nesne, eller, sahne. Kompozisyonun kendisi hikâyeyi anlatmalı.
* **Fotoğraf çıpası prompt'ta ZORUNLU** (aşağıya bkz).
* Doygunluk **post'ta** yükseltilir, prompt'ta değil. `saturation` 1,5-1,6
  iyi; 1,85'te ten turuncuya kayıyor.

### Kapak illüstrasyona kaydı — sebep ve düzeltme (9 Eyl 2026)

V18 ve V19'un kapakları fotoğraf değil, 3B render/illüstrasyon gibi çıktı.
Erdem fark etti. **Sahne görselleri etkilenmedi** — yalnızca kapaklar.

**Sebep bendeydi.** 8 Eyl'deki CTR düzeltmesinde kapak prompt'unu yeniden
yazarken fotoğraf çıpasını düşürdüm. Eski kapaklar `"Colour cinematic film
still, rich saturated colour..."` diye başlıyordu; ben onu atıp yerine
`"rich saturated colour, strong colour contrast, bright clean exposure"`
koydum. Doygunluk talebi + fotoğraf çıpasının yokluğu + baştan beri orada
duran `"painterly"` kelimesi birleşince model illüstrasyona kaydı.

**Kural: kapak prompt'u bu blokla biter (`painterly` KULLANILMAZ):**

```
Colour cinematic film still, 35mm colour film photograph, shot on Kodak
stock, photographed with a fast prime lens, natural skin texture with
visible pores and fine lines, real fabric texture, subtle lens falloff,
visible film grain, shallow depth of field, naturalistic imperfect
lighting, documentary photographic realism
```

Doygunluk/parlaklık talebi prompt'a **yazılmaz**; ışık yalnızca sahne
diliyle tarif edilir ("warm practical light from an open doorway against
cool blue dusk", "faces the brightest thing in the frame"). Renk gücü
sonradan ffmpeg ile verilir.

**Doygunluk hedefi (>20) geri çekildi.** O sayı illüstrasyon bulaşmış bir
görüntüden türetilmişti. Gerçek fotoğrafik bir alacakaranlık iç mekânı
doğal olarak daha düşük ölçüyor: V18'in fotoğrafik hâli post'ta 1,55 ile
bile 9,96, V19'unki 18,5 — ikisi de 168 px'te iyi okunuyor. Kare geneli
SATAVG karanlık kıyafet ve nötr duvarlarla düşüyor, yani tek başına ölçüt
değil. **Ölçüt 168 px kontrolüdür**; sayı yalnızca yardımcı.

**Yayınlanmış iki kapak değiştirildi** (V18 ZuEMpBVKBF4, V19 0kAtEsUqktc).
Video dosyalarına dokunulmadı.

---


**Kanıt sınırı:** bunların CTR'ı yükselttiği **kanıtlanmadı** — gösterim ve
CTR API'de yok, yalnızca Studio'da. Yukarıdakiler ölçülmüş kusurlar; etkisi
Studio'dan izlenecek.

**Parlaklık hedefi düzeltmesi:** 7 Eyl'de konan "YAVG 70-90" hedefi yüz
ağırlıklı kırpımlardan türetilmişti ve iki kişilik/geniş kompozisyonlarda
yanıltıyor — V18'in kapağı 51,8 ölçüyor ama iki yüz de kadrenin en parlak
öğesi. Ölçüm tüm kare yerine **yüz bölgesinden** yapılmalı; bu yapılana
kadar sayı tek başına ölçüt sayılmaz, 168 px kontrolü esas alınır.

---

### Kapak üstü yazı (10 Eyl 2026'dan itibaren)

Erdem kapağa **merak uyandırıcı biçimde konuyu yazmamızı** istedi. V20 bunun
ilk uygulaması. Niş standardı buydu ve tek istisna bizdik (8 Eyl teşhisi).

**Yazı modele çizdirilmez.** Görsel modelleri metni bozuk üretir. Fotoğraf
üretilir, yazı sonradan **ffmpeg drawtext** ile eklenir — tipografi böylece
kontrollü ve keskin olur.

Kalıp (V20):
```
drawbox=x=0:y=520:w=1280:h=200:color=black@0.62:t=fill,
drawtext=...:text='<KANCA SATIRI>':fontcolor=white:fontsize=62:y=548,
drawtext=...:text='<KONU SATIRI>':fontcolor=0xE8B923:fontsize=52:y=630
```

Kurallar:
* İki satır: üstte **merak** (`BORN 4 DAYS APART`), altta **konu**
  (`ONE BECAME AUDREY HEPBURN`). İkinci satır kanal altın sarısı (0xE8B923).
* Kompozisyon yazıya yer bırakacak şekilde kurulur — V20'de figürler üstte,
  alt üçte bir boş.
* Sonuç **168 px**'te okunacak: yatayda (1280 px) 62/52 punto iyi.
* **Dikeyde (1080 px) 62 punto SIĞMIYOR.** S19'da 'THE ADDRESS DID NOT EXIST'
  ve 'HE WALKED NINE HOURS ANYWAY' iki satır da kenarlardan kesildi ve
  kontrol edilmeden yüklendi. Dikeyde satır **~14 karakteri geçmemeli**;
  uzun kanca iki satıra bölünür (76 punto) ve konu satırı 44 puntoya iner.
* **Yazı eklendikten sonra küçük boyutta MUTLAKA bakılır** — kesilme
  yalnızca orada görünüyor.
* Fotoğraf çıpası korunur (9 Eyl kuralı); yazı fotoğrafı illüstrasyona
  çevirmez, prompt çevirir.

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
