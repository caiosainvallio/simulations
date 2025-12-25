import unittest
import numpy as np
from src.models.sir import SIRModel
from src.models.sird import SIRDModel
from src.solvers.ode_solver import ODESolver

class TestModels(unittest.TestCase):
    def test_sir_conservation(self):
        model = SIRModel()
        solver = ODESolver(model)
        
        params = model.get_default_params()
        # Set mu/birth to 0 so N is constant
        
        ic = {"S": 0.9, "I": 0.1, "R": 0.0}
        t, sol = solver.solve(ic, params, t_max=10, steps=10)
        
        # Check if sum is ~1.0 at all steps
        total_pop = np.sum(sol, axis=1)
        self.assertTrue(np.allclose(total_pop, 1.0), f"Population not conserved: {total_pop}")

    def test_sird_dimensions(self):
        model = SIRDModel()
        solver = ODESolver(model)
        ic = model.get_default_initial_conditions()
        params = model.get_default_params()
        
        t, sol = solver.solve(ic, params, t_max=10, steps=50)
        self.assertEqual(sol.shape, (50, 4))

if __name__ == '__main__':
    unittest.main()
