from .building import Building3x3
from ..utils import Pos, Yaw
from ..ItemEnum import ItemEnum

class Smelter(Building3x3):
    def __init__(self, name: str, pos: Pos, recipe_id: int = 0):
        super().__init__(name)
        self.pos1 = pos
        self.pos2 = pos
        self.yaw = Yaw.North
        self.yaw2 = Yaw.North
        self.item_id = ItemEnum.ArcSmelter
        self.model_index = 62
        self.output_object_index = -1
        self.input_object_index = -1
        self.recipe_id = recipe_id
        self.parameter_count = 1
        self.parameters = [0]
        
class ArcSmelter(Smelter):
    def __init__(self, name: str, pos: Pos, recipe_id: int = 0):
        super().__init__(name, pos, recipe_id)
        self.item_id = ItemEnum.ArcSmelter
        self.model_index = 62
        
class PlaneSmelter(Smelter):
    def __init__(self, name: str, pos: Pos, recipe_id: int = 0):
        super().__init__(name, pos, recipe_id)
        self.item_id = 0 # TODO Find the right id
        self.model_index = 0 # TODO Find the right index
        
class NegentrophySmelter(Smelter):
    def __init__(self, name: str, pos: Pos, recipe_id: int = 0):
        super().__init__(name, pos, recipe_id)
        self.item_id = 0 # TODO Find the right id
        self.model_index = 0 # TODO Find the right index
