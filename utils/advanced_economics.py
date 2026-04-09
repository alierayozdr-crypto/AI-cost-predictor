import numpy as np
from .engineering_economics import EngineeringEconomics

class AdvancedEconomics:
    """
    İleri Seviye Mühendislik Ekonomisi
    
    Enflasyon, vergi, amortisman ve vergi sonrası nakit akışı hesaplamaları.
    Gerçek dünya finansal simülasyonu.
    """
    
    @staticmethod
    def inflation_adjusted_npv(cash_flows, discount_rate, inflation_rate):
        """
        Enflasyon ayarlı NPV hesabı
        
        Gerçek iskonto oranı = (1 + nominal_rate) / (1 + inflation_rate) - 1
        
        Args:
            cash_flows: Nakit akışları
            discount_rate: Nominal iskonto oranı
            inflation_rate: Enflasyon oranı
        
        Returns:
            dict: Nominal ve reel NPV değerleri
        """
        real_discount_rate = ((1 + discount_rate) / (1 + inflation_rate)) - 1
        
        nominal_npv = EngineeringEconomics.npv(cash_flows, discount_rate)
        
        real_cash_flows = [cash_flows[0]]
        for t in range(1, len(cash_flows)):
            real_cf = cash_flows[t] / ((1 + inflation_rate) ** t)
            real_cash_flows.append(real_cf)
        
        real_npv = EngineeringEconomics.npv(real_cash_flows, real_discount_rate)
        
        return {
            'nominal_npv': nominal_npv,
            'real_npv': real_npv,
            'real_discount_rate': real_discount_rate,
            'inflation_impact': nominal_npv - real_npv
        }
    
    @staticmethod
    def after_tax_cash_flow(revenue, operating_cost, depreciation, tax_rate):
        """
        Vergi sonrası nakit akışı hesabı
        
        ATCF = (Revenue - OpCost - Depreciation) × (1 - tax_rate) + Depreciation
        
        Args:
            revenue: Gelir
            operating_cost: İşletme maliyeti
            depreciation: Amortisman
            tax_rate: Vergi oranı (örn: 0.20 = %20)
        
        Returns:
            dict: Vergi öncesi ve sonrası nakit akışları
        """
        taxable_income = revenue - operating_cost - depreciation
        
        tax = max(0, taxable_income * tax_rate)
        
        net_income = taxable_income - tax
        
        after_tax_cf = net_income + depreciation
        
        before_tax_cf = revenue - operating_cost
        
        return {
            'before_tax_cash_flow': before_tax_cf,
            'taxable_income': taxable_income,
            'tax': tax,
            'net_income': net_income,
            'after_tax_cash_flow': after_tax_cf,
            'tax_shield': depreciation * tax_rate
        }
    
    @staticmethod
    def depreciation_vuk(initial_cost, asset_type='genel'):
        """
        Türkiye VUK amortisman oranları
        Kaynak: Vergi Usul Kanunu Genel Tebliği
        
        Args:
            initial_cost: İlk maliyet
            asset_type: Varlık türü
        
        Returns:
            dict: Amortisman detayları
        """
        vuk_rates = {
            'bina':          0.02,   # %2 — binalar
            'makine':        0.10,   # %10 — makine ve teçhizat
            'tasit':         0.20,   # %20 — taşıtlar
            'bilgisayar':    0.33,   # %33 — bilgisayar ve çevre birimleri
            'yazilim':       0.50,   # %50 — yazılım
            'mobilya':       0.10,   # %10 — demirbaşlar
            'genel':         0.10,   # %10 — genel varsayılan
        }
        rate = vuk_rates.get(asset_type, 0.10)
        years = int(1 / rate)
        annual_depreciation = initial_cost * rate
        return {
            'annual_depreciation': annual_depreciation,
            'useful_life_years': years,
            'rate': rate,
            'asset_type': asset_type,
            'schedule': [annual_depreciation] * years
        }
    
    @staticmethod
    def macrs_depreciation(initial_cost, recovery_period=5):
        """
        MACRS (Modified Accelerated Cost Recovery System) Amortisman
        
        # Not: MACRS ABD vergi sistemidir. Türkiye için depreciation_vuk() kullanın.
        
        ABD vergi sistemi amortisman yöntemi.
        Türkiye'de benzer hızlandırılmış amortisman uygulamaları var.
        
        Args:
            initial_cost: İlk maliyet
            recovery_period: İyileşme süresi (3, 5, 7, 10, 15, 20 yıl)
        
        Returns:
            list: Yıllık amortisman tutarları
        """
        macrs_rates = {
            3: [0.3333, 0.4445, 0.1481, 0.0741],
            5: [0.2000, 0.3200, 0.1920, 0.1152, 0.1152, 0.0576],
            7: [0.1429, 0.2449, 0.1749, 0.1249, 0.0893, 0.0892, 0.0893, 0.0446],
            10: [0.1000, 0.1800, 0.1440, 0.1152, 0.0922, 0.0737, 0.0655, 
                 0.0655, 0.0656, 0.0655, 0.0328],
            15: [0.0500, 0.0950, 0.0855, 0.0770, 0.0693, 0.0623, 0.0590,
                 0.0590, 0.0591, 0.0590, 0.0591, 0.0590, 0.0591, 0.0590,
                 0.0591, 0.0295],
            20: [0.03750, 0.07219, 0.06677, 0.06177, 0.05713, 0.05285,
                 0.04888, 0.04522, 0.04462, 0.04461, 0.04462, 0.04461,
                 0.04462, 0.04461, 0.04462, 0.04461, 0.04462, 0.04461,
                 0.04462, 0.04461, 0.02231]
        }
        
        if recovery_period not in macrs_rates:
            recovery_period = 5
        
        rates = macrs_rates[recovery_period]
        depreciation_schedule = [initial_cost * rate for rate in rates]
        
        return depreciation_schedule
    
    @staticmethod
    def declining_balance_depreciation(initial_cost, salvage_value, useful_life, rate=2):
        """
        Azalan Bakiye Amortismanı (Declining Balance)
        
        DDB (Double Declining Balance) için rate=2
        
        Args:
            initial_cost: İlk maliyet
            salvage_value: Hurda değeri
            useful_life: Faydalı ömür
            rate: Hızlandırma oranı (2 = DDB)
        
        Returns:
            list: Yıllık amortisman tutarları
        """
        depreciation_rate = rate / useful_life
        book_value = initial_cost
        depreciation_schedule = []
        
        for year in range(useful_life):
            depreciation = book_value * depreciation_rate
            
            if book_value - depreciation < salvage_value:
                depreciation = book_value - salvage_value
            
            depreciation_schedule.append(depreciation)
            book_value -= depreciation
            
            if book_value <= salvage_value:
                break
        
        while len(depreciation_schedule) < useful_life:
            depreciation_schedule.append(0)
        
        return depreciation_schedule
    
    @staticmethod
    def project_npv_with_taxes(initial_investment, annual_revenue, annual_operating_cost,
                               project_life, discount_rate, tax_rate, depreciation_method='straight_line',
                               salvage_value=0, inflation_rate=0):
        """
        Vergi ve amortisman dahil tam NPV analizi
        
        Args:
            initial_investment: İlk yatırım
            annual_revenue: Yıllık gelir
            annual_operating_cost: Yıllık işletme maliyeti
            project_life: Proje ömrü
            discount_rate: İskonto oranı
            tax_rate: Vergi oranı
            depreciation_method: 'straight_line', 'macrs', 'declining_balance'
            salvage_value: Hurda değeri
            inflation_rate: Enflasyon oranı
        
        Returns:
            dict: Detaylı finansal analiz
        """
        if depreciation_method == 'straight_line':
            annual_depreciation = EngineeringEconomics.depreciation_straight_line(
                initial_investment, salvage_value, project_life
            )
            depreciation_schedule = [annual_depreciation] * int(project_life)
        
        elif depreciation_method == 'macrs':
            depreciation_schedule = AdvancedEconomics.macrs_depreciation(
                initial_investment, recovery_period=min(int(project_life), 7)
            )
            while len(depreciation_schedule) < int(project_life):
                depreciation_schedule.append(0)
        
        elif depreciation_method == 'declining_balance':
            depreciation_schedule = AdvancedEconomics.declining_balance_depreciation(
                initial_investment, salvage_value, int(project_life)
            )
        
        else:
            annual_depreciation = initial_investment / project_life
            depreciation_schedule = [annual_depreciation] * int(project_life)
        
        cash_flows = [-initial_investment]
        after_tax_cash_flows = [-initial_investment]
        
        yearly_details = []
        
        for year in range(int(project_life)):
            inflated_revenue = annual_revenue * ((1 + inflation_rate) ** year)
            inflated_opcost = annual_operating_cost * ((1 + inflation_rate) ** year)
            
            depreciation = depreciation_schedule[year] if year < len(depreciation_schedule) else 0
            
            atcf_data = AdvancedEconomics.after_tax_cash_flow(
                inflated_revenue, inflated_opcost, depreciation, tax_rate
            )
            
            cash_flows.append(atcf_data['before_tax_cash_flow'])
            after_tax_cash_flows.append(atcf_data['after_tax_cash_flow'])
            
            yearly_details.append({
                'year': year + 1,
                'revenue': inflated_revenue,
                'operating_cost': inflated_opcost,
                'depreciation': depreciation,
                'taxable_income': atcf_data['taxable_income'],
                'tax': atcf_data['tax'],
                'after_tax_cash_flow': atcf_data['after_tax_cash_flow'],
                'tax_shield': atcf_data['tax_shield']
            })
        
        if salvage_value > 0:
            after_tax_cash_flows[-1] += salvage_value
        
        before_tax_npv = EngineeringEconomics.npv(cash_flows, discount_rate)
        after_tax_npv = EngineeringEconomics.npv(after_tax_cash_flows, discount_rate)
        
        after_tax_irr = EngineeringEconomics.irr(after_tax_cash_flows)
        if after_tax_irr is None:
            print("IRR hesaplanamadı — nakit akışları yakınsamaya uygun değil")
        
        total_tax_shield = sum(detail['tax_shield'] for detail in yearly_details)
        
        return {
            'before_tax_npv': before_tax_npv,
            'after_tax_npv': after_tax_npv,
            'after_tax_irr': after_tax_irr,
            'total_tax_paid': sum(detail['tax'] for detail in yearly_details),
            'total_tax_shield': total_tax_shield,
            'tax_benefit': total_tax_shield,
            'yearly_details': yearly_details,
            'depreciation_method': depreciation_method,
            'effective_tax_rate': (sum(detail['tax'] for detail in yearly_details) / 
                                  sum(detail['taxable_income'] for detail in yearly_details) 
                                  if sum(detail['taxable_income'] for detail in yearly_details) > 0 else 0)
        }
    
    @staticmethod
    def lease_vs_buy_analysis(purchase_price, lease_payment, lease_term,
                              discount_rate, tax_rate, depreciation_life,
                              salvage_value=0, maintenance_cost=0):
        """
        Kiralama vs Satın Alma Analizi
        
        Args:
            purchase_price: Satın alma fiyatı
            lease_payment: Yıllık kira ödemesi
            lease_term: Kira süresi
            discount_rate: İskonto oranı
            tax_rate: Vergi oranı
            depreciation_life: Amortisman süresi
            salvage_value: Hurda değeri
            maintenance_cost: Yıllık bakım maliyeti
        
        Returns:
            dict: Kiralama vs satın alma karşılaştırması
        """
        annual_depreciation = (purchase_price - salvage_value) / depreciation_life
        
        buy_cash_flows = [-purchase_price]
        for year in range(int(lease_term)):
            depreciation = annual_depreciation if year < depreciation_life else 0
            
            tax_shield = depreciation * tax_rate
            
            after_tax_maintenance = maintenance_cost * (1 - tax_rate)
            
            net_cf = tax_shield - after_tax_maintenance
            buy_cash_flows.append(net_cf)
        
        if salvage_value > 0:
            buy_cash_flows[-1] += salvage_value
        
        lease_cash_flows = [0]
        for year in range(int(lease_term)):
            after_tax_lease = lease_payment * (1 - tax_rate)
            lease_cash_flows.append(-after_tax_lease)
        
        buy_npv = EngineeringEconomics.npv(buy_cash_flows, discount_rate)
        lease_npv = EngineeringEconomics.npv(lease_cash_flows, discount_rate)
        
        return {
            'buy_npv': buy_npv,
            'lease_npv': lease_npv,
            'net_advantage_to_leasing': lease_npv - buy_npv,
            'recommendation': 'Satın Al' if buy_npv > lease_npv else 'Kirala',
            'buy_total_cost': purchase_price + (maintenance_cost * lease_term),
            'lease_total_cost': lease_payment * lease_term,
            'break_even_lease_payment': (buy_npv / lease_term) / (1 - tax_rate)
        }
    
    @staticmethod
    def working_capital_analysis(revenue, days_receivable, days_inventory, days_payable):
        """
        İşletme Sermayesi Analizi
        
        Args:
            revenue: Yıllık gelir
            days_receivable: Alacak tahsil süresi (gün)
            days_inventory: Envanter devir süresi (gün)
            days_payable: Borç ödeme süresi (gün)
        
        Returns:
            dict: İşletme sermayesi metrikleri
        """
        daily_revenue = revenue / 365
        
        accounts_receivable = daily_revenue * days_receivable
        inventory = daily_revenue * days_inventory
        accounts_payable = daily_revenue * days_payable
        
        working_capital = accounts_receivable + inventory - accounts_payable
        
        cash_conversion_cycle = days_receivable + days_inventory - days_payable
        
        return {
            'accounts_receivable': accounts_receivable,
            'inventory': inventory,
            'accounts_payable': accounts_payable,
            'working_capital': working_capital,
            'cash_conversion_cycle': cash_conversion_cycle,
            'working_capital_ratio': (working_capital / revenue) * 100,
            'recommendation': 'İyi' if cash_conversion_cycle < 60 else 'Orta' if cash_conversion_cycle < 90 else 'İyileştirme Gerekli'
        }
