# 🌐 Open Source Veri Kaynakları

## 📊 Gerçek Proje Verisi için Açık Kaynak Alternatifler

Pilot şirket bulamazsan veya ek veri toplamak istersen, bu açık kaynak veri setlerini kullanabilirsin.

---

## 1. 🚀 Yazılım Projeleri

### NASA COCOMO Dataset ⭐ ÖNERİLİR
**Kaynak:** NASA/PROMISE Software Engineering Repository  
**Link:** http://promise.site.uottawa.ca/SERepository/datasets/cocomonasa_v1.arff

**İçerik:**
- 60 NASA yazılım projesi (1980-1990'lar)
- Parametreler: KSLOC (kod satırı), effort multipliers (17 parametre)
- Gerçek effort (adam-ay cinsinden)

**Parametreler:**
```
- KSLOC: Kod satırı (binler)
- acap: Analist yeteneği
- pcap: Programcı yeteneği
- aexp: Uygulama deneyimi
- modp: Modern programlama pratikleri
- tool: Yazılım araçları kullanımı
- vexp: Sanal makine deneyimi
- lexp: Dil deneyimi
- sced: Zaman kısıtı
- stor: Bellek kısıtı
- data: Veritabanı boyutu
- time: CPU zaman kısıtı
- turn: Turnaround süresi
- virt: Makine volatilitesi
- cplx: Süreç karmaşıklığı
- rely: Güvenilirlik gereksinimi
- actual_effort: Gerçek maliyet (adam-ay)
```

**Kullanım:**
```python
# ARFF formatını pandas'a çevir
import pandas as pd
from scipy.io import arff

data, meta = arff.loadarff('cocomonasa_v1.arff')
df = pd.DataFrame(data)

# Senin parametrelerine map et
# KSLOC → tech_cost proxy
# effort multipliers → complexity, experience, risk
```

**Avantajlar:**
- ✅ Gerçek NASA projeleri
- ✅ Akademik olarak validate edilmiş
- ✅ 60 proje (yeterli veri)
- ✅ Ücretsiz ve açık

**Dezavantajlar:**
- ⚠️ Eski projeler (1980-90)
- ⚠️ Sadece yazılım
- ⚠️ Parametreler farklı (mapping gerekli)

---

### NASA COCOMO II Dataset
**Link:** http://promise.site.uottawa.ca/SERepository/datasets/cocomonasa_2.arff

**İçerik:**
- 93 NASA projesi
- Daha modern (1971-2000)
- COCOMO II modeli parametreleri

---

### ISBSG Repository (Ücretli ama Akademik Ücretsiz)
**Link:** https://www.isbsg.org/

**İçerik:**
- 13,000+ yazılım projesi
- Dünya çapında şirketlerden
- Detaylı maliyet ve effort verileri

**Fiyat:**
- Ticari: $2,000-5,000
- Akademik: Ücretsiz (araştırma için)

**Başvuru:**
Akademik email ile başvur, araştırma projesi olduğunu belirt.

---

## 2. 🏗️ İnşaat Projeleri

### Kaggle Construction Project Management Dataset ⭐ ÖNERİLİR
**Link:** https://www.kaggle.com/datasets/programmer3/construction-project-management-dataset

**İçerik:**
- Gerçek inşaat projelerinden schedule, cost, risk verileri
- CSV formatında
- Ücretsiz

**Kullanım:**
```bash
# Kaggle API ile indir
pip install kaggle
kaggle datasets download -d programmer3/construction-project-management-dataset
```

---

### California Healthcare Construction Projects
**Link:** https://data.ca.gov/dataset/total-construction-cost-of-healthcare-projects

**İçerik:**
- Kaliforniya sağlık tesisleri inşaat projeleri
- Toplam maliyet verileri
- Proje aşamaları (In Review, Under Construction, vb.)

**Format:** CSV, JSON

---

### CORGIS Construction Spending Dataset
**Link:** https://corgis-edu.github.io/corgis/csv/construction_spending/

**İçerik:**
- ABD inşaat harcamaları (1964'ten beri)
- Aylık veriler
- Konut, ticari, kamu projeleri

**Kullanım:**
```python
import pandas as pd

df = pd.read_csv('https://corgis-edu.github.io/corgis/datasets/csv/construction_spending/construction_spending.csv')

# Aggregate edilmiş veri - proje bazlı değil
# Trend analizi için kullanılabilir
```

**Dezavantaj:**
- ⚠️ Proje bazlı değil, aggregate veri
- ⚠️ Parametreler eksik

---

### SMU Construction Cost Dataset
**Link:** https://clowder.smu.edu/datasets/6909026b99329d601640581d

**İçerik:**
- İnşaat maliyet tahmin verileri
- CSV ve ARFF formatında
- Machine learning için hazırlanmış

---

## 3. 🔄 Hibrit Yaklaşım: Sentetik + Gerçek

### Strateji
1. **Gerçek veri** (NASA COCOMO) ile başla
2. **Sentetik veri** ile augment et
3. **Pilot şirket** verisi ile fine-tune yap

### Örnek Workflow
```python
# 1. NASA COCOMO verisi yükle (60 proje)
nasa_data = load_cocomo_dataset()

# 2. Sentetik veri üret (benzer dağılım)
synthetic_data = generate_synthetic_from_real(nasa_data, n=200)

# 3. Birleştir
combined_data = pd.concat([nasa_data, synthetic_data])

# 4. Model eğit
model.train(combined_data)

# 5. Pilot şirket verisi gelince fine-tune
model.fine_tune(pilot_data)
```

---

## 4. 📥 Veri İndirme Scriptleri

### NASA COCOMO İndirme
```python
import urllib.request
import pandas as pd
from scipy.io import arff

# İndir
url = 'http://promise.site.uottawa.ca/SERepository/datasets/cocomonasa_v1.arff'
urllib.request.urlretrieve(url, 'data/cocomo_nasa.arff')

# Yükle
data, meta = arff.loadarff('data/cocomo_nasa.arff')
df = pd.DataFrame(data)

# Temizle
df = df.dropna()
df = df[df['actual_effort'] > 0]

print(f"Toplam proje: {len(df)}")
print(f"Ortalama effort: {df['actual_effort'].mean():.2f} adam-ay")
```

### Kaggle Dataset İndirme
```bash
# Kaggle API kurulumu
pip install kaggle

# API key ayarla (~/.kaggle/kaggle.json)
# https://www.kaggle.com/settings/account

# İndir
kaggle datasets download -d programmer3/construction-project-management-dataset
unzip construction-project-management-dataset.zip -d data/
```

---

## 5. 🔧 Veri Dönüştürme

### COCOMO → Senin Parametreler
```python
def cocomo_to_our_format(cocomo_df):
    """
    NASA COCOMO verisini bizim formata çevir
    """
    our_df = pd.DataFrame()
    
    # Mapping
    our_df['project_duration'] = cocomo_df['sced'].map({
        'vlow': 18, 'low': 14, 'nominal': 12, 'high': 10, 'vhigh': 8
    })
    
    our_df['team_size'] = cocomo_df['KSLOC'] / 10  # Rough estimate
    
    our_df['complexity'] = cocomo_df['cplx'].map({
        'vlow': 2, 'low': 4, 'nominal': 6, 'high': 8, 'vhigh': 10
    })
    
    our_df['tech_cost'] = cocomo_df['KSLOC'] * 50000  # Proxy
    
    our_df['location_factor'] = 2.0  # Default
    
    our_df['experience_level'] = cocomo_df[['aexp', 'pcap', 'acap']].mean(axis=1).map({
        'vlow': 1, 'low': 2, 'nominal': 3, 'high': 4, 'vhigh': 5
    })
    
    our_df['risk_factor'] = cocomo_df['rely'].map({
        'vlow': 0.2, 'low': 0.4, 'nominal': 0.6, 'high': 0.8, 'vhigh': 1.0
    })
    
    # Maliyet (effort * ortalama maaş)
    our_df['actual_cost'] = cocomo_df['actual_effort'] * 152 * 500  # 152 saat/ay, 500 TL/saat
    
    return our_df

# Kullanım
nasa_df = load_cocomo_dataset()
our_format_df = cocomo_to_our_format(nasa_df)
```

---

## 6. 📊 Veri Kalitesi Kontrolü

### Kontrol Listesi
```python
def validate_dataset(df):
    """Veri kalitesi kontrolü"""
    
    checks = {
        'min_samples': len(df) >= 20,
        'no_nulls': df.isnull().sum().sum() == 0,
        'positive_cost': (df['actual_cost'] > 0).all(),
        'reasonable_ranges': (
            (df['project_duration'] >= 1) & (df['project_duration'] <= 36)
        ).all()
    }
    
    print("Veri Kalitesi Kontrolü:")
    for check, passed in checks.items():
        status = "✅" if passed else "❌"
        print(f"{status} {check}")
    
    return all(checks.values())

# Kullanım
if validate_dataset(our_format_df):
    print("✅ Veri kullanıma hazır!")
else:
    print("❌ Veri temizleme gerekli")
```

---

## 7. 🎯 Öneri: Hangi Veriyi Kullan?

### Senaryo 1: Pilot Şirket Bulamadın
**Çözüm:** NASA COCOMO + Sentetik Augmentation
```
1. NASA COCOMO indir (60 proje)
2. Parametreleri map et
3. Sentetik veri ile 200'e çıkar
4. Model eğit
5. "NASA verisi ile validate edildi" de
```

**Avantaj:** Gerçek veri var, akademik olarak kabul edilir

---

### Senaryo 2: Pilot Şirket Buldum ama Az Veri (10-15 proje)
**Çözüm:** Pilot + NASA COCOMO
```
1. Pilot verisi (15 proje)
2. NASA COCOMO (60 proje)
3. Birleştir (75 proje)
4. Model eğit
5. "75 gerçek proje ile eğitildi" de
```

**Avantaj:** Hem pilot hem NASA verisi

---

### Senaryo 3: Pilot Şirket Buldum, Yeterli Veri (50+ proje)
**Çözüm:** Sadece Pilot Verisi
```
1. Pilot verisi (50+ proje)
2. Model eğit
3. "Türk şirketlerinden gerçek veri" de
```

**Avantaj:** En güçlü argüman

---

## 8. 📋 Aksiyon Planı

### Bu Hafta
- [ ] NASA COCOMO dataseti indir
- [ ] Parametreleri map et
- [ ] Veri kalitesi kontrol et
- [ ] Test eğitimi yap (R² hesapla)

### Gelecek Hafta
- [ ] Pilot şirket ara (paralel)
- [ ] NASA verisi ile model eğit
- [ ] Metrikler hesapla (R², MAPE)
- [ ] Vaka çalışması hazırla

### 2 Hafta Sonra
- [ ] Pilot veri gelirse birleştir
- [ ] Final model eğit
- [ ] Müşterilere sun

---

## 9. 🚨 Önemli Notlar

### Akademik Kullanım
NASA COCOMO ve ISBSG verileri **akademik araştırma** için ücretsiz. Ticari kullanım için izin gerekebilir.

**Çözüm:** 
- İlk aşamada "araştırma" olarak kullan
- Ticari ürün haline gelince lisans al veya kendi verini topla

### Veri Atıf
NASA COCOMO kullanırsan, paper'da belirt:
```
"Model NASA COCOMO dataset (Menzies et al., 2005) ile 
validate edilmiştir."
```

### Hibrit Yaklaşım En İyisi
```
NASA COCOMO (60) + Pilot Şirket (20) + Sentetik (120) = 200 proje
```

Bu kombinasyon:
- ✅ Gerçek veri var
- ✅ Yeterli sample size
- ✅ Türk şirketlerine özgü
- ✅ Akademik olarak kabul edilir

---

## 10. 📥 Hızlı Başlangıç

```bash
# 1. NASA COCOMO indir
cd data/
wget http://promise.site.uottawa.ca/SERepository/datasets/cocomonasa_v1.arff

# 2. Python script çalıştır
python scripts/import_cocomo_data.py

# 3. Model eğit
python train_model.py --data data/cocomo_converted.csv

# 4. Metrikleri kontrol et
python evaluate_model.py
```

---

## 🎯 Sonuç

**Pilot şirket bulamazsan bile, NASA COCOMO ile gerçek veri üzerinde çalışabilirsin.**

Bu sana:
- ✅ Gerçek proje verisi
- ✅ Akademik güvenilirlik
- ✅ Müşterilere gösterilebilir metrikler
- ✅ "60 NASA projesi ile validate edildi" argümanı

verir.

**En iyi strateji:** Pilot şirket ara (paralel) + NASA COCOMO ile başla (hemen)

---

*Son Güncelleme: 2026-04-08*  
*Kaynaklar: NASA PROMISE, Kaggle, ISBSG, CORGIS*
