import argparse
from dsp_bp_generator.utils import Yaw, Vector
from dsp_bp_generator.blueprint import Blueprint
from dsp_bp_generator.factory_generator import Factory, ItemFlow, recipes
from dsp_bp_generator.buildings import Building
import math
import argparse
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, QPushButton, QLabel, QComboBox, QLineEdit
from PyQt5.QtGui import QDoubleValidator

from dsp_bp_generator.factory_generator import FactorySection

from dsp_bp_generator.factory_generator import Recipe

import sys
import pyperclip

class OutputFlowWidget(QWidget):
    
    def __init__(self, delete_callback = None):
        super().__init__()
        
        self.layout = QHBoxLayout()
        self.item = QComboBox()
        self.item.addItems(Recipe.recipes.keys())
        self.flow_rate = QLineEdit()
        self.flow_rate.setText("1.0")
        self.double_validator = QDoubleValidator(0.0, 1000.0, 3)
        self.flow_rate.setValidator(self.double_validator)
        if delete_callback != None:
            self.delete_button = QPushButton("Delete flow")
            self.delete_button.clicked.connect(lambda: delete_callback(self))
        
        self.layout.addWidget(self.item)
        self.layout.addWidget(self.flow_rate)
        if delete_callback != None:
            self.layout.addWidget(self.delete_button)
        
        self.setLayout(self.layout)

class OutputFlows(QWidget):
    def __init__(self):
        super().__init__()
        
        self.layout = QVBoxLayout()
        
        self.output_flows_label = QLabel('Select target output flows:')
        self.layout.addWidget(self.output_flows_label)
        
        self.flow_layout = QVBoxLayout()
        self.flow = []
        self.flow.append(OutputFlowWidget())
        self.flow_layout.addWidget(self.flow[-1])
        self.layout.addLayout(self.flow_layout)

        self.add_flow_button = QPushButton("Add output flow!")
        self.add_flow_button.clicked.connect(self.add_flow)
        self.layout.addWidget(self.add_flow_button)   
        
        self.setLayout(self.layout)

    def add_flow(self):
        self.flow.append(OutputFlowWidget(self.remove_flow))
        self.flow_layout.addWidget(self.flow[-1])

    def remove_flow(self, flow):
        if len(self.flow) > 1:
            flow.hide()
            self.flow_layout.removeWidget(flow)            
            self.flow.remove(flow)

class ProlifiratorWidget(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.layout = QVBoxLayout()
        
        
        self.enable_layout = QHBoxLayout()
        
        self.enable_prolifirator_text = QLabel("Enable Prolifirator")
        self.enable_layout.addWidget(self.enable_prolifirator_text)
        
        self.enable_prolifirator = QCheckBox()
        self.enable_prolifirator.stateChanged.connect(self.enable_event)
        self.enable_layout.addWidget(self.enable_prolifirator)
        
        self.layout.addLayout(self.enable_layout)


        self.prolifirator_selector_layout = QHBoxLayout()

        self.prolifirator_selector_label = QLabel("Select prolifirator:")
        self.prolifirator_selector_layout.addWidget(self.prolifirator_selector_label)

        self.prolifirator_selector = QComboBox()
        self.prolifirator_selector.addItems(["Prolifirator MK. I", "Prolifirator MK. II", "Prolifirator MK. III"])
        
        self.prolifirator_selector_layout.addWidget(self.prolifirator_selector)
        
        self.layout.addLayout(self.prolifirator_selector_layout)


        self.production_mode_layout = QHBoxLayout()

        self.production_mode_label = QLabel("Select production mode:")
        self.production_mode_layout.addWidget(self.production_mode_label)

        self.production_mode = QComboBox()
        self.production_mode.addItems(["External production", "Internal production"])
        self.production_mode.setCurrentText("External production")
        self.production_mode_layout.addWidget(self.production_mode)

        self.layout.addLayout(self.production_mode_layout)

        self.hide()
        self.setLayout(self.layout)

    def show(self):
        self.prolifirator_selector.show()
        self.production_mode.show()
        self.prolifirator_selector_label.show()
        self.production_mode_label.show()
        
    def hide(self):
        self.prolifirator_selector.hide()
        self.production_mode.hide()
        self.prolifirator_selector_label.hide()
        self.production_mode_label.hide()
        
    def enable_event(self, state):
        if state == 2: # Checked
            self.show()
        else:
            self.hide()

class RecipiSelectorWidget(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.layout = QVBoxLayout()

        self.setLayout(self.layout)

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
        pyperclip.copy(self.blueprint.text())

    def set_blueprint_string(self, bp_string):
        self.blueprint.setText(bp_string)

class GeneratorWidget(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.layout = QVBoxLayout()
        
        self.output_flows = OutputFlows()
        self.layout.addWidget(self.output_flows)
        
        self.prolifirator = ProlifiratorWidget()
        self.layout.addWidget(self.prolifirator)
        
        self.recipiSelector = RecipiSelectorWidget()
        self.layout.addWidget(self.recipiSelector)
        
        self.generator_button = QPushButton("Generate!")
        self.generator_button.clicked.connect(self.update_production_flows)
        self.layout.addWidget(self.generator_button)
        
        self.blueprint = BlueprintStringWidget()
        self.layout.addWidget(self.blueprint)

        self.setLayout(self.layout)

        self.update()

    def update(self):

        self.update_production_flows()

        self.generate_factories()
        
        blueprint = Blueprint()
        #blueprint_string = blueprint.serialize(Building.buildings)
        #self.blueprint.blueprint.setText(blueprint_string)

    def update_production_flows(self):
        requirement_stack = []
        production_stack = []

        for flow in self.output_flows.flow:
            item = flow.item.currentText()
            flow_rate = float(flow.flow_rate.text())
            requirement_stack.append(
                ItemFlow(item, flow_rate)
            )

        print(requirement_stack)

        while len(requirement_stack) > 0:
            
            item = requirement_stack.pop()
            
            # Add ingredients to stack
            for ingredient in item.get_needed_ingredients(self.prolifirator.prolifirator_selector.currentText()):
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

        self.target_output_flow = production_stack[::-1] # Reverse list
        self.input_flow = []
        for flow in self.target_output_flow:
            if Recipe.recipes[flow.name] == None:
                self.input_flow.append(flow)
                self.target_output_flow.remove(flow)

        #self.blueprint.blueprint.setText()

    def generate_factories(self, debug = True):
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
        
        for product in self.target_output_flow:
            
            recipe = Recipe.select(product.name)

            # If the product is a raw material, skip it
            if Recipe.recipes[product.name] == None:
                continue
            self.factories.append(
                FactorySection(
                    pos = Vector(0, y),
                    input_count = input_count,
                    output_count = output_count,
                    main_belts = self.main_belts,
                    product = product,
                    recipe = recipe
                )
            )
            
            if len(self.factories) > 1:
                self.factories[-2].connect_to_section(self.factories[-1])
            
            output_count += self.factories[-1].product_count
            y += self.factories[-1].height

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
    widget.setWindowTitle('Simple Qt Widget')
    widget.resize(300, 200)
    widget.show()
    sys.exit(app.exec_())

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