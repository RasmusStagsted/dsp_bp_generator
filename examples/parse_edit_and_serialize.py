import argparse
from dsp_bp_generator.blueprint import Blueprint
from dsp_bp_generator.utils import Vector

if __name__ == "__main__":
    
    # Parse the arguments
    parser = argparse.ArgumentParser(
        prog = "Blueprint parser",
        description = "Apllication to parse blueprints for the game Dyson Sphere program"
    )
    parser.add_argument("--input_file", "--if", type = str, help = "Input file where to read the input from (if not defined, the input will be read from standard input)")
    parser.add_argument("--output_file", "--of", type = str, help = "Output file where to save the output to (if not defined, the output will be written to standard output)")
    args = parser.parse_args()

    # Load the blueprint
    if args.input_file == None:
        print("Using standard input to read the blueprint:")
        input_blueprint_string = input("")
    else:
        print("Loading file:", args.input_file)
        with open(args.input_file, 'r') as file:
            input_blueprint_string = file.read()
    print("Input blueprint string:", input_blueprint_string)
    print()
    
    # Parse the blueprint
    bp = Blueprint()
    buildings = bp.parse(input_blueprint_string)
    
    # Validate hash
    assert bp.validate_hash(), "Could not validate hash"

    #########################
    # Change blueprint here #
    #########################

    # Move the building at index 0
    buildings[0].move_relative(Vector(x = 1))

    # Serialize the blueprint again
    output_blueprint_string = bp.serialize(buildings)
    
    # Validate hash
    assert bp.validate_hash(), "Could not validate hash"
    
    # Write parsed data
    if args.output_file == None:
        for building in buildings:
            print(building)
            print(output_blueprint_string)
    else:
        with open(args.output_file, "w") as file:
            for building in buildings:
                file.write(building.__str__())
            file.write(output_blueprint_string)