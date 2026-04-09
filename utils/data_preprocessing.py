import numpy as np

class DataPreprocessor:
    """
    Veri ön işleme ve özellik mühendisliği
    Finansal verileri yapay zeka modeline uygun hale getirir
    """
    
    def __init__(self):
        self.feature_means = None
        self.feature_stds = None
        self.target_mean = None
        self.target_std = None
        
    def normalize(self, data, fit=True):
        """
        Z-score normalizasyonu: z = (x - μ) / σ
        
        Neden gerekli?
        - Farklı ölçeklerdeki özellikleri (örn: 1000 TL vs 0.05 faiz oranı) aynı ölçeğe getirir
        - Gradient descent'in daha hızlı yakınsamasını sağlar
        
        Args:
            data: Normalize edilecek veri
            fit: True ise μ ve σ hesapla, False ise önceki değerleri kullan
        
        Returns:
            normalized_data: Normalize edilmiş veri
        """
        if fit:
            self.feature_means = np.mean(data, axis=0)
            self.feature_stds = np.std(data, axis=0) + 1e-8
        
        return (data - self.feature_means) / self.feature_stds
    
    def denormalize(self, normalized_data, is_target=False):
        """
        Normalize edilmiş veriyi orijinal ölçeğe geri döndür
        
        Args:
            normalized_data: Normalize edilmiş veri
            is_target: Hedef değişken mi?
        
        Returns:
            original_data: Orijinal ölçekteki veri
        """
        if is_target:
            return normalized_data * self.target_std + self.target_mean
        else:
            return normalized_data * self.feature_stds + self.feature_means
    
    def normalize_target(self, target, fit=True):
        """
        Hedef değişkeni normalize et
        """
        if fit:
            self.target_mean = np.mean(target)
            self.target_std = np.std(target) + 1e-8
        
        return (target - self.target_mean) / self.target_std
    
    def create_polynomial_features(self, X, degree=2):
        """
        Polinom özellikleri oluştur
        
        Örnek: [x1, x2] -> [x1, x2, x1², x2², x1*x2]
        
        Neden kullanılır?
        - Doğrusal olmayan ilişkileri yakalamak için
        - Model kapasitesini artırır
        
        Args:
            X: Girdi özellikleri
            degree: Polinom derecesi
        
        Returns:
            poly_features: Polinom özellikleri
        """
        n_samples, n_features = X.shape
        poly_features = [X]
        
        if degree >= 2:
            for i in range(n_features):
                for j in range(i, n_features):
                    poly_features.append((X[:, i] * X[:, j]).reshape(-1, 1))
        
        return np.hstack(poly_features)
    
    def add_time_features(self, dates):
        """
        Zaman serisi özellikleri ekle
        
        Özellikler:
        - Ay (1-12)
        - Çeyrek (1-4)
        - Yıl içindeki gün (1-365)
        - Mevsim (0-3)
        
        Args:
            dates: Tarih dizisi (YYYY-MM-DD formatında)
        
        Returns:
            time_features: Zaman özellikleri
        """
        pass
    
    def handle_missing_values(self, data, strategy='mean'):
        """
        Eksik değerleri işle
        
        Stratejiler:
        - 'mean': Ortalama ile doldur
        - 'median': Medyan ile doldur
        - 'forward_fill': Önceki değerle doldur
        
        Args:
            data: Veri
            strategy: Doldurma stratejisi
        
        Returns:
            filled_data: Doldurulmuş veri
        """
        if strategy == 'mean':
            col_mean = np.nanmean(data, axis=0)
            indices = np.where(np.isnan(data))
            data[indices] = np.take(col_mean, indices[1])
        elif strategy == 'median':
            col_median = np.nanmedian(data, axis=0)
            indices = np.where(np.isnan(data))
            data[indices] = np.take(col_median, indices[1])
        
        return data
    
    def train_test_split(self, X, y, test_size=0.2, random_state=None):
        """
        Veriyi eğitim ve test setlerine ayır
        
        Args:
            X: Özellikler
            y: Hedef değişken
            test_size: Test seti oranı
            random_state: Rastgelelik tohumu
        
        Returns:
            X_train, X_test, y_train, y_test
        """
        if random_state is not None:
            np.random.seed(random_state)
        
        n_samples = X.shape[0]
        n_test = int(n_samples * test_size)
        
        indices = np.random.permutation(n_samples)
        test_indices = indices[:n_test]
        train_indices = indices[n_test:]
        
        return X[train_indices], X[test_indices], y[train_indices], y[test_indices]
