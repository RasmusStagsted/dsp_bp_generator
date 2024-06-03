from ..blueprint import BlueprintBuilding
from ..utils import Pos, Yaw
from ..ItemEnum import ItemEnum

class Building(BlueprintBuilding):
    
    buildings = []
    
    def __init__(self, name = "Unknown", **kwargs):
        super().__init__(**kwargs)
        self.__class__.buildings.append(self)
        self.index = len(Building.buildings) - 1
        self.name = name
    
    def count():
        return len(Building.buildings)
    
    def get_last_building():
        return Building.buildings[-1]
    
    def get_building(index):
        return Building.buildings[index]
    
    def __str__(self):
        string = f"""
Blue Print Building:
====================
Name: {self.name}
====================
Index: {self.index}
Area index: {self.area_index}
position 1 x: {self.pos1.x}
position 1 y: {self.pos1.y}
position 1 z: {self.pos1.z}
position 2 x: {self.pos2.x}
position 2 y: {self.pos2.y}
position 2 z: {self.pos2.z}
Yaw: {self.yaw}
Yaw2: {self.yaw2}
Item ID: {str(ItemEnum(self.item_id))[9:]} ({self.item_id})
Model index: {self.model_index}
Output object index: {self.output_object_index}
Input object index: {self.input_object_index}
Output to slot: {self.output_to_slot}
Input from slot: {self.input_from_slot}
Output from slot: {self.output_from_slot}
Input to slot: {self.input_to_slot}
Output offset: {self.output_offset}
Input offset: {self.input_offset}
Recipe id: {self.recipe_id}
Filter id: {self.filter_id}
Parameter count: {self.parameter_count}
"""
        for i in range(self.parameter_count):
            string += f"\tParam_{i}: {self.parameters[i]}\n"
        return string
    
class Building3x3(Building):
    
    def __init__(self, name = "Unknown", **kwargs):
        super().__init__(name, **kwargs)
        
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
            
    def get_pos_from_slot(self, slot):
        assert slot >= 0 and slot <= 11, f"slot index needs to be: slot >= 0 and slot <= 8 (slot was {slot})"
        if slot == 0:
            delta_pos = Pos(x = -0.8, y = 0.8)
        elif slot == 1:
            delta_pos = Pos(x = 0.0, y = 0.8)
        elif slot == 2:
            delta_pos = Pos(x = 0.8, y = 0.8)
        elif slot == 3:
            delta_pos = Pos(x = 1.2, y = 0.8)
        elif slot == 4:
            delta_pos = Pos(x = 1.2, y = 0.0)
        elif slot == 5:
            delta_pos = Pos(x = 1.2, y = -0.8)
        elif slot == 6:
            delta_pos = Pos(x = 0.8, y = -0.8)
        elif slot == 7:
            delta_pos = Pos(x = 0.0, y = -0.8)
        elif slot == 8:
            delta_pos = Pos(x = -0.8, y = -0.8)
        elif slot == 9:
            delta_pos = Pos(x = -1.2, y = -0.8)
        elif slot == 10:
            delta_pos = Pos(x = -1.2, y = 0.0)
        elif slot == 11:
            delta_pos = Pos(x = -1.2, y = 0.8)

        return self.pos1 + delta_pos