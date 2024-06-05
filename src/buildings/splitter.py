from .building import Building
from .conveyer_belt import ConveyorBelt
from ..utils import Pos, Yaw
from ..ItemEnum import ItemEnum

class Splitter(Building):
    def __init__(self, name, pos: Pos, yaw: Yaw):
        super().__init__(name)
        self.pos1 = pos
        self.pos2 = pos
        self.yaw = yaw
        self.yaw2 = yaw
        self.item_id = ItemEnum.Splitter
        self.model_index = 39
        self.output_object_index = -1
        self.input_object_index = -1
        self.output_to_slot = 14
        self.input_from_slot = 15
        self.output_from_slot = 15
        self.input_to_slot = 14
        self.output_offset = 0
        self.input_offset = 0
        self.parameter_count = 6
        self.parameters = [0, 0, 0, 0, 0, 0]
        
    def connect_to_belt(self, belt: ConveyorBelt):
        assert (int(self.yaw - belt.yaw) % 180 == 0), f"Wrong orientation (splitter: {splitter.yaw}, belt: {belt.yaw})"
        
        belt.input_object_index = self.index
        
        if self.yaw == belt.yaw:
            belt.input_from_slot = 0
        else:
            belt.input_from_slot = 2
        if belt.pos1.z == 1:
            belt.input_from_slot += 1
        
        dx, dy = Yaw.direction_to_unit_vector(belt.yaw)
        belt.move_relative(Pos(dx * 0.2, dy * 0.2))
    
    def prioritize_input(self, slot):
        assert False, "Not supported"

    def prioritize_output(self, slot):
        assert False, "Not supported"
    
    def set_output_filter(self, slot, item):
        assert False, "Not supported"