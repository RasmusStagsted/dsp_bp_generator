from ..buildings import TeslaTower, ArcSmelter, ConveyorBeltMKI
from ..enums import Item
from ..utils import Yaw, Vector
from .factory_block import FactoryBlock

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
    
    def __init__(self, pos, input_count, output_count, factory_type, recipe, factory_count):
        
        self.height = 6
        self._factory_type = factory_type
        self.block_width = self._get_factory_width()
        
        # Generate factory_blocks
        factory_blocks = []
        for i in range(factory_count):
            temp_pos = pos + Vector(x = i * self.block_width)
            input_belt_types = [ConveyorBeltMKI for i in range(input_count)]
            output_belt_types = [ConveyorBeltMKI for i in range(output_count)]
            factory_block = FactoryBlock(temp_pos, input_belt_types, output_belt_types, factory_type, self.block_width, recipe)
            factory_blocks.append(factory_block)
        
        # Connect factory_blocks
        for i in range(len(factory_blocks) - 1):
            factory_blocks[i].connect_to_factory_block(factory_blocks[i + 1])
        
        self.input_belts = [factory_blocks[0].input_belts[i][0] for i in range(input_count)]
        self.output_belts = [factory_blocks[0].output_belts[i][-1] for i in range(output_count)]
    
    def _get_factory_width(self):
        return self._factory_type.get_size().x
        
