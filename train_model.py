import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from neural_network.network import NeuralNetwork
from utils.data_preprocessing import DataPreprocessor
from utils.data_generator import CostDataGenerator

def train_cost_prediction_model():
    """
    Maliyet tahmin modelini eğit
    """
    print("=" * 70)
    print("MALİYET TAHMİN VE OPTİMİZASYON MODELİ - EĞİTİM")
    print("Sıfırdan Yazılmış Yapay Zeka (Hiçbir Dış API Kullanılmamıştır)")
    print("=" * 70)
    print()
    
    print("📊 Veri Üretiliyor...")
    X, y, feature_names = CostDataGenerator.generate_project_cost_data(n_samples=2000)
    print(f"✓ {X.shape[0]} örnek, {X.shape[1]} özellik üretildi")
    print(f"✓ Özellikler: {', '.join(feature_names)}")
    print()
    
    print("🔧 Veri Ön İşleme...")
    preprocessor = DataPreprocessor()
    X_train, X_test, y_train, y_test = preprocessor.train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    X_train_norm = preprocessor.normalize(X_train, fit=True)
    X_test_norm = preprocessor.normalize(X_test, fit=False)
    
    y_train_norm = preprocessor.normalize_target(y_train, fit=True)
    y_test_norm = preprocessor.normalize_target(y_test, fit=False)
    
    print(f"✓ Eğitim seti: {X_train.shape[0]} örnek")
    print(f"✓ Test seti: {X_test.shape[0]} örnek")
    print()
    
    print("🧠 Sinir Ağı Oluşturuluyor...")
    model = NeuralNetwork()
    
    input_size = X_train_norm.shape[1]
    model.add_layer(input_size, 64, activation='relu')
    model.add_layer(64, 32, activation='relu')
    model.add_layer(32, 16, activation='relu')
    model.add_layer(16, 1, activation='linear')
    
    print(f"✓ Mimari: {input_size} -> 64 -> 32 -> 16 -> 1")
    print(f"✓ Toplam katman: {len(model.layers)}")
    print()
    
    print("🎯 Model Eğitiliyor...")
    print("(Bu işlem birkaç dakika sürebilir)")
    print("-" * 70)
    
    model.train(
        X_train_norm, 
        y_train_norm,
        epochs=1000,
        learning_rate=0.001,
        batch_size=32,
        verbose=True,
        validation_data=(X_test_norm, y_test_norm)
    )
    
    print("-" * 70)
    print()
    
    print("📈 Model Değerlendiriliyor...")
    y_pred_norm = model.predict(X_test_norm)
    y_pred = preprocessor.denormalize(y_pred_norm, is_target=True)
    
    metrics = model.evaluate(X_test_norm, y_test_norm)
    
    print(f"✓ R² Score: {metrics['r2']:.4f}")
    print(f"✓ RMSE: {metrics['rmse']:.6f} (normalize)")
    print(f"✓ MAE: {metrics['mae']:.6f} (normalize)")
    print()
    
    actual_rmse = np.sqrt(np.mean((y_test - y_pred) ** 2))
    actual_mae = np.mean(np.abs(y_test - y_pred))
    mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
    
    print("📊 Gerçek Değerler Üzerinde Performans:")
    print(f"✓ RMSE: {actual_rmse:,.2f} TL")
    print(f"✓ MAE: {actual_mae:,.2f} TL")
    print(f"✓ MAPE: {mape:.2f}%")
    print()
    
    print("💾 Model Kaydediliyor...")
    os.makedirs('models', exist_ok=True)
    model.save('models/cost_prediction_model.pkl')
    
    import pickle
    with open('models/preprocessor.pkl', 'wb') as f:
        pickle.dump(preprocessor, f)
    print("✓ Preprocessor kaydedildi: models/preprocessor.pkl")
    
    with open('models/feature_names.pkl', 'wb') as f:
        pickle.dump(feature_names, f)
    print("✓ Özellik isimleri kaydedildi: models/feature_names.pkl")
    print()
    
    print("🎉 EĞİTİM TAMAMLANDI!")
    print("=" * 70)
    print()
    print("📋 Örnek Tahminler:")
    print("-" * 70)
    
    for i in range(min(5, len(X_test))):
        print(f"\nÖrnek {i+1}:")
        for j, name in enumerate(feature_names):
            print(f"  {name}: {X_test[i, j]:.2f}")
        print(f"  → Gerçek Maliyet: {y_test[i, 0]:,.2f} TL")
        print(f"  → Tahmin: {y_pred[i, 0]:,.2f} TL")
        error = abs(y_test[i, 0] - y_pred[i, 0])
        error_pct = (error / y_test[i, 0]) * 100
        print(f"  → Hata: {error:,.2f} TL ({error_pct:.2f}%)")
    
    print()
    print("=" * 70)
    print("Tahmin yapmak için: python predict.py")
    print("=" * 70)

if __name__ == "__main__":
    train_cost_prediction_model()
