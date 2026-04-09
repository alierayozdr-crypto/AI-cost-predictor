"""
Güvenli API - JWT Authentication, Rate Limiting, Multi-tenancy
"""

from fastapi import FastAPI, HTTPException, Depends, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import numpy as np
import pickle
import sys
import os
from datetime import datetime, timedelta
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from neural_network.network import NeuralNetwork
from utils.explainable_ai import ExplainableAI
from auth.security import (
    verify_token, verify_api_key, hash_api_key, create_access_token,
    verify_password, UserRole, check_permission, RateLimiter
)
from auth.database import UserDatabase

app = FastAPI(
    title="AI Maliyet Tahmin API (Secure)",
    description="Güvenli, çok kiracılı, kimlik doğrulamalı API",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://localhost:3000", "https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

security = HTTPBearer()
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

db = UserDatabase()
rate_limiter = RateLimiter()

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 1800

class ProjectInput(BaseModel):
    project_duration: float = Field(..., ge=1, le=36)
    team_size: int = Field(..., ge=2, le=50)
    complexity: float = Field(..., ge=1, le=10)
    tech_cost: float = Field(..., ge=10000, le=10000000)
    location_factor: float = Field(..., ge=1, le=3)
    experience_level: float = Field(..., ge=1, le=5)
    risk_factor: float = Field(..., ge=0, le=1)

def load_model():
    """Model yükle"""
    try:
        model = NeuralNetwork()
        model.load('models/cost_prediction_model.pkl')
        
        with open('models/preprocessor.pkl', 'rb') as f:
            preprocessor = pickle.load(f)
        
        with open('models/feature_names.pkl', 'rb') as f:
            feature_names = pickle.load(f)
        
        return model, preprocessor, feature_names
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Model bulunamadı")

async def get_current_user_from_token(
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    """JWT token ile kullanıcı doğrulama"""
    token = credentials.credentials
    payload = verify_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Geçersiz veya süresi dolmuş token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Geçersiz token")
    
    user = db.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=401, detail="Kullanıcı bulunamadı")
    
    return user

async def get_current_user_from_api_key(
    api_key: str = Security(api_key_header)
):
    """API key ile kullanıcı doğrulama"""
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key gerekli",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    
    api_key_hash = hash_api_key(api_key)
    user = db.get_user_by_api_key(api_key_hash)
    
    if not user:
        raise HTTPException(status_code=401, detail="Geçersiz API key")
    
    return user

async def check_rate_limit(user):
    """Rate limit kontrolü"""
    if not rate_limiter.check_rate_limit(user.username, max_requests=100, window_seconds=3600):
        raise HTTPException(
            status_code=429,
            detail="Rate limit aşıldı. Lütfen 1 saat sonra tekrar deneyin."
        )

async def check_subscription(user):
    """Abonelik kontrolü"""
    if user.company:
        company_id = int(user.company)
        if not db.check_subscription_valid(company_id):
            raise HTTPException(
                status_code=402,
                detail="Abonelik süresi dolmuş. Lütfen yenileyin."
            )

@app.post("/auth/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """
    Kullanıcı girişi - JWT token al
    """
    user = db.get_user_by_username(request.username)
    
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Kullanıcı adı veya şifre hatalı",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Kullanıcı aktif değil")
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role.value},
        expires_delta=access_token_expires
    )
    
    return TokenResponse(
        access_token=access_token,
        expires_in=1800
    )

@app.post("/auth/api-key")
async def generate_api_key(current_user = Depends(get_current_user_from_token)):
    """
    API key oluştur
    
    Requires: JWT token
    """
    from auth.security import generate_api_key
    
    api_key = generate_api_key()
    api_key_hash = hash_api_key(api_key)
    
    db.update_api_key(current_user.username, api_key_hash)
    
    return {
        "api_key": api_key,
        "message": "API key oluşturuldu. Bu key'i güvenli bir yerde saklayın.",
        "warning": "Bu key bir daha gösterilmeyecek!"
    }

@app.get("/")
async def root():
    """API ana sayfası"""
    return {
        "message": "AI Maliyet Tahmin API (Secure)",
        "version": "2.0.0",
        "authentication": {
            "jwt": "POST /auth/login ile token alın",
            "api_key": "X-API-Key header ile kullanın"
        },
        "documentation": "/docs"
    }

@app.get("/health")
async def health_check():
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
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.post("/api/v2/predict")
async def predict_secure(
    project: ProjectInput,
    current_user = Depends(get_current_user_from_api_key)
):
    """
    Güvenli maliyet tahmini
    
    Requires: API Key (X-API-Key header)
    """
    start_time = time.time()
    
    await check_rate_limit(current_user)
    await check_subscription(current_user)
    
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
    
    response_time = (time.time() - start_time) * 1000
    
    if current_user.company:
        db.log_api_usage(
            user_id=1,
            company_id=int(current_user.company),
            endpoint="/api/v2/predict",
            response_time_ms=response_time,
            status_code=200
        )
    
    return {
        "predicted_cost": float(predicted_cost),
        "user": current_user.username,
        "company": current_user.company,
        "timestamp": datetime.now().isoformat(),
        "response_time_ms": response_time
    }

@app.post("/api/v2/explain")
async def explain_prediction(
    project: ProjectInput,
    current_user = Depends(get_current_user_from_api_key)
):
    """
    Açıklanabilir AI - Güvenli
    
    Requires: API Key
    """
    await check_rate_limit(current_user)
    await check_subscription(current_user)
    
    if not check_permission(current_user.role, UserRole.USER):
        raise HTTPException(status_code=403, detail="Yetersiz yetki")
    
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
    
    return {
        "predicted_cost": float(contributions['base_prediction']),
        "explanation_text": explanation_text,
        "feature_contributions": {
            feature: {
                "contribution": float(data['contribution']),
                "percentage": float(data['percentage']),
                "importance": float(data['importance'])
            }
            for feature, data in contributions['contributions'].items()
        },
        "user": current_user.username,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/v2/usage")
async def get_usage_stats(current_user = Depends(get_current_user_from_token)):
    """
    Kullanım istatistikleri
    
    Requires: JWT token
    """
    if not current_user.company:
        return {"message": "Şirket bilgisi yok"}
    
    company_id = int(current_user.company)
    monthly_usage = db.get_monthly_api_usage(company_id)
    
    return {
        "company_id": company_id,
        "monthly_api_calls": monthly_usage,
        "user": current_user.username,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/v2/admin/users")
async def list_users(current_user = Depends(get_current_user_from_token)):
    """
    Kullanıcı listesi (Admin only)
    
    Requires: JWT token, ADMIN role
    """
    if not check_permission(current_user.role, UserRole.ADMIN):
        raise HTTPException(status_code=403, detail="Sadece admin erişebilir")
    
    return {"message": "Admin endpoint - Kullanıcı listesi"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
