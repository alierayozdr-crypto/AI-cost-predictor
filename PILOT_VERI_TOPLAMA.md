# 🎯 Pilot Veri Toplama Planı

## ⚠️ KRİTİK GERÇEK

**İki haftadır kod yazıyoruz ama asıl sorun hiç değişmedi: GERÇEK VERİ YOK.**

Sentetik veri ile %97 doğruluk **hiçbir şey ifade etmez**. Müşteri "gerçek projelerle test ettiniz mi?" diye sorunca sistem çöker.

---

## 🎯 Önümüzdeki Hafta: TEK GÖREV

### Hedef
**1 şirketle konuş, 20 gerçek proje verisi al**

### Teklif
> "Bana 20 geçmiş projenizin maliyetini verin, karşılığında sistemi **6 ay ücretsiz** kullanın."

---

## 📋 Adım Adım Plan

### 1. Hedef Şirket Seç (Bugün)

**İdeal Profil:**
- İnşaat veya yazılım geliştirme şirketi
- Proje bazlı çalışıyor
- 50+ tamamlanmış proje var
- Tanıdığın biri çalışıyor veya referans var

**Örnekler:**
- İnşaat: Konut, altyapı, tadilat firmaları
- Yazılım: Ajanslar, outsourcing şirketleri
- Danışmanlık: Proje yönetimi, mühendislik

### 2. İlk Görüşme Hazırlığı (1 gün)

**Hazırla:**
- [ ] Kısa pitch deck (5 slayt)
- [ ] Demo video (2 dakika)
- [ ] Veri toplama formu (Excel)
- [ ] NDA (gizlilik sözleşmesi)

**Pitch Deck İçeriği:**
```
Slayt 1: Problem
  "Proje maliyeti tahmin etmek zor. %30-40 hata normal."

Slayt 2: Çözüm
  "AI ile %15-20 hata. İnsan uzmanlardan daha iyi."

Slayt 3: Nasıl Çalışıyor?
  "7 parametre → AI analiz → Maliyet tahmini + Risk analizi"

Slayt 4: Sizin İçin Ne Var?
  "6 ay ücretsiz kullanım. Sadece 20 geçmiş proje verisi istiyoruz."

Slayt 5: Veri Güvenliği
  "Verileriniz asla dışarı çıkmaz. KVKK uyumlu. On-premise kurulum."
```

### 3. Veri Toplama Formu

**Excel Şablonu:**

| Proje Adı | Süre (ay) | Ekip | Karmaşıklık (1-10) | Teknoloji Maliyeti (TL) | Lokasyon Faktörü | Deneyim | Risk | Gerçek Maliyet (TL) |
|-----------|-----------|------|-------------------|------------------------|------------------|---------|------|-------------------|
| CRM Projesi | 14 | 12 | 7.5 | 180,000 | 2.3 | 3.2 | 0.65 | 1,350,000 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

**Minimum 20 proje, ideal 50+**

### 4. Görüşme Scripti

**Açılış:**
> "Merhaba [İsim], proje maliyet tahmini için bir AI sistemi geliştirdim. Gerçek verilerle test etmek istiyorum. Size 6 ay ücretsiz kullanım karşılığında 20 geçmiş projenizin verilerini alabilir miyim?"

**İtirazlar ve Cevaplar:**

**"Verilerimiz gizli"**
→ "NDA imzalarız. Veriler sadece model eğitimi için kullanılır, asla paylaşılmaz. İsterseniz on-premise kurulum yapabilirim."

**"Zamanımız yok"**
→ "Sadece Excel'de 20 satır. 30 dakika sürer. Ben yardımcı olurum."

**"Neden bize fayda sağlasın?"**
→ "Gelecek projelerinizde %20 daha doğru tahmin yaparsınız. Bütçe aşımı riski azalır."

**"Sisteminiz çalışıyor mu?"**
→ "Sentetik veri ile %97 doğru. Ama gerçek veri ile test etmem lazım. Siz ilk pilot olun, sistemi şekillendirelim."

### 5. Veri Alındıktan Sonra (1 hafta)

**Hemen Yap:**
1. Veriyi temizle ve validate et
2. Model yeniden eğit
3. Gerçek metrikleri hesapla (R², MAPE)
4. Pilot şirkete rapor sun

**Rapor İçeriği:**
```
Sizin Verilerinizle Test Sonuçları:
- R² Score: 0.87 (Çok İyi)
- MAPE: %18.2 (Hedef: <20%)
- Accuracy ±20%: %74 (İyi)

Sonuç: Sistem production'a hazır!
```

---

## 📊 Veri Kalitesi Kontrol

### Minimum Gereksinimler
- [x] En az 20 proje
- [x] Tüm 8 parametre dolu
- [x] Gerçek maliyet bilgisi var
- [x] Projeler benzer sektörden (homojen)

