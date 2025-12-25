import unittest
from src.models.sir import SIRModel
from src.models.sird import SIRDModel
from src.models.extensions import SIRFModel, SEWIRFModel

class TestMetrics(unittest.TestCase):
    def test_sir_r0(self):
        model = SIRModel()
        params = {"beta": 0.5, "gamma": 0.1}
        # R0 = 0.5 / 0.1 = 5.0
        self.assertAlmostEqual(model.calculate_r0(params), 5.0)

    def test_sird_r0(self):
        model = SIRDModel()
        params = {"beta": 0.5, "gamma": 0.1, "mu": 0.1}
        # R0 = 0.5 / (0.1 + 0.1) = 2.5
        self.assertAlmostEqual(model.calculate_r0(params), 2.5)
        
    def test_sirf_r0(self):
        model = SIRFModel()
        # R0 = beta / (gamma_i + alpha)
        params = {"beta": 0.4, "gamma_i": 0.1, "alpha": 0.1, "gamma_f": 0.1, "mu": 0.1}
        expected = 0.4 / (0.1 + 0.1) 
        self.assertAlmostEqual(model.calculate_r0(params), expected)

    def test_sewrif_r0(self):
        model = SEWIRFModel()
        # R0 = beta / (gamma_i + alpha)
        params = {"beta": 0.6, "sigma": 0.2, "gamma_i": 0.1, "alpha": 0.1, "gamma_f": 0.1, "mu": 0.1, "omega": 0.01, "rho": 0.1}
        expected = 0.6 / (0.1 + 0.1) 
        self.assertAlmostEqual(model.calculate_r0(params), expected)

if __name__ == '__main__':
    unittest.main()
