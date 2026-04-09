import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pickle
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from neural_network.network import NeuralNetwork
from utils.engineering_economics import EngineeringEconomics
from utils.advanced_economics import AdvancedEconomics
from utils.sensitivity_analysis import SensitivityAnalysis
from utils.explainable_ai import ExplainableAI
from utils.continuous_learning import ContinuousLearning
from utils.pdf_report import PDFReportGenerator
from utils.smart_inputs import SmartInputs
from utils.collect_inputs import collect_project_inputs
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="AI Maliyet Tahmin Sistemi",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f4788;
        text-align: center;
        padding: 1rem 0;
        border-bottom: 3px solid #2c5aa0;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .success-box {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .danger-box {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    """Model ve preprocessor'ı yükle"""
    try:
        model = NeuralNetwork()
        model.load('models/cost_prediction_model.pkl')
        
        with open('models/preprocessor.pkl', 'rb') as f:
            preprocessor = pickle.load(f)
        
        with open('models/feature_names.pkl', 'rb') as f:
            feature_names = pickle.load(f)
        
        return model, preprocessor, feature_names
    except FileNotFoundError:
        return None, None, None

def main():
    st.markdown('<div class="main-header">💰 AI Destekli Maliyet Tahmin ve Optimizasyon Sistemi</div>', 
                unsafe_allow_html=True)
    
    model, preprocessor, feature_names = load_model()
    
    if model is None:
        st.error("⚠️ Model bulunamadı! Lütfen önce modeli eğitin: `python train_model.py`")
        return
    
    st.sidebar.title("📊 Kontrol Paneli")
    page = st.sidebar.radio(
        "Sayfa Seçin",
        ["🎯 Hızlı Tahmin", "📈 Detaylı Analiz", "🔍 Duyarlılık Analizi", 
         "📊 Senaryo Karşılaştırma", "🧠 Açıklanabilir AI", "💼 İleri Ekonomi", 
         "📚 Sürekli Öğrenme"]
    )
    
    if page == "🎯 Hızlı Tahmin":
        quick_prediction_page(model, preprocessor, feature_names)
    elif page == "📈 Detaylı Analiz":
        detailed_analysis_page(model, preprocessor, feature_names)
    elif page == "🔍 Duyarlılık Analizi":
        sensitivity_page(model, preprocessor, feature_names)
    elif page == "📊 Senaryo Karşılaştırma":
        scenario_comparison_page(model, preprocessor, feature_names)
    elif page == "🧠 Açıklanabilir AI":
        explainable_ai_page(model, preprocessor, feature_names)
    elif page == "💼 İleri Ekonomi":
        advanced_economics_page(model, preprocessor, feature_names)
    elif page == "📚 Sürekli Öğrenme":
        continuous_learning_page(model, preprocessor, feature_names)

