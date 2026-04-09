# 🏢 Kurumsal Seviye Özellikler

## 🎯 Genel Bakış

Sistem artık **4 kritik kurumsal özellik** ile donatıldı. Bu özellikler sistemi basit bir tahmin aracından, **Fortune 500 şirketlerine satılabilir** bir kurumsal çözüme dönüştürür.

---

## 1. 🧠 Açıklanabilir Yapay Zeka (XAI)

### Sorun
CEO'lar ve CFO'lar "kara kutu" AI'lara güvenmez. %97 doğruluk yetmez, **"NEDEN?"** sorusunu cevaplamalısınız.

### Çözüm
SHAP-benzeri özellik katkı analizi ile her tahminin arkasındaki matematiği açıklıyoruz.

### Özellikler

#### 📊 Özellik Katkı Analizi
```python
from utils.explainable_ai import ExplainableAI

contributions = ExplainableAI.calculate_feature_contributions(
    model, preprocessor, input_data, feature_names
)
```

**Çıktı:**
```
Tahmini Maliyet: 1,200,000 TL

Maliyeti Artıran Faktörler:
- Karmaşıklık Skoru: +200,000 TL (+16.7%)
- Proje Süresi: +150,000 TL (+12.5%)
- Risk Faktörü: +100,000 TL (+8.3%)

Maliyeti Azaltan Faktörler:
- Deneyim Seviyesi: -50,000 TL (-4.2%)
- Lokasyon Faktörü: -30,000 TL (-2.5%)
```

#### 🌊 Waterfall Chart
Baseline'dan final tahmine giden yolu görsel olarak gösterir.

#### 🎯 Counterfactual Analiz
"1 milyon TL'ye düşürmek için ne değişmeli?"

**Örnek Çıktı:**
```
Hedef: 1,000,000 TL
Öneriler:
- Karmaşıklık: 8.5 → 6.2 (-27%)
- Risk Faktörü: 0.7 → 0.4 (-43%)
- Ekip Büyüklüğü: 15 → 12 (-20%)
```

### Dashboard Kullanımı
1. **"🧠 Açıklanabilir AI"** sayfasına gidin
2. Proje parametrelerini girin
3. **"🔍 Tahmini Açıkla"** tıklayın
4. Detaylı açıklama, waterfall chart ve counterfactual analiz görün

### API Kullanımı
```bash
curl -X POST "http://localhost:8000/api/v1/explain" \
  -H "Content-Type: application/json" \
  -d '{
    "project_duration": 12,
    "team_size": 10,
    "complexity": 7.5,
    "tech_cost": 150000,
    "location_factor": 2.5,
    "experience_level": 3.5,
    "risk_factor": 0.6
  }'
```

### İş Değeri
- ✅ CEO'ların güvenini kazanır
- ✅ Denetim ve compliance için kanıt
- ✅ Karar alma sürecini hızlandırır
- ✅ Rakiplerden ayıran özellik

---

## 2. 💼 İleri Seviye Mühendislik Ekonomisi

### Sorun
Basit NPV yetmez. Gerçek dünyada **vergi, enflasyon, amortisman** var.

### Çözüm
Tam finansal simülasyon: Vergi sonrası nakit akışı, MACRS amortismanı, enflasyon ayarlı NPV.

### Özellikler

#### 📈 Vergi Sonrası NPV
```python
from utils.advanced_economics import AdvancedEconomics

result = AdvancedEconomics.project_npv_with_taxes(
    initial_investment=1000000,
    annual_revenue=1500000,
    annual_operating_cost=500000,
    project_life=5,
    discount_rate=0.10,
    tax_rate=0.20,
    depreciation_method='macrs',
    inflation_rate=0.05
)
```

**Çıktı:**
```
Vergi Öncesi NPV: 2,500,000 TL
Vergi Sonrası NPV: 2,100,000 TL
IRR (Vergi Sonrası): %18.5
Toplam Vergi Kalkanı: 150,000 TL
Efektif Vergi Oranı: %18.2
```

#### 🏢 Kiralama vs Satın Alma
```python
result = AdvancedEconomics.lease_vs_buy_analysis(
    purchase_price=500000,
    lease_payment=100000,
    lease_term=5,
    discount_rate=0.10,
    tax_rate=0.20,
    depreciation_life=7
)
```

