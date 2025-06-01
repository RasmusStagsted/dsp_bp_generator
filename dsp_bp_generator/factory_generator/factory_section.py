from .factory_line import FactoryLine
from .recipes import Recipe
from ..blueprint import Blueprint, BlueprintBuildingV1
from .factory_router_interface import FactoryRouterInterface
from .factory_block_interface import FactoryBlockInterface
from ..buildings import Building
from .factory_router import FactoryRouter
from ..utils import Vector
import enum

class FactorySection:
    
    class BeltRouting:
        
        def __init__(self, name, max_count_per_second, item_type, direction, placement, router_index, belt_index):
            self.name = name
            self.max_count_per_second = max_count_per_second
            self.item_type = item_type
            self.direction = direction
            self.placement = placement
            self.router_index = router_index
            self.belt_index = belt_index

        def __str__(self):
            return (f"BeltRouting(name={self.name}, max_count_per_second={self.max_count_per_second}, "
                    f"direction={self.direction}, placement={self.placement}, "
                    f"router_index={self.router_index}, belt_index={self.belt_index})")
    
    def __init__(self, pos, factory_router_interface, recipe, factory_count, proliferator = None):

        block_interface = []
        factory_line_pos = pos + Vector(x = 2 * (len(factory_router_interface) + len(recipe.output_items)))
        self.factory_line = FactoryLine(factory_line_pos, block_interface, recipe, factory_count)

        self.factory_router = FactoryRouter(
            pos = pos,
            factory_router_interface = factory_router_interface,
            factory_block_interface = block_interface,
            proliferator = None
        )

    
    """        
    def __init__(self, pos, input_count, output_count, main_belts, product, recipe):
        self.product_count = len(recipe["output_items"].keys())
        
        self.router_width = 2 * (input_count + output_count + self.product_count)
        self.height = 7

        belt_routing = FactorySection.get_belt_routing(product, main_belts, recipe)
        factory_line_pos = pos + Vector(x = self.router_width)
        factory_count = 5
        self.factory_line = FactoryLine(factory_line_pos, belt_routing, recipe, factory_count)
        
        # Create router
        self.router = FactoryRouter(pos, input_count, output_count, self.product_count, belt_routing, self.height)
        
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
                    max_count_per_second = ingredient.count_pr_sec,
                    item_type = "",
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
                    max_count_per_second = product.count_pr_sec,
                    item_type = "",
                    direction = "product",
                    placement = "top",
                    router_index = 0,
                    belt_index = 0
                )
            )
        
        routes.sort(reverse = True, key = lambda flow: flow.max_count_per_second)
        
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
        for i in range(factory_input_count):
            print(self.router.selector_belts[i][-1])
            print(self.factory_line.factory_blocks[0].ingredient_belts[factory_input_count - i - 1][0])
            #self.router.selector_belts[i][-1].connect_to_belt(self.factory_line.factory_blocks[0].ingredient_belts[factory_input_count - i - 1][0])
        for i in range(factory_output_count):
            self.factory_line.factory_blocks[0].product_belts[i][-1].connect_to_belt(self.router.product_belts[i][0])
                
    def connect_to_section(self, section2):
        assert \
            len(self.router.input_belts) == len(section2.router.input_splitters) and \
            len(self.router.output_belts) == len(section2.router.output_splitters), \
                "The two sections must have same dimensions of input- and output belts"
        
        for i in range(len(self.router.input_belts)):
            section2.router.input_splitters[i].connect_to_belt(self.router.input_belts[i])
        for i in range(len(self.router.output_belts)):
            self.router.output_belts[i].connect_to_splitter(section2.router.output_splitters[i])
    """

if __name__ == "__main__":

    pos = Vector(x = 0, y = 0)
    
    INGREDIENT = FactoryBlockInterface.Direction.INGREDIENT
    PRODUCT = FactoryBlockInterface.Direction.PRODUCT
    
    factory_router_interface = [
        FactoryRouterInterface(
            name = "Belt router interface iron ore",
            item_type = "IronOre",
            direction = INGREDIENT,
            pos = Vector(0, 0),
            throughput = 6,
            proliferator = None,
        ),
        FactoryRouterInterface(
            name = "Belt router interface copper ore",
            item_type = "CopperOre",
            direction = INGREDIENT,
            pos = Vector(2, 0),
            throughput = 10,
            proliferator = None,
        ),
        FactoryRouterInterface(
            name = "Belt router interface iron ingot",
            item_type = "IronIngot",
            direction = PRODUCT,
            pos = Vector(4, 0),
            throughput = 20,
            proliferator = None,
        ),
    ]

    recipe = Recipe.recipes["MagneticCoil"]
    factory_count = 3

    FactorySection(pos, factory_router_interface, recipe, factory_count)
        
    blueprint = Blueprint()
    output_blueprint_string = blueprint.serialize(Building.buildings, blueprint_building_version=BlueprintBuildingV1)
    print(f"Blueprint string: {output_blueprint_string}")
    