"""
Model Değerlendirme ve Validasyon
Gerçek veri ile model performansını ölçme
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
import matplotlib.pyplot as plt
from datetime import datetime

class ModelEvaluator:
    """
    Kapsamlı model değerlendirme sistemi
    
    Gerçek proje verileri ile modelin performansını ölçer.
    """
    
    @staticmethod
    def calculate_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict:
        """
        Temel performans metrikleri
        
        Args:
            y_true: Gerçek değerler
            y_pred: Tahmin edilen değerler
        
        Returns:
            dict: Tüm metrikler
        """
        # R² Score (Coefficient of Determination)
        # 1.0 = mükemmel, 0.0 = ortalama kadar iyi, negatif = ortalamadan kötü
        ss_res = np.sum((y_true - y_pred) ** 2)
        ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
        r2 = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        
        # RMSE (Root Mean Squared Error)
        # Mutlak hata, y ile aynı birimde
        rmse = np.sqrt(np.mean((y_true - y_pred) ** 2))
        
        # MAE (Mean Absolute Error)
        # Ortalama mutlak hata
        mae = np.mean(np.abs(y_true - y_pred))
        
        # MAPE (Mean Absolute Percentage Error)
        # Yüzde olarak hata - en anlaşılır metrik
        mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
        
        # Median Absolute Error
        # Outlier'lara karşı daha robust
        median_ae = np.median(np.abs(y_true - y_pred))
        
        # Max Error
        # En kötü tahmin
        max_error = np.max(np.abs(y_true - y_pred))
        
        # Accuracy within X%
        # Tahminlerin yüzde kaçı ±X% içinde?
        within_10_pct = np.mean(np.abs((y_true - y_pred) / y_true) < 0.10) * 100
        within_20_pct = np.mean(np.abs((y_true - y_pred) / y_true) < 0.20) * 100
        within_30_pct = np.mean(np.abs((y_true - y_pred) / y_true) < 0.30) * 100
        
        # Bias (Sistematik hata)
        # Pozitif = model fazla tahmin ediyor
        # Negatif = model az tahmin ediyor
        bias = np.mean(y_pred - y_true)
        bias_pct = (bias / np.mean(y_true)) * 100
        
        return {
            'r2_score': r2,
            'rmse': rmse,
            'mae': mae,
            'mape': mape,
            'median_absolute_error': median_ae,
            'max_error': max_error,
            'accuracy_within_10_pct': within_10_pct,
            'accuracy_within_20_pct': within_20_pct,
            'accuracy_within_30_pct': within_30_pct,
            'bias': bias,
            'bias_percentage': bias_pct,
            'n_samples': len(y_true)
        }
    
    @staticmethod
    def evaluate_by_segment(y_true: np.ndarray, y_pred: np.ndarray, 
                           segments: np.ndarray, segment_name: str) -> pd.DataFrame:
        """
        Segment bazlı değerlendirme
        
        Örnek: Küçük/orta/büyük projeler için ayrı metrikler
        
        Args:
            y_true: Gerçek değerler
            y_pred: Tahminler
            segments: Segment etiketleri
            segment_name: Segment adı
        
        Returns:
            DataFrame: Segment bazlı metrikler
        """
        results = []
        
        for segment in np.unique(segments):
            mask = segments == segment
            
            if np.sum(mask) > 0:
                metrics = ModelEvaluator.calculate_metrics(
                    y_true[mask], 
                    y_pred[mask]
                )
                metrics['segment'] = segment
                metrics['segment_name'] = segment_name
                results.append(metrics)
        
        return pd.DataFrame(results)
    
    @staticmethod
    def cross_validation_score(model, preprocessor, X: np.ndarray, 
                              y: np.ndarray, k_folds: int = 5) -> Dict:
        """
        K-Fold Cross Validation
        
        Veriyi K parçaya böl, her seferinde 1 parça test, K-1 parça train
        
        Args:
            model: Model
            preprocessor: Veri ön işleyici
            X: Özellikler
            y: Hedef
            k_folds: Kaç fold
        
        Returns:
            dict: CV metrikleri
        """
        from sklearn.model_selection import KFold
        
        kf = KFold(n_splits=k_folds, shuffle=True, random_state=42)
        
        r2_scores = []
        mape_scores = []
        
        for train_idx, test_idx in kf.split(X):
            X_train, X_test = X[train_idx], X[test_idx]
            y_train, y_test = y[train_idx], y[test_idx]
            
            # Normalize
            X_train_norm = preprocessor.normalize(X_train, fit=True)
            X_test_norm = preprocessor.normalize(X_test, fit=False)
            y_train_norm = preprocessor.normalize_target(y_train, fit=True)
            
            # Train
            model.train(X_train_norm, y_train_norm, epochs=200, 
                       learning_rate=0.001, verbose=False)
            
            # Predict
            y_pred_norm = model.predict(X_test_norm)
            y_pred = preprocessor.denormalize(y_pred_norm, is_target=True)
            
            # Metrics
            metrics = ModelEvaluator.calculate_metrics(y_test, y_pred)
            r2_scores.append(metrics['r2_score'])
            mape_scores.append(metrics['mape'])
        
        return {
            'cv_r2_mean': np.mean(r2_scores),
            'cv_r2_std': np.std(r2_scores),
            'cv_mape_mean': np.mean(mape_scores),
            'cv_mape_std': np.std(mape_scores),
            'cv_r2_scores': r2_scores,
            'cv_mape_scores': mape_scores
        }
    
    @staticmethod
    def business_impact_analysis(y_true: np.ndarray, y_pred: np.ndarray) -> Dict:
        """
        İş etkisi analizi
        
        Tahmin hatalarının finansal etkisi
        
        Args:
            y_true: Gerçek maliyetler
            y_pred: Tahmin edilen maliyetler
        
        Returns:
            dict: İş metrikleri
        """
        errors = y_pred - y_true
        
        # Fazla tahmin edilen projeler (bütçe kaybı riski)
        overestimated = errors > 0
        overestimation_total = np.sum(errors[overestimated])
        overestimation_count = np.sum(overestimated)
        
        # Az tahmin edilen projeler (bütçe aşımı riski)
        underestimated = errors < 0
        underestimation_total = np.sum(np.abs(errors[underestimated]))
        underestimation_count = np.sum(underestimated)
        
        # Kritik hatalar (>%30 hata)
        critical_errors = np.abs(errors / y_true) > 0.30
        critical_error_count = np.sum(critical_errors)
        critical_error_rate = (critical_error_count / len(y_true)) * 100
        
        # Toplam finansal etki
        total_financial_impact = np.sum(np.abs(errors))
        avg_financial_impact = np.mean(np.abs(errors))
        
        return {
            'overestimation_total': overestimation_total,
            'overestimation_count': int(overestimation_count),
            'overestimation_avg': overestimation_total / max(overestimation_count, 1),
            'underestimation_total': underestimation_total,
            'underestimation_count': int(underestimation_count),
            'underestimation_avg': underestimation_total / max(underestimation_count, 1),
            'critical_error_count': int(critical_error_count),
            'critical_error_rate': critical_error_rate,
            'total_financial_impact': total_financial_impact,
            'avg_financial_impact': avg_financial_impact
        }
    
    @staticmethod
    def generate_evaluation_report(y_true: np.ndarray, y_pred: np.ndarray,
                                   project_names: List[str] = None,
                                   save_path: str = None) -> str:
        """
        Kapsamlı değerlendirme raporu oluştur
        
        Args:
            y_true: Gerçek değerler
            y_pred: Tahminler
            project_names: Proje isimleri (opsiyonel)
            save_path: Rapor kayıt yolu
        
        Returns:
            str: Rapor metni
        """
        metrics = ModelEvaluator.calculate_metrics(y_true, y_pred)
        business = ModelEvaluator.business_impact_analysis(y_true, y_pred)
        
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║          MODEL PERFORMANS DEĞERLENDİRME RAPORU              ║
╚══════════════════════════════════════════════════════════════╝

📅 Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
📊 Örnek Sayısı: {metrics['n_samples']}

═══════════════════════════════════════════════════════════════
1. TEMEL PERFORMANS METRİKLERİ
═══════════════════════════════════════════════════════════════

R² Score (Açıklanan Varyans):     {metrics['r2_score']:.4f}
  ├─ 1.0 = Mükemmel
  ├─ 0.85+ = Çok İyi (Hedef)
  ├─ 0.70-0.85 = İyi
  └─ <0.70 = İyileştirme Gerekli

MAPE (Ortalama Yüzde Hata):       %{metrics['mape']:.2f}
  ├─ <10% = Mükemmel
  ├─ 10-20% = İyi (Hedef)
  ├─ 20-30% = Kabul Edilebilir
  └─ >30% = Zayıf

RMSE (Kök Ortalama Kare Hata):    {metrics['rmse']:,.0f} TL
MAE (Ortalama Mutlak Hata):       {metrics['mae']:,.0f} TL
Median Mutlak Hata:               {metrics['median_absolute_error']:,.0f} TL
Maksimum Hata:                    {metrics['max_error']:,.0f} TL

═══════════════════════════════════════════════════════════════
2. DOĞRULUK ANALİZİ
═══════════════════════════════════════════════════════════════

Tahminlerin Doğruluk Oranları:
  ├─ ±10% içinde:  %{metrics['accuracy_within_10_pct']:.1f}
  ├─ ±20% içinde:  %{metrics['accuracy_within_20_pct']:.1f}
  └─ ±30% içinde:  %{metrics['accuracy_within_30_pct']:.1f}

Sistematik Hata (Bias):
  ├─ Mutlak:       {metrics['bias']:,.0f} TL
  └─ Yüzde:        %{metrics['bias_percentage']:+.2f}
     {'└─ Model FAZLA tahmin ediyor' if metrics['bias'] > 0 else '└─ Model AZ tahmin ediyor' if metrics['bias'] < 0 else '└─ Dengeli'}

═══════════════════════════════════════════════════════════════
3. İŞ ETKİSİ ANALİZİ
═══════════════════════════════════════════════════════════════

Fazla Tahmin (Overestimation):
  ├─ Proje Sayısı:     {business['overestimation_count']}
  ├─ Toplam Fark:      {business['overestimation_total']:,.0f} TL
  └─ Ortalama Fark:    {business['overestimation_avg']:,.0f} TL

Az Tahmin (Underestimation):
  ├─ Proje Sayısı:     {business['underestimation_count']}
  ├─ Toplam Fark:      {business['underestimation_total']:,.0f} TL
  └─ Ortalama Fark:    {business['underestimation_avg']:,.0f} TL

Kritik Hatalar (>%30):
  ├─ Proje Sayısı:     {business['critical_error_count']}
  └─ Oran:             %{business['critical_error_rate']:.1f}

Toplam Finansal Etki:  {business['total_financial_impact']:,.0f} TL
Ortalama Etki/Proje:   {business['avg_financial_impact']:,.0f} TL

═══════════════════════════════════════════════════════════════
4. SONUÇ ve ÖNERİLER
═══════════════════════════════════════════════════════════════
"""
        
        # Değerlendirme
        if metrics['r2_score'] >= 0.85 and metrics['mape'] <= 20:
            report += "\n✅ MÜKEMMEL: Model production'a hazır!\n"
        elif metrics['r2_score'] >= 0.70 and metrics['mape'] <= 30:
            report += "\n⚠️  İYİ: Model kullanılabilir, iyileştirme yapılabilir.\n"
        else:
            report += "\n❌ ZAYIF: Model yeniden eğitilmeli!\n"
        
        # Öneriler
        report += "\nÖneriler:\n"
        
        if metrics['mape'] > 20:
            report += "  • MAPE yüksek - Daha fazla veri toplayın\n"
            report += "  • Feature engineering yapın\n"
        
        if business['critical_error_rate'] > 10:
            report += f"  • Kritik hata oranı yüksek (%{business['critical_error_rate']:.1f})\n"
            report += "  • Outlier'ları inceleyin\n"
        
        if abs(metrics['bias_percentage']) > 5:
            report += f"  • Sistematik hata var (%{metrics['bias_percentage']:+.2f})\n"
            report += "  • Model kalibrasyonu yapın\n"
        
        report += "\n═══════════════════════════════════════════════════════════════\n"
        
        if save_path:
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(report)
        
        return report
    
    @staticmethod
    def acceptance_criteria_check(metrics: Dict) -> Dict:
        """
        Kabul kriterleri kontrolü
        
        Production'a geçiş için minimum kriterler
        
        Args:
            metrics: calculate_metrics çıktısı
        
        Returns:
            dict: Kriter kontrolü
        """
        criteria = {
            'r2_score_min_0.85': {
                'value': metrics['r2_score'],
                'threshold': 0.85,
                'passed': metrics['r2_score'] >= 0.85,
                'importance': 'CRITICAL'
            },
            'mape_max_20': {
                'value': metrics['mape'],
                'threshold': 20,
                'passed': metrics['mape'] <= 20,
                'importance': 'CRITICAL'
            },
            'accuracy_within_20_pct_min_70': {
                'value': metrics['accuracy_within_20_pct'],
                'threshold': 70,
                'passed': metrics['accuracy_within_20_pct'] >= 70,
                'importance': 'HIGH'
            },
            'bias_max_5_pct': {
                'value': abs(metrics['bias_percentage']),
                'threshold': 5,
                'passed': abs(metrics['bias_percentage']) <= 5,
                'importance': 'MEDIUM'
            },
            'min_samples_50': {
                'value': metrics['n_samples'],
                'threshold': 50,
                'passed': metrics['n_samples'] >= 50,
                'importance': 'CRITICAL'
            }
        }
        
        critical_passed = all(
            c['passed'] for c in criteria.values() 
            if c['importance'] == 'CRITICAL'
        )
        
        all_passed = all(c['passed'] for c in criteria.values())
        
        return {
            'criteria': criteria,
            'critical_passed': critical_passed,
            'all_passed': all_passed,
            'ready_for_production': critical_passed
        }
