from .building import Building, Building3x3
from utils import Pos, Yaw
from ItemEnum import ItemEnum

class AssemblingMachine(Building3x3):
    def __init__(self, name, pos: Pos, item_id: ItemEnum, model_index: int, recipe_id: int = 0):
        super().__init__(name)
        self.pos1 = pos
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
        
class AssemblingMachineMkI(AssemblingMachine):
    def __init__(self, name, pos: Pos, recipe_id: int = 0):
        super().__init__(
            name = name,
            pos = pos,
            item_id = ItemEnum.AssemblingMachineMkI,
            model_index = 67, # TODO Find the right id 
            recipe_id = recipe_id
        )
            
class AssemblingMachineMkII(AssemblingMachine):
    def __init__(self, name, pos: Pos, recipe_id: int = 0):
        super().__init__(
            name = name,
            pos = pos,
            item_id = ItemEnum.AssemblingMachineMkII,
            model_index = 67, # TODO Find the right id 
            recipe_id = recipe_id
        )
            
class AssemblingMachineMkIII(AssemblingMachine):
    def __init__(self, name, pos: Pos, recipe_id: int = 0):
        super().__init__(
            name = name,
            pos = pos,
            item_id = ItemEnum.AssemblingMachineMkIII,
            model_index = 67,
            recipe_id = recipe_id
        )
            
class ReComposingAssembler(AssemblingMachine):
    def __init__(self, name, pos: Pos, recipe_id: int = 0):
        super().__init__(
            name = name,
            pos = pos,
            item_id = ItemEnum.ReComposingAssembler,
            model_index = 67, # TODO Find the right id 
            recipe_id = recipe_id
        )