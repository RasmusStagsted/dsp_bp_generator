from dsp_bp.utils import Yaw, Pos
from dsp_bp.blueprint import Blueprint
from dsp_bp.blueprint import BlueprintStringHeader
from dsp_bp.blueprint import BlueprintHeader
from dsp_bp.blueprint import BlueprintArea
from dsp_bp.blueprint import BlueprintBuildingHeader
from dsp_bp.blueprint import BlueprintBuildingV1

from dsp_bp import buildings
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

    # This is a small example of a assmeblemachine getting items from a belt,
    # and passing the products to another belt
    #
    # Input belt coordinates are (0.0, 4.0), (1.0, 4.0) and (2.0, 4.0)
    # Output belt coordinates are (2.0, 0.0), (1.0, 0.0) and (0.0, 0.0)
    # Assembler coordinate = (1.0, 2.0)
    # The sorters has two coordinates. One for pickup and one for drop-off:
    #  - Input Sorter coordinates are (1.0, 4.0) and (1.0, 2.8)
    #  - Input Sorter coordinates are (1.0, 4.0) and (1.0, 2.8)
    #             
    #    ┌───────┬───────┬───────┐
    #    │       │┌─────┐│       │
    #  4 │ → → → ││→ → →││ → → → │
    #    │       ││  ↓  ││       │
    #    ├───────┴┼──↓──┼┘───────┤
    #    │        │  ↓  │        │
    #  3 │        │  ↓  │        │
    #    │        │  ↓  │        │
    #    │        └─────┘        │
    #    │                       │
    #  2 │   Assembling machine  │
    #    │                       │
    #    │        ┌─────┐        │
    #    │        │  ↓  │        │
    #  1 │        │  ↓  │        │
    #    │        │  ↓  │        │
    #    ├───────┬┼──↓──┼┬───────┤
    #    │       ││  ↓  ││       │
    #  0 │ ← ← ← ││← ← ←││ ← ← ← │
    #    │       │└─────┘│       │
    #    └───────┴───────┘───────┘
    # Y/x    0       1       2  
    
    # Generate three belts on a line, from coordinate x:0, y:3, going east
    input_belts = buildings.ConveyorBeltMKI.generate_belt(
        name = "InputBelt",
        pos = Pos(0, 4),
        yaw = Yaw.East,
        length = 3
    )

    # Generate three belts on a line, from coordinate x:2, y:0, going west
    output_belts = buildings.ConveyorBeltMKI.generate_belt(
        name = "OutputBelt",
        pos = Pos(2, 0),
        yaw = Yaw.West,
        length = 3
    )
    
    # Generate an assembling machine at coordinate x:1, y:2
    factory = buildings.AssemblingMachineMKI(
        name = "Factory",
        pos = Pos(1, 2)
    )
    
    # Generate a sorter picking items from the second piece of the input belt and droping at the assembler
    sorter = buildings.Sorter.generate_sorter_from_belt_to_factory(
        name = "InputSorter",
        belt = input_belts[1],
        factory = factory,
        sorter_type = buildings.SorterMKI,
    )
    
    # Generate a sorter picking items from the assembler and droping at the second piece of the output belt
    sorter = buildings.Sorter.generate_sorter_from_factory_to_belt(
        name = "OutputSorter",
        belt = output_belts[1],
        factory = factory,
        sorter_type = buildings.SorterMKI,
    )
    
    blueprint = Blueprint()
    output_blueprint_string = blueprint.serialize(buildings.Building.buildings, blueprint_building_version = BlueprintBuildingV1)

    # Write parsed data
    if args.output_file == None:
        for building in buildings.Building.buildings:
            print(building)
    else:
        with open(args.output_file, "w") as file:
            for building in buildings.Building.buildings:
                file.write(building.__str__())
            file.write(output_blueprint_string)
            print(output_blueprint_string)