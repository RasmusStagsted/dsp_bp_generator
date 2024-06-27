#import Buildings
from ..utils import Vector, Yaw
from ..buildings import ConveyorBeltMKI, Splitter
from ..enums import BuildingModel

class BeltRouter:

    def __init__(self, pos, input_count, output_count, product_count, belt_routing, belt_length):
        self.width = 2 * (input_count + output_count + product_count)
        
        self.generate_splitters(pos, input_count, output_count, product_count)
        self.generate_input_belts(pos, input_count, belt_length)
        self.generate_output_belts(pos, input_count, output_count, product_count, belt_length)
        self.generate_router_belts(pos, belt_routing)
        
    def generate_splitters(self, pos, input_count, output_count, product_count):
        self.input_splitters = []
        for i in range(input_count):
            temp_pos = Vector(pos.x + 2 * i, pos.y)
            input_splitter = Splitter(
                name = f"InputSplitter:{i}",
                pos = temp_pos,
                yaw = Yaw.North,
                mode = BuildingModel.SplitterTwoLayerStraight
            )
            self.input_splitters.append(input_splitter)
        self.output_splitters = []
        for i in range(output_count):
            temp_pos = Vector(pos.x + 2 * (i + input_count), pos.y)
            output_splitter = Splitter(
                name = f"OutputSplitter:{i}",
                pos = temp_pos,
                yaw = Yaw.North,
                mode = BuildingModel.SplitterTwoLayerStraight
            )
            self.output_splitters.append(output_splitter)
        self.product_splitters = []
        for i in range(product_count):
            temp_pos = Vector(pos.x + 2 * (i + input_count + output_count), pos.y)
            product_splitter = Splitter(
                name = f"ProductSplitter:{i}",
                pos = temp_pos,
                yaw = Yaw.North,
                mode = BuildingModel.SplitterTwoLayerStraight
            )
            self.product_splitters.append(product_splitter)
        self.splitters = self.input_splitters + self.output_splitters + self.product_splitters
        
    def generate_input_belts(self, pos, input_count, belt_length):
        self.input_belts = []
        for i in range(input_count):
            temp_pos = Vector(pos.x + 2 * i, pos.y + belt_length - 1, 1)
            belts = ConveyorBeltMKI.generate_belt(f"BeltRouter:InputBelt:{i}", temp_pos, Yaw.South, belt_length)
            belt_start = belts[0]
            belt_end = belts[-1]
            self.input_belts.append(belt_start)
            ### Connect belts to splitters
            splitter = self.input_splitters[i]
            belt_end.connect_to_splitter(splitter)
            
    def generate_output_belts(self, pos, input_count, output_count, product_count, belt_length):
        self.output_belts = []
        for i in range(output_count):
            temp_pos = Vector(pos.x + 2 * (i + input_count), pos.y, 1)
            belts = ConveyorBeltMKI.generate_belt(f"BeltRouter:OutputBelt:{i}", temp_pos, Yaw.North, belt_length)
            belt_start = belts[0]
            belt_end = belts[-1]
            ## Connect belts to splitters
            self.output_belts.append(belt_end)
            splitter = self.output_splitters[i]
            splitter.connect_to_belt(belt_start)
        for i in range(product_count):
            temp_pos = Vector(pos.x + 2 * (i + input_count + output_count), pos.y, 1)
            belts = ConveyorBeltMKI.generate_belt(f"BeltRouter:ProductBelt:{i}", temp_pos, Yaw.North, belt_length)
            belt_start = belts[0]
            belt_end = belts[-1]
            ## Connect belts to splitters
            self.output_belts.append(belt_end)
            splitter = self.product_splitters[i]
            splitter.connect_to_belt(belt_start)
    
    def generate_router_belts(self, pos, routes):
        self.product_belts = []
        self.selector_belts = []
        for route in routes:
            if route.direction == "product":
                if route.placement == "top":
                    start_pos = pos + Vector(self.width, 2 + route.belt_index)
                    yaw = [Yaw.West, Yaw.South]
                else:
                    start_pos = pos + Vector(self.width - 1, -2 - route.belt_index)
                    yaw = [Yaw.West, Yaw.North]
                name = "Productbelt"
                length = [self.width - 1 - 2 * route.router_index, 3 + route.belt_index]
                self.product_belts.append(ConveyorBeltMKI.generate_belt(name, start_pos, yaw, length))
                splitter = self.splitters[route.router_index]
                self.product_belts[-1][-1].connect_to_splitter(splitter)
                
                for i in range(route.belt_index):
                    self.product_belts[-1][-2-i].move_relative(Vector(z = 0.0))
                
                # Raise belt to allow crossing belts to go under
                for i in range(route.belt_index):
                    self.product_belts[-1][-3 - i].move_relative(Vector(z = 0.3))
                
            elif route.direction == "ingredient":
                if route.placement == "top":
                    start_pos = pos + Vector(route.router_index * 2, 0)
                    yaw = [Yaw.North, Yaw.East]
                else:
                    start_pos = pos + Vector(route.router_index * 2, 0)
                    yaw = [Yaw.South, Yaw.East]
                
                name = "SelectorBelt",
                length = [2 + route.belt_index, self.width - 2 * route.router_index]
                self.selector_belts.append(ConveyorBeltMKI.generate_belt(name, start_pos, yaw, length))
                splitter = self.splitters[route.router_index]
                splitter.connect_to_belt(self.selector_belts[-1][0])
                
                # Raise belt to allow crossing belts to go under
                for i in range(route.belt_index):
                    self.selector_belts[-1][2 + i].move_relative(Vector(z = 0.3))
