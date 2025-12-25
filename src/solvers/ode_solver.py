import numpy as np
from scipy.integrate import odeint
from typing import Dict, Any, Tuple
from ..models.base import ModelingInterface

class ODESolver:
    """
    Numerical solver for ODEs defined by a ModelingInterface.
    Uses scipy.integrate.odeint for integration.
    """

    def __init__(self, model: ModelingInterface):
        self.model = model

    def solve(self, initial_conditions: Dict[str, float], params: Dict[str, float], t_max: int, steps: int = 100) -> Tuple[np.ndarray, np.ndarray]:
        """
        Solve the ODE system.

        Args:
            initial_conditions: Dictionary mapping compartment names to initial values.
            params: Dictionary mapping parameter names to values.
            t_max: Maximum time to simulate (e.g., days).
            steps: Number of time steps.

        Returns:
            Tuple of (time_points, solution_matrix).
            time_points: Array of shape (steps,)
            solution_matrix: Array of shape (steps, num_compartments)
        """
        # Prepare time points
        t = np.linspace(0, t_max, steps)

        # Prepare initial state vector in correct order
        compartments = self.model.get_compartment_names()
        y0 = [initial_conditions[c] for c in compartments]

        # Define wrapper for odeint (scipy expects func(y, t, ...))
        # Note: ModelingInterface.get_derivatives signature is (t, y, params)
        # odeint signature is func(y, t, *args)
        def func(y, t, p):
            return self.model.get_derivatives(t, y, p)

        # Solve
        solution = odeint(func, y0, t, args=(params,))

        return t, solution
