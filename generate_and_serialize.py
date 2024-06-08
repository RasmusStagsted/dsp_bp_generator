from src.utils import Yaw, Pos
from src.blueprint import Blueprint
from src.blueprint import BlueprintStringHeader
from src.blueprint import BlueprintHeader
from src.blueprint import BlueprintArea
from src.blueprint import BlueprintBuildingHeader
from src.blueprint import BlueprintBuildingV1

from src import buildings
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

    # This is a small example of a simple blueprint connecting
    # a belt of three pieces to an assembler using a sorter
    #
    # Belt coordinates are 0,3 1,3 and 2,3
    # Assembler coordinate = 1,1
    # The sorter has two coordinates. One for pickup-(1,3) and one for drop location (1,2)
    #             ┌─────┐
    #    ┌───────┬┼─────┼┬───────┐
    #    │       ││     ││       │
    #  3 │   →   ││  →  ││   →   │
    #    │       ││     ││       │
    #    └───────┴┼─────┼┘───────┘
    #    ┌───────┬┼─────┼┬───────┐
    #    │       ││     ││       │
    #  2 │       ││  ↓  ││       │
    #    │       │└─────┘│       │
    #    ├───────┼───────┼───────┤
    #    │       │       │       │
    #  1 │       │       │       │
    #    │       │       │       │
    #    ├───────┼───────┼───────┤
    #    │       │       │       │
    #  0 │       │       │       │
    #    │       │       │       │
    #    └───────┴───────┴───────┘
    # Y/x    0       1       2  
    
    # Generate three belts on a line, from coordinate x:0, y:3, going east
    belts = buildings.ConveyorBeltMKIII.generate_belt(
        name = "Belt",
        pos = Pos(0, 3),
        yaw = Yaw.East,
        length = 3
    )
    
    # Generate an assembling machine at coordinate x:1, y:1
    factory = buildings.AssemblingMachineMKI(
        name = "Factory",
        pos = Pos(1, 1)
    )
    
    # Generate a sorter picking items from the second belt (belt[1]) and droping at the assembler
    
    """
    The sorter is not working at the moment
    sorter = buildings.Sorter.generate_sorter_from_belt_to_factory(
        name = "Sorter",
        belt = belts[1],
        factory = factory,
        sorter_type = buildings.SorterMKIII,
    )
    """
    
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