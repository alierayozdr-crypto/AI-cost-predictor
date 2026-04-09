# Railway Deployment Talimatları

## Hızlı Başlangıç

1. **Railway hesabı aç:** https://railway.app
2. **GitHub'a push et** (veya Railway CLI kullan)
3. **Railway'de New Project → Deploy from GitHub**
4. **Environment Variables ekle:**
   - `PORT=8501` (otomatik ayarlanır)
   - `DATABASE_URL` (opsiyonel - PostgreSQL eklenirse)

## Deployment Sonrası

Railway size bir URL verecek: `https://your-app.railway.app`

Bu linki arkadaşına gönder ve **gerçek proje verilerini** girmesini iste:
- Geçmiş 3-5 proje
- Gerçek süre, ekip, maliyet
- Tahminlerin doğruluğunu karşılaştır

## Kritik Not

⚠️ **Model şu an sentetik veriyle eğitilmiş**

PDF raporunda `97.58%` doğruluk gösteriyor ama bu:
- Sentetik veri üzerinde ölçülmüş
- Gerçek dünya performansını yansıtmıyor
- Müşteriye gösterilemez

**Çözüm:** 
1. Arkadaşından 10-20 gerçek proje verisi topla
2. `train_model.py` ile yeniden eğit
3. Gerçek R² skorunu PDF'e ekle
4. O zaman satılabilir ürün olur

## Railway Komutları

```bash
# Railway CLI kur
npm i -g @railway/cli

# Login
railway login

# Deploy
railway up

# Logs
railway logs

# Environment variables
railway variables
```

## Maliyet

- İlk $5 ücretsiz
- Sonrası ~$5-10/ay (hobby plan)
- Production için ~$20-50/ay

## Alternatif: Render.com

Railway yerine Render kullanmak istersen:
1. `render.yaml` oluştur
2. Render.com'a bağla
3. Aynı şekilde deploy et

Her iki platform da ücretsiz tier sunuyor.
