from ..buildings import TeslaTower, ArcSmelter, AssemblingMachineMKI, ConveyorBeltMKI
from ..enums import Item
from ..utils import Yaw, Vector
from .factory_block import FactoryBlock
from .recipes import Recipe
from ..blueprint import Blueprint, BlueprintBuildingV1
from ..buildings import Building

import math

class FactoryLine:
    """Represents a line of factory blocks with connected belts and sorters."""

    def __init__(self, pos, belt_routing, recipe, factory_count, factory_type = None):
        """Initialize the factory line and generate its factory blocks."""
        self.height = 6
        if factory_type is None:
            factory_type = FactoryLine.select_factory(recipe)
        self.block_width = int(factory_type.get_size().x)

        # Generate factory_blocks
        self.factory_blocks = []
        for i in range(factory_count):
            temp_pos = pos + Vector(x = i * self.block_width)
            factory_block = FactoryBlock(temp_pos, belt_routing, factory_type, recipe)
            self.factory_blocks.append(factory_block)

        # Connect factory_blocks
        for i in range(len(self.factory_blocks) - 1):
            
            FactoryBlock.connect_to_factory_block(
                self.factory_blocks[i],
                self.factory_blocks[i + 1]
            )
        
        #self.input_belts = [self.factory_blocks[0].input_belts[i][0] for i in range(self.input_count)]
        #self.output_belts = [self.factory_blocks[0].output_belts[i][-1] for i in range(self.output_count)]
    
    @staticmethod
    def select_factory(recipe):
        """Select the appropriate factory type based on the recipe's tool."""
        if recipe["tool"] == "Smelting Facility":
            return ArcSmelter
        elif recipe["tool"] == "Assembling Machine":
            return AssemblingMachineMKI
        else:
            raise ValueError(f"Unknown tool: {recipe['tool']}, Recipe: {recipe['name']}, ID: {recipe['recipe_id']}")

if __name__ == "__main__":
    # Example Route class for demonstration
    class Route:
        def __init__(self, placement, direction, belt_index):
            self.placement = placement
            self.direction = direction
            self.belt_index = belt_index

    # Example recipe dictionary
    example_recipe = {
        "tool": "Assembling Machine",
        "name": "Example Product",
        "recipe_id": 1
    }

    pos = Vector(x = 0, y = 0)
    belt_routing = [
        Route(placement = "top", direction = "ingredient", belt_index = 0),
        Route(placement = "buttom", direction = "product", belt_index = 1)
    ]
    factory_count = 2
    factory_type = None  # Let FactoryLine select the factory type based on the recipe

    factory_line = FactoryLine(pos, belt_routing, example_recipe, factory_count, factory_type)
    blueprint = Blueprint()
    output_blueprint_string = blueprint.serialize(Building.buildings, blueprint_building_version = BlueprintBuildingV1)
    print(f"FactoryLine created: {output_blueprint_string}")