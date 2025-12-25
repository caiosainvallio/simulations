from typing import Dict, Any

# Population of Sao Paulo State (2024 Est)
POP_SP = 45_973_194

# Scenarios Dictionary
SCENARIOS: Dict[str, Dict[str, Any]] = {
    "Custom (Manual Input)": {
        "description": "Adjust parameters manually.",
        "params": None,
        "initial_conditions": None
    },
    "COVID-19 (SP - Standard)": {
        "model_type": "SIR",
        "description": "Approximation of COVID-19 in SP. R0 ≈ 3.1, Infectious period ≈ 7 days.\nPopulation: ~46 Million.",
        "params": {
            "beta": 0.44, # 3.1 * (1/7)
            "gamma": 0.14 # 1/7
        },
        "initial_conditions": {
            "S": 1.0 - (1000/POP_SP), # Assume 1000 initial cases
            "I": 1000/POP_SP,
            "R": 0.0
        }
    },
    "Influenza (SP - Seasonal)": {
        "model_type": "SIR",
        "description": "Seasonal Flu scenario. R0 ≈ 1.3, Infectious period ≈ 5 days.",
        "params": {
            "beta": 0.26, # 1.3 * 0.2
            "gamma": 0.2  # 1/5
        },
        "initial_conditions": {
            "S": 1.0 - (500/POP_SP),
            "I": 500/POP_SP,
            "R": 0.0
        }
    },
    "RSV (VSR) (SP - High Transmissibility)": {
        "model_type": "SIR",
        "description": "VSR scenario (Children/Elderly impact). R0 ≈ 3.0, Infectious period ≈ 7 days.",
        "params": {
            "beta": 0.43, # 3.0 * 0.143
            "gamma": 0.143 # 1/7
        },
        "initial_conditions": {
            "S": 1.0 - (200/POP_SP),
            "I": 200/POP_SP,
            "R": 0.0
        }
    }
}