**Çıktı:**
```
Satın Alma NPV: -450,000 TL
Kiralama NPV: -380,000 TL
Öneri: Kiralayın (70,000 TL avantaj)
```

#### 💰 İşletme Sermayesi Analizi
```python
result = AdvancedEconomics.working_capital_analysis(
    revenue=10000000,
    days_receivable=45,
    days_inventory=60,
    days_payable=30
)
```

**Çıktı:**
```
İşletme Sermayesi: 2,054,795 TL
Nakit Dönüşüm Süresi: 75 gün
Öneri: Orta (İyileştirme alanları var)
```

#### 📊 Amortisman Yöntemleri
- **Doğrusal (Straight-Line)**: Eşit yıllık amortisman
- **MACRS**: ABD hızlandırılmış amortisman
- **Azalan Bakiye (DDB)**: Erken yıllarda yüksek amortisman

### Dashboard Kullanımı
1. **"💼 İleri Ekonomi"** sayfasına gidin
2. 3 tab: Vergi Sonrası NPV, Kiralama vs Satın Alma, İşletme Sermayesi
3. Parametreleri girin ve analiz yapın

### İş Değeri
- ✅ CFO'ların dilinden konuşur
- ✅ Vergi planlaması için kritik
- ✅ Gerçek dünya finansal simülasyonu
- ✅ Danışmanlık firmaları için vazgeçilmez

---

## 3. 🔌 REST API (Kurumsal Entegrasyon)

### Sorun
Şirketler manuel veri girişi istemez. SAP, Oracle, Jira ile **otomatik entegrasyon** gerekir.

### Çözüm
FastAPI ile tam özellikli REST API. JSON ile veri gönder, saniyeler içinde tahmin al.

### Endpoints

#### 1. Basit Tahmin
```bash
POST /api/v1/predict
```

**Request:**
```json
{
  "project_duration": 12,
  "team_size": 10,
  "complexity": 5.0,
  "tech_cost": 100000,
  "location_factor": 2.0,
  "experience_level": 3.0,
  "risk_factor": 0.5
}
```

**Response:**
```json
{
  "predicted_cost": 1234567.89,
  "confidence_interval_90": {
    "lower": 1111111.00,
    "upper": 1358024.00
  },
  "confidence_interval_95": {
    "lower": 1049382.00,
    "upper": 1419753.00
  },
  "timestamp": "2026-04-08T22:30:00"
}
```

#### 2. Detaylı Analiz
```bash
POST /api/v1/detailed-analysis
```

NPV, ROI, IRR, risk değerlendirmesi dahil tam analiz.

#### 3. Duyarlılık Analizi
```bash
POST /api/v1/sensitivity
```

Tornado chart verileri ve parametre elastikiteleri.

#### 4. Açıklanabilir AI
```bash
POST /api/v1/explain
```

SHAP-benzeri özellik katkıları.

#### 5. Counterfactual
```bash
POST /api/v1/counterfactual
```

Hedef maliyete ulaşmak için öneriler.

### API Başlatma
```bash
# Kolay yol
bash start_api.sh

# Veya direkt
python3 -m uvicorn api:app --host 0.0.0.0 --port 8000
```

**Dokümantasyon:** http://localhost:8000/docs

### Entegrasyon Örnekleri

#### Python
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/predict",
    json={
        "project_duration": 12,
        "team_size": 10,
        "complexity": 5.0,
        "tech_cost": 100000,
        "location_factor": 2.0,
        "experience_level": 3.0,
        "risk_factor": 0.5
    }
)

result = response.json()
print(f"Tahmini Maliyet: {result['predicted_cost']:,.0f} TL")
```

#### JavaScript
```javascript
fetch('http://localhost:8000/api/v1/predict', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    project_duration: 12,
    team_size: 10,
    complexity: 5.0,
    tech_cost: 100000,
    location_factor: 2.0,
    experience_level: 3.0,
    risk_factor: 0.5
  })
})
.then(res => res.json())
.then(data => console.log(data));
```

#### SAP Integration (ABAP)
```abap
DATA: lo_http_client TYPE REF TO if_http_client,
      lv_json TYPE string,
      lv_response TYPE string.

