import numpy as np

class ExplainableAI:
    """
    Açıklanabilir Yapay Zeka (Explainable AI - XAI)
    
    SHAP-benzeri özellik katkı analizi.
    Modelin neden bu tahmini yaptığını açıklar.
    """
    
    @staticmethod
    def calculate_feature_contributions(model, preprocessor, input_data, 
                                        feature_names, baseline=None):
        """
        Her özelliğin tahmine katkısını hesapla (SHAP-benzeri)
        
        Mantık:
        1. Baseline (ortalama) tahminini al
        2. Her özelliği tek tek değiştir
        3. Tahmin değişimini ölç
        4. Bu değişim = o özelliğin katkısı
        
        Args:
            model: Eğitilmiş model
            preprocessor: Veri ön işleyici
            input_data: Tahmin yapılacak veri (1, n_features)
            feature_names: Özellik isimleri
            baseline: Baseline değerler (None ise ortalama kullan)
        
        Returns:
            dict: Her özellik için katkı değerleri
        """
        if baseline is None:
            baseline = np.zeros_like(input_data)
            typical_values = {
                0: 12.0,   # proje süresi — 12 ay
                1: 10.0,   # ekip büyüklüğü — 10 kişi
                2: 5.0,    # karmaşıklık — orta
                3: 100000, # teknoloji maliyeti
                4: 2.0,    # lokasyon faktörü — orta
                5: 3.0,    # deneyim seviyesi — orta
                6: 0.3,    # risk faktörü — düşük-orta
            }
            for i in range(input_data.shape[1]):
                baseline[0, i] = typical_values.get(i, input_data[0, i])
        
        input_norm = preprocessor.normalize(input_data, fit=False)
        prediction_norm = model.predict(input_norm)
        base_prediction = preprocessor.denormalize(prediction_norm, is_target=True)[0, 0]
        
        baseline_norm = preprocessor.normalize(baseline, fit=False)
        baseline_pred_norm = model.predict(baseline_norm)
        baseline_prediction = preprocessor.denormalize(baseline_pred_norm, is_target=True)[0, 0]
        
        contributions = {}
        
        for i, feature_name in enumerate(feature_names):
            modified_input = baseline.copy()
            modified_input[0, i] = input_data[0, i]
            
            modified_norm = preprocessor.normalize(modified_input, fit=False)
            modified_pred_norm = model.predict(modified_norm)
            modified_prediction = preprocessor.denormalize(modified_pred_norm, is_target=True)[0, 0]
            
            contribution = modified_prediction - baseline_prediction
            
            contributions[feature_name] = {
                'contribution': contribution,
                'value': input_data[0, i],
                'percentage': (contribution / base_prediction * 100) if base_prediction != 0 else 0
            }
        
        total_contribution = sum(abs(c['contribution']) for c in contributions.values())
        for feature_name in contributions:
            if total_contribution > 0:
                contributions[feature_name]['importance'] = (
                    abs(contributions[feature_name]['contribution']) / total_contribution * 100
                )
            else:
                contributions[feature_name]['importance'] = 0
        
        return {
            'base_prediction': base_prediction,
            'baseline_prediction': baseline_prediction,
            'contributions': contributions
        }
    
    @staticmethod
    def generate_explanation_text(contributions_data, top_n=5):
        """
        İnsan tarafından okunabilir açıklama metni oluştur
        
        Args:
            contributions_data: calculate_feature_contributions çıktısı
            top_n: Kaç özellik gösterilsin
        
        Returns:
            str: Açıklama metni
        """
        contributions = contributions_data['contributions']
        base_prediction = contributions_data['base_prediction']
        
        sorted_features = sorted(
            contributions.items(),
            key=lambda x: abs(x[1]['contribution']),
            reverse=True
        )
        
        explanation = f"**Tahmini Maliyet: {base_prediction:,.0f} TL**\n\n"
        explanation += "### 🔍 Tahmin Açıklaması\n\n"
        
        positive_features = []
        negative_features = []
        
        for feature_name, data in sorted_features[:top_n]:
            if data['contribution'] > 0:
                positive_features.append((feature_name, data))
            else:
                negative_features.append((feature_name, data))
        
        if positive_features:
            explanation += "**📈 Maliyeti Artıran Faktörler:**\n\n"
            for feature_name, data in positive_features:
                explanation += f"- **{feature_name}**: +{data['contribution']:,.0f} TL "
                explanation += f"({data['percentage']:+.1f}%) - Değer: {data['value']:.2f}\n"
            explanation += "\n"
        
        if negative_features:
            explanation += "**📉 Maliyeti Azaltan Faktörler:**\n\n"
            for feature_name, data in negative_features:
                explanation += f"- **{feature_name}**: {data['contribution']:,.0f} TL "
                explanation += f"({data['percentage']:+.1f}%) - Değer: {data['value']:.2f}\n"
            explanation += "\n"
        
        explanation += "**💡 Önem Sıralaması:**\n\n"
        for i, (feature_name, data) in enumerate(sorted_features[:top_n], 1):
            explanation += f"{i}. {feature_name}: %{data['importance']:.1f}\n"
        
        return explanation
    
    @staticmethod
    def create_waterfall_data(contributions_data):
        """
        Waterfall chart için veri hazırla
        
        Args:
            contributions_data: calculate_feature_contributions çıktısı
        
        Returns:
            dict: Waterfall chart verileri
        """
        contributions = contributions_data['contributions']
        baseline = contributions_data['baseline_prediction']
        final = contributions_data['base_prediction']
        
        sorted_features = sorted(
            contributions.items(),
            key=lambda x: abs(x[1]['contribution']),
            reverse=True
        )
        
        waterfall_data = {
            'labels': ['Baseline'],
            'values': [baseline],
            'measures': ['absolute']
        }
        
        cumulative = baseline
        for feature_name, data in sorted_features:
            waterfall_data['labels'].append(feature_name)
            waterfall_data['values'].append(data['contribution'])
            waterfall_data['measures'].append('relative')
            cumulative += data['contribution']
        
        waterfall_data['labels'].append('Toplam Tahmin')
        waterfall_data['values'].append(final)
        waterfall_data['measures'].append('total')
        
        return waterfall_data
    
    @staticmethod
    def interaction_effects(model, preprocessor, input_data, 
                           feature_names, feature_idx1, feature_idx2):
        """
        İki özellik arasındaki etkileşim etkisini hesapla
        
        Args:
            model: Eğitilmiş model
            preprocessor: Veri ön işleyici
            input_data: Girdi verisi
            feature_names: Özellik isimleri
            feature_idx1: İlk özellik indeksi
            feature_idx2: İkinci özellik indeksi
        
        Returns:
            dict: Etkileşim analizi
        """
        baseline = input_data.copy()
        baseline[0, feature_idx1] = input_data[0, feature_idx1] * 0.9
        baseline[0, feature_idx2] = input_data[0, feature_idx2] * 0.9
        
        baseline_norm = preprocessor.normalize(baseline, fit=False)
        baseline_pred = preprocessor.denormalize(
            model.predict(baseline_norm), is_target=True
        )[0, 0]
        
        only_f1 = baseline.copy()
        only_f1[0, feature_idx1] = input_data[0, feature_idx1]
        only_f1_pred = preprocessor.denormalize(
            model.predict(preprocessor.normalize(only_f1, fit=False)), 
            is_target=True
        )[0, 0]
        
        only_f2 = baseline.copy()
        only_f2[0, feature_idx2] = input_data[0, feature_idx2]
        only_f2_pred = preprocessor.denormalize(
            model.predict(preprocessor.normalize(only_f2, fit=False)), 
            is_target=True
        )[0, 0]
        
        both = input_data.copy()
        both_pred = preprocessor.denormalize(
            model.predict(preprocessor.normalize(both, fit=False)), 
            is_target=True
        )[0, 0]
        
        individual_effect = (only_f1_pred - baseline_pred) + (only_f2_pred - baseline_pred)
        combined_effect = both_pred - baseline_pred
        interaction = combined_effect - individual_effect
        
        return {
            'feature1': feature_names[feature_idx1],
            'feature2': feature_names[feature_idx2],
            'individual_effect': individual_effect,
            'combined_effect': combined_effect,
            'interaction_effect': interaction,
            'synergy': 'Pozitif Sinerji' if interaction > 0 else 'Negatif Sinerji' if interaction < 0 else 'Bağımsız'
        }
    
    @staticmethod
    def counterfactual_explanation(model, preprocessor, input_data, 
                                   feature_names, target_cost, max_iterations=100):
        """
        Counterfactual açıklama: "X maliyete ulaşmak için ne değişmeli?"
        
        Args:
            model: Eğitilmiş model
            preprocessor: Veri ön işleyici
            input_data: Mevcut girdi
            feature_names: Özellik isimleri
            target_cost: Hedef maliyet
            max_iterations: Maksimum iterasyon
        
        Returns:
            dict: Önerilen değişiklikler
        """
        current_norm = preprocessor.normalize(input_data, fit=False)
        current_pred = preprocessor.denormalize(
            model.predict(current_norm), is_target=True
        )[0, 0]
        
        if abs(current_pred - target_cost) < target_cost * 0.01:
            return {
                'success': True,
                'message': 'Mevcut tahmin zaten hedefe çok yakın',
                'changes': {}
            }
        
        modified = input_data.copy()
        changes = {}
        
        for iteration in range(max_iterations):
            modified_norm = preprocessor.normalize(modified, fit=False)
            current_pred = preprocessor.denormalize(
                model.predict(modified_norm), is_target=True
            )[0, 0]
            
            if abs(current_pred - target_cost) < target_cost * 0.02:
                break
            
            sensitivities = []
            for i in range(input_data.shape[1]):
                test_input = modified.copy()
                delta = modified[0, i] * 0.01
                test_input[0, i] += delta
                
                test_norm = preprocessor.normalize(test_input, fit=False)
                test_pred = preprocessor.denormalize(
                    model.predict(test_norm), is_target=True
                )[0, 0]
                
                sensitivity = (test_pred - current_pred) / delta
                sensitivities.append((i, sensitivity))
            
            if current_pred > target_cost:
                best_feature = min(sensitivities, key=lambda x: x[1])
            else:
                best_feature = max(sensitivities, key=lambda x: x[1])
            
            feature_idx = best_feature[0]
            adjustment = (target_cost - current_pred) / (best_feature[1] + 1e-10) * 0.1
            
            modified[0, feature_idx] += adjustment
            modified[0, feature_idx] = np.clip(
                modified[0, feature_idx],
                input_data[0, feature_idx] * 0.5,
                input_data[0, feature_idx] * 1.5
            )
            
            change_pct = ((modified[0, feature_idx] - input_data[0, feature_idx]) / 
                         input_data[0, feature_idx] * 100)
            
            changes[feature_names[feature_idx]] = {
                'original': input_data[0, feature_idx],
                'suggested': modified[0, feature_idx],
                'change_pct': change_pct
            }
        
        final_norm = preprocessor.normalize(modified, fit=False)
        final_pred = preprocessor.denormalize(
            model.predict(final_norm), is_target=True
        )[0, 0]
        
        return {
            'success': abs(final_pred - target_cost) < target_cost * 0.05,
            'target_cost': target_cost,
            'achieved_cost': final_pred,
            'original_cost': preprocessor.denormalize(
                model.predict(preprocessor.normalize(input_data, fit=False)), 
                is_target=True
            )[0, 0],
            'changes': changes
        }
