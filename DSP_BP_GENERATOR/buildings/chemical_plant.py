from .building import Factory
from ..utils import Vector, Yaw

class ChemicalPlant(Factory):
    def __init__(self, name, pos: Vector, yaw: Yaw, recipe_id: int = 0):
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

    def get_slot_from_pos(self, pos):
        dx = pos.x - self.pos.x
        dy = pos.y - self.pos.y

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
        assert slot >= 0 and slot <= 7, f"slot index needs to be: slot >= 0 and slot <= 7 (slot was {slot})"
        assert False, "Not tested"
        if slot == 0:
            delta_pos = Vector(x = 0.8, y = -0.8)
        elif slot == 1:
            delta_pos = Vector(x = 0.8, y = 0.0)
        elif slot == 2:
            delta_pos = Vector(x = 0.8, y = 0.8)
        elif slot == 3:
            delta_pos = Vector(x = -0.8, y = 0.8)
        elif slot == 4:
            delta_pos = Vector(x = -0.8, y = 0.0)
        elif slot == 5:
            delta_pos = Vector(x = -0.8, y = -0.8)
        elif slot == 6:
            delta_pos = Vector(x = 0.8, y = -0.8)
        elif slot == 7:
            delta_pos = Vector(x = 0.0, y = -0.8)
        elif slot == 8:
            delta_pos = Vector(x = -0.8, y = -0.8)
        elif slot == 9:
            delta_pos = Vector(x = -1.2, y = -0.8)
        elif slot == 10:
            delta_pos = Vector(x = -1.2, y = 0.0)
        elif slot == 11:
            delta_pos = Vector(x = -1.2, y = 0.8)

class QuantumChemicalPlant(ChemicalPlant):
    def __init__(self, name, pos: Vector, yaw: Yaw, recipe_id: int = 0):
        super().__init__(name, pos, yaw, recipe_id)
        self.item_id = BuildingItem.QuantumChemicalPlant
        self.model_index = BuildingModel.QuantumChemicalPlant