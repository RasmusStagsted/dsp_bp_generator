import Blueprint
from BlueprintStringHeader import BlueprintStringHeader
from BlueprintArea import BlueprintArea
from BlueprintHeader import BlueprintHeader
from BlueprintBuilding import BlueprintBuilding
from BlueprintBuildingHeader import BlueprintBuildingHeader
from FactoryLine import FactoryLine
from BeltRouter import BeltRouter
from FactorySection import FactorySection
import Buildings

import math

from utils import generate_belt


from recipes import recipes
from ItemEnum import Yaw, ItemEnum

raw_items = [
    ItemEnum.IronOre,
    ItemEnum.CopperOre,
    ItemEnum.SiliconOre,
    ItemEnum.TitaniumOre,
    ItemEnum.Stone,
    ItemEnum.Coal,
    ItemEnum.CrudeOil,
    ItemEnum.Water
]

class ItemFlow:

    def __init__(self, id, count_pr_sec):
        self.id = id
        self.count_pr_sec = count_pr_sec

    def get_ingredients(self, prolifirator = None):

        if prolifirator == "Mk.I":
            scale = 1/0.95
        elif prolifirator == "Mk.II":
            scale = 1/0.88
        elif prolifirator == "Mk.III":
            scale = 1/0.8
        else:
            scale = 1
            
        if self.id in raw_items:
            return []
        recipe = recipes[self.id]

        ingredients = []

        for input_item, input_item_count in recipe.input_items.items():
            ingredients.append(ItemFlow(input_item, input_item_count * self.count_pr_sec * scale / recipe.output_items[self.id]))

        return ingredients
    
    def get_waste_product(self):
        return []

class FactoryProcess:

    def __init__(self, input_count, output_count, time, tool):
        pass

class Factory:

    def __init__(self):
        self.prolifirator = None # Mk.I, Mk.II, Mk.III
        self.input_flow = []

    def set_tartget_output_flow(self, products, debug = False):

        ingredient_stack = products
        production_stack = []

        while len(ingredient_stack) > 0:
            ingredient = ingredient_stack.pop()
            # Add sub ingredients to stack
            for sub_ingredient in ingredient.get_ingredients(self.prolifirator):
                ingredient_stack.append(sub_ingredient)

            # Add to production stack
            index = -1
            for i in range(len(production_stack)):
                if production_stack[i].id == ingredient.id:
                    index = i
                    break
            if index != -1:
                ingredient_to_bump = production_stack.pop(index)
                production_stack.append(ingredient_to_bump)
                production_stack[-1].count_pr_sec += ingredient.count_pr_sec
            else:
                production_stack.append(ingredient)

        self.target_output_flow = production_stack[::-1] # Reverse list
        self.input_flow = []
        for flow in self.target_output_flow:
            if flow.id in raw_items:
                self.input_flow.append(flow)
                self.target_output_flow.remove(flow)

        if debug:
            print("Inputs stack")
            for item in self.input_flow:
                print(f"\t{ItemEnum(item.id).name}: {float(item.count_pr_sec)}/s")
            print("Outputs stack")
            for item in self.target_output_flow:
                print(f"\t{ItemEnum(item.id).name}: {float(item.count_pr_sec)}/s")

    def generate_factories(self, buildings, debug = False):
        self.main_belts = []
        for item in self.input_flow:
            self.main_belts.append(item)
        for item in self.target_output_flow:
            self.main_belts.append(item)
        
        if debug:
            print("Main belts:")
            for belt in self.main_belts:
                print(f"\t{ItemEnum(belt.id).name}, {belt.count_pr_sec}/s")
        
        self.factories = []
        input_count = len(self.input_flow)
        output_count = 0
        y = 0
        
        for product in self.target_output_flow:
            
            if recipes[product.id].tool == "Smelting Facility":
                factory_type = ItemEnum.Smelter
            elif recipes[product.id].tool == "Assembling machine":
                factory_type = ItemEnum.AssemblingMachineMkIII
                
            recipe_id = recipes[product.id].recipe_id
            assert recipe_id != None, "Recipe not supported"
                
            input_indicies = []
            for ingredient in product.get_ingredients(self.prolifirator):
                for i in range(len(self.main_belts)):
                    if self.main_belts[i].id == ingredient.id:
                        input_indicies.append(i)
            if debug:
                print("Generate factory section:")
                print(f"\tx: {0}")
                print(f"\ty: {y}")
                print(f"\tInputs: {input_count}")
                print(f"\tOutputs: {output_count}")
                print(f"\tBelt Selectors: {input_indicies}")
                print(f"\tProduct count: {1}")
                print(f"\tOutputs: {product.id.name}")
        
            self.factories.append(
                FactorySection(
                    buildings = buildings,
                    x = 0,
                    y = y,
                    input_count = input_count,
                    output_count = output_count,
                    selector_belts = input_indicies,
                    product_count = 1,
                    factory_type = factory_type,
                    recipe = recipe_id,
                    factory_count = math.ceil(product.count_pr_sec * recipes[product.id].time)
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

def generate_blueprint_string_header():
    return BlueprintStringHeader()

def generate_blueprint_header(size_x, size_y):
    return BlueprintHeader(size_x, size_y)

def generate_blueprint_areas(size_x, size_y):
    return [BlueprintArea(size_x, size_y)]

def generate_blueprint_building_header(building_count):
    return BlueprintBuildingHeader(building_count)

def generate_blueprint_buildings():

    buildings = []

    factory = Factory()

    output_flow = [ItemFlow(ItemEnum.MagneticCoil, 2.0)]
    factory.set_tartget_output_flow(output_flow, debug = False)
    factory.generate_factories(buildings, debug = False)

    return buildings, 20, 20

if __name__ == "__main__":
    
    buildings, size_x, size_y = generate_blueprint_buildings()
    
    blueprint_data = {
        "blueprint_string_header": generate_blueprint_string_header(),
        "blueprint_header": generate_blueprint_header(size_x, size_y),
        "blueprint_areas": generate_blueprint_areas(size_x, size_y),
        "blueprint_building_header": generate_blueprint_building_header(len(buildings)),
        "blueprint_buildings": buildings,
    }
    
    output_bp_str = Blueprint.serialize(**blueprint_data)
    print(output_bp_str)