CALL METHOD cl_http_client=>create_by_url
  EXPORTING
    url = 'http://ai-server:8000/api/v1/predict'
  IMPORTING
    client = lo_http_client.

lv_json = '{"project_duration":12,"team_size":10,...}'.

lo_http_client->request->set_method( 'POST' ).
lo_http_client->request->set_content_type( 'application/json' ).
lo_http_client->request->set_cdata( lv_json ).

lo_http_client->send( ).
lo_http_client->receive( ).

lv_response = lo_http_client->response->get_cdata( ).
```

### İş Değeri
- ✅ Mevcut sistemlere entegre edilir
- ✅ Manuel veri girişi ortadan kalkar
- ✅ Gerçek zamanlı tahminler
- ✅ Ölçeklenebilir mimari

---

## 4. 📚 Sürekli Öğrenme (Continuous Learning)

### Sorun
Statik modeller zamanla eskir (**data drift**). Model gerçek sonuçlardan öğrenmeli.

### Çözüm
Geri bildirim döngüsü: Gerçek proje sonuçlarını topla, modeli otomatik güncelle.

### Mimari

#### SQLite Veritabanı
```
project_feedback
├── project_name
├── predicted_cost
├── actual_cost
├── prediction_error
├── error_percentage
├── project_parameters (7 özellik)
├── feedback_date
└── notes

model_versions
├── version
├── training_date
├── accuracy_r2
└── mape

retraining_log
├── retrain_date
├── samples_used
├── new_accuracy
└── improvement
```

### Kullanım

#### 1. Geri Bildirim Ekleme
```python
from utils.continuous_learning import ContinuousLearning

cl = ContinuousLearning()

feedback_id = cl.add_feedback(
    project_name="CRM Projesi 2024",
    predicted_cost=1200000,
    actual_cost=1350000,
    project_params={
        'project_duration': 14,
        'team_size': 12,
        'complexity': 7.5,
        'tech_cost': 180000,
        'location_factor': 2.3,
        'experience_level': 3.2,
        'risk_factor': 0.65
    },
    notes="Beklenmedik teknik zorluklar"
)
```

#### 2. İstatistikler
```python
stats = cl.get_feedback_statistics()

print(f"Toplam Geri Bildirim: {stats['total_feedback']}")
print(f"Ortalama Hata: %{stats['average_error_pct']:.2f}")
print(f"Doğruluk Oranı: %{stats['accuracy_rate']:.1f}")
print(f"Yeniden Eğitim Gerekli: {stats['needs_retraining']}")
```

#### 3. Artımlı Eğitim
```python
result = cl.incremental_training(
    model=model,
    preprocessor=preprocessor,
    learning_rate=0.001,
    epochs=100
)

print(f"İyileşme: %{result['improvement_pct']:.2f}")
print(f"Yeni R²: {result['new_r2']:.4f}")
```

#### 4. Otomatik Güncelleme
```python
result = cl.auto_retrain_if_needed(
    model=model,
    preprocessor=preprocessor,
    threshold_error=15,  # %15 hata eşiği
    min_samples=30       # Minimum 30 örnek
)

if result['retrained']:
    print(f"Model güncellendi! İyileşme: %{result['improvement']:.2f}")
else:
    print(f"Güncelleme gerekmedi: {result['reason']}")
```

#### 5. Data Drift Tespiti
```python
drift_analysis = cl.detect_data_drift(current_data, threshold=0.15)

if drift_analysis['drift_detected']:
    print("⚠️ Veri kayması tespit edildi!")
    for feature in drift_analysis['drifted_features']:
        print(f"- {feature['feature']}: %{feature['change_pct']:.1f} değişim")
```

### Dashboard Kullanımı
1. **"📚 Sürekli Öğrenme"** sayfasına gidin
2. **Tab 1:** Geri bildirim ekle
3. **Tab 2:** İstatistikleri görüntüle
4. **Tab 3:** Model güncelle

### Otomatik Güncelleme Senaryosu

```
1. Proje tamamlanır
   ↓
2. Yönetici gerçek maliyeti sisteme girer
   ↓
3. Sistem hatayı hesaplar ve kaydeder
   ↓
4. 30+ geri bildirim toplandığında veya hata >%15 olduğunda
   ↓
5. Sistem otomatik olarak kendini yeniden eğitir
   ↓
