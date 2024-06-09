from .building import Building
from ..utils import Pos, Yaw

class OilRefinary(Building):
    def __init__(self, name, pos: Pos, recipe_id: int = 0):
        super().__init__(name)
        self.pos1 = pos
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