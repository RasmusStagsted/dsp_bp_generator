from dsp_bp_generator.blueprint import Blueprint, BlueprintBuildingV1
from dsp_bp_generator.buildings import Building
from dsp_bp_generator.utils import Vector

from .factory_line import FactoryLine
from .factory_router_interface import FactoryRouterInterface, FactoryRouterBelt
from .factory_block_interface import FactoryBlockInterface, FactoryBlockBelt
from .factory_router import FactoryRouter

from ..proliferator import ProliferatorNone, Proliferator

from ..recipes import Recipe

class FactorySection:
    
    class BeltRouting:
        
        def __init__(self, name, max_count_per_second, item_type, direction, placement, router_index, belt_index):
            self.name = name
            self.max_count_per_second = max_count_per_second
            self.item_type = item_type
            self.direction = direction
            self.placement = placement
            self.router_index = router_index
            self.belt_index = belt_index

        def __str__(self):
            return (f"BeltRouting(name={self.name}, max_count_per_second={self.max_count_per_second}, "
                    f"direction={self.direction}, placement={self.placement}, "
                    f"router_index={self.router_index}, belt_index={self.belt_index})")
    
    def __init__(self, pos, factory_router_interface, factory_block_interfaces, recipe, factory_count, proliferator = None):

        factory_line_pos = pos + Vector(x = 2 * (factory_router_interface.get_belt_count() + len(recipe.output_items)) - 2)
        self.factory_line = FactoryLine(factory_line_pos, factory_block_interfaces, recipe, factory_count)

        print(pos)
        self.factory_router = FactoryRouter(
            pos = pos,
            factory_router_interface = factory_router_interface,
            factory_block_interface = factory_block_interfaces,
            height = 8, 
            splitter_offset = Vector(y = -1 - factory_block_interfaces.get_top_belt_count()),
            proliferator = None
        )
        
    def get_height(self):
        return self.factory_line.get_height()

