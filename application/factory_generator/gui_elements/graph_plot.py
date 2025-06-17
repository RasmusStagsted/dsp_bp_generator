import networkx as nx

from PySide6.QtWidgets import QVBoxLayout, QWidget
from ..production_graph.production_graph import ProductionGraph

class GraphPlotWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.graph = ProductionGraph()
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.graph)
        self.setLayout(self.layout)

    def refresh(self):
        self.graph.refresh()

    def set_graph(self, graph: nx.DiGraph):
        self._graph = graph
        self._view.set_graph(graph)
        
    def add_node(self, node):
        self.graph.add_node(node)
        
    def remove_node(self, node):
        self.graph.remove_node(node)