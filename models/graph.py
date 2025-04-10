import networkx as nx
from typing import Dict, List, Any

class Graph:
    def __init__(self):
        self.graph = nx.DiGraph()
        
    def add_node(self, node_id: str, data: Dict[str, Any]):
        self.graph.add_node(node_id, **data)
        
    def add_edge(self, source: str, target: str):
        self.graph.add_edge(source, target)
        
    def get_nodes(self):
        return self.graph.nodes(data=True)
    
    def get_edges(self):
        return self.graph.edges()
    
    def get_predecessors(self, node_id: str):
        return list(self.graph.predecessors(node_id))
    
    def get_successors(self, node_id: str):
        return list(self.graph.successors(node_id))
    
    def bfs_traversal(self, start_node=None):
        """Traverse the graph in breadth-first search order"""
        if start_node is None:
            # Find root nodes (nodes with no predecessors)
            root_nodes = [node for node, in_degree in self.graph.in_degree() if in_degree == 0]
            
            if not root_nodes:
                # If no root nodes found, use the first node
                root_nodes = list(self.graph.nodes())[0:1]
        else:
            root_nodes = [start_node]
            
        visited = set()
        traversal_order = []
        
        for root in root_nodes:
            if root not in visited:
                queue = [root]
                visited.add(root)
                
                while queue:
                    current = queue.pop(0)
                    traversal_order.append(current)
                    
                    for neighbor in self.graph.successors(current):
                        if neighbor not in visited:
                            queue.append(neighbor)
                            visited.add(neighbor)
                            
        return traversal_order