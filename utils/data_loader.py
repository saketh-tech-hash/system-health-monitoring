from models.graph import Graph
from typing import Dict, Any, List

def load_graph_from_json(json_data: Dict[str, Any]) -> Graph:
    """Load graph from JSON data with array of nodes format"""
    graph = Graph()
    
    # Add nodes from array format
    if isinstance(json_data.get("nodes"), list):
        # Array format
        for node_data in json_data.get("nodes", []):
            node_id = node_data.get("id")
            if node_id:
                # Remove the id from node_data to avoid duplicating it in node attributes
                node_attrs = {k: v for k, v in node_data.items() if k != "id"}
                graph.add_node(node_id, node_attrs)
    elif isinstance(json_data.get("nodes"), dict):
        # Dictionary format
        for node_id, node_data in json_data.get("nodes", {}).items():
            graph.add_node(node_id, node_data)
    
    # Add edges
    for edge in json_data.get("edges", []):
        source = edge.get("source")
        target = edge.get("target")
        if source and target:
            graph.add_edge(source, target)
    
    return graph