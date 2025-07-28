import sys
import networkx as nx
import logging

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QTabWidget, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt

from .factory_generator.gui_elements.output_flows import OutputFlows
from .factory_generator.gui_elements.input_flows import InputFlows
from .factory_generator.gui_elements.proliferator_production_option import ProliferatorProductionOption
from .factory_generator.gui_elements.blueprint_string_widget import BlueprintStringWidget
from .factory_generator.gui_elements.graph_plot import GraphPlotWidget
from .factory_generator.gui_elements.processes import Processes

from .factory_generator.production_graph.production_graph import ProductionGraph
from .factory_generator.factory_components.factory import Factory

VERSION = "0.1.0"

class GeneratorWidget(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initialize_production_graph()
        self.generate_gui_elements()
    
    def initialize_production_graph(self):
        self.production_graph = ProductionGraph()
    
    def generate_gui_elements(self):
        self.tabs = QTabWidget()
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)
        self.generate_factory_tab()
        self.generate_about_tab()
        self.setup_callbacks()
        self.post_setup()

    def generate_factory_tab(self):
        self.factory_tab = QWidget()
        self.factory_layout = QHBoxLayout()
        self.factory_tab.setLayout(self.factory_layout)
        self.tabs.addTab(self.factory_tab, "Factory")
        self.generate_factory_settings_layout(self.factory_layout)
        self.generate_factory_graph_layout(self.factory_layout)

    def generate_factory_settings_layout(self, layout):
        self.factory_settings_layout = QVBoxLayout()
        # Set minimum width policy for the settings layout's parent widget
        parent_widget = QWidget()
        parent_widget.setLayout(self.factory_settings_layout)
        parent_widget.setSizePolicy(parent_widget.sizePolicy().horizontalPolicy(), parent_widget.sizePolicy().verticalPolicy())
        parent_widget.setSizePolicy(QSizePolicy.Policy.Fixed, parent_widget.sizePolicy().verticalPolicy())
        parent_widget.setMinimumWidth(740)
        layout.addWidget(parent_widget)
        self.output_flows = OutputFlows()
        self.factory_settings_layout.addWidget(self.output_flows)
        self.insert_horizontal_line(self.factory_settings_layout)
        self.proliferator = ProliferatorProductionOption()
        self.factory_settings_layout.addWidget(self.proliferator)
        self.insert_horizontal_line(self.factory_settings_layout)
        #self.intermediate_flows = Processes()
        #self.factory_settings_layout.addWidget(self.intermediate_flows)
        #self.insert_horizontal_line(self.factory_settings_layout)
        self.input_flow_widget = InputFlows()
        self.factory_settings_layout.addWidget(self.input_flow_widget)
        self.insert_horizontal_line(self.factory_settings_layout)
        self.blueprint = BlueprintStringWidget()
        self.blueprint.set_callbacks(self.generate_blueprint)
        self.factory_settings_layout.addWidget(self.blueprint)
        self.insert_horizontal_line(self.factory_settings_layout)
        self.expandable_dummy_widget = QWidget()
        self.factory_settings_layout.addWidget(self.expandable_dummy_widget)
        # TODO: Add trash output settings
        
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
        
        github_label = QLabel('<a href="https://github.com/RasmusStagsted/dsp_bp_generator">GitHub: RasmusStagsted/dsp_bp_generator</a>')
        github_label.setOpenExternalLinks(True)
        github_label.setAlignment(Qt.AlignCenter)
        about_layout.addWidget(github_label)
        self.about_tab.setLayout(about_layout)

    def setup_callbacks(self):
        self.output_flows.set_callbacks(
            flow_created_callback = self.flow_created_callback,
            flow_deleted_callback = self.flow_deleted_callback,
            item_changed_callback = self.item_changed_callback,
            flow_rate_changed_callback = self.flow_rate_changed_callback,
            proliferator_changed_callback = self.proliferator_changed_callback,
            any_changed_callback = self.any_changed_callback
        )
        
    def flow_deleted_callback(self, output_flows, index):
        logging.info("Flow deleted callback")
        self.graph_plot_widget.reduce_flow(output_flows[index].get_item_flow())
        self.input_flow_widget.update(self.graph_plot_widget.graph)
    
    def flow_created_callback(self, output_flows, index):
        logging.info(f"Flow created callback {output_flows[index].item_combo.currentText()}")
        self.graph_plot_widget.increase_flow(output_flows[index].get_item_flow())
        self.input_flow_widget.update(self.graph_plot_widget.graph)
        
    def item_changed_callback(self, output_flows, index):
        old_item_flow = output_flows[index].get_old_item_flow()
        new_item_flow = output_flows[index].get_item_flow()
        logging.info(f"Item changed from {old_item_flow.name} to {new_item_flow.name}")
        self.graph_plot_widget.reduce_flow(old_item_flow)
        self.graph_plot_widget.increase_flow(new_item_flow)
        self.input_flow_widget.update(self.graph_plot_widget.graph)
        
    def flow_rate_changed_callback(self, output_flows, index):
        old_item_flow = output_flows[index].get_old_item_flow()
        new_item_flow = output_flows[index].get_item_flow()
        logging.info(f"Flow rate changed for {old_item_flow.name} from {old_item_flow.count_per_second} item/s to {new_item_flow.count_per_second} item/s")
        self.graph_plot_widget.reduce_flow(old_item_flow)
        self.graph_plot_widget.increase_flow(new_item_flow)
        self.input_flow_widget.update(self.graph_plot_widget.graph)
        
    def proliferator_changed_callback(self, output_flows, index):
        old_item_flow = output_flows[index].get_old_item_flow()
        new_item_flow = output_flows[index].get_item_flow()
        logging.info(f"Proliferator changed for {old_item_flow.name} from {old_item_flow.proliferator} to {new_item_flow.proliferator}")
        self.graph_plot_widget.reduce_flow(old_item_flow)
        self.graph_plot_widget.increase_flow(new_item_flow)
        self.input_flow_widget.update(self.graph_plot_widget.graph)

        output_flows = self.output_flows.output_flows
        proliferators = [output_flows[i].get_item_flow().proliferator for i in range(len(output_flows))]
        self.proliferator.update(proliferators)
        
    def any_changed_callback(self, output_flows):
        logging.info("Any changed callback")
        self.graph_plot_widget.graph.refresh()

    def generate_blueprint(self):
        factory = Factory()
        
        factory.generate(
            graph = self.graph_plot_widget.graph,
            input_sources = self.input_flow_widget.get_input_sources(),
            output_destinations = self.output_flows.get_output_destination(),
        )
        print(factory.generate_bp_string())

    def post_setup(self):
        self.output_flows.add_flow()

