"""
Model testleri - Unit tests
"""

import unittest
import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from neural_network.network import NeuralNetwork
from neural_network.activation_functions import ActivationFunctions
from utils.data_preprocessing import DataPreprocessor

class TestActivationFunctions(unittest.TestCase):
    """Aktivasyon fonksiyonları testleri"""
    
    def test_sigmoid(self):
        """Sigmoid fonksiyonu testi"""
        x = np.array([0, 1, -1])
        result = ActivationFunctions.sigmoid(x)
        
        self.assertEqual(result[0], 0.5)
        self.assertGreater(result[1], 0.5)
        self.assertLess(result[2], 0.5)
    
    def test_relu(self):
        """ReLU fonksiyonu testi"""
        x = np.array([-1, 0, 1, 2])
        result = ActivationFunctions.relu(x)
        
        np.testing.assert_array_equal(result, [0, 0, 1, 2])
    
    def test_tanh(self):
        """Tanh fonksiyonu testi"""
        x = np.array([0])
        result = ActivationFunctions.tanh(x)
        
        self.assertEqual(result[0], 0)

class TestNeuralNetwork(unittest.TestCase):
    """Sinir ağı testleri"""
    
    def setUp(self):
        """Test için model oluştur"""
        self.model = NeuralNetwork()
        self.model.add_layer(3, 5, activation='relu')
        self.model.add_layer(5, 1, activation='linear')
    
    def test_forward_pass(self):
        """İleri besleme testi"""
        X = np.array([[1, 2, 3]])
        output = self.model.forward(X)
        
        self.assertEqual(output.shape, (1, 1))
        self.assertIsInstance(output[0, 0], (int, float, np.number))
    
    def test_training(self):
        """Eğitim testi"""
        X = np.random.randn(10, 3)
        y = np.random.randn(10, 1)
        
        initial_loss = self.model.mse_loss(y, self.model.forward(X))
        
        self.model.train(X, y, epochs=10, learning_rate=0.01, verbose=False)
        
        final_loss = self.model.mse_loss(y, self.model.forward(X))
        
        self.assertLess(final_loss, initial_loss)
    
    def test_model_save_load(self):
        """Model kaydetme/yükleme testi"""
        import tempfile
        
        with tempfile.NamedTemporaryFile(suffix='.pkl', delete=False) as f:
            temp_path = f.name
        
        try:
            self.model.save(temp_path)
            
            new_model = NeuralNetwork()
            new_model.load(temp_path)
            
            self.assertEqual(len(new_model.layers), len(self.model.layers))
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

class TestDataPreprocessor(unittest.TestCase):
    """Veri ön işleme testleri"""
    
    def setUp(self):
        """Test için preprocessor oluştur"""
        self.preprocessor = DataPreprocessor()
    
    def test_normalization(self):
        """Normalizasyon testi"""
        data = np.array([[1, 2, 3], [4, 5, 6]])
        
        normalized = self.preprocessor.normalize(data, fit=True)
        
        self.assertAlmostEqual(np.mean(normalized), 0, places=5)
        self.assertAlmostEqual(np.std(normalized), 1, places=5)
    
    def test_train_test_split(self):
        """Train/test split testi"""
        X = np.random.randn(100, 5)
        y = np.random.randn(100, 1)
        
        X_train, X_test, y_train, y_test = self.preprocessor.train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        self.assertEqual(len(X_train), 80)
        self.assertEqual(len(X_test), 20)
        self.assertEqual(len(y_train), 80)
        self.assertEqual(len(y_test), 20)

if __name__ == '__main__':
    unittest.main()
