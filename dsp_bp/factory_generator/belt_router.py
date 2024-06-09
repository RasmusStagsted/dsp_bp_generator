#import Buildings
from ..utils import Pos, Yaw
from ..buildings import ConveyorBeltMKI, Splitter

class BeltRouter:

    def __init__(self, pos, input_count, output_count, product_count, selector_belt_indicies, belt_length):
        self.generate_splitters(pos, input_count, output_count, product_count)
        self.generate_input_belts(pos, input_count, belt_length)
        self.generate_output_belts(pos, input_count, output_count, product_count, belt_length)
        self.generate_selector_belts(pos, input_count, output_count, product_count, selector_belt_indicies)
        self.generate_production_belts(pos, input_count, output_count, product_count)
        
    def generate_splitters(self, pos, input_count, output_count, product_count):
        self.input_splitters = []
        for i in range(input_count):
            temp_pos = Pos(pos.x + 2 * i, pos.y)
            input_splitter = Splitter(f"InputSplitter:{i}", temp_pos, Yaw.North)
            self.input_splitters.append(input_splitter)
        self.output_splitters = []
        for i in range(output_count):
            temp_pos = Pos(pos.x + 2 * (i + input_count), pos.y)
            output_splitter = Splitter(f"OutputSplitter:{i}", temp_pos, Yaw.North)
            self.output_splitters.append(output_splitter)
        self.product_splitters = []
        for i in range(product_count):
            temp_pos = Pos(pos.x + 2 * (i + input_count + output_count), pos.y)
            product_splitter = Splitter(f"ProductSplitter:{i}", temp_pos, Yaw.North)
            self.product_splitters.append(product_splitter)
        self.splitters = self.input_splitters + self.output_splitters + self.product_splitters
        
    def generate_input_belts(self, pos, input_count, belt_length):
        self.input_belts = []
        for i in range(input_count):
            temp_pos = Pos(pos.x + 2 * i, pos.y + belt_length - 1, 1)
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
            temp_pos = Pos(pos.x + 2 * (i + input_count), pos.y, 1)
            belts = ConveyorBeltMKI.generate_belt(f"BeltRouter:OutputBelt:{i}", temp_pos, Yaw.North, belt_length)
            belt_start = belts[0]
            belt_end = belts[-1]
            ## Connect belts to splitters
            self.output_belts.append(belt_end)
            splitter = self.output_splitters[i]
            splitter.connect_to_belt(belt_start)
        for i in range(product_count):
            temp_pos = Pos(pos.x + 2 * (i + input_count + output_count), pos.y, 1)
            belts = ConveyorBeltMKI.generate_belt(f"BeltRouter:ProductBelt:{i}", temp_pos, Yaw.North, belt_length)
            belt_start = belts[0]
            belt_end = belts[-1]
            ## Connect belts to splitters
            self.output_belts.append(belt_end)
            splitter = self.product_splitters[i]
            splitter.connect_to_belt(belt_start)
            
    def generate_selector_belts(self, pos, input_count, output_count, product_count, selector_belt_indicies):
        self.selector_belts = []
        for i in range(len(selector_belt_indicies)):
            ### Generate belt
            start_pos = Pos(pos.x + 2 * selector_belt_indicies[i], pos.y)
            yaw = [Yaw.North, Yaw.East]
            length = [1 + len(selector_belt_indicies) - i, 1 + (input_count + output_count + product_count - selector_belt_indicies[i]) * 2]
            belts = ConveyorBeltMKI.generate_belt(f"BeltRouter:SelectorBelts:{i}", start_pos, yaw, length)
            belt_start = belts[0]
            belt_end = belts[-1]
            ### Connect belt to splitter
            splitter = self.splitters[selector_belt_indicies[i]]
            splitter.connect_to_belt(belt_start)
            self.selector_belts.append(belt_end)
        
    def generate_production_belts(self, pos, input_count, output_count, product_count):

        self.production_belts = []
        for i in range(product_count):
            ### Generate west bounding belt
            temp_pos = Pos(pos.x + 2 * (input_count + output_count + product_count), pos.y - 2 - i)
            yaw = [Yaw.West, Yaw.North]
            length = [2 + 2 * i, 3 + i]
            belts = ConveyorBeltMKI.generate_belt(f"BeltRouter:ProductionBelt:{i}", temp_pos, yaw, length)
            belt_start = belts[0]
            belt_end = belts[-1]
            ### Connect belt to splitter
            splitter = self.product_splitters[-i]
            belt_end.connect_to_splitter(splitter)
            self.production_belts.append(belt_start)