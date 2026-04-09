"""
utils/smart_inputs.py
Kullanıcıdan ham gerçekler alınır, sistem puanları kendisi hesaplar.
Kullanıcı asla "karmaşıklık: 7" veya "risk: 0.6" girmez.
"""


class SmartInputs:

    @staticmethod
    def calculate_complexity(
        num_integrations: int,
        has_mobile: bool,
        has_ai_ml: bool,
        num_user_roles: int,
        has_realtime: bool,
        regulatory_requirements: int,
        num_modules: int,
    ) -> float:
        """Gerçek proje özelliklerinden karmaşıklık skoru hesapla (1-10)"""
        score = 1.0
        score += min(num_integrations * 0.4, 3.0)
        if has_mobile:
            score += 1.0
        if has_ai_ml:
            score += 1.5
        score += min(num_user_roles * 0.3, 2.0)
        if has_realtime:
            score += 0.8
        score += min(regulatory_requirements * 0.3, 1.5)
        score += min(num_modules * 0.05, 1.0)
        return round(min(score, 10.0), 1)

    @staticmethod
    def calculate_location_factor(
        city: str,
        district_type: str,
        work_model: str,
        office_sqm: int,
        rent_per_sqm: float,
    ) -> float:
        """Gerçek lokasyon koşullarından lokasyon faktörü hesapla (1.0-3.0)"""
        city_base = {
            "istanbul": 2.5,
            "ankara":   2.0,
            "izmir":    1.9,
            "bursa":    1.6,
            "antalya":  1.6,
            "diger":    1.3,
        }
        base = city_base.get(city.lower(), 1.3)

        district_adj = {
            "merkez":  +0.3,
            "ilce":     0.0,
            "sanayi":  -0.2,
            "uzak":    -0.3,
        }
        base += district_adj.get(district_type, 0.0)

        if work_model == "uzaktan":
            base *= 0.75
        elif work_model == "hibrit":
            base *= 0.88

        if rent_per_sqm > 0 and office_sqm > 0:
            monthly_rent = rent_per_sqm * office_sqm
            if monthly_rent > 100000:
                base = min(base + 0.2, 3.0)
            elif monthly_rent < 20000:
                base = max(base - 0.2, 1.0)

        return round(min(max(base, 1.0), 3.0), 1)

    @staticmethod
    def calculate_experience_level(
        senior_count: int,
        mid_count: int,
        junior_count: int,
        team_done_similar: bool,
        has_tech_lead: bool,
        domain_expertise: bool,
    ) -> float:
        """Ekip kompozisyonundan deneyim seviyesi hesapla (1.0-5.0)"""
        total = senior_count + mid_count + junior_count
        if total == 0:
            return 3.0
        weighted = (senior_count * 5 + mid_count * 3 + junior_count * 1) / total
        if team_done_similar:
            weighted += 0.5
        if has_tech_lead:
            weighted += 0.3
        if domain_expertise:
            weighted += 0.3
        return round(min(max(weighted, 1.0), 5.0), 1)

    @staticmethod
    def calculate_risk_factor(
        market_validated: bool,
        competitor_count: int,
        target_customer_defined: bool,
        new_technology: bool,
        third_party_dependency: int,
        has_prototype: bool,
        key_person_dependency: bool,
        regulatory_approval_needed: bool,
        budget_flexibility: str,
        has_confirmed_funding: bool,
        runway_months: int,
    ) -> dict:
        """
        Çok boyutlu risk analizi.
        Model için birleşik skoru + her boyutu ayrı döndürür.
        """
        # Pazar riski
        market = 0.5
        if market_validated:
            market -= 0.2
        if competitor_count > 10:
            market += 0.2
        elif competitor_count == 0:
            market += 0.1
        if not target_customer_defined:
            market += 0.2

        # Teknik risk
        technical = 0.3
        if new_technology:
            technical += 0.3
        technical += min(third_party_dependency * 0.05, 0.25)
        if has_prototype:
            technical -= 0.15

        # Operasyonel risk
        operational = 0.2
        if key_person_dependency:
            operational += 0.25
        if regulatory_approval_needed:
            operational += 0.2
        budget_adj = {"esnek": -0.1, "sabit": 0.0, "kati": +0.2}
        operational += budget_adj.get(budget_flexibility, 0.0)

        # Finansal risk
        financial = 0.3
        if has_confirmed_funding:
            financial -= 0.2
        if runway_months >= 18:
            financial -= 0.15
        elif runway_months < 6:
            financial += 0.3

        scores = {
            "pazar_riski":       round(min(max(market,      0.0), 1.0), 2),
            "teknik_risk":       round(min(max(technical,   0.0), 1.0), 2),
            "operasyonel_risk":  round(min(max(operational, 0.0), 1.0), 2),
            "finansal_risk":     round(min(max(financial,   0.0), 1.0), 2),
        }

        combined = (
            scores["pazar_riski"]       * 0.30 +
            scores["teknik_risk"]       * 0.25 +
            scores["operasyonel_risk"]  * 0.25 +
            scores["finansal_risk"]     * 0.20
        )
        scores["birlesik_risk"] = round(combined, 2)

        if combined < 0.3:
            scores["risk_seviyesi"] = "Düşük"
            scores["aciklama"] = "Proje iyi temellendirilmiş, riskler kontrol altında."
        elif combined < 0.55:
            scores["risk_seviyesi"] = "Orta"
            scores["aciklama"] = "Yönetilebilir riskler var, dikkatli takip gerekli."
        elif combined < 0.75:
            scores["risk_seviyesi"] = "Yüksek"
            scores["aciklama"] = "Birden fazla kritik risk faktörü var. Plan B hazırlayın."
        else:
            scores["risk_seviyesi"] = "Çok Yüksek"
            scores["aciklama"] = "Bu proje ciddi risk taşıyor. Devam kararı önceden detaylı analiz şart."

        return scores
