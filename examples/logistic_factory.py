from dsp_bp_generator.utils import Vector
from dsp_bp_generator.blueprint import Blueprint
from dsp_bp_generator.blueprint import BlueprintBuildingV1
from dsp_bp_generator.factory_generator.recipes import Recipe
from dsp_bp_generator.enums import Item, AssemblingRecipe

from dsp_bp_generator import buildings
import argparse
import difflib
import sys

if __name__ == "__main__":
    
    # Parse the arguments
    parser = argparse.ArgumentParser(
        prog = "Blueprint parser",
        description = "Apllication to parse blueprints for the game Dyson Sphere program"
    )
    parser.add_argument("--output_file", "--of", type = str, help = "Output file where to save the output to (if not defined, the output will be written to standard output)")
    parser.add_argument("--item", required = True, type = str, help = "Output item (name from the list in 'recipes.yaml')")
    args = parser.parse_args()

    product_string = args.item

    if not product_string in Recipe.recipes.keys():
        closest_match = difflib.get_close_matches(product_string, Recipe.recipes.keys(), n=1, cutoff=0.6)
        if closest_match:
            print(f"{product_string} not found, did you mean '{closest_match[0]}'?")
            sys.exit(0)
        else:
            print(f"{product_string} not found")
            sys.exit(0)

    product = Recipe.recipes[product_string]
    ingredients = product["input_items"]

    # This is a small example of how to generate a simple logistic factory
    input_depot_positions = [Vector(-4, 2), Vector(-4, -2), Vector(4, 2), Vector(4, -2), Vector(0, -4)]
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
            name = f"Input depot {ingredient}",
            pos = input_depot_positions[i],
            blocked_slots = 29
        )
        depot.create_logistic_distributor(
            name = f"Distributor {ingredient}",
            filter_id = Item[ingredient],
            chargin_power = 150000,
            icarus_mode = buildings.LogisticDistributor.IcarusMode.CollectFromIcarus,
            distributor_mode = buildings.LogisticDistributor.DistributorMode.RequestFromDistributors
        )
        
        # Connect input_depot to assembler
        sorter = buildings.SorterMKI.generate_sorter_from_building_to_building(
            name = f"Input sorter {ingredient}",
            building_1 = depot,
            building_2 = assembler
        )

    # Create the output depot
    output_depot = buildings.DepotMKI(
        name = "Output depot",
        pos = output_depot_position,
        blocked_slots = 29
    )
    
    output_depot.create_logistic_distributor(
        name = f"Distributor {ingredient}",
        filter_id = Item[product_string],
        chargin_power = 150000,
        icarus_mode = buildings.LogisticDistributor.IcarusMode.ProvideToIcarus,
        distributor_mode = buildings.LogisticDistributor.DistributorMode.ProvideToDistributors
    )
        
    # Connect the assembler to the output depot
    sorter = buildings.SorterMKI.generate_sorter_from_building_to_building(
        name = "output sorter",
        building_1 = assembler,
        building_2 = output_depot
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
            file.write(output_blueprint_string)
            print(output_blueprint_string)
            
            
            
            
!blueprint 0eNrNmt1uozAQhd/F12SFMfaM8yqrqkopbdGmJBtItVWVd1/SNA3tEjxnrvaqP4GP0RyOzxD8Zu7W+3q7a9reLN9MU23azix/vpmueWxX6+P/+tdtbZam6etnk5l29Xz8a7dq1uaQmaa9r/+YpT3cZKZu+6Zv6tP573+83rb757t6NxzweWa1373U94t3QGa2m244Z9MeLzRwCldm5tUsF9YWA/2+2dXV6WM6ZP9Ai09ot7/r+tX7kRNMPjPLwwTFySjezlJKGSX4WYqXUTifpQQZJc73hWSSOVtckayYgPKltH7gPT71V++EeMbaNDaKsaUFsDaXcx3CtXKuR7iFnEsI18m5iGy2FHM9pJuXcyHdgpwL6UZyLqSb3G4e0k3ut4DoVsj9FhDdCrnfAqJbIfdbQHQr5H4LiG6F3G8E6Sb3G0G6yf1GkG5yvxGkm9xvBOkm9xsjujm53xjRzcn9xohuTu43RnRzcr8xopuT+y1Cusn9FiHd5H6LkG5yv0VIN7nfIqSb2G8uR3QrczkX0a20ci6iW1nIuYhu5dhvq+rXomm7etcPH009B/w4l5wPv36Fl1Pwi+nWm8em65tqUT3V3VB6/Xs//ExehofLTIH9l8ffxccj8tQD50zJYYoc5P0oLdoPAuA5CmdNs8eXudbsqALbJNjnQDsKsB3eqqou0lUXQNUBrdqpqqZ01Sorjuu/BvZAOwhtB+JGRuGkakl6dfI6J3IaHIF2oIt1yDVVe5esOlh51WOcrOpCVbVPV61yoi/T4BJoR4m2A3DjuAkyeFC1JL2GBCAXPbqkBpUbQzq+gioXQzpwCcjFgI4JBLgxoAMOqdwY0msIqdwY0mlOgBsDOoMQ4MaArnwEZGNAg5dU2RjScwgxUDWa6ATkY0DzkVX5GNLjAqsm1ZAeFxiYVAldR1jlSEqvfqyaVCmd6OxV4HSiM+BEQkOXgWwkdFxgVTZS2uasykZKjwoRyEZCV70IZCOhc0hUZSOn55AIfIXDaKJHlRs5HbxR5UZOjwoRcCOjoRsBNzI6LkSVGzm9QEUgFxldQ2yuCkZO55fNVcnIUUAGopEj3BHEkQzTVZaMuaArKk9GKyADpow53BHAldHCdJUt47e7MDMfR98+NOvhlNPerPOmrc8rtPtqXa92i4d9ffw+u9rsj9vB3LGuj2Mvd261WY2OGXx4uJms/+L+h9VQ9Vxz4Fvdaszvcv+/NGe0/yfRnC9FC5tzKef4zqZddP1mO/fGJo/f3thk5rxpbGnM5CWc7E2Iy+ffhNxkp22Fy9EuxMy8DFKcCmFbUhkp0GBlHw6Hv2ElKu0=