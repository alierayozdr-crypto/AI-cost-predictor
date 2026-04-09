import numpy as np
import sqlite3
import pickle
from datetime import datetime
import os
try:
    import psycopg2
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False

class ContinuousLearning:
    """
    Sürekli Öğrenme Sistemi (Continuous Learning / Feedback Loop)
    
    Gerçek proje sonuçlarını toplayarak modeli sürekli iyileştirir.
    Data drift'e karşı koruma sağlar.
    """
    
    def __init__(self, db_path='data/feedback.db', pg_conn_string=None):
        self.pg_conn_string = pg_conn_string or os.getenv('DATABASE_URL')
        if self.pg_conn_string and POSTGRES_AVAILABLE:
            # PostgreSQL modu
            self.use_postgres = True
        else:
            # Geliştirme ortamı için SQLite fallback
            self.use_postgres = False
            self.db_path = db_path
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._initialize_database()
    
    def _initialize_database(self):
        """Veritabanını oluştur"""
        if self.use_postgres:
            # PostgreSQL - schema.sql'deki predictions tablosunu kullan
            # Tablo zaten var, ek işlem gerekmez
            return
        
        # SQLite fallback
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS project_feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_name TEXT,
                predicted_cost REAL,
                actual_cost REAL,
                prediction_error REAL,
                error_percentage REAL,
                project_duration REAL,
                team_size INTEGER,
                complexity REAL,
                tech_cost REAL,
                location_factor REAL,
                experience_level REAL,
                risk_factor REAL,
                feedback_date TEXT,
                notes TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS model_versions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                version TEXT,
                training_date TEXT,
                samples_count INTEGER,
                accuracy_r2 REAL,
                mape REAL,
                notes TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS retraining_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                retrain_date TEXT,
                samples_used INTEGER,
                new_accuracy REAL,
                improvement REAL,
                status TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_feedback(self, project_name, predicted_cost, actual_cost,
                    project_params, notes=""):
        """
        Proje geri bildirimi ekle
        
        Args:
            project_name: Proje adı
            predicted_cost: Tahmin edilen maliyet
            actual_cost: Gerçekleşen maliyet
            project_params: Proje parametreleri (dict)
            notes: Notlar
        
        Returns:
            int: Feedback ID
        """
        prediction_error = actual_cost - predicted_cost
        error_percentage = (prediction_error / actual_cost * 100) if actual_cost > 0 else 0
        
        if self.use_postgres:
            # PostgreSQL - predictions tablosuna ekle
            conn = psycopg2.connect(self.pg_conn_string)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO predictions (
                    project_name, predicted_cost, actual_cost, prediction_error,
                    error_percentage, project_duration, team_size, complexity,
                    tech_cost, location_factor, experience_level, risk_factor,
                    created_at, notes
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            ''', (
                project_name,
                predicted_cost,
                actual_cost,
                prediction_error,
                error_percentage,
                project_params.get('project_duration'),
                project_params.get('team_size'),
                project_params.get('complexity'),
                project_params.get('tech_cost'),
                project_params.get('location_factor'),
                project_params.get('experience_level'),
                project_params.get('risk_factor'),
                datetime.now(),
                notes
            ))
            
            feedback_id = cursor.fetchone()[0]
            conn.commit()
            conn.close()
        else:
            # SQLite fallback
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO project_feedback (
                    project_name, predicted_cost, actual_cost, prediction_error,
                    error_percentage, project_duration, team_size, complexity,
                    tech_cost, location_factor, experience_level, risk_factor,
                    feedback_date, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                project_name,
                predicted_cost,
                actual_cost,
                prediction_error,
                error_percentage,
                project_params.get('project_duration'),
                project_params.get('team_size'),
                project_params.get('complexity'),
                project_params.get('tech_cost'),
                project_params.get('location_factor'),
                project_params.get('experience_level'),
                project_params.get('risk_factor'),
                datetime.now().isoformat(),
                notes
            ))
            
            feedback_id = cursor.lastrowid
            conn.commit()
            conn.close()
        
        return feedback_id
    
    def get_feedback_statistics(self):
        """
        Geri bildirim istatistiklerini al
        
        Returns:
            dict: İstatistikler
        """
        if self.use_postgres:
            # PostgreSQL — şimdilik pass, sonraki versiyonda implement edilecek
            return {
                'total_feedback': 0,
                'average_error_pct': 0,
                'average_predicted_cost': 0,
                'average_actual_cost': 0,
                'accurate_predictions': 0,
                'poor_predictions': 0,
                'accuracy_rate': 0,
                'needs_retraining': False
            }
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM project_feedback')
        total_feedback = cursor.fetchone()[0]
        
        cursor.execute('SELECT AVG(ABS(error_percentage)) FROM project_feedback')
        avg_error = cursor.fetchone()[0] or 0
        
        cursor.execute('SELECT AVG(predicted_cost), AVG(actual_cost) FROM project_feedback')
        avg_costs = cursor.fetchone()
        
        cursor.execute('''
            SELECT COUNT(*) FROM project_feedback 
            WHERE ABS(error_percentage) < 10
        ''')
        accurate_predictions = cursor.fetchone()[0]
        
        cursor.execute('''
            SELECT COUNT(*) FROM project_feedback 
            WHERE ABS(error_percentage) > 20
        ''')
        poor_predictions = cursor.fetchone()[0]
        
        conn.close()
        
        accuracy_rate = (accurate_predictions / total_feedback * 100) if total_feedback > 0 else 0
        
        return {
            'total_feedback': total_feedback,
            'average_error_pct': avg_error,
            'average_predicted_cost': avg_costs[0] or 0,
            'average_actual_cost': avg_costs[1] or 0,
            'accurate_predictions': accurate_predictions,
            'poor_predictions': poor_predictions,
            'accuracy_rate': accuracy_rate,
            'needs_retraining': avg_error > 15 or total_feedback > 50
        }
    
    def get_feedback_data_for_training(self, min_samples=20):
        """
        Eğitim için geri bildirim verilerini al
        
        Args:
            min_samples: Minimum örnek sayısı
        
        Returns:
            tuple: (X, y) veya None
        """
        if self.use_postgres:
            # PostgreSQL — şimdilik pass, sonraki versiyonda implement edilecek
            return None, None
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM project_feedback')
        count = cursor.fetchone()[0]
        
        if count < min_samples:
            conn.close()
            return None, None
        
        cursor.execute('''
            SELECT project_duration, team_size, complexity, tech_cost,
                   location_factor, experience_level, risk_factor, actual_cost
            FROM project_feedback
            ORDER BY feedback_date DESC
        ''')
        
        data = cursor.fetchall()
        conn.close()
        
        X = np.array([[row[0], row[1], row[2], row[3], row[4], row[5], row[6]] 
                      for row in data])
        y = np.array([[row[7]] for row in data])
        
        return X, y
    
    def incremental_training(self, model, preprocessor, learning_rate=0.001, epochs=100):
        """
        Artımlı eğitim - mevcut modeli yeni verilerle güncelle
        
        Args:
            model: Mevcut model
            preprocessor: Veri ön işleyici
            learning_rate: Öğrenme oranı
            epochs: Epoch sayısı
        
        Returns:
            dict: Eğitim sonuçları
        """
        X_new, y_new = self.get_feedback_data_for_training(min_samples=20)
        
        if X_new is None:
            return {
                'success': False,
                'message': 'Yetersiz geri bildirim verisi (minimum 20 gerekli)'
            }
        
        X_new_norm = preprocessor.normalize(X_new, fit=False)
        y_new_norm = preprocessor.normalize_target(y_new, fit=False)
        
        initial_metrics = model.evaluate(X_new_norm, y_new_norm)
        initial_mse = initial_metrics['mse']
        
        model.train(
            X_new_norm, y_new_norm,
            epochs=epochs,
            learning_rate=learning_rate,
            batch_size=min(16, len(X_new)),
            verbose=False
        )
        
        final_metrics = model.evaluate(X_new_norm, y_new_norm)
        final_mse = final_metrics['mse']
        
        improvement = ((initial_mse - final_mse) / initial_mse * 100) if initial_mse > 0 else 0
        
        if self.use_postgres:
            # PostgreSQL — şimdilik pass, sonraki versiyonda implement edilecek
            return {
                'success': True,
                'samples_used': len(X_new),
                'initial_mse': initial_mse,
                'final_mse': final_mse,
                'improvement_pct': improvement,
                'new_r2': final_metrics['r2'],
                'new_mape': (final_metrics['mae'] / np.mean(y_new)) * 100
            }
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO retraining_log (
                retrain_date, samples_used, new_accuracy, improvement, status
            ) VALUES (?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            len(X_new),
            final_metrics['r2'],
            improvement,
            'success'
        ))
        conn.commit()
        conn.close()
        
        return {
            'success': True,
            'samples_used': len(X_new),
            'initial_mse': initial_mse,
            'final_mse': final_mse,
            'improvement_pct': improvement,
            'new_r2': final_metrics['r2'],
            'new_mape': (final_metrics['mae'] / np.mean(y_new)) * 100
        }
    
    def detect_data_drift(self, current_data, threshold=0.15):
        """
        Veri kayması (data drift) tespit et
        
        Args:
            current_data: Mevcut veri dağılımı
            threshold: Kayma eşiği
        
        Returns:
            dict: Kayma analizi
        """
        if self.use_postgres:
            # PostgreSQL — şimdilik pass, sonraki versiyonda implement edilecek
            return {
                'drift_detected': False,
                'message': 'PostgreSQL modu - veri kayması tespiti henüz implement edilmedi'
            }
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT AVG(project_duration), AVG(team_size), AVG(complexity),
                   AVG(tech_cost), AVG(location_factor), AVG(experience_level),
                   AVG(risk_factor)
            FROM project_feedback
        ''')
        
        historical_means = cursor.fetchone()
        conn.close()
        
        if not historical_means or historical_means[0] is None:
            return {
                'drift_detected': False,
                'message': 'Yetersiz geçmiş veri'
            }
        
        historical_means = np.array(historical_means)
        current_means = np.mean(current_data, axis=0)
        
        relative_changes = np.abs((current_means - historical_means) / (historical_means + 1e-10))
        
        drift_detected = np.any(relative_changes > threshold)
        
        feature_names = [
            'Proje Süresi', 'Ekip Büyüklüğü', 'Karmaşıklık',
            'Teknoloji Maliyeti', 'Lokasyon Faktörü', 'Deneyim', 'Risk'
        ]
        
        drifted_features = []
        for i, change in enumerate(relative_changes):
            if change > threshold:
                drifted_features.append({
                    'feature': feature_names[i],
                    'change_pct': float(change * 100),
                    'historical_mean': float(historical_means[i]),
                    'current_mean': float(current_means[i])
                })
        
        return {
            'drift_detected': drift_detected,
            'drifted_features': drifted_features,
            'max_drift_pct': float(np.max(relative_changes) * 100),
            'recommendation': 'Model yeniden eğitilmeli' if drift_detected else 'Model güncel'
        }
    
    def get_recent_feedback(self, limit=10):
        """
        Son geri bildirimleri al
        
        Args:
            limit: Kaç kayıt
        
        Returns:
            list: Geri bildirimler
        """
        if self.use_postgres:
            # PostgreSQL — şimdilik pass, sonraki versiyonda implement edilecek
            return []
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT project_name, predicted_cost, actual_cost, 
                   error_percentage, feedback_date, notes
            FROM project_feedback
            ORDER BY feedback_date DESC
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                'project_name': row[0],
                'predicted_cost': row[1],
                'actual_cost': row[2],
                'error_percentage': row[3],
                'feedback_date': row[4],
                'notes': row[5]
            }
            for row in rows
        ]
    
    def auto_retrain_if_needed(self, model, preprocessor, threshold_error=15, 
                               min_samples=30):
        """
        Gerekirse otomatik yeniden eğitim
        
        Args:
            model: Mevcut model
            preprocessor: Veri ön işleyici
            threshold_error: Hata eşiği (%)
            min_samples: Minimum örnek sayısı
        
        Returns:
            dict: Yeniden eğitim sonucu
        """
        stats = self.get_feedback_statistics()
        
        if stats['total_feedback'] < min_samples:
            return {
                'retrained': False,
                'reason': f'Yetersiz veri ({stats["total_feedback"]}/{min_samples})'
            }
        
        if stats['average_error_pct'] < threshold_error:
            return {
                'retrained': False,
                'reason': f'Model performansı yeterli (Hata: %{stats["average_error_pct"]:.2f})'
            }
        
        result = self.incremental_training(model, preprocessor)
        
        if result['success']:
            model.save('models/cost_prediction_model.pkl')
            
            with open('models/preprocessor.pkl', 'wb') as f:
                pickle.dump(preprocessor, f)
            
            return {
                'retrained': True,
                'reason': f'Yüksek hata oranı (%{stats["average_error_pct"]:.2f})',
                'improvement': result['improvement_pct'],
                'new_accuracy': result['new_r2']
            }
        
        return {
            'retrained': False,
            'reason': 'Yeniden eğitim başarısız',
            'error': result.get('message')
        }
    
    def export_feedback_data(self, output_file='data/feedback_export.csv'):
        """
        Geri bildirim verilerini CSV'ye aktar
        
        Args:
            output_file: Çıktı dosyası
        """
        if self.use_postgres:
            # PostgreSQL — şimdilik pass, sonraki versiyonda implement edilecek
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM project_feedback')
        rows = cursor.fetchall()
        
        column_names = [description[0] for description in cursor.description]
        
        conn.close()
        
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w') as f:
            f.write(','.join(column_names) + '\n')
            for row in rows:
                f.write(','.join(str(val) for val in row) + '\n')
        
        return output_file
