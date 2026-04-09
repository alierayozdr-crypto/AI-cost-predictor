from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
import numpy as np
import pickle
import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from neural_network.network import NeuralNetwork
from utils.engineering_economics import EngineeringEconomics
from utils.advanced_economics import AdvancedEconomics
from utils.sensitivity_analysis import SensitivityAnalysis
from utils.explainable_ai import ExplainableAI

app = FastAPI(
    title="AI Maliyet Tahmin API",
    description="Kurumsal entegrasyon için REST API. SAP, Oracle, Jira ile entegre edilebilir.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://localhost:3000", "https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

class ProjectInput(BaseModel):
    """Proje girdi parametreleri"""
    project_duration: float = Field(..., ge=1, le=36, description="Proje süresi (ay)")
    team_size: int = Field(..., ge=2, le=50, description="Ekip büyüklüğü")
    complexity: float = Field(..., ge=1, le=10, description="Karmaşıklık skoru")
    tech_cost: float = Field(..., ge=10000, le=10000000, description="Teknoloji maliyeti (TL)")
    location_factor: float = Field(..., ge=1, le=3, description="Lokasyon faktörü")
    experience_level: float = Field(..., ge=1, le=5, description="Deneyim seviyesi")
    risk_factor: float = Field(..., ge=0, le=1, description="Risk faktörü")
    
    class Config:
        json_schema_extra = {
            "example": {
                "project_duration": 12,
                "team_size": 10,
                "complexity": 5.0,
                "tech_cost": 100000,
                "location_factor": 2.0,
                "experience_level": 3.0,
                "risk_factor": 0.5
            }
        }

class FinancialInput(BaseModel):
    """Finansal analiz parametreleri"""
    expected_revenue: Optional[float] = Field(None, description="Beklenen gelir (TL)")
    discount_rate: Optional[float] = Field(0.10, description="İskonto oranı")
    tax_rate: Optional[float] = Field(0.20, description="Vergi oranı")
    inflation_rate: Optional[float] = Field(0.05, description="Enflasyon oranı")
    depreciation_method: Optional[str] = Field("straight_line", description="Amortisman yöntemi")

class PredictionResponse(BaseModel):
    """Tahmin yanıtı"""
    predicted_cost: float
    confidence_interval_90: Dict[str, float]
    confidence_interval_95: Dict[str, float]
    timestamp: str
    model_version: str = "1.0"

class DetailedAnalysisResponse(BaseModel):
    """Detaylı analiz yanıtı"""
    predicted_cost: float
    roi: Optional[float] = None
    npv: Optional[float] = None
    after_tax_npv: Optional[float] = None
    irr: Optional[float] = None
    break_even_months: Optional[float] = None
    risk_assessment: Dict
    scenarios: Dict
    explanation: str
    timestamp: str

class SensitivityResponse(BaseModel):
    """Duyarlılık analizi yanıtı"""
    base_cost: float
    tornado_data: List[Dict]
    parameter_sensitivities: Dict
    timestamp: str

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
        raise HTTPException(status_code=500, detail="Model bulunamadı. Lütfen önce modeli eğitin.")

@app.get("/")
def root():
    """API ana sayfası"""
    return {
        "message": "AI Maliyet Tahmin API",
        "version": "1.0.0",
        "endpoints": {
            "predict": "/api/v1/predict",
            "detailed_analysis": "/api/v1/detailed-analysis",
            "sensitivity": "/api/v1/sensitivity",
            "explainability": "/api/v1/explain",
            "health": "/health"
        },
        "documentation": "/docs"
    }

@app.get("/health")
def health_check():
    """Sistem sağlık kontrolü"""
    try:
        model, preprocessor, feature_names = load_model()
        return {
            "status": "healthy",
            "model_loaded": True,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "model_loaded": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.post("/api/v1/predict", response_model=PredictionResponse)
def predict(project: ProjectInput):
    """
    Basit maliyet tahmini
    
    SAP, Oracle veya diğer ERP sistemlerinden gelen verilerle
    hızlı tahmin yapar.
    """
    model, preprocessor, feature_names = load_model()
    
    X_new = np.array([[
        project.project_duration,
        project.team_size,
        project.complexity,
        project.tech_cost,
        project.location_factor,
        project.experience_level,
        project.risk_factor
    ]])
    
    X_new_norm = preprocessor.normalize(X_new, fit=False)
    y_pred_norm = model.predict(X_new_norm)
    predicted_cost = preprocessor.denormalize(y_pred_norm, is_target=True)[0, 0]
    
    monte_carlo = SensitivityAnalysis.monte_carlo_simulation(predicted_cost, volatility=0.15)
    
    return PredictionResponse(
        predicted_cost=float(predicted_cost),
        confidence_interval_90={
            "lower": float(monte_carlo['p10']),
            "upper": float(monte_carlo['p90'])
        },
        confidence_interval_95={
            "lower": float(monte_carlo['confidence_95_lower']),
            "upper": float(monte_carlo['confidence_95_upper'])
        },
        timestamp=datetime.now().isoformat()
    )

@app.post("/api/v1/detailed-analysis", response_model=DetailedAnalysisResponse)
def detailed_analysis(project: ProjectInput, financial: FinancialInput):
    """
    Detaylı finansal analiz
    
    NPV, IRR, ROI, vergi sonrası analiz dahil
    tam finansal değerlendirme.
    """
    model, preprocessor, feature_names = load_model()
    
    X_new = np.array([[
        project.project_duration,
        project.team_size,
        project.complexity,
        project.tech_cost,
        project.location_factor,
        project.experience_level,
        project.risk_factor
    ]])
    
    X_new_norm = preprocessor.normalize(X_new, fit=False)
    y_pred_norm = model.predict(X_new_norm)
    predicted_cost = preprocessor.denormalize(y_pred_norm, is_target=True)[0, 0]
    
    roi = None
    npv = None
    after_tax_npv = None
    irr_value = None
    break_even = None
    
    if financial.expected_revenue:
        roi = EngineeringEconomics.roi(financial.expected_revenue, predicted_cost)
        
        monthly_revenue = financial.expected_revenue / project.project_duration
        cash_flows = [-predicted_cost]
        for _ in range(int(project.project_duration)):
            cash_flows.append(monthly_revenue)
        
        npv = EngineeringEconomics.npv(cash_flows, financial.discount_rate / 12)
        
        irr_value = EngineeringEconomics.irr(cash_flows)
        if irr_value is None:
            print("IRR hesaplanamadı — nakit akışları yakınsamaya uygun değil")
        
        if monthly_revenue > 0:
            break_even = predicted_cost / monthly_revenue
        
        tax_analysis = AdvancedEconomics.project_npv_with_taxes(
            initial_investment=predicted_cost,
            annual_revenue=financial.expected_revenue / (project.project_duration / 12),
            annual_operating_cost=0,
            project_life=project.project_duration / 12,
            discount_rate=financial.discount_rate,
            tax_rate=financial.tax_rate,
            depreciation_method=financial.depreciation_method,
            inflation_rate=financial.inflation_rate
        )
        
        after_tax_npv = tax_analysis['after_tax_npv']
    
    risk_assessment = SensitivityAnalysis.risk_assessment(
        predicted_cost,
        financial.expected_revenue if financial.expected_revenue else predicted_cost * 1.5
    )
    
    scenarios = SensitivityAnalysis.scenario_analysis(predicted_cost)
    
    contributions = ExplainableAI.calculate_feature_contributions(
        model, preprocessor, X_new, feature_names
    )
    explanation = ExplainableAI.generate_explanation_text(contributions, top_n=5)
    
    return DetailedAnalysisResponse(
        predicted_cost=float(predicted_cost),
        roi=float(roi) if roi is not None else None,
        npv=float(npv) if npv is not None else None,
        after_tax_npv=float(after_tax_npv) if after_tax_npv is not None else None,
        irr=float(irr_value) if irr_value is not None else None,
        break_even_months=float(break_even) if break_even is not None else None,
        risk_assessment={
            "risk_level": risk_assessment['risk_level'],
            "probability_of_profit": float(risk_assessment['probability_of_profit']),
            "recommendation": risk_assessment['recommendation']
        },
        scenarios={
            "optimistic": float(scenarios['optimistic']['cost']),
            "expected": float(scenarios['expected']['cost']),
            "pessimistic": float(scenarios['pessimistic']['cost']),
            "expected_value": float(scenarios['expected_value'])
        },
        explanation=explanation,
        timestamp=datetime.now().isoformat()
    )

@app.post("/api/v1/sensitivity", response_model=SensitivityResponse)
def sensitivity_analysis(project: ProjectInput):
    """
    Duyarlılık analizi
    
    Her parametrenin maliyet üzerindeki etkisini hesaplar.
    """
    model, preprocessor, feature_names = load_model()
    
    X_new = np.array([[
        project.project_duration,
        project.team_size,
        project.complexity,
        project.tech_cost,
        project.location_factor,
        project.experience_level,
        project.risk_factor
    ]])
    
    X_new_norm = preprocessor.normalize(X_new, fit=False)
    y_pred_norm = model.predict(X_new_norm)
    predicted_cost = preprocessor.denormalize(y_pred_norm, is_target=True)[0, 0]
    
    tornado_data = SensitivityAnalysis.tornado_chart_data(
        model, preprocessor, X_new, feature_names
    )
    
    parameter_sensitivities = {}
    for i, feature_name in enumerate(feature_names):
        sensitivity = SensitivityAnalysis.sensitivity_to_parameter(
            model, preprocessor, X_new, i, feature_name
        )
        parameter_sensitivities[feature_name] = {
            "elasticity": float(sensitivity['elasticity']),
            "cost_change_pct": float(sensitivity['cost_change_pct']),
            "base_value": float(sensitivity['base_value'])
        }
    
    return SensitivityResponse(
        base_cost=float(predicted_cost),
        tornado_data=[
            {
                "feature": item['feature'],
                "impact": float(item['impact']),
                "elasticity": float(item['elasticity'])
            }
            for item in tornado_data
        ],
        parameter_sensitivities=parameter_sensitivities,
        timestamp=datetime.now().isoformat()
    )

@app.post("/api/v1/explain")
def explain_prediction(project: ProjectInput):
    """
    Açıklanabilir AI - Tahminin nedenleri
    
    SHAP-benzeri özellik katkı analizi.
    """
    model, preprocessor, feature_names = load_model()
    
    X_new = np.array([[
        project.project_duration,
        project.team_size,
        project.complexity,
        project.tech_cost,
        project.location_factor,
        project.experience_level,
        project.risk_factor
    ]])
    
    contributions = ExplainableAI.calculate_feature_contributions(
        model, preprocessor, X_new, feature_names
    )
    
    explanation_text = ExplainableAI.generate_explanation_text(contributions, top_n=7)
    
    waterfall_data = ExplainableAI.create_waterfall_data(contributions)
    
    return {
        "predicted_cost": float(contributions['base_prediction']),
        "baseline_cost": float(contributions['baseline_prediction']),
        "explanation_text": explanation_text,
        "feature_contributions": {
            feature: {
                "contribution": float(data['contribution']),
                "percentage": float(data['percentage']),
                "importance": float(data['importance']),
                "value": float(data['value'])
            }
            for feature, data in contributions['contributions'].items()
        },
        "waterfall_chart_data": waterfall_data,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/v1/counterfactual")
def counterfactual_analysis(project: ProjectInput, target_cost: float):
    """
    Counterfactual analiz: "X maliyete ulaşmak için ne değişmeli?"
    """
    model, preprocessor, feature_names = load_model()
    
    X_new = np.array([[
        project.project_duration,
        project.team_size,
        project.complexity,
        project.tech_cost,
        project.location_factor,
        project.experience_level,
        project.risk_factor
    ]])
    
    result = ExplainableAI.counterfactual_explanation(
        model, preprocessor, X_new, feature_names, target_cost
    )
    
    return {
        "success": result['success'],
        "target_cost": float(result['target_cost']),
        "achieved_cost": float(result['achieved_cost']),
        "original_cost": float(result['original_cost']),
        "suggested_changes": {
            feature: {
                "original": float(data['original']),
                "suggested": float(data['suggested']),
                "change_pct": float(data['change_pct'])
            }
            for feature, data in result['changes'].items()
        },
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/v1/model-info")
def model_info():
    """Model bilgileri"""
    model, preprocessor, feature_names = load_model()
    
    return {
        "model_type": "Neural Network (Custom Implementation)",
        "architecture": "7 -> 64 -> 32 -> 16 -> 1",
        "features": feature_names,
        "accuracy": "⚠️ SENTETIK VERİ - Gerçek projelerle test edilmedi",
        "training_samples": 2000,
        "version": "1.0.0-beta",
        "last_trained": "2026-04-08",
        "warning": "Bu model demo amaçlıdır. Gerçek proje kararları için kullanmadan önce gerçek verilerle yeniden eğitilmelidir."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
