import unittest
from src.scenarios.data import SCENARIOS

class TestScenarios(unittest.TestCase):
    def test_scenario_structure(self):
        for name, data in SCENARIOS.items():
            if name == "Custom (Manual Input)":
                continue
                
            self.assertIn("model_type", data)
            self.assertIn("params", data)
            self.assertIn("initial_conditions", data)
            
            # Check if Beta/Gamma are plausible (positive)
            self.assertGreater(data["params"]["beta"], 0)
            self.assertGreater(data["params"]["gamma"], 0)
            
            # Check initial conditions sum to 1.0 (approx)
            ic = data["initial_conditions"]
            total = sum(ic.values())
            self.assertAlmostEqual(total, 1.0, places=5, msg=f"Scenario {name} IC sum {total} != 1.0")

    def test_covid_r0_approx(self):
        # Verify R0 is approx 3.1
        data = SCENARIOS["COVID-19 (SP - Standard)"]
        r0 = data["params"]["beta"] / data["params"]["gamma"]
        self.assertAlmostEqual(r0, 3.14, delta=0.1)

if __name__ == '__main__':
    unittest.main()
