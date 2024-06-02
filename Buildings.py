from BlueprintBuilding import BlueprintBuilding
from ItemEnum import ItemEnum
from utils import direction_to_unit_vector, Yaw, Pos
import Buildings

class Building(BlueprintBuilding):
    
    buildings = []
    
    def __init__(self, name = "Unknown", **kwargs):
        super().__init__(**kwargs)
        self.__class__.buildings.append(self)
        self.index = len(Building.buildings) - 1
        self.name = name
    
    def count():
        return len(Building.buildings)
    
    def get_last_building():
        return Building.buildings[-1]
    
    def get_building(index):
        return Building.buildings[index]
    
    def move(self, dx, dy, dz = 0):
        self.pos1.x += dx
        self.pos1.y += dy
        self.pos2.x += dx
        self.pos2.y += dy
    
    def __str__(self):
        string = f"""
Blue Print Building:
====================
Name: {self.name}
====================
Index: {self.index}
Area index: {self.area_index}
position 1 x: {self.pos1.x}
position 1 y: {self.pos1.y}
position 1 z: {self.pos1.z}
position 2 x: {self.pos2.x}
position 2 y: {self.pos2.y}
position 2 z: {self.pos2.z}
Yaw: {self.yaw}
Yaw2: {self.yaw2}
Item ID: {str(ItemEnum(self.item_id))[9:]} ({self.item_id})
Model index: {self.model_index}
Output object index: {self.output_object_index}
Input object index: {self.input_object_index}
Output to slot: {self.output_to_slot}
Input from slot: {self.input_from_slot}
Output from slot: {self.output_from_slot}
Input to slot: {self.input_to_slot}
Output offset: {self.output_offset}
Input offset: {self.input_offset}
Recipe id: {self.recipe_id}
Filter id: {self.filter_id}
Parameter count: {self.parameter_count}
"""
        for i in range(self.parameter_count):
            string += f"\tParam_{i}: {self.parameters[i]}\n"
        return string
    
class AssemblingMachine(Building):
    def __init__(self, name, pos: Pos, item_id: ItemEnum, model_index: int, recipe_id: int = 0):
        super().__init__(name)
        self.pos1 = pos
        self.pos2 = pos
        self.yaw = Yaw.North
        self.yaw2 = Yaw.North
        self.item_id = item_id
        self.model_index = model_index
        self.output_object_index = -1
        self.input_object_index = -1
        self.recipe_id = recipe_id
        self.parameter_count = 1
        self.parameters = [0]

    def get_input_slot(self, source):
        dx = source.x - self.pos1.x
        dy = source.y - self.pos1.y

        if dx < -0.5:
            if dy < -0.5:
                if -dy > -dx:
                    return 8
                else:
                    return 9
            elif dy > 0.5:
                if -dx > dy:
                    return 11
                else:
                    return 0               
            else:
                return 10        
        elif dx > 0.5:
            if dy < -0.5:
                if -dy > dx:
                    return 6
                else:
                    return 5
            elif dy > 0.5:
                if dx > dy:
                    return 3
                else:
                    return 2
            else:
                return 4
        else:
            if dy < -0.5:
                return 7
            elif dy > 0.5:
                return 1
            else:
                assert False, "Can't find slot index when source on top of target"
            
    def get_pos_from_slot(self, slot):
        assert slot >= 0 and slot <= 11, f"slot index needs to be: slot >= 0 and slot <= 8 (slot was {slot})"
        if slot == 0:
            delta_pos = Pos(x = -0.8, y = 0.8)
        elif slot == 1:
            delta_pos = Pos(x = 0.0, y = 0.8)
        elif slot == 2:
            delta_pos = Pos(x = 0.8, y = 0.8)
        elif slot == 3:
            delta_pos = Pos(x = 1.2, y = 0.8)
        elif slot == 4:
            delta_pos = Pos(x = 1.2, y = 0.0)
        elif slot == 5:
            delta_pos = Pos(x = 1.2, y = -0.8)
        elif slot == 6:
            delta_pos = Pos(x = 0.8, y = -0.8)
        elif slot == 7:
            delta_pos = Pos(x = 0.0, y = -0.8)
        elif slot == 8:
            delta_pos = Pos(x = -0.8, y = -0.8)
        elif slot == 9:
            delta_pos = Pos(x = -1.2, y = -0.8)
        elif slot == 10:
            delta_pos = Pos(x = -1.2, y = 0.0)
        elif slot == 11:
            delta_pos = Pos(x = -1.2, y = 0.8)

        return self.pos1 + delta_pos
        
class AssemblingMachineMkI(AssemblingMachine):
    def __init__(self, name, pos: Pos, recipe_id: int = 0):
        super().__init__(
            name = name,
            pos = pos,
            item_id = ItemEnum.AssemblingMachineMkI,
            model_index = 67,
            recipe_id = recipe_id
        )
            
class AssemblingMachineMkII(AssemblingMachine):
    def __init__(self, name, pos: Pos, recipe_id: int = 0):
        super().__init__(
            name = name,
            pos = pos,
            item_id = ItemEnum.AssemblingMachineMkII,
            model_index = 67,
            recipe_id = recipe_id
        )
            
