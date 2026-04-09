# Pilot Test Planı — Gerçek Veri Toplama

## Amaç
Sistemi gerçek dünya verileriyle test etmek ve ilk pilot müşteriyi bulmak.

## Adımlar

### 1. Railway'e Deploy Et
```bash
# GitHub'a push et
git add .
git commit -m "Railway deployment hazır"
git push

# Railway'de deploy et
# URL örnek: https://ai-cost-predictor.railway.app
```

### 2. Arkadaşına Gönder

**Mesaj Şablonu:**
```
Merhaba,

Proje maliyet tahmin sistemi geliştirdim. Senin şirketin için test etmek istiyorum.

Link: [RAILWAY_URL]

Yapman gereken:
1. Linke tıkla
2. Geçmiş 3-5 projenizin verilerini gir:
   - Proje süresi (ay)
   - Ekip büyüklüğü
   - Teknoloji maliyeti
   - Gerçekleşen maliyet
3. Sistemin tahmini ile gerçek maliyeti karşılaştır

Tahminler makul çıkarsa, şirketiniz için özelleştirilmiş versiyon hazırlayabilirim.

Ne dersin?
```

### 3. Geri Bildirim Topla

**Sorulacak Sorular:**
- Tahminler gerçekçi mi?
- Hangi tahmin en uzak, hangi en yakın?
- Sistemin eksik gördüğü faktörler var mı?
- Şirketiniz bunu kullanır mı?

### 4. Veri Toplama

Eğer arkadaşın ilgiliyse:

**Veri Toplama Formu:**
```
Proje Adı: _______________
Süre (ay): ___
Ekip: ___ kişi
Teknoloji Maliyeti: ___ TL
Gerçek Maliyet: ___ TL

Proje Özellikleri:
- Mobil var mı? □
- AI/ML var mı? □
- Kaç entegrasyon? ___
- Risk seviyesi: Düşük / Orta / Yüksek
```

**Hedef:** Minimum 10-20 gerçek proje

### 5. Model Yeniden Eğitimi

Gerçek veri toplandıktan sonra:

```bash
# Verileri data/real_projects.csv'ye ekle
# Model yeniden eğit
python train_model.py

# Yeni doğruluk skorunu kontrol et
# Eğer R² > 0.85 ise → Production-ready
# Eğer R² < 0.85 ise → Daha fazla veri gerekli
```

### 6. Pilot Müşteri Anlaşması

Eğer sistem iyi çalışıyorsa:

**Teklif:**
- İlk 3 ay ücretsiz kullanım
- Şirket verilerini kullanarak özel model eğitimi
- Aylık raporlama ve iyileştirme
- 4. aydan itibaren aylık ücret

**Fiyatlandırma Önerisi:**
- Startup: 500-1000 TL/ay
- KOBİ: 2000-5000 TL/ay
- Kurumsal: Özel fiyat

## Başarı Kriterleri

✅ **Demo Başarılı Sayılır Eğer:**
- Arkadaşın "bunu kullanmak istiyorum" derse
- En az 1 gerçek proje tahmini %20 hata içinde
- Sistem crash etmeden çalışırsa

✅ **Pilot Başarılı Sayılır Eğer:**
- 10+ gerçek proje verisi toplandı
- Yeni model R² > 0.85
- Müşteri ödeme yapmaya razı

## Riskler ve Çözümler

**Risk 1:** Tahminler çok kötü çıkar
- **Çözüm:** "Beta versiyonu, gerçek verilerle iyileşecek" de

**Risk 2:** Arkadaşın veri vermek istemez
- **Çözüm:** NDA imzala, verilerin gizli kalacağını garanti et

**Risk 3:** Sistem çok yavaş
- **Çözüm:** Railway'i upgrade et veya caching ekle

## Sonraki Adımlar

Pilot başarılı olursa:
1. İkinci müşteri bul (referans üzerinden)
2. SaaS versiyonu yap (çoklu tenant)
3. Fiyatlandırma planları oluştur
4. Marketing sitesi kur
5. Ödeme sistemi entegre et (Stripe/iyzico)

---

**Önemli:** Bu pilot test, sistemin gerçek değerini ölçmenin tek yolu. Sentetik veriyle ne kadar iyi görünürse görünsün, gerçek dünyada test edilmeden satılamaz.
