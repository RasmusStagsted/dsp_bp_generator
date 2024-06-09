import argparse
from dsp_bp.utils import Yaw, Vector
from dsp_bp.blueprint import Blueprint
from dsp_bp.factory_generator import Factory, ItemFlow, recipes
from dsp_bp.buildings import Building
import math
import argparse

if __name__ == "__main__":
    
    # Parse the arguments
    parser = argparse.ArgumentParser(
        prog = "Blueprint parser",
        description = "Apllication to parse blueprints for the game Dyson Sphere program"
    )
    parser.add_argument("--output_file", "--of", type = str, help = "Output file where to save the output to (if not defined, the output will be written to standard output)")
    args = parser.parse_args()

    # Generate the factory
    factory = Factory()
    output_flow = [ItemFlow("SorterMKI", 2.0)]
    factory.set_tartget_output_flow(output_flow, debug = True)
    factory.generate_factories(debug = True)
    blueprint = Blueprint()
    output_blueprint_string = blueprint.serialize(Building.buildings)

    # Write parsed data
    if args.output_file == None:
        print(output_blueprint_string)
    else:
        with open(args.output_file, "w") as file:
            file.write(output_blueprint_string)