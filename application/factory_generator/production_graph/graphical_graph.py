import networkx as nx

from PySide6.QtCore import QEasingCurve, QParallelAnimationGroup, QPointF, QPropertyAnimation
from PySide6.QtWidgets import QGraphicsScene, QGraphicsView

from ..production_graph.graphical_edge import GraphicalEdge
from ..production_graph.graphical_node import GraphicalNode

class GraphicalGraph(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.graph = nx.DiGraph()
        self._scene = QGraphicsScene()
        self.setScene(self._scene)

        # Used to add space between nodes
        self._graph_scale = 200

        # Map node name to Node object {str=>Node}
        self._nodes_map = {}

        # List of networkx layout function
        self._nx_layout = {
            "circular": nx.circular_layout,
            "planar": nx.planar_layout,
            "random": nx.random_layout,
            "shell_layout": nx.shell_layout,
            "kamada_kawai_layout": nx.kamada_kawai_layout,
            "spring_layout": nx.spring_layout,
            "spiral_layout": nx.spiral_layout,
        }

        self.refresh()
    
    def get_nx_layouts(self) -> list:
        return self._nx_layout.keys()

    def set_nx_layout(self, name: str):
        if name in self._nx_layout:
            self._nx_layout_function = self._nx_layout[name]

            # Compute node position from layout function
            positions = self._nx_layout_function(self.graph)

            # Set node positions directly, no animation
            for node, pos in positions.items():
                x, y = pos
                x *= self._graph_scale
                y *= self._graph_scale
                item = self._nodes_map[node]
                item.setPos(QPointF(x, y))
    
    def refresh(self):
        self.scene().clear()
        self._nodes_map.clear()

        # Add nodes
        for node in self.graph:
            color = "red" if "color" not in self.graph.nodes[node].keys() else self.graph.nodes[node]["color"]
            label = self.graph.nodes[node].get("label", node)
            item = GraphicalNode(
                node,
                label = label,
                label_color = "black",
                color = color
            )
            self.scene().addItem(item)
            self._nodes_map[node] = item

        # Add edges
        for a, b in self.graph.edges:
            source = self._nodes_map[a]
            dest = self._nodes_map[b]
            color = self.graph.edges[a, b].get("color", "#000000")
            label = self.graph.edges[a, b].get("label", "")
            self.scene().addItem(GraphicalEdge(source, dest, color=color, label=label))
        
        self.set_nx_layout("spring_layout")
        
    def add_node(self, node):
        self.graph.add_node(node.name + node.proliferator, node = node)

    def remove_item_flow(self, node):
        self.graph.remove_node(node.name + node.proliferator)

    def generate_label(self, name):
        import re
        label = re.sub(r'(?<!^)(?=[A-Z0-9])', '\n', name)
        return label
    