class FactoryLine2:

    def __init__(self, x, y, input_count, output_count, factory_type, recipe, factory_count):
        
        
        assert (factory_type == Item.Smelter) or \
            (factory_type == Item.AssemblingMachineMKI) or \
            (factory_type == Item.AssemblingMachineMKII) or \
            (factory_type == Item.AssemblingMachineMKIII), \
            f"Factory type ({factory_type}) isn't supported yet."
            
        assert output_count == 1, "recipes with multiple outputs isn't supported yet."
        
        if ((factory_type == Item.AssemblingMachineMKI) or \
            (factory_type == Item.AssemblingMachineMKII) or \
            (factory_type == Item.AssemblingMachineMKIII)):
            self._factory_width = 4
        elif (factory_type == Item.Smelter):
            self._factory_width = 3
        self._factory_height = 3
        self.height = self._factory_height + input_count + output_count
        
        belt_length = int(factory_count * self._factory_width + 1) + (math.ceil(factory_count / 4))
        self.height = self._factory_height + input_count + output_count + 1
        
        # Generate input-/output belts
        input_belts = self._generate_input_belts(x, y + self._factory_height // 2 + input_count, input_count, belt_length)
        output_belts = self._generate_factory_line_output_belts(x, y - 2, output_count, belt_length)
        self.input_belts = [input_belts[i][0] for i in range(input_count)]
        self.output_belts = [output_belts[i][-1] for i in range(output_count)]
        
        # Generate the factories
        factory_offset = 4
        power_pole_frequency = 0
        if factory_type == Item.Smelter:
            factory_offset = 3
            power_pole_frequency = 4
        factory_idicies = self._generate_factory_line_factories(x, y, factory_count, factory_offset, factory_type, recipe, power_pole_frequency)
        
        # Generate the sorters
        input_sorter_x = x
        input_sorter_y = y + self._factory_height // 2 + 1
        self._generate_factory_line_input_sorters(input_sorter_x, input_sorter_y, input_belts, factory_count, factory_offset, factory_idicies, power_pole_frequency)
        output_sorter_x = x
        output_sorter_y = y - self._factory_height // 2 - 1
        self._generate_factory_line_output_sorters(output_sorter_x, output_sorter_y, output_belts, factory_count, factory_offset, factory_idicies, power_pole_frequency)
        
        # Generate the power poles
        if factory_type == Item.Smelter:
            for i in range(math.ceil(factory_count / 4)):
                tesla_tower = Buildings.TeslaTower(
                    x = x + 13 * i + 7,
                    y = y
                )
            if factory_count % 4 == 1:
                tesla_tower.move(-3, 0)
        else:
            for i in range(math.ceil(factory_count / 4)):
                tesla_tower = Buildings.TeslaTower(
                    x = x + 16 * i + 8,
                    y = y
                )
            if factory_count % 4 == 1:
                tesla_tower.move(-4, 0)

        # Generate prolifirator
        # TODO
        #factory = self._generate_factory_block(buildings, x - 1, y, input_count, output_count, recipe)
        #self.input_belts = factory["input_belts"]
        #self.output_belts = factory["output_belts"]
        
    def _generate_factory_block(self, x, y, input_count, output_count, recipe):
        factory = Buildings.Smelter(
            x = x + self._factory_width // 2,
            y = y,
            z = 0,
            yaw = Yaw.North,
            recipe_id = recipe
        )
        
        input_belts = []
        for i in range(input_count):
            input_belts.append(generate_belt(x, y + (self._factory_height + 1) / 2 + i, 0, Yaw.East, self._factory_width - 1))
        
        output_belts = []
        for i in range(output_count):
            output_belts.append(generate_belt(x + self._factory_width - 1, y - (self._factory_height + 1) // 2 - i, 0, Yaw.West, self._factory_width - 1))
        return {"input_belts": [input_belts[i][0] for i in range(input_count)], "output_belts": [output_belts[i][-1] for i in range(output_count)]}
        
    def _generate_input_belts(self, x, y, input_count, belt_length):
        if input_count > 3:
            raise "More than three inputs isn't supported yet."
        input_belts = []
        for i in range(input_count):
            belts = generate_belt(
                x = x,
                y = y - i,
                z = 0.0,
                yaw = Yaw.East,
                length = belt_length
            )
            input_belts.append(belts)
            
        return input_belts
    
    def _generate_factory_line_output_belts(self, x, y, output_count, belt_length):
        if output_count > 3:
            raise "More than three outputs is not supported"
        output_belts = []
        for i in range(output_count):
            belts = generate_belt(
                x = x + belt_length - 1,
                y = y + i,
                z = 0.0,
                yaw = Yaw.West,
                length = belt_length
            )
            output_belts.append(belts)
            
        return output_belts

    def _generate_factory_line_factories(self, x, y, factory_count, factory_offset, factory_type, recipe, power_pole_frequency):
        factory_idicies = []
        for i in range(factory_count):
            factory_idicies.append(len(buildings))
            if factory_type == Item.Smelter:
                factory_height = 3
                pos_x = x + 2 + factory_offset * i
                if power_pole_frequency != 0:
                    pos_x += math.ceil((i - 1) / power_pole_frequency)
                Buildings.Smelter(
                    x = pos_x,
                    y = y,
                    z = 0,
                    yaw = Yaw.North,
                    recipe_id = recipe
                )
            elif factory_type == Item.AssemblingMachineMKIII:
                factory_height = 3
                Buildings.AssemblingMachineMKIII(
                    x = x + 2 + factory_offset * i,
                    y = y,
                    z = 0,
                    yaw = Yaw.North,
                    recipe_id = recipe
                )
            else:
                assert True, f"Factory type is not supported {factory_type}"
        return factory_idicies

    def _generate_factory_line_input_sorters(self, x, y, input_belts, factory_count, factory_offset, factory_idicies, power_pole_frequency):
        sorter_x_offset = [1.2, 2, 2.8]
        for i in range(len(input_belts)):
            for j in range(factory_count):
                x_pos = sorter_x_offset[i] + j * factory_offset
                if power_pole_frequency != 0:
                    x_pos += math.ceil((j - 1) / power_pole_frequency)
                Buildings.Sorter(
                    x1 = x + x_pos,
                    y1 = y + i,
                    z1 = 0.0,
                    x2 = x + x_pos,
                    y2 = y - 1.2,
                    z2 = 0.0,
                    yaw = Yaw.South,
                    output_object_index = factory_idicies[j],
                    input_object_index = input_belts[i][1 + j * factory_offset].index,
                    output_to_slot = i,
                    input_from_slot = -1,
                    output_from_slot = 0,
                    input_to_slot = 1,
                    output_offset = -1,
                    input_offset = 0,
                    parameters = [1]
                )

    def _generate_factory_line_output_sorters(self, x, y, output_belts, factory_count, factory_offset, factory_idicies, power_pole_frequency):
        sorter_x_offset = [1.2, 2, 2.8]
        for i in range(len(output_belts)):
            for j in range(factory_count):
                pos_x = sorter_x_offset[i] + j * factory_offset
                if power_pole_frequency != 0:
                    pos_x += math.ceil((j - 1) / power_pole_frequency)
                Buildings.Sorter(
                    x1 = x + pos_x,
                    y1 = y + 1.2,
                    z1 = 0.0,
                    x2 = x + pos_x,
                    y2 = y + i,
                    z2 = 0.0,
                    yaw = Yaw.South,
                    output_object_index = output_belts[i][2 + j * factory_offset].index,
                    input_object_index = factory_idicies[j],
                    output_to_slot = -1,
                    input_from_slot = 8 - i,
                    output_from_slot = 0,
                    input_to_slot = 1,
                    output_offset = -1,
                    input_offset = 0,
                    parameters = [1]
                )
        