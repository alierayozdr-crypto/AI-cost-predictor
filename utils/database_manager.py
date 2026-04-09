"""
Veritabanı bağlantı yöneticisi
financial_modeling.py için DB desteği
"""

import sqlite3
import pandas as pd
from typing import List, Dict, Optional
from datetime import datetime
import os

class DatabaseManager:
    """
    Finansal analiz sonuçlarını kaydetme ve yönetme
    """
    
    def __init__(self, db_path='data/financial_analysis.db'):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._initialize_database()
    
    def _initialize_database(self):
        """Veritabanı tablolarını oluştur"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS financial_evaluations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_name TEXT NOT NULL,
                evaluation_date TEXT NOT NULL,
                initial_investment REAL,
                total_revenue REAL,
                total_cost REAL,
                roi_percentage REAL,
                payback_months INTEGER,
                probability_of_profit REAL,
                risk_level TEXT,
                npv REAL,
                recommendation TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS monthly_cash_flows (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                evaluation_id INTEGER,
                month INTEGER,
                revenue REAL,
                cost REAL,
                profit REAL,
                cumulative_profit REAL,
                FOREIGN KEY (evaluation_id) REFERENCES financial_evaluations(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_evaluation(self, evaluation: Dict) -> int:
        """
        Finansal değerlendirmeyi kaydet
        
        Args:
            evaluation: business_case_evaluation çıktısı
        
        Returns:
            int: Evaluation ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        roi = evaluation['roi_analysis']
        risk = evaluation['risk_analysis']
        npv = evaluation['npv_analysis']
        
        cursor.execute('''
            INSERT INTO financial_evaluations (
                project_name, evaluation_date, initial_investment,
                total_revenue, total_cost, roi_percentage, payback_months,
                probability_of_profit, risk_level, npv, recommendation
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            evaluation['project_name'],
            evaluation['evaluation_date'],
            roi['initial_investment'],
            roi['total_revenue'],
            roi['total_cost'],
            roi['roi_percentage'],
            roi['payback_months'],
            risk['probability_of_profit'],
            risk['risk_level'],
            npv['npv'],
            evaluation['recommendation']
        ))
        
        evaluation_id = cursor.lastrowid
        
        # Aylık nakit akışlarını kaydet
        for month, (profit, cum_profit) in enumerate(zip(
            roi['monthly_profits'], 
            roi['cumulative_profit']
        ), 1):
            revenue = roi['monthly_revenues'][month-1]
            cost = revenue - profit
            
            cursor.execute('''
                INSERT INTO monthly_cash_flows (
                    evaluation_id, month, revenue, cost, profit, cumulative_profit
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (evaluation_id, month, revenue, cost, profit, cum_profit))
        
        conn.commit()
        conn.close()
        
        return evaluation_id
    
    def get_evaluation(self, evaluation_id: int) -> Optional[Dict]:
        """Değerlendirmeyi getir"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM financial_evaluations WHERE id = ?', (evaluation_id,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return None
        
        cursor.execute('SELECT * FROM monthly_cash_flows WHERE evaluation_id = ?', (evaluation_id,))
        cash_flows = cursor.fetchall()
        
        conn.close()
        
        return {
            'id': row[0],
            'project_name': row[1],
            'evaluation_date': row[2],
            'initial_investment': row[3],
            'total_revenue': row[4],
            'total_cost': row[5],
            'roi_percentage': row[6],
            'payback_months': row[7],
            'probability_of_profit': row[8],
            'risk_level': row[9],
            'npv': row[10],
            'recommendation': row[11],
            'cash_flows': [
                {
                    'month': cf[2],
                    'revenue': cf[3],
                    'cost': cf[4],
                    'profit': cf[5],
                    'cumulative_profit': cf[6]
                }
                for cf in cash_flows
            ]
        }
    
    def list_evaluations(self, limit: int = 10) -> List[Dict]:
        """Son değerlendirmeleri listele"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, project_name, evaluation_date, roi_percentage, 
                   payback_months, risk_level, recommendation
            FROM financial_evaluations
            ORDER BY created_at DESC
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': row[0],
                'project_name': row[1],
                'evaluation_date': row[2],
                'roi_percentage': row[3],
                'payback_months': row[4],
                'risk_level': row[5],
                'recommendation': row[6]
            }
            for row in rows
        ]
