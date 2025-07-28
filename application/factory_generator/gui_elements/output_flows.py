from dataclasses import dataclass
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel,
    QComboBox, QDoubleSpinBox, QTableWidget, QHeaderView
)
from PySide6.QtWidgets import QSizePolicy

from PySide6.QtGui import QDoubleValidator
from PySide6.QtCore import Qt
import logging

from ..recipes import Recipe
from ..item_flow import ItemFlow

class OutputFlows(QWidget):
    
    class OutputFlow:
        
        def __init__(self, item, flow_rate, proliferator):
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
        self.table = QTableWidget(0, 5)
        header_labels = ["Item", "Flow rate [items/s]", "Proliferator", "Destination", "Add/Delete flow"]
        self.table.setHorizontalHeaderLabels(header_labels)

        font_metrics = self.table.fontMetrics()
        for col, label in enumerate(header_labels):
            width = font_metrics.horizontalAdvance(label) + 24  # Add some padding
            self.table.setColumnWidth(col, width)
            self.table.horizontalHeader().setMinimumSectionSize(width)

        self.table.setSizePolicy(self.table.sizePolicy().horizontalPolicy(), self.table.sizePolicy().verticalPolicy())
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(True)

        self.layout.addWidget(self.table)
        self.add_button = QPushButton("Add flow")
        self.add_button.clicked.connect(lambda: self.add_flow())
        self.layout.addWidget(self.add_button)
        self.setLayout(self.layout)
        self.setSizePolicy(self.sizePolicy().horizontalPolicy(), QSizePolicy.Fixed)

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

    def create_item_combo_box(self, row, item_name = None):
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

    def create_flow_rate_spin_box(self, row, count_per_second = 1.0):
        flow_rate = QDoubleSpinBox()
        flow_rate.setRange(0, 1e6)
        flow_rate.setSingleStep(1.0)
        flow_rate.setValue(float(count_per_second))
        flow_rate.textChanged.connect(lambda _, r = row: self.flow_rate_changed(r))
        return flow_rate
        
    def create_proliferator_combo_box(self, row, proliferator_name = "No-Proliferator"):
        proliferator = QComboBox()
        proliferator.addItems(["No-Proliferator", "MK.I", "MK.II", "MK.III"])
        proliferator.currentIndexChanged.connect(lambda _, r = row: self.proliferator_changed(r))
        idx = proliferator.findText(proliferator_name)
        if idx != -1:
            proliferator.setCurrentIndex(idx)
        return proliferator
    
    def set_flow(self, row, item_name, count_per_second, proliferator_name, update = True):
        item = self.create_item_combo_box(row, item_name)
        self.table.setCellWidget(row, 0, item)
        flow_rate = self.create_flow_rate_spin_box(row, count_per_second)
        self.table.setCellWidget(row, 1, flow_rate)
        proliferator = self.create_proliferator_combo_box(row, proliferator_name)
        self.table.setCellWidget(row, 2, proliferator)

        self.output_flows[row].set(item, flow_rate, proliferator)
        if update:
            self.changed()
    
    def create_delete_button(self):
        delete_button = QPushButton("Delete flow")
        delete_button.clicked.connect(lambda _, btn = delete_button: self.remove_flow(self.get_row_from_button(btn)))
        return delete_button

    def adjust_table_height(self):
        header_height = self.table.horizontalHeader().height()
        row_count = self.table.rowCount()
        row_height = self.table.verticalHeader().defaultSectionSize()
        total_height = header_height + (row_height * max(1, row_count)) + 4  # Add a small margin
        self.table.setMinimumHeight(total_height)
        self.table.setMaximumHeight(total_height)

    def add_flow(self, update = True):
        row = self.table.rowCount()
        self.table.insertRow(row)
        
        item = self.create_item_combo_box(row)
        flow_rate = self.create_flow_rate_spin_box(row)
        proliferator = self.create_proliferator_combo_box(row)
        destination = QComboBox()
        destination.addItems(["Belt", "PLS", "ILS"])
        self.output_flows.append(OutputFlows.OutputFlow(item, flow_rate, proliferator))
        self.table.setCellWidget(row, 0, item)
        self.table.setCellWidget(row, 1, flow_rate)
        self.table.setCellWidget(row, 2, proliferator)
        self.table.setCellWidget(row, 3, destination)
        self.delete_button.append(self.create_delete_button())
        self.table.setCellWidget(row, 4, self.delete_button[row])
        
        self.flow_created(row, update = False)
        self.adjust_table_height()
        if update:
            self.changed()
        
    def remove_flow(self, flow_index, update = True):
        self.flow_deleted(flow_index)
        for col in range(4):
            widget = self.table.cellWidget(flow_index, col)
            if widget is not None:
                widget.deleteLater()
                self.table.removeCellWidget(flow_index, col)
        self.table.removeRow(flow_index)
        self.delete_button.pop(flow_index)
        self.output_flows.pop(flow_index)
        self.adjust_table_height()
        if update:
            self.changed()

    def get_row_from_button(self, button):
        row = -1
        for r in range(self.table.rowCount()):
            if self.table.cellWidget(r, 3) == button:
                row = r
                break
        return row
    
    def get_output_destination(self):
        output_destinations = {}
        for row in range(self.table.rowCount()):
            item = self.table.cellWidget(row, 0).currentText().strip()
            proliferator = self.table.cellWidget(row, 2).currentText().strip()
            destination = {
                "type": self.table.cellWidget(row, 3).currentText(),
                "items_per_second": float(self.table.cellWidget(row, 1).text().strip())   
            }
            output_destinations[item + proliferator] = destination
        return output_destinations
    
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

    def print(self):
        for i, flow in enumerate(self.output_flows):
            logging.info(str(i) + ":" + (self.output_flows[i].item_combo.currentText() if self.output_flows[i].item_combo else "None"))
            logging.info(str(i) + ":" + str(self.output_flows[i].flow_rate.value() if self.output_flows[i].flow_rate else "None"))
            logging.info(str(i) + ":" + (self.output_flows[i].proliferator.currentText() if self.output_flows[i].proliferator else "No-proliferator"))

if __name__ == "__main__":
    
    from PySide6.QtWidgets import QApplication
    app = QApplication()
    output_flows = OutputFlows()
    output_flows.show()
    output_flows.add_flow()
    output_flows.add_flow()
    output_flows.set_flow(0, "Iron Plate", 10.0, "MK.I")
    output_flows.set_flow(1, "Copper Plate", 5.0, "MK.II")
    output_flows.remove_flow(0)
    output_flows.remove_flow(0)
    print(0)