from src.utils import Yaw, Pos
from src.blueprint import Blueprint
from src.blueprint import BlueprintStringHeader
from src.blueprint import BlueprintHeader
from src.blueprint import BlueprintArea
from src.blueprint import BlueprintBuildingHeader
from src.blueprint import BlueprintBuilding

from src import buildings
import math

if __name__ == "__main__":
    
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
    factory = buildings.AssemblingMachineMkIII(
        name = "Factory",
        pos = Pos(1, 1)
    )
    
    # Generate a sorter picking items from the second belt (belt[1]) and droping at the assembler
    sorter = buildings.Sorter.generate_sorter_from_belt_to_factory(
        name = "Sorter",
        belt = belts[1],
        factory = factory
    )
    
    blueprint = Blueprint()
    bp_str = blueprint.serialize(buildings.Building.buildings)
    print(bp_str)
