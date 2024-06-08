from .building import Building
from ..utils import Pos, Yaw

class ChemicalPlant(Building):
    def __init__(self, name, pos: Pos, yaw: Yaw, recipe_id: int = 0):
        super().__init__(name)
        self.pos1 = pos
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

    def get_input_slot(self, source):
        dx = source.x - self.pos1.x
        dy = source.y - self.pos1.y

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
            

class QuantumChemicalPlant(ChemicalPlant):
    def __init__(self, name, pos: Pos, yaw: Yaw, recipe_id: int = 0):
        super().__init__(name, pos, yaw, recipe_id)
        self.item_id = BuildingItem.QuantumChemicalPlant
        self.model_index = BuildingModel.QuantumChemicalPlant