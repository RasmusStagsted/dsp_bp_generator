from dsp_bp_generator.utils import Vector

from .factory_router_interface import FactoryRouterInterface, FactoryRouterBelt
from .factory_block_interface import FactoryBlockInterface
from .factory_section import FactorySection
from .factory_block_interface import FactoryBlockInterface, FactoryBlockBelt
from dsp_bp_generator.blueprint import Blueprint
from dsp_bp_generator import buildings
from dsp_bp_generator.blueprint import BlueprintBuildingV1
from ..proliferator import ProliferatorNone, Proliferator
from ..recipes import Recipe
from copy import deepcopy
import math

class Factory:

    def __init__(self):
        buildings.Building.buildings.clear()

    def generate(self, graph):
        self.graph = graph
        self.bus = FactoryRouterInterface()
        self.factory_line_list, self.input_list = self.generate_factory_line_lists()
        self.factory_section_list = []
        x_offset = 0
        y_offset = 0

        for i, node_name in enumerate(self.input_list):
            node = self.graph.graph.nodes[node_name]
            
            self.bus.add_belt(FactoryRouterBelt(
                name = node_name + "Bus",
                item_type = node["name"],
                direction = FactoryRouterBelt.Direction.INGREDIENT,
                pos = Vector(x_offset, 0),
                throughput = node["items_per_second"],
                proliferator = node["proliferator"]
            ))
            x_offset += 2
        
        for node_name in self.factory_line_list:
            if node_name[-7:] == "Process":
                node = self.graph.graph.nodes[node_name]
                for product_node_name in self.graph.graph.successors(node_name):
                    product_node = self.graph.graph.nodes[product_node_name]
                    self.bus.add_belt(FactoryRouterBelt(
                        name = product_node["name"],
                        item_type = product_node["name"],
                        direction = FactoryRouterBelt.Direction.PRODUCT,
                        pos = Vector(x_offset, 0),
                        throughput = product_node["items_per_second"],
                        proliferator = product_node["proliferator"]
                    ))
                    x_offset += 2
                
                recipe_time = node["selected_recipe"].time
                factory_count = int(math.ceil(recipe_time * node["processes_per_second"])) # TODO: Fix
                
                factory_block_interface = FactoryBlockInterface.generate_interface(
                    recipe = node["selected_recipe"],
                    factory_count = factory_count,
                    proliferator = node["proliferator"]
                )
                
                self.factory_section_list.append(FactorySection(
                    pos = Vector(0, y_offset),
                    factory_router_interface = deepcopy(self.bus),
                    factory_block_interfaces = factory_block_interface,
                    recipe = node["selected_recipe"],
                    factory_count = factory_count,
                    proliferator = ProliferatorNone # TODO: Fix
                ))
                y_offset += self.factory_section_list[-1].get_height()
                if len(self.factory_section_list) > 1:
                    self.factory_section_list[-1].factory_router.connect_router_to_router(self.factory_section_list[-2].factory_router)
        
        
    def generate_factory_line_lists(self):
        available_items = []
        input_list = []

        for i in range(10): # Fix range to be dynamic calculated
            changes_done = False
            for node in self.graph.graph.nodes:
                if not node in available_items:
                    missing_input = False
                    detected_input = False
                    for item in self.graph.graph.predecessors(node):
                        detected_input = True
                        if item not in available_items:
                            missing_input = True 
                    if not detected_input:
                        input_list.append(node)
                    if not missing_input:
                        available_items.append(node)
                        changes_done = True
            if not changes_done:
                break
        return available_items, input_list

    def generate_bp_string(self):
        blueprint = Blueprint()
        blueprint_string = blueprint.serialize(buildings.Building.buildings, blueprint_building_version = BlueprintBuildingV1)
        return blueprint_string

    def has_predecessor(self, node):
        for item in self.graph.graph.predecessors(node):
            return True
        return False

class Factory2:

    def __init__(self, bus_input, assemblies, proliferators):
        self.bus_input = bus_input
        self.assemblies = assemblies
        self.proliferators = proliferators
        self.sections = []
    
    def generate_factory_buildings(self):
        self.height = 0
        for assembly in self.assemblies:
            
            section = FactorySection(
                pos = Vector(x = 0, y = 0),  # Placeholder position, should be calculated based on previous sections
                factory_router_interface = self.bus_input,
                factory_block_interfaces = [],
                recipe = Recipe(assembly),
                factory_count = assembly.get("Factories", 1),
                proliferator = assembly.get("Proliferator", None)
            )
            self.sections.append(section)
            self.height += section.get_height()
    
if __name__ == "__main__":
    
    INGREDIENT = FactoryBlockInterface.Direction.INGREDIENT
    PRODUCT = FactoryBlockInterface.Direction.PRODUCT
    
    bus_input = [
        FactoryRouterInterface(
            name = "Belt router interface iron ore",
            item_type = "IronOre",
            direction = INGREDIENT,
            pos = Vector(0, 0),
            throughput = 6,
            proliferator = None,
        ),
        FactoryRouterInterface(
            name = "Belt router interface iron ore",
            item_type = "CopperOre",
            direction = INGREDIENT,
            pos = Vector(0, 0),
            throughput = 6,
            proliferator = None,
        ),
    ]
    
    assemblies = [
        {
            "Magnet": {
                "Factories": 5,
                "Proliferator": None
            }
        }, {
            "CopperIngot": {
                "Factories": 2,
                "Proliferator": None
            },
        }, {"MagneticCoil": {
                "Factories": 3,
                "Proliferator": None
            },
        },
    ]
    
    factory = Factory(bus_input, assemblies)
    factory.calculate_assemblies()
    factory.generate_factory_buildings()