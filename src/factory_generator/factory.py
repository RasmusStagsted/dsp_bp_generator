from .recipes import recipes
from ..ItemEnum import ItemEnum
from .factory_section import FactorySection
from ..utils import Pos
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
            for ingredient in item.get_ingredients(self.prolifirator):
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
            if recipes[flow.name] == None:
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
        self.main_belts = []
        for item in self.input_flow:
            self.main_belts.append(item)
        for item in self.target_output_flow:
            self.main_belts.append(item)
        
        if debug:
            print("Main belts:")
            for belt in self.main_belts:
                print(f"\t{belt.name}, {belt.count_pr_sec}/s")
        
        self.factories = []
        input_count = len(self.input_flow)
        output_count = 0
        y = 0
        
        for product in self.target_output_flow:
            if recipes[product.name] == None:
                continue
            print(recipes[product.name])
            if recipes[product.name]["tool"] == "Smelting Facility":
                factory_type = ItemEnum.ArcSmelter
            elif recipes[product.name]["tool"] == "Assembling machine":
                factory_type = ItemEnum.AssemblingMachineMkIII
            
            recipe_id = recipes[product.name]["recipe_id"]
            assert recipe_id != None, "Recipe not supported"
            
            input_indicies = []
            for ingredient in product.get_ingredients(self.prolifirator):
                for i in range(len(self.main_belts)):
                    if self.main_belts[i].name == ingredient.name:
                        input_indicies.append(i)
            if debug:
                print("Generate factory section:")
                print(f"\tx: {0}")
                print(f"\ty: {y}")
                print(f"\tInputs: {input_count}")
                print(f"\tOutputs: {output_count}")
                print(f"\tBelt Selectors: {input_indicies}")
                print(f"\tProduct count: {1}")
                print(f"\tOutputs: {product.name}")
            self.factories.append(
                FactorySection(
                    pos = Pos(0, y),
                    input_count = input_count,
                    output_count = output_count,
                    selector_belts = input_indicies,
                    product_count = 1,
                    factory_type = factory_type,
                    recipe = recipe_id,
                    factory_count = ceil(product.count_pr_sec * recipes[product.name]["time"])
                )
            )
            
            if len(self.factories) > 1:
                self.factories[-2].connect_to_section(self.factories[-1])
            
            output_count += 1
            factory_height = 3
            y += factory_height + len(input_indicies) + 1

    def generate_blueprint(self):
        for factory_process in self.factory_processes:
            print(factory_process)
