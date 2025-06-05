from dsp_bp_generator.factory_generator.factory_router_interface import FactoryRouterInterface
from dsp_bp_generator.factory_generator.proliferator import Proliferator
from dsp_bp_generator.factory_generator.factory_block_interface import FactoryBlockInterface
from dsp_bp_generator.factory_generator.recipes import Recipe
from dsp_bp_generator.factory_generator.factory_section import FactorySection
from ..utils import Vector

class Factory:

    def __init__(self, bus_input, assemblies, proliferators):
        self.bus_input = bus_input
        self.assemblies = assemblies
        self.proliferators = proliferators
        self.sections = []
    
    def generate_factory_buildings(self):
        self.height = 0
        for assembly in self.assemblies:
            
            section = FactorySection(
                pos = Vector(x = 0, y = 0),  # Placeholder position, should be calculated based on previous sections
                factory_router_interface = self.bus_input,
                factory_block_interfaces = [],
                recipe = Recipe(assembly),
                factory_count = assembly.get("Factories", 1),
                proliferator = assembly.get("Proliferator", None)
            )
            self.sections.append(section)
            self.height += section.get_height()
    
if __name__ == "__main__":
    
    INGREDIENT = FactoryBlockInterface.Direction.INGREDIENT
    PRODUCT = FactoryBlockInterface.Direction.PRODUCT
    
    bus_input = [
        FactoryRouterInterface(
            name = "Belt router interface iron ore",
            item_type = "IronOre",
            direction = INGREDIENT,
            pos = Vector(0, 0),
            throughput = 6,
            proliferator = None,
        ),
        FactoryRouterInterface(
            name = "Belt router interface iron ore",
            item_type = "CopperOre",
            direction = INGREDIENT,
            pos = Vector(0, 0),
            throughput = 6,
            proliferator = None,
        ),
    ]
    
    assemblies = [
        {
            "Magnet": {
                "Factories": 5,
                "Proliferator": None
            }
        }, {
            "CopperIngot": {
                "Factories": 2,
                "Proliferator": None
            },
        }, {"MagneticCoil": {
                "Factories": 3,
                "Proliferator": None
            },
        },
    ]
    
    factory = Factory(bus_input, assemblies)
    factory.calculate_assemblies()
    factory.generate_factory_buildings()