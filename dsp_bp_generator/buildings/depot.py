from .building import Building, Factory3x3
from ..utils import Vector, Yaw
from ..enums import BuildingItem, BuildingModel, Item

import enum

class DepotMKI(Factory3x3):
    def __init__(self, name, pos: Vector, blocked_slots: int = 0):
        super().__init__(name)
        self.pos = pos
        self.pos2 = pos
        self.yaw = Yaw.North
        self.yaw2 = Yaw.North
        self.item_id = BuildingItem.DepotMKI
        self.model_index = BuildingModel.DepotMKI
        self.output_object_index = -1
        self.input_object_index = -1
        self.parameter_count = 110
        self.parameters = [blocked_slots] + [0 for i in range(109)]
        
    def get_size():
        return Vector(4.0, 4.0)
    
    def get_offset():
        return Vector(2.0, 2.0)

    def create_logistic_distributor(self, name, filter_id, chargin_power, icarus_mode, distributor_mode):
        self.output_to_slot = 14
        self.input_from_slot = 15
        self.output_to_slot = 15
        self.input_from_slot = 14
        return LogisticDistributor(
            name = name,
            pos = self.pos + Vector(z = 1.875),
            input_object_index = self.index,
            filter_id = filter_id,
            charging_power = chargin_power,
            icarus_mode = icarus_mode,
            distributor_mode = distributor_mode
        )

class DepotMKII:
    pass
      
class LogisticDistributor(Building):
    
    """
    0 < charging_power < 9 [MW]
    """
    
    class IcarusMode(enum.IntEnum):
        DisableIcarus = 0
        CollectFromIcarus = 1
        CollectFromAndProvideToIcarus = 2
        ProvideToIcarus = 3
    
    class DistributorMode(enum.IntEnum):
        DisableDistributors = 0
        ProvideToDistributors = 1
        RequestFromDistributors = 2

    def __init__(self, name, pos: Vector, input_object_index, charging_power: int, filter_id: Item, icarus_mode: IcarusMode, distributor_mode: DistributorMode):
        super().__init__(name)
        self.pos = pos
        self.pos2 = pos
        self.yaw = Yaw.North
        self.yaw2 = Yaw.North
        self.item_id = BuildingItem.LogisticDistributor
        self.model_index = BuildingModel.LogisticDistributor
        self.input_object_index = input_object_index
        self.filter_id = filter_id
        self.output_to_slot = 0
        self.input_from_slot = 13
        self.input_to_slot = 0
        self.output_from_slot = 0
        self.parameter_count = 128
        self.parameters = [icarus_mode, distributor_mode, 150000] + [0 for i in range(125)]
        