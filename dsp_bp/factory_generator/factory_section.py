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
    
    def __init__(self, pos, input_count, output_count, main_belts, product, recipe):
        self.product_count = len(recipe["output_items"].keys())
        
        self.router_width = 2 * (input_count + output_count + self.product_count)
        self.height = 7

        belt_routing = FactorySection.get_belt_routing(product, main_belts, recipe)
        
        # Create factory line
        factory_line_pos = pos + Vector(x = self.router_width)
        factory_count = 5
        self.factory_line = FactoryLine(factory_line_pos, belt_routing, recipe, factory_count)
        
        # Create router
        self.router = BeltRouter(pos, input_count, output_count, self.product_count, belt_routing, self.height)
        
        # Connect factory line and router
        self.connect_to_factory_line(len(recipe["input_items"].keys()), self.product_count)
        
    def get_belt_routing(product, main_belts, recipe):
        ingredients = product.get_needed_ingredients()
        normalized_products = recipe["output_items"]
        products = product.get_products()
        
        routes = []
        for ingredient in ingredients:
            routes.append(
                FactorySection.BeltRouting(
                    name = ingredient.name,
                    count_per_second = ingredient.count_pr_sec,
                    direction = "ingredient",
                    placement = "top",
                    router_index = 0,
                    belt_index = 0
                )
            )
            
        for product in products:
            routes.append(
                FactorySection.BeltRouting(
                    name = product.name,
                    count_per_second = product.count_pr_sec,
                    direction = "product",
                    placement = "top",
                    router_index = 0,
                    belt_index = 0
                )
            )
        
        routes.sort(reverse = True, key = lambda flow: flow.count_per_second)
        
        top_count = 0
        buttom_count = 0
        for i, route in enumerate(routes):
            if i % 2 == 0:
                route.placement = "top"
                route.belt_index = top_count
                top_count += 1
            else:
                route.placement = "buttom"
                route.belt_index = buttom_count
                buttom_count += 1
            for i, belt in enumerate(main_belts):
                if belt.name == route.name:
                    route.router_index = i
                    break
            
        return routes
    
    def connect_to_factory_line(self, factory_input_count, factory_output_count):
        #for i in range(factory_input_count):
        #    self.router.selector_belts[i][-1].connect_to_belt(self.factory_line.factory_blocks[0].ingredient_belts[factory_input_count - i - 1][0])
        
        """
        for i in range(factory_output_count):
            print()
            self.factory_line.factory_blocks[0].product_belts[i][-1].connect_to_belt(self.router.product_belts[i][0])
        """    
    def connect_to_section(self, section2):
        assert \
            len(self.router.input_belts) == len(section2.router.input_splitters) and \
            len(self.router.output_belts) == len(section2.router.output_splitters), \
                "The two sections must have same dimensions of input- and output belts"
        
        for i in range(len(self.router.input_belts)):
            section2.router.input_splitters[i].connect_to_belt(self.router.input_belts[i])
        for i in range(len(self.router.output_belts)):
            self.router.output_belts[i].connect_to_splitter(section2.router.output_splitters[i])