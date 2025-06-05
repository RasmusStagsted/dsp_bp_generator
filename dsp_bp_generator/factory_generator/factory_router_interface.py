from enum import IntEnum
from dsp_bp_generator.factory_generator.proliferator import Proliferator

from dataclasses import dataclass

@dataclass
class FactoryRouterInterface:
    
    belts: list = None
    
    def get_ingredient_count(self):
        ingredient_count = 0
        for belt in self.belts:
            if belt.direction == FactoryRouterBelt.Direction.INGREDIENT:
                ingredient_count += 1
        return ingredient_count
    
    def get_product_count(self):
        product_count = 0
        for belt in self.belts:
            if belt.direction == FactoryRouterBelt.Direction.PRODUCT:
                product_count += 1
        return product_count
    
    def get_belt_count(self):
        return len(self.belts)

    def get_width(self):
        width = self.get_belt_count() * 2
        return width
    
    def __str__(self):
        text = (
            f"[FactoryRouterInterface] Belts count: {self.get_belt_count()}\n"
            f"  Ingredient count: {self.get_ingredient_count()}\n"
            f"  Product count: {self.get_product_count()}\n"
        )
        for belt in self.belts:
            text += str(belt) + "\n"
        return text.strip()

class FactoryRouterBelt:

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
            f"[FactoryRouterBelt] {self.name}\n"
            f"  Item type: {self.item_type}\n"
            f"  Direction: {self.direction.name.title()}\n"
            f"  Position: {self.pos.x}, {self.pos.y}, {self.pos.z}\n"
            f"  Throughput: {self.throughput} items/s\n"
            f"  Proliferator: {self.proliferator.name if self.proliferator else 'None'}\n"
        )