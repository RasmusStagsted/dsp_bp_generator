from BlueprintBuilding import BlueprintBuilding
from ItemEnum import ItemEnum
from utils import direction_to_unit_vector, Yaw, Pos
import Buildings

class Building(BlueprintBuilding):
    
    buildings = []
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__class__.buildings.append(self)
        self.index = len(Building.buildings) - 1
    
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
    
class AssemblingMachineMkIII(Building):
    def __init__(self, pos, yaw = Yaw.North, recipe_id = 0):
        super().__init__()
        self.pos1 = pos
        self.pos2 = pos
        self.yaw = yaw
        self.yaw2 = yaw
        self.item_id = ItemEnum.AssemblingMachineMkIII
        self.model_index = 67
        self.output_object_index = -1
        self.input_object_index = -1
        self.recipe_id = recipe_id
        self.parameter_count = 1
        self.parameters = [0]
    
class Smelter(Building):
    def __init__(self, pos, yaw = Yaw.North, recipe_id = 0):
        super().__init__()
        self.pos1 = pos
        self.pos2 = pos
        self.yaw = yaw
        self.yaw2 = yaw
        self.item_id = ItemEnum.ArcSmelter
        self.model_index = 62
        self.output_object_index = -1
        self.input_object_index = -1
        self.recipe_id = recipe_id
        self.parameter_count = 1
        self.parameters = [0]

class Belt(Building):
    def __init__(self, pos, yaw, output_object_index = -1, input_object_index = -1, output_to_slot = 0):
        super().__init__()
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
        
    def connect_to_belt(self, belt2):
        dx, dy = direction_to_unit_vector(self.yaw)
        if ((int(self.pos1.x + dx) == belt2.pos.x) and (int(self.pos1.y + dy) == belt2.pos1.y) and self.yaw == belt2.yaw):
            self.output_object_index = belt2.index
            self.output_to_slot = 1
        else:
            print("Belt 1 direction:")
            print(f"dx: {dx}, dy: {dy}")
            print("Belt 1")
            print(self)
            dx, dy = direction_to_unit_vector(belt2.yaw)
            print("Belt 2 direction:")
            print(f"dx: {dx}, dy: {dy}")
            print("Belt 2")
            print(belt2)
            
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

    def generate_belt(pos, yaw, length):
        
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
                    pos = pos,
                    yaw = yaw[i],
                    output_object_index = Buildings.Building.count() + 1,
                    output_to_slot = 1
                )
                belts.append(belt)
                pos += Pos(dx, dy)
            
            if (i != len(yaw) - 1):
                belt.yaw = direction_average(yaw[i], yaw[i + 1])
            else:
                belt.output_object_index = -1
                belt.output_to_slot = -1
        return belts

class Sorter(Building):
    def __init__(self, pos1, pos2, yaw, output_object_index = -1, input_object_index = -1, output_to_slot = -1, input_from_slot = -1, output_from_slot = -1, input_to_slot = -1, output_offset = -1, input_offset = -1, parameters = []):
        super().__init__()
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
    """
    def generate_sorter_from_belt_to_factory(belt, factory, factory_slot):
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
    def __init__(self, pos, yaw):
        super().__init__()
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
        
    def connect_to_belt(self, belt):
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
    def __init__(self, pos):
        super().__init__()
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