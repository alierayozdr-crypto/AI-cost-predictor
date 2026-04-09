import numpy as np

class EngineeringEconomics:
    """
    Endüstri Mühendisliği - Mühendislik Ekonomisi Hesaplamaları
    
    Bu modül, finansal analiz ve maliyet optimizasyonu için
    endüstri mühendisliği prensiplerini içerir.
    """
    
    @staticmethod
    def npv(cash_flows, discount_rate):
        """
        Net Present Value (Net Bugünkü Değer)
        
        NPV = Σ [CF_t / (1 + r)^t]
        
        Gelecekteki nakit akışlarının bugünkü değerini hesaplar.
        NPV > 0 ise yatırım karlıdır.
        
        Args:
            cash_flows: Nakit akışları dizisi [CF_0, CF_1, ..., CF_n]
            discount_rate: İskonto oranı (örn: 0.10 = %10)
        
        Returns:
            npv: Net bugünkü değer
        """
        npv = 0
        for t, cf in enumerate(cash_flows):
            npv += cf / ((1 + discount_rate) ** t)
        return npv
    
    @staticmethod
    def irr(cash_flows, max_iterations=1000, tolerance=1e-6):
        """
        Internal Rate of Return (İç Verim Oranı)
        
        NPV = 0 olduğu iskonto oranını bulur.
        Newton-Raphson yöntemi ile iteratif olarak hesaplanır.
        Birden fazla başlangıç noktası deneyerek yakınsama garantisi sağlar.
        
        Args:
            cash_flows: Nakit akışları
            max_iterations: Maksimum iterasyon sayısı
            tolerance: Yakınsama toleransı
        
        Returns:
            irr: İç verim oranı veya None (yakınsamazsa)
        """
        start_rates = [-0.5, -0.1, 0.0, 0.1, 0.2, 0.5, 1.0]
        
        for start_rate in start_rates:
            rate = start_rate
            converged = False
            
            for _ in range(max_iterations):
                npv = EngineeringEconomics.npv(cash_flows, rate)
                
                if abs(npv) < tolerance:
                    converged = True
                    break
                
                npv_derivative = 0
                for t, cf in enumerate(cash_flows):
                    if t > 0:
                        npv_derivative -= t * cf / ((1 + rate) ** (t + 1))
                
                if abs(npv_derivative) < 1e-10:
                    break
                
                rate = rate - npv / npv_derivative
                
                # Sınır kontrolü
                if rate < -0.99 or rate > 10:
                    break
            
            if converged:
                return rate
        
        # Hiçbir başlangıç noktası yakınsamadı
        return None
    
    @staticmethod
    def payback_period(cash_flows):
        """
        Geri Ödeme Süresi
        
        İlk yatırımın ne kadar sürede geri döneceğini hesaplar.
        
        Args:
            cash_flows: Nakit akışları (ilk değer negatif olmalı)
        
        Returns:
            payback_period: Geri ödeme süresi (yıl)
        """
        cumulative = 0
        for t, cf in enumerate(cash_flows):
            cumulative += cf
            if cumulative >= 0:
                return t
        return len(cash_flows)
    
    @staticmethod
    def depreciation_straight_line(initial_cost, salvage_value, useful_life):
        """
        Doğrusal Amortisman (Straight-Line Depreciation)
        
        D = (P - S) / n
        
        Args:
            initial_cost: İlk maliyet (P)
            salvage_value: Hurda değeri (S)
            useful_life: Faydalı ömür (n)
        
        Returns:
            annual_depreciation: Yıllık amortisman
        """
        return (initial_cost - salvage_value) / useful_life
    
    @staticmethod
    def depreciation_declining_balance(initial_cost, rate, year):
        """
        Azalan Bakiye Amortismanı (Declining Balance)
        
        D_t = P * (1 - r)^(t-1) * r
        
        Args:
            initial_cost: İlk maliyet
            rate: Amortisman oranı
            year: Yıl
        
        Returns:
            depreciation: O yıl için amortisman
        """
        return initial_cost * ((1 - rate) ** (year - 1)) * rate
    
    @staticmethod
    def break_even_analysis(fixed_costs, variable_cost_per_unit, price_per_unit):
        """
        Başabaş Noktası Analizi (Break-Even Analysis)
        
        BEP = FC / (P - VC)
        
        Args:
            fixed_costs: Sabit maliyetler
            variable_cost_per_unit: Birim değişken maliyet
            price_per_unit: Birim satış fiyatı
        
        Returns:
            break_even_quantity: Başabaş noktası (adet)
        """
        if price_per_unit <= variable_cost_per_unit:
            return float('inf')
        
        return fixed_costs / (price_per_unit - variable_cost_per_unit)
    
    @staticmethod
    def roi(gain, cost):
        """
        Return on Investment (Yatırım Getirisi)
        
        ROI = (Kazanç - Maliyet) / Maliyet * 100
        
        Args:
            gain: Kazanç
            cost: Maliyet
        
        Returns:
            roi: Yatırım getirisi (%)
        """
        return ((gain - cost) / cost) * 100
    
    @staticmethod
    def economic_order_quantity(annual_demand, ordering_cost, holding_cost):
        """
        Ekonomik Sipariş Miktarı (EOQ)
        
        EOQ = √(2 * D * S / H)
        
        Envanter maliyetlerini minimize eden sipariş miktarı.
        
        Args:
            annual_demand: Yıllık talep (D)
            ordering_cost: Sipariş maliyeti (S)
            holding_cost: Elde tutma maliyeti (H)
        
        Returns:
            eoq: Ekonomik sipariş miktarı
        """
        return np.sqrt((2 * annual_demand * ordering_cost) / holding_cost)
    
    @staticmethod
    def future_value(present_value, interest_rate, periods):
        """
        Gelecek Değer (Future Value)
        
        FV = PV * (1 + r)^n
        
        Args:
            present_value: Bugünkü değer
            interest_rate: Faiz oranı
            periods: Dönem sayısı
        
        Returns:
            future_value: Gelecek değer
        """
        return present_value * ((1 + interest_rate) ** periods)
    
    @staticmethod
    def present_value(future_value, interest_rate, periods):
        """
        Bugünkü Değer (Present Value)
        
        PV = FV / (1 + r)^n
        
        Args:
            future_value: Gelecek değer
            interest_rate: Faiz oranı
            periods: Dönem sayısı
        
        Returns:
            present_value: Bugünkü değer
        """
        return future_value / ((1 + interest_rate) ** periods)
    
    @staticmethod
    def annuity_present_value(payment, interest_rate, periods):
        """
        Anüite Bugünkü Değeri
        
        PV = PMT * [(1 - (1 + r)^-n) / r]
        
        Args:
            payment: Dönemsel ödeme
            interest_rate: Faiz oranı
            periods: Dönem sayısı
        
        Returns:
            pv: Bugünkü değer
        """
        if interest_rate == 0:
            return payment * periods
        
        return payment * ((1 - (1 + interest_rate) ** -periods) / interest_rate)
