"""
Güvenlik ve Kimlik Doğrulama Modülü
JWT token, API key, role-based access control
"""

from datetime import datetime, timedelta
from typing import Optional, Dict
from passlib.context import CryptContext
from jose import JWTError, jwt
import secrets
import hashlib
from enum import Enum

SECRET_KEY = "your-secret-key-change-in-production-use-env-variable"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
API_KEY_EXPIRE_DAYS = 365

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRole(str, Enum):
    """Kullanıcı rolleri"""
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"
    API_CLIENT = "api_client"

class User:
    """Kullanıcı modeli"""
    def __init__(self, username: str, email: str, role: UserRole, 
                 company: str = None, hashed_password: str = None):
        self.username = username
        self.email = email
        self.role = role
        self.company = company
        self.hashed_password = hashed_password
        self.is_active = True
        self.created_at = datetime.now()
        self.api_key = None
        self.api_key_hash = None

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Şifre doğrulama"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Şifre hash'leme"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    JWT access token oluştur
    
    Args:
        data: Token'a eklenecek veri (user_id, role, vb.)
        expires_delta: Token geçerlilik süresi
    
    Returns:
        JWT token string
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def verify_token(token: str) -> Optional[Dict]:
    """
    JWT token doğrulama
    
    Args:
        token: JWT token
    
    Returns:
        Token payload veya None
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def generate_api_key() -> str:
    """
    API key oluştur
    
    Returns:
        API key (32 karakter hex)
    """
    return secrets.token_hex(32)

def hash_api_key(api_key: str) -> str:
    """
    API key'i hash'le (veritabanında saklamak için)
    
    Args:
        api_key: Plain API key
    
    Returns:
        Hashed API key
    """
    return hashlib.sha256(api_key.encode()).hexdigest()

def verify_api_key(plain_api_key: str, hashed_api_key: str) -> bool:
    """
    API key doğrulama
    
    Args:
        plain_api_key: Gelen API key
        hashed_api_key: Veritabanındaki hash'lenmiş key
    
    Returns:
        Doğrulama sonucu
    """
    return hash_api_key(plain_api_key) == hashed_api_key

def check_permission(user_role: UserRole, required_role: UserRole) -> bool:
    """
    Rol bazlı yetki kontrolü
    
    Hiyerarşi: ADMIN > MANAGER > USER > API_CLIENT
    
    Args:
        user_role: Kullanıcının rolü
        required_role: Gerekli minimum rol
    
    Returns:
        Yetki var mı?
    """
    role_hierarchy = {
        UserRole.ADMIN: 4,
        UserRole.MANAGER: 3,
        UserRole.USER: 2,
        UserRole.API_CLIENT: 1
    }
    
    return role_hierarchy.get(user_role, 0) >= role_hierarchy.get(required_role, 0)

class RateLimiter:
    """
    Rate limiting - API kötüye kullanımını önler
    """
    
    def __init__(self):
        self.requests = {}
    
    def check_rate_limit(self, user_id: str, max_requests: int = 100, 
                        window_seconds: int = 3600) -> bool:
        """
        Rate limit kontrolü
        
        Args:
            user_id: Kullanıcı ID
            max_requests: Maksimum istek sayısı
            window_seconds: Zaman penceresi (saniye)
        
        Returns:
            İstek yapılabilir mi?
        """
        now = datetime.now()
        
        if user_id not in self.requests:
            self.requests[user_id] = []
        
        self.requests[user_id] = [
            req_time for req_time in self.requests[user_id]
            if (now - req_time).total_seconds() < window_seconds
        ]
        
        if len(self.requests[user_id]) >= max_requests:
            return False
        
        self.requests[user_id].append(now)
        return True

class AuditLog:
    """
    Denetim kaydı - Tüm API çağrılarını logla
    """
    
    @staticmethod
    def log_api_call(user_id: str, endpoint: str, method: str, 
                     status_code: int, response_time: float):
        """
        API çağrısını logla
        
        Args:
            user_id: Kullanıcı ID
            endpoint: API endpoint
            method: HTTP method
            status_code: Response status
            response_time: Yanıt süresi (ms)
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'endpoint': endpoint,
            'method': method,
            'status_code': status_code,
            'response_time_ms': response_time
        }
        
        print(f"[AUDIT] {log_entry}")

def validate_company_data_isolation(user_company: str, data_company: str) -> bool:
    """
    Multi-tenancy: Şirket verisi izolasyonu
    
    Bir şirketin verisi başka şirkete görünmemeli
    
    Args:
        user_company: Kullanıcının şirketi
        data_company: Erişilmek istenen verinin şirketi
    
    Returns:
        Erişim izni var mı?
    """
    return user_company == data_company
