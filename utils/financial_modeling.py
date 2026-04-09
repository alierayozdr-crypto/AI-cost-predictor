"""
Gerçekçi Finansal Modelleme
Büyüme, gelir akışları, dinamik ROI hesaplaması
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta

class FinancialModeling:
    """
    Kapsamlı finansal modelleme ve iş değerlendirmesi
    
    Senin örneğindeki gibi: Aylık gelir, büyüme, ROI, geri dönüş süresi
    """
    
    @staticmethod
    def calculate_dynamic_roi(
        initial_investment: float,
        monthly_revenues: List[float],
        monthly_costs: List[float],
        investor_share: float = 0.25,
        growth_rate: float = 0.03
    ) -> Dict:
        """
        Dinamik ROI hesabı - Büyüme dahil
        
        Args:
            initial_investment: İlk yatırım (₺)
            monthly_revenues: Aylık gelirler listesi
            monthly_costs: Aylık maliyetler listesi
            investor_share: Yatırımcı payı (0.25 = %25)
            growth_rate: Aylık büyüme oranı (0.03 = %3)
        
        Returns:
            dict: ROI analizi
        """
        months = len(monthly_revenues)
        
        # Büyüme ile gelir projeksiyonu
        projected_revenues = []
        for i, base_revenue in enumerate(monthly_revenues):
            projected = base_revenue * ((1 + growth_rate) ** i)
            projected_revenues.append(projected)
        
        # Net kâr hesabı
        monthly_profits = []
        for revenue, cost in zip(projected_revenues, monthly_costs):
            profit = revenue - cost
            monthly_profits.append(profit)
        
        # Kümülatif kâr
        cumulative_profit = np.cumsum(monthly_profits)
        
        # Yatırımcı payı
        investor_monthly_profit = [p * investor_share for p in monthly_profits]
        investor_cumulative = np.cumsum(investor_monthly_profit)
        
        # Geri dönüş süresi (payback period)
        payback_month = None
        for i, cum_profit in enumerate(investor_cumulative):
            if cum_profit >= initial_investment:
                payback_month = i + 1
                break
        
        # Toplam getiri
        total_investor_profit = sum(investor_monthly_profit)
        roi = (total_investor_profit / initial_investment) * 100 if initial_investment > 0 else 0
        
        # Yıllık getiri
        annual_roi = (roi / months) * 12 if months > 0 else 0
        
        return {
            'initial_investment': initial_investment,
            'total_revenue': sum(projected_revenues),
            'total_cost': sum(monthly_costs),
            'total_profit': sum(monthly_profits),
            'investor_share_pct': investor_share * 100,
            'investor_total_profit': total_investor_profit,
            'roi_percentage': roi,
            'annual_roi': annual_roi,
            'payback_months': payback_month,
            'payback_years': payback_month / 12 if payback_month else None,
            'monthly_revenues': projected_revenues,
            'monthly_profits': monthly_profits,
            'cumulative_profit': cumulative_profit.tolist(),
            'investor_cumulative': investor_cumulative.tolist(),
            'growth_rate': growth_rate,
            'profitable': total_investor_profit > initial_investment
        }
    
    @staticmethod
    def realistic_risk_assessment(
        initial_investment: float,
        monthly_revenues: List[float],
        monthly_costs: List[float],
        growth_rate: float = 0.03,
        growth_volatility: float = 0.02,
        revenue_volatility: float = 0.15,
        n_simulations: int = 10000
    ) -> Dict:
        """
        Gerçekçi risk değerlendirmesi - Monte Carlo ile
        
        Args:
            initial_investment: İlk yatırım
            monthly_revenues: Aylık gelirler
            monthly_costs: Aylık maliyetler
            growth_rate: Beklenen büyüme oranı
            growth_volatility: Büyüme belirsizliği
            revenue_volatility: Gelir belirsizliği
            n_simulations: Simülasyon sayısı
        
        Returns:
            dict: Risk analizi
        """
        months = len(monthly_revenues)
        
        # Monte Carlo simülasyonu
        final_profits = []
        payback_months_list = []
        
        for _ in range(n_simulations):
            # Rastgele büyüme oranı
            sim_growth = np.random.normal(growth_rate, growth_volatility)
            
            # Aylık gelir simülasyonu
            sim_revenues = []
            for i, base_revenue in enumerate(monthly_revenues):
                # Büyüme + rastgele volatilite
                growth_factor = (1 + sim_growth) ** i
                volatility_factor = np.random.normal(1.0, revenue_volatility)
                sim_revenue = base_revenue * growth_factor * volatility_factor
                sim_revenues.append(max(0, sim_revenue))
            
            # Maliyet simülasyonu (daha düşük volatilite)
            sim_costs = [c * np.random.normal(1.0, 0.10) for c in monthly_costs]
            
            # Kâr hesabı
            sim_profits = [r - c for r, c in zip(sim_revenues, sim_costs)]
            cumulative = np.cumsum(sim_profits)
            
            # Geri dönüş süresi
            payback = None
            for i, cum in enumerate(cumulative):
                if cum >= initial_investment:
                    payback = i + 1
                    break
            
            final_profits.append(cumulative[-1] if len(cumulative) > 0 else 0)
            if payback:
                payback_months_list.append(payback)
        
        final_profits = np.array(final_profits)
        
        # İstatistikler
        mean_profit = np.mean(final_profits)
        std_profit = np.std(final_profits)
        
        # Karlılık olasılığı
        prob_profitable = np.sum(final_profits > initial_investment) / n_simulations
        
        # Value at Risk (VaR) - %5 en kötü senaryo
        var_5 = np.percentile(final_profits, 5)
        
        # Beklenen getiri
        expected_roi = ((mean_profit - initial_investment) / initial_investment * 100) if initial_investment > 0 else 0
        
        # Geri dönüş süresi dağılımı
        avg_payback = np.mean(payback_months_list) if payback_months_list else None
        
        # Risk seviyesi
        if prob_profitable > 0.80 and expected_roi > 50:
            risk_level = 'Düşük'
        elif prob_profitable > 0.60 and expected_roi > 20:
            risk_level = 'Orta'
        else:
            risk_level = 'Yüksek'
        
        return {
            'probability_of_profit': prob_profitable,
            'expected_profit': mean_profit,
            'expected_roi': expected_roi,
            'profit_std': std_profit,
            'value_at_risk_5pct': var_5,
            'best_case': np.percentile(final_profits, 95),
            'worst_case': np.percentile(final_profits, 5),
            'median_profit': np.median(final_profits),
            'risk_level': risk_level,
            'avg_payback_months': avg_payback,
            'payback_probability': len(payback_months_list) / n_simulations,
            'recommendation': FinancialModeling._generate_recommendation(
                prob_profitable, expected_roi, risk_level
            )
        }
    
    @staticmethod
    def _generate_recommendation(prob_profit: float, roi: float, risk: str) -> str:
        """Yatırım önerisi oluştur"""
        if prob_profit > 0.80 and roi > 50:
            return "Güçlü Yatırım - Yüksek getiri ve düşük risk"
        elif prob_profit > 0.70 and roi > 30:
            return "İyi Yatırım - Kabul edilebilir risk/getiri oranı"
        elif prob_profit > 0.60 and roi > 15:
            return "Orta Yatırım - Dikkatli değerlendirme gerekli"
        else:
            return "Riskli Yatırım - Alternatif senaryolar değerlendirin"
    
    @staticmethod
    def business_case_evaluation(
        project_name: str,
        initial_investment: float,
        monthly_data: pd.DataFrame,
        investor_share: float = 0.25,
        growth_rate: float = 0.03,
        discount_rate: float = 0.10
    ) -> Dict:
        """
        Kapsamlı iş değerlendirmesi
        
        Args:
            project_name: Proje adı
            initial_investment: İlk yatırım
            monthly_data: DataFrame with 'revenue' and 'cost' columns
            investor_share: Yatırımcı payı
            growth_rate: Büyüme oranı
            discount_rate: İskonto oranı
        
        Returns:
            dict: Tam iş değerlendirmesi
        """
        monthly_revenues = monthly_data['revenue'].tolist()
        monthly_costs = monthly_data['cost'].tolist()
        
        # 1. Dinamik ROI
        roi_analysis = FinancialModeling.calculate_dynamic_roi(
            initial_investment, monthly_revenues, monthly_costs,
            investor_share, growth_rate
        )
        
        # 2. Risk analizi
        risk_analysis = FinancialModeling.realistic_risk_assessment(
            initial_investment, monthly_revenues, monthly_costs,
            growth_rate
        )
        
        # 3. NPV hesabı (büyüme dahil)
        npv_analysis = FinancialModeling.calculate_npv_with_growth(
            initial_investment, monthly_revenues, monthly_costs,
            growth_rate, discount_rate
        )
        
        # 4. Senaryo analizi
        scenarios = FinancialModeling.scenario_analysis(
            initial_investment, monthly_revenues, monthly_costs,
            investor_share
        )
        
        return {
            'project_name': project_name,
            'evaluation_date': datetime.now().isoformat(),
            'roi_analysis': roi_analysis,
            'risk_analysis': risk_analysis,
            'npv_analysis': npv_analysis,
            'scenarios': scenarios,
            'recommendation': FinancialModeling._final_recommendation(
                roi_analysis, risk_analysis, npv_analysis
            )
        }
    
    @staticmethod
    def calculate_npv_with_growth(
        initial_investment: float,
        monthly_revenues: List[float],
        monthly_costs: List[float],
        growth_rate: float,
        discount_rate: float
    ) -> Dict:
        """
        NPV hesabı - büyüme dahil
        
        Args:
            initial_investment: İlk yatırım
            monthly_revenues: Aylık gelirler
            monthly_costs: Aylık maliyetler
            growth_rate: Büyüme oranı
            discount_rate: İskonto oranı (yıllık)
        
        Returns:
            dict: NPV analizi
        """
        monthly_discount = (1 + discount_rate) ** (1/12) - 1
        
        cash_flows = [-initial_investment]
        discounted_flows = [-initial_investment]
        
        for i, (revenue, cost) in enumerate(zip(monthly_revenues, monthly_costs)):
            # Büyüme ile gelir
            projected_revenue = revenue * ((1 + growth_rate) ** i)
            net_flow = projected_revenue - cost
            
            # İskonto
            discount_factor = (1 + monthly_discount) ** (i + 1)
            discounted_flow = net_flow / discount_factor
            
            cash_flows.append(net_flow)
            discounted_flows.append(discounted_flow)
        
        npv = sum(discounted_flows)
        
        # IRR hesabı
        try:
            from numpy import irr as np_irr
            monthly_irr = np_irr(cash_flows)
            annual_irr = ((1 + monthly_irr) ** 12 - 1) * 100
        except:
            annual_irr = None
        
        return {
            'npv': npv,
            'total_cash_flows': sum(cash_flows),
            'discounted_cash_flows': sum(discounted_flows),
            'annual_irr': annual_irr,
            'npv_positive': npv > 0,
            'discount_rate': discount_rate
        }
    
    @staticmethod
    def scenario_analysis(
        initial_investment: float,
        monthly_revenues: List[float],
        monthly_costs: List[float],
        investor_share: float
    ) -> Dict:
        """
        Senaryo analizi: İyimser, Beklenen, Kötümser
        
        Args:
            initial_investment: İlk yatırım
            monthly_revenues: Aylık gelirler
            monthly_costs: Aylık maliyetler
            investor_share: Yatırımcı payı
        
        Returns:
            dict: 3 senaryo
        """
        scenarios = {}
        
        # İyimser: %5 büyüme
        optimistic = FinancialModeling.calculate_dynamic_roi(
            initial_investment, monthly_revenues, monthly_costs,
            investor_share, growth_rate=0.05
        )
        scenarios['optimistic'] = {
            'growth_rate': 0.05,
            'roi': optimistic['roi_percentage'],
            'payback_months': optimistic['payback_months'],
            'total_profit': optimistic['investor_total_profit']
        }
        
        # Beklenen: %3 büyüme
        expected = FinancialModeling.calculate_dynamic_roi(
            initial_investment, monthly_revenues, monthly_costs,
            investor_share, growth_rate=0.03
        )
        scenarios['expected'] = {
            'growth_rate': 0.03,
            'roi': expected['roi_percentage'],
            'payback_months': expected['payback_months'],
            'total_profit': expected['investor_total_profit']
        }
        
        # Kötümser: %0 büyüme
        pessimistic = FinancialModeling.calculate_dynamic_roi(
            initial_investment, monthly_revenues, monthly_costs,
            investor_share, growth_rate=0.00
        )
        scenarios['pessimistic'] = {
            'growth_rate': 0.00,
            'roi': pessimistic['roi_percentage'],
            'payback_months': pessimistic['payback_months'],
            'total_profit': pessimistic['investor_total_profit']
        }
        
        return scenarios
    
    @staticmethod
    def _final_recommendation(roi_analysis: Dict, risk_analysis: Dict, 
                             npv_analysis: Dict) -> str:
        """Final yatırım önerisi"""
        roi = roi_analysis['roi_percentage']
        payback = roi_analysis['payback_months']
        prob_profit = risk_analysis['probability_of_profit']
        npv = npv_analysis['npv']
        
        score = 0
        
        # ROI değerlendirmesi
        if roi > 100:
            score += 3
        elif roi > 50:
            score += 2
        elif roi > 20:
            score += 1
        
        # Geri dönüş süresi
        if payback and payback <= 12:
            score += 3
        elif payback and payback <= 24:
            score += 2
        elif payback and payback <= 36:
            score += 1
        
        # Karlılık olasılığı
        if prob_profit > 0.80:
            score += 3
        elif prob_profit > 0.60:
            score += 2
        elif prob_profit > 0.40:
            score += 1
        
        # NPV
        if npv > 0:
            score += 2
        
        # Öneri
        if score >= 9:
            return "🟢 ÇOK GÜÇLÜ YATIRIM - Hemen değerlendirin!"
        elif score >= 6:
            return "🟡 İYİ YATIRIM - Detaylı analiz ile ilerleyin"
        elif score >= 4:
            return "🟠 ORTA YATIRIM - Dikkatli değerlendirin"
        else:
            return "🔴 RİSKLİ YATIRIM - Alternatif senaryolar gerekli"
    
    @staticmethod
    def generate_financial_report(evaluation: Dict, save_path: str = None) -> str:
        """
        Finansal değerlendirme raporu oluştur
        
        Args:
            evaluation: business_case_evaluation çıktısı
            save_path: Rapor kayıt yolu
        
        Returns:
            str: Rapor metni
        """
        roi = evaluation['roi_analysis']
        risk = evaluation['risk_analysis']
        npv = evaluation['npv_analysis']
        scenarios = evaluation['scenarios']
        
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║              FİNANSAL DEĞERLENDİRME RAPORU                  ║
╚══════════════════════════════════════════════════════════════╝

📋 Proje: {evaluation['project_name']}
📅 Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

═══════════════════════════════════════════════════════════════
1. YATIRIM ÖZETİ
═══════════════════════════════════════════════════════════════

İlk Yatırım:                  {roi['initial_investment']:,.0f} TL
Yatırımcı Payı:               %{roi['investor_share_pct']:.0f}
Büyüme Oranı:                 %{roi['growth_rate']*100:.1f} (aylık)

═══════════════════════════════════════════════════════════════
2. GETİRİ ANALİZİ (ROI)
═══════════════════════════════════════════════════════════════

Toplam Gelir:                 {roi['total_revenue']:,.0f} TL
Toplam Maliyet:               {roi['total_cost']:,.0f} TL
Toplam Kâr:                   {roi['total_profit']:,.0f} TL

Yatırımcı Toplam Kârı:        {roi['investor_total_profit']:,.0f} TL
ROI (Yatırım Getirisi):       %{roi['roi_percentage']:.1f}
Yıllık ROI:                   %{roi['annual_roi']:.1f}

Geri Dönüş Süresi:            {roi['payback_months']} ay ({roi['payback_years']:.1f} yıl)

═══════════════════════════════════════════════════════════════
3. RİSK DEĞERLENDİRMESİ
═══════════════════════════════════════════════════════════════

Risk Seviyesi:                {risk['risk_level']}
Karlılık Olasılığı:           %{risk['probability_of_profit']*100:.1f}
Beklenen Kâr:                 {risk['expected_profit']:,.0f} TL
Beklenen ROI:                 %{risk['expected_roi']:.1f}

Value at Risk (VaR %5):       {risk['value_at_risk_5pct']:,.0f} TL
En İyi Senaryo (%95):         {risk['best_case']:,.0f} TL
En Kötü Senaryo (%5):         {risk['worst_case']:,.0f} TL

Geri Dönüş Olasılığı:         %{risk['payback_probability']*100:.1f}
Ort. Geri Dönüş Süresi:       {risk['avg_payback_months']:.1f} ay

═══════════════════════════════════════════════════════════════
4. NPV ANALİZİ
═══════════════════════════════════════════════════════════════

Net Bugünkü Değer (NPV):      {npv['npv']:,.0f} TL
İskonto Oranı:                %{npv['discount_rate']*100:.1f}
IRR (İç Verim Oranı):         {f"%{npv['annual_irr']:.1f}" if npv['annual_irr'] else "Hesaplanamadı"}

NPV Durumu:                   {"✅ Pozitif (Uygun)" if npv['npv_positive'] else "❌ Negatif (Uygun Değil)"}

═══════════════════════════════════════════════════════════════
5. SENARYO ANALİZİ
═══════════════════════════════════════════════════════════════

İYİMSER (Büyüme %{scenarios['optimistic']['growth_rate']*100:.0f}):
  ROI:                        %{scenarios['optimistic']['roi']:.1f}
  Geri Dönüş:                 {scenarios['optimistic']['payback_months']} ay
  Toplam Kâr:                 {scenarios['optimistic']['total_profit']:,.0f} TL

BEKLENEN (Büyüme %{scenarios['expected']['growth_rate']*100:.0f}):
  ROI:                        %{scenarios['expected']['roi']:.1f}
  Geri Dönüş:                 {scenarios['expected']['payback_months']} ay
  Toplam Kâr:                 {scenarios['expected']['total_profit']:,.0f} TL

KÖTÜMSER (Büyüme %{scenarios['pessimistic']['growth_rate']*100:.0f}):
  ROI:                        %{scenarios['pessimistic']['roi']:.1f}
  Geri Dönüş:                 {scenarios['pessimistic']['payback_months']} ay
  Toplam Kâr:                 {scenarios['pessimistic']['total_profit']:,.0f} TL

═══════════════════════════════════════════════════════════════
6. SONUÇ ve ÖNERİ
═══════════════════════════════════════════════════════════════

{evaluation['recommendation']}

Öneriler:
{risk['recommendation']}

═══════════════════════════════════════════════════════════════
"""
        
        if save_path:
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(report)
        
        return report
