from .recipes import Recipe
from ..enums import Item
from .factory_section import FactorySection
from ..buildings import ArcSmelter, AssemblingMachineMKI, OilRefinary, ChemicalPlant, MatrixLab
from ..utils import Vector
from math import ceil

class Factory:

    def __init__(self):
        self.prolifirator = None # Mk.I, Mk.II, Mk.III
        self.input_flow = []

    def set_tartget_output_flow(self, products, debug = False):

        requirement_stack = products
        production_stack = []

        while len(requirement_stack) > 0:
            
            item = requirement_stack.pop()
            
            # Add ingredients to stack
            for ingredient in item.get_needed_ingredients(self.prolifirator):
                requirement_stack.append(ingredient)

            # Add item to production stack
            index = -1
            for i in range(len(production_stack)):
                if production_stack[i].name == item.name:
                    index = i
                    break
            if index != -1:
                ingredient_to_bump = production_stack.pop(index)
                ingredient_to_bump.count_pr_sec += item.count_pr_sec
                production_stack.append(ingredient_to_bump)
            else:
                production_stack.append(item)

        self.target_output_flow = production_stack[::-1] # Reverse list
        self.input_flow = []
        for flow in self.target_output_flow:
            if Recipe.recipes[flow.name] == None:
                self.input_flow.append(flow)
                self.target_output_flow.remove(flow)

        if debug:
            print("Inputs stack")
            for item in self.input_flow:
                print(f"\t{item.name}: {float(item.count_pr_sec)}/s")
            print("Outputs stack")
            for item in self.target_output_flow:
                print(f"\t{item.name}: {float(item.count_pr_sec)}/s")

    def generate_factories(self, debug = False):
        
        # Define main belt
        self.main_belts = []
        for item in self.input_flow:
            self.main_belts.append(item)
        for item in self.target_output_flow:
            self.main_belts.append(item)
        
        # Print debug for main belt
        if debug:
            print("Main belts:")
            for belt in self.main_belts:
                print(f"\t{belt.name}, {belt.count_pr_sec}/s")


        self.factories = []
        input_count = len(self.input_flow)
        output_count = 0
        y = 0
        
        for product in self.target_output_flow:
            
            recipe = Recipe.select(product.name)

            # If the product is a raw material, skip it
            if Recipe.recipes[product.name] == None:
                continue
            self.factories.append(
                FactorySection(
                    pos = Vector(0, y),
                    input_count = input_count,
                    output_count = output_count,
                    main_belts = self.main_belts,
                    product = product,
                    recipe = recipe
                )
            )
            
            if len(self.factories) > 1:
                self.factories[-2].connect_to_section(self.factories[-1])
            
            output_count += self.factories[-1].product_count
            y += self.factories[-1].height

    def get_factory(self, factory_type):
        factories = {
            "Smelting Facility": ArcSmelter,
            "Assembling machine": AssemblingMachineMKI,
            "Refining Facility": OilRefinary,
            "Chemical Facility": ChemicalPlant,
            "Matrix Lab": MatrixLab
        }
        return factories[factory_type]

    def generate_blueprint(self):
        pass
