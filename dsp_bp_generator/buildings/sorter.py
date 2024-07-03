from .building import Building
from ..utils import Vector, Yaw
from ..enums import BuildingItem, BuildingModel

class Sorter(Building):
    
    def __init__(self, name, pos: Vector, pos2: Vector, yaw: Yaw, output_object_index: int = -1, input_object_index: int = -1, output_to_slot: int = -1, input_from_slot: int = -1, output_from_slot: int = -1, input_to_slot: int = -1, output_offset: int = -1, input_offset: int = -1, parameters = []):
        super().__init__(name)
        self.pos = pos
        self.pos2 = pos2
        self.yaw = yaw
        self.yaw2 = yaw
        self.item_id = -1
        self.model_index = -1
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

    def set_filter(self, item):
        assert False, "Not supported"

    def generate_sorter_from_belt_to_building(name, belt, building, sorter_type):
        yaw = Yaw.get_neares_90_degree(belt.pos, building.pos)
        slot = building.get_nearest_slot_from_position(belt.pos)
        slot_pos = building.get_position_of_slot(slot)
        return sorter_type(
            name = name,
            pos = belt.pos,
            pos2 = slot_pos,
            yaw = yaw,
            output_object_index = building.index,
            input_object_index = belt.index,
            output_to_slot = slot,
            input_from_slot = -1,
            output_from_slot = 0,
            input_to_slot = 1,
            output_offset = 0,
            input_offset = 0,
            parameters = [1]
        )

    def generate_sorter_from_building_to_belt(name, building, belt, sorter_type = None):
        yaw = Yaw.get_neares_90_degree(building.pos, belt.pos)
        slot = building.get_nearest_slot_from_position(belt.pos)
        slot_pos = building.get_position_of_slot(slot)
        return sorter_type(
            name = name,
            pos = slot_pos,
            pos2 = belt.pos,
            yaw = yaw,
            output_object_index = belt.index,
            input_object_index = building.index,
            output_to_slot = -1,
            input_from_slot = slot,
            output_from_slot = 0,
            input_to_slot = 1,
            output_offset = -1,
            input_offset = 0,
            parameters = [1]
        )

    def generate_sorter_from_building_to_building(name, building_1, building_2, sorter_type = None):
        # Only one sorter can be generated from one factory to another
        yaw = Yaw.get_neares_90_degree(building_1.pos, building_2.pos)
        slot_1 = building_1.get_nearest_slot_from_position(building_2.pos)
        slot_2 = building_2.get_nearest_slot_from_position(building_1.pos)
        slot_1_pos = building_1.get_position_of_slot(slot_1)
        slot_2_pos = building_2.get_position_of_slot(slot_2)
        return sorter_type(
            name = name,
            pos = slot_1_pos,
            pos2 = slot_2_pos,
            yaw = yaw,
            output_object_index = building_2.index,
            input_object_index = building_1.index,
            output_to_slot = slot_2,
            input_from_slot = slot_1,
            output_from_slot = 0,
            input_to_slot = 1,
            output_offset = 0,
            input_offset = 0,
            parameters = [1]
        )

    def generate_sorter_from_belt_to_belt(name, factory, belt, sorter_type = None):
        assert False, "Not supported"

class SorterMKI(Sorter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.item_id = BuildingItem.SorterMKI
        self.model_index = BuildingModel.SorterMKI
        
    def generate_sorter_from_belt_to_building(name, belt, building):
        return Sorter.generate_sorter_from_belt_to_building(name, belt, building, SorterMKI)
    
    def generate_sorter_from_building_to_belt(name, building, belt):
        return Sorter.generate_sorter_from_building_to_belt(name, building, belt, SorterMKI)
    
    def generate_sorter_from_building_to_building(name, building_1, building_2):
        return Sorter.generate_sorter_from_building_to_building(name, building_1, building_2, SorterMKI)

class SorterMKII(Sorter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.item_id = BuildingItem.SorterMKII
        self.model_index = BuildingModel.SorterMKII
                
    def generate_sorter_from_belt_to_building(name, belt, building):
        return Sorter.generate_sorter_from_belt_to_building(name, belt, building, SorterMKII)
    
    def generate_sorter_from_building_to_belt(name, building, belt):
        return Sorter.generate_sorter_from_building_to_belt(name, building, belt, SorterMKII)

    def generate_sorter_from_building_to_building(name, building_1, building_2):
        return Sorter.generate_sorter_from_building_to_building(name, building_1, building_2, SorterMKII)

class SorterMKIII(Sorter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.item_id = BuildingItem.SorterMKIII
        self.model_index = BuildingModel.SorterMKIII
                
    def generate_sorter_from_belt_to_building(name, belt, building):
        return Sorter.generate_sorter_from_belt_to_building(name, belt, building, SorterMKIII)
    
    def generate_sorter_from_building_to_belt(name, building, belt):
        return Sorter.generate_sorter_from_building_to_belt(name, building, belt, SorterMKIII)

    def generate_sorter_from_building_to_building(name, building_1, building_2):
        return Sorter.generate_sorter_from_building_to_building(name, building_1, building_2, SorterMKIII)

class PileSorter(Sorter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.item_id = BuildingItem.PileSorter
        self.model_index = BuildingModel.PileSorter
                
    def generate_sorter_from_belt_to_building(name, belt, building):
        return Sorter.generate_sorter_from_belt_to_building(name, belt, building, PileSorter)
    
    def generate_sorter_from_building_to_belt(name, building, belt):
        return Sorter.generate_sorter_from_building_to_belt(name, building, belt, PileSorter)

    def generate_sorter_from_building_to_building(name, building_1, building_2):
        return Sorter.generate_sorter_from_building_to_building(name, building_1, building_2, PileSorter)