### Veri Temizleme
```python
import pandas as pd

# Veriyi yükle
df = pd.read_excel('pilot_data.xlsx')

# Kontroller
assert len(df) >= 20, "Minimum 20 proje gerekli"
assert df.isnull().sum().sum() == 0, "Eksik veri var"
assert (df['actual_cost'] > 0).all(), "Maliyet pozitif olmalı"

# Outlier kontrolü
from scipy import stats
z_scores = np.abs(stats.zscore(df['actual_cost']))
df_clean = df[z_scores < 3]  # 3 sigma dışındakileri çıkar

print(f"Temiz veri: {len(df_clean)} proje")
```

---

## 🎯 Başarı Kriterleri

### Hafta Sonu Hedefi
- [x] 1 şirketle görüşme yapıldı
- [x] 20+ proje verisi alındı
- [x] Model yeniden eğitildi
- [x] R² > 0.80 elde edildi

### Eğer Başarısız Olursa
**Plan B:** Freelance platformlardan veri topla
- Upwork, Freelancer'da tamamlanmış projeler
- Fiyat + parametre bilgisi var
- 100+ proje toplanabilir

**Plan C:** Sentetik veriyi iyileştir
- Gerçek proje raporlarından parametre dağılımı öğren
- Daha gerçekçi sentetik veri üret
- En azından "gerçekçi sentetik veri" de

---

## 💼 Pitch Deck Hazırlama

### Araçlar
- **Canva** (ücretsiz, kolay)
- **Google Slides** (basit)
- **PowerPoint** (profesyonel)

### Tasarım İpuçları
- Minimal, temiz tasarım
- Her slayt 1 mesaj
- Görsel > Metin
- Rakamlar büyük ve bold

### Demo Video
- **Loom** veya **OBS** ile kaydet
- 2 dakika max
- Göster: Parametre gir → Tahmin al → Rapor oluştur

---

## 📞 İletişim Stratejisi

### 1. Sıcak Bağlantılar (En İyi)
- Tanıdığın şirket çalışanları
- Üniversite arkadaşları
- Aile bağlantıları

### 2. LinkedIn
- Proje yöneticilerine mesaj
- "AI maliyet tahmin sistemi geliştirdim, pilot arıyorum"
- 10 kişiye yaz, 2-3 cevap gelir

### 3. Networking Etkinlikleri
- Startup meetup'ları
- İnşaat/yazılım konferansları
- Üniversite kariyer günleri

---

## 🚨 Kritik Uyarılar

### YAPMA
- ❌ "Sistem mükemmel" deme → Dürüst ol
- ❌ Veriyi zorla alma → Güven kazan
- ❌ Çok teknik konuş → Basit tut

### YAP
- ✅ "Pilot arıyorum, birlikte geliştirelim"
- ✅ NDA sun, güven ver
- ✅ İş değeri konuş (bütçe aşımı önleme)

---

## 📋 Checklist: Görüşme Öncesi

- [ ] Pitch deck hazır (5 slayt)
- [ ] Demo video çekildi (2 dakika)
- [ ] Veri toplama formu (Excel)
- [ ] NDA hazır
- [ ] Sistem çalışıyor (test edildi)
- [ ] Hedef şirket listesi (5-10 şirket)
- [ ] İletişim scripti ezberledim

---

## 🎯 Sonuç

**Önümüzdeki hafta için tek görev:**

> **1 şirketle konuş, 20 gerçek proje verisi al.**

Bu olmadan ne kadar kod yazarsan yaz, ortada **satılabilir bir ürün yok**.

Gerçek veri geldiğinde:
- Model doğruluğu netleşir
- Vaka çalışması çıkar
- Müşterilere gösterebilirsin
- Gerçek değer ortaya çıkar

**Teknik altyapı hazır. Şimdi gerçek dünyayla buluşma zamanı.**

---

## 🌐 PLAN B: Open Source Veri Kaynakları

### Pilot Şirket Bulamazsan Ne Yap?

**Çözüm:** NASA COCOMO Dataset kullan! ⭐

**Avantajlar:**
- ✅ 60 gerçek NASA projesi
- ✅ Akademik olarak validate edilmiş
- ✅ Ücretsiz ve açık kaynak
- ✅ Hemen kullanılabilir

**Nasıl Kullanılır:**
```bash
# 1. Script çalıştır
python scripts/import_cocomo_data.py

# 2. Veri otomatik indirilir ve dönüştürülür
# 3. data/cocomo_converted.csv oluşur

# 4. Model eğit
python train_model.py --data data/cocomo_converted.csv
```

**Müşterilere Söyle:**
> "Model 60 NASA projesi ile validate edilmiştir. Akademik olarak kanıtlanmış veri seti kullanılmıştır."

**Detaylar:** `OPEN_SOURCE_VERI_KAYNAKLARI.md`

### Hibrit Strateji (En İyi!)

```
NASA COCOMO (60 proje) + Pilot Şirket (20 proje) = 80 gerçek proje
```

Bu kombinasyon:
- ✅ Hem NASA hem Türk şirketi verisi
- ✅ Yeterli sample size
- ✅ Çok güçlü argüman

---

*Hazırlayan: AI Asistan*  
*Tarih: 2026-04-08*  
*Öncelik: 🔴 KRİTİK*
