import streamlit as st
from src.models.sir import SIRModel
from src.models.sird import SIRDModel
from src.models.extensions import SIRFModel, SEWIRFModel
from src.ui.layout import render_dashboard

st.set_page_config(
    page_title="Simulation Lab",
    page_icon="🔬",
    layout="wide"
)

def main():
    st.sidebar.title("🔬 Simulation Lab")
    
    # Model Selection
    model_options = {
        "SIR": SIRModel,
        "SIR-D": SIRDModel,
        "SIR-F": SIRFModel,
        "SEWIR-F": SEWIRFModel
    }
    
    model_name = st.sidebar.selectbox("Select Model", list(model_options.keys()))
    
    # Instantiate Model
    model_class = model_options[model_name]
    model_instance = model_class()
    
    # Render Dashboard
    render_dashboard(model_instance)

if __name__ == "__main__":
    main()
