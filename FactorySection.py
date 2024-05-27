from FactoryLine import FactoryLine
from BeltRouter import BeltRouter

class FactorySection:
    
    def __init__(self, buildings, x, y, input_count, output_count, selector_belts, product_count, factory_type, recipe, factory_count):
        
        self.router_width = 2 * (input_count + output_count + product_count) + 1
        
        # Create factory_line
        self.factory_line = FactoryLine(buildings, x + self.router_width, y, len(selector_belts), product_count, factory_type, recipe, factory_count)
                
        # Create router
        self.router = BeltRouter(buildings, x, y, input_count, output_count, product_count, selector_belts, self.factory_line.height)
        self.connect_factory_line_to_router(len(selector_belts), product_count)
        
    def connect_factory_line_to_router(self, facory_input_count, facory_output_count):
        for i in range(facory_input_count):
            self.router.selector_belts[i].connect_to_belt(self.factory_line.input_belts[i])
        
        for i in range(facory_output_count):
            self.factory_line.output_belts[i].connect_to_belt(self.router.production_belts[i])
            
    def connect_to_section(self, section2):
        assert len(self.router.input_belts) == len(section2.router.input_splitters) and len(self.router.output_belts) == len(section2.router.output_splitters), "The two sections must have same dimensions of input- and output belts"
        for i in range(len(self.router.input_belts)):
            section2.router.input_splitters[i].connect_to_belt(self.router.input_belts[i])
        for i in range(len(self.router.output_belts)):
            self.router.output_belts[i].connect_to_splitter(section2.router.output_splitters[i])