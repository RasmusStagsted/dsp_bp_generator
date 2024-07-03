from .building import Factory
from ..utils import Vector, Yaw
from ..enums import BuildingItem, BuildingModel

class OilRefinary(Factory):

#         ┌───────────────────────┐
#         │                       │
#         │                       │
#         │                       │
#         │-----------------------│
#         │                       │
# slot 2  │                       │ slot 3
#         │                       │
#         │-----------------------│
#         │                       │
# slot 1  │           X           │ slot 4
#         │                       │
#         │-----------------------│
#         │                       │
# slot 0  │                       │ slot 5
#         │                       │
#         │-----------------------│
#         │                       │
#         │                       │
#         │                       │
#         │-----------------------│
#         │                       │
#         │                       │
#         │                       │
#         └───────────────────────┘
#           slot 8  slot 7  slot 6  

    def __init__(self, name, pos: Vector, recipe_id: int = 0):
        super().__init__(name)
        self.pos = pos
        self.pos2 = pos
        self.yaw = Yaw.North
        self.yaw2 = Yaw.North
        self.item_id = BuildingItem.OilRefinary
        self.model_index = BuildingModel.OilRefinary
        self.output_object_index = -1
        self.input_object_index = -1
        self.recipe_id = recipe_id
        self.parameter_count = 1
        self.parameters = [0]

    def number_of_slots(self):
        return 9

    def get_position_of_slot(self, slot):
        assert slot >= 0 and slot < self.number_of_slots(), f"slot index needs to be: slot >= 0 and slot < {self.number_of_slots()} (slot was {slot})"
        if slot == 0:
            delta_pos = Vector(x = 0.877, y = -0.8)
        elif slot == 1:
            delta_pos = Vector(x = 0.877, y = 0.0)
        elif slot == 2:
            delta_pos = Vector(x = 0.877, y = 0.8)
        elif slot == 3:
            delta_pos = Vector(x = -0.877, y = 0.8)
        elif slot == 4:
            delta_pos = Vector(x = -0.877, y = 0.0)
        elif slot == 5:
            delta_pos = Vector(x = -0.877, y = -0.8)
        elif slot == 6:
            delta_pos = Vector(x = -0.9, y = -2.862)
        elif slot == 7:
            delta_pos = Vector(x = 0.0, y = -2.862)
        elif slot == 8:
            delta_pos = Vector(x = 0.9, y = -2.862)
        return delta_pos + self.pos
