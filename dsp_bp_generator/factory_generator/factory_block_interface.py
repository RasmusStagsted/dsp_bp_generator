from enum import IntEnum

from dsp_bp_generator.factory_generator.proliferator import Proliferator

from dsp_bp_generator.factory_generator.recipes import Recipe

class FactoryBlockInterface:
    
    class Direction(IntEnum):
        INGREDIENT = 0
        PRODUCT = 1
        
    class Placement(IntEnum):
        TOP = 0
        BOTTOM = 1
    
    def __init__(self, name: str, item_type: str, direction: Direction, placement: Placement, throughput: float, belt_index: int, proliferator: Proliferator = None):
        # Name of the connection
        self.name = name
        # Type of item being transported
        self.item_type = item_type
        # Direction of the connection ("input", "output")
        self.direction = direction
        # Placement of the belt (top or bottom)
        self.placement = placement
        self.throughput = throughput
        # Index of the belt in the factory block
        # (1-3 for both top and buttom (1 is closest to the center of the machine))
        self.belt_index = belt_index
        # Optional proliferator for the connection
        self.proliferator = proliferator
        
    def __str__(self):
        return (
            f"[FactoryBlockInterface] {self.name}\n"
            f"  Item type: {self.item_type}\n"
            f"  Direction: {FactoryBlockInterface.Direction(self.direction).name}\n"
            f"  Placement: {FactoryBlockInterface.Placement(self.placement).name}\n"
            f"  Throughput: {self.throughput} items/s\n"
            f"  Belt index: {self.belt_index}\n"
            f"  Proliferator: {self.proliferator.name if self.proliferator else 'None'}\n"
        )
