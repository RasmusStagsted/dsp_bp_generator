from dsp_bp_generator.utils import Vector, Yaw
from dsp_bp_generator.buildings import ConveyorBelt, Splitter
from dsp_bp_generator.enums import BuildingModel
from dsp_bp_generator.blueprint import Blueprint, BlueprintBuildingV1
from dsp_bp_generator.buildings import Building

from .factory_router_interface import FactoryRouterInterface, FactoryRouterBelt
from .factory_block_interface import FactoryBlockInterface, FactoryBlockBelt
from ..proliferator import ProliferatorNone

class FactoryRouter:
    """Handles the routing of routing belts and splitters for factory layouts."""

    def __init__(self, pos, factory_router_interface, factory_block_interface, height, splitter_offset, proliferator = None):
        self.width = factory_router_interface.get_width()
        self.height = height
        self.splitter_offset = splitter_offset
        self.generate_splitters(pos, factory_router_interface)
        self.generate_bus_belts(pos, factory_router_interface)
        self.generate_router_belts(pos + self.splitter_offset, factory_router_interface, factory_block_interface, proliferator)

    def generate_splitters(self, pos, factory_router_interface):
        self.splitters = {}
        for connection in factory_router_interface.belts:
            print(type(pos), type(connection.pos), type(self.splitter_offset))
            self.splitters[connection] = Splitter(
                name = f"{connection.name}",
                pos = pos + connection.pos + self.splitter_offset,
                yaw = Yaw.North,
                mode = BuildingModel.SplitterTwoLayerStraight
            )
            
    def generate_bus_belts(self, pos, factory_router_interface):
        self.bus_belts = {}
        for connection in factory_router_interface.belts:
            belt_type = ConveyorBelt.get_minimum_required_belt_type(connection.throughput)
            if connection.direction == FactoryBlockBelt.Direction.INGREDIENT:
                self.bus_belts[connection] = {
                    "top": belt_type.generate_belt(
                        name = f"{connection.name}:BusBelt",
                        pos = pos + connection.pos + Vector(z = 1.0),
                        yaw = Yaw.South,
                        length = -self.splitter_offset.y + 1
                    ),
                    "bottom": belt_type.generate_belt(
                        name = f"{connection.name}:BusBelt",
                        pos = pos + connection.pos + Vector(y = self.splitter_offset.y, z = 1.0),
                        yaw = Yaw.South,
                        length = self.height + self.splitter_offset.y - 2
                    ),
                }
                self.bus_belts[connection]["top"][-1].connect_to_splitter(self.splitters[connection])
                self.splitters[connection].connect_to_belt(self.bus_belts[connection]["bottom"][0])
                
            elif connection.direction == FactoryBlockBelt.Direction.PRODUCT:
                self.bus_belts[connection] = {
                    "top": belt_type.generate_belt(
                        name = f"{connection.name}:BusBelt",
                        pos = pos + connection.pos + Vector(y = self.splitter_offset.y, z = 1.0),
                        yaw = Yaw.North,
                        length = -self.splitter_offset.y + 1
                    ),
                    "bottom": belt_type.generate_belt(
                        name = f"{connection.name}:BusBelt",
                        pos = pos + connection.pos + Vector(y = -self.height + 3, z = 1.0),
                        yaw = Yaw.North,
                        length = self.height + self.splitter_offset.y - 2
                    ),
                }
                self.splitters[connection].connect_to_belt(self.bus_belts[connection]["top"][0])
                self.bus_belts[connection]["bottom"][-1].connect_to_splitter(self.splitters[connection])
            else:
                raise ValueError(f"Unknown direction: {connection.direction} for router interface connection: {connection.name}")
    
    def generate_router_belts(self, pos, factory_router_interface, factory_block_interface, proliferator):
        self.router_belts = {}
        for block_connection in factory_block_interface.belts:
            for router_connection in factory_router_interface.belts:
                if block_connection.item_type == router_connection.item_type:
                    if block_connection.direction == FactoryBlockBelt.Direction.INGREDIENT:
                        self.route_splitter_to_factory_line(pos, router_connection, block_connection, proliferator)
                    elif block_connection.direction == FactoryBlockBelt.Direction.PRODUCT:
                        self.route_factory_line_to_splitter(pos, router_connection, block_connection, proliferator)
                    else:
                        raise ValueError(f"Unknown direction: {block_connection.direction} for block connection: {block_connection.name}")
                    break
                elif router_connection == factory_router_interface.belts[-1]:
                    raise ValueError(f"Unable to find {block_connection.item_type} on the bus. {[belt.item_type for belt in factory_router_interface.belts]}")
                    
    def route_splitter_to_factory_line(self, pos, router_connection, block_connection, proliferator):
        initial_direction = Yaw.Unknown
        if block_connection.placement == FactoryBlockBelt.Placement.TOP:
            initial_direction = Yaw.North
        elif block_connection.placement == FactoryBlockBelt.Placement.BOTTOM:
            initial_direction = Yaw.South            
        else:
            raise ValueError(f"Unknown placement: {block_connection.placement} for block connection: {block_connection.name}")

        belt_type = ConveyorBelt.get_minimum_required_belt_type(block_connection.throughput)

        self.router_belts[block_connection] = ConveyorBelt.generate_belt(
            name = f"{block_connection.name}:RouterBelt",
            pos = pos + router_connection.pos,
            yaw = [initial_direction, Yaw.East],
            length = [2 + block_connection.belt_index, 3 + self.width - router_connection.pos.x],
            belt_type = belt_type
        )
        self.splitters[router_connection].connect_to_belt(self.router_belts[block_connection][0])

    def route_factory_line_to_splitter(self, pos, router_connection, block_connection, proliferator):
        end_direction = Yaw.Unknown
        if block_connection.placement == FactoryBlockBelt.Placement.TOP:
            end_direction = Yaw.South
        elif block_connection.placement == FactoryBlockBelt.Placement.BOTTOM:
            end_direction = Yaw.North            
        else:
            raise ValueError(f"Unknown placement: {block_connection.placement} for block connection: {block_connection.name}")
        
        belt_type = ConveyorBelt.get_minimum_required_belt_type(block_connection.throughput)
        
        y_dir = 1 if block_connection.placement == FactoryBlockBelt.Placement.TOP else -1
        start_pos = Vector(2 + self.width - router_connection.pos.x, (2 + block_connection.belt_index) * y_dir)
        self.router_belts[block_connection] = ConveyorBelt.generate_belt(
            name = f"{block_connection.name}:RouterBelt",
            pos = pos + router_connection.pos + start_pos,
            yaw = [Yaw.West, end_direction],
            length = [2 + self.width - router_connection.pos.x, 3 + block_connection.belt_index],
            belt_type = belt_type
        )
        self.router_belts[block_connection][-1].connect_to_splitter(self.splitters[router_connection])
        
