import numpy as np

class ActivationFunctions:
    """
    Aktivasyon fonksiyonları ve türevleri.
    Sinir ağının doğrusal olmayan (non-linear) öğrenme yeteneği bu fonksiyonlardan gelir.
    """
    
    @staticmethod
    def sigmoid(x):
        """
        Sigmoid aktivasyon fonksiyonu: σ(x) = 1 / (1 + e^(-x))
        Çıktı aralığı: (0, 1) - Olasılık tahminleri için ideal
        """
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))
    
    @staticmethod
    def sigmoid_derivative(x):
        """
        Sigmoid türevi: σ'(x) = σ(x) * (1 - σ(x))
        Geri yayılımda kullanılır
        """
        s = ActivationFunctions.sigmoid(x)
        return s * (1 - s)
    
    @staticmethod
    def relu(x):
        """
        ReLU (Rectified Linear Unit): f(x) = max(0, x)
        Derin ağlarda gradient vanishing problemini çözer
        """
        return np.maximum(0, x)
    
    @staticmethod
    def relu_derivative(x):
        """
        ReLU türevi: f'(x) = 1 if x > 0, else 0
        """
        return (x > 0).astype(float)
    
    @staticmethod
    def tanh(x):
        """
        Tanh aktivasyon: tanh(x) = (e^x - e^(-x)) / (e^x + e^(-x))
        Çıktı aralığı: (-1, 1) - Sigmoid'den daha güçlü gradientler
        """
        return np.tanh(x)
    
    @staticmethod
    def tanh_derivative(x):
        """
        Tanh türevi: tanh'(x) = 1 - tanh²(x)
        """
        return 1 - np.tanh(x) ** 2
    
    @staticmethod
    def linear(x):
        """
        Lineer aktivasyon: f(x) = x
        Regresyon problemleri için çıkış katmanında kullanılır
        """
        return x
    
    @staticmethod
    def linear_derivative(x):
        """
        Lineer türev: f'(x) = 1
        """
        return np.ones_like(x)
    
    @staticmethod
    def leaky_relu(x, alpha=0.01):
        """
        Leaky ReLU: f(x) = x if x > 0, else alpha * x
        ReLU'nun "dying ReLU" problemini çözer
        """
        return np.where(x > 0, x, alpha * x)
    
    @staticmethod
    def leaky_relu_derivative(x, alpha=0.01):
        """
        Leaky ReLU türevi
        """
        return np.where(x > 0, 1, alpha)
