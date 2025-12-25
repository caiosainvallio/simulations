from typing import List, Dict, Tuple
import numpy as np
from .base import ModelingInterface

class SIRDModel(ModelingInterface):
    """
    The SIR-D model extends SIR by adding a Deceased compartment.
    """

    @property
    def name(self) -> str:
        return "SIR-D"

    @property
    def description(self) -> str:
        return (
            "The SIR-D model extends SIR by separating the 'Removed' compartment into "
            "Recovered (R) and Deceased (D)."
        )

    def get_compartment_names(self) -> List[str]:
        return ["S", "I", "R", "D"]

    def get_default_params(self) -> Dict[str, float]:
        return {
            "beta": 0.5,   # Infection rate
            "gamma": 0.1,  # Recovery rate
            "mu": 0.05     # Mortality rate
        }

    def get_parameter_descriptions(self) -> Dict[str, str]:
        return {
            "beta": "Infection rate (beta).",
            "gamma": "Recovery rate (gamma).",
            "mu": "Mortality rate (mu): Rate of death from infection."
        }

    def calculate_r0(self, params: Dict[str, float]) -> float:
        # R0 = beta / (gamma + mu)
        return params["beta"] / (params["gamma"] + params["mu"])

    def get_default_initial_conditions(self) -> Dict[str, float]:
        return {
            "S": 0.99,
            "I": 0.01,
            "R": 0.0,
            "D": 0.0
        }

    def get_derivatives(self, t: float, y: np.ndarray, params: Dict[str, float]) -> np.ndarray:
        S, I, R, D = y
        beta = params["beta"]
        gamma = params["gamma"]
        mu = params["mu"]
        
        N = S + I + R + D
        
        dSdt = -beta * S * I / N
        dIdt = (beta * S * I / N) - (gamma * I) - (mu * I)
        dRdt = gamma * I
        dDdt = mu * I
        
        return np.array([dSdt, dIdt, dRdt, dDdt])

    def get_transitions(self) -> List[Tuple[str, str, str]]:
        return [
            ("S", "I", "beta"),
            ("I", "R", "gamma"),
            ("I", "D", "mu")
        ]
