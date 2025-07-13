import networkx as nx
import logging
from .connection import Connection

from ..recipes import Recipe

from .graphical_graph import GraphicalGraph
from ..proliferator import Proliferator

class ProductionGraph(GraphicalGraph):

    def __init__(self):
        super().__init__()
    
    def change_required_flow_rate(self, flow_name, items_per_second, proliferator_name):
        if not self.node_name_exists(flow_name + proliferator_name + "Flow"):
            logging.info("Node does not exist in the graph, adding node: " + flow_name + proliferator_name)
            self.add_flow(flow_name, proliferator_name)
        flow = self.graph.nodes.get(flow_name + proliferator_name + "Flow")
        if not "required_items_per_second" in flow:
            flow["required_items_per_second"] = 0
        flow["required_items_per_second"] += items_per_second
        self.change_flow_rate(flow_name, items_per_second, proliferator_name)
    
    def change_flow_rate(self, flow_name, items_per_second, proliferator_name):
        if not self.node_name_exists(flow_name + proliferator_name + "Flow"):
            logging.info("Node does not exist in the graph, adding node: " + flow_name + proliferator_name)
            self.add_flow(flow_name, proliferator_name)
        flow = self.graph.nodes.get(flow_name + proliferator_name + "Flow")
        old_flow_rate = flow["items_per_second"]
        new_flow_rate = old_flow_rate + items_per_second
        logging.info("Changing flow rate for " + flow_name + proliferator_name + " from " + str(old_flow_rate) + " to " + str(new_flow_rate))
        flow["items_per_second"] += items_per_second
        edges_to_edit = []
        processes_to_edit = []
        for node_name in self.graph.predecessors(flow_name + proliferator_name + "Flow"):
            process_name = self.graph.nodes.get(node_name)["name"]
            processes_to_edit.append({"name": process_name, "processes_per_second": items_per_second, "proliferator_name": proliferator_name})
            edge_source = process_name + proliferator_name + "Process"
            edge_destination = flow_name + proliferator_name + "Flow"
            edges_to_edit.append({"source": edge_source, "destination": edge_destination, "items_per_second_diff": items_per_second})
        for edge in edges_to_edit:
            self.change_edge_flow_rate(edge["source"], edge["destination"], edge["items_per_second_diff"])
        for process in processes_to_edit:
            self.change_process_rate(process["name"], process["processes_per_second"], process["proliferator_name"])
        if flow["items_per_second"] <= 0:
            logging.info(f"Flow {flow_name + proliferator_name} has a flow rate of zero, removing flow.")
            self.remove_flow(flow_name, proliferator_name)
    
    def change_process_rate(self, process_name, processes_per_second, proliferator_name):
        if not self.node_name_exists(process_name + proliferator_name + "Process"):
            logging.error(f"Process {process_name + proliferator_name} does not exist in the production graph.")
            logging.debug(self.graph.nodes.keys())
            return
        process = self.graph.nodes.get(process_name + proliferator_name + "Process")
        old_process_rate = process["processes_per_second"]
        new_process_rate = old_process_rate + processes_per_second
        logging.info("Changing process rate for: " + process_name + proliferator_name + " from " + str(old_process_rate) + " to " + str(new_process_rate))
        productivity = Proliferator.get_productivity(proliferator_name)
        output_item_count_per_process = process["selected_recipe"].output_items[process_name]
        processes_per_second_diff = processes_per_second / output_item_count_per_process / productivity
        process["processes_per_second"] += processes_per_second_diff
        edges_to_edit = []
        flows_to_edit = []
        for node_name in self.graph.predecessors(process_name + proliferator_name + "Process"):
            flow_name = self.graph.nodes.get(node_name)["name"]
            input_item_count = process["selected_recipe"].input_items[flow_name]
            items_per_second = processes_per_second_diff * input_item_count
            flows_to_edit.append({"name": flow_name, "items_per_second": items_per_second, "proliferator_name": proliferator_name})
            edge_source = flow_name + proliferator_name + "Flow"
            edge_destination = process_name + proliferator_name + "Process"
            edges_to_edit.append({"source": edge_source, "destination": edge_destination, "items_per_second_diff": items_per_second})
        for edge in edges_to_edit:            
            self.change_edge_flow_rate(edge["source"], edge["destination"], edge["items_per_second_diff"])
        for flow in flows_to_edit:
            self.change_flow_rate(flow["name"], flow["items_per_second"], flow["proliferator_name"])
        if process["processes_per_second"] <= 0:
            logging.info(f"Process {process_name + proliferator_name} has a process rate of zero, removing process.")
            self.remove_process(process_name, proliferator_name)
    
    def change_edge_flow_rate(self, source_name, destination_name, items_per_second_diff):
        if not self.node_name_exists(source_name):
            logging.error(f"Source node {source_name} does not exist in the graph.")
            return
        if not self.node_name_exists(destination_name):
            logging.error(f"Destination node {destination_name} does not exist in the graph.")
            return
        edge = self.graph.get_edge_data(source_name, destination_name)
        old_items_per_second = edge["items_per_second"]
        new_items_per_second = old_items_per_second + items_per_second_diff
        logging.info(f"Changing edge flow rate from {source_name} to {destination_name} from {old_items_per_second} to {new_items_per_second}")
        if edge is None:
            logging.error(f"No edge exists between {source_name} and {destination_name}.")
            return
        edge["items_per_second"] = new_items_per_second
        edge["color"] = self.generate_edge_color(edge["items_per_second"])
        edge["label"] = str(round(new_items_per_second, 2))
        if edge["items_per_second"] <= 0:
            logging.info(f"Edge from {source_name} to {destination_name} has a flow rate of zero, removing edge.")
            self.graph.remove_edge(source_name, destination_name)
    
    def add_flow(self, flow_name, proliferator_name):
        logging.info("Adding flow to the graph: " + flow_name + proliferator_name)
        if self.node_name_exists(flow_name + proliferator_name + "Flow"):
            logging.error("Flow already exists in the graph: " + flow_name + proliferator_name)
            logging.debug(self.graph.nodes.keys())
            return
        node_id = flow_name + proliferator_name + "Flow"
        label = self.generate_label(flow_name)
        self.graph.add_node(
            node_for_adding = node_id,
            color = self.generate_node_color(proliferator_name, "flow"),
            name = flow_name,
            items_per_second = 0,
            proliferator = Proliferator.get_proliferator(proliferator_name),
            label = label
        )
        if not Recipe.has_recipe(flow_name):
            if not (flow_name in ["IronOre", "CopperOre", "Stone", "Coal", "Water", "CrudeOil", "TitaniumOre", "UnipolarMagnet"]):
                logging.warning(f"No recipe found for the flow ({flow_name}), cannot add process.")
            logging.info("Adding raw item to the graph: " + flow_name + proliferator_name)
            return
        recipes = Recipe.get_recipes_for_output_item(flow_name)
        if len(recipes) == 0:
            logging.warning(f"No recipes found for output item {flow_name}. Cannot create process.")
            return
        process_name = flow_name
        if not self.node_name_exists(process_name + proliferator_name + "Process"):
            self.add_process(process_name, recipes, recipes[0], proliferator_name)
        self.connect_process_to_flow(process_name, flow_name, proliferator_name, 0)

    def add_process(self, process_name, recipes, recipe, proliferator_name):
        logging.info("Adding process to the graph: " + process_name + proliferator_name)
        if self.node_name_exists(process_name + proliferator_name + "Process"):
            logging.error("Process already exists in the graph: " + process_name + proliferator_name)
            return
        name = process_name + proliferator_name + "Process"
        label = self.generate_label(process_name)
        self.graph.add_node(
            node_for_adding = name,
            color = self.generate_node_color(proliferator_name, "process"),
            name = process_name,
            recipes = recipes,
            selected_recipe = recipe,
            processes_per_second = 0,
            proliferator = Proliferator.get_proliferator(proliferator_name),
            label = label
        )
        for flow_name in recipe.input_items.keys():
            if not self.node_name_exists(flow_name + proliferator_name + "Flow"):
                self.add_flow(flow_name, proliferator_name)
            self.connect_flow_to_process(flow_name, process_name, proliferator_name, 0)
                    
    def remove_flow(self, flow_name, proliferator_name):
        logging.info("Removing flow from the graph: " + flow_name + proliferator_name)
        if not self.node_name_exists(flow_name + proliferator_name + "Flow"):
            logging.error("Flow does not exist in the graph, cannot remove: " + flow_name + proliferator_name + " from " + str(self.graph.nodes.keys()))
            return
        flow_rate = self.graph.nodes.get(flow_name + proliferator_name + "Flow")["items_per_second"]
        if flow_rate > 0.001:
            logging.error("Flow still has a flow-rate greater than zero, cannot remove: " + flow_name + proliferator_name + ": " + str(flow_rate))
            return
        for node_name in self.graph.predecessors(flow_name + proliferator_name + "Flow"):
            process_name = self.graph.nodes.get(node_name)["name"]
            process = self.graph.nodes.get(process_name + proliferator_name + "Process")
            if process["processes_per_second"] != 0:
                logging.error(f"Process {process_name} is still having a flow-rate to flow {flow_name + proliferator_name}, cannot remove process.")
            else:
                self.remove_process(process_name, proliferator_name)
                self.disconnect_process_from_flow(process_name, flow_name, proliferator_name)
        self.graph.remove_node(flow_name + proliferator_name + "Flow")
        
    def remove_process(self, process_name, proliferator_name):
        logging.info("Removing process from the graph: " + process_name + proliferator_name)
        if not self.node_name_exists(process_name + proliferator_name + "Process"):
            logging.error("Process does not exist in the graph, cannot remove: " + process_name + proliferator_name + " from " + str(self.graph.nodes.keys()))
            return
        flow_rate = self.graph.nodes.get(process_name + proliferator_name + "Process")["processes_per_second"]
        if flow_rate > 0.001:
            logging.error("Process still has a flow-rate greater than zero, cannot remove: " + process_name + proliferator_name + ": " + str(flow_rate))
            return
        for flow_name in self.graph.predecessors(process_name + proliferator_name + "Process"):
            flow = self.graph.nodes.get(flow_name)
            if flow["items_per_second"] != 0:
                logging.error(f"Flow {flow_name} is still having a flow-rate to process {process_name + proliferator_name}, cannot remove process.")
            else:
                self.disconnect_flow_from_process(flow_name, process_name, proliferator_name)
                self.remove_flow(flow_name, proliferator_name)
        self.graph.remove_node(process_name + proliferator_name + "Process")
    
    def connect_flow_to_process(self, flow_name, process_name, proliferator_name, items_per_second):
        logging.info(f"Connecting {flow_name}(flow) to {process_name}(process), proliferator_name: {proliferator_name}")
        if not self.node_name_exists(flow_name + proliferator_name + "Flow"):
            logging.error("Flow does not exist in the graph, cannot connect: " + flow_name + proliferator_name)
            return
        if not self.node_name_exists(process_name + proliferator_name + "Process"):
            logging.error("Process does not exist in the graph, cannot connect: " + process_name + proliferator_name)
            return
        self.graph.add_edge(
            flow_name + proliferator_name + "Flow",
            process_name + proliferator_name + "Process",
            destination = self.graph.nodes[process_name + proliferator_name + "Process"],
            source = self.graph.nodes[flow_name + proliferator_name + "Flow"],
            name = f"{flow_name}(flow) to {process_name}(process), proliferator_name: {proliferator_name}",
            color = self.generate_edge_color(items_per_second),
            items_per_second = items_per_second,
            label = str(round(items_per_second, 2)),
        )
    
    def connect_process_to_flow(self, process_name, flow_name, proliferator_name, items_per_second):
        logging.info(f"Connecting {process_name}(process) to {flow_name}(flow), proliferator_name: {proliferator_name}")
        if not self.node_name_exists(flow_name + proliferator_name + "Flow"):
            logging.error("Flow does not exist in the graph, cannot connect: " + flow_name + proliferator_name)
            return
        if not self.node_name_exists(process_name + proliferator_name + "Process"):
            logging.error("Process does not exist in the graph, cannot connect: " + process_name + proliferator_name)
            return
        self.graph.add_edge(
            process_name + proliferator_name + "Process",
            flow_name + proliferator_name + "Flow",
            source = self.graph.nodes[process_name + proliferator_name + "Process"],
            destination = self.graph.nodes[flow_name + proliferator_name + "Flow"],
            name = f"{process_name}(process) to {flow_name}(flow), proliferator_name: {proliferator_name}",
            color = self.generate_edge_color(items_per_second),
            items_per_second = items_per_second,
            label = str(round(items_per_second, 2)),
        )
        
    def disconnect_flow_from_process(self, flow_name, process_name, proliferator_name):
        logging.info(f"Disconnecting {flow_name}(flow) from {process_name}(process), proliferator_name: {proliferator_name}")
        if not self.node_name_exists(flow_name + proliferator_name + "Flow"):
            logging.error("Flow does not exist in the graph, cannot disconnect: " + flow_name + proliferator_name)
            return
        if not self.node_name_exists(process_name + proliferator_name + "Process"):
            logging.error("Process does not exist in the graph, cannot disconnect: " + process_name + proliferator_name)
            return
        self.graph.remove_edge(
            flow_name + proliferator_name + "Flow",
            process_name + proliferator_name + "Process"
        )
    
    def disconnect_process_from_flow(self, process_name, flow_name, proliferator_name):
        logging.info(f"Disconnecting {process_name}(process) from {flow_name}(flow), proliferator_name: {proliferator_name}")
        if not self.node_name_exists(flow_name + proliferator_name + "Flow"):
            logging.error("Flow does not exist in the graph, cannot disconnect: " + flow_name + proliferator_name)
            return
        if not self.node_name_exists(process_name + proliferator_name + "Process"):
            logging.error("Process does not exist in the graph, cannot disconnect: " + process_name + proliferator_name)
            return
        self.graph.remove_edge(
            process_name + proliferator_name + "Process",
            flow_name + proliferator_name + "Flow"
        )
    
    def node_name_exists(self, node_name):
        return node_name in self.graph.nodes.keys()
    
    def generate_edge_color(self, items_per_second):
        if items_per_second <= 6:
            return "#f0c33c"
        elif items_per_second <= 12:
            return "#1ed14b"
        elif items_per_second <= 30:
            return "#72aee6"
        else:
            return "#ff0000"

    def generate_node_color(self, proliferator, node_type):
        if node_type == "flow":
            if proliferator == "No-proliferator":
                return "#a7aaad"
            elif proliferator == "MK.I":
                return "#f0c33c"
            elif proliferator == "MK.II":
                return "#1ed14b"
            elif proliferator == "MK.III":
                return "#72aee6"
        elif node_type == "process":
            if proliferator == "No-proliferator":
                return "#646970"
            elif proliferator == "MK.I":
                return "#996b00"
            elif proliferator == "MK.II":
                return "#008a20"
            elif proliferator == "MK.III":
                return "#2271b1"
        return "#ff0000"
    
    def get_recipe(self, item_name):
        if not Recipe.has_recipe(item_name):
            logging.error(f"No recipe found for item {item_name}.")
            return None
        recipes = Recipe.get_recipes_for_output_item(item_name)
        if len(recipes) == 0:
            logging.error(f"No recipes found for output item {item_name}.")
            return None
        return recipes[0]

if __name__ == "__main__":
    from dsp_bp_generator.factory_generator.production_graph.process import Process
    from dsp_bp_generator.factory_generator.production_graph.item_flow import ItemFlow
    from dsp_bp_generator.factory_generator.recipes import Recipe
    from dsp_bp_generator.factory_generator.proliferator import ProliferatorNone, ProliferatorMKI, ProliferatorMKII, ProliferatorMKIII

    production_graph = ProductionGraph()

    iron_ingot_flow = ItemFlow(
        name = "Magnet",
        proliferator = ProliferatorNone
    )
    
    iron_ingot_flow2 = ItemFlow(
        name = "MagneticCoil",
        proliferator = ProliferatorNone
    )
    
    production_graph.add_output_item_flow(iron_ingot_flow, 1.0)
    print(production_graph)
    production_graph.add_output_item_flow(iron_ingot_flow2, 1.0)
    #production_graph.reduce_output_item_flow(iron_ingot_flow2)
    #production_graph.processes["Magnet"].set_proliferator("MK.I")
    print(production_graph)