if __name__ == "__main__":

    pos = Vector(x = 0, y = 0)
    
    INGREDIENT = FactoryBlockBelt.Direction.INGREDIENT
    PRODUCT = FactoryBlockBelt.Direction.PRODUCT
    
    factory_router_interface = FactoryRouterInterface([
        FactoryRouterBelt(
            name = "Belt router interface iron ore",
            item_type = "IronOre",
            direction = INGREDIENT,
            pos = Vector(0, 0),
            throughput = 6,
            proliferator = None,
        ),
        FactoryRouterBelt(
            name = "Belt router interface copper ore",
            item_type = "CopperOre",
            direction = INGREDIENT,
            pos = Vector(2, 0),
            throughput = 10,
            proliferator = None,
        ),
        FactoryRouterBelt(
            name = "Belt router interface magnet",
            item_type = "Magnet",
            direction = PRODUCT,
            pos = Vector(4, 0),
            throughput = 20,
            proliferator = None,
        ),
    ])
    factory_block_interfaces = FactoryBlockInterface([
        FactoryBlockBelt(
            name = "FactoryBlock",
            item_type = "IronOre",
            direction = INGREDIENT,
            placement = FactoryBlockBelt.Placement.BOTTOM,
            throughput = 4.5,
            belt_index = 0,
            proliferator = None
        ),
        FactoryBlockBelt(
            name = "FactoryBlock",
            item_type = "Magnet",
            direction = PRODUCT,
            placement = FactoryBlockBelt.Placement.TOP,
            throughput = 4.5,
            belt_index = 0,
            proliferator = None
        ),
    ])

    recipe = Recipe.recipes["Magnet"]
    factory_count = 3
    proliferator = None # Not implemented yet, set to None for now
    FactorySection(pos, factory_router_interface, factory_block_interfaces, recipe, factory_count, proliferator)
        
    blueprint = Blueprint()
    output_blueprint_string = blueprint.serialize(Building.buildings, blueprint_building_version=BlueprintBuildingV1)
    print(f"Blueprint string:\n{output_blueprint_string}")
    
    Building.buildings = []  # Reset the buildings list to avoid duplicates

    pos = Vector(x = 0, y = 10)
    
    factory_router_interface = FactoryRouterInterface([
        FactoryRouterBelt(
            name = "Belt router interface iron ore",
            item_type = "IronOre",
            direction = INGREDIENT,
            pos = Vector(0, 0),
            throughput = 6,
            proliferator = ProliferatorNone,
        ),
        FactoryRouterBelt(
            name = "Belt router interface copper ore",
            item_type = "CopperOre",
            direction = INGREDIENT,
            pos = Vector(2, 0),
            throughput = 10,
            proliferator = ProliferatorNone,
        ),
        FactoryRouterBelt(
            name = "Belt router interface iron ingot",
            item_type = "IronIngot",
            direction = PRODUCT,
            pos = Vector(4, 0),
            throughput = 6,
            proliferator = ProliferatorNone,
        ),
        FactoryRouterBelt(
            name = "Belt router interface copper ingot",
            item_type = "CopperIngot",
            direction = PRODUCT,
            pos = Vector(6, 0),
            throughput = 10,
            proliferator = ProliferatorNone,
        ),
        FactoryRouterBelt(
            name = "Belt router interface circuit board",
            item_type = "CircuitBoard",
            direction = PRODUCT,
            pos = Vector(8, 0),
            throughput = 20,
            proliferator = ProliferatorNone,
        ),
    ])
    factory_block_interfaces = FactoryBlockInterface([
        FactoryBlockBelt(
            name = "FactoryBlock",
            item_type = "IronIngot",
            direction = INGREDIENT,
            placement = FactoryBlockBelt.Placement.TOP,
            throughput = 2.0,
            belt_index = 0,
            proliferator = None
        ),
        FactoryBlockBelt(
            name = "FactoryBlock",
            item_type = "CircuitBoard",
            direction = PRODUCT,
            placement = FactoryBlockBelt.Placement.BOTTOM,
            throughput = 4.5,
            belt_index = 0,
            proliferator = None
        ),
        FactoryBlockBelt(
            name = "FactoryBlock",
            item_type = "CopperIngot",
            direction = INGREDIENT,
            placement = FactoryBlockBelt.Placement.TOP,
            throughput = 4.5,
            belt_index = 1,
            proliferator = None
        ),
    ])
        
    recipe = Recipe.recipes["CircuitBoard"]
    factory_count = 1
    proliferator = ProliferatorNone # Not implemented yet, set to None for now
    FactorySection(pos, factory_router_interface, factory_block_interfaces, recipe, factory_count, proliferator)
    
    blueprint = Blueprint()
    output_blueprint_string = blueprint.serialize(Building.buildings, blueprint_building_version=BlueprintBuildingV1)
    print(f"Blueprint string:\n{output_blueprint_string}")
    
    Building.buildings = []  # Reset the buildings list to avoid duplicates

    
    
    pos = Vector(x = 0, y = 0)
    
    INGREDIENT = FactoryBlockBelt.Direction.INGREDIENT
    PRODUCT = FactoryBlockBelt.Direction.PRODUCT
    
    factory_router_interface = FactoryRouterInterface([
        FactoryRouterBelt(
            name = "Belt router interface circuit board",
            item_type = "CircuitBoard",
            direction = INGREDIENT,
            pos = Vector(0, 0),
            throughput = 1,
            proliferator = None,
        ),
        FactoryRouterBelt(
            name = "Belt router interface magnetic coil",
            item_type = "MagneticCoil",
            direction = INGREDIENT,
            pos = Vector(2, 0),
            throughput = 1,
            proliferator = None,
        ),
        FactoryRouterBelt(
            name = "Belt router interface electromagnetic matrix",
            item_type = "ElectromagneticMatrix",
            direction = PRODUCT,
            pos = Vector(4, 0),
            throughput = 1,
            proliferator = None,
        ),
    ])
    factory_block_interfaces = FactoryBlockInterface([
        FactoryBlockBelt(
            name = "FactoryBlock",
            item_type = "CircuitBoard",
            direction = INGREDIENT,
            placement = FactoryBlockBelt.Placement.BOTTOM,
            throughput = 1,
            belt_index = 0,
            proliferator = None
        ),
        FactoryBlockBelt(
            name = "FactoryBlock",
            item_type = "MagneticCoil",
            direction = INGREDIENT,
            placement = FactoryBlockBelt.Placement.BOTTOM,
            throughput = 1,
            belt_index = 1,
            proliferator = None
        ),
        FactoryBlockBelt(
            name = "FactoryBlock",
            item_type = "ElectromagneticMatrix",
            direction = PRODUCT,
            placement = FactoryBlockBelt.Placement.TOP,
            throughput = 1,
            belt_index = 0,
            proliferator = None
        ),
    ])

    recipe = Recipe.recipes["ElectromagneticMatrix"]
    factory_count = 1
    proliferator = None # Not implemented yet, set to None for now
    FactorySection(pos, factory_router_interface, factory_block_interfaces, recipe, factory_count, proliferator)
    
    blueprint = Blueprint()
    output_blueprint_string = blueprint.serialize(Building.buildings, blueprint_building_version=BlueprintBuildingV1)
    print(f"Blueprint string:\n{output_blueprint_string}")
    
    Building.buildings = []  # Reset the buildings list to avoid duplicates
