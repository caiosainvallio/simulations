from typing import List, Dict, Tuple
import numpy as np
from .base import ModelingInterface

class SIRFModel(ModelingInterface):
    """
    The SIR-F model usually adds 'F' for Fatalities or Failure of quarantine.
    Here we implement a version where F stands for Fatalities, similar to SIR-D 
    but often implies different dynamics or subsets. 
    However, for this lab, we will interpret SIR-F as:
    Susceptible -> Infected -> Recovered
                         -> Fatalities (F)
    Which is structurally identical to SIR-D, so let's make it more interesting.
    Let's use the definition where F is 'Forced Isolation' (quarantined infectious).
    S -> I -> R
         I -> F (quarantine) -> R
         I -> F -> D (death from quarantine)
         
    Simplified SIR-F from some COVID papers:
    S -> I
    I -> R (recover unmarked)
    I -> F (infectious but isolated/fatal/severe)
    F -> R (recover from severe)
    F -> D (die)
    """

    @property
    def name(self) -> str:
        return "SIR-F"

    @property
    def description(self) -> str:
        return (
            "SIR-F model includes a compartment F for severe cases/isolation. "
            "Flows: S->I, I->R, I->F, F->R, F->D."
        )

    def get_compartment_names(self) -> List[str]:
        return ["S", "I", "R", "F", "D"]

    def get_default_params(self) -> Dict[str, float]:
        return {
            "beta": 0.4,
            "gamma_i": 0.1, # Recovery from I
            "alpha": 0.05,  # Progression I -> F
            "gamma_f": 0.05, # Recovery from F
            "mu": 0.02      # Death from F
        }

    def get_parameter_descriptions(self) -> Dict[str, str]:
        return {
            "beta": "Infection rate",
            "gamma_i": "Recovery rate from Infected (I)",
            "alpha": "Progression rate from I to Failure/Fatal (F)",
            "gamma_f": "Recovery rate from F",
            "mu": "Mortality rate from F"
        }

    def calculate_r0(self, params: Dict[str, float]) -> float:
        # R0 = beta / (outflow from I) = beta / (gamma_i + alpha)
        # Assuming F compartment is effectively isolated/fatal and does not transmit.
        return params["beta"] / (params["gamma_i"] + params["alpha"])

    def get_default_initial_conditions(self) -> Dict[str, float]:
        return {
            "S": 0.99,
            "I": 0.01,
            "R": 0.0,
            "F": 0.0,
            "D": 0.0
        }

    def get_derivatives(self, t: float, y: np.ndarray, params: Dict[str, float]) -> np.ndarray:
        S, I, R, F, D = y
        beta = params["beta"]
        gamma_i = params["gamma_i"]
        alpha = params["alpha"]
        gamma_f = params["gamma_f"]
        mu = params["mu"]

        N = S + I + R + F + D

        dSdt = -beta * S * I / N
        dIdt = (beta * S * I / N) - (gamma_i * I) - (alpha * I)
        dRdt = (gamma_i * I) + (gamma_f * F)
        dFdt = (alpha * I) - (gamma_f * F) - (mu * F)
        dDdt = mu * F

        return np.array([dSdt, dIdt, dRdt, dFdt, dDdt])

    def get_transitions(self) -> List[Tuple[str, str, str]]:
        return [
            ("S", "I", "beta"),
            ("I", "R", "gamma_i"),
            ("I", "F", "alpha"),
            ("F", "R", "gamma_f"),
            ("F", "D", "mu")
        ]

class SEWIRFModel(ModelingInterface):
    """
    Susceptible-Exposed-Waning-Infected-Recovered-Fatalities(or F).
    Let's simplify to SEIR-F for now as 'Waning' adds loop back to S or E.
    SEWIR-F:
    S -> E (exposed)
    E -> I (infectious)
    I -> R (recovered)
    I -> F (severe/fatal)
    F -> D (death)
    F -> R (recovered)
    R -> W (waning immunity) -> S
    """
    
    @property
    def name(self) -> str:
        return "SEWIR-F"

    @property
    def description(self) -> str:
        return (
            "Complex model with Waning immunity. "
            "S->E->I->R->W->S. Plus I->F->D/R."
        )

    def get_compartment_names(self) -> List[str]:
        return ["S", "E", "W", "I", "R", "F", "D"]

    def get_default_params(self) -> Dict[str, float]:
        return {
            "beta": 0.5,
            "sigma": 0.2, # E -> I (incubation)
            "gamma_i": 0.1,
            "alpha": 0.05,
            "gamma_f": 0.05,
            "mu": 0.02,
            "omega": 0.001 # Waning immunity R -> W -> S? Or R->S directly via W? Let's use R->S with rate omega. 
                           # Or if W is a compartment: R->W->S. Let's do R->W->S.
            , "rho": 0.1 # W -> S
        }

    def get_parameter_descriptions(self) -> Dict[str, str]:
        return {
            "beta": "Infection rate",
            "sigma": "Progression E -> I (1/incubation period)",
            "gamma_i": "Recovery rate from I",
            "alpha": "Progression I -> F (severe cases)",
            "gamma_f": "Recovery rate from F",
            "mu": "Mortality rate from F",
            "omega": "Waning immunity rate (1/immunity duration)",
            "rho": "Rate of loss of protection W -> S"
        }

    def calculate_r0(self, params: Dict[str, float]) -> float:
        # R0 for SEIR-type is typically beta / gamma
        # Here outflow from I is gamma_i + alpha
        # R0 = beta / (gamma_i + alpha)
        # Note: If E implies latent period, it doesn't reduce total infections produced if everyone survives E.
        return params["beta"] / (params["gamma_i"] + params["alpha"])

    def get_default_initial_conditions(self) -> Dict[str, float]:
         return {
            "S": 0.99,
            "E": 0.0,
            "W": 0.0,
            "I": 0.01,
            "R": 0.0,
            "F": 0.0,
            "D": 0.0
        }

    def get_derivatives(self, t: float, y: np.ndarray, params: Dict[str, float]) -> np.ndarray:
        S, E, W, I, R, F, D = y
        beta = params["beta"]
        sigma = params["sigma"]
        gamma_i = params["gamma_i"]
        alpha = params["alpha"]
        gamma_f = params["gamma_f"]
        mu = params["mu"]
        omega = params["omega"] # R -> W
        rho = params["rho"] # W -> S

        N = S + E + W + I + R + F + D
        
        # Infective force from I and maybe F? Let's assume only I is mobile? 
        # Or F is isolated but still infectious? Let's assume F is isolated (no transmission).
        
        dSdt = -beta * S * I / N + rho * W
        dEdt = (beta * S * I / N) - (sigma * E)
        dWdt = (omega * R) - (rho * W)
        dIdt = (sigma * E) - (gamma_i * I) - (alpha * I)
        dRdt = (gamma_i * I) + (gamma_f * F) - (omega * R)
        dFdt = (alpha * I) - (gamma_f * F) - (mu * F)
        dDdt = mu * F
        
        return np.array([dSdt, dEdt, dWdt, dIdt, dRdt, dFdt, dDdt])

    def get_transitions(self) -> List[Tuple[str, str, str]]:
        return [
            ("S", "E", "beta"),
            ("E", "I", "sigma"),
            ("I", "R", "gamma_i"),
            ("I", "F", "alpha"),
            ("F", "R", "gamma_f"),
            ("F", "D", "mu"),
            ("R", "W", "omega"),
            ("W", "S", "rho")
        ]
