# Simulation Laboratory 🔬

A Python-based simulation laboratory for exploring ODE models (SIR, SIR-D, etc.) with interactive visualizations.

## Features
- **Modular Architecture**: Clean separation of Models, Solvers, and UI.
- **Models Implemented**:
    - **SIR**: Susceptible-Infectious-Recovered.
    - **SIR-D**: Adds Deceased compartment.
    - **SIR-F**: Adds "Forced Isolation" or fatal flows.
    - **SEWIR-F**: Complex model with Expose, Waning immunity, and Fatalities.
- **Interactive Graphs**: Plotly time-series charts.
- **Dynamic DAGs**: Graphviz visualization of model structure.

## Installation

This project uses `uv` for dependency management.

```bash
uv sync
```

## Running the App

```bash
uv run streamlit run main.py
```

## Running Tests

```bash
uv run python -m unittest tests/test_models.py
```