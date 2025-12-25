from typing import List, Dict, Tuple
import numpy as np
from .base import ModelingInterface

class SIRModel(ModelingInterface):
    """
    The classic SIR (Susceptible-Infectious-Recovered) model.
    """

    @property
    def name(self) -> str:
        return "SIR"

    @property
    def description(self) -> str:
        return (
            "The classic SIR model describes the flow of individuals from Susceptible (S) "
            "to Infectious (I) and then to Recovered (R)."
        )

    def get_compartment_names(self) -> List[str]:
        return ["S", "I", "R"]

    def get_default_params(self) -> Dict[str, float]:
        return {
            "beta": 0.5,  # Infection rate
            "gamma": 0.1  # Recovery rate
        }

    def get_parameter_descriptions(self) -> Dict[str, str]:
        return {
            "beta": "Infection rate (beta): Probability of transmitting disease per contact.",
            "gamma": "Recovery rate (gamma): Rate at which infected individuals recover (1/duration)."
        }

    def calculate_r0(self, params: Dict[str, float]) -> float:
        return params["beta"] / params["gamma"]

    def get_default_initial_conditions(self) -> Dict[str, float]:
        return {
            "S": 0.99,
            "I": 0.01,
            "R": 0.0
        }

    def get_derivatives(self, t: float, y: np.ndarray, params: Dict[str, float]) -> np.ndarray:
        # Unpack state
        S, I, R = y
        
        # Unpack parameters
        beta = params["beta"]
        gamma = params["gamma"]
        
        # Total population (assuming constant N=1 if working with proportions)
        N = S + I + R
        
        # Equations
        dSdt = -beta * S * I / N
        dIdt = (beta * S * I / N) - (gamma * I)
        dRdt = gamma * I
        
        return np.array([dSdt, dIdt, dRdt])

    def get_transitions(self) -> List[Tuple[str, str, str]]:
        return [
            ("S", "I", "beta"),
            ("I", "R", "gamma")
        ]
