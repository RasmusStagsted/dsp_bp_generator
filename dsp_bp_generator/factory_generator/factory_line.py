from ..buildings import TeslaTower, ArcSmelter, AssemblingMachineMKI, ConveyorBeltMKI
from ..enums import Item
from ..utils import Yaw, Vector
from .factory_block import FactoryBlock
from .recipes import Recipe

import math

"""
A factory block consist of:
 - A single factory of any type
 - One to three input belts
 - One to three input sorters
 - One to three output belts
 - One to three output sorters
"""

class FactoryLine:
    
    def __init__(self, pos, belt_routing, recipe, factory_count):
        
        self.height = 6
        self._factory_type = FactoryLine.select_factory(recipe)
        self.block_width = int(self._get_factory_width())
        
        # Generate factory_blocks
        self.factory_blocks = []
        for i in range(factory_count):
            temp_pos = pos + Vector(x = i * self.block_width)
            factory_block = FactoryBlock(temp_pos, belt_routing, self._factory_type, self.block_width, recipe)
            self.factory_blocks.append(factory_block)
        
        # Connect factory_blocks
        for i in range(len(self.factory_blocks) - 1):
            self.factory_blocks[i].connect_to_factory_block(self.factory_blocks[i + 1])
        
        #self.input_belts = [factory_blocks[0].input_belts[i][0] for i in range(input_count)]
        #self.output_belts = [factory_blocks[0].output_belts[i][-1] for i in range(output_count)]
    
    def _get_factory_width(self):
        return self._factory_type.get_size().x
    
    def select_factory(recipe):
        if recipe["tool"] == "Smelting Facility":
            return ArcSmelter
        elif recipe["tool"] == "Assembling Machine":
            return AssemblingMachineMKI
        else:
            assert False, f"Unknown tool: {recipe['tool']}, Recipe: {recipe['name']}, ID: {recipe['recipe_id']}"