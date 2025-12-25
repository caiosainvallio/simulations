import streamlit as st
import numpy as np
import subprocess
import sys
from ..models.base import ModelingInterface
from ..solvers.ode_solver import ODESolver
from ..visualization.charts import plot_simulation_results
from ..visualization.dag import render_interaction_graph

from ..scenarios.data import SCENARIOS
import streamlit.components.v1 as components
from ..simulation_game.web_sim import get_simulation_html

def update_params_from_scenario():
    """Callback to update session state when scenario changes."""
    scenario_name = st.session_state["selected_scenario"]
    scenario_data = SCENARIOS.get(scenario_name, {})
    
    if scenario_data.get("params"):
        for key, val in scenario_data["params"].items():
            if f"param_{key}" in st.session_state: # Check if key exists (model might differ)
                st.session_state[f"param_{key}"] = float(val)
                
    if scenario_data.get("initial_conditions"):
        for key, val in scenario_data["initial_conditions"].items():
             if f"ic_{key}" in st.session_state:
                st.session_state[f"ic_{key}"] = float(val)

def render_sidebar(model: ModelingInterface) -> tuple:
    """
    Render sidebar controls for parameters and initial conditions.
    Returns (params, initial_conditions, t_max)
    """
    st.sidebar.header("Simulation Parameters")
    
    # Scenarios
    scenario_options = list(SCENARIOS.keys())
    
    st.sidebar.selectbox(
        "Load Scenario (São Paulo)", 
        scenario_options, 
        key="selected_scenario",
        on_change=update_params_from_scenario
    )
    
    # Time settings
    t_max = st.sidebar.slider("Simulation Time (Days)", min_value=10, max_value=365, value=100)
    
    st.sidebar.subheader("Model Parameters")
    default_params = model.get_default_params()
    param_descriptions = model.get_parameter_descriptions()
    params = {}
    
    # Create sliders with keys to allow programmatic updates
    for key, val in default_params.items():
        # Heuristic for slider ranges
        max_val = max(1.0, val * 3.0) 
        step = 0.001 if val < 0.1 else 0.01
        help_text = param_descriptions.get(key, "")
        
        # Initialize session state if not present
        if f"param_{key}" not in st.session_state:
            st.session_state[f"param_{key}"] = float(val)
            
        params[key] = st.sidebar.slider(
            f"{key}", 
            min_value=0.0, 
            max_value=float(max_val), 
            key=f"param_{key}",
            step=step, 
            help=help_text
        )
        
    st.sidebar.subheader("Initial Conditions")
    default_ic = model.get_default_initial_conditions()
    initial_conditions = {}
    
    for key, val in default_ic.items():
        if f"ic_{key}" not in st.session_state:
            st.session_state[f"ic_{key}"] = float(val)
            
        initial_conditions[key] = st.sidebar.number_input(
            f"Initial {key}", 
            min_value=0.0, 
            max_value=1.0, 
            key=f"ic_{key}",
            step=0.00001, # Finer step for small initial populations
            format="%.5f"
        )
        
    # Normalize initial conditions warning
    total_ic = sum(initial_conditions.values())
    if not np.isclose(total_ic, 1.0, atol=1e-3):
        st.sidebar.warning(f"Total initial population is {total_ic:.5f} (Expected ~1.0)")
        
    # --- Embedded Simulation Launcher ---
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎮 Particle Simulation")
    # Toggle to show
    if "show_sim" not in st.session_state:
        st.session_state["show_sim"] = False
        
    if st.sidebar.button("Toggle Physics Sim"):
        st.session_state["show_sim"] = not st.session_state["show_sim"]
        
    if st.session_state["show_sim"]:
        # Extract params for Sim
        # Fallback if beta/gamma not present
        beta_val = params.get("beta", 0.5)
        gamma_val = params.get("gamma", 0.1)
        # Assuming SIR-like I fraction
        init_i_val = initial_conditions.get("I", 0.05) if "I" in initial_conditions else 0.05
        
        st.sidebar.info("Simulating in browser...")
        
        sim_html = get_simulation_html(
            population_size=150, # Keep small for performance
            beta=beta_val,
            gamma=gamma_val,
            initial_i=init_i_val
        )
        
        # Render in main area or sidebar? 
        # Sidebar might be too small. Render in Sidebar dedicated container or bottom.
        # Let's render in sidebar for now as requested "incorporated". 
        # Actually components.html renders in the main flow where called. 
        # Let's put it in the sidebar.
        with st.sidebar:
            components.html(sim_html, height=350, scrolling=False)

    st.sidebar.markdown("---")
    
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
