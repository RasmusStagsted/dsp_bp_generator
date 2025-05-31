from ..utils import Vector, Yaw
from .factory_router_interface import FactoryRouterInterface
from .factory_block_interface import FactoryBlockInterface
from ..buildings import ConveyorBeltMKI, Splitter
from ..enums import BuildingModel
from ..blueprint import Blueprint, BlueprintBuildingV1
from ..buildings import Building

class FactoryRouter:
    """Handles the routing of routing belts and splitters for factory layouts."""

    def __init__(self, pos, input_count, output_count, product_count, belt_routing, belt_length):
        self.width = 2 * (input_count + output_count + product_count)
        self.generate_splitters(pos, input_count, output_count, product_count)
        self.generate_input_belts(pos, input_count, belt_length)
        self.generate_output_belts(pos, input_count, output_count, product_count, belt_length)
        self.generate_router_belts(pos, belt_routing)

    def generate_splitters(self, pos, input_count, output_count, product_count):
        """Generate input, output, and product splitters."""
        self.input_splitters = []
        self.output_splitters = []
        self.product_splitters = []
        input_splitter_properties = {
            "buffer": self.input_splitters,
            "name": "InputSplitter",
            "pos": pos,
            "count": input_count,
        }
        output_splitter_properties = {
            "buffer": self.output_splitters,
            "name": "OutputSplitter",
            "pos": pos + Vector(x = 2 * input_count),
            "count": output_count,
        }
        product_splitter_properties = {
            "buffer": self.product_splitters,
            "name": "ProductSplitter",
            "pos": pos + Vector(x = 2 * (input_count + output_count)),
            "count": product_count,
        }
        self.generate_splitter_section(**input_splitter_properties)
        self.generate_splitter_section(**output_splitter_properties)
        self.generate_splitter_section(**product_splitter_properties)
        self.splitters = self.input_splitters + self.output_splitters + self.product_splitters
        
    def generate_splitter_section(self, buffer, name, pos, count):
        """Generate splitter section."""
        for i in range(count):
            temp_pos = Vector(pos.x + 2 * i, pos.y)
            splitter = Splitter(
                name = f"{name}:{i}",
                pos = temp_pos,
                yaw = Yaw.North,
                mode = BuildingModel.SplitterTwoLayerStraight
            )
            buffer.append(splitter)
        
    def generate_input_belts(self, pos, input_count, belt_length):
        """Generate input belts and connect them to input splitters."""
        self.input_belts = []
        for i in range(input_count):
            temp_pos = Vector(pos.x + 2 * i, pos.y + belt_length - 1, 1)
            belts = ConveyorBeltMKI.generate_belt(f"BeltRouter:InputBelt:{i}", temp_pos, Yaw.South, belt_length)
            belt_start = belts[0]
            belt_end = belts[-1]
            self.input_belts.append(belt_start)
            splitter = self.input_splitters[i]
            belt_end.connect_to_splitter(splitter)

    def generate_output_belts(self, pos, input_count, output_count, product_count, belt_length):
        """Generate output and product belts, and connect them to splitters."""
        self.output_belts = []
        for i in range(output_count):
            temp_pos = Vector(pos.x + 2 * (i + input_count), pos.y, 1)
            belts = ConveyorBeltMKI.generate_belt(f"BeltRouter:OutputBelt:{i}", temp_pos, Yaw.North, belt_length)
            belt_start = belts[0]
            belt_end = belts[-1]
            self.output_belts.append(belt_end)
            splitter = self.output_splitters[i]
            splitter.connect_to_belt(belt_start)
        for i in range(product_count):
            temp_pos = Vector(pos.x + 2 * (i + input_count + output_count), pos.y, 1)
            belts = ConveyorBeltMKI.generate_belt(f"BeltRouter:ProductBelt:{i}", temp_pos, Yaw.North, belt_length)
            belt_start = belts[0]
            belt_end = belts[-1]
            self.output_belts.append(belt_end)
            splitter = self.product_splitters[i]
            splitter.connect_to_belt(belt_start)

    def generate_router_belts(self, pos, routes):
        """Generate product and selector belts based on routing information."""
        self.product_belts = []
        self.selector_belts = []
        for route in routes:
            if route.direction == "product":
                if route.placement == "top":
                    start_pos = pos + Vector(self.width - 1, 2 + route.belt_index)
                    yaw = [Yaw.West, Yaw.South]
                else:
                    start_pos = pos + Vector(self.width - 1, -2 - route.belt_index)
                    yaw = [Yaw.West, Yaw.North]
                name = "Productbelt"
                length = [self.width - 1 - 2 * route.router_index, 3 + route.belt_index]
                belt = ConveyorBeltMKI.generate_belt(name, start_pos, yaw, length)
                self.product_belts.append(belt)
                splitter = self.splitters[route.router_index]
                belt[-1].connect_to_splitter(splitter)
                for i in range(route.belt_index):
                    belt[-2 - i].move_relative(Vector(z = 0.0))
                for i in range(route.belt_index):
                    belt[-3 - i].move_relative(Vector(z = 0.3))
            elif route.direction == "ingredient":
                if route.placement == "top":
                    start_pos = pos + Vector(route.router_index * 2, 0)
                    yaw = [Yaw.North, Yaw.East]
                else:
                    start_pos = pos + Vector(route.router_index * 2, 0)
                    yaw = [Yaw.South, Yaw.East]
                name = "SelectorBelt"
                length = [2 + route.belt_index, self.width - 2 * route.router_index]
                belt = ConveyorBeltMKI.generate_belt(name, start_pos, yaw, length)
                self.selector_belts.append(belt)
                splitter = self.splitters[route.router_index]
                splitter.connect_to_belt(belt[0])
                for i in range(route.belt_index):
                    belt[2 + i].move_relative(Vector(z = 0.3))

if __name__ == "__main__":
    
    factory_router_interface = [
        FactoryRouterInterface(
            name = "Belt router interface iron ingot",
            item_type = "",
            direction = "ingredient",
        ),
    ]
    
    factory_block_interface = [
        FactoryBlockInterface(
            name="FactoryBlock",
            item_type="FactoryBlock",
            direction="product",
            placement="top",
            belt_index=0,
            factory_block_index=0,
            proliferator=None
        ),
    ]
    
    # Example usage
    pos = Vector(x = 0, y = 0)
    input_count = 3
    output_count = 3
    product_count = 3
    belt_length = 3


    router = BeltRouter(pos, input_count, output_count, product_count, belt_routing, belt_length)
    print(f"BeltRouter created: {router}")

    blueprint = Blueprint()
    output_blueprint_string = blueprint.serialize(Building.buildings, blueprint_building_version = BlueprintBuildingV1)
    print(output_blueprint_string)