class AlignedColorFormatter(logging.Formatter):
    def format(self, record):
        # Compose and pad custom field
        record.loc = f"[{record.filename}:{record.lineno:3d}]"
        record.loc = f"{record.loc:<20}"  # Left-align to 20 characters

        record.asctime = self.formatTime(record, 'T%H:%M:%S.%f')

        # Add color if you like
        COLORS = {
            'DEBUG': '\033[36m',
            'INFO': '\033[32m',
            'WARNING': '\033[33m',
            'ERROR': '\033[31m',
            'CRITICAL': '\033[1;31m',
            'RESET': '\033[0m',
        }
        color = COLORS.get(record.levelname, COLORS['RESET'])
        reset = COLORS['RESET']

        return color + super().format(record) + reset
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='DSP Factory Blueprint Generator')
    parser.add_argument('--test', action='store_true', help='Run in test mode')
    parser.add_argument('--log_level', type=str, default='DEBUG', help='Set logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)')

    log_levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }

    handler = logging.StreamHandler()
    handler.setFormatter(AlignedColorFormatter('%(asctime)s, %(levelname)-8s %(loc)s %(message)s'))
    handler.setLevel(logging.DEBUG)
    log_level = log_levels[parser.parse_args().log_level.upper()]
    print(log_level)
    logging.basicConfig(handlers = [handler], level = log_level)
    print(f"Log level set to {parser.parse_args().log_level.upper()}")

    args = parser.parse_args()
    if args.test:
        sys.exit(0)
    app = QApplication(sys.argv)
    widget = GeneratorWidget()
    widget.setWindowTitle('Factory generator')
    widget.resize(1400, 800)
    widget.show()
    sys.exit(app.exec())