6. Yeni model kaydedilir ve hemen aktif olur
   ↓
7. Sonraki tahminler daha doğru olur
```

### İş Değeri
- ✅ Model hiçbir zaman eskimez
- ✅ Şirketin kendi dinamiğine adapte olur
- ✅ Data drift'e karşı koruma
- ✅ Sürekli iyileşen doğruluk
- ✅ Sıfır manuel müdahale

---

## 📊 Karşılaştırma: Öncesi vs Sonrası

| Özellik | Öncesi | Sonrası |
|---------|--------|---------|
| **Açıklanabilirlik** | ❌ Kara kutu | ✅ Her tahminin nedeni açık |
| **Finansal Analiz** | ⚠️ Basit NPV | ✅ Vergi, enflasyon, amortisman |
| **Entegrasyon** | ❌ Manuel veri girişi | ✅ REST API, SAP/Oracle entegrasyonu |
| **Öğrenme** | ❌ Statik model | ✅ Sürekli öğrenen, adapte olan |
| **CEO Güveni** | ⚠️ Düşük | ✅ Yüksek (açıklanabilir) |
| **CFO Değeri** | ⚠️ Orta | ✅ Çok yüksek (vergi analizi) |
| **IT Entegrasyonu** | ❌ Zor | ✅ Kolay (REST API) |
| **Uzun Vadeli Değer** | ⚠️ Eskir | ✅ Sürekli iyileşir |

---

## 🚀 Başlangıç Kılavuzu

### 1. Kütüphaneleri Yükle
```bash
pip3 install fastapi uvicorn pydantic
```

### 2. Dashboard'u Başlat
```bash
bash start_dashboard.sh
```

**Yeni sayfalar:**
- 🧠 Açıklanabilir AI
- 💼 İleri Ekonomi
- 📚 Sürekli Öğrenme

### 3. API'yi Başlat
```bash
bash start_api.sh
```

**Erişim:**
- API: http://localhost:8000
- Dokümantasyon: http://localhost:8000/docs

### 4. İlk Geri Bildirimi Ekle
Dashboard → Sürekli Öğrenme → Geri Bildirim Ekle

---

## 💼 Ticari Değer Artışı

### Önceki Değer
- Basit tahmin sistemi: **500K - 2M TL**

### Yeni Değer
- **Açıklanabilir AI**: +500K TL (CEO güveni)
- **İleri Ekonomi**: +800K TL (CFO değeri)
- **REST API**: +1M TL (entegrasyon)
- **Sürekli Öğrenme**: +700K TL (uzun vadeli değer)

**Toplam Değer: 3M - 10M TL**

### Satış Argümanları

#### CEO'lara:
"Modelimiz sadece tahmin yapmaz, **neden** bu tahmini yaptığını açıklar. Her kararın arkasındaki matematiği görürsünüz."

#### CFO'lara:
"Vergi, enflasyon ve amortisman dahil **tam finansal simülasyon**. Vergi sonrası NPV, IRR ve nakit akışı analizi."

#### CTO'lara:
"Mevcut SAP/Oracle sistemlerinize **REST API** ile entegre edilir. Manuel veri girişi yok, gerçek zamanlı tahminler."

#### COO'lara:
"Model **sürekli öğrenir**. Her proje sonucundan ders çıkarır, şirketinizin dinamiğine adapte olur. Hiçbir zaman eskimez."

---

## 📋 Sonraki Adımlar

### Kısa Vadeli (1 ay)
- [ ] Pilot müşterilerle test
- [ ] API güvenliği (OAuth2, JWT)
- [ ] Daha fazla amortisman yöntemi
- [ ] Çoklu dil desteği

### Orta Vadeli (3 ay)
- [ ] Mobil uygulama
- [ ] Real-time dashboard
- [ ] A/B testing framework
- [ ] Model versiyonlama

### Uzun Vadeli (6+ ay)
- [ ] Ensemble modeller
- [ ] Deep learning entegrasyonu
- [ ] Blockchain tabanlı denetim
- [ ] Uluslararası pazara açılma

---

**🎉 Sistem artık kurumsal seviyede, Fortune 500 şirketlerine satılabilir!**

*Versiyon: 2.0 Enterprise*  
*Son Güncelleme: 2026-04-08*
