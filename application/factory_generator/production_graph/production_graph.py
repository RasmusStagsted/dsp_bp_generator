import networkx as nx
from .connection import Connection

from .graphical_graph import GraphicalGraph

class ProductionGraph(GraphicalGraph):
    
    class ProcessList:

        def __init__(self):
            self.processes = {}
        
        def add_process(self, process):
            if not process in self:
                self.processes[process.name] = process
            else:
                raise ValueError(f"Process {process.name} already exists in production graph processes.")
    
        def remove_process(self, process):
            if process in self:
                del self.processes[process.name]
            else:
                raise ValueError(f"Process {process.name} does not exist in production graph processes.")
    
        def get_processes(self):
            return self.processes.values()
    
        def __contains__(self, process):
            return process.name in self.processes.keys()
    
        def __str__(self):
            text = "["
            for key, process in self.processes.items():
                text += str(process) + "\n"
            text += "]"
            return text
    
    class ItemFlowList:
        
        def __init__(self):
            self.flows = {}
        
        def add_flow(self, item_flow):
            if not item_flow in self:
                self.flows[item_flow.__hash__()] = item_flow 
            else:
                raise ValueError(f"Item flow {item_flow.name} {item_flow.proliferator} already exists in item_flows flows.")
    
        def remove_flow(self, item_flow):
            if item_flow in self:
                del self.flows[item_flow.__hash__()]
            else:
                raise ValueError(f"Item flow {item_flow.name} {item_flow.proliferator} does not exist in item_flows flows.")
    
        def get_flows(self):
            return self.flows.values()
    
        def __contains__(self, item_flow):
            return item_flow.__hash__() in self.flows.keys()

        """
        def __getitem__(self, item_flow):
            return self.flows[item_flow.__hash__()]

        def __setitem__(self, item_flow, value):
            self.flows[item_flow.__hash__()] = value
        """
        
        def __str__(self):
            text = "["
            for key, input_flow in self.flows.items():
                text += str(input_flow) + "\n"
            text += "]"
            return text
        
    def __init__(self, graph = None, parent = None):
        if graph is None:
            graph = nx.DiGraph()
        super().__init__(graph, parent)
        self.output_flows = ProductionGraph.ItemFlowList()
        self.input_flows = ProductionGraph.ItemFlowList()
        
        #self.forced_item_flows = ProductionGraph.ItemFlowList()
        #self.forced_output_flows = ProductionGraph.ItemFlowList()

        self.processes = ProductionGraph.ProcessList()
        self.item_flows = ProductionGraph.ItemFlowList()

    def add_process(self, process):
        if process.name not in self.processes.keys():
            self.processes[process.name] = process
            for input_flow in process.inputs:
                input_flow.add_destination(process)
            for output_flow in process.outputs:
                output_flow.add_source(process)
    """
    def add_item_flow(self, item_flow):
        if item_flow.name not in self.item_flows.keys():
            self.item_flows[item_flow.name] = item_flow
            for source in item_flow.sources:
                source.add_output(item_flow)
            for destination in item_flow.destinations:
                destination.add_input(item_flow)
    """
    def __str__(self):
        text = ""
        text += "Processes:\n" + str(self.processes) + "\n\n"
        text += "Item Flows:\n" + str(self.item_flows) + "\n\n"
        text += "Output Flows:\n" + str(self.output_flows) + "\n\n"
        text += "Input Flows:\n" + str(self.input_flows) + "\n\n"
        return text

    def add_output_item_flow(self, item_flow):
        print("Adding output item flow:", item_flow.name, "with count per sec:", item_flow.count_per_second)
        self._add_item_flow(item_flow)
        if not item_flow in self.output_flows:
            self.output_flows.add_flow(item_flow)

    def _add_item_flow(self, item_flow, destination = None):
        if not item_flow in self.item_flows:
            self._generate_item_flow(item_flow, destination)
        #else:
        #    self._add_to_item_flow(item_flow, destination)
            
    def reduce_output_item_flow(self, item_flow):
        if not self.output_flows.includes(item_flow):
            raise ValueError(f"Item flow {item_flow.name} does not exist in output flows.")
        else:
            if not self.output_flows[item_flow].count_per_sec > item_flow.count_per_sec:
                self.output_flows.remove_flow(item_flow)
            if self.item_flows.includes(item_flow):
                self.reduce_item_flow(item_flow)
    
    def _add_to_item_flow(self, item_flow, destination = None):
        if not item_flow in self.item_flows:
            raise ValueError(f"Item flow {item_flow.name} does not exist in item flows.")
        else:
            if len(item_flow.input_connections) > 0:
                connection = item_flow.input_connections[0]
                connection.count_per_sec += item_flow.count_per_sec
                if not destination is None:
                    self._connect_item_flow_to_process_input(item_flow, destination)
                self._add_to_process_output(destination, item_flow, connection.count_per_sec)
    
    def _add_to_process_output(self, process, item_flow, count_per_sec):
        prev_count_per_sec = process.output_connections[0].count_per_sec
        scale = (count_per_sec + prev_count_per_sec) / prev_count_per_sec
        process.output_connections[0].count_per_sec += count_per_sec
        for input_flow in process.input_connections:
            self._add_to_item_flow(input_flow, input_flow.count_per_sec * scale, process)
    
    def reduce_item_flow(self, item_flow):
        if not self.item_flows.includes(item_flow):
            raise ValueError(f"Item flow {item_flow.name} does not exist in item flows.")
        else:
            pass
    
    def _connect_item_flow_to_process_input(self, item_flow, process):
        item_count_per_recipe = process.recipe.input_items[item_flow.name]
        proliferator_multiplier = item_flow.proliferator.get_process_input_multiplier() if item_flow.proliferator != None else 1.0
        count_per_sec = process.factory_count / process.recipe.time * item_count_per_recipe * proliferator_multiplier
        Connection.connect(
            name = f"{item_flow.name}(item flow) to {process.name}(process)",
            source = item_flow,
            destination = process,
            count_per_sec = count_per_sec
        )
    
    def _generate_item_flow(self, new_item_flow, destination = None, round_up = False):
        if new_item_flow in self.item_flows:
            raise ValueError(f"Item flow {new_item_flow.name} already exists in item flow list.")
        else:
            self.item_flows.add_flow(new_item_flow)
            if not destination is None:
                self._connect_item_flow_to_process_input(new_item_flow, destination)
            
            #recipe = Recipe.select(new_item_flow.name)
            #
            #if recipe is None:
            #    if new_item_flow in self.input_flows:
            #        raise ValueError(f"Item flow {new_item_flow.name} already exists in input flows, cannot add as output flow.")
            #    else:
            #        self.input_flows.add_flow(new_item_flow)
            #elif len(recipe.output_items) != 1:
            #    raise ValueError(f"Recipe for {new_item_flow.name} has multiple outputs, cannot handle this case.")
            #else:
            #    self._generate_process_for_item_flow(new_item_flow, count_per_sec, recipe)

    def _generate_process_for_item_flow(self, item_flow, count_per_sec, recipe, round_up = False):
        factory_count = count_per_sec * recipe.time / recipe.output_items[item_flow.name]
        if round_up:
            factory_count = int(factory_count) + (1 if factory_count % 1 > 0 else 0)
        process = Process(
            name = item_flow.name,
            recipe = recipe,
            factory_count = factory_count,
            output_proliferator = ProliferatorNone
        )
        self.processes.add_process(process)
        
        Connection.connect(
            source = process,
            destination = item_flow,
            name = f"{process.name}(process) to {item_flow.name}(item flow)",
            count_per_sec = recipe.output_items[item_flow.name] / recipe.time * factory_count
        ) 
        
        for name, count in recipe.input_items.items():
            self._add_item_flow(
                ItemFlow(
                    name = name,
                    proliferator = ProliferatorNone
                ),
                count_per_sec = count * factory_count / recipe.time,
                destination = process
            )
    
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
    