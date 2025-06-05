import sys
import math
import argparse
from dataclasses import dataclass

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, QPushButton, QLabel,
    QComboBox, QLineEdit, QTableWidget, QStyledItemDelegate, QTabWidget
)
from PySide6.QtGui import QDoubleValidator
from PySide6.QtCore import Qt

from dsp_bp_generator.utils import Yaw, Vector
from dsp_bp_generator.blueprint import Blueprint
from dsp_bp_generator.factory_generator import (
    Factory, ItemFlow, recipes, FactorySection, Recipe
)
from dsp_bp_generator.factory_generator.factory_router_interface import FactoryRouterInterface, FactoryRouterBelt
from dsp_bp_generator.factory_generator.factory_block_interface import FactoryBlockInterface, FactoryBlockBelt
from dsp_bp_generator.buildings import Building

# import pyperclip

class OutputFlows(QWidget):
    def __init__(self):
        super().__init__()

        self.item = []
        self.flow_rate = []
        self.proliferator = []
        self.delete_button = []

        self.layout = QVBoxLayout()

        self.table = QTableWidget(2, 4)
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 150)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        self.layout.addWidget(self.table)

        label_item = QLabel("Item name")
        label_item.setAlignment(Qt.AlignCenter)
        self.table.setCellWidget(0, 0, label_item)

        label_flow = QLabel("Flow rate [items/s]")
        label_flow.setAlignment(Qt.AlignCenter)
        self.table.setCellWidget(0, 1, label_flow)

        label_proliferator = QLabel("Proliferator")
        label_proliferator.setAlignment(Qt.AlignCenter)
        self.table.setCellWidget(0, 2, label_proliferator)

        label_add = QLabel("Add/Delete flow")
        label_add.setAlignment(Qt.AlignCenter)
        self.table.setCellWidget(0, 3, label_add)

        self.add_button = QPushButton("Add flow")
        self.table.setCellWidget(1, 3, self.add_button)
        self.add_button.clicked.connect(lambda: self.add_flow())

        self.add_flow()
        
        self.setLayout(self.layout)

    def add_flow(self):
        table_row = self.table.rowCount() - 1
        flow_index = table_row - 1
        
        self.table.insertRow(table_row)

        self.item.append(QComboBox())
        self.item[flow_index].addItems(["None"] + list(Recipe.recipes.keys()))
        # Set default to 'Gear' if it exists
        idx = self.item[flow_index].findText("Gear")
        if idx != -1:
            self.item[flow_index].setCurrentIndex(idx)
        self.table.setCellWidget(table_row, 0, self.item[flow_index])

        self.flow_rate.append(QLineEdit())
        self.flow_rate[flow_index].setText("1.0")
        self.flow_rate[flow_index].setValidator(QDoubleValidator(0.0, 1e6, 3))
        self.table.setCellWidget(table_row, 1, self.flow_rate[flow_index])

        self.proliferator.append(QComboBox())
        self.proliferator[flow_index].addItems(["None", "MK.I", "MK.II", "MK.III"])
        self.table.setCellWidget(table_row, 2, self.proliferator[flow_index])

        self.delete_button.append(QPushButton("Delete flow"))
        self.delete_button[flow_index].clicked.connect(lambda _, btn = self.delete_button[flow_index]: self.remove_flow(btn))
        self.table.setCellWidget(table_row, 3, self.delete_button[flow_index])
        
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
        
        self.item.pop(flow_index)
        self.flow_rate.pop(flow_index)
        self.proliferator.pop(flow_index)
        self.delete_button.pop(flow_index)

    def get_row_from_button(self, button):
        row = -1
        for r in range(self.table.rowCount()):
            if self.table.cellWidget(r, 3) == button:
                row = r
                break
        return row

