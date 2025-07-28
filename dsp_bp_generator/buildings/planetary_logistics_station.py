from .building import Building
from ..utils import Yaw
from ..enums import BuildingItem, BuildingModel
from ..utils import Vector

MAX_CHARGING_POWER_INDEX = 320

ITEM_ID_INDEX = 0
ITEM_MODE_INDEX = 1
ITEM_STORAGE_LIMIT_INDEX = 3
ENABLE_SLOT_OUTPUT_INDEX = 192
SLOT_OUTPUT_ITEM_INDEX = 193

ITEM_SETTINGS_SIZE = 6

class PlanetaryLogisticsStation(Building):    
    
#                 slot 2  slot 1  slot 0
#         ┌─────────────────────────────────────┐
#         │                                     │
#         │                                     │
#         │                                     │
# slot 3  │                                     │ slot 11
#         │                                     │
#         │                                     │
# slot 4  │                  X                  │ slot 10
#         │                                     │
#         │                                     │
# slot 5  │                                     │ slot 9
#         │                                     │
#         │                                     │
#         │                                     │
#         │                                     │
#         └─────────────────────────────────────┘
#                  slot 0  slot 1  slot 2  

    class ItemMode:
        STORAGE = 0
        SUPPLY = 1
        DEMAND = 2
        
    class ItemIndex:
        ITEM_1 = 0
        ITEM_2 = 1
        ITEM_3 = 2
        
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
    
    def set_item(self, item_index: ItemIndex, item_id: int, mode: ItemMode, storage_limit: int = 5000):
        assert item_index >= 0 and item_index <= 2, f"index needs to be: index >= 0 and index <= 2 (index was {item_index})"
        assert storage_limit >= 0 and storage_limit <= 5000, f"storage_limit needs to be >= 0 and <= 5000 (storage_limit was {storage_limit})"
        self.parameters[ITEM_ID_INDEX + item_index * ITEM_SETTINGS_SIZE] = item_id
        self.parameters[ITEM_MODE_INDEX + item_index * ITEM_SETTINGS_SIZE] = mode
        self.parameters[ITEM_STORAGE_LIMIT_INDEX + item_index * ITEM_SETTINGS_SIZE] = storage_limit
        
        
    def set_item_output(self, item_index: ItemIndex, slot_index: int):
        SLOT_SETTINGS_SIZE = 4
        self.parameters[ENABLE_SLOT_OUTPUT_INDEX + slot_index * SLOT_SETTINGS_SIZE] = 1
        self.parameters[SLOT_OUTPUT_ITEM_INDEX + slot_index * SLOT_SETTINGS_SIZE] = item_index + 1
        
    def number_of_slots(self):
        return 12
    
    def get_position_of_slot(self, slot):
        assert slot >= 0 and slot <= 11, f"slot index needs to be: slot >= 0 and slot <= 11 (slot was {slot})"
        if slot == 0:
            delta_pos = Vector(x =  1.00, y =  2.15)
        elif slot == 1:
            delta_pos = Vector(x =  0.00, y =  2.15)
        elif slot == 2:
            delta_pos = Vector(x = -1.00, y =  2.15)
        elif slot == 3:
            delta_pos = Vector(x = -2.15, y =  1.00)
        elif slot == 4:
            delta_pos = Vector(x = -2.15, y =  0.00)
        elif slot == 5:
            delta_pos = Vector(x = -2.15, y = -1.00)
        elif slot == 6:
            delta_pos = Vector(x = -1.00, y = -2.15)
        elif slot == 7:
            delta_pos = Vector(x =  0.00, y = -2.15)
        elif slot == 8:
            delta_pos = Vector(x =  1.00, y = -2.15)
        elif slot == 9:
            delta_pos = Vector(x =  2.15, y = -1.00)
        elif slot == 10:
            delta_pos = Vector(x =  2.15, y =  0.00)
        elif slot == 11:
            delta_pos = Vector(x =  2.15, y =  1.00)
        return self.pos + delta_pos
        
    def connect_output_to_belt(self, belt, item_index):
        slot = self.get_nearest_slot_from_position(belt.pos)
        belt.input_object_index = self.index
        belt.input_from_slot = slot
        belt.parameter_count = 2
        belt.parameters = [self.parameters[(item_index) * ITEM_SETTINGS_SIZE + ITEM_ID_INDEX], 0]
        self.set_item_output(item_index, slot)