"""
Kullanıcı ve şirket veritabanı yönetimi
PostgreSQL veya SQLite
"""

import sqlite3
from datetime import datetime
from typing import Optional, List
from .security import User, UserRole, get_password_hash, hash_api_key
import os

class UserDatabase:
    """Kullanıcı veritabanı yönetimi"""
    
    def __init__(self, db_path='data/users.db'):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._initialize_database()
    
    def _initialize_database(self):
        """Veritabanı tablolarını oluştur"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                hashed_password TEXT NOT NULL,
                role TEXT NOT NULL,
                company_id INTEGER,
                is_active BOOLEAN DEFAULT 1,
                created_at TEXT,
                last_login TEXT,
                api_key_hash TEXT,
                api_key_created_at TEXT,
                subscription_plan TEXT DEFAULT 'free',
                subscription_expires TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                industry TEXT,
                size TEXT,
                created_at TEXT,
                subscription_plan TEXT DEFAULT 'trial',
                subscription_expires TEXT,
                max_users INTEGER DEFAULT 5,
                max_api_calls_per_month INTEGER DEFAULT 1000,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                company_id INTEGER,
                endpoint TEXT,
                timestamp TEXT,
                response_time_ms REAL,
                status_code INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (company_id) REFERENCES companies(id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_id INTEGER,
                plan TEXT NOT NULL,
                price REAL,
                start_date TEXT,
                end_date TEXT,
                is_active BOOLEAN DEFAULT 1,
                FOREIGN KEY (company_id) REFERENCES companies(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_user(self, username: str, email: str, password: str, 
                   role: UserRole, company_id: Optional[int] = None) -> int:
        """
        Yeni kullanıcı oluştur
        
        Returns:
            User ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        hashed_password = get_password_hash(password)
        
        cursor.execute('''
            INSERT INTO users (username, email, hashed_password, role, company_id, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (username, email, hashed_password, role.value, company_id, datetime.now().isoformat()))
        
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return user_id
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Kullanıcıyı username ile bul"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return User(
                username=row[1],
                email=row[2],
                role=UserRole(row[4]),
                company=str(row[5]) if row[5] else None,
                hashed_password=row[3]
            )
        return None
    
    def get_user_by_api_key(self, api_key_hash: str) -> Optional[User]:
        """API key ile kullanıcı bul"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE api_key_hash = ?', (api_key_hash,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return User(
                username=row[1],
                email=row[2],
                role=UserRole(row[4]),
                company=str(row[5]) if row[5] else None,
                hashed_password=row[3]
            )
        return None
    
    def update_api_key(self, user_id: int, api_key_hash: str):
        """Kullanıcının API key'ini güncelle"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users 
            SET api_key_hash = ?, api_key_created_at = ?
            WHERE id = ?
        ''', (api_key_hash, datetime.now().isoformat(), user_id))
        
        conn.commit()
        conn.close()
    
    def create_company(self, name: str, industry: str = None, 
                      size: str = None, subscription_plan: str = 'trial') -> int:
        """
        Yeni şirket oluştur
        
        Returns:
            Company ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO companies (name, industry, size, created_at, subscription_plan)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, industry, size, datetime.now().isoformat(), subscription_plan))
        
        company_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return company_id
    
    def log_api_usage(self, user_id: int, company_id: int, endpoint: str, 
                     response_time_ms: float, status_code: int):
        """API kullanımını logla"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO api_usage (user_id, company_id, endpoint, timestamp, response_time_ms, status_code)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, company_id, endpoint, datetime.now().isoformat(), response_time_ms, status_code))
        
        conn.commit()
        conn.close()
    
    def get_monthly_api_usage(self, company_id: int) -> int:
        """Şirketin aylık API kullanımını getir"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT COUNT(*) FROM api_usage
            WHERE company_id = ? 
            AND datetime(timestamp) > datetime('now', '-30 days')
        ''', (company_id,))
        
        count = cursor.fetchone()[0]
        conn.close()
        
        return count
    
    def check_subscription_valid(self, company_id: int) -> bool:
        """Şirket aboneliği geçerli mi?"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT subscription_expires FROM companies
            WHERE id = ?
        ''', (company_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row or not row[0]:
            return False
        
        expires = datetime.fromisoformat(row[0])
        return expires > datetime.now()
