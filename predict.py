import numpy as np
import sys
import os
import pickle

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from neural_network.network import NeuralNetwork
from utils.engineering_economics import EngineeringEconomics

def load_model():
    """
    Eğitilmiş modeli ve preprocessor'ı yükle
    """
    model = NeuralNetwork()
    model.load('models/cost_prediction_model.pkl')
    
    with open('models/preprocessor.pkl', 'rb') as f:
        preprocessor = pickle.load(f)
    
    with open('models/feature_names.pkl', 'rb') as f:
        feature_names = pickle.load(f)
    
    return model, preprocessor, feature_names

def predict_project_cost():
    """
    Yeni proje için maliyet tahmini yap
    """
    print("=" * 70)
    print("MALİYET TAHMİN SİSTEMİ")
    print("=" * 70)
    print()
    
    if not os.path.exists('models/cost_prediction_model.pkl'):
        print("❌ Model bulunamadı!")
        print("Önce modeli eğitin: python train_model.py")
        return
    
    print("📥 Model Yükleniyor...")
    model, preprocessor, feature_names = load_model()
    print("✓ Model başarıyla yüklendi")
    print()
    
    print("📝 Proje Bilgilerini Girin:")
    print("-" * 70)
    
    try:
        project_duration = float(input("Proje Süresi (ay): "))
        team_size = int(input("Ekip Büyüklüğü (kişi): "))
        complexity = float(input("Karmaşıklık Skoru (1-10): "))
        tech_cost = float(input("Teknoloji Maliyeti (TL): "))
        location_factor = float(input("Lokasyon Faktörü (1-3): "))
        experience_level = float(input("Deneyim Seviyesi (1-5): "))
        risk_factor = float(input("Risk Faktörü (0-1): "))
        
        X_new = np.array([[
            project_duration,
            team_size,
            complexity,
            tech_cost,
            location_factor,
            experience_level,
            risk_factor
        ]])
        
        X_new_norm = preprocessor.normalize(X_new, fit=False)
        
        y_pred_norm = model.predict(X_new_norm)
        y_pred = preprocessor.denormalize(y_pred_norm, is_target=True)
        
        predicted_cost = y_pred[0, 0]
        
        print()
        print("=" * 70)
        print("🎯 TAHMİN SONUÇLARI")
        print("=" * 70)
        print()
        print(f"💰 Tahmini Proje Maliyeti: {predicted_cost:,.2f} TL")
        print()
        
        base_uncertainty = 0.08
        risk_adjustment = risk_factor * 0.12
        complexity_adjustment = (complexity / 10) * 0.05
        uncertainty_rate = base_uncertainty + risk_adjustment + complexity_adjustment
        confidence_interval = predicted_cost * uncertainty_rate
        print(f"📊 Güven Aralığı (%90):")
        print(f"   Alt Sınır: {predicted_cost - confidence_interval:,.2f} TL")
        print(f"   Üst Sınır: {predicted_cost + confidence_interval:,.2f} TL")
        print()
        
        print("📈 Finansal Analiz:")
        print("-" * 70)
        
        monthly_cost = predicted_cost / project_duration
        print(f"Aylık Ortalama Maliyet: {monthly_cost:,.2f} TL")
        
        per_person_cost = predicted_cost / team_size
        print(f"Kişi Başı Maliyet: {per_person_cost:,.2f} TL")
        
        print()
        print("💡 Maliyet Optimizasyon Önerileri:")
        print("-" * 70)
        
        if complexity > 7:
            print("⚠️  Yüksek karmaşıklık maliyeti artırıyor")
            print("   → Projeyi daha küçük modüllere bölmeyi düşünün")
        
        if risk_factor > 0.6:
            print("⚠️  Yüksek risk faktörü mevcut")
            print("   → Risk azaltma stratejileri geliştirin")
        
        if experience_level < 3:
            print("⚠️  Düşük deneyim seviyesi")
            print("   → Mentörlük veya eğitim programları ekleyin")
        
        if team_size > 20:
            print("💡 Büyük ekip boyutu")
            print("   → İletişim maliyetlerini göz önünde bulundurun")
        
        print()
        
        print("🔧 Endüstri Mühendisliği Analizleri:")
        print("-" * 70)
        
        print("\n1. Başabaş Noktası Analizi:")
        expected_revenue_per_month = float(input("   Beklenen Aylık Gelir (TL): "))
        
        if expected_revenue_per_month > 0:
            break_even_months = predicted_cost / expected_revenue_per_month
            print(f"   → Başabaş Süresi: {break_even_months:.1f} ay")
            
            if break_even_months < project_duration:
                print(f"   ✓ Proje süresi içinde başabaş sağlanabilir")
            else:
                print(f"   ⚠️  Başabaş için {break_even_months - project_duration:.1f} ek ay gerekli")
        
        print("\n2. Yatırım Getirisi (ROI) Hesabı:")
        expected_total_revenue = float(input("   Beklenen Toplam Gelir (TL): "))
        
        roi = EngineeringEconomics.roi(expected_total_revenue - predicted_cost, predicted_cost)
        print(f"   → ROI: %{roi:.2f}")
        
        if roi > 20:
            print("   ✓ Yüksek getiri potansiyeli")
        elif roi > 0:
            print("   ⚠️  Orta düzey getiri")
        else:
            print("   ❌ Negatif getiri - Projeyi yeniden değerlendirin")
        
        print("\n3. Net Bugünkü Değer (NPV) Analizi:")
        discount_rate = float(input("   İskonto Oranı (örn: 0.10 = %10): "))
        
        monthly_operating_cost = predicted_cost / project_duration
        net_monthly = expected_revenue_per_month - monthly_operating_cost
        cash_flows = [-predicted_cost]
        for _ in range(int(project_duration)):
            cash_flows.append(net_monthly)
        
        npv = EngineeringEconomics.npv(cash_flows, discount_rate / 12)
        print(f"   → NPV: {npv:,.2f} TL")
        
        if npv > 0:
            print("   ✓ Proje ekonomik olarak uygun")
        else:
            print("   ❌ Proje ekonomik olarak uygun değil")
        
        print()
        print("=" * 70)
        print("✅ Analiz Tamamlandı")
        print("=" * 70)
        
    except ValueError as e:
        print(f"\n❌ Hata: Geçersiz giriş! Lütfen sayısal değerler girin.")
    except Exception as e:
        print(f"\n❌ Beklenmeyen hata: {e}")

def batch_predict():
    """
    Toplu tahmin yap (CSV dosyasından)
    """
    print("Bu özellik yakında eklenecek!")

if __name__ == "__main__":
    predict_project_cost()
