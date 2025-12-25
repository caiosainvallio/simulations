from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Any
import numpy as np

class ModelingInterface(ABC):
    """
    Abstract base class for all ODE-based simulation models.
    Enforces a standard structure for derivatives, compartment names, and visualization metadata.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the human-readable name of the model."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Return a brief description of the model."""
        pass

    @abstractmethod
    def get_compartment_names(self) -> List[str]:
        """
        Return the list of state variable names (compartments).
        Example: ['S', 'I', 'R']
        """
        pass

    @abstractmethod
    def get_default_params(self) -> Dict[str, float]:
        """
        Return default parameter values for the model.
        Example: {'beta': 0.3, 'gamma': 0.1}
        """
        pass
    
    @abstractmethod
    def get_parameter_descriptions(self) -> Dict[str, str]:
        """
        Return descriptions for each parameter to be used as tooltips.
        Example: {'beta': 'Infection rate per contact'}
        """
        pass

    @abstractmethod
    def calculate_r0(self, params: Dict[str, float]) -> float:
        """
        Calculate the Basic Reproduction Number (R0) for the given parameters.
        """
        pass

    @abstractmethod
    def get_default_initial_conditions(self) -> Dict[str, float]:
        """
        Return default initial conditions (proportions or counts).
        Example: {'S': 0.99, 'I': 0.01, 'R': 0.0}
        """
        pass

    @abstractmethod
    def get_derivatives(self, t: float, y: np.ndarray, params: Dict[str, float]) -> np.ndarray:
        """
        Compute the time derivative of the state vector at time t.
        
        Args:
            t: Time point.
            y: State vector (array of compartment values).
            params: Dictionary of model parameters.
            
        Returns:
            dy/dt as a numpy array.
        """
        pass

    @abstractmethod
    def get_transitions(self) -> List[Tuple[str, str, str]]:
        """
        Return a list of transitions for DAG visualization.
        Format: [(source_compartment, target_compartment, rate_parameter_name), ...]
        Example: [('S', 'I', 'beta'), ('I', 'R', 'gamma')]
        """
        pass
