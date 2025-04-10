# utils/graph_visualizer.py
import networkx as nx
import matplotlib.pyplot as plt
import io
import base64
from models.graph import Graph
from typing import Dict, Any
import os
import datetime

class GraphVisualizer:
    def __init__(self):
        self.node_size = 2000
        self.font_size = 10
        self.arrow_size = 20
        self.figure_size = (14, 10)  # Larger figure for more space
        self.static_dir = "static"
    
    def visualize(self, graph: Graph, health_results: Dict[str, Dict[str, Any]]) -> Dict[str, str]:
        """Visualize the graph and highlight failed components in red"""
        # Create a new matplotlib figure
        plt.figure(figsize=self.figure_size)
        
        # Get networkx graph
        nx_graph = graph.graph
        
        # Create position layout with more scattering
        # Increase k value to push nodes further apart
        # More iterations for better convergence
        pos = nx.spring_layout(
            nx_graph, 
            k=0.6,          # Increase this value to scatter nodes more (default is 0.1)
            iterations=100,  # More iterations for better layout
            seed=42          # For reproducibility
        )
        
        # Create node colors based on health status
        node_colors = []
        for node in nx_graph.nodes():
            if node in health_results:
                node_colors.append('green' if health_results[node]["status"] else 'red')
            else:
                node_colors.append('gray')
        
        # Draw the graph
        nx.draw(
            nx_graph, 
            pos, 
            with_labels=True, 
            node_color=node_colors,
            node_size=self.node_size, 
            font_size=self.font_size,
            arrowsize=self.arrow_size,
            font_weight='bold',
            edge_color='gray',
            alpha=0.9,        # Slightly transparent nodes
            width=1.5,        # Thicker edges
            arrows=True       # Show arrows for directed edges
        )
        
        # Create timestamp for unique filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"graph_{timestamp}.png"
        filepath = os.path.join(self.static_dir, filename)
        
        # Save figure to both a file and convert to base64
        plt.savefig(filepath, format='png', dpi=150, bbox_inches='tight')
        
        # Also create base64 representation for embedding in HTML
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        
        # Close the figure to free memory
        plt.close()
        
        return {
            "base64": image_base64,
            "filename": filename,
            "filepath": filepath
        }