class AssemblingMachineMkIII(AssemblingMachine):
    def __init__(self, name, pos: Pos, recipe_id: int = 0):
        super().__init__(
            name = name,
            pos = pos,
            item_id = ItemEnum.AssemblingMachineMkIII,
            model_index = 67,
            recipe_id = recipe_id
        )

class Smelter(Building):
    def __init__(self, name, pos: Pos, recipe_id: int = 0):
        super().__init__(name)
        self.pos1 = pos
        self.pos2 = pos
        self.yaw = Yaw.North
        self.yaw2 = Yaw.North
        self.item_id = ItemEnum.ArcSmelter
        self.model_index = 62
        self.output_object_index = -1
        self.input_object_index = -1
        self.recipe_id = recipe_id
        self.parameter_count = 1
        self.parameters = [0]
        
    def get_input_slot(self, source):
        dx = source.x - self.pos1.x
        dy = source.y - self.pos1.y

        if dx < -0.5:
            if dy < -0.5:
                if -dy > -dx:
                    return 8
                else:
                    return 9
            elif dy > 0.5:
                if -dx > dy:
                    return 11
                else:
                    return 0               
            else:
                return 10        
        elif dx > 0.5:
            if dy < -0.5:
                if -dy > dx:
                    return 6
                else:
                    return 5
            elif dy > 0.5:
                if dx > dy:
                    return 3
                else:
                    return 2
            else:
                return 4
        else:
            if dy < -0.5:
                return 7
            elif dy > 0.5:
                return 1
            else:
                assert False, "Can't find slot index when source on top of target"
            
    def get_pos_from_slot(self, slot):
        assert slot >= 0 and slot <= 11, f"slot index needs to be: slot >= 0 and slot <= 8 (slot was {slot})"
        if slot == 0:
            delta_pos = Pos(x = -1.0, y = 1.2)
        elif slot == 1:
            delta_pos = Pos(x = 0.0, y = 1.2)
        elif slot == 2:
            delta_pos = Pos(x = 1.0, y = 1.2)
        elif slot == 3:
            delta_pos = Pos(x = 1.2, y = 1.0)
        elif slot == 4:
            delta_pos = Pos(x = 1.2, y = 0.0)
        elif slot == 5:
            delta_pos = Pos(x = 1.2, y = -1.0)
        elif slot == 6:
            delta_pos = Pos(x = 1.0, y = -1.2)
        elif slot == 7:
            delta_pos = Pos(x = 0.0, y = -1.2)
        elif slot == 8:
            delta_pos = Pos(x = -1.0, y = -1.2)
        elif slot == 9:
            delta_pos = Pos(x = -1.2, y = -1.0)
        elif slot == 10:
            delta_pos = Pos(x = -1.2, y = 0.0)
        elif slot == 11:
            delta_pos = Pos(x = -1.2, y = 1.0)

        return self.pos1 + delta_pos

class Belt(Building):
    def __init__(self, name, pos: Pos, yaw: float, output_object_index: int = -1, input_object_index: int = -1, output_to_slot: int = 0):
        super().__init__(name)
        self.pos1 = pos
        self.pos2 = pos
        self.yaw = yaw
        self.yaw2 = yaw
        self.item_id = ItemEnum.ConveyorBeltMKIII
        self.model_index = 37
        self.output_object_index = output_object_index
        self.output_to_slot = output_to_slot
        
        self.output_from_slot = 0
        self.input_to_slot = 1
        
    def connect_to_belt(belt1, belt2):
        dx, dy = direction_to_unit_vector(belt1.yaw)
        if ((int(belt1.pos1.x + dx) == belt2.pos1.x) and (int(belt1.pos1.y + dy) == belt2.pos1.y) and belt1.yaw == belt2.yaw):
            belt1.output_object_index = belt2.index
            belt1.output_to_slot = 1
        else:
            print("Belt 1 direction:")
            print(f"dx: {dx}, dy: {dy}")
            print("Belt 1")
            print(belt1)
            dx, dy = direction_to_unit_vector(belt2.yaw)
            print("Belt 2 direction:")
            print(f"dx: {dx}, dy: {dy}")
            print("Belt 2")
            print(belt2)
            print()
            print(belt1.name)
            print(belt2.name)
            assert False, "Wrong use of belt-to_belt connection"
            
    def connect_to_splitter(self, splitter):
        assert (int(splitter.yaw - self.yaw) % 180 == 0), f"Wrong orientation (splitter: {splitter.yaw}, belt: {self.yaw})"
        
        self.output_object_index = splitter.index
        self.output_to_slot = 1
        
        if self.yaw == splitter.yaw:
            self.output_to_slot = 2
        else:
            self.output_to_slot = 0
        if self.pos1.z == 1:
            self.output_to_slot += 1
        
        # Move the belt back 0.2 spaces
        dx, dy = direction_to_unit_vector(self.yaw)
        self.move(-dx * 0.2, -dy * 0.2)

    def connect_to_sorter(self, sorter):
        pass

    def generate_belt(name, pos, yaw, length: int):
        
        if type(yaw) != list:
            yaw = [yaw]
        if type(length) != list:
            length = [length]
        assert len(yaw) == len(length), "\"yaw\" and \"length\" must have the same length"
        
        belts = []
        for i in range(len(yaw)):
            dx, dy = direction_to_unit_vector(yaw[i])
            for j in range(length[i]):
                belt = Buildings.Belt(
                    name = f"{name}:{len(belts)}",
                    pos = pos,
                    yaw = yaw[i],
                    output_object_index = Buildings.Building.count() + 1,
                    output_to_slot = 1
                )
                belts.append(belt)
                pos += Pos(dx, dy)
            
            if (i != len(yaw) - 1):
                belt.yaw = Yaw.direction_average(yaw[i], yaw[i + 1])
            else:
                belt.output_object_index = -1
                belt.output_to_slot = -1
        return belts

