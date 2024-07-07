from dsp_bp_generator.utils import Yaw, Vector
from dsp_bp_generator.blueprint import Blueprint
from dsp_bp_generator.blueprint import BlueprintBuildingV1
from dsp_bp_generator import buildings
import argparse

if __name__ == "__main__":
    
    # Parse the arguments
    parser = argparse.ArgumentParser(
        prog = "Blueprint parser",
        description = "Apllication to parse blueprints for the game Dyson Sphere program"
    )
    parser.add_argument("--output_file", "--of", type = str, help = "Output file where to save the output to (if not defined, the output will be written to standard output)")
    args = parser.parse_args()

    # This is a small example of how to create sime buildings
    assmeblemachine_mki = buildings.AssemblingMachineMKI(name = "Factory", pos = Vector(0, 0))
    assmeblemachine_mkii = buildings.AssemblingMachineMKII(name = "Factory", pos = Vector(5, 0))
    assmeblemachine_mkiii = buildings.AssemblingMachineMKIII(name = "Factory", pos = Vector(10, 0))
    
    tesla_tower = buildings.TeslaTower(name = "TeslaTower", pos = Vector(0, 5))
    wireless_power_tower = buildings.WirelessPowerTower(name = "WirelessPowerTower", pos = Vector(5, 5))
    satelite_sub_station = buildings.SateliteSubstation(name = "SateliteSubstation", pos = Vector(10, 5))
    
    belt_mki = buildings.ConveyorBeltMKI.generate_belt(name = "belt_mki", pos = Vector(-1, 10), yaw = [Yaw.North, Yaw.East, Yaw.South], length = [2, 2, 3])
    belt_mkii = buildings.ConveyorBeltMKII.generate_belt(name = "belt_mkii", pos = Vector(4, 10), yaw = [Yaw.North, Yaw.East, Yaw.South], length = [2, 2, 3])
    belt_mkiii = buildings.ConveyorBeltMKIII.generate_belt(name = "belt_mkiii", pos = Vector(9, 10), yaw = [Yaw.North, Yaw.East, Yaw.South], length = [2, 2, 3])
    
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