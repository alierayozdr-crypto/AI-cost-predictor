# 📊 Model Değerlendirme Kriterleri

## 🎯 Genel Bakış

Gerçek veri topladıktan sonra modeli **nasıl değerlendireceğiz?** İşte kapsamlı kriter çerçevesi.

---

## 1. 📈 Temel Performans Metrikleri

### R² Score (Coefficient of Determination)
**Ne ölçer:** Modelin varyansın ne kadarını açıkladığı

**Değerlendirme:**
- **1.0** = Mükemmel (her tahmini doğru)
- **0.85+** = ✅ Çok İyi (HEDEF - Production'a hazır)
- **0.70-0.85** = ⚠️ İyi (Kullanılabilir, iyileştirme yapılabilir)
- **<0.70** = ❌ Zayıf (Yeniden eğitim gerekli)

**Neden önemli:**
- Akademik standart metrik
- Yatırımcılara gösterilebilir
- Rakiplerle karşılaştırılabilir

---

### MAPE (Mean Absolute Percentage Error)
**Ne ölçer:** Ortalama yüzde hata

**Değerlendirme:**
- **<10%** = ✅ Mükemmel
- **10-20%** = ✅ İyi (HEDEF - Endüstri standardı)
- **20-30%** = ⚠️ Kabul edilebilir
- **>30%** = ❌ Zayıf

**Neden önemli:**
- **En anlaşılır metrik** (CEO'lar için)
- "Tahminlerimiz ortalama %15 hata ile doğru" diyebilirsin
- Müşterilere kolayca açıklanır

**Örnek:**
```
Gerçek Maliyet: 1,000,000 TL
Tahmin: 1,150,000 TL
Hata: %15 → İyi!
```

---

### RMSE (Root Mean Squared Error)
**Ne ölçer:** Mutlak hata (TL cinsinden)

**Değerlendirme:**
- Projenin ortalama maliyetinin **%10'undan az** = ✅ İyi
- **%10-20** = ⚠️ Kabul edilebilir
- **>%20** = ❌ Zayıf

**Neden önemli:**
- Büyük hataları daha fazla cezalandırır
- Outlier tespiti için kullanılır

---

### Accuracy Within X%
**Ne ölçer:** Tahminlerin yüzde kaçı ±X% içinde?

**Hedefler:**
- **±10% içinde:** En az %40 (Mükemmel tahminler)
- **±20% içinde:** En az %70 (HEDEF - Güvenilir tahminler)
- **±30% içinde:** En az %90 (Kabul edilebilir)

**Neden önemli:**
- **İş değeri açısından en kritik metrik**
- "Tahminlerimizin %70'i ±%20 doğrulukta" → Müşteri güveni

**Örnek:**
```
100 proje:
- 45 proje ±10% içinde → %45
- 72 proje ±20% içinde → %72 ✅
- 91 proje ±30% içinde → %91
```

---

## 2. 💼 İş Etkisi Metrikleri

### Fazla Tahmin (Overestimation)
**Ne ölçer:** Model gerçekten fazla mı tahmin ediyor?

**Etki:**
- Müşteri kaybı riski (fiyat yüksek görünür)
- Rekabet dezavantajı
- Fırsat maliyeti

**Kabul Edilebilir:**
- Fazla tahmin oranı: <%60
- Ortalama fazla tahmin: <%15

---

### Az Tahmin (Underestimation)
**Ne ölçer:** Model gerçekten az mı tahmin ediyor?

**Etki:**
- Bütçe aşımı riski
- Müşteri memnuniyetsizliği
- Kar kaybı

**Kabul Edilebilir:**
- Az tahmin oranı: <%40
- Ortalama az tahmin: <%15

---

### Kritik Hatalar (>%30 hata)
**Ne ölçer:** Çok kötü tahminler

**Hedef:**
- Kritik hata oranı: **<%10** (HEDEF)
- Maksimum: %15

**Neden önemli:**
- 1 kritik hata tüm güveni yok edebilir
- Müşteri kaybı riski

---

### Sistematik Hata (Bias)
**Ne ölçer:** Model sürekli fazla mı, az mı tahmin ediyor?

**Değerlendirme:**
- **-5% ile +5% arası** = ✅ Dengeli
- **>+5%** = ⚠️ Sürekli fazla tahmin ediyor
- **<-5%** = ⚠️ Sürekli az tahmin ediyor

**Neden önemli:**
- Sistematik hata düzeltilebilir (kalibrasyon)
- Random hata düzeltmesi daha zor

---

## 3. 📊 Segment Bazlı Değerlendirme

Model **her segment** için iyi çalışmalı:

### Proje Büyüklüğüne Göre
```
Küçük Projeler (<500K TL):
  - R² > 0.80
  - MAPE < 25%

Orta Projeler (500K-2M TL):
  - R² > 0.85
  - MAPE < 20%

Büyük Projeler (>2M TL):
  - R² > 0.85
  - MAPE < 15%
```

### Sektöre Göre
```
İnşaat:
  - MAPE < 20%

Yazılım:
  - MAPE < 15%

Danışmanlık:
  - MAPE < 18%
```

### Karmaşıklığa Göre
```
Düşük Karmaşıklık (1-4):
  - MAPE < 12%

Orta Karmaşıklık (4-7):
  - MAPE < 20%

Yüksek Karmaşıklık (7-10):
  - MAPE < 30%
```

---

## 4. ✅ Production Kabul Kriterleri

Model production'a geçmek için **TÜM** kritik kriterler sağlanmalı:

### Kritik Kriterler (Olmazsa Olmaz)
- [x] **R² ≥ 0.85** (Açıklanan varyans)
- [x] **MAPE ≤ 20%** (Ortalama hata)
- [x] **Minimum 50 gerçek proje** (Veri sayısı)
- [x] **Accuracy within ±20% ≥ 70%** (Güvenilirlik)

### Yüksek Öncelikli Kriterler
- [ ] **Kritik hata oranı < 10%** (>%30 hata)
- [ ] **Bias < ±5%** (Sistematik hata)
- [ ] **Her segment için MAPE < 25%**

### Orta Öncelikli Kriterler
- [ ] **Cross-validation R² > 0.80**
- [ ] **Test seti performansı train'e yakın** (overfitting yok)

---

## 5. 🔄 Cross-Validation

**Ne:** Veriyi K parçaya böl, her seferinde farklı parça test

**Hedef:**
- CV R² > 0.80
- CV R² std < 0.05 (tutarlı)
- CV MAPE < 22%

**Neden önemli:**
- Overfitting tespiti
- Model genelleme yeteneği
- Güvenilirlik kanıtı

---

## 6. 📉 Gerçek Veri vs Sentetik Veri

### Sentetik Veri (Şu an)
```
R² = 0.9758
MAPE = %15.18
```
**Sorun:** Kendi ürettiğin veriye uyuyor, gerçek dünyayı bilmiyor

### Gerçek Veri Hedefi
```
R² > 0.85
MAPE < 20%
```
**Gerçekçi:** Gerçek dünya karmaşık, %100 doğruluk imkansız

---

## 7. 🎯 Benchmark: Rakipler ve İnsan Uzmanlar

### İnsan Uzman (Proje Yöneticisi)
- MAPE: %25-35%
- Bias: Genelde fazla tahmin (+%15)

**Hedef:** İnsan uzmanlardan daha iyi (MAPE < %20)

### Diğer AI Sistemler
- Basit regresyon: MAPE %30-40%
- Gelişmiş ML: MAPE %15-25%

**Hedef:** Sektör ortalamasında veya üstünde

---

## 8. 📊 Değerlendirme Raporu Örneği

```
═══════════════════════════════════════════════════════════════
          MODEL PERFORMANS DEĞERLENDİRME RAPORU
═══════════════════════════════════════════════════════════════

📅 Tarih: 2026-04-15
📊 Örnek Sayısı: 73 gerçek proje

1. TEMEL PERFORMANS METRİKLERİ
═══════════════════════════════════════════════════════════════

R² Score:                         0.8723 ✅
MAPE:                             %18.45 ✅
RMSE:                             234,567 TL
Accuracy within ±20%:             %73.97 ✅

2. İŞ ETKİSİ ANALİZİ
═══════════════════════════════════════════════════════════════

Fazla Tahmin:                     42 proje (%57.5)
Az Tahmin:                        31 proje (%42.5)
Kritik Hatalar (>%30):            6 proje (%8.2) ✅
Sistematik Hata (Bias):           +%2.3 ✅

3. SEGMENT ANALİZİ
═══════════════════════════════════════════════════════════════

Küçük Projeler:                   MAPE %22.1 ⚠️
Orta Projeler:                    MAPE %16.8 ✅
Büyük Projeler:                   MAPE %14.2 ✅

4. SONUÇ
═══════════════════════════════════════════════════════════════

✅ PRODUCTION'A HAZIR!

Tüm kritik kriterler sağlandı. Model güvenle kullanılabilir.

Öneriler:
  • Küçük projeler için iyileştirme yapın
  • Daha fazla veri toplayarak doğruluğu artırın
```

---

## 9. 🚨 Red Flags (Alarm Sinyalleri)

Model **kullanılmamalı** eğer:

- ❌ R² < 0.70
- ❌ MAPE > 30%
- ❌ Kritik hata oranı > %20
- ❌ Bir segment için MAPE > %40
- ❌ Sistematik hata > ±%15
- ❌ Test performansı train'den çok farklı (overfitting)

---

## 10. 📋 Değerlendirme Checklist

### Veri Toplama Sonrası
- [ ] Minimum 50 gerçek proje verisi toplandı
- [ ] Veriler temizlendi ve validate edildi
- [ ] Train/test split yapıldı (%80/%20)

### Model Eğitimi Sonrası
- [ ] R² ≥ 0.85
- [ ] MAPE ≤ 20%
- [ ] Accuracy within ±20% ≥ 70%
- [ ] Kritik hata oranı < 10%
- [ ] Bias < ±5%

### Segment Analizi
- [ ] Her segment için MAPE < 25%
- [ ] Hiçbir segment için MAPE > 40%

### Cross-Validation
- [ ] CV R² > 0.80
- [ ] CV R² std < 0.05

### İş Değeri
- [ ] İnsan uzmanlardan daha iyi (MAPE < %25)
- [ ] Pilot müşterilerden pozitif feedback
- [ ] En az 2 vaka çalışması hazır

### Production Hazırlığı
- [ ] Tüm kritik kriterler ✅
- [ ] Değerlendirme raporu hazır
- [ ] Müşterilere sunulabilir metrikler

---

## 11. 💡 Kullanım

```python
from utils.model_evaluation import ModelEvaluator

# Gerçek veri ile test
y_true = actual_costs  # Gerçek maliyetler
y_pred = model.predict(X_test)  # Tahminler

# Metrikler
metrics = ModelEvaluator.calculate_metrics(y_true, y_pred)

print(f"R²: {metrics['r2_score']:.4f}")
print(f"MAPE: {metrics['mape']:.2f}%")
print(f"Accuracy ±20%: {metrics['accuracy_within_20_pct']:.1f}%")

# Kabul kriterleri kontrolü
acceptance = ModelEvaluator.acceptance_criteria_check(metrics)

if acceptance['ready_for_production']:
    print("✅ Production'a hazır!")
else:
    print("❌ İyileştirme gerekli")

# Detaylı rapor
report = ModelEvaluator.generate_evaluation_report(
    y_true, y_pred, 
    save_path='reports/evaluation_report.txt'
)
print(report)
```

---

## 🎯 Özet: En Önemli 3 Metrik

1. **MAPE < 20%** → Müşterilere gösterilecek ana metrik
2. **R² > 0.85** → Teknik doğruluk kanıtı
3. **Accuracy ±20% > 70%** → Güvenilirlik göstergesi

Bu 3 metrik sağlanırsa → **Production'a hazır!**

---

*Son Güncelleme: 2026-04-08*  
*Versiyon: 2.0*