class Sorter(Building):
    def __init__(self, name, pos1: Pos, pos2: Pos, yaw: float, output_object_index: int = -1, input_object_index: int = -1, output_to_slot: int = -1, input_from_slot: int = -1, output_from_slot: int = -1, input_to_slot: int = -1, output_offset: int = -1, input_offset: int = -1, parameters = []):
        super().__init__(name)
        self.pos1 = pos1
        self.pos2 = pos2
        self.yaw = yaw
        self.yaw2 = yaw
        self.item_id = ItemEnum.SorterMKIII
        self.model_index = 43
        self.output_object_index = output_object_index
        self.input_object_index = input_object_index
        self.output_to_slot = output_to_slot
        self.input_from_slot = input_from_slot
        self.output_from_slot = output_from_slot
        self.input_to_slot = input_to_slot
        self.output_offset = output_offset
        self.input_offset = input_offset
        self.parameter_count = len(parameters)
        self.parameters = parameters

    def connect_to_belt(self, belt):
        pass
    
    def generate_sorter_from_belt_to_factory(name, belt, factory):
        yaw = Yaw.get_neares_90_degree(belt.pos1, factory.pos1)
        slot = factory.get_input_slot(belt.pos1)
        pos = factory.get_pos_from_slot(slot)
        print(slot)
        print(yaw)
        print(pos)
        return Sorter(
            name = name,
            pos1 = belt.pos1,
            pos2 = pos,
            yaw = yaw,
            output_object_index = belt.index,
            input_object_index = factory.index,
            output_to_slot = slot,
            input_from_slot = -1,
            output_from_slot = 0,
            input_to_slot = 1,
            output_offset = -1,
            input_offset = 0,
            parameters = [1]            
        )

    """
    def generate_sorter_from_factory_to_belt(factory, belt, factory_slot):
        
        yaw = Yaw.get_nearest_90_degree_yaw(factory.pos, belt.pos)
        return Sorter(
            x1 = belt.x,
            y1 = belt.y,
            z1 = belt.z,
            x2 = 
            y2 = 
            z2 = 0,
            yaw = 
            output_object_index = belt.index,
            input_object_index = factory.index,
            output_to_slot = 1
            
        )
    """

class Splitter(Building):
    def __init__(self, name, pos: Pos, yaw: float):
        super().__init__(name)
        self.pos1 = pos
        self.pos2 = pos
        self.yaw = yaw
        self.yaw2 = yaw
        self.item_id = ItemEnum.Splitter
        self.model_index = 39
        self.output_object_index = -1
        self.input_object_index = -1
        self.output_to_slot = 14
        self.input_from_slot = 15
        self.output_from_slot = 15
        self.input_to_slot = 14
        self.output_offset = 0
        self.input_offset = 0
        self.parameter_count = 6
        self.parameters = [0, 0, 0, 0, 0, 0]
        
    def connect_to_belt(self, belt: Belt):
        assert (int(self.yaw - belt.yaw) % 180 == 0), f"Wrong orientation (splitter: {splitter.yaw}, belt: {belt.yaw})"
        
        belt.input_object_index = self.index
        
        if self.yaw == belt.yaw:
            belt.input_from_slot = 0
        else:
            belt.input_from_slot = 2
        if belt.pos1.z == 1:
            belt.input_from_slot += 1
        
        dx, dy = direction_to_unit_vector(belt.yaw)
        belt.move(dx * 0.2, dy * 0.2)
        
class TeslaTower(Building):
    def __init__(self, name, pos):
        super().__init__(name)
        self.pos1 = pos
        self.pos2 = pos
        self.yaw = Yaw.North
        self.yaw2 = Yaw.North
        self.item_id = ItemEnum.TeslaTower
        self.model_index = 44
        self.output_object_index = -1
        self.input_object_index = -1
        self.output_to_slot = 0
        self.input_from_slot = 0
        self.output_from_slot = 0
        self.input_to_slot = 0
        self.output_offset = 0
        self.input_offset = 0
        self.parameter_count = 0
        self.parameters = []