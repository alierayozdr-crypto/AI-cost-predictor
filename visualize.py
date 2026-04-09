import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import pickle

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from neural_network.network import NeuralNetwork

def visualize_training_history():
    """
    Eğitim sürecini görselleştir
    """
    if not os.path.exists('models/cost_prediction_model.pkl'):
        print("❌ Model bulunamadı! Önce modeli eğitin: python train_model.py")
        return
    
    print("📊 Eğitim Geçmişi Görselleştiriliyor...")
    
    model = NeuralNetwork()
    model.load('models/cost_prediction_model.pkl')
    
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(model.loss_history, linewidth=2)
    plt.title('Eğitim Kaybı (Training Loss)', fontsize=14, fontweight='bold')
    plt.xlabel('Epoch', fontsize=12)
    plt.ylabel('MSE Loss', fontsize=12)
    plt.grid(True, alpha=0.3)
    
    plt.subplot(1, 2, 2)
    plt.plot(model.loss_history[50:], linewidth=2, color='orange')
    plt.title('Eğitim Kaybı (İlk 50 Epoch Sonrası)', fontsize=14, fontweight='bold')
    plt.xlabel('Epoch', fontsize=12)
    plt.ylabel('MSE Loss', fontsize=12)
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('training_history.png', dpi=300, bbox_inches='tight')
    print("✓ Grafik kaydedildi: training_history.png")
    plt.show()

def visualize_predictions():
    """
    Tahmin vs Gerçek değerleri görselleştir
    """
    if not os.path.exists('models/cost_prediction_model.pkl'):
        print("❌ Model bulunamadı!")
        return
    
    print("📊 Tahminler Görselleştiriliyor...")
    
    from utils.data_generator import CostDataGenerator
    from utils.data_preprocessing import DataPreprocessor
    
    model = NeuralNetwork()
    model.load('models/cost_prediction_model.pkl')
    
    with open('models/preprocessor.pkl', 'rb') as f:
        preprocessor = pickle.load(f)
    
    X, y, _ = CostDataGenerator.generate_project_cost_data(n_samples=500)
    _, X_test, _, y_test = preprocessor.train_test_split(X, y, test_size=0.3, random_state=123)
    
    X_test_norm = preprocessor.normalize(X_test, fit=False)
    y_pred_norm = model.predict(X_test_norm)
    y_pred = preprocessor.denormalize(y_pred_norm, is_target=True)
    
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.scatter(y_test, y_pred, alpha=0.5, s=30)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', linewidth=2, label='Mükemmel Tahmin')
    plt.xlabel('Gerçek Maliyet (TL)', fontsize=12)
    plt.ylabel('Tahmin Edilen Maliyet (TL)', fontsize=12)
    plt.title('Tahmin vs Gerçek Değerler', fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.subplot(1, 2, 2)
    errors = y_test - y_pred
    plt.hist(errors, bins=30, edgecolor='black', alpha=0.7)
    plt.xlabel('Tahmin Hatası (TL)', fontsize=12)
    plt.ylabel('Frekans', fontsize=12)
    plt.title('Hata Dağılımı', fontsize=14, fontweight='bold')
    plt.axvline(x=0, color='r', linestyle='--', linewidth=2)
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('prediction_analysis.png', dpi=300, bbox_inches='tight')
    print("✓ Grafik kaydedildi: prediction_analysis.png")
    plt.show()

def visualize_feature_importance():
    """
    Özellik önem analizi (basit yaklaşım)
    """
    print("📊 Özellik Önem Analizi...")
    
    from utils.data_generator import CostDataGenerator
    from utils.data_preprocessing import DataPreprocessor
    
    model = NeuralNetwork()
    model.load('models/cost_prediction_model.pkl')
    
    with open('models/preprocessor.pkl', 'rb') as f:
        preprocessor = pickle.load(f)
    
    with open('models/feature_names.pkl', 'rb') as f:
        feature_names = pickle.load(f)
    
    X, y, _ = CostDataGenerator.generate_project_cost_data(n_samples=200)
    X_norm = preprocessor.normalize(X, fit=False)
    
    baseline_pred = model.predict(X_norm)
    baseline_loss = np.mean((preprocessor.normalize_target(y, fit=False) - baseline_pred) ** 2)
    
    importances = []
    for i in range(X.shape[1]):
        X_permuted = X_norm.copy()
        np.random.shuffle(X_permuted[:, i])
        
        permuted_pred = model.predict(X_permuted)
        permuted_loss = np.mean((preprocessor.normalize_target(y, fit=False) - permuted_pred) ** 2)
        
        importance = permuted_loss - baseline_loss
        importances.append(importance)
    
    importances = np.array(importances)
    importances = (importances / importances.sum()) * 100
    
    plt.figure(figsize=(10, 6))
    colors = plt.cm.viridis(np.linspace(0, 1, len(feature_names)))
    bars = plt.barh(feature_names, importances, color=colors, edgecolor='black')
    plt.xlabel('Önem Skoru (%)', fontsize=12)
    plt.title('Özellik Önem Analizi', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3, axis='x')
    
    for i, (bar, imp) in enumerate(zip(bars, importances)):
        plt.text(imp + 0.5, i, f'{imp:.1f}%', va='center', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
    print("✓ Grafik kaydedildi: feature_importance.png")
    plt.show()

if __name__ == "__main__":
    print("=" * 70)
    print("GÖRSELLEŞTİRME ARAÇLARI")
    print("=" * 70)
    print()
    print("1. Eğitim Geçmişi")
    print("2. Tahmin Analizi")
    print("3. Özellik Önem Analizi")
    print("4. Tümünü Göster")
    print()
    
    choice = input("Seçiminiz (1-4): ")
    
    if choice == "1":
        visualize_training_history()
    elif choice == "2":
        visualize_predictions()
    elif choice == "3":
        visualize_feature_importance()
    elif choice == "4":
        visualize_training_history()
        visualize_predictions()
        visualize_feature_importance()
    else:
        print("Geçersiz seçim!")
