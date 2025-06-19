from dataclasses import dataclass
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel,
    QComboBox, QDoubleSpinBox, QTableWidget, QHeaderView
)
from PySide6.QtGui import QDoubleValidator
from PySide6.QtCore import Qt
import logging

from ..recipes import Recipe
from ..item_flow import ItemFlow

class OutputFlows(QWidget):
    
    class OutputFlow:
        
        def __init__(self):
            pass
        
        def set(self, item, flow_rate, proliferator):
            self.item_combo = item
            self.lasts_name = self.item_combo.currentText()
            self.flow_rate = flow_rate
            self.last_flow_rate = self.flow_rate.value()
            self.proliferator = proliferator
            self.last_proliferator = proliferator.currentText()
            
        def get_item_flow(self):
            return ItemFlow(
                name = self.item_combo.currentText(),
                count_per_second = float(self.flow_rate.value()),
                proliferator = self.proliferator.currentText()
            )
        
        def get_old_item_flow(self):
            return ItemFlow(
                name = self.lasts_name,
                count_per_second = self.last_flow_rate,
                proliferator = self.last_proliferator
            )
    
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
        
        self.output_flows = []
        
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

    def create_item_combo_box(self, row, item_name):
        item = QComboBox()
        options = list(Recipe.recipes.keys())
        options.sort()
        item.addItems(options)
        item.currentIndexChanged.connect(lambda _, r = row: self.item_changed(r))
        if item_name is None:
            item.setCurrentIndex(0)
            item_name = item.currentText()
        idx = item.findText(item_name)
        if idx != -1:
            item.setCurrentIndex(idx)
        return item

    def create_flow_rate_spin_box(self, row, count_per_second):
        flow_rate = QDoubleSpinBox()
        flow_rate.setRange(0, 1e6)
        flow_rate.setSingleStep(1.0)
        flow_rate.setValue(float(count_per_second))
        flow_rate.textChanged.connect(lambda _, r = row: self.flow_rate_changed(r))
        return flow_rate
        
    def create_proliferator_combo_box(self, row, proliferator_name):
        proliferator = QComboBox()
        proliferator.addItems(["None", "MK.I", "MK.II", "MK.III"])
        proliferator.currentIndexChanged.connect(lambda _, r = row: self.proliferator_changed(r))
        idx = proliferator.findText(proliferator_name)
        if idx != -1:
            proliferator.setCurrentIndex(idx)
        return proliferator
    
    def create_delete_button(self, row):
        delete_button = QPushButton("Delete flow")
        delete_button.clicked.connect(lambda _, btn = delete_button: self.remove_flow(btn))
        return delete_button
    
    def set_flow(self, row, item_name, count_per_second, proliferator_name, update = True):
        item = self.create_item_combo_box(row, item_name)
        self.table.setCellWidget(row, 0, item)
        flow_rate = self.create_flow_rate_spin_box(row, count_per_second)
        self.table.setCellWidget(row, 1, flow_rate)
        proliferator = self.create_proliferator_combo_box(row, proliferator_name)
        self.table.setCellWidget(row, 2, proliferator)        
        self.delete_button.append(self.create_delete_button(row))
        self.table.setCellWidget(row, 3, self.delete_button[row])

        self.output_flows[row].set(item, flow_rate, proliferator)
        self.flow_created(row, update = False)
        if update:
            self.changed()

    def add_flow(self, update = True):
        self.output_flows.append(OutputFlows.OutputFlow())
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.set_flow(row, None, 1.0, "None", update = False)
        if update:
            self.changed()
        logging.debug(f"Added flow at row {row}")
        
    def remove_flow(self, button, update = True):
        flow_index = self.get_row_from_button(button)
        logging.debug(f"Removed flow at row {flow_index}")
        self.flow_deleted(flow_index)
        for col in range(4):
            widget = self.table.cellWidget(flow_index, col)
            if widget is not None:
                widget.deleteLater()
                self.table.removeCellWidget(flow_index, col)
        self.table.removeRow(flow_index)
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
    
    def flow_created(self, index, update = True):
        if self.callbacks.flow_created_callback is not None:
            self.callbacks.flow_created_callback(self.output_flows, index)
        if update:
            self.changed()

    def flow_deleted(self, index, update = True):
        if self.callbacks.flow_deleted_callback is not None:
            self.callbacks.flow_deleted_callback(self.output_flows, index)
        if update:
            self.changed()

    def item_changed(self, index, update = True):
        if self.callbacks.item_changed_callback is not None:
            self.callbacks.item_changed_callback(self.output_flows, index)
        if update:
            self.changed()
        self.output_flows[index].lasts_name = self.output_flows[index].item_combo.currentText()

    def flow_rate_changed(self, index, update = True):
        if self.callbacks.flow_rate_changed_callback is not None:
            self.callbacks.flow_rate_changed_callback(self.output_flows, index)
        if update:
            self.changed()
        self.output_flows[index].last_flow_rate = float(self.output_flows[index].flow_rate.value())

    def proliferator_changed(self, index, update = True):
        if self.callbacks.proliferator_changed_callback != None:
            self.callbacks.proliferator_changed_callback(self.output_flows, index)
        if update:
            self.changed()
        self.output_flows[index].last_proliferator = self.output_flows[index].proliferator.currentText()

    def changed(self):
        if self.callbacks.any_changed_callback is not None:
            self.callbacks.any_changed_callback(self.output_flows)