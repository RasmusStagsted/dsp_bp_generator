
from src.utils import Yaw, Pos
from src.ItemEnum import ItemEnum
from src.blueprint import Blueprint
from src.factory_generator import Factory, ItemFlow, recipes
from src.buildings import Building
import math

if __name__ == "__main__":
    
    factory = Factory()

    output_flow = [ItemFlow("Magnet", 2.0)]
    factory.set_tartget_output_flow(output_flow, debug = True)
    factory.generate_factories(debug = True)

    blueprint = Blueprint()
    output_bp_str = blueprint.serialize(Building.buildings)
    print(output_bp_str)