class ProliferatorAssemblySelection(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.mki_label = QLabel("Proliferator MK.I assembly:")
        self.mki = QComboBox()
        self.mki.addItems(["Local", "External"])
        self.layout.addWidget(self.mki_label)
        self.layout.addWidget(self.mki)

        self.mkii_label = QLabel("Proliferator MK.II assembly:")
        self.mkii = QComboBox()
        self.mkii.addItems(["Local", "External"])
        self.layout.addWidget(self.mkii_label)
        self.layout.addWidget(self.mkii)

        self.mkiii_label = QLabel("Proliferator MK.III assembly:")
        self.mkiii = QComboBox()
        self.mkiii.addItems(["Local", "External"])
        self.layout.addWidget(self.mkiii_label)
        self.layout.addWidget(self.mkiii)

        self.setLayout(self.layout)
        
    def get_proliferator_assembly(self):
        return {
            "MK.I": self.mki.currentText(),
            "MK.II": self.mkii.currentText(),
            "MK.III": self.mkiii.currentText()
        }

class BlueprintStringWidget(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.layout = QVBoxLayout()

        self.blueprint = QLineEdit()
        self.layout.addWidget(self.blueprint)
        
        self.copy = QPushButton("Copy blueprint!")
        self.copy.clicked.connect(self.copy_blueprint)
        self.layout.addWidget(self.copy)
        
        self.setLayout(self.layout)

    def copy_blueprint(self):
        try:
            import pyperclip
            pyperclip.copy(self.blueprint.text())
        except ImportError:
            print("pyperclip not installed, clipboard copy skipped.")
        print(self.blueprint.text())

    def set_blueprint_string(self, bp_string):
        self.blueprint.setText(bp_string)

class GeneratorWidget(QWidget):
    
    def __init__(self):
        super().__init__()

        self.tabs = QTabWidget()

        # First tab: Factory Generator
        self.factory_tab = QWidget()
        self.factory_layout = QVBoxLayout()

        self.output_flows = OutputFlows()
        self.factory_layout.addWidget(self.output_flows)

        self.proliferator = ProliferatorAssemblySelection()
        self.factory_layout.addWidget(self.proliferator)

        self.generator_button = QPushButton("Generate blueprint!")
        self.generator_button.clicked.connect(self.update_production_flows)
        self.factory_layout.addWidget(self.generator_button)

        self.factory_layout.addWidget(QLabel("Blueprint string:"))

        self.blueprint = BlueprintStringWidget()
        self.factory_layout.addWidget(self.blueprint)

        self.factory_tab.setLayout(self.factory_layout)
        self.tabs.addTab(self.factory_tab, "Output flows")

        # Second tab: About (example)
        self.about_tab = QWidget()
        about_layout = QVBoxLayout()
        about_label = QLabel("Dyson Sphere Program Factory Blueprint Generator\nVersion 0.1.0\nBy Stagsted")
        about_label.setAlignment(Qt.AlignCenter)
        about_layout.addWidget(about_label)
        
        # Add clickable GitHub link
        github_label = QLabel('<a href="https://github.com/RasmusStagsted/dsp_bp_generator">GitHub: RasmusStagsted/dsp_bp_generator</a>')
        github_label.setOpenExternalLinks(True)
        github_label.setAlignment(Qt.AlignCenter)
        about_layout.addWidget(github_label)
        self.about_tab.setLayout(about_layout)
        self.tabs.addTab(self.about_tab, "About")

        # Set main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

        self.update()

    def update(self):

        self.update_production_flows()

        #self.generate_factories()
        
        blueprint = Blueprint()
        #blueprint_string = blueprint.serialize(Building.buildings)
        #self.blueprint.blueprint.setText(blueprint_string)

    def update_production_flows(self):
        requirement_stack = []
        production_stack = []

        for i in range(len(self.output_flows.item)):
            item = self.output_flows.item[i].currentText()
            flow_rate = float(self.output_flows.flow_rate[i].text())
            proliferator = self.output_flows.proliferator[i].currentText()
            requirement_stack.append(
                ItemFlow(item, flow_rate, proliferator)
            )

        while len(requirement_stack) > 0:
            
            item = requirement_stack.pop()
            
            # Add ingredients to stack
            for ingredient in item.get_needed_ingredients("None"):
                requirement_stack.append(ingredient)

            # Add item to production stack
            index = -1
            for i in range(len(production_stack)):
                if production_stack[i].name == item.name:
                    index = i
                    break
            if index != -1:
                ingredient_to_bump = production_stack.pop(index)
                ingredient_to_bump.count_pr_sec += item.count_pr_sec
                production_stack.append(ingredient_to_bump)
            else:
                production_stack.append(item)

        self.target_output_flow = production_stack
        self.input_flow = []
        for flow in self.target_output_flow:
            if not flow.name in Recipe.recipes:
                self.input_flow.append(flow)
                self.target_output_flow.remove(flow)

        production_stack = production_stack[::-1] 
        self.generate_factories()

    def generate_factories(self, debug = False):

        # Print input flow
        if debug:
            print("Input flow:")
            for item in self.input_flow:
                print(f"\t{item.name}, {item.count_pr_sec}/s, {item.proliferator}")

        # Print target output flow
        if debug:
            print("Target output flow:")
            for item in self.target_output_flow:
                print(f"\t{item.name}, {item.count_pr_sec}/s, {item.proliferator}")

        # Define main belt
        self.main_belts = []
        for item in self.input_flow:
            self.main_belts.append(item)
        for item in self.target_output_flow:
            self.main_belts.append(item)
        
        # Print debug for main belt
        if debug:
            print("Main belts:")
            for belt in self.main_belts:
                print(f"\t{belt.name}, {belt.count_pr_sec}/s")

        self.factories = []
        input_count = len(self.input_flow)
        output_count = 0
        y = 0

        router_interface = FactoryRouterInterface(belts = [])

        for item in self.input_flow:            
            router_interface.belts.append(
                FactoryRouterBelt(
                    name = "Input flow - " + item.name,
                    item_type = item.name,
                    direction = FactoryRouterBelt.Direction.INGREDIENT,
                    pos = Vector(2 * len(router_interface.belts), 0),
                    throughput = 6, # TODO: Define throughput
                    proliferator = None, # TODO define proliferator
                )
            )
        
        for product in self.target_output_flow[::-1]:
            
            recipe = Recipe.select(product.name)

            # If the product is a raw material, skip it
            if not product.name in Recipe.recipes:
                continue
            
            # TODO: Define factory count
            factory_count = 5
            
            factory_block_interface = FactoryBlockInterface.generate_interface(
                recipe = recipe,
                factory_count = factory_count,
                proliferator = None
            )

            for product in recipe.output_items:
                router_interface.belts.append(
                    FactoryRouterBelt(
                        name = "Input flow - " + product,
                        item_type = product,
                        direction = FactoryRouterBelt.Direction.PRODUCT,
                        pos = Vector(2 * len(router_interface.belts), 0),
                        throughput = 6, # TODO: Define throughput
                        proliferator = None, # TODO define proliferator
                    )
                )
            self.factories.append(
                FactorySection(
                    pos = Vector(0, y),
                    factory_router_interface = router_interface,
                    factory_block_interfaces = factory_block_interface,
                    recipe = recipe,
                    factory_count = factory_count,
                    proliferator = None
                )
            )
            
            #if len(self.factories) > 1:
            #    self.factories[-2].connect_to_section(self.factories[-1])
            
            #output_count += self.factories[-1].product_count
            y += self.factories[-1].get_height()
        # Add the blueprint string to the widget
        blueprint = Blueprint()
        output_blueprint_string = blueprint.serialize(Building.buildings)
        self.blueprint.set_blueprint_string(output_blueprint_string)
        Building.buildings.clear()

if __name__ == "__main__":
    
    # Parse the arguments
    parser = argparse.ArgumentParser(
        prog = "Blueprint parser",
        description = "Apllication to parse blueprints for the game Dyson Sphere program"
    )
    parser.add_argument("--output_file", "--of", type = str, help = "Output file where to save the output to (if not defined, the output will be written to standard output)")
    args = parser.parse_args()

    app = QApplication(sys.argv)
    widget = GeneratorWidget()
    widget.setWindowTitle('Factory generator')
    widget.resize(700, 500)
    widget.show()
    sys.exit(app.exec())
    
    # Generate the factory
    factory = Factory()
    output_flow = [ItemFlow("PhotonCombiner", 1.0)]
    factory.set_tartget_output_flow(output_flow, debug = True)
    factory.generate_factories(debug = True)
    blueprint = Blueprint()
    output_blueprint_string = blueprint.serialize(Building.buildings)

    # Write parsed data
    if args.output_file == None:
        print(output_blueprint_string)
    else:
        with open(args.output_file, "w") as file:
            file.write(output_blueprint_string)