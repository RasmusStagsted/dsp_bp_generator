from dsp_bp_generator.utils import Yaw, Vector
from dsp_bp_generator.blueprint import Blueprint
from dsp_bp_generator.blueprint import BlueprintBuildingV1

from dsp_bp_generator import buildings
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

    station = buildings.PlanetaryLogisticsStation(
        name = "Planetary Logistics Station",
        pos = Vector(x = 0, y = 0)
    )
    station.set_item(0, 1001, buildings.PlanetaryLogisticsStation.ItemMode.DEMAND)
    station.set_item(1, 1002, buildings.PlanetaryLogisticsStation.ItemMode.SUPPLY)
    station.set_item(2, 1003, buildings.PlanetaryLogisticsStation.ItemMode.STORAGE)
    
    blueprint = Blueprint()
    print(buildings.Building.buildings[0].parameter_count)
    output_blueprint_string = blueprint.serialize(buildings.Building.buildings, blueprint_building_version = BlueprintBuildingV1)
    print(output_blueprint_string)