import numpy as np
from .engineering_economics import EngineeringEconomics

class SensitivityAnalysis:
    """
    Duyarlılık Analizi ve Monte Carlo Simülasyonu
    
    "What-If" senaryoları ve risk analizi için kullanılır.
    Yöneticilerin farklı koşullarda projenin nasıl performans göstereceğini
    görmesini sağlar.
    """
    
    @staticmethod
    def monte_carlo_simulation(base_cost, volatility=0.15, n_simulations=10000):
        """
        Monte Carlo Simülasyonu ile maliyet dağılımını hesapla
        
        Args:
            base_cost: Temel maliyet tahmini
            volatility: Volatilite (standart sapma oranı)
            n_simulations: Simülasyon sayısı
        
        Returns:
            dict: Simülasyon sonuçları (min, max, mean, percentiles)
        """
        simulated_costs = np.random.normal(
            loc=base_cost,
            scale=base_cost * volatility,
            size=n_simulations
        )
        
        simulated_costs = np.maximum(simulated_costs, base_cost * 0.5)
        
        return {
            'simulations': simulated_costs,
            'mean': np.mean(simulated_costs),
            'std': np.std(simulated_costs),
            'min': np.min(simulated_costs),
            'max': np.max(simulated_costs),
            'p10': np.percentile(simulated_costs, 10),
            'p25': np.percentile(simulated_costs, 25),
            'p50': np.percentile(simulated_costs, 50),
            'p75': np.percentile(simulated_costs, 75),
            'p90': np.percentile(simulated_costs, 90),
            'confidence_95_lower': np.percentile(simulated_costs, 2.5),
            'confidence_95_upper': np.percentile(simulated_costs, 97.5)
        }
    
    @staticmethod
    def scenario_analysis(base_cost, scenarios=None):
        """
        Senaryo Analizi: İyimser, Beklenen, Kötümser
        
        Args:
            base_cost: Temel maliyet tahmini
            scenarios: Özel senaryolar (dict)
        
        Returns:
            dict: Senaryo sonuçları
        """
        if scenarios is None:
            scenarios = {
                'pessimistic': {'multiplier': 1.30, 'probability': 0.20},
                'expected': {'multiplier': 1.00, 'probability': 0.60},
                'optimistic': {'multiplier': 0.85, 'probability': 0.20}
            }
        
        if scenarios is not None:
            total_prob = sum(s.get('probability', 0) for s in scenarios.values())
            if abs(total_prob - 1.0) > 0.01:
                # olasılıkları normalize et
                for key in scenarios:
                    scenarios[key]['probability'] = scenarios[key]['probability'] / total_prob
        
        results = {}
        for scenario_name, params in scenarios.items():
            results[scenario_name] = {
                'cost': base_cost * params['multiplier'],
                'probability': params['probability'],
                'multiplier': params['multiplier']
            }
        
        expected_value = sum(
            result['cost'] * result['probability'] 
            for result in results.values()
        )
        results['expected_value'] = expected_value
        
        return results
    
    @staticmethod
    def sensitivity_to_parameter(model, preprocessor, base_input, 
                                  parameter_index, parameter_name,
                                  variation_range=(-0.3, 0.3), n_points=20):
        """
        Tek bir parametrenin değişimine karşı duyarlılık analizi
        
        Args:
            model: Eğitilmiş model
            preprocessor: Veri ön işleyici
            base_input: Temel girdi değerleri
            parameter_index: Değiştirilecek parametrenin indeksi
            parameter_name: Parametre adı
            variation_range: Değişim aralığı (örn: -30% ile +30%)
            n_points: Analiz noktası sayısı
        
        Returns:
            dict: Duyarlılık analizi sonuçları
        """
        base_value = base_input[0, parameter_index]
        variations = np.linspace(
            base_value * (1 + variation_range[0]),
            base_value * (1 + variation_range[1]),
            n_points
        )
        
        costs = []
        for variation in variations:
            modified_input = base_input.copy()
            modified_input[0, parameter_index] = variation
            
            normalized_input = preprocessor.normalize(modified_input, fit=False)
            prediction_norm = model.predict(normalized_input)
            prediction = preprocessor.denormalize(prediction_norm, is_target=True)
            
            costs.append(prediction[0, 0])
        
        base_input_norm = preprocessor.normalize(base_input, fit=False)
        base_prediction_norm = model.predict(base_input_norm)
        base_cost = preprocessor.denormalize(base_prediction_norm, is_target=True)[0, 0]
        
        elasticity = []
        for i, (var, cost) in enumerate(zip(variations, costs)):
            pct_change_param = ((var - base_value) / base_value) * 100
            pct_change_cost = ((cost - base_cost) / base_cost) * 100
            
            if pct_change_param != 0:
                elasticity.append(pct_change_cost / pct_change_param)
            else:
                elasticity.append(0)
        
        return {
            'parameter_name': parameter_name,
            'base_value': base_value,
            'variations': variations,
            'costs': np.array(costs),
            'base_cost': base_cost,
            'elasticity': np.mean(elasticity),
            'cost_range': (np.min(costs), np.max(costs)),
            'cost_change_pct': ((np.max(costs) - np.min(costs)) / base_cost) * 100
        }
    
    @staticmethod
    def tornado_chart_data(model, preprocessor, base_input, feature_names):
        """
        Tornado Chart için tüm parametrelerin duyarlılık verilerini hesapla
        
        Args:
            model: Eğitilmiş model
            preprocessor: Veri ön işleyici
            base_input: Temel girdi değerleri
            feature_names: Özellik isimleri
        
        Returns:
            list: Her parametre için duyarlılık verileri
        """
        results = []
        
        for i, feature_name in enumerate(feature_names):
            sensitivity = SensitivityAnalysis.sensitivity_to_parameter(
                model, preprocessor, base_input, i, feature_name,
                variation_range=(-0.2, 0.2), n_points=10
            )
            
            results.append({
                'feature': feature_name,
                'impact': sensitivity['cost_change_pct'],
                'elasticity': sensitivity['elasticity'],
                'cost_range': sensitivity['cost_range']
            })
        
        results.sort(key=lambda x: abs(x['impact']), reverse=True)
        
        return results
    
    @staticmethod
    def npv_sensitivity(initial_investment, annual_revenue, operating_cost,
                       project_life, base_discount_rate, discount_rate_range=(-0.05, 0.05)):
        """
        NPV'nin iskonto oranına duyarlılığını analiz et
        
        Args:
            initial_investment: İlk yatırım
            annual_revenue: Yıllık gelir
            operating_cost: İşletme maliyeti
            project_life: Proje ömrü
            base_discount_rate: Temel iskonto oranı
            discount_rate_range: İskonto oranı değişim aralığı
        
        Returns:
            dict: NPV duyarlılık analizi
        """
        discount_rates = np.linspace(
            base_discount_rate + discount_rate_range[0],
            base_discount_rate + discount_rate_range[1],
            20
        )
        
        npvs = []
        for rate in discount_rates:
            cash_flows = [-initial_investment]
            for _ in range(int(project_life)):
                net_cash_flow = annual_revenue - operating_cost
                cash_flows.append(net_cash_flow)
            
            npv = EngineeringEconomics.npv(cash_flows, rate)
            npvs.append(npv)
        
        base_cash_flows = [-initial_investment]
        for _ in range(int(project_life)):
            base_cash_flows.append(annual_revenue - operating_cost)
        base_npv = EngineeringEconomics.npv(base_cash_flows, base_discount_rate)
        
        break_even_rate = None
        for rate, npv in zip(discount_rates, npvs):
            if npv <= 0:
                break_even_rate = rate
                break
        
        return {
            'discount_rates': discount_rates,
            'npvs': np.array(npvs),
            'base_discount_rate': base_discount_rate,
            'base_npv': base_npv,
            'break_even_rate': break_even_rate,
            'npv_range': (np.min(npvs), np.max(npvs))
        }
    
    @staticmethod
    def risk_assessment(predicted_cost, expected_revenue, confidence_level=0.95,
                       project_duration_months=12, growth_rate=0.0):
        """
        Risk değerlendirmesi ve karlılık olasılığı
        
        UYARI: Bu basit statik analiz. Gerçekçi analiz için
        financial_modeling.py kullanın!
        
        Args:
            predicted_cost: Tahmin edilen maliyet (tek seferlik)
            expected_revenue: Beklenen gelir (toplam veya yıllık)
            confidence_level: Güven seviyesi
            project_duration_months: Proje süresi (ay)
            growth_rate: Aylık büyüme oranı
        
        Returns:
            dict: Risk değerlendirmesi
        """
        # Büyüme ile gelir projeksiyonu
        if growth_rate > 0 and project_duration_months > 1:
            # Dinamik gelir hesabı
            monthly_revenue = expected_revenue / project_duration_months
            total_projected_revenue = 0
            for month in range(project_duration_months):
                total_projected_revenue += monthly_revenue * ((1 + growth_rate) ** month)
            expected_revenue = total_projected_revenue
        
        profit = expected_revenue - predicted_cost
        profit_margin = (profit / expected_revenue) * 100 if expected_revenue > 0 else 0
        
        cost_volatility = 0.15
        revenue_volatility = 0.20
        
        n_sims = 10000
        simulated_costs = np.random.normal(predicted_cost, predicted_cost * cost_volatility, n_sims)
        
        # Büyüme ile gelir simülasyonu
        simulated_revenues = []
        for _ in range(n_sims):
            if growth_rate > 0 and project_duration_months > 1:
                first_month_revenue = expected_revenue / sum(
                    (1 + growth_rate) ** m for m in range(project_duration_months)
                )
                total_rev = 0
                for month in range(project_duration_months):
                    month_rev = first_month_revenue * ((1 + growth_rate) ** month)
                    month_rev *= np.random.normal(1.0, revenue_volatility)
                    total_rev += month_rev
                simulated_revenues.append(max(0, total_rev))
            else:
                simulated_revenues.append(max(0, np.random.normal(expected_revenue, expected_revenue * revenue_volatility)))
        
        simulated_revenues = np.array(simulated_revenues)
        simulated_profits = simulated_revenues - simulated_costs
        probability_of_profit = np.sum(simulated_profits > 0) / n_sims
        
        var = np.percentile(simulated_profits, (1 - confidence_level) * 100)
        
        return {
            'expected_profit': profit,
            'profit_margin_pct': profit_margin,
            'probability_of_profit': probability_of_profit,
            'value_at_risk': var,
            'risk_level': 'Düşük' if probability_of_profit > 0.8 else 'Orta' if probability_of_profit > 0.6 else 'Yüksek',
            'recommendation': 'Onaylanabilir' if probability_of_profit > 0.7 else 'Dikkatli İnceleme Gerekli' if probability_of_profit > 0.5 else 'Yüksek Risk'
        }
