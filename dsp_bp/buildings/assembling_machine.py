from .building import Building, Factory3x3
from ..utils import Vector, Yaw
from ..enums import BuildingItem, BuildingModel

class AssemblingMachine(Factory3x3):
    def __init__(self, name, pos: Vector, item_id: BuildingItem, model_index: int, recipe_id: int = 0):
        super().__init__(name)
        self.pos = pos
        self.pos2 = pos
        self.yaw = Yaw.North
        self.yaw2 = Yaw.North
        self.item_id = item_id
        self.model_index = model_index
        self.output_object_index = -1
        self.input_object_index = -1
        self.recipe_id = recipe_id
        self.parameter_count = 1
        self.parameters = [0]
        
    def get_size():
        return Vector(4.0, 4.0)
    
    def get_offset():
        return Vector(2.0, 2.0)
        
class AssemblingMachineMKI(AssemblingMachine):
    def __init__(self, name, pos: Vector, recipe_id: int = 0):
        super().__init__(
            name = name,
            pos = pos,
            item_id = BuildingItem.AssemblingMachineMKI,
            model_index = BuildingModel.AssemblingMachineMKI,
            recipe_id = recipe_id
        )
            
class AssemblingMachineMKII(AssemblingMachine):
    def __init__(self, name, pos: Vector, recipe_id: int = 0):
        super().__init__(
            name = name,
            pos = pos,
            item_id = BuildingItem.AssemblingMachineMKII,
            model_index = BuildingModel.AssemblingMachineMKII,
            recipe_id = recipe_id
        )
            
class AssemblingMachineMKIII(AssemblingMachine):
    def __init__(self, name, pos: Vector, recipe_id: int = 0):
        super().__init__(
            name = name,
            pos = pos,
            item_id = BuildingItem.AssemblingMachineMKIII,
            model_index = BuildingModel.AssemblingMachineMKIII,
            recipe_id = recipe_id
        )
            
class ReComposingAssembler(AssemblingMachine):
    def __init__(self, name, pos: Vector, recipe_id: int = 0):
        super().__init__(
            name = name,
            pos = pos,
            item_id = BuildingItem.ReComposingAssembler,
            model_index = BuildingModel.ReComposingAssembler,
            recipe_id = recipe_id
        )