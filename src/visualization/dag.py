import graphviz
from typing import List, Tuple

def render_interaction_graph(compartment_names: List[str], transitions: List[Tuple[str, str, str]]) -> graphviz.Digraph:
    """
    Render a Directed Acyclic Graph (DAG) for the model compartments and transitions.
    
    Args:
        compartment_names: List of all compartment names (nodes).
        transitions: List of (source, target, label) tuples.
        
    Returns:
        graphviz.Digraph
    """
    dot = graphviz.Digraph(comment='Model Interaction Graph')
    dot.attr(rankdir='LR') # Left to Right layout
    
    # Node attributes
    dot.attr('node', shape='circle', style='filled', color='lightblue2', fontname='Helvetica')
    dot.attr('edge', fontname='Helvetica', fontsize='10')

    # Add nodes
    for name in compartment_names:
        dot.node(name, name)
        
    # Add edges
    for source, target, label in transitions:
        dot.edge(source, target, label=label)
        
    return dot
