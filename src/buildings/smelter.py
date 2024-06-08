from .building import Building3x3
from ..utils import Pos, Yaw
from ..enums import BuildingItem, BuildingModel

class Smelter(Building3x3):
    def __init__(self, name: str, pos: Pos, recipe_id: int = 0):
        super().__init__(name)
        self.pos1 = pos
        self.pos2 = pos
        self.yaw = Yaw.North
        self.yaw2 = Yaw.North
        self.output_object_index = -1
        self.input_object_index = -1
        self.recipe_id = recipe_id
        self.parameter_count = 1
        self.parameters = [0]
        
class ArcSmelter(Smelter):
    def __init__(self, name: str, pos: Pos, recipe_id: int = 0):
        super().__init__(name, pos, recipe_id)
        self.item_id = BuildingItem.ArcSmelter
        self.model_index = BuildingModel.ArcSmelter
        
class PlaneSmelter(Smelter):
    def __init__(self, name: str, pos: Pos, recipe_id: int = 0):
        super().__init__(name, pos, recipe_id)
        self.item_id = BuildingItem.PlaneSmelter
        self.model_index = BuildingModel.PlaneSmelter
        
class NegentrophySmelter(Smelter):
    def __init__(self, name: str, pos: Pos, recipe_id: int = 0):
        super().__init__(name, pos, recipe_id)
        self.item_id = BuildingItem.NegentrophySmelter
        self.model_index = BuildingModel.NegentrophySmelter
