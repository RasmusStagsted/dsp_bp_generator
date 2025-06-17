from dataclasses import dataclass
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel,
    QComboBox, QDoubleSpinBox, QTableWidget, QHeaderView
)
from PySide6.QtGui import QDoubleValidator
from PySide6.QtCore import Qt

from ..recipes import Recipe
from ..item_flow import ItemFlow

class OutputFlows(QWidget):
    
    @dataclass
    class Callbacks:
        flow_created_callback: callable = None
        flow_deleted_callback: callable = None
        item_changed_callback: callable = None
        flow_rate_changed_callback: callable = None
        proliferator_changed_callback: callable = None
        any_changed_callback: callable = None
    
    def __init__(self):
        super().__init__()
        
        self.callbacks = self.Callbacks()
        
        self.last_item_text = []
        self.item = []
        self.flow_rate = []
        self.proliferator = []
        self.delete_button = []

        self.layout = QVBoxLayout()
        self.table_label = QLabel("Select output flows:")
        self.layout.addWidget(self.table_label)
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Item", "Flow rate [items/s]", "Proliferator", "Add/Delete flow"])
        self.table.setSizePolicy(self.table.sizePolicy().horizontalPolicy(), self.table.sizePolicy().verticalPolicy())
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(True)
        self.layout.addWidget(self.table)
        self.add_button = QPushButton("Add flow")
        self.add_button.clicked.connect(lambda: self.add_flow())
        self.layout.addWidget(self.add_button)
        self.setLayout(self.layout)

    def set_proliferator_change_callback(self, callback = None):
        self.proliferator_update_callback = callback

    def set_callbacks(self, flow_created_callback = None, flow_deleted_callback = None,
                      item_changed_callback = None, flow_rate_changed_callback = None,
                      proliferator_changed_callback = None, any_changed_callback = None):
        if not flow_created_callback is None:
            self.callbacks.flow_created_callback = flow_created_callback
        if not flow_deleted_callback is None:
            self.callbacks.flow_deleted_callback = flow_deleted_callback
        if not item_changed_callback is None:
            self.callbacks.item_changed_callback = item_changed_callback
        if not flow_rate_changed_callback is None:
            self.callbacks.flow_rate_changed_callback = flow_rate_changed_callback
        if not proliferator_changed_callback is None:
            self.callbacks.proliferator_changed_callback = proliferator_changed_callback
        if not any_changed_callback is None:
            self.callbacks.any_changed_callback = any_changed_callback

    def set_flow(self, row, item_name, flow_rate, proliferator, update = True):
        self.item.append(QComboBox())
        options = list(Recipe.recipes.keys())
        options.sort()
        self.item[row].addItems(options)
        self.item[row].currentIndexChanged.connect(lambda _, r=row: self.item_changed(r))
        if item_name is None:
            self.item[row].setCurrentIndex(0)
            item_name = self.item[row].currentText()
        idx = self.item[row].findText(item_name)
        if idx != -1:
            self.item[row].setCurrentIndex(idx)
        print(f"Setting item {item_name} at row {row}")
        self.last_item_text.append(item_name)
        self.table.setCellWidget(row, 0, self.item[row])
        self.flow_rate.append(QDoubleSpinBox())
        self.flow_rate[row].setRange(0, 1e6)
        self.flow_rate[row].setSingleStep(1.0)
        self.flow_rate[row].setValue(float(flow_rate))
        self.flow_rate[row].textChanged.connect(lambda _, r=row: self.flow_rate_changed(r))
        self.table.setCellWidget(row, 1, self.flow_rate[row])
        self.proliferator.append(QComboBox())
        self.proliferator[row].addItems(["None", "MK.I", "MK.II", "MK.III"])
        self.proliferator[row].currentIndexChanged.connect(lambda _, r=row: self.proliferator_changed(r))
        idx = self.proliferator[row].findText(proliferator)
        if idx != -1:
            self.proliferator[row].setCurrentIndex(idx)
        self.table.setCellWidget(row, 2, self.proliferator[row])
        self.delete_button.append(QPushButton("Delete flow"))
        self.delete_button[row].clicked.connect(lambda _, btn = self.delete_button[row]: self.remove_flow(btn))
        self.table.setCellWidget(row, 3, self.delete_button[row])
        self.flow_created(row)

    def add_flow(self, update = True):
        flow_index = self.table.rowCount()
        flow_index = flow_index
        self.table.insertRow(flow_index)
        self.set_flow(flow_index, None, 1.0, "None")
        if update:
            self.changed()
        
    def remove_flow(self, button, update = True):
        flow_index = self.get_row_from_button(button)
        self.flow_deleted(flow_index)
        for col in range(4):
            widget = self.table.cellWidget(flow_index, col)
            if widget is not None:
                widget.deleteLater()
                self.table.removeCellWidget(flow_index, col)
        self.table.removeRow(flow_index)
        self.last_item_text.pop(flow_index)
        self.item.pop(flow_index)
        self.flow_rate.pop(flow_index)
        self.proliferator.pop(flow_index)
        self.delete_button.pop(flow_index)
        if update:
            self.changed()

    def get_row_from_button(self, button):
        row = -1
        for r in range(self.table.rowCount()):
            if self.table.cellWidget(r, 3) == button:
                row = r
                break
        return row
    
    def flow_created(self, index):
        if self.callbacks.flow_created_callback is not None:
            self.callbacks.flow_created_callback(self.item, self.flow_rate, self.proliferator, index)
        self.changed()

    def flow_deleted(self, index):
        if self.callbacks.flow_deleted_callback is not None:
            self.callbacks.flow_deleted_callback(self.item, self.flow_rate, self.proliferator, index)
        self.changed()

    def item_changed(self, index):
        if self.callbacks.item_changed_callback is not None:
            self.callbacks.item_changed_callback(self.item, self.flow_rate, self.proliferator, index)
        self.changed()

    def flow_rate_changed(self, index):
        if self.callbacks.flow_rate_changed_callback is not None:
            self.callbacks.flow_rate_changed_callback(self.item, self.flow_rate, self.proliferator, index)
        self.changed()

    def proliferator_changed(self, index):
        if self.callbacks.proliferator_changed_callback != None:
            self.callbacks.proliferator_changed_callback(self.item, self.flow_rate, self.proliferator, index)
        self.changed()

    def changed(self):
        if self.callbacks.any_changed_callback is not None:
            self.callbacks.any_changed_callback()