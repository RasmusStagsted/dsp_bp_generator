from ..blueprint import BlueprintBuilding
from ..utils import Vector, Yaw
from ..enums import BuildingItem, BuildingModel

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
    
    def get_nearest_slot_from_position(self, pos):
        distances = []
        for i in range(self.number_of_slots()):
            distance = pos.get_distance(self.get_position_of_slot(i))
            distances.append(distance)
        slot = distances.index(min(distances))
        return slot
    
    def __str__(self):
        string = f"""
Blue Print Building:
====================
Name: {self.name}
====================
Index: {self.index}
Area index: {self.area_index}
position 1 x: {self.pos.x}
position 1 y: {self.pos.y}
position 1 z: {self.pos.z}
position 2 x: {self.pos2.x}
position 2 y: {self.pos2.y}
position 2 z: {self.pos2.z}
Yaw: {self.yaw}
Yaw2: {self.yaw2}
Item ID: {str(BuildingItem(self.item_id))} ({self.item_id})
Model index: {str(BuildingModel(self.model_index))} ({self.model_index})
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

class Factory(Building):
    
    def __init__(self, name = "Unknown", **kwargs):
        super().__init__(name, **kwargs)

    def set_recipe(self, recipe_id):
        self.recipe_id = recipe_id

class Factory3x3(Factory):

#          slot 0  slot 1  slot 2
#         ┌───────────────────────┐
#         │                       │
# slot 11 │                       │ slot 3
#         │                       │
#         │                       │
# slot 10 │           X           │ slot 4
#         │                       │
#         │                       │
# slot 9  │                       │ slot 5
#         │                       │
#         └───────────────────────┘
#           slot 8  slot 7  slot6  
    
    def number_of_slots(self):
        return 12
    
    def __init__(self, name = "Unknown", **kwargs):
        super().__init__(name, **kwargs)
        
    def get_position_of_slot(self, slot):
        assert slot >= 0 and slot <= 11, f"slot index needs to be: slot >= 0 and slot <= 11 (slot was {slot})"
        if slot == 0:
            delta_pos = Vector(x = -0.75, y = 0.8)
        elif slot == 1:
            delta_pos = Vector(x = 0.0, y = 0.8)
        elif slot == 2:
            delta_pos = Vector(x = 0.75, y = 0.8)
        elif slot == 3:
            delta_pos = Vector(x = 0.8, y = 0.75)
        elif slot == 4:
            delta_pos = Vector(x = 0.8, y = 0.0)
        elif slot == 5:
            delta_pos = Vector(x = 0.8, y = -0.75)
        elif slot == 6:
            delta_pos = Vector(x = 0.75, y = -0.8)
        elif slot == 7:
            delta_pos = Vector(x = 0.0, y = -0.8)
        elif slot == 8:
            delta_pos = Vector(x = -0.75, y = -0.8)
        elif slot == 9:
            delta_pos = Vector(x = -0.8, y = -0.75)
        elif slot == 10:
            delta_pos = Vector(x = -0.8, y = 0.0)
        elif slot == 11:
            delta_pos = Vector(x = -0.8, y = 0.75)

        return self.pos + delta_pos