if __name__ == "__main__":
    
    pos = Vector(x = 0, y = 0)
    
    INGREDIENT = FactoryRouterBelt.Direction.INGREDIENT
    PRODUCT = FactoryRouterBelt.Direction.PRODUCT
    
    factory_router_interface = FactoryRouterInterface(belts = [
        FactoryRouterBelt(
            name = "Belt router interface iron ore",
            item_type = "IronOre",
            direction = INGREDIENT,
            pos = Vector(0, 0),
            throughput = 6,
            proliferator = ProliferatorNone(),
        ),
        FactoryRouterBelt(
            name = "Belt router interface copper ore",
            item_type = "CopperOre",
            direction = INGREDIENT,
            pos = Vector(2, 0),
            throughput = 10,
            proliferator = ProliferatorNone(),
        ),
        FactoryRouterBelt(
            name = "Belt router interface iron ingot",
            item_type = "IronIngot",
            direction = PRODUCT,
            pos = Vector(4, 0),
            throughput = 20,
            proliferator = ProliferatorNone(),
        ),
    ])
    
    BOTTOM = FactoryBlockBelt.Placement.BOTTOM
    TOP = FactoryBlockBelt.Placement.TOP
    
    factory_block_interface = FactoryBlockInterface([
        FactoryBlockBelt(
            name = "FactoryBlock",
            item_type = "IronOre",
            direction = INGREDIENT,
            placement = BOTTOM,
            throughput = 6.0,
            belt_index = 0,
            proliferator = None
        ),
        FactoryBlockBelt(
            name = "FactoryBlock",
            item_type = "IronIngot",
            direction = PRODUCT,
            placement = TOP,
            throughput = 20.0,
            belt_index = 0,
            proliferator = None
        ),
    ])
    
    height = 10
    splitter_offset = Vector(y = -5)

    router = FactoryRouter(pos, factory_router_interface, factory_block_interface, height, splitter_offset, proliferator = None)
    print(f"BeltRouter created: {router}")

    blueprint = Blueprint()
    output_blueprint_string = blueprint.serialize(Building.buildings, blueprint_building_version = BlueprintBuildingV1)
    print(output_blueprint_string)