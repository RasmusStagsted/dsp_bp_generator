import Buildings
from ItemEnum import Yaw
from utils import *

class BeltRouter:

    def __init__(self, x, y, input_count, output_count, product_count, selector_belt_indicies, belt_length):
        self.generate_splitters(x, y, input_count, output_count, product_count)
        self.generate_input_belts(x, y, input_count, belt_length)
        self.generate_output_and_product_belts(x, y, input_count, output_count, product_count, belt_length)
        self.generate_selector_belts(x, y, input_count, output_count, product_count, selector_belt_indicies)
        self.generate_production_belts(x, y, input_count, output_count, product_count)
        
    def generate_splitters(self, x, y, input_count, output_count, product_count):
        self.input_splitters = []
        for i in range(input_count):
            input_splitter = Buildings.Splitter(x + 2 * i, y, 0, Yaw.North)
            self.input_splitters.append(input_splitter)
        self.output_splitters = []
        for i in range(output_count):
            output_splitter = Buildings.Splitter(x + 2 * (i + input_count), y, 0, Yaw.North)
            self.output_splitters.append(output_splitter)
        self.product_splitters = []
        for i in range(product_count):
            product_splitter = Buildings.Splitter(x + 2 * (i + input_count + output_count), y, 0, Yaw.North)
            self.product_splitters.append(product_splitter)
        self.splitters = self.input_splitters + self.output_splitters + self.product_splitters
        
    def generate_input_belts(self, x, y, input_count, belt_length):
        self.input_belts = []
        for i in range(input_count):
            belts = generate_belt(x + 2 * i, y + belt_length - 1, 1, Yaw.South, belt_length)
            belt_start = belts[0]
            belt_end = belts[-1]
            self.input_belts.append(belt_start)
            ### Connect belts to splitters
            splitter = self.input_splitters[i]
            belt_end.connect_to_splitter(splitter)
            
            
    def generate_output_and_product_belts(self, x, y, input_count, output_count, product_count, belt_length):
        self.output_belts = []
        for i in range(output_count):
            belts = generate_belt(x + 2 * (i + input_count), y, 1, Yaw.North, belt_length)
            belt_start = belts[0]
            belt_end = belts[-1]
            ## Connect belts to splitters
            self.output_belts.append(belt_end)
            splitter = self.output_splitters[i]
            splitter.connect_to_belt(belt_start)
        for i in range(product_count):
            belts = generate_belt(x + 2 * (i + input_count + output_count), y, 1, Yaw.North, belt_length)
            belt_start = belts[0]
            belt_end = belts[-1]
            ## Connect belts to splitters
            self.output_belts.append(belt_end)
            splitter = self.product_splitters[i]
            splitter.connect_to_belt(belt_start)
            
    def generate_selector_belts(self, x, y, input_count, output_count, product_count, selector_belt_indicies):
        self.selector_belts = []
        for i in range(len(selector_belt_indicies)):
            ### Generate north bound belts
            belts = generate_belt(x + 2 * selector_belt_indicies[i], y, 0.0, Yaw.North, 1 + len(selector_belt_indicies) - i)
            north_belt_start = belts[0]
            north_belt_end = belts[-1]
            ### Connect north bound belts to splitter
            splitter = self.splitters[selector_belt_indicies[i]]
            splitter.connect_to_belt(north_belt_start)
            ### Generate east bound belts            
            belts = generate_belt(x + 2 * selector_belt_indicies[i] + 1, y + 1 + len(selector_belt_indicies) - i, 0, Yaw.East, (input_count + output_count + product_count - selector_belt_indicies[i]) * 2)
            east_belt_start = belts[0]
            east_belt_end = belts[-1]
            self.selector_belts.append(east_belt_end)
            # TODO remove function "connect_cornor_belt" and implement it in Belt.connect_to_belt
            connect_cornor_belt(north_belt_end, east_belt_start)
        
    def generate_production_belts(self, x, y, input_count, output_count, product_count):

        self.production_belts = []
        for i in range(product_count):
            ### Generate west bounding belt
            belts = generate_belt(x + 2 * (input_count + output_count + product_count), y - 2 - i, 0.0, Yaw.West, 2 + 2 * i)
            west_belt_start = belts[0]
            west_belt_end = belts[-1]
            ### Generate north bounding belt
            belts = generate_belt(x + 2 * (input_count + output_count + product_count) - 2 * (i + 1), y - 1 - i, 0, Yaw.North, i + 2)
            north_belt_start = belts[0]
            north_belt_end = belts[-1]
            # Connect cornor
            # TODO remove function "connect_cornor_belt" and implement it in Belt.connect_to_belt
            connect_cornor_belt(west_belt_end, north_belt_start)
            # Connect belts to splitters
            splitter = self.product_splitters[-i]
            
            # TODO
            north_belt_end.connect_to_splitter(splitter)            
            self.production_belts.append(west_belt_start)