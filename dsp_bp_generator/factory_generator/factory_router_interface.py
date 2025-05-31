from enum import IntEnum
from dsp_bp_generator.factory_generator.proliferator import Proliferator

class FactoryRouterInterface:
    pass
"""
    class Direction(IntEnum):
        INGREDIENT = 0
        PRODUCT = 1
        
    def __init__(self, name: str, item_type: str, direction: Direction, placement: Placement, router_index: int, belt_index: int, factory_block_index: int, proliferator: Proliferator = None):
        # Name of the connection
        self.name = name
        # Type of item being transported
        self.item_type = item_type
        # Direction of the connection ("input", "output")
        self.direction = direction
        # Placement of the belt x or xz placement
        self.placement = placement
        # Optional proliferator for the connection
        self.proliferator = proliferator

    def __str__(self):
        return (
            f"[FactoryBlockInterface] {self.name}\n"
            f"  Item type: {self.item_type}\n"
            f"  Direction: {self.direction.name.title()}\n"
            f"  Placement: {self.placement.name.title()}\n"
            f"  Proliferator: {self.proliferator.name if self.proliferator else 'None'}\n"
        )
"""
pass