from .building import Building
from ..utils import Yaw
from ..enums import BuildingItem, BuildingModel

class PowerDistributor(Building):
    def __init__(self, name, pos):
        super().__init__(name)
        self.pos = pos
        self.pos2 = pos
        self.yaw = Yaw.North
        self.yaw2 = Yaw.North
        self.item_id = None
        self.model_index = None
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

class TeslaTower(PowerDistributor):
    def __init__(self, name, pos):
        super().__init__(name, pos)
        self.item_id = BuildingItem.TeslaTower
        self.model_index = BuildingModel.TeslaTower

    def get_size(self):
        return Vector(1.0, 1.0)
    
    def get_offset(self):
        return Vector(0.5, 0.5)

class WirelessPowerTower(PowerDistributor):
    def __init__(self, name, pos):
        super().__init__(name, pos)
        self.item_id = BuildingItem.WirelessPowerTower
        self.model_index = BuildingModel.WirelessPowerTower
        
    def get_size(self):
        return Vector(1.0, 1.0)
    
    def get_offset(self):
        return Vector(0.5, 0.5)

class SateliteSubstation(PowerDistributor):
    def __init__(self, name, pos):
        super().__init__(name, pos)
        self.item_id = BuildingItem.SateliteSubstation
        self.model_index = BuildingModel.SateliteSubstation

    def get_size(self):
        return Vector(4.0, 4.0)
    
    def get_offset(self):
        return Vector(2.0, 2.0)
