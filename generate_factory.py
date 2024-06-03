
from src.utils import Yaw, Pos
from src.ItemEnum import ItemEnum
from src.blueprint import Blueprint
from src.factory_generator import Factory, ItemFlow, recipes
import math

if __name__ == "__main__":
    
    factory = Factory()

    output_flow = [ItemFlow("MagneticCoil", 2.0)]
    factory.set_tartget_output_flow(output_flow, debug = True)
    factory.generate_factories(debug = True)

    output_bp_str = Blueprint.serialize()
    print(output_bp_str)
