"""
Kurumsal Seviye Dashboard Sayfaları
XAI, İleri Ekonomi ve Sürekli Öğrenme
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from utils.explainable_ai import ExplainableAI
from utils.advanced_economics import AdvancedEconomics
from utils.continuous_learning import ContinuousLearning
from utils.collect_inputs import collect_project_inputs

def explainable_ai_page(model, preprocessor, feature_names):
    """Açıklanabilir AI sayfası - SHAP benzeri açıklamalar"""
    st.header("🧠 Açıklanabilir Yapay Zeka (XAI)")
    
    st.info("💡 **CEO'lar için:** Model sadece tahmin yapmaz, neden bu tahmini yaptığını da açıklar.")
    
    inputs = collect_project_inputs(prefix="xai_")
    
    if st.button("🔍 Tahmini Açıkla", type="primary", use_container_width=True):
        X_new = np.array([[
            inputs["project_duration"],
            inputs["team_size"],
            inputs["complexity"],
            inputs["tech_cost"],
            inputs["location_factor"],
            inputs["experience_level"],
            inputs["risk_factor"],
        ]])
        
        contributions = ExplainableAI.calculate_feature_contributions(
            model, preprocessor, X_new, feature_names
        )
        
        predicted_cost = contributions['base_prediction']
        
        st.success(f"✅ **Tahmini Maliyet: {predicted_cost:,.0f} TL**")
        
        st.divider()
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📊 Özellik Katkıları (SHAP-benzeri)")
            
            sorted_contributions = sorted(
                contributions['contributions'].items(),
                key=lambda x: abs(x[1]['contribution']),
                reverse=True
            )
            
            features = [item[0] for item in sorted_contributions]
            contribs = [item[1]['contribution'] for item in sorted_contributions]
            colors = ['green' if c < 0 else 'red' for c in contribs]
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                y=features,
                x=contribs,
                orientation='h',
                marker=dict(
                    color=contribs,
                    colorscale='RdYlGn_r',
                    showscale=True,
                    colorbar=dict(title="Katkı (TL)")
                ),
                text=[f"{c:,.0f} TL" for c in contribs],
                textposition='outside'
            ))
            
            fig.update_layout(
                title="Her Parametrenin Maliyete Katkısı",
                xaxis_title="Maliyet Katkısı (TL)",
                yaxis_title="Parametre",
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("💡 Açıklama")
            
            explanation = ExplainableAI.generate_explanation_text(contributions, top_n=7)
            st.markdown(explanation)
        
        st.divider()
        
        st.subheader("🌊 Waterfall Chart - Tahmin Oluşumu")
        
        waterfall_data = ExplainableAI.create_waterfall_data(contributions)
        
        fig = go.Figure(go.Waterfall(
            name="Maliyet",
            orientation="v",
            measure=waterfall_data['measures'],
            x=waterfall_data['labels'],
            y=waterfall_data['values'],
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            decreasing={"marker": {"color": "#5cb85c"}},
            increasing={"marker": {"color": "#d9534f"}},
            totals={"marker": {"color": "#5bc0de"}}
        ))
        
        fig.update_layout(
            title="Baseline'dan Final Tahmine Giden Yol",
            height=500,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        st.subheader("🎯 Counterfactual Analiz: 'Ne Değişmeli?'")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            target_cost = st.number_input(
                "Hedef Maliyet (TL)",
                min_value=int(predicted_cost * 0.5),
                max_value=int(predicted_cost * 1.5),
                value=int(predicted_cost * 0.9),
                step=10000
            )
        
        with col2:
            if st.button("🔄 Önerileri Hesapla"):
                result = ExplainableAI.counterfactual_explanation(
                    model, preprocessor, X_new, feature_names, target_cost
                )
                
                if result['success']:
                    st.success(f"✅ Hedefe ulaşıldı: {result['achieved_cost']:,.0f} TL")
                else:
                    st.warning(f"⚠️ Yaklaşık: {result['achieved_cost']:,.0f} TL")
                
                if result['changes']:
                    st.subheader("📝 Önerilen Değişiklikler")
                    
                    changes_df = pd.DataFrame([
                        {
                            'Parametre': feature,
                            'Mevcut': f"{data['original']:.2f}",
                            'Önerilen': f"{data['suggested']:.2f}",
                            'Değişim': f"{data['change_pct']:+.1f}%"
                        }
                        for feature, data in result['changes'].items()
                    ])
                    
                    st.dataframe(changes_df, use_container_width=True, hide_index=True)

def advanced_economics_page(model, preprocessor, feature_names):
    """İleri seviye mühendislik ekonomisi sayfası"""
    st.header("💼 İleri Seviye Mühendislik Ekonomisi")
    
    st.info("📊 **CFO'lar için:** Vergi, enflasyon ve amortisman dahil tam finansal simülasyon.")
    
    tab1, tab2, tab3 = st.tabs(["📈 Vergi Sonrası NPV", "🏢 Kiralama vs Satın Alma", "💰 İşletme Sermayesi"])
    
    with tab1:
        st.subheader("Vergi ve Amortisman Dahil NPV Analizi")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            initial_investment = st.number_input("İlk Yatırım (TL)", 100000, 10000000, 1000000, 50000)
            annual_revenue = st.number_input("Yıllık Gelir (TL)", 100000, 10000000, 1500000, 50000)
            annual_opcost = st.number_input("Yıllık İşletme Maliyeti (TL)", 0, 5000000, 500000, 50000)
        
        with col2:
            project_life = st.slider("Proje Ömrü (yıl)", 3, 20, 5)
            discount_rate = st.slider("İskonto Oranı", 0.05, 0.30, 0.10, 0.01)
            tax_rate = st.slider("Vergi Oranı", 0.10, 0.40, 0.20, 0.01)
        
        with col3:
            inflation_rate = st.slider("Enflasyon Oranı", 0.0, 0.20, 0.05, 0.01)
            depreciation_method = st.selectbox(
                "Amortisman Yöntemi",
                ["straight_line", "vuk", "declining_balance"],
                format_func=lambda x: {
                    "straight_line": "Doğrusal",
                    "vuk": "VUK (Türkiye — Vergi Usul Kanunu)",
                    "declining_balance": "Azalan Bakiye"
                }[x]
            )
            salvage_value = st.number_input("Hurda Değeri (TL)", 0, 1000000, 0, 10000)
        
        if st.button("📊 Analiz Yap", type="primary", use_container_width=True):
            # VUK seçilirse şimdilik straight_line olarak ele al
            method_to_use = "straight_line" if depreciation_method == "vuk" else depreciation_method
            
            result = AdvancedEconomics.project_npv_with_taxes(
                initial_investment=initial_investment,
                annual_revenue=annual_revenue,
                annual_operating_cost=annual_opcost,
                project_life=project_life,
                discount_rate=discount_rate,
                tax_rate=tax_rate,
                depreciation_method=method_to_use,
                salvage_value=salvage_value,
                inflation_rate=inflation_rate
            )
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Vergi Öncesi NPV", f"{result['before_tax_npv']:,.0f} TL")
            
            with col2:
                st.metric("Vergi Sonrası NPV", f"{result['after_tax_npv']:,.0f} TL",
                         delta=f"{result['after_tax_npv'] - result['before_tax_npv']:,.0f} TL")
            
            with col3:
                if result['after_tax_irr']:
                    st.metric("IRR (Vergi Sonrası)", f"%{result['after_tax_irr']*100:.2f}")
                else:
                    st.metric("IRR", "Hesaplanamadı")
            
            with col4:
                st.metric("Toplam Vergi Kalkanı", f"{result['total_tax_shield']:,.0f} TL")
            
            st.divider()
            
            st.subheader("📅 Yıllık Detaylar")
            
            yearly_df = pd.DataFrame(result['yearly_details'])
            yearly_df['revenue'] = yearly_df['revenue'].apply(lambda x: f"{x:,.0f} TL")
            yearly_df['operating_cost'] = yearly_df['operating_cost'].apply(lambda x: f"{x:,.0f} TL")
            yearly_df['depreciation'] = yearly_df['depreciation'].apply(lambda x: f"{x:,.0f} TL")
            yearly_df['tax'] = yearly_df['tax'].apply(lambda x: f"{x:,.0f} TL")
            yearly_df['after_tax_cash_flow'] = yearly_df['after_tax_cash_flow'].apply(lambda x: f"{x:,.0f} TL")
            
            yearly_df.columns = ['Yıl', 'Gelir', 'İşletme Maliyeti', 'Amortisman', 
                                'Vergi Matrahı', 'Vergi', 'Vergi Sonrası Nakit Akışı', 'Vergi Kalkanı']
            
            st.dataframe(yearly_df, use_container_width=True, hide_index=True)
            
            fig = go.Figure()
            
            years = [d['year'] for d in result['yearly_details']]
            atcf = [d['after_tax_cash_flow'] for d in result['yearly_details']]
            
            fig.add_trace(go.Bar(
                x=years,
                y=atcf,
                name='Vergi Sonrası Nakit Akışı',
                marker_color='#5cb85c'
            ))
            
            fig.update_layout(
                title="Yıllık Vergi Sonrası Nakit Akışı",
                xaxis_title="Yıl",
                yaxis_title="Nakit Akışı (TL)",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Kiralama vs Satın Alma Analizi")
        
        col1, col2 = st.columns(2)
        
        with col1:
            purchase_price = st.number_input("Satın Alma Fiyatı (TL)", 100000, 10000000, 500000, 50000, key="lease_buy_price")
            salvage_value_lb = st.number_input("Hurda Değeri (TL)", 0, 1000000, 50000, 10000, key="lease_buy_salvage")
            maintenance_cost = st.number_input("Yıllık Bakım Maliyeti (TL)", 0, 100000, 10000, 1000)
        
        with col2:
            lease_payment = st.number_input("Yıllık Kira Ödemesi (TL)", 10000, 500000, 100000, 10000)
            lease_term = st.slider("Kira Süresi (yıl)", 1, 10, 5, key="lease_term")
            discount_rate_lb = st.slider("İskonto Oranı", 0.05, 0.30, 0.10, 0.01, key="lease_discount")
            tax_rate_lb = st.slider("Vergi Oranı", 0.10, 0.40, 0.20, 0.01, key="lease_tax")
            depreciation_life = st.slider("Amortisman Süresi (yıl)", 3, 20, 7)
        
        if st.button("⚖️ Karşılaştır", type="primary", use_container_width=True, key="lease_compare"):
            result = AdvancedEconomics.lease_vs_buy_analysis(
                purchase_price=purchase_price,
                lease_payment=lease_payment,
                lease_term=lease_term,
                discount_rate=discount_rate_lb,
                tax_rate=tax_rate_lb,
                depreciation_life=depreciation_life,
                salvage_value=salvage_value_lb,
                maintenance_cost=maintenance_cost
            )
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Satın Alma NPV", f"{result['buy_npv']:,.0f} TL")
            
            with col2:
                st.metric("Kiralama NPV", f"{result['lease_npv']:,.0f} TL")
            
            with col3:
                advantage = result['net_advantage_to_leasing']
                st.metric("Net Avantaj", f"{abs(advantage):,.0f} TL",
                         delta=result['recommendation'])
            
            if result['recommendation'] == 'Satın Al':
                st.success(f"✅ **Öneri: Satın Alın** - {abs(advantage):,.0f} TL daha avantajlı")
            else:
                st.info(f"💡 **Öneri: Kiralayın** - {abs(advantage):,.0f} TL daha avantajlı")
            
            st.divider()
            
            comparison_data = {
                'Metrik': ['Toplam Maliyet', 'NPV', 'Başabaş Kira Ödemesi'],
                'Satın Alma': [
                    f"{result['buy_total_cost']:,.0f} TL",
                    f"{result['buy_npv']:,.0f} TL",
                    "-"
                ],
                'Kiralama': [
                    f"{result['lease_total_cost']:,.0f} TL",
                    f"{result['lease_npv']:,.0f} TL",
                    f"{result['break_even_lease_payment']:,.0f} TL/yıl"
                ]
            }
            
            st.table(pd.DataFrame(comparison_data))
    
    with tab3:
        st.subheader("İşletme Sermayesi Analizi")
        
        col1, col2 = st.columns(2)
        
        with col1:
            revenue_wc = st.number_input("Yıllık Gelir (TL)", 1000000, 100000000, 10000000, 100000, key="wc_revenue")
            days_receivable = st.slider("Alacak Tahsil Süresi (gün)", 15, 120, 45)
        
        with col2:
            days_inventory = st.slider("Envanter Devir Süresi (gün)", 15, 180, 60)
            days_payable = st.slider("Borç Ödeme Süresi (gün)", 15, 90, 30)
        
        if st.button("💰 Hesapla", type="primary", use_container_width=True, key="wc_calc"):
            result = AdvancedEconomics.working_capital_analysis(
                revenue=revenue_wc,
                days_receivable=days_receivable,
                days_inventory=days_inventory,
                days_payable=days_payable
            )
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("İşletme Sermayesi", f"{result['working_capital']:,.0f} TL")
            
            with col2:
                st.metric("Nakit Dönüşüm Süresi", f"{result['cash_conversion_cycle']:.0f} gün")
            
            with col3:
                st.metric("İşletme Sermayesi Oranı", f"%{result['working_capital_ratio']:.2f}")
            
            st.divider()
            
            components = {
                'Bileşen': ['Alacaklar', 'Envanter', 'Borçlar', 'Net İşletme Sermayesi'],
                'Tutar (TL)': [
                    f"{result['accounts_receivable']:,.0f}",
                    f"{result['inventory']:,.0f}",
                    f"-{result['accounts_payable']:,.0f}",
                    f"{result['working_capital']:,.0f}"
                ]
            }
            
            st.table(pd.DataFrame(components))
            
            if result['recommendation'] == 'İyi':
                st.success(f"✅ **{result['recommendation']}** - Nakit dönüşüm süresi optimal")
            elif result['recommendation'] == 'Orta':
                st.warning(f"⚠️ **{result['recommendation']}** - İyileştirme alanları var")
            else:
                st.error(f"❌ **{result['recommendation']}** - Acil iyileştirme gerekli")

def continuous_learning_page(model, preprocessor, feature_names):
    """Sürekli öğrenme ve geri bildirim sayfası"""
    st.header("📚 Sürekli Öğrenme Sistemi")
    
    st.info("🔄 **Sistem Yöneticileri için:** Model gerçek proje sonuçlarından öğrenir ve kendini geliştirir.")
    
    cl = ContinuousLearning()
    
    tab1, tab2, tab3 = st.tabs(["➕ Geri Bildirim Ekle", "📊 İstatistikler", "🔄 Model Güncelleme"])
    
    with tab1:
        st.subheader("Proje Geri Bildirimi Ekle")
        
        col1, col2 = st.columns(2)
        
        with col1:
            project_name = st.text_input("Proje Adı", "Örnek Proje 2024", key="cl_project_name")
            predicted_cost = st.number_input("Tahmin Edilen Maliyet (TL)", 100000, 100000000, 1000000, 50000, key="cl_predicted")
            actual_cost = st.number_input("Gerçekleşen Maliyet (TL)", 100000, 100000000, 1200000, 50000, key="cl_actual")
        
        with col2:
            st.write("**Proje Parametreleri:**")
            inputs_fb = collect_project_inputs(prefix="cl_")
        
        notes = st.text_area("Notlar (opsiyonel)", "", key="cl_notes")
        
        if st.button("💾 Geri Bildirimi Kaydet", type="primary", use_container_width=True):
            project_params = {
                'project_duration': inputs_fb['project_duration'],
                'team_size': inputs_fb['team_size'],
                'complexity': inputs_fb['complexity'],
                'tech_cost': inputs_fb['tech_cost'],
                'location_factor': inputs_fb['location_factor'],
                'experience_level': inputs_fb['experience_level'],
                'risk_factor': inputs_fb['risk_factor']
            }
            
            feedback_id = cl.add_feedback(
                project_name=project_name,
                predicted_cost=predicted_cost,
                actual_cost=actual_cost,
                project_params=project_params,
                notes=notes
            )
            
            error = actual_cost - predicted_cost
            error_pct = (error / actual_cost * 100) if actual_cost > 0 else 0
            
            st.success(f"✅ Geri bildirim kaydedildi (ID: {feedback_id})")
            
            if abs(error_pct) < 10:
                st.balloons()
                st.success(f"🎯 Mükemmel tahmin! Hata: %{abs(error_pct):.2f}")
            elif abs(error_pct) < 20:
                st.info(f"✓ İyi tahmin. Hata: %{abs(error_pct):.2f}")
            else:
                st.warning(f"⚠️ Yüksek hata: %{abs(error_pct):.2f} - Model iyileştirmesi gerekebilir")
    
    with tab2:
        st.subheader("Geri Bildirim İstatistikleri")
        
        stats = cl.get_feedback_statistics()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Toplam Geri Bildirim", stats['total_feedback'])
        
        with col2:
            st.metric("Ortalama Hata", f"%{stats['average_error_pct']:.2f}")
        
        with col3:
            st.metric("Doğru Tahminler", f"{stats['accurate_predictions']} (%<10 hata)")
        
        with col4:
            st.metric("Doğruluk Oranı", f"%{stats['accuracy_rate']:.1f}")
        
        if stats['needs_retraining']:
            st.warning("⚠️ **Model yeniden eğitilmeli!** Yeterli geri bildirim toplandı veya hata oranı yüksek.")
        else:
            st.success("✅ Model performansı yeterli.")
        
        st.divider()
        
        st.subheader("Son Geri Bildirimler")
        
        recent = cl.get_recent_feedback(limit=10)
        
        if recent:
            recent_df = pd.DataFrame(recent)
            recent_df['predicted_cost'] = recent_df['predicted_cost'].apply(lambda x: f"{x:,.0f} TL")
            recent_df['actual_cost'] = recent_df['actual_cost'].apply(lambda x: f"{x:,.0f} TL")
            recent_df['error_percentage'] = recent_df['error_percentage'].apply(lambda x: f"{x:+.2f}%")
            
            recent_df.columns = ['Proje', 'Tahmin', 'Gerçek', 'Hata %', 'Tarih', 'Notlar']
            
            st.dataframe(recent_df, use_container_width=True, hide_index=True)
        else:
            st.info("Henüz geri bildirim yok.")
    
    with tab3:
        st.subheader("Model Güncelleme ve Yeniden Eğitim")
        
        stats = cl.get_feedback_statistics()
        
        st.write(f"**Mevcut Durum:** {stats['total_feedback']} geri bildirim, ortalama %{stats['average_error_pct']:.2f} hata")
        
        col1, col2 = st.columns(2)
        
        with col1:
            learning_rate = st.slider("Öğrenme Oranı", 0.0001, 0.01, 0.001, 0.0001, format="%.4f")
            epochs = st.slider("Epoch Sayısı", 50, 500, 100, 50)
        
        with col2:
            min_samples = st.number_input("Minimum Örnek Sayısı", 10, 100, 20, 5)
            threshold_error = st.slider("Hata Eşiği (%)", 10.0, 30.0, 15.0, 1.0)
        
        if st.button("🔄 Artımlı Eğitim Yap", type="primary", use_container_width=True):
            with st.spinner("Model güncelleniyor..."):
                result = cl.incremental_training(
                    model=model,
                    preprocessor=preprocessor,
                    learning_rate=learning_rate,
                    epochs=epochs
                )
                
                if result['success']:
                    st.success("✅ Model başarıyla güncellendi!")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Kullanılan Örnek", result['samples_used'])
                    
                    with col2:
                        st.metric("İyileşme", f"%{result['improvement_pct']:.2f}")
                    
                    with col3:
                        st.metric("Yeni R²", f"{result['new_r2']:.4f}")
                    
                    st.info("💾 Model otomatik olarak kaydedildi. Değişiklikler hemen aktif.")
                else:
                    st.error(f"❌ {result['message']}")
        
        st.divider()
        
        if st.button("🤖 Otomatik Güncelleme (Gerekirse)", use_container_width=True):
            with st.spinner("Kontrol ediliyor..."):
                result = cl.auto_retrain_if_needed(
                    model=model,
                    preprocessor=preprocessor,
                    threshold_error=threshold_error,
                    min_samples=min_samples
                )
                
                if result['retrained']:
                    st.success(f"✅ Model güncellendi! Sebep: {result['reason']}")
                    st.metric("İyileşme", f"%{result['improvement']:.2f}")
                else:
                    st.info(f"ℹ️ Güncelleme gerekmedi. Sebep: {result['reason']}")
