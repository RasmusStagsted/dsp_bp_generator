from .building import Factory3x3
from ..utils import Vector, Yaw
from ..enums import BuildingItem, BuildingModel

class Smelter(Factory3x3):
    def __init__(self, name: str, pos: Vector, recipe_id: int = 0):
        super().__init__(name)
        self.pos = pos
        self.pos2 = pos
        self.yaw = Yaw.North
        self.yaw2 = Yaw.North
        self.output_object_index = -1
        self.input_object_index = -1
        self.output_to_slot = 0
        self.input_from_slot = 0
        self.output_from_slot = 0
        self.input_to_slot = 0
        self.recipe_id = recipe_id
        self.parameter_count = 1
        self.parameters = [0]
        
    def get_size():
        return Vector(3.0, 3.0)
    
    def get_offset():
        return Vector(1.5, 1.5)
        
class ArcSmelter(Smelter):
    def __init__(self, name: str, pos: Vector, recipe_id: int = 0):
        super().__init__(name, pos, recipe_id)
        self.item_id = BuildingItem.ArcSmelter
        self.model_index = BuildingModel.ArcSmelter
        
class PlaneSmelter(Smelter):
    def __init__(self, name: str, pos: Vector, recipe_id: int = 0):
        super().__init__(name, pos, recipe_id)
        self.item_id = BuildingItem.PlaneSmelter
        self.model_index = BuildingModel.PlaneSmelter
        
class NegentrophySmelter(Smelter):
    def __init__(self, name: str, pos: Vector, recipe_id: int = 0):
        super().__init__(name, pos, recipe_id)
        self.item_id = BuildingItem.NegentrophySmelter
        self.model_index = BuildingModel.NegentrophySmelter
