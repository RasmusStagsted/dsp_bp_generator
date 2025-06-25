import networkx as nx
import logging
from .connection import Connection

from ..recipes import Recipe

from .graphical_graph import GraphicalGraph
from .process import Process
from ..proliferator import Proliferator

class ProductionGraph(GraphicalGraph):

    def __init__(self):
        super().__init__()
    
    def increase_flow(self, flow_name, count_per_second, proliferator):
        if not self.node_name_exists(flow_name + proliferator + "Flow"):
            logging.info("Node does not exist in the graph, adding node: " + flow_name + proliferator)
            self.add_flow(flow_name, proliferator)
        logging.info("Increasing flow for node: " + flow_name + proliferator)
        logging.error("Not implemented yet, need to handle flow increase logic.")
        # TODO 
        
    def increase_process(self, process_name, count_per_second, proliferator):
        if not self.node_name_exists(process_name + proliferator + "Process"):
            logging.error(f"Process {process_name + proliferator} does not exist in the production graph.")
            logging.debug(self.graph.nodes.keys())
            return
        logging.error("Not implemented yet, need to handle process increase logic.")
        # TODO
    
    def decrease_flow(self, flow_name, count_per_second, proliferator):
        if not self.node_name_exists(flow_name + proliferator + "Flow"):
            logging.error(f"Flow {flow_name + proliferator} does not exist in the production graph.")
            logging.debug(self.graph.nodes.keys())
            return
        logging.info("Decreasing flow: " + flow_name + proliferator)
        flow = self.graph.nodes.get(flow_name + proliferator + "Flow")
        flow["count_per_second"] -= count_per_second
        if flow["count_per_second"] < count_per_second:
            self.remove_flow(flow_name, proliferator)
        logging.error("Not implemented yet, need to handle flow decrease logic.")
        # TODO Decrease connected processes
        
    def decrease_process(self, process_name, count_per_second, proliferator):
        if not self.node_name_exists(process_name + proliferator + "Process"):
            logging.error(f"Process {process_name + proliferator} does not exist in the production graph.")
            logging.debug(self.graph.nodes.keys())
            return
        logging.error("Not implemented yet, need to handle process decrease logic.")
        # TODO
    
    def add_flow(self, flow_name, proliferator):
        logging.info("Adding flow to the graph: " + flow_name + proliferator)
        if self.node_name_exists(flow_name + proliferator + "Flow"):
            logging.error("Flow already exists in the graph: " + flow_name + proliferator)
            logging.debug(self.graph.nodes.keys())
            return
        node_id = flow_name + proliferator + "Flow"
        label = self.generate_label(flow_name + proliferator)
        self.graph.add_node(
            node_for_adding = node_id,
            color = "#797979",
            name = flow_name,
            count_per_second = 0,
            proliferator = proliferator,
            label = label
        )
        if not Recipe.has_recipe(flow_name):
            logging.warning("No recipe found for the flow, cannot add process.")
            logging.info("Adding raw item to the graph: " + flow_name + proliferator)
            return
        recipes = Recipe.get_recipes_for_output_item(flow_name)
        if len(recipes) == 0:
            logging.warning(f"No recipes found for output item {flow_name}. Cannot create process.")
            return
        recipes = recipes[0]            
        self.add_process(recipes, proliferator)
        self.connect_process_to_flow(recipes.name, flow_name, proliferator, 0)

    def add_process(self, recipe, proliferator):
        process_name = recipe.name
        logging.info("Adding process to the graph: " + process_name + proliferator)
        if self.node_name_exists(process_name + proliferator + "Process"):
            logging.error("Process already exists in the graph: " + process_name + proliferator)
            return
        name = process_name + proliferator + "Process"
        label = self.generate_label(process_name + proliferator)
        self.graph.add_node(
            node_for_adding = name,
            color = "#2F44FF",
            name = process_name,
            recipe = recipe,
            process_count_per_sec = 0,
            proliferator = proliferator,
            label = label
        )
        for flow_name in recipe.input_items.keys():
            if not self.node_name_exists(flow_name + proliferator + "Flow"):
                self.add_flow(flow_name, proliferator)
            self.connect_flow_to_process(flow_name, process_name, proliferator, 0)
                    
    def remove_flow(self, flow_name, proliferator):
        logging.info("Removing flow from the graph: " + flow_name + proliferator)
        if not self.node_name_exists(flow_name + proliferator + "Flow"):
            logging.error("Flow does not exist in the graph, cannot remove: " + flow_name + proliferator + " from " + str(self.graph.nodes.keys()))
            return
        if not self.graph.nodes.get(flow_name + proliferator + "Flow")["count_per_second"] == 0:
            logging.error("Flow still has count per second greater than zero, cannot remove: " + flow_name + proliferator)
            return
        for process_name in self.graph.predecessors(flow_name + proliferator + "Flow"):
            process = self.graph.nodes.get(process_name)
            if process["process_count_per_sec"] != 0:
                logging.error(f"Process {process_name} is still connected to flow {flow_name + proliferator}, cannot remove flow.")
            else:
                self.remove_process(process_name, proliferator)
        self.graph.remove_node(flow_name + proliferator + "Flow")
        
    def remove_process(self, process_name, proliferator):
        logging.info("Removing process from the graph: " + process_name + proliferator)
        if not self.node_name_exists(process_name + proliferator + "Process"):
            logging.error("Process does not exist in the graph, cannot remove: " + process_name + proliferator + " from " + str(self.graph.nodes.keys()))
            return
        if not self.graph.nodes.get(process_name + proliferator + "Process")["process_count_per_sec"] == 0:
            logging.error("Process still has count per second greater than zero, cannot remove: " + process_name + proliferator)
            return
        self.graph.remove_node(process_name + proliferator + "Process")
        for flow_name in self.graph.predecessors(process_name + proliferator + "Process"):
            flow = self.graph.nodes.get(flow_name)
            if flow["count_per_second"] != 0:
                logging.error(f"Flow {flow_name} is still connected to process {process_name + proliferator}, cannot remove process.")
            else:
                self.remove_flow(flow_name, proliferator)
        self.graph.remove_node(process_name + proliferator + "Process")
    
    def connect_flow_to_process(self, flow_name, process_name, proliferator, count_per_second):
        logging.info(f"Connecting {flow_name}(flow) to {process_name}(process), proliferator: {proliferator}")
        if not self.node_name_exists(flow_name + proliferator + "Flow"):
            logging.error("Flow does not exist in the graph, cannot connect: " + flow_name + proliferator)
            return
        if not self.node_name_exists(process_name + proliferator + "Process"):
            logging.error("Process does not exist in the graph, cannot connect: " + process_name + proliferator)
            return
        self.graph.add_edge(
            flow_name + proliferator + "Flow",
            process_name + proliferator + "Process",
            destination = self.graph.nodes[process_name + proliferator + "Process"],
            source = self.graph.nodes[flow_name + proliferator + "Flow"],
            name = f"{flow_name}(flow) to {process_name}(process), proliferator: {proliferator}",
            color = self.generate_edge_color(count_per_second),
            count_per_second = count_per_second
        )
    
    def connect_process_to_flow(self, process_name, flow_name, proliferator, count_per_second):
        logging.info(f"Connecting {process_name}(process) to {flow_name}(flow), proliferator: {proliferator}")
        if not self.node_name_exists(flow_name + proliferator + "Flow"):
            logging.error("Flow does not exist in the graph, cannot connect: " + flow_name + proliferator)
            return
        if not self.node_name_exists(process_name + proliferator + "Process"):
            logging.error("Process does not exist in the graph, cannot connect: " + process_name + proliferator)
            return
        self.graph.add_edge(
            process_name + proliferator + "Process",
            flow_name + proliferator + "Flow",
            source = self.graph.nodes[process_name + proliferator + "Process"],
            destination = self.graph.nodes[flow_name + proliferator + "Flow"],
            name = f"{process_name}(process) to {flow_name}(flow), proliferator: {proliferator}",
            color = self.generate_edge_color(count_per_second),
            count_per_sec = count_per_second
        )
    
    """
    def increase_flow(self, flow_name, count_per_second, proliferator):

        if self.node_name_exists(flow_name + proliferator + "Flow"):
            logging.info("Increasing flow for node: " + flow_name + proliferator)
            logging.error("Not implemented yet, need to handle flow increase logic.")
            # TODO
        else:
            logging.info("Node does not exist in the graph, adding node: " + flow_name + proliferator)
            self.add_flow(flow_name, count_per_second, proliferator)
            
    def add_flow(self, flow_name, count_per_second, proliferator):

        if self.node_name_exists(flow_name + proliferator + "Flow"):
            logging.error("Flow already exists in the graph: " + flow_name + proliferator)
            logging.debug(self.graph.nodes.keys())
            return
        node_id = flow_name + proliferator + "Flow"
        label = self.generate_label(flow_name + proliferator)
        self.graph.add_node(
            node_for_adding = node_id,
            color = "#797979",
            name = flow_name,
            count_per_second = count_per_second,
            proliferator = proliferator,
            label = label
        )
        if not Recipe.has_recipe(flow_name):
            logging.info("Adding raw item to the graph: " + flow_name + proliferator)
            return
        else:
            self.add_process_to_flow(flow_name, count_per_second, proliferator)

    def add_process_to_flow(self, flow_name, count_per_second, proliferator):

        if self.node_name_exists(flow_name + proliferator + "Process"):
            logging.error("Process already exists in the graph: " + flow_name + proliferator)
        else:
            recipes = Recipe.get_recipes_for_output_item(flow_name)
            if len(recipes) == 0:
                logging.warning(f"No recipes found for output item {flow_name}. Cannot create process.")
            elif len(recipes) == 1:
                recipe = recipes[0]
                name = flow_name + proliferator + "Process"
                process_name = flow_name
                label = self.generate_label(process_name + proliferator)
                output_multiplier = Proliferator.get_productivity(proliferator)
                process_count_per_sec = count_per_second / recipe.output_items[flow_name] / output_multiplier
                self.graph.add_node(
                    node_for_adding = name,
                    color = "#2F44FF",
                    name = process_name,
                    recipe = recipe,
                    process_count_per_sec = process_count_per_sec,
                    proliferator = proliferator,
                    label = label
                )
                self.add_connection_from_process_to_flow(process_name, flow_name, proliferator, count_per_second)
                logging.debug(f"Added connection from {process_name + proliferator + 'Process'} to {flow_name + proliferator + 'Flow'} with count_per_sec {count_per_second}")
                for input_item, input_count in recipe.input_items.items():
                    input_count_per_sec = input_count * process_count_per_sec
                    self.increase_flow(input_item, input_count_per_sec, proliferator)
                    self.add_connection_from_flow_to_process(input_item, process_name, proliferator, input_count_per_sec)
            else:
                logging.error(f"Multiple recipes found for output item {flow_name}. Cannot create process. Please specify a recipe.")
                    
            
    def reduce_flow(self, flow_name, count_per_second, proliferator):

        if not self.node_name_exists(flow_name + proliferator + "Flow"):
            logging.error(f"Flow {flow_name + proliferator} does not exist in the production graph.")
            logging.debug(self.graph.nodes.keys())
            return
        # Reduce the flow
        logging.info("Reducing flow:" + flow_name + proliferator)
        graph_flow = self.graph.nodes[flow_name + proliferator + "Flow"]
        graph_flow["count_per_second"] -= count_per_second
        # Reduce connected processes
        processes_to_reduce = []
        for process_name in self.graph.predecessors(graph_flow["name"] + proliferator + "Flow"):
            process = self.graph.nodes.get(process_name)
            processes_to_reduce.append(process)
        for process in processes_to_reduce:
            self.reduce_process(process["name"], flow_name, count_per_second, proliferator)
        # Delete the flow if the count per second is zero or less
        if graph_flow["count_per_second"] <= 0:
            self.remove_flow(flow_name, count_per_second, proliferator, recursive = False)
    
    def reduce_process(self, process, flow_name, count_per_second, proliferator):

        if not self.node_name_exists(process + proliferator + "Process"):
            logging.error(f"Process {process + proliferator} does not exist in the production graph.")
            logging.debug(self.graph.nodes.keys())
            return
        # Reduce the process
        logging.info(f"Reducing process {process} for item flow {flow_name}")
        graph_process = self.graph.nodes[process + proliferator + "Process"]
        production_count_per_sec = graph_process["recipe"].output_items[process] / graph_process["recipe"].time
        # Reduce connected item flows
        item_flows_to_reduce = []
        for item_flow_name in self.graph.predecessors(graph_process["name"] + proliferator + "Process"):
            item_flow = self.graph.nodes.get(item_flow_name)
            item_flows_to_reduce.append(item_flow)
        for item_flow in item_flows_to_reduce:
            print(item_flow["name"])
            self.reduce_flow(item_flow["name"], , proliferator)
        # Delete the process if the production count per second is zero or less
        if production_count_per_sec <= 0:
            self.remove_process(process, proliferator)

    def remove_flow(self, flow_name, count_per_second, proliferator, recursive = True):
        if not self.node_name_exists(flow_name + proliferator + "Flow"):
            logging.error("Flow does not exist in the graph, cannot remove: " + flow_name + proliferator + " from " + str(self.graph.nodes.keys()))
            return
        logging.info("Removing flow from the graph: " + flow_name + proliferator)
        if recursive:
            graph_flow = self.graph.nodes[flow_name + proliferator + "Flow"]
            for connection in self.graph.predecessors(graph_flow["name"]):
                source = connection.source
                self.reduce_process(source, flow_name, count_per_second, proliferator)
        self.graph.remove_node(flow_name + proliferator + "Flow")
    
    def remove_process(self, process_name, proliferator):
        if not self.node_name_exists(process_name + proliferator + "Process"):
            logging.error("Process does not exist in the graph, cannot remove: " + process_name + proliferator + " from " + str(self.graph.nodes.keys()))
            return
        logging.info("Removing process from the graph: " + process_name + proliferator)
        self.graph.remove_node(process_name + proliferator + "Process")
    
    def add_connection_from_process_to_flow(self, process_name, flow_name, proliferator, count_per_second):
        logging.info("Adding process to the graph: " + flow_name + proliferator)
        self.graph.add_edge(
            flow_name + proliferator + "Flow",
            process_name + proliferator + "Process",
            name = f"{flow_name}(flow) to {flow_name}(process), proliferator: {proliferator}",
            color = self.generate_edge_color(count_per_second),
            source = self.graph.nodes[flow_name + proliferator + "Process"],
            destination = self.graph.nodes[flow_name + proliferator + "Flow"],
            count_per_sec = count_per_second
        )
        
    def add_connection_from_flow_to_process(self, flow_name, process_name, proliferator, count_per_second):
        self.graph.add_edge(
            flow_name + proliferator + "Process",
            process_name + proliferator + "Flow",
            name = f"{process_name}(process) to {flow_name}(flow), proliferator: {proliferator}",
            color = self.generate_edge_color(count_per_second),
            source = self.graph.nodes[flow_name + proliferator + "Flow"],
            destination = self.graph.nodes[process_name + proliferator + "Process"],
            count_per_second = count_per_second
        )
    """
    def node_name_exists(self, node_name):
        return node_name in self.graph.nodes.keys()
    
    def generate_edge_color(self, count_per_second):
        red = int(255 * count_per_second / 30)
        green = int(255 * (1 - count_per_second / 30))
        return f"#{red:02X}{green:02X}00"
    
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
