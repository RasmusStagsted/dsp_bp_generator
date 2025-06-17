import sys
import networkx as nx

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QTabWidget, QFrame
)
from PySide6.QtCore import Qt
from .factory_generator import Process
from .factory_generator.recipes import Recipe

from .factory_generator.gui_elements.output_flows import OutputFlows
from .factory_generator.gui_elements.input_flows import InputFlows
from .factory_generator.gui_elements.proliferator_production_option import ProliferatorProductionOption
from .factory_generator.gui_elements.blueprint_string_widget import BlueprintStringWidget
from .factory_generator.gui_elements.graph_plot import GraphPlotWidget

from .factory_generator.production_graph.production_graph import ProductionGraph
from .factory_generator.production_graph.item_flow import ItemFlow

VERSION = "0.1.0"

class GeneratorWidget(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initialize_production_graph()
        self.generate_gui_elements()
    
    def initialize_production_graph(self):
        self.production_graph = ProductionGraph()
    
    def generate_gui_elements(self):
        # Setup layout
        self.tabs = QTabWidget()
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)
        # Add widgets
        self.generate_factory_tab()
        self.generate_about_tab()
        # Setup callbacks
        self.setup_callbacks()
        # Post setup
        self.post_setup()
        # Setup the production graph
        self.update()

    def generate_factory_tab(self):
        # Setup layout
        self.factory_tab = QWidget()
        self.factory_layout = QHBoxLayout()
        self.factory_tab.setLayout(self.factory_layout)
        self.tabs.addTab(self.factory_tab, "Factory")
        # Add widgets
        self.generate_factory_settings_layout(self.factory_layout)
        self.generate_factory_graph_layout(self.factory_layout)

    def generate_factory_settings_layout(self, layout):
        # Setup layout
        self.factory_settings_layout = QVBoxLayout()
        layout.addLayout(self.factory_settings_layout)
        # Add widgets
        self.output_flows = OutputFlows()
        self.factory_settings_layout.addWidget(self.output_flows)
        self.insert_horizontal_line(self.factory_settings_layout)
        self.proliferator = ProliferatorProductionOption()
        self.factory_settings_layout.addWidget(self.proliferator)
        self.insert_horizontal_line(self.factory_settings_layout)
        self.input_flow_widget = InputFlows()
        self.factory_settings_layout.addWidget(self.input_flow_widget)
        self.insert_horizontal_line(self.factory_settings_layout)
        self.blueprint = BlueprintStringWidget()
        self.factory_settings_layout.addWidget(self.blueprint)
        self.insert_horizontal_line(self.factory_settings_layout)

        # TODO: Add trash output info

        # TODO: Add Graph
        #https://doc.qt.io/qtforpython-6/examples/example_external_networkx.html
        
    def insert_horizontal_line(self, layout):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)
    
    def generate_factory_graph_layout(self, layout):
        self.factory_graph_layout = QVBoxLayout()
        layout.addLayout(self.factory_graph_layout)
        self.graph_plot_widget = GraphPlotWidget()
        self.factory_graph_layout.addWidget(self.graph_plot_widget)
    
    def generate_about_tab(self):
        self.about_tab = QWidget()
        about_layout = QVBoxLayout()
        self.tabs.addTab(self.about_tab, "About")
        about_label = QLabel(f"Dyson Sphere Program Factory Blueprint Generator\nVersion {VERSION}\nBy Stagsted")
        about_label.setAlignment(Qt.AlignCenter)
        about_layout.addWidget(about_label)
        
        # Add clickable GitHub link
        github_label = QLabel('<a href="https://github.com/RasmusStagsted/dsp_bp_generator">GitHub: RasmusStagsted/dsp_bp_generator</a>')
        github_label.setOpenExternalLinks(True)
        github_label.setAlignment(Qt.AlignCenter)
        about_layout.addWidget(github_label)
        self.about_tab.setLayout(about_layout)

    def setup_callbacks(self):
        self.output_flows.set_callbacks(
            flow_created_callback = self.flow_created_callback,
            #flow_deleted_callback = self.update,
            item_changed_callback = self.item_changed_callback,
            #flow_rate_changed_callback = self.update,
            proliferator_changed_callback = self.proliferator_changed_callback,
            any_changed_callback = self.any_changed_callback
        )
        
    def flow_created_callback(self, item, flow_rate, proliferator, index):
        self.production_graph.add_output_item_flow(
            ItemFlow(
                item[index],
                flow_rate[index],
                proliferator[index]
            )
        )
        self.graph_plot_widget.add_node(item[index].currentText())
    
    def flow_deleted_callback(self, item, flow_rate, proliferator, index):
        #self.production_graph.remove_output_item_flow()
        self.graph_plot_widget.graph.remove_node(item[index].currentText())
    
    def item_changed_callback(self, item, flow_rate, proliferator, index):
        old_item = self.output_flows.last_item_text[index]
        new_item = item[index].currentText()
        print(f"Item changed from {old_item} to {new_item}")
        
        #self.production_graph.remove_output_item_flow()
        self.graph_plot_widget.remove_node(old_item)
        
        self.production_graph.add_output_item_flow(
            ItemFlow(
                item[index],
                flow_rate[index],
                proliferator[index]
            )
        )
        self.graph_plot_widget.add_node(new_item)
        self.output_flows.last_item_text[index] = new_item
        
    def proliferator_changed_callback(self, item, flow_rate, proliferator, index):
        self.proliferator.update(proliferator, index)
        
    def any_changed_callback(self):
        self.graph_plot_widget.refresh()

    def post_setup(self):
        self.output_flows.add_flow()

    def update(self):

        pass
        #self.update_process_graph()
        #self.plot_process_graph()

        #self.generate_factories()
        
        #blueprint = Blueprint()
        #blueprint_string = blueprint.serialize(Building.buildings)
        #self.blueprint.blueprint.setText(blueprint_string)

    """

    def plot_process_graph(self):
        print("Plot process graph")
        edges = []
        nodes = []
        for process in self.production_stack:
            nodes.append(process.name)
        for process in self.production_stack:
            recipe = Recipe.select(process.name)
            #for recipe_input in recipe.input_items:
        
        self.graph.add_edges_from([("11", "2"), ("2", "10"), ("10", "4")])   
        self.view = GraphView(self.graph)
        self.choice_combo = QComboBox()
        self.choice_combo.addItems(self.view.get_nx_layouts())
        v_layout = QVBoxLayout()
        v_layout.addWidget(self.choice_combo)
        v_layout.addWidget(self.view)
        self.choice_combo.currentTextChanged.connect(self.view.set_nx_layout)

    """
    """

    def update_process_graph(self):
        print("Update process graph")
        self.item_flow_stack = []
        self.requirement_stack = []
        #for flow in self.output_flows.item_flows:
        #    if flow.name != "None":
        #        self.requirement_stack.append(copy.deepcopy(flow))
        
        self.production_stack = []
        while len(self.requirement_stack) > 0:
            
            item_flow = self.requirement_stack.pop()
            print("Name:", item_flow.name)

            self.item_flow_stack.append(item_flow)
            process = Process(
                name = item_flow.name,
                recipe = Recipe.select(item_flow.name)
            )
            self.production_stack.append(process)
            
            # Add ingredients to stack
            proliferator = None
            
            #for ingredient in process.get_needed_ingredients("None"): # TODO define proliferator
            #    self.requirement_stack.append(ingredient)
    """
    """        

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
    """
    """
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
    """

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='DSP Factory Blueprint Generator')
    parser.add_argument('--test', action='store_true', help='Run in test mode')
    args = parser.parse_args()
    if args.test:
        sys.exit(0)
    app = QApplication(sys.argv)
    widget = GeneratorWidget()
    widget.setWindowTitle('Factory generator')
    widget.resize(1000, 800)
    widget.show()
    sys.exit(app.exec())