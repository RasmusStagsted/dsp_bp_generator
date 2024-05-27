import Buildings
from ItemEnum import Yaw
from utils import *

class BeltRouter:

    def __init__(self, buildings, x, y, input_count, output_count, product_count, selector_belt_indicies, belt_length):
        
        ## Generate Splitters
        self.input_splitters = []
        for i in range(input_count):
            buildings.append(
                Buildings.Splitter(len(buildings), x + 2 * i, y, 0, Yaw.North)
            )
            self.input_splitters.append(buildings[-1])
        self.output_splitters = []
        for i in range(output_count):
            buildings.append(
                Buildings.Splitter(len(buildings), x + 2 * (i + input_count), y, 0, Yaw.North)
            )
            self.output_splitters.append(buildings[-1])
        self.product_splitters = []
        for i in range(product_count):
            buildings.append(
                Buildings.Splitter(len(buildings), x + 2 * (i + input_count + output_count), y, 0, Yaw.North)
            )
            self.product_splitters.append(buildings[-1])
        self.splitters = self.input_splitters + self.output_splitters + self.product_splitters
        
        ## Generate input belts
        self.input_belts = []
        for i in range(input_count):
            belts = generate_belt(buildings, x + 2 * i, y + belt_length - 1, 1, Yaw.South, belt_length)
            belt_start = belts[0]
            belt_end = belts[-1]
            self.input_belts.append(belt_start)
            ### Connect belts to splitters
            splitter = self.input_splitters[i]
            belt_end.connect_to_splitter(splitter)
            
            
        ## Generate output- and product belts
        self.output_belts = []
        for i in range(output_count):
            belts = generate_belt(buildings, x + 2 * (i + input_count), y, 1, Yaw.North, belt_length)
            belt_start = belts[0]
            belt_end = belts[-1]
            ## Connect belts to splitters
            self.output_belts.append(belt_end)
            splitter = self.output_splitters[i]
            splitter.connect_to_belt(belt_start)
        for i in range(product_count):
            belts = generate_belt(buildings, x + 2 * (i + input_count + output_count), y, 1, Yaw.North, belt_length)
            belt_start = belts[0]
            belt_end = belts[-1]
            ## Connect belts to splitters
            self.output_belts.append(belt_end)
            splitter = self.product_splitters[i]
            splitter.connect_to_belt(belt_start)
            
        ## Generate selector belts
        self.selector_belts = []
        for i in range(len(selector_belt_indicies)):
            ### Generate north bound belts
            belts = generate_belt(buildings, x + 2 * selector_belt_indicies[i], y, 0.0, Yaw.North, 1 + len(selector_belt_indicies) - i)
            north_belt_start = belts[0]
            north_belt_end = belts[-1]
            ### Connect north bound belts to splitter
            splitter = self.splitters[selector_belt_indicies[i]]
            splitter.connect_to_belt(north_belt_start)
            ### Generate east bound belts            
            belts = generate_belt(buildings, x + 2 * selector_belt_indicies[i] + 1, y + 1 + len(selector_belt_indicies) - i, 0, Yaw.East, (input_count + output_count + product_count - selector_belt_indicies[i]) * 2)
            east_belt_start = belts[0]
            east_belt_end = belts[-1]
            self.selector_belts.append(east_belt_end)
            # TODO remove function "connect_cornor_belt" and implement it in Belt.connect_to_belt
            connect_cornor_belt(buildings, north_belt_end, east_belt_start)
        
        ## Generate production belts
        self.production_belts = []
        for i in range(product_count):
            ### Generate west bounding belt
            belts = generate_belt(buildings, x + 2 * (input_count + output_count + product_count), y - 2 - i, 0.0, Yaw.West, 2 + 2 * i)
            west_belt_start = belts[0]
            west_belt_end = belts[-1]
            ### Generate north bounding belt
            belts = generate_belt(buildings, x + 2 * (input_count + output_count + product_count) - 2 * (i + 1), y - 1 - i, 0, Yaw.North, i + 2)
            north_belt_start = belts[0]
            north_belt_end = belts[-1]
            # Connect cornor
            # TODO remove function "connect_cornor_belt" and implement it in Belt.connect_to_belt
            connect_cornor_belt(buildings, west_belt_end, north_belt_start)
            # Connect belts to splitters
            splitter = self.product_splitters[-i]
            
            # TODO
            north_belt_end.connect_to_splitter(splitter)            
            self.production_belts.append(west_belt_start)