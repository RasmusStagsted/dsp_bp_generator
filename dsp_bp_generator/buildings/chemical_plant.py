from .building import Factory
from ..utils import Vector, Yaw
from ..enums import BuildingItem, BuildingModel

class ChemicalPlant(Factory):
    def __init__(self, name, pos: Vector, yaw: Yaw = Yaw.North, recipe_id: int = 0):
        super().__init__(name)
        self.pos = pos
        self.pos2 = pos
        self.yaw = yaw
        self.yaw2 = yaw
        self.item_id = BuildingItem.ChemicalPlant
        self.model_index = BuildingModel.ChemicalPlant
        self.output_object_index = -1
        self.input_object_index = -1
        self.recipe_id = recipe_id
        self.parameter_count = 1
        self.parameters = [0]

    def get_belt_sorter_position_offset(self):
        return 4
    
    def get_size():
        return Vector(7.0, 4.0)
    
    def get_height():
        return 4.0

    def get_offset():
        return Vector(3.5, 2)
    
    def number_of_slots(self):
        return 8

    def get_position_of_slot(self, slot):
        assert slot >= 0 and slot <= 7, f"slot index needs to be: slot >= 0 and slot <= 7 (slot was {slot})"
        if slot == 0:
            delta_pos = Vector(x =  1.375, y = -1.3)
        elif slot == 1:
            delta_pos = Vector(x =  0.375, y = -1.3)
        elif slot == 2:
            delta_pos = Vector(x = -0.375, y = -1.3)
        elif slot == 3:
            delta_pos = Vector(x = -1.375, y =  1.3)
        elif slot == 4:
            delta_pos = Vector(x = -0.375, y =  1.3)
        elif slot == 5:
            delta_pos = Vector(x =  0.375, y =  1.3)
        elif slot == 6:
            delta_pos = Vector(x =  1.375, y =  1.3)
        elif slot == 7:
            delta_pos = Vector(x = -1.375, y = -1.3)
        return self.pos + delta_pos

class QuantumChemicalPlant(ChemicalPlant):
    def __init__(self, name, pos: Vector, yaw: Yaw, recipe_id: int = 0):
        super().__init__(name, pos, yaw, recipe_id)
        self.item_id = BuildingItem.QuantumChemicalPlant
        self.model_index = BuildingModel.QuantumChemicalPlant