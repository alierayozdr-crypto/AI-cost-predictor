import numpy as np
from .activation_functions import ActivationFunctions

class DenseLayer:
    """
    Tam bağlı (Fully Connected) sinir ağı katmanı.
    Her nöron bir önceki katmandaki tüm nöronlara bağlıdır.
    
    Matematiksel gösterim: y = f(W·x + b)
    - W: Ağırlık matrisi (weights)
    - x: Girdi vektörü
    - b: Sapma vektörü (bias)
    - f: Aktivasyon fonksiyonu
    """
    
    def __init__(self, input_size, output_size, activation='relu'):
        """
        Args:
            input_size: Girdi boyutu
            output_size: Çıktı boyutu (nöron sayısı)
            activation: Aktivasyon fonksiyonu ('relu', 'sigmoid', 'tanh', 'linear')
        """
        self.input_size = input_size
        self.output_size = output_size
        self.activation_name = activation
        
        self.weights = np.random.randn(input_size, output_size) * np.sqrt(2.0 / input_size)
        self.bias = np.zeros((1, output_size))
        
        self.activation_func = getattr(ActivationFunctions, activation)
        self.activation_derivative = getattr(ActivationFunctions, f"{activation}_derivative")
        
        self.input = None
        self.z = None
        self.output = None
        
        self.dW = None
        self.db = None
    
    def forward(self, input_data):
        """
        İleri besleme (Forward Propagation)
        
        Adımlar:
        1. z = W·x + b (Lineer transformasyon)
        2. a = f(z) (Aktivasyon)
        
        Args:
            input_data: Girdi verisi (batch_size, input_size)
        
        Returns:
            output: Aktivasyon sonrası çıktı (batch_size, output_size)
        """
        self.input = input_data
        self.z = np.dot(input_data, self.weights) + self.bias
        self.output = self.activation_func(self.z)
        return self.output
    
    def backward(self, output_gradient, learning_rate):
        """
        Geri yayılım (Backpropagation)
        
        Zincir kuralı ile gradientleri hesaplar:
        ∂L/∂W = ∂L/∂a · ∂a/∂z · ∂z/∂W
        
        Args:
            output_gradient: Bir sonraki katmandan gelen gradient (∂L/∂a)
            learning_rate: Öğrenme oranı (α)
        
        Returns:
            input_gradient: Bir önceki katmana gönderilecek gradient
        """
        activation_gradient = self.activation_derivative(self.z)
        delta = output_gradient * activation_gradient
        
        self.dW = np.dot(self.input.T, delta)
        self.db = np.sum(delta, axis=0, keepdims=True)
        
        input_gradient = np.dot(delta, self.weights.T)
        
        self.weights -= learning_rate * self.dW
        self.bias -= learning_rate * self.db
        
        return input_gradient
    
    def get_params(self):
        """Model parametrelerini döndür"""
        return {
            'weights': self.weights.copy(),
            'bias': self.bias.copy()
        }
    
    def set_params(self, params):
        """Model parametrelerini ayarla"""
        self.weights = params['weights'].copy()
        self.bias = params['bias'].copy()
