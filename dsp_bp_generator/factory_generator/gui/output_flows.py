from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel,
    QComboBox, QLineEdit, QTableWidget, QHeaderView
)
from PySide6.QtGui import QDoubleValidator
from PySide6.QtCore import Qt

from dsp_bp_generator.factory_generator.recipes import Recipe
from dsp_bp_generator.factory_generator import ItemFlow
class OutputFlows(QWidget):
    def __init__(self, proliferator_update_callback = None, any_update_callback = None):
        super().__init__()

        self.proliferator_update_callback = proliferator_update_callback
        self.any_update_callback = any_update_callback

        self.item_flows = []

        self.item = []
        self.flow_rate = []
        self.proliferator = []
        self.delete_button = []

        self.layout = QVBoxLayout()

        self.table_label = QLabel("Select output flows:")
        self.layout.addWidget(self.table_label)
        
        self.table = QTableWidget(1, 4)
        self.table.setHorizontalHeaderLabels(["Item", "Flow rate [items/s]", "Proliferator", "Add/Delete flow"])
        self.table.setSizePolicy(self.table.sizePolicy().horizontalPolicy(), self.table.sizePolicy().verticalPolicy())
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 150)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(True)
        self.layout.addWidget(self.table)

        self.add_button = QPushButton("Add flow")
        self.add_button.clicked.connect(lambda: self.add_flow())
        self.layout.addWidget(self.add_button)

        self.set_flow(0, "None", 1.0, "None")
        
        self.setLayout(self.layout)

    def set_proliferator_change_callback(self, callback = None):
        self.proliferator_update_callback = callback

    def set_any_update_callback(self, callback = None):
        self.any_update_callback = callback

    def set_flow(self, row, item_name, flow_rate, proliferator):
        self.item.append(QComboBox())
        self.item[row].addItems(["None"] + list(Recipe.recipes.keys()))
        self.item[row].currentIndexChanged.connect(self.updated)
        idx = self.item[row].findText(item_name)
        if idx != -1:
            self.item[row].setCurrentIndex(idx)
        self.table.setCellWidget(row, 0, self.item[row])

        self.flow_rate.append(QLineEdit())
        self.flow_rate[row].setText(str(flow_rate))
        self.flow_rate[row].setValidator(QDoubleValidator(0.0, 1e6, 3))
        self.flow_rate[row].textChanged.connect(self.updated)
        self.table.setCellWidget(row, 1, self.flow_rate[row])

        self.proliferator.append(QComboBox())
        self.proliferator[row].addItems(["None", "MK.I", "MK.II", "MK.III"])
        self.proliferator[row].currentIndexChanged.connect(self.update_proliferators)
        idx = self.proliferator[row].findText(proliferator)
        if idx != -1:
            self.proliferator[row].setCurrentIndex(idx)
        self.table.setCellWidget(row, 2, self.proliferator[row])

        self.delete_button.append(QPushButton("Delete flow"))
        self.delete_button[row].clicked.connect(lambda _, btn = self.delete_button[row]: self.remove_flow(btn))
        self.table.setCellWidget(row, 3, self.delete_button[row])

        self.item_flows.append(ItemFlow(item_name, float(flow_rate), proliferator))

    def add_flow(self):
        table_row = self.table.rowCount()
        flow_index = table_row
        
        self.table.insertRow(table_row)

        self.set_flow(table_row, "None", 1.0, "None")
        
    def remove_flow(self, button):
        table_row = self.get_row_from_button(button)
        if table_row == -1:
            return  # Button not found
        else:
            flow_index = table_row - 1
        
        for col in range(4):
            widget = self.table.cellWidget(table_row, col)
            if widget is not None:
                widget.deleteLater()
                self.table.removeCellWidget(table_row, col)
        self.table.removeRow(table_row)
        
        self.item_flows.pop(flow_index)
        self.item.pop(flow_index)
        self.flow_rate.pop(flow_index)
        self.proliferator.pop(flow_index)
        self.delete_button.pop(flow_index)
        self.updated()

    def get_row_from_button(self, button):
        row = -1
        for r in range(self.table.rowCount()):
            if self.table.cellWidget(r, 3) == button:
                row = r
                break
        return row
    
    def update_proliferators(self):
        if self.proliferator_update_callback != None:
            proliferator = [self.proliferator[i].currentText() for i in range(len(self.proliferator))]
            proliferator = list(set(proliferator))
            proliferator.sort()
            if "None" in proliferator:
                proliferator.remove("None")
            self.proliferator_update_callback(proliferator)
        self.updated()
            
    def updated(self):
        if self.any_update_callback is not None:
            self.any_update_callback()