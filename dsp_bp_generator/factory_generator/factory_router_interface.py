from enum import IntEnum
from dsp_bp_generator.factory_generator.proliferator import Proliferator

class FactoryRouterInterface:

    class Direction(IntEnum):
        INGREDIENT = 0
        PRODUCT = 1
        
    def __init__(self, name: str, item_type: str, direction: Direction, pos, throughput: float, proliferator: Proliferator = None):
        self.name = name
        self.item_type = item_type
        self.direction = direction
        self.pos = pos
        self.throughput = throughput
        self.proliferator = proliferator

    def __str__(self):
        return (
            f"[FactoryBlockInterface] {self.name}\n"
            f"  Item type: {self.item_type}\n"
            f"  Direction: {self.direction.name.title()}\n"
            f"  Position: {self.pos.x}, {self.pos.y}, {self.pos.z}\n"
            f"  Throughput: {self.throughput} items/s\n"
            f"  Proliferator: {self.proliferator.name if self.proliferator else 'None'}\n"
        )