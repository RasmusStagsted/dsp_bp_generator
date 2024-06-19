from dsp_bp.utils import Yaw, Vector
from dsp_bp.blueprint import Blueprint
from dsp_bp.blueprint import BlueprintBuildingV1
from dsp_bp.factory_generator.recipes import Recipe
from dsp_bp.enums import Item, AssemblingRecipe

from dsp_bp import buildings
import argparse

if __name__ == "__main__":
    
    # Parse the arguments
    parser = argparse.ArgumentParser(
        prog = "Blueprint parser",
        description = "Apllication to parse blueprints for the game Dyson Sphere program"
    )
    parser.add_argument("--output_file", "--of", type = str, help = "Output file where to save the output to (if not defined, the output will be written to standard output)")
    parser.add_argument("--item", required = True, type = str, help = "Output item")
    args = parser.parse_args()

    product_string = args.item

    product = Recipe.recipes[product_string]
    ingredients = product["input_items"]

    # This is a small example of how to generate a simple logistic factory
    input_depot_positions = [Vector(-4, 2), Vector(-4, -2), Vector(0, -4), Vector(4, 0)]
    output_depot_position = Vector(0, 4)

    # Create the assembler
    assembler = buildings.AssemblingMachineMKI(
        name = "Factory",
        pos = Vector(0, 0),
        recipe_id = AssemblingRecipe[product_string]
    )
    # Create the input depots
    for i, ingredient in enumerate(ingredients):
        # Create input_depot
        depot = buildings.DepotMKI(
            f"Input depot {ingredient}",
            input_depot_positions[i],
            blocked_slots = 29
        )
        print(ingredient)
        print(Item[ingredient])
        depot.create_logistic_distributor(
            name = f"Distributor {ingredient}",
            filter_id = Item[ingredient],
            chargin_power = 150000,
            icarus_mode = buildings.LogisticDistributor.IcarusMode.CollectFromIcarus,
            distributor_mode = buildings.LogisticDistributor.DistributorMode.RequestFromDistributors
        )
        
        # Connect input_depot to assembler
        sorter = buildings.SorterMKI.generate_sorter_from_factory_to_factory(
            name = f"Input sorter {ingredient}",
            factory_1 = depot,
            factory_2 = assembler
        )

    # Create the output depot
    output_depot = buildings.DepotMKI(
        name = "Output depot",
        pos = output_depot_position,
        blocked_slots = 29
    )
    print(product_string)
    print(Item[product_string])
    
    output_depot.create_logistic_distributor(
        name = f"Distributor {ingredient}",
        filter_id = Item[product_string],
        chargin_power = 150000,
        icarus_mode = buildings.LogisticDistributor.IcarusMode.ProvideToIcarus,
        distributor_mode = buildings.LogisticDistributor.DistributorMode.ProvideToDistributors
    )
        
    # Connect the assembler to the output depot
    sorter = buildings.SorterMKI.generate_sorter_from_factory_to_factory(
        "output sorter",
        assembler,
        output_depot
    )
    
    # Generate the blueprint
    blueprint = Blueprint()
    output_blueprint_string = blueprint.serialize(buildings.Building.buildings, blueprint_building_version = BlueprintBuildingV1)

    # Write parsed data
    if args.output_file == None:
        for building in buildings.Building.buildings:
            print(building)
        print(output_blueprint_string)
    else:
        with open(args.output_file, "w") as file:
            for building in buildings.Building.buildings:
                file.write(building.__str__())
            file.write(output_blueprint_string)
            print(output_blueprint_string)