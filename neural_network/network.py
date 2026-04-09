import numpy as np
from .layers import DenseLayer
import pickle
import os

class NeuralNetwork:
    """
    Çok katmanlı sinir ağı (Multi-Layer Perceptron)
    Sıfırdan yazılmış, hiçbir dış API kullanılmamıştır.
    
    Öğrenme süreci:
    1. Forward Propagation: Veriyi ağdan geçir, tahmin üret
    2. Loss Calculation: Hatayı hesapla
    3. Backpropagation: Gradientleri hesapla
    4. Weight Update: Ağırlıkları güncelle (Gradient Descent)
    """
    
    def __init__(self):
        self.layers = []
        self.loss_history = []
        
    def add_layer(self, input_size, output_size, activation='relu'):
        """
        Ağa yeni katman ekle
        
        Args:
            input_size: Girdi boyutu
            output_size: Çıktı boyutu
            activation: Aktivasyon fonksiyonu
        """
        layer = DenseLayer(input_size, output_size, activation)
        self.layers.append(layer)
        
    def forward(self, X):
        """
        İleri besleme - tüm katmanlardan veriyi geçir
        
        Args:
            X: Girdi verisi
        
        Returns:
            output: Ağın tahmini
        """
        output = X
        for layer in self.layers:
            output = layer.forward(output)
        return output
    
    def backward(self, loss_gradient, learning_rate):
        """
        Geri yayılım - gradientleri geriye doğru hesapla ve ağırlıkları güncelle
        
        Args:
            loss_gradient: Kayıp fonksiyonunun gradienti
            learning_rate: Öğrenme oranı
        """
        gradient = loss_gradient
        for layer in reversed(self.layers):
            gradient = layer.backward(gradient, learning_rate)
    
    def mse_loss(self, y_true, y_pred):
        """
        Mean Squared Error (Ortalama Kare Hatası)
        
        MSE = (1/n) * Σ(y_true - y_pred)²
        
        Regresyon problemleri için standart kayıp fonksiyonu
        """
        return np.mean((y_true - y_pred) ** 2)
    
    def mse_loss_derivative(self, y_true, y_pred):
        """
        MSE türevi: ∂MSE/∂y_pred = -2(y_true - y_pred) / n
        """
        return -2 * (y_true - y_pred) / y_true.shape[0]
    
    def mae_loss(self, y_true, y_pred):
        """
        Mean Absolute Error (Ortalama Mutlak Hata)
        
        MAE = (1/n) * Σ|y_true - y_pred|
        """
        return np.mean(np.abs(y_true - y_pred))
    
    def train(self, X_train, y_train, epochs=1000, learning_rate=0.01, 
              batch_size=32, verbose=True, validation_data=None):
        """
        Modeli eğit
        
        Args:
            X_train: Eğitim verisi girdileri
            y_train: Eğitim verisi çıktıları
            epochs: Epoch sayısı (veri setinin kaç kez işleneceği)
            learning_rate: Öğrenme oranı (α)
            batch_size: Mini-batch boyutu
            verbose: Eğitim ilerlemesini göster
            validation_data: Doğrulama verisi (X_val, y_val)
        """
        n_samples = X_train.shape[0]
        self.loss_history = []
        
        for epoch in range(epochs):
            indices = np.random.permutation(n_samples)
            X_shuffled = X_train[indices]
            y_shuffled = y_train[indices]
            
            epoch_loss = 0
            n_batches = 0
            
            for i in range(0, n_samples, batch_size):
                X_batch = X_shuffled[i:i+batch_size]
                y_batch = y_shuffled[i:i+batch_size]
                
                y_pred = self.forward(X_batch)
                
                loss = self.mse_loss(y_batch, y_pred)
                epoch_loss += loss
                n_batches += 1
                
                loss_gradient = self.mse_loss_derivative(y_batch, y_pred)
                self.backward(loss_gradient, learning_rate)
            
            avg_loss = epoch_loss / n_batches
            self.loss_history.append(avg_loss)
            
            if verbose and (epoch + 1) % 100 == 0:
                val_info = ""
                if validation_data is not None:
                    X_val, y_val = validation_data
                    y_val_pred = self.predict(X_val)
                    val_loss = self.mse_loss(y_val, y_val_pred)
                    val_info = f" - Val Loss: {val_loss:.6f}"
                
                print(f"Epoch {epoch+1}/{epochs} - Loss: {avg_loss:.6f}{val_info}")
    
    def predict(self, X):
        """
        Tahmin yap
        
        Args:
            X: Girdi verisi
        
        Returns:
            predictions: Tahminler
        """
        return self.forward(X)
    
    def evaluate(self, X_test, y_test):
        """
        Modeli değerlendir
        
        Returns:
            metrics: Performans metrikleri (MSE, MAE, R²)
        """
        y_pred = self.predict(X_test)
        
        mse = self.mse_loss(y_test, y_pred)
        mae = self.mae_loss(y_test, y_pred)
        
        ss_res = np.sum((y_test - y_pred) ** 2)
        ss_tot = np.sum((y_test - np.mean(y_test)) ** 2)
        r2 = 1 - (ss_res / ss_tot)
        
        return {
            'mse': mse,
            'mae': mae,
            'r2': r2,
            'rmse': np.sqrt(mse)
        }
    
    def save(self, filepath):
        """
        Modeli kaydet
        
        Args:
            filepath: Kaydedilecek dosya yolu
        """
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        model_data = {
            'layers': [],
            'loss_history': self.loss_history
        }
        
        for layer in self.layers:
            layer_data = {
                'input_size': layer.input_size,
                'output_size': layer.output_size,
                'activation': layer.activation_name,
                'params': layer.get_params()
            }
            model_data['layers'].append(layer_data)
        
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"Model kaydedildi: {filepath}")
    
    def load(self, filepath):
        """
        Modeli yükle
        
        Args:
            filepath: Yüklenecek dosya yolu
        """
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)
        
        self.layers = []
        for layer_data in model_data['layers']:
            layer = DenseLayer(
                layer_data['input_size'],
                layer_data['output_size'],
                layer_data['activation']
            )
            layer.set_params(layer_data['params'])
            self.layers.append(layer)
        
        self.loss_history = model_data['loss_history']
        
        print(f"Model yüklendi: {filepath}")
