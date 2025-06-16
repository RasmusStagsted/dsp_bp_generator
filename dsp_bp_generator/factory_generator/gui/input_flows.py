from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QLineEdit, QTableWidget, QHeaderView
)
from PySide6.QtGui import QDoubleValidator
from dsp_bp_generator.factory_generator.recipes import Recipe

class InputFlows(QWidget):
    
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        
        self.proliferator_layout = QHBoxLayout()
        self.proliferator_layout.addWidget(QLabel("Proliferator:"))
        self.proliferator_selector = QComboBox()
        self.proliferator_selector.addItems(["None", "MK.I", "MK.II", "MK.III", "Individual"])
        self.proliferator_selector.currentTextChanged.connect(self.proliferator_option_changed)
        self.proliferator_layout.addWidget(self.proliferator_selector)
        self.layout.addLayout(self.proliferator_layout)

        self.label = QLabel("Input flows:")
        self.layout.addWidget(self.label)

        self.table = QTableWidget(1, 3)
        self.table.setHorizontalHeaderLabels(["Item", "Flow rate [items/s]", "Proliferator"])
        self.table.setSizePolicy(self.table.sizePolicy().horizontalPolicy(), self.table.sizePolicy().verticalPolicy())
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 100)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(True)
        self.layout.addWidget(self.table)

        self.item = QLabel("")
        self.table.setCellWidget(0, 0, self.item)

        self.flow_rate = QLabel("")
        self.table.setCellWidget(0, 1, self.flow_rate)

        self.proliferator = QComboBox()
        self.proliferator.addItems(["None", "MK.I", "MK.II", "MK.III"])
        self.table.setCellWidget(0, 2, self.proliferator)

        self.setLayout(self.layout)
    
    def update(self, input_flows):
        for flow in input_flows:
            print(flow)
    
    def proliferator_option_changed(self):
        pass
    