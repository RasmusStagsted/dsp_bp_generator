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
        
    def increase_flow(self, node):
        self.graph.change_required_flow_rate(node.name, node.count_per_second, node.proliferator)
        
    def reduce_flow(self, node):
        self.graph.change_required_flow_rate(node.name, -node.count_per_second, node.proliferator)
        