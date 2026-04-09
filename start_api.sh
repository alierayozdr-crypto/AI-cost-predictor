#!/bin/bash

echo "======================================================================"
echo "AI Maliyet Tahmin API Sunucusu"
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
        echo "❌ Model olmadan API çalıştırılamaz."
        exit 1
    fi
fi

echo "🚀 API sunucusu başlatılıyor..."
echo ""
echo "📡 Erişim adresleri:"
echo "   API: http://localhost:8000"
echo "   Dokümantasyon: http://localhost:8000/docs"
echo "   Alternatif Dok: http://localhost:8000/redoc"
echo ""
echo "⏹️  Durdurmak için: Ctrl+C"
echo ""
echo "======================================================================"
echo ""

python3 -m uvicorn api:app --host 0.0.0.0 --port 8000 --reload
