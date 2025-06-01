from ..utils import Vector, Yaw
from .factory_router_interface import FactoryRouterInterface
from .factory_block_interface import FactoryBlockInterface
from ..buildings import ConveyorBelt, Splitter
from ..enums import BuildingModel
from ..blueprint import Blueprint, BlueprintBuildingV1
from ..buildings import Building

class FactoryRouter:
    """Handles the routing of routing belts and splitters for factory layouts."""

    def __init__(self, pos, factory_router_interface, factory_block_interface, proliferator = None):
        
        self.width = max([con.pos.x for con in factory_router_interface]) + 1
        self.height = 6
        self.generate_splitters(pos, factory_router_interface)
        self.generate_bus_belts(pos, factory_router_interface)
        self.generate_router_belts(pos, factory_router_interface, factory_block_interface, proliferator)

    def generate_splitters(self, pos, factory_router_interface):
        self.splitters = {}
        for connection in factory_router_interface:
            self.splitters[connection] = Splitter(
                name = f"{connection.name}",
                pos = pos + connection.pos,
                yaw = Yaw.North,
                mode = BuildingModel.SplitterTwoLayerStraight
            )
            
    def generate_bus_belts(self, pos, factory_router_interface):
        self.bus_belts = {}
        for connection in factory_router_interface:
            belt_type = ConveyorBelt.get_minimum_required_belt_type(connection.throughput)
            if connection.direction == FactoryBlockInterface.Direction.INGREDIENT:
                self.bus_belts[connection] = belt_type.generate_belt(
                    name = f"{connection.name}:BusBelt",
                    pos = pos + connection.pos + Vector(y = self.height - 1.0, z = 1.0),
                    yaw = Yaw.South,
                    length = self.height
                )
                self.bus_belts[connection][-1].connect_to_splitter(self.splitters[connection])
            elif connection.direction == FactoryBlockInterface.Direction.PRODUCT:
                
                self.bus_belts[connection] = belt_type.generate_belt(
                    name = f"{connection.name}:BusBelt",
                    pos = pos + connection.pos + Vector(z = 1.0),
                    yaw = Yaw.North,
                    length = self.height
                )
                self.splitters[connection].connect_to_belt(self.bus_belts[connection][0])
            else:
                raise ValueError(f"Unknown direction: {connection.direction} for router interface connection: {connection.name}")
    
    def generate_router_belts(self, pos, factory_router_interface, factory_block_interface, proliferator):
        self.router_belts = {}
        for block_connection in factory_block_interface:
            for router_connection in factory_router_interface:
                if block_connection.item_type == router_connection.item_type:
                    self.route_splitter_to_factory_line(pos, router_connection, block_connection, proliferator)
                    continue
                    
    def route_splitter_to_factory_line(self, pos, router_connection, block_connection, proliferator):
        initial_direction = Yaw.Unknown
        if block_connection.placement == FactoryBlockInterface.Placement.TOP:
            initial_direction = Yaw.North
        elif block_connection.placement == FactoryBlockInterface.Placement.BOTTOM:
            initial_direction = Yaw.South            
        else:
            raise ValueError(f"Unknown placement: {block_connection.placement} for block connection: {block_connection.name}")

        belt_type = ConveyorBelt.get_minimum_required_belt_type(block_connection.throughput)

        self.router_belts[block_connection] = ConveyorBelt.generate_belt(
            name = f"{block_connection.name}:RouterBelt",
            pos = pos + router_connection.pos,
            yaw = [initial_direction, Yaw.East],
            length = [2 + block_connection.belt_index, 5 + self.width - router_connection.pos.x],
            belt_type = belt_type
        )
        self.splitters[router_connection].connect_to_belt(self.router_belts[block_connection][0])

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
    
    factory_block_interface = [
        FactoryBlockInterface(
            name = "FactoryBlock",
            item_type = "IronOre",
            direction = INGREDIENT,
            placement = FactoryBlockInterface.Placement.BOTTOM,
            throughput = 6.0,
            belt_index = 0,
            proliferator = None
        ),
        FactoryBlockInterface(
            name = "FactoryBlock",
            item_type = "IronIngot",
            direction = PRODUCT,
            placement = FactoryBlockInterface.Placement.TOP,
            throughput = 20.0,
            belt_index = 0,
            proliferator = None
        ),
    ]

    router = FactoryRouter(pos, factory_router_interface, factory_block_interface, proliferator = None)
    print(f"BeltRouter created: {router}")

    blueprint = Blueprint()
    output_blueprint_string = blueprint.serialize(Building.buildings, blueprint_building_version = BlueprintBuildingV1)
    print(output_blueprint_string)