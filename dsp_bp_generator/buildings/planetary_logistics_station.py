from .building import Building
from ..utils import Yaw
from ..enums import BuildingItem, BuildingModel


MAX_CHARGING_POWER_INDEX = 320

ITEM_ID_INDEX = 0
ITEM_MODE_INDEX = 1
ITEM_STORAGE_LIMIT_INDEX = 3

ITEM_SETTINGS_SIZE = 6

class PlanetaryLogisticsStation(Building):
    
    class ItemMode:
        STORAGE = 0
        SUPPLY = 1
        DEMAND = 2
        
    def __init__(self, name, pos):
        super().__init__(name)
        self.pos = pos
        self.pos2 = pos
        self.yaw = Yaw.North
        self.yaw2 = Yaw.North
        self.item_id = BuildingItem.PlanetaryLogisticsStation
        self.model_index = BuildingModel.PlanetaryLogisticsStation
        self.output_object_index = -1
        self.input_object_index = -1
        self.output_to_slot = 0
        self.input_from_slot = 0
        self.output_from_slot = 0
        self.input_to_slot = 0
        self.output_offset = 0
        self.input_offset = 0
        self.parameter_count = 2048
        self.parameters = [0] * 2048
        
        self.parameters[320] = 200000
        self.parameters[321] = -100000000
        self.parameters[322] = 240000000
        self.parameters[323] = 1
        self.parameters[324] = 480000
        self.parameters[325] = 1
        self.parameters[326] = 10
        self.parameters[327] = 100
        
    def set_max_charging_power(self, max_charging_power: float):
        assert max_charging_power >= 6 and max_charging_power <= 60, "max_changing_power should be in the range of 6 to 60 MW"
        self.parameters[MAX_CHARGING_POWER_INDEX] = int(max_charging_power / 60 * 1000000)
    
    def set_item(self, index, item_id, mode, storage_limit = 5000):
        assert index >= 0 and index <= 2, f"index needs to be: index >= 0 and index <= 2 (index was {index})"
        assert storage_limit >= 0 and storage_limit <= 5000, f"storage_limit needs to be >= 0 and <= 5000 (storage_limit was {storage_limit})"
        self.parameters[ITEM_ID_INDEX + index * ITEM_SETTINGS_SIZE] = item_id
        self.parameters[ITEM_MODE_INDEX + index * ITEM_SETTINGS_SIZE] = mode
        self.parameters[ITEM_STORAGE_LIMIT_INDEX + index * ITEM_SETTINGS_SIZE] = storage_limit