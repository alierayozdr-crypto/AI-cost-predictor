#!/bin/bash

echo "======================================================================"
echo "AI Destekli Maliyet Tahmin ve Optimizasyon Sistemi"
echo "======================================================================"
echo ""

if [ ! -f "models/cost_prediction_model.pkl" ]; then
    echo "⚠️  Model bulunamadı! Önce modeli eğitmeniz gerekiyor."
    echo ""
    read -p "Modeli şimdi eğitmek ister misiniz? (e/h): " choice
    if [ "$choice" = "e" ] || [ "$choice" = "E" ]; then
        echo ""
        echo "🎯 Model eğitiliyor..."
        python3 train_model.py
        echo ""
    else
        echo "❌ Model olmadan dashboard çalıştırılamaz."
        exit 1
    fi
fi

echo "🚀 Dashboard başlatılıyor..."
echo ""
echo "📊 Tarayıcınızda otomatik olarak açılacak."
echo "   Eğer açılmazsa: http://localhost:8501"
echo ""
echo "⏹️  Durdurmak için: Ctrl+C"
echo ""
echo "======================================================================"
echo ""

streamlit run app.py
