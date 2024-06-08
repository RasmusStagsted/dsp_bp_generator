from .building import Building
from ..utils import Pos, Yaw
from ..enums import BuildingItem, BuildingModel

class Sorter(Building):
    
    def __init__(self, name, pos1: Pos, pos2: Pos, yaw: Yaw, output_object_index: int = -1, input_object_index: int = -1, output_to_slot: int = -1, input_from_slot: int = -1, output_from_slot: int = -1, input_to_slot: int = -1, output_offset: int = -1, input_offset: int = -1, parameters = []):
        super().__init__(name)
        self.pos1 = pos1
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

    def generate_sorter_from_belt_to_factory(name, belt, factory, sorter_type):
        yaw = Yaw.get_neares_90_degree(belt.pos1, factory.pos1)
        slot = factory.get_input_slot(belt.pos1)
        pos = factory.get_pos_from_slot(slot)
        return sorter_type(
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

    def generate_sorter_from_factory_to_belt(name, factory, belt, sorter_type = None):
        assert False, "Not supported"

    def generate_sorter_from_factory_to_factory(name, factory, belt, sorter_type = None):
        assert False, "Not supported"

    def generate_sorter_from_belt_to_belt(name, factory, belt, sorter_type = None):
        assert False, "Not supported"

class SorterMKI(Sorter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.item_id = BuildingItem.SorterMKI
        self.model_index = BuildingModel.SorterMKI

class SorterMKII(Sorter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.item_id = BuildingItem.SorterMKII
        self.model_index = BuildingModel.SorterMKII

class SorterMKIII(Sorter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.item_id = BuildingItem.SorterMKIII
        self.model_index = BuildingModel.SorterMKIII

class PileSorter(Sorter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.item_id = BuildingItem.PileSorter
        self.model_index = BuildingModel.PileSorter