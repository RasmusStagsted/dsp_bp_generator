from ..buildings import TeslaTower, ArcSmelter, AssemblingMachineMKI, ConveyorBeltMKI, SorterMKI
from ..enums import Item
from ..utils import Yaw, Vector
from .factory_block import FactoryBlock
from .factory_block_interface import FactoryBlockInterface
from .proliferator import ProliferatorMKI, ProliferatorMKII, ProliferatorMKIII
from .recipes import Recipe
from ..blueprint import Blueprint, BlueprintBuildingV1
from ..buildings import Building
from copy import deepcopy

import math

class FactoryLine:
    """Represents a line of factory blocks with connected belts and sorters."""

    def __init__(self, pos, block_interface, recipe, factory_count, factory_type = None, belt_type = None, sorter_type = None):
        """Initialize the factory line and generate its factory blocks."""
        block_interface = deepcopy(block_interface)
        self.height = 6
        if factory_type is None:
            factory_type = FactoryLine.select_factory(recipe)
        self.block_width = int(factory_type.get_size().x)

        # Generate factory_blocks
        self.factory_blocks = []
        for i in range(factory_count):
            temp_pos = pos + Vector(x = i * self.block_width)
            factory_block = FactoryBlock(temp_pos, block_interface, recipe, factory_type, belt_type, sorter_type)
            self.factory_blocks.append(factory_block)
            FactoryLine.reduce_throughput(block_interface, recipe)

        # Connect factory_blocks
        for i in range(len(self.factory_blocks) - 1):
            
            FactoryBlock.connect_to_factory_block(
                self.factory_blocks[i],
                self.factory_blocks[i + 1]
            )
        
    @staticmethod
    def reduce_throughput(block_interface, recipe):
        for interface in block_interface:
            if interface.direction == FactoryBlockInterface.Direction.INGREDIENT:
                proliferator_scale = interface.proliferator.SPEED
                throughput_reduction = recipe.input_items[interface.item_type] * proliferator_scale
            elif interface.direction == FactoryBlockInterface.Direction.PRODUCT:
                proliferator_scale = interface.proliferator.SPEED * interface.proliferator.PRODUCTIVITY
                throughput_reduction = recipe.output_items[interface.item_type] * proliferator_scale
            else:
                raise ValueError(f"Unknown direction: {interface.direction} for item type: {interface.item_type}")
            interface.throughput = interface.throughput - throughput_reduction
            
    @staticmethod
    def select_factory(recipe):
        """Select the appropriate factory type based on the recipe's tool."""
        if recipe.tool == "Smelting Facility":
            return ArcSmelter
        elif recipe.tool == "Assembling Machine":
            return AssemblingMachineMKI
        else:
            raise ValueError(f"Unknown tool: {recipe['tool']}, Recipe: {recipe['name']}, ID: {recipe['recipe_id']}")

if __name__ == "__main__":
    INGREDIENT = FactoryBlockInterface.Direction.INGREDIENT
    PRODUCT = FactoryBlockInterface.Direction.PRODUCT
    BUTTOM = FactoryBlockInterface.Placement.BOTTOM
    TOP = FactoryBlockInterface.Placement.TOP

    pos = Vector(x = 0, y = 0)
    block_interface = [
        FactoryBlockInterface(
            name = "Magnet interface",
            item_type = "Magnet",
            direction = INGREDIENT,
            placement = BUTTOM,
            throughput = 12.0,
            belt_index = 0,
            proliferator = ProliferatorMKIII
        ),
        FactoryBlockInterface(
            name = "Copper interface",
            item_type = "CopperIngot",
            direction = INGREDIENT,
            placement = BUTTOM,
            throughput = 6.0,
            belt_index = 1,
            proliferator = ProliferatorMKIII
        ),
        FactoryBlockInterface(
            name = "MagneticCoil interface",
            item_type = "MagneticCoil",
            direction = PRODUCT,
            placement = TOP,
            throughput = 15.0,
            belt_index = 0,
            proliferator = ProliferatorMKIII
        ),
    ]
    recipe = Recipe.recipes["MagneticCoil"]
    factory_count = 3
    factory_type = None  # Let FactoryLine select the factory type based on the recipe

    factory_line = FactoryLine(pos, block_interface, recipe, factory_count, factory_type)
    blueprint = Blueprint()
    output_blueprint_string = blueprint.serialize(Building.buildings, blueprint_building_version = BlueprintBuildingV1)
    print(f"\nAssembly line created:\n{output_blueprint_string}\n")
    Building.buildings.clear()  # Clear the buildings for the next example
    
    pos = Vector(x = 0, y = 0)
    block_interface = [
        FactoryBlockInterface(
            name = "Iron ore interface",
            item_type = "IronOre",
            direction = INGREDIENT,
            placement = BUTTOM,
            throughput = 6.0,
            belt_index = 0,
            proliferator = ProliferatorMKIII
        ),
        FactoryBlockInterface(
            name = "Iron ingot interface",
            item_type = "IronIngot",
            direction = PRODUCT,
            placement = TOP,
            throughput = 7.5,
            belt_index = 0,
            proliferator = ProliferatorMKIII
        ),
    ]
    recipe = Recipe.recipes["IronIngot"]
    factory_count = 3
    factory_type = None  # Let FactoryLine select the factory type based on the recipe

    factory_line = FactoryLine(pos, block_interface, recipe, factory_count, factory_type)
    blueprint = Blueprint()
    output_blueprint_string = blueprint.serialize(Building.buildings, blueprint_building_version = BlueprintBuildingV1)
    print(f"Smeltery line created:\n{output_blueprint_string}")