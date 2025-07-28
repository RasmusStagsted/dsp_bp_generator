from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QLineEdit, QTableWidget, QHeaderView
)
from ..proliferator import ProliferatorNone, ProliferatorMKI, ProliferatorMKII, ProliferatorMKIII
from PySide6.QtGui import QDoubleValidator

from ..recipes import Recipe

class IntermidiateFlows(QWidget):
    
    class IntermidiateFlow:
        
        def __init__(self, item, flow_rate, proliferator):
            self.item_combo = item
            self.flow_rate = flow_rate
            self.proliferator = proliferator
            
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        
        self.label = QLabel("Input flows:")
        self.layout.addWidget(self.label)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Item", "Flow rate [items/s]", "Proliferator"])
        self.table.setSizePolicy(self.table.sizePolicy().horizontalPolicy(), self.table.sizePolicy().verticalPolicy())
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 100)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(True)
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)
        
    def proliferator_option_changed(self):
        pass
    
    def remove_all_input_flows(self):
        while self.table.rowCount() > 0:
            self.table.removeRow(0)
    
    def add_input_flow(self, item_name, flow_rate, proliferator):
        proliferator_name = {
            ProliferatorNone: "None",
            ProliferatorMKI: "MK.I",
            ProliferatorMKII: "MK.II",
            ProliferatorMKIII: "MK.III"
        }
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        
        item_combo = QLabel(" " + item_name)
        flow_rate_edit = QLabel(" " + str(flow_rate))

        proliferator_combo = QLabel(" " + proliferator_name[proliferator])

        self.table.setCellWidget(row_position, 0, item_combo)
        self.table.setCellWidget(row_position, 1, flow_rate_edit)
        self.table.setCellWidget(row_position, 2, proliferator_combo)
    
    def update(self, graph):
        self.remove_all_input_flows()
        
        for node_name in graph.graph.nodes:
            node = graph.graph.nodes[node_name]
            if list(graph.graph.predecessors(node_name)) == []:
                self.add_input_flow(node["name"], node["items_per_second"], node["proliferator"])