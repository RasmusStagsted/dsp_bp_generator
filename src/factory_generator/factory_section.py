from .factory_line import FactoryLine
from .belt_router import BeltRouter
from ..utils import Pos

class FactorySection:
    
    def __init__(self, pos, input_count, output_count, selector_belts, product_count, factory_type, recipe, factory_count):
        
        self.router_width = 2 * (input_count + output_count + product_count) + 1
        
        # Create factory line
        factory_line_pos = pos + Pos(x = self.router_width)
        self.factory_line = FactoryLine(factory_line_pos, len(selector_belts), product_count, factory_type, recipe, factory_count)
        
        # Create router
        self.router = BeltRouter(pos, input_count, output_count, product_count, selector_belts, self.factory_line.height)
        
        # Connect factory line and router
        self.connect_to_factory_line(len(selector_belts), product_count)
        
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