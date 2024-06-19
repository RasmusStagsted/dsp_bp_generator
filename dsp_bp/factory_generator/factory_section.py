from .factory_line import FactoryLine
from .belt_router import BeltRouter
from ..utils import Vector
import enum

class FactorySection:
    
    class BeltRouting:
        
        def __init__(self, name, count_per_second, direction, placement, router_index, belt_index):
            self.name = name
            self.count_per_second = count_per_second
            self.direction = direction
            self.placement = placement
            self.router_index = router_index
            self.belt_index = belt_index
    
    def __init__(self, pos, input_count, output_count, product, recipe):
        print(recipe)
        self.product_count = len(recipe["output_items"].keys())
        
        self.router_width = 2 * (input_count + output_count + self.product_count)
        self.height = 7

        belt_routing = FactorySection.get_belt_routing(product, recipe)
        
        # Create factory line
        factory_line_pos = pos + Vector(x = self.router_width)
        factory_count = 5
        self.factory_line = FactoryLine(factory_line_pos, 1, self.product_count, recipe, factory_count)
        
        # Create router
        self.router = BeltRouter(pos, input_count, output_count, self.product_count, belt_routing, self.height)
        
        # Connect factory line and router
        #self.connect_to_factory_line(len(selector_belts), self.product_count)
        
    def get_belt_routing(product, recipe):
        ingredients = product.get_needed_ingredients()
        normalized_products = recipe["output_items"]
        products = product.get_products
        
        belts = [
            FactorySection.BeltRouting(
                name = "IronIngot",
                count_per_second = 1,
                direction = "input",
                placement = "buttom",
                router_index = 3,
                belt_index = 0
            ),
            FactorySection.BeltRouting(
                name = "IronOre",
                count_per_second = 1,
                direction = "output",
                placement = "top",
                router_index = 0,
                belt_index = 0
            ),
            FactorySection.BeltRouting(
                name = "IronOre",
                count_per_second = 1,
                direction = "output",
                placement = "top",
                router_index = 1,
                belt_index = 1
            ),
            FactorySection.BeltRouting(
                name = "IronOre",
                count_per_second = 1,
                direction = "output",
                placement = "buttom",
                router_index = 2,
                belt_index = 1
            )
        ]
        
        
        
        return belts
    
    def connect_to_factory_line(self, factory_input_count, factory_output_count):
        for i in range(factory_input_count):
            self.router.selector_belts[i].connect_to_belt(self.factory_line.input_belts[factory_input_count - i - 1])
        
        for i in range(factory_output_count):
            self.factory_line.output_belts[i].connect_to_belt(self.router.production_belts[i])
            
    def connect_to_section(self, section2):
        assert \
            len(self.router.input_belts) == len(section2.router.input_splitters) and \
            len(self.router.output_belts) == len(section2.router.output_splitters), \
                "The two sections must have same dimensions of input- and output belts"
        
        for i in range(len(self.router.input_belts)):
            section2.router.input_splitters[i].connect_to_belt(self.router.input_belts[i])
        for i in range(len(self.router.output_belts)):
            self.router.output_belts[i].connect_to_splitter(section2.router.output_splitters[i])