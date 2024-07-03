from dsp_bp.utils import Yaw, Vector
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
    #         ┌───────────────────────┐
    #         │                       │
    #         │                       │
    #         │                       │
    #         │-----------------------│
    #         │                       │
    # slot 2  │                       │ slot 3
    #         │                       │
    #         │-----------------------│
    #         │                       │
    # slot 1  │           X           │ slot 4
    #         │                       │
    #         │-----------------------│
    #         │                       │
    # slot 0  │                       │ slot 5
    #         │                       │
    #         │-----------------------│
    #         │                       │
    #         │                       │
    #         │                       │
    #         │-----------------------│
    #         │                       │
    #         │                       │
    #         │                       │
    #         └───────────────────────┘
    #           slot 8  slot 7  slot 6  
    
    #input_belt1 = buildings.ConveyorBeltMKI.generate_belt(
    #    name = "InputBelt1",
    #    pos = Vector(0, 7),
    #    yaw = Yaw.South,
    #    length = 5
    #)

    #input_belt2 = buildings.ConveyorBeltMKI.generate_belt(
    #    name = "InputBelt2",
    #    pos = Vector(4, 7),
    #    yaw = Yaw.South,
    #    length = 5
    #)
    
    output_belt = buildings.ConveyorBeltMKI.generate_belt(
        name = "OutputBelt",
        pos = Vector(1, 0),
        yaw = Yaw.East,
        length = 4
    )
    
    refinary = buildings.OilRefinary(
        name = "Oilrefinary",
        pos = Vector(2, 4)
    )
    
    #buildings.Sorter.generate_sorter_from_belt_to_factory(
    #    name = "InputSorter1",
    #    belt = input_belt1[-2],
    #    factory = refinary,
    #    sorter_type = buildings.SorterMKI,
    #)
    
    #buildings.Sorter.generate_sorter_from_belt_to_factory(
    #    name = "InputSorter2",
    #    belt = input_belt2[-2],
    #    factory = refinary,
    #    sorter_type = buildings.SorterMKI,
    #)

    buildings.Sorter.generate_sorter_from_building_to_belt(
        name = "OutputSorter",
        building = refinary,
        belt = output_belt[0],
        sorter_type = buildings.SorterMKI,
    )

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