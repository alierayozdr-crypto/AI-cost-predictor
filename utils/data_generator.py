import numpy as np

class CostDataGenerator:
    """
    Gerçekçi maliyet verileri üretir.
    Eğitim ve test için sentetik veri seti oluşturur.
    """
    
    @staticmethod
    def generate_project_cost_data(n_samples=1000, random_state=42):
        """
        Proje maliyet tahmini için veri üret
        
        Özellikler:
        - Proje süresi (ay)
        - Ekip büyüklüğü (kişi)
        - Karmaşıklık skoru (1-10)
        - Teknoloji maliyeti (TL)
        - Lokasyon faktörü (1-3)
        - Deneyim seviyesi (1-5)
        - Risk faktörü (0-1)
        
        Hedef: Toplam proje maliyeti (TL)
        
        Args:
            n_samples: Üretilecek örnek sayısı
            random_state: Rastgelelik tohumu
        
        Returns:
            X: Özellikler (n_samples, n_features)
            y: Hedef değişken (n_samples, 1)
            feature_names: Özellik isimleri
        """
        np.random.seed(random_state)
        
        project_duration = np.random.uniform(1, 36, n_samples)
        team_size = np.random.randint(2, 50, n_samples)
        complexity = np.random.uniform(1, 10, n_samples)
        tech_cost = np.random.uniform(10000, 500000, n_samples)
        location_factor = np.random.uniform(1, 3, n_samples)
        experience_level = np.random.uniform(1, 5, n_samples)
        risk_factor = np.random.uniform(0, 1, n_samples)
        
        base_cost = (
            project_duration * 50000 +
            team_size * 15000 * project_duration +
            complexity * 30000 +
            tech_cost * 1.2 +
            location_factor * 100000
        )
        
        experience_discount = 1 - (experience_level / 10)
        risk_premium = 1 + (risk_factor * 0.5)
        
        total_cost = base_cost * experience_discount * risk_premium
        
        noise = np.random.normal(0, total_cost * 0.05, n_samples)
        total_cost += noise
        
        X = np.column_stack([
            project_duration,
            team_size,
            complexity,
            tech_cost,
            location_factor,
            experience_level,
            risk_factor
        ])
        
        y = total_cost.reshape(-1, 1)
        
        feature_names = [
            'Proje Süresi (ay)',
            'Ekip Büyüklüğü',
            'Karmaşıklık Skoru',
            'Teknoloji Maliyeti (TL)',
            'Lokasyon Faktörü',
            'Deneyim Seviyesi',
            'Risk Faktörü'
        ]
        
        return X, y, feature_names
    
    @staticmethod
    def generate_manufacturing_cost_data(n_samples=1000, random_state=42):
        """
        Üretim maliyet tahmini için veri üret
        
        Özellikler:
        - Üretim miktarı (adet)
        - Hammadde maliyeti (TL/adet)
        - İşçilik saati (saat)
        - Makine saati (saat)
        - Kalite kontrol seviyesi (1-5)
        - Enerji maliyeti (TL/saat)
        
        Hedef: Toplam üretim maliyeti (TL)
        """
        np.random.seed(random_state)
        
        quantity = np.random.randint(100, 10000, n_samples)
        material_cost = np.random.uniform(5, 200, n_samples)
        labor_hours = np.random.uniform(0.5, 10, n_samples)
        machine_hours = np.random.uniform(0.2, 5, n_samples)
        quality_level = np.random.uniform(1, 5, n_samples)
        energy_cost = np.random.uniform(10, 50, n_samples)
        
        fixed_cost = 50000
        
        variable_cost = (
            material_cost * quantity +
            labor_hours * quantity * 150 +
            machine_hours * quantity * energy_cost +
            quality_level * 1000
        )
        
        economies_of_scale = 1 - (np.log(quantity) / 20)
        economies_of_scale = np.clip(economies_of_scale, 0.7, 1.0)
        
        total_cost = fixed_cost + (variable_cost * economies_of_scale)
        
        noise = np.random.normal(0, total_cost * 0.03, n_samples)
        total_cost += noise
        
        X = np.column_stack([
            quantity,
            material_cost,
            labor_hours,
            machine_hours,
            quality_level,
            energy_cost
        ])
        
        y = total_cost.reshape(-1, 1)
        
        feature_names = [
            'Üretim Miktarı',
            'Hammadde Maliyeti (TL/adet)',
            'İşçilik Saati',
            'Makine Saati',
            'Kalite Kontrol Seviyesi',
            'Enerji Maliyeti (TL/saat)'
        ]
        
        return X, y, feature_names
    
    @staticmethod
    def generate_investment_analysis_data(n_samples=500, random_state=42):
        """
        Yatırım analizi için veri üret
        
        Özellikler:
        - İlk yatırım (TL)
        - Yıllık gelir (TL)
        - İşletme maliyeti (TL/yıl)
        - Proje ömrü (yıl)
        - İskonto oranı (%)
        - Risk skoru (1-10)
        
        Hedef: NPV (Net Present Value)
        """
        np.random.seed(random_state)
        
        initial_investment = np.random.uniform(100000, 5000000, n_samples)
        annual_revenue = np.random.uniform(50000, 2000000, n_samples)
        operating_cost = np.random.uniform(20000, 800000, n_samples)
        project_life = np.random.randint(3, 20, n_samples)
        discount_rate = np.random.uniform(0.05, 0.20, n_samples)
        risk_score = np.random.uniform(1, 10, n_samples)
        
        npv_values = []
        for i in range(n_samples):
            cash_flows = [-initial_investment[i]]
            for year in range(int(project_life[i])):
                net_cash_flow = annual_revenue[i] - operating_cost[i]
                cash_flows.append(net_cash_flow)
            
            npv = 0
            for t, cf in enumerate(cash_flows):
                npv += cf / ((1 + discount_rate[i]) ** t)
            
            risk_adjustment = 1 - (risk_score[i] / 20)
            npv *= risk_adjustment
            
            npv_values.append(npv)
        
        X = np.column_stack([
            initial_investment,
            annual_revenue,
            operating_cost,
            project_life,
            discount_rate,
            risk_score
        ])
        
        y = np.array(npv_values).reshape(-1, 1)
        
        feature_names = [
            'İlk Yatırım (TL)',
            'Yıllık Gelir (TL)',
            'İşletme Maliyeti (TL/yıl)',
            'Proje Ömrü (yıl)',
            'İskonto Oranı',
            'Risk Skoru'
        ]
        
        return X, y, feature_names
