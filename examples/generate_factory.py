import sys
import math
import argparse
from dataclasses import dataclass

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, QPushButton, QLabel,
    QComboBox, QLineEdit, QTableWidget, QStyledItemDelegate, QTabWidget, QHeaderView, QFrame
)
from PySide6.QtGui import QDoubleValidator
from PySide6.QtCore import Qt

from dsp_bp_generator.utils import Yaw, Vector
from dsp_bp_generator.blueprint import Blueprint
from dsp_bp_generator.factory_generator import (
    Factory, ItemFlow, Process, FactorySection
)
from dsp_bp_generator.factory_generator.recipes import Recipe
from dsp_bp_generator.factory_generator.factory_router_interface import FactoryRouterInterface, FactoryRouterBelt
from dsp_bp_generator.factory_generator.factory_block_interface import FactoryBlockInterface, FactoryBlockBelt
from dsp_bp_generator.buildings import Building

from dsp_bp_generator.factory_generator.gui.output_flows import OutputFlows
from dsp_bp_generator.factory_generator.gui.input_flows import InputFlows
from dsp_bp_generator.factory_generator.gui.proliferator_production_option import ProliferatorProductionOption

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

        self.insert_horizontal_line()

        self.proliferator = ProliferatorProductionOption()
        self.factory_layout.addWidget(self.proliferator)

        self.insert_horizontal_line()

        self.input_flow_widget = InputFlows()
        self.factory_layout.addWidget(self.input_flow_widget)
        
        self.insert_horizontal_line()
        
        self.generator_button = QPushButton("Generate blueprint!")
        self.generator_button.clicked.connect(self.update_production_flows)
        self.factory_layout.addWidget(self.generator_button)
        
        self.insert_horizontal_line()

        self.factory_layout.addWidget(QLabel("Blueprint string:"))
        self.blueprint = BlueprintStringWidget()
        self.factory_layout.addWidget(self.blueprint)
        
        self.insert_horizontal_line()

        self.factory_tab.setLayout(self.factory_layout)
        self.tabs.addTab(self.factory_tab, "Output flows")

        # TODO: Add trash output info

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
        
        self.output_flows.set_proliferator_change_callback(self.proliferator.update)
        self.output_flows.set_any_update_callback(self.update_production_flows)
        
    def insert_horizontal_line(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        self.factory_layout.addWidget(line)

    def update(self):

        self.update_production_flows()

        #self.generate_factories()
        
        blueprint = Blueprint()
        #blueprint_string = blueprint.serialize(Building.buildings)
        #self.blueprint.blueprint.setText(blueprint_string)

    
    def update_process_graph(self):
        requirement_stack = self.output_flows.item_flows.copy()
        self.requirement_stack = [flow for flow in self.requirement_stack if flow.name != "None"]
        
        while len(self.requirement_stack) > 0:
            
            item_flow = self.requirement_stack.pop()
            print("Name:", item_flow.name)

            if item_flow.name in [flow.name for flow in self.item_flow_stack]:
                print("Old item flow")
                # Update flows and processes
            else:
                self.item_flow_stack.append(item_flow)
                process = Process(
                    name = item_flow.name,
                    recipe = Recipe.select(item_flow.name)
                )
                self.production_stack.append(process)
            
            # Add ingredients to stack
            proliferator = None
            
            for ingredient in process.get_needed_ingredients("None"): # TODO define proliferator
                self.requirement_stack.append(ingredient)

    def update_production_flows(self, proliferator = {}):
        self.requirement_stack = self.output_flows.item_flows.copy()
        self.requirement_stack = [flow for flow in self.requirement_stack if flow.name != "None"]
        self.production_stack = []
        self.item_flow_stack = []

        while len(self.requirement_stack) > 0:
            
            item_flow = self.requirement_stack.pop()
            print("Name:", item_flow.name)

            if item_flow.name in [flow.name for flow in self.item_flow_stack]:
                print("Old item flow")
                # Update flows and processes
            else:
                self.item_flow_stack.append(item_flow)
                process = Process(
                    name = item_flow.name,
                    recipe = Recipe.select(item_flow.name)
                )
                self.production_stack.append(process)
            
            # Add ingredients to stack
            proliferator = None
            
            for ingredient in process.get_needed_ingredients("None"): # TODO define proliferator
                self.requirement_stack.append(ingredient)

        self.target_output_flow = self.item_flow_stack
        self.input_flow = []
        for flow in self.target_output_flow:
            if not flow.name in Recipe.recipes:
                self.input_flow.append(flow)
                self.target_output_flow.remove(flow)

        self.item_flow_stack = self.item_flow_stack[::-1]
        
        self.input_flow_widget.update(self.input_flow)
        
        #self.generate_factories()

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
    widget.resize(700, 800)
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