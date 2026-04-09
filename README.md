# Maliyet Tahmin ve Optimizasyon Modeli (AI)

## 🎯 Proje Amacı
Şirketlerin geçmiş finansal verilerini analiz edip, gelecekteki proje maliyetlerini, başabaş noktasını ve riskleri tahmin eden yapay zeka modeli. **Hiçbir dış API kullanılmadan**, tüm sinir ağı matematiği sıfırdan kodlanmıştır.

## 🏗️ Mimari
- **Sıfırdan Sinir Ağı**: NumPy ile yazılmış, forward propagation, backpropagation ve gradient descent
- **Özellik Mühendisliği**: Endüstri mühendisliği prensipleri (amortisman, NPV, IRR hesaplamaları)
- **Optimizasyon Algoritmaları**: Maliyet minimizasyonu ve kaynak optimizasyonu
- **Risk Analizi**: Monte Carlo simülasyonu ve senaryo analizi

## 📊 Kullanım Alanları
- Proje maliyet tahmini
- Başabaş noktası (Break-even) analizi
- Yatırım getirisi (ROI) tahmini
- Kaynak optimizasyonu
- Risk değerlendirmesi

## 🚀 Kurulum

```bash
# Gerekli kütüphaneler (sadece temel matematik için)
pip install -r requirements.txt

# Modeli eğit
python train_model.py

# Tahmin yap
python predict.py
```

## 📁 Proje Yapısı
```
├── neural_network/      # Sıfırdan yazılmış sinir ağı
├── data/               # Veri setleri
├── models/             # Eğitilmiş modeller
├── utils/              # Yardımcı fonksiyonlar
├── train_model.py      # Eğitim scripti
├── predict.py          # Tahmin scripti
└── visualize.py        # Görselleştirme
```

## 🧮 Matematiksel Temel
Model, aşağıdaki matematiksel prensiplere dayanır:
- **İleri Besleme**: y = f(W₃·f(W₂·f(W₁·x + b₁) + b₂) + b₃)
- **Kayıp Fonksiyonu**: MSE = (1/n)Σ(y_pred - y_true)²
- **Geri Yayılım**: ∂L/∂W = ∂L/∂y · ∂y/∂W (Chain Rule)
- **Optimizasyon**: W_new = W_old - α·∇L

## 📈 Performans
- Eğitim süresi: ~5-10 dakika (CPU)
- Tahmin doğruluğu: %85-95 (veri kalitesine bağlı)
- Gerçek zamanlı tahmin: <100ms

## 🎓 Öğrenme Kaynakları
Bu proje, yapay zeka matematiğini sıfırdan öğrenmek için tasarlanmıştır.
Her kod satırı açıklamalıdır ve matematiksel formüller kodda belirtilmiştir.

---
**Geliştirici**: Endüstri Mühendisliği + AI
**Lisans**: MIT
