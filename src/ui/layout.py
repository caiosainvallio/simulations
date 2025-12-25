import streamlit as st
import numpy as np
from ..models.base import ModelingInterface
from ..solvers.ode_solver import ODESolver
from ..visualization.charts import plot_simulation_results
from ..visualization.dag import render_interaction_graph

def render_sidebar(model: ModelingInterface) -> tuple:
    """
    Render sidebar controls for parameters and initial conditions.
    Returns (params, initial_conditions, t_max)
    """
    st.sidebar.header("Simulation Parameters")
    
    # Time settings
    t_max = st.sidebar.slider("Simulation Time (Days)", min_value=10, max_value=365, value=100)
    
    st.sidebar.subheader("Model Parameters")
    default_params = model.get_default_params()
    param_descriptions = model.get_parameter_descriptions()
    params = {}
    for key, val in default_params.items():
        # Heuristic for slider ranges: 0 to 2*default or 1.0
        max_val = max(1.0, val * 2.0)
        step = 0.001 if val < 0.1 else 0.01
        help_text = param_descriptions.get(key, "")
        params[key] = st.sidebar.slider(f"{key}", min_value=0.0, max_value=float(max_val), value=float(val), step=step, help=help_text)
        
    st.sidebar.subheader("Initial Conditions")
    default_ic = model.get_default_initial_conditions()
    initial_conditions = {}
    for key, val in default_ic.items():
        initial_conditions[key] = st.sidebar.number_input(f"Initial {key}", min_value=0.0, max_value=1.0, value=float(val), step=0.01)
        
    # Normalize initial conditions if sum != 1? 
    # Let's trust the user or add a warning if sum > 1
    total_ic = sum(initial_conditions.values())
    if not np.isclose(total_ic, 1.0):
        st.sidebar.warning(f"Total initial population is {total_ic:.2f} (Expected ~1.0)")
        
    return params, initial_conditions, t_max

def render_dashboard(model: ModelingInterface):
    """
    Main dashboard rendering function.
    """
    st.title(f"Simulation Lab: {model.name}")
    st.markdown(model.description)
    
    # Render Sidebar and get inputs
    params, initial_conditions, t_max = render_sidebar(model)
    
    # Run Simulation
    solver = ODESolver(model)
    t, solution = solver.solve(initial_conditions, params, t_max)
    
    # Visuals Layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Population Dynamics")
        fig = plot_simulation_results(t, solution, model.get_compartment_names())
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.subheader("Model Structure")
        dag = render_interaction_graph(model.get_compartment_names(), model.get_transitions())
        st.graphviz_chart(dag)
        
    # Metrics / Data
    st.subheader("Simulation Metrics")
    
    # Calculate Metrics
    r0 = model.calculate_r0(params)
    peak_infected_idx = np.argmax(solution[:, model.get_compartment_names().index("I")])
    peak_day = t[peak_infected_idx]
    peak_infected_val = solution[peak_infected_idx, model.get_compartment_names().index("I")]
    
    # Calculate Rt over time: Rt = R0 * S(t) (Approximation for SIR-like models)
    # This assumes S is the first compartment and normalized to 1. 
    # For more complex models this might be varying, but it's a good standard approx.
    s_idx = model.get_compartment_names().index("S")
    rt_series = r0 * solution[:, s_idx]
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Basic Reprod. Number (R0)", f"{r0:.2f}")
    c2.metric("Effective R (Rt) @ End", f"{rt_series[-1]:.2f}")
    c3.metric("Peak Infection Day", f"Day {peak_day:.1f}")
    c4.metric("Peak Infection %", f"{peak_infected_val*100:.1f}%")
    
    st.subheader("Effective Reproduction Number ($R_t$) over Time")
    st.line_chart(rt_series)
    
    st.expander("Raw Data").dataframe(solution)
