from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QLineEdit, QTableWidget, QHeaderView
)
from PySide6.QtWidgets import QSizePolicy

from ..proliferator import ProliferatorNone, ProliferatorMKI, ProliferatorMKII, ProliferatorMKIII
from PySide6.QtGui import QDoubleValidator

from ..recipes import Recipe

class InputFlows(QWidget):
    
    class InputFlow:
        
        def __init__(self, item, flow_rate, proliferator):
            self.item_combo = item
            self.flow_rate = flow_rate
            self.proliferator = proliferator
            
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        
        self.label = QLabel("Input flows:")
        self.layout.addWidget(self.label)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Item", "Flow rate [items/s]", "Proliferator", "Source"])
        self.table.setSizePolicy(self.table.sizePolicy().horizontalPolicy(), self.table.sizePolicy().verticalPolicy())
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 100)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(True)
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)
        self.setSizePolicy(self.sizePolicy().horizontalPolicy(), QSizePolicy.Fixed)

    def proliferator_option_changed(self):
        pass
    
    def adjust_table_height(self):
        header_height = self.table.horizontalHeader().height()
        row_count = self.table.rowCount()
        row_height = self.table.verticalHeader().defaultSectionSize()
        total_height = header_height + (row_height * max(1, row_count)) + 4  # Add a small margin
        self.table.setMinimumHeight(total_height)
        self.table.setMaximumHeight(total_height)

    def remove_all_input_flows(self):
        while self.table.rowCount() > 0:
            self.table.removeRow(0)
        self.adjust_table_height()

    def add_input_flow(self, item_name, flow_rate, proliferator):
        proliferator_name = {
            ProliferatorNone: "No-Proliferator",
            ProliferatorMKI: "MK.I",
            ProliferatorMKII: "MK.II",
            ProliferatorMKIII: "MK.III"
        }
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        
        item = QLabel(" " + item_name)
        flow_rate = QLabel(" " + str("{:.2f}".format(flow_rate)))
        proliferator = QLabel(" " + proliferator_name[proliferator])
        source = QComboBox()
        source.addItems(["Belt", "PLS", "ILS"])

        self.table.setCellWidget(row_position, 0, item)
        self.table.setCellWidget(row_position, 1, flow_rate)
        self.table.setCellWidget(row_position, 2, proliferator)
        self.table.setCellWidget(row_position, 3, source)
        self.adjust_table_height()
    
    def update(self, graph):
        self.remove_all_input_flows()
        
        for node_name in graph.graph.nodes:
            node = graph.graph.nodes[node_name]
            if list(graph.graph.predecessors(node_name)) == []:
                self.add_input_flow(node["name"], node["items_per_second"], node["proliferator"])
                
    def get_input_sources(self):
        input_sources = {}
        for row in range(self.table.rowCount()):
            item = self.table.cellWidget(row, 0).text().strip()
            proliferator = self.table.cellWidget(row, 2).text().strip()
            source = {
                "type": self.table.cellWidget(row, 3).currentText(),
                "items_per_second": float(self.table.cellWidget(row, 1).text().strip())
            }        
            input_sources[item + proliferator] = source

        return input_sources