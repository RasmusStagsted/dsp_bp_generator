from .building import Factory5x5
from ..utils import Vector, Yaw
from ..enums import BuildingItem, BuildingModel

class MatrixLab(Factory5x5):
    def __init__(self, name, pos: Vector, recipe_id: int = 0):
        super().__init__(name)
        self.pos = pos
        self.pos2 = pos
        self.yaw = Yaw.North
        self.yaw2 = Yaw.North
        self.item_id = BuildingItem.MatrixLab
        self.model_index = BuildingModel.MatrixLab
        self.output_object_index = -1
        self.input_object_index = -1
        self.recipe_id = recipe_id
        self.parameter_count = 1
        self.parameters = [0]

    def get_size():
        return Vector(5.0, 5.0)
    
    def get_height():
        return 5.0

    def get_offset():
        return Vector(2.5, 2.5)

class SelfEvolutionLab(Factory5x5):
    pass