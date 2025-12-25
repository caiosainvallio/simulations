import plotly.graph_objects as go
import numpy as np
from typing import List

def plot_simulation_results(t: np.ndarray, solution: np.ndarray, compartment_names: List[str]):
    """
    Create a Plotly figure showing the simulation results.
    
    Args:
        t: Time points.
        solution: Solution matrix (steps x compartments).
        compartment_names: Names of the compartments.
        
    Returns:
        plotly.graph_objects.Figure
    """
    fig = go.Figure()
    
    for i, name in enumerate(compartment_names):
        fig.add_trace(go.Scatter(
            x=t, 
            y=solution[:, i],
            mode='lines',
            name=name
        ))
        
    fig.update_layout(
        title="Simulation Results",
        xaxis_title="Time",
        yaxis_title="Population / Proportion",
        hovermode="x unified",
        template="plotly_dark", 
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig
