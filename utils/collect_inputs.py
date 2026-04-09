"""
Ortak girdi toplama fonksiyonu - tüm sayfalarda kullanılır
"""
import streamlit as st
from utils.smart_inputs import SmartInputs


def collect_project_inputs(prefix: str = ""):
    """Tüm sayfalarda kullanılan ortak girdi toplama fonksiyonu."""

    st.subheader("Temel Bilgiler")
    project_name   = st.text_input("Proje Adı", "Yeni Proje", key=f"{prefix}project_name")
    project_duration = st.slider("Proje Süresi (ay)", 1, 36, 12, key=f"{prefix}duration")
    team_size        = st.slider("Toplam Ekip Büyüklüğü (kişi)", 1, 100, 10, key=f"{prefix}team")
    tech_cost        = st.number_input(
        "Teknoloji Maliyeti (TL) — yazılım lisansı, sunucu, donanım",
        min_value=0, max_value=10000000, value=100000, step=10000, key=f"{prefix}tech"
    )

    st.divider()
    st.subheader("Karmaşıklık")
    st.caption("Sistem skoru sizin için hesaplayacak.")
    col1, col2 = st.columns(2)
    with col1:
        num_integrations = st.number_input(
            "Kaç farklı sistemle entegrasyon? (ERP, ödeme, SMS vb.)",
            min_value=0, max_value=20, value=2, key=f"{prefix}integrations"
        )
        has_mobile  = st.checkbox("Mobil uygulama var mı?", key=f"{prefix}mobile")
        has_ai_ml   = st.checkbox("AI / ML bileşeni var mı?", key=f"{prefix}ai")
        has_realtime = st.checkbox("Gerçek zamanlı veri akışı gerekiyor mu?", key=f"{prefix}realtime")
    with col2:
        num_user_roles = st.number_input(
            "Kaç farklı kullanıcı rolü? (admin, müşteri vb.)",
            min_value=1, max_value=15, value=2, key=f"{prefix}roles"
        )
        num_modules = st.number_input(
            "Tahminen kaç ana ekran / modül?",
            min_value=1, max_value=100, value=8, key=f"{prefix}modules"
        )
        regulatory_requirements = st.number_input(
            "Yasal / uyumluluk gereksinimi sayısı (KVKK, BDDK vb.)",
            min_value=0, max_value=10, value=0, key=f"{prefix}regulatory"
        )

    complexity = SmartInputs.calculate_complexity(
        num_integrations=num_integrations,
        has_mobile=has_mobile,
        has_ai_ml=has_ai_ml,
        num_user_roles=num_user_roles,
        has_realtime=has_realtime,
        regulatory_requirements=regulatory_requirements,
        num_modules=num_modules,
    )
    st.info(f"Hesaplanan karmaşıklık skoru: **{complexity} / 10**")

    st.divider()
    st.subheader("Lokasyon")
    col1, col2 = st.columns(2)
    with col1:
        city = st.selectbox(
            "Proje hangi şehirde?",
            ["istanbul", "ankara", "izmir", "bursa", "antalya", "diger"],
            format_func=lambda x: x.title(), key=f"{prefix}city"
        )
        district_type = st.selectbox(
            "Ofis nerede?",
            options=["merkez", "ilce", "sanayi", "uzak"], key=f"{prefix}district",
            format_func=lambda x: {
                "merkez": "Şehir merkezi / iş bölgesi",
                "ilce":   "İlçe / banliyö",
                "sanayi": "Sanayi bölgesi / OSB",
                "uzak":   "Uzak / taşra"
            }[x]
        )
    with col2:
        work_model = st.selectbox(
            "Çalışma modeli?",
            options=["ofis", "hibrit", "uzaktan"], key=f"{prefix}workmodel",
            format_func=lambda x: {
                "ofis":    "Tam zamanlı ofis",
                "hibrit":  "Hibrit (haftada 2-3 gün ofis)",
                "uzaktan": "Tam uzaktan"
            }[x]
        )
        office_sqm    = st.number_input("Ofis alanı m² (uzaktansa 0)", min_value=0, value=50, key=f"{prefix}sqm")
        rent_per_sqm  = st.number_input("Aylık kira TL/m² (bilmiyorsanız 0)", min_value=0.0, step=50.0, key=f"{prefix}rent")

    location_factor = SmartInputs.calculate_location_factor(
        city=city,
        district_type=district_type,
        work_model=work_model,
        office_sqm=office_sqm,
        rent_per_sqm=rent_per_sqm,
    )
    st.info(f"Hesaplanan lokasyon faktörü: **{location_factor} / 3.0**")

    st.divider()
    st.subheader("Ekip Deneyimi")
    col1, col2 = st.columns(2)
    with col1:
        senior_count = st.number_input("Kıdemli çalışan (5+ yıl)", min_value=0, value=2, key=f"{prefix}senior")
        mid_count    = st.number_input("Orta seviye (2-5 yıl)",     min_value=0, value=4, key=f"{prefix}mid")
        junior_count = st.number_input("Junior (0-2 yıl)",          min_value=0, value=2, key=f"{prefix}junior")
    with col2:
        team_done_similar = st.checkbox("Ekip daha önce benzer proje yaptı mı?", key=f"{prefix}similar")
        has_tech_lead     = st.checkbox("Teknik lider var mı?", key=f"{prefix}techlead")
        domain_expertise  = st.checkbox("Bu sektörde uzman biri ekipte var mı?", key=f"{prefix}domain")

    experience_level = SmartInputs.calculate_experience_level(
        senior_count=senior_count,
        mid_count=mid_count,
        junior_count=junior_count,
        team_done_similar=team_done_similar,
        has_tech_lead=has_tech_lead,
        domain_expertise=domain_expertise,
    )
    st.info(f"Hesaplanan deneyim seviyesi: **{experience_level} / 5.0**")

    st.divider()
    st.subheader("Risk Değerlendirmesi")
    st.caption("Her risk boyutu ayrı değerlendirilir.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Pazar**")
        market_validated        = st.checkbox("Ürün / hizmet gerçek müşteriyle test edildi mi?", key=f"{prefix}market_val")
        competitor_count        = st.number_input("Doğrudan rakip sayısı", min_value=0, value=3, key=f"{prefix}competitors")
        target_customer_defined = st.checkbox("Hedef müşteri profili net tanımlandı mı?", key=f"{prefix}target")

        st.markdown("**Teknik**")
        new_technology          = st.checkbox("Ekibin hiç kullanmadığı yeni teknoloji var mı?", key=f"{prefix}newtech")
        third_party_dependency  = st.number_input(
            "Kritik 3. parti bağımlılık sayısı", min_value=0, value=1, key=f"{prefix}thirdparty"
        )
        has_prototype           = st.checkbox("Prototip / MVP hazır mı?", key=f"{prefix}prototype")

    with col2:
        st.markdown("**Operasyonel**")
        key_person_dependency   = st.checkbox("Tek kişiye kritik bağımlılık var mı? (bus factor)", key=f"{prefix}keyperson")
        regulatory_needed       = st.checkbox("Yasal onay veya lisans gerekiyor mu?", key=f"{prefix}regneed")
        budget_flexibility      = st.selectbox(
            "Bütçe esnekliği",
            options=["esnek", "sabit", "kati"], key=f"{prefix}budget",
            format_func=lambda x: {
                "esnek": "Esnek — ihtiyaç halinde artabilir",
                "sabit": "Sabit — değiştirilemez ama yönetilebilir",
                "kati":  "Katı — tek kuruş fazla yok"
            }[x]
        )

        st.markdown("**Finansal**")
        has_confirmed_funding   = st.checkbox("Finansman onaylandı mı?", key=f"{prefix}funding")
        runway_months           = st.number_input(
            "Mevcut finansman kaç ay yeter?", min_value=0, max_value=60, value=12, key=f"{prefix}runway"
        )

    risk_data = SmartInputs.calculate_risk_factor(
        market_validated=market_validated,
        competitor_count=competitor_count,
        target_customer_defined=target_customer_defined,
        new_technology=new_technology,
        third_party_dependency=third_party_dependency,
        has_prototype=has_prototype,
        key_person_dependency=key_person_dependency,
        regulatory_approval_needed=regulatory_needed,
        budget_flexibility=budget_flexibility,
        has_confirmed_funding=has_confirmed_funding,
        runway_months=runway_months,
    )
    risk_factor = risk_data["birlesik_risk"]

    severity_fn = {"Düşük": st.success, "Orta": st.info,
                   "Yüksek": st.warning, "Çok Yüksek": st.error}
    severity_fn[risk_data["risk_seviyesi"]](
        f"**{risk_data['risk_seviyesi']} Risk** ({risk_factor}) — {risk_data['aciklama']}"
    )
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Pazar",       risk_data["pazar_riski"])
    c2.metric("Teknik",      risk_data["teknik_risk"])
    c3.metric("Operasyonel", risk_data["operasyonel_risk"])
    c4.metric("Finansal",    risk_data["finansal_risk"])

    return {
        "project_name":     project_name,
        "project_duration": project_duration,
        "team_size":        team_size,
        "complexity":       complexity,
        "tech_cost":        tech_cost,
        "location_factor":  location_factor,
        "experience_level": experience_level,
        "risk_factor":      risk_factor,
        "risk_breakdown":   risk_data,
    }