def quick_prediction_page(model, preprocessor, feature_names):
    """Hızlı tahmin sayfası"""
    st.header("🎯 Hızlı Maliyet Tahmini")
    
    inputs = collect_project_inputs()
    
    if st.button("🚀 Tahmin Yap", type="primary", use_container_width=True):
        X_new = np.array([[
            inputs["project_duration"],
            inputs["team_size"],
            inputs["complexity"],
            inputs["tech_cost"],
            inputs["location_factor"],
            inputs["experience_level"],
            inputs["risk_factor"],
        ]])
        
        X_new_norm = preprocessor.normalize(X_new, fit=False)
        y_pred_norm = model.predict(X_new_norm)
        predicted_cost = preprocessor.denormalize(y_pred_norm, is_target=True)[0, 0]
        
        st.success("✅ Tahmin Tamamlandı!")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("💰 Tahmini Maliyet", f"{predicted_cost:,.0f} TL")
        
        with col2:
            monthly_cost = predicted_cost / inputs["project_duration"]
            st.metric("📅 Aylık Maliyet", f"{monthly_cost:,.0f} TL")
        
        with col3:
            per_person = predicted_cost / inputs["team_size"]
            st.metric("👤 Kişi Başı Maliyet", f"{per_person:,.0f} TL")
        
        st.divider()
        
        # Risk faktörüne bağlı volatilite
        base_uncertainty = 0.08
        risk_adj = inputs["risk_factor"] * 0.12
        complexity_adj = (inputs["complexity"] / 10) * 0.05
        dynamic_volatility = base_uncertainty + risk_adj + complexity_adj
        
        monte_carlo = SensitivityAnalysis.monte_carlo_simulation(predicted_cost, volatility=dynamic_volatility)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Güven Aralıkları")
            confidence_data = pd.DataFrame({
                'Seviye': ['%90 Güven', '%95 Güven', 'Ortalama'],
                'Alt Sınır': [
                    f"{monte_carlo['p10']:,.0f} TL",
                    f"{monte_carlo['confidence_95_lower']:,.0f} TL",
                    f"{monte_carlo['mean']:,.0f} TL"
                ],
                'Üst Sınır': [
                    f"{monte_carlo['p90']:,.0f} TL",
                    f"{monte_carlo['confidence_95_upper']:,.0f} TL",
                    f"{monte_carlo['mean']:,.0f} TL"
                ]
            })
            st.dataframe(confidence_data, use_container_width=True, hide_index=True)
        
        with col2:
            st.subheader("🎲 Monte Carlo Simülasyonu")
            fig = go.Figure()
            fig.add_trace(go.Histogram(
                x=monte_carlo['simulations'],
                nbinsx=50,
                name='Maliyet Dağılımı',
                marker_color='#667eea'
            ))
            fig.add_vline(x=predicted_cost, line_dash="dash", line_color="red",
                         annotation_text="Tahmin")
            fig.update_layout(
                xaxis_title="Maliyet (TL)",
                yaxis_title="Frekans",
                height=300,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        with st.expander("💡 Optimizasyon Önerileri"):
            if inputs["complexity"] > 7:
                st.markdown('<div class="warning-box">⚠️ <b>Yüksek Karmaşıklık:</b> Projeyi daha küçük modüllere bölmeyi düşünün.</div>', unsafe_allow_html=True)
            
            if inputs["risk_factor"] > 0.6:
                st.markdown('<div class="danger-box">🚨 <b>Yüksek Risk:</b> Risk azaltma stratejileri geliştirin ve acil durum planı hazırlayın.</div>', unsafe_allow_html=True)
            
            if inputs["experience_level"] < 3:
                st.markdown('<div class="warning-box">⚠️ <b>Düşük Deneyim:</b> Mentörlük programları veya eğitim ekleyin.</div>', unsafe_allow_html=True)
            
            if inputs["team_size"] > 20:
                st.markdown('<div class="warning-box">💡 <b>Büyük Ekip:</b> İletişim maliyetlerini ve koordinasyon zorluklarını göz önünde bulundurun.</div>', unsafe_allow_html=True)
            
            if all([inputs["complexity"] <= 7, inputs["risk_factor"] <= 0.6, inputs["experience_level"] >= 3]):
                st.markdown('<div class="success-box">✅ <b>İyi Durum:</b> Proje parametreleri optimal görünüyor!</div>', unsafe_allow_html=True)

def detailed_analysis_page(model, preprocessor, feature_names):
    """Detaylı analiz sayfası"""
    st.header("📈 Detaylı Finansal Analiz")
    
    inputs = collect_project_inputs()
    
    st.divider()
    st.subheader("💼 Finansal Parametreler")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        expected_revenue = st.number_input("Beklenen Toplam Gelir (TL)", 
                                          min_value=0, value=5000000, step=100000)
    
    with col2:
        discount_rate = st.number_input("İskonto Oranı", 0.01, 0.30, 0.10, 0.01,
                                       help="Örn: 0.10 = %10")
    
    with col3:
        monthly_revenue = st.number_input("Aylık Gelir (TL)", 
                                         min_value=0, value=200000, step=10000)
    
    if st.button("📊 Detaylı Analiz Yap", type="primary", use_container_width=True):
        X_new = np.array([[
            inputs["project_duration"],
            inputs["team_size"],
            inputs["complexity"],
            inputs["tech_cost"],
            inputs["location_factor"],
            inputs["experience_level"],
            inputs["risk_factor"]
        ]])
        
        X_new_norm = preprocessor.normalize(X_new, fit=False)
        y_pred_norm = model.predict(X_new_norm)
        predicted_cost = preprocessor.denormalize(y_pred_norm, is_target=True)[0, 0]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("💰 Tahmini Maliyet", f"{predicted_cost:,.0f} TL")
        
        with col2:
            roi = EngineeringEconomics.roi(expected_revenue - predicted_cost, predicted_cost)
            st.metric("📈 ROI", f"%{roi:.2f}", 
                     delta="Pozitif" if roi > 0 else "Negatif",
                     delta_color="normal" if roi > 0 else "inverse")
        
        with col3:
            monthly_operating_cost = predicted_cost / inputs["project_duration"]
            net_monthly = monthly_revenue - monthly_operating_cost
            cash_flows = [-predicted_cost]
            for _ in range(int(inputs["project_duration"])):
                cash_flows.append(net_monthly)
            npv = EngineeringEconomics.npv(cash_flows, discount_rate / 12)
            st.metric("💵 NPV", f"{npv:,.0f} TL",
                     delta="Uygun" if npv > 0 else "Uygun Değil",
                     delta_color="normal" if npv > 0 else "inverse")
        
        with col4:
            if monthly_revenue > 0:
                break_even = predicted_cost / monthly_revenue
                st.metric("⏱️ Başabaş", f"{break_even:.1f} ay")
            else:
                st.metric("⏱️ Başabaş", "N/A")
        
        st.divider()
        
        risk_assessment = SensitivityAnalysis.risk_assessment(
            predicted_cost, expected_revenue
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎯 Risk Değerlendirmesi")
            
            risk_color = "success" if risk_assessment['risk_level'] == 'Düşük' else \
                        "warning" if risk_assessment['risk_level'] == 'Orta' else "error"
            
            st.markdown(f"**Risk Seviyesi:** :{risk_color}[{risk_assessment['risk_level']}]")
            st.markdown(f"**Karlılık Olasılığı:** {risk_assessment['probability_of_profit']*100:.1f}%")
            st.markdown(f"**Kar Marjı:** %{risk_assessment['profit_margin_pct']:.2f}")
            st.markdown(f"**Value at Risk (VaR):** {risk_assessment['value_at_risk']:,.0f} TL")
            
            st.info(f"**Öneri:** {risk_assessment['recommendation']}")
        
        with col2:
            st.subheader("📊 Senaryo Analizi")
            
            scenarios = SensitivityAnalysis.scenario_analysis(predicted_cost)
            
            scenario_df = pd.DataFrame({
                'Senaryo': ['İyimser', 'Beklenen', 'Kötümser'],
                'Maliyet (TL)': [
                    f"{scenarios['optimistic']['cost']:,.0f}",
                    f"{scenarios['expected']['cost']:,.0f}",
                    f"{scenarios['pessimistic']['cost']:,.0f}"
                ],
                'Olasılık': [
                    f"%{scenarios['optimistic']['probability']*100:.0f}",
                    f"%{scenarios['expected']['probability']*100:.0f}",
                    f"%{scenarios['pessimistic']['probability']*100:.0f}"
                ]
            })
            
            st.dataframe(scenario_df, use_container_width=True, hide_index=True)
            
            st.metric("Beklenen Değer", f"{scenarios['expected_value']:,.0f} TL")
        
        st.divider()
        
        st.subheader("📄 PDF Rapor Oluştur")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            project_name = st.text_input("Proje Adı", "Maliyet Analizi Projesi")
            company_name = st.text_input("Şirket Adı", "")
        
        with col2:
            st.write("")
            st.write("")
            if st.button("📥 PDF İndir", type="secondary"):
                generate_pdf_report(
                    project_name, company_name, predicted_cost,
                    roi, npv, break_even if monthly_revenue > 0 else 0,
                    risk_assessment, scenarios,
                    {
                        'Proje Süresi': f"{inputs['project_duration']} ay",
                        'Ekip Büyüklüğü': f"{inputs['team_size']} kişi",
                        'Karmaşıklık': f"{inputs['complexity']}/10",
                        'Teknoloji Maliyeti': f"{inputs['tech_cost']:,.0f} TL",
                        'Risk Faktörü': f"{inputs['risk_factor']:.2f}"
                    }
                )

def sensitivity_page(model, preprocessor, feature_names):
    """Duyarlılık analizi sayfası"""
    st.header("🔍 Duyarlılık Analizi")
    
    st.info("Bu analiz, her parametrenin maliyet üzerindeki etkisini gösterir.")
    
    inputs = collect_project_inputs(prefix="sens_")
    
    if st.button("🔍 Duyarlılık Analizi Yap", type="primary", use_container_width=True):
        X_base = np.array([[
            inputs["project_duration"],
            inputs["team_size"],
            inputs["complexity"],
            inputs["tech_cost"],
            inputs["location_factor"],
            inputs["experience_level"],
            inputs["risk_factor"],
        ]])
        
        tornado_data = SensitivityAnalysis.tornado_chart_data(
            model, preprocessor, X_base, feature_names
        )
        
        st.subheader("📊 Tornado Chart - Parametre Etkileri")
        
        features = [item['feature'] for item in tornado_data]
        impacts = [item['impact'] for item in tornado_data]
        
        fig = go.Figure()
        
        colors = ['#d9534f' if imp > 20 else '#f0ad4e' if imp > 10 else '#5cb85c' 
                 for imp in impacts]
        
        fig.add_trace(go.Bar(
            y=features,
            x=impacts,
            orientation='h',
            marker=dict(color=colors),
            text=[f"{imp:.1f}%" for imp in impacts],
            textposition='outside'
        ))
        
        fig.update_layout(
            title="Parametrelerin Maliyet Üzerindeki Etkisi",
            xaxis_title="Etki (%)",
            yaxis_title="Parametre",
            height=500,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        st.subheader("📈 Detaylı Parametre Analizi")
        
        selected_param = st.selectbox(
            "Analiz edilecek parametreyi seçin:",
            feature_names
        )
        
        param_index = feature_names.index(selected_param)
        
        sensitivity = SensitivityAnalysis.sensitivity_to_parameter(
            model, preprocessor, X_base, param_index, selected_param,
            variation_range=(-0.3, 0.3), n_points=30
        )
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=sensitivity['variations'],
            y=sensitivity['costs'],
            mode='lines',
            name='Maliyet',
            line=dict(color='#667eea', width=3)
        ))
        
        fig.add_hline(y=sensitivity['base_cost'], line_dash="dash", 
                     line_color="red", annotation_text="Temel Maliyet")
        
        fig.add_vline(x=sensitivity['base_value'], line_dash="dash",
                     line_color="green", annotation_text="Temel Değer")
        
        fig.update_layout(
            title=f"{selected_param} Değişiminin Maliyet Üzerindeki Etkisi",
            xaxis_title=selected_param,
            yaxis_title="Tahmini Maliyet (TL)",
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Elastikiyet", f"{sensitivity['elasticity']:.3f}")
        c2.metric("Maliyet Değişim Aralığı", f"{sensitivity['cost_change_pct']:.1f}%")
        cr = sensitivity['cost_range']
        c3.metric("Min - Max", f"{cr[0]:,.0f} – {cr[1]:,.0f} TL")

def scenario_comparison_page(model, preprocessor, feature_names):
    """Senaryo karşılaştırma sayfası"""
    st.header("📊 Senaryo Karşılaştırma")
    
    st.info("Farklı proje senaryolarını yan yana karşılaştırın.")
    
    num_scenarios = st.slider("Kaç senaryo karşılaştırmak istersiniz?", 2, 4, 2)
    
    scenarios_data = []
    
    cols = st.columns(num_scenarios)
    
    for i, col in enumerate(cols):
        with col:
            st.subheader(f"Senaryo {i+1}")
            scenario_name = st.text_input(f"Senaryo Adı", f"Senaryo {i+1}", key=f"scen_name_{i}")
            scenario_inputs = collect_project_inputs(prefix=f"scen_{i}_")
            scenarios_data.append({
                'name': scenario_name,
                'data': [
                    scenario_inputs["project_duration"],
                    scenario_inputs["team_size"],
                    scenario_inputs["complexity"],
                    scenario_inputs["tech_cost"],
                    scenario_inputs["location_factor"],
                    scenario_inputs["experience_level"],
                    scenario_inputs["risk_factor"],
                ]
            })
    
    if st.button("⚖️ Senaryoları Karşılaştır", type="primary", use_container_width=True):
        results = []
        
        for scenario in scenarios_data:
            X = np.array([scenario['data']])
            X_norm = preprocessor.normalize(X, fit=False)
            y_pred_norm = model.predict(X_norm)
            cost = preprocessor.denormalize(y_pred_norm, is_target=True)[0, 0]
            
            results.append({
                'Senaryo': scenario['name'],
                'Maliyet': cost,
                'Süre': scenario['data'][0],
                'Ekip': scenario['data'][1],
                'Karmaşıklık': scenario['data'][2]
            })
        
        st.subheader("📊 Karşılaştırma Sonuçları")
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=[r['Senaryo'] for r in results],
            y=[r['Maliyet'] for r in results],
            marker=dict(
                color=[r['Maliyet'] for r in results],
                colorscale='Viridis',
                showscale=True
            ),
            text=[f"{r['Maliyet']:,.0f} TL" for r in results],
            textposition='outside'
        ))
        
        fig.update_layout(
            title="Senaryo Maliyet Karşılaştırması",
            xaxis_title="Senaryo",
            yaxis_title="Tahmini Maliyet (TL)",
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        comparison_df = pd.DataFrame(results)
        comparison_df['Maliyet'] = comparison_df['Maliyet'].apply(lambda x: f"{x:,.0f} TL")
        comparison_df['Süre'] = comparison_df['Süre'].apply(lambda x: f"{x:.0f} ay")
        comparison_df['Ekip'] = comparison_df['Ekip'].apply(lambda x: f"{x:.0f} kişi")
        comparison_df['Karmaşıklık'] = comparison_df['Karmaşıklık'].apply(lambda x: f"{x:.1f}/10")
        
        st.dataframe(comparison_df, use_container_width=True, hide_index=True)
        
        best_scenario = min(results, key=lambda x: x['Maliyet'])
        st.success(f"✅ **En Ekonomik Senaryo:** {best_scenario['Senaryo']} ({best_scenario['Maliyet']:,.0f} TL)")

def generate_pdf_report(project_name, company_name, predicted_cost, roi, npv, 
                       break_even, risk_assessment, scenarios, project_data):
    """PDF rapor oluştur"""
    try:
        pdf = PDFReportGenerator(f"reports/{project_name.replace(' ', '_')}_report.pdf")
        
        os.makedirs('reports', exist_ok=True)
        
        pdf.add_title_page(project_name, company_name)
        
        monte_carlo = SensitivityAnalysis.monte_carlo_simulation(predicted_cost)
        
        summary_data = {
            'predicted_cost': predicted_cost,
            'confidence_lower': monte_carlo['p10'],
            'confidence_upper': monte_carlo['p90'],
            'roi': roi,
            'npv': npv,
            'break_even': break_even,
            'risk_level': risk_assessment['risk_level'],
            'recommendation': risk_assessment['recommendation'],
            'model_accuracy': '⚠️ Sentetik Veri - Gerçek Doğruluk Bilinmiyor'
        }
        
        pdf.add_executive_summary(summary_data)
        pdf.add_project_details(project_data)
        pdf.add_scenario_analysis(scenarios)
        
        filename = pdf.generate()
        
        st.success(f"✅ PDF rapor oluşturuldu: {filename}")
        
        with open(filename, 'rb') as f:
            st.download_button(
                label="📥 PDF'i İndir",
                data=f,
                file_name=f"{project_name}_report.pdf",
                mime="application/pdf"
            )
    
    except Exception as e:
        st.error(f"PDF oluşturulurken hata: {e}")

from app_enterprise_pages import explainable_ai_page, advanced_economics_page, continuous_learning_page

if __name__ == "__main__":
    main()
