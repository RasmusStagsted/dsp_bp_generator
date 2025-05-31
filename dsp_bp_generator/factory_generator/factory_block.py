from ..enums import Item
from ..utils import Vector, Yaw
from ..factory_generator.recipes import Recipe
from .factory_block_interface import FactoryBlockInterface
from ..factory_generator.proliferator import ProliferatorMKI, ProliferatorMKII, ProliferatorMKIII
from ..blueprint import Blueprint, BlueprintBuildingV1
from ..buildings import Building
from ..buildings import ConveyorBeltMKI, ConveyorBeltMKII, ConveyorBeltMKIII
from ..buildings import SorterMKI, SorterMKII, SorterMKIII, PileSorter
from ..buildings import ArcSmelter, PlaneSmelter, NegentrophySmelter
from ..buildings import AssemblingMachineMKI, AssemblingMachineMKII, AssemblingMachineMKIII, ReComposingAssembler
from ..buildings import MatrixLab, SelfEvolutionLab
from ..buildings import OilRefinary
from ..buildings import ChemicalPlant, QuantumChemicalPlant



class FactoryBlock:
    """
    A factory block consist of:
    - A single factory of any type
    - One to three input belts
    - One to three input sorters
    - One to three output belts
    - One to three output sorters
    """

    @staticmethod
    def select_belt_type(required_throughput, factory_block_index):
        belt_types = [ConveyorBeltMKI, ConveyorBeltMKII, ConveyorBeltMKIII]
        for belt_type in belt_types:
            if required_throughput * (1 + factory_block_index) <= belt_type.MAX_THROUGHPUT:
                return belt_type
        raise ValueError(f"Required throughput {required_throughput * (1 + factory_block_index)}/s exceeds maximum throughput of all belt types.")

    @staticmethod
    def select_sorter_type(required_throughput, belt_index):
        sorter_types = [SorterMKI, SorterMKII, SorterMKIII, PileSorter]
        for sorter_type in sorter_types:
            if required_throughput <= sorter_type.MAX_THROUGHPUT / (1 + belt_index):
                return sorter_type
        raise ValueError(f"Required throughput {required_throughput}/s exceeds maximum throughput of all sorter types.")

    def __init__(self, pos, connections, recipe, factory_type, belt_type, sorter_type):
        """Initialize the factory block and generate its components."""
        factory_pos = pos + FactoryBlock.get_factory_offset(factory_type)
        self.generate_factory(factory_pos, factory_type, recipe)
        top_belt_pos = pos + FactoryBlock.get_top_belt_offset(factory_type)
        buttom_belt_pos = pos + FactoryBlock.get_buttom_belt_offset(factory_type)
        self.generate_belts_and_sorters(connections, recipe, top_belt_pos, buttom_belt_pos, belt_type, sorter_type, self.factory)

    def generate_belts_and_sorters(self, connections, recipe, top_belt_pos, buttom_belt_pos, requested_belt_type, requested_sorter_type, factory):
        """Generate ingredient and product belts and connect them to the factory."""
        width = int(type(factory).get_size().x)
        self.ingredient_belts = []
        self.product_belts = []
        
        # Fetch lowest level of proliferator properties
        prolifirator_speedup = 1
        proliferator_productivity = 1
        for connection in connections:
            prolifirator_speedup = min(prolifirator_speedup, connection.proliferator.PRODUCTIVITY)
            proliferator_productivity = min(proliferator_productivity, connection.proliferator.PRODUCTIVITY)
        
        for connection in connections:
            # Calculate throughput based on recipe and connection
            throughput = connection.get_throughput(recipe) / recipe.time * prolifirator_speedup
            if connection.direction == FactoryBlockInterface.Direction.PRODUCT:
                throughput *= proliferator_productivity

            # Determine belt and sorter types based on throughput and connection properties
            if requested_belt_type is None:
                belt_type = FactoryBlock.select_belt_type(throughput, connection.factory_block_index)
            else:
                belt_type = requested_belt_type
            if requested_sorter_type is None:
                sorter_type = FactoryBlock.select_sorter_type(throughput, connection.belt_index)
            else:
                sorter_type = requested_sorter_type

            # Generate the belt based on the connection properties
            if connection.placement == FactoryBlockInterface.Placement.TOP:
                pos = top_belt_pos + Vector(y = connection.belt_index)
            elif connection.placement == FactoryBlockInterface.Placement.BOTTOM:
                pos = buttom_belt_pos - Vector(y = connection.belt_index)
            else:
                raise ValueError(f"Unknown placement: {connection.placement}")
            if connection.direction == FactoryBlockInterface.Direction.PRODUCT:
                yaw = Yaw.West
                pos += Vector(x = width - 1)
            elif connection.direction == FactoryBlockInterface.Direction.INGREDIENT:
                yaw = Yaw.East
            else:
                raise ValueError(f"Unknown direction: {connection.direction}")
            belts = belt_type.generate_belt(
                name = "",
                pos = pos,
                yaw = yaw,
                length = width
            )
            
            # Connect the belts to the factory using sorters
            if connection.direction == FactoryBlockInterface.Direction.PRODUCT:
                sorter_belt_index = width - 1 - connection.belt_index
                sorter_type.generate_sorter_from_belt_to_building(
                    name = "Sorter",
                    belt = belts[sorter_belt_index],
                    building = factory
                )
                self.product_belts.append(belts)
            elif connection.direction == FactoryBlockInterface.Direction.INGREDIENT:
                sorter_belt_index = connection.belt_index
                sorter_type.generate_sorter_from_building_to_belt(
                    name = "Sorter",
                    building = factory,
                    belt = belts[sorter_belt_index]
                )
                self.ingredient_belts.append(belts)
            else:
                raise ValueError(f"Unknown direction: {connection.direction}")

    def generate_factory(self, pos, factory_type, recipe):
        """Instantiate the factory building for this block."""
        self.factory = factory_type(
            name = "FactoryBlock",
            pos = pos,
            recipe_id = recipe.recipe_id,
        )

    @staticmethod
    def connect_to_factory_block(factory_block1, factory_block2):
        """Connect ingredient and product belts between two factory blocks."""
        for i in range(len(factory_block1.ingredient_belts)):
            factory_block1.ingredient_belts[i][-1].connect_to_belt(factory_block2.ingredient_belts[i][0])
        for i in range(len(factory_block1.product_belts)):
            factory_block2.product_belts[i][-1].connect_to_belt(factory_block1.product_belts[i][0])

    @staticmethod
    def get_inserter_offset(factory_type, side, index):
        """Get the offset for an inserter based on factory type and side."""
        assert side in ("top", "buttom"), 'Side needs to be "top" or "buttom"'
        if factory_type in (Item.ArcSmelter, Item.PlaneSmelter, Item.NegentrophySmelter):
            return Vector(x=-0.8 + 0.8 * index, y=1.2 if side == "top" else -1.2)
        elif factory_type in (Item.AssemblingMachineMKI, Item.AssemblingMachineMKII, Item.AssemblingMachineMKIII, Item.ReComposingAssembler):
            return Vector(x=-0.8 + 0.8 * index, y=1.2 if side == "buttom" else -1.2) # TODO: Check if this is correct, or if the side == "top" should be used
        elif factory_type in (Item.MatrixLab, Item.SelfEvolutionLab):
            raise NotImplementedError("Labs aren't supported yet")
        elif factory_type == Item.OilRefinary:
            raise NotImplementedError("Oil refinaries aren't supported yet")
        elif factory_type in (Item.ChemicalPlant, Item.QuantumChemicalPlant):
            raise NotImplementedError("Chemical plants aren't supported yet")
        else:
            raise NotImplementedError(f"Unsupported factory type: {factory_type}")

    @staticmethod
    def get_inserter_slot(factory_type, side, index):
        """Get the slot index for an inserter based on factory type and side."""
        assert side in ("top", "buttom", "left", "right"), 'Side needs to be "top", "buttom", "left" or "right"'
        if factory_type in (Item.ArcSmelter, Item.PlaneSmelter, Item.NegentrophySmelter):
            return index if side == "top" else 8 - index
        elif factory_type in (Item.AssemblingMachineMKI, Item.AssemblingMachineMKII, Item.AssemblingMachineMKIII, Item.ReComposingAssembler):
            return index if side == "buttom" else 8 - index # TODO: Check if this is correct, or if the side == "top" should be used
        elif factory_type in (Item.MatrixLab, Item.SelfEvolutionLab):
            raise NotImplementedError("Labs aren't supported yet")
        elif factory_type == Item.OilRefinary:
            raise NotImplementedError("Oil refinaries aren't supported yet")
        elif factory_type in (Item.ChemicalPlant, Item.QuantumChemicalPlant):
            raise NotImplementedError("Chemical plants aren't supported yet")
        else:
            raise NotImplementedError(f"Unsupported factory type: {factory_type}")

    @staticmethod
    def get_belt_index_offset(factory_type):
        """Get the belt index offset for a given factory type."""
        if factory_type in (Item.ArcSmelter, Item.PlaneSmelter, Item.NegentrophySmelter, Item.AssemblingMachineMKI, Item.AssemblingMachineMKII, Item.AssemblingMachineMKIII, Item.ReComposingAssembler):
            return 0
        elif factory_type in (Item.MatrixLab, Item.SelfEvolutionLab):
            raise NotImplementedError("Labs aren't supported yet")
        elif factory_type == Item.OilRefinary:
            raise NotImplementedError("Oil refinaries aren't supported yet")
        elif factory_type in (Item.ChemicalPlant, Item.QuantumChemicalPlant):
            raise NotImplementedError("Chemical plants aren't supported yet")
        else:
            raise NotImplementedError(f"Unsupported factory type: {factory_type}")

    @staticmethod
    def get_belt_offset(factory_type, side):
        """Get the belt offset vector for a given factory type and side."""
        if side == "top":
            return Vector(y = FactoryBlock.get_top_belt_y_offset(factory_type))
        elif side == "buttom":
            return Vector(y = FactoryBlock.get_buttom_belt_y_offset(factory_type))

    @staticmethod
    def get_top_belt_offset(factory_type):
        """Get the top belt offset vector for a given factory type."""
        if factory_type in (ArcSmelter, PlaneSmelter, NegentrophySmelter, AssemblingMachineMKI, AssemblingMachineMKII, AssemblingMachineMKIII, ReComposingAssembler):
            return Vector(y = 2)
        elif factory_type in (MatrixLab, SelfEvolutionLab):
            raise NotImplementedError("Labs aren't supported yet")
        elif factory_type == OilRefinary:
            raise NotImplementedError("Oil refinaries aren't supported yet")
        elif factory_type in (ChemicalPlant, QuantumChemicalPlant):
            raise NotImplementedError("Chemical plants aren't supported yet")
        else:
            raise NotImplementedError(f"Unsupported factory type: {factory_type}")

    @staticmethod
    def get_buttom_belt_offset(factory_type):
        """Get the bottom belt offset vector for a given factory type."""
        if factory_type in (ArcSmelter, PlaneSmelter, NegentrophySmelter, AssemblingMachineMKI, AssemblingMachineMKII, AssemblingMachineMKIII, ReComposingAssembler):
            return Vector(y = -2)
        elif factory_type in (MatrixLab, SelfEvolutionLab):
            raise NotImplementedError("Labs aren't supported yet")
        elif factory_type == OilRefinary:
            raise NotImplementedError("Oil refinaries aren't supported yet")
        elif factory_type in (ChemicalPlant, QuantumChemicalPlant):
            raise NotImplementedError("Chemical plants aren't supported yet")
        else:
            raise NotImplementedError(f"Unsupported factory type: {factory_type}")

    @staticmethod
    def get_factory_offset(factory_type):
        """Get the factory offset vector for a given factory type."""
        if factory_type in (ArcSmelter, PlaneSmelter, NegentrophySmelter, AssemblingMachineMKI, AssemblingMachineMKII, AssemblingMachineMKIII, ReComposingAssembler):
            return Vector(x = 1)
        elif factory_type in (MatrixLab, SelfEvolutionLab):
            raise NotImplementedError("Labs aren't supported yet")
        elif factory_type == OilRefinary:
            raise NotImplementedError("Oil refinaries aren't supported yet")
        elif factory_type in (ChemicalPlant, QuantumChemicalPlant):
            raise NotImplementedError("Chemical plants aren't supported yet")
        else:
            raise NotImplementedError(f"Unsupported factory type: {factory_type}")

if __name__ == "__main__":
    INGREDIENT = FactoryBlockInterface.Direction.INGREDIENT
    PRODUCT = FactoryBlockInterface.Direction.PRODUCT
    BUTTOM = FactoryBlockInterface.Placement.BOTTOM
    TOP = FactoryBlockInterface.Placement.TOP
    
    pos = Vector(x = 0, y = 0)
    factory_routing = [
        FactoryBlockInterface(
            name = "Magnet interface",
            item_type = "Magnet",
            direction = INGREDIENT,
            placement = BUTTOM,
            belt_index = 0,
            factory_block_index = 4,
            proliferator = ProliferatorMKIII
        ),
        FactoryBlockInterface(
            name = "Copper interface",
            item_type = "CopperIngot",
            direction = INGREDIENT,
            placement = BUTTOM,
            belt_index = 1,
            factory_block_index = 4,
            proliferator = ProliferatorMKIII
        ),
        FactoryBlockInterface(
            name = "MagneticCoil interface",
            item_type = "MagneticCoil",
            direction = PRODUCT,
            placement = TOP,
            belt_index = 0,
            factory_block_index = 4,
            proliferator = ProliferatorMKIII
        ),
    ]
    recipe = Recipe.recipes["MagneticCoil"]
    factory_type = AssemblingMachineMKI
    belt_type = None  # Let FactoryBlock select the belt type based on throughput
    sorter_type = None  # Let FactoryBlock select the sorter type based on throughput
    block = FactoryBlock(pos, factory_routing, recipe, factory_type, belt_type, sorter_type)
    print(f"FactoryBlock created: {block}")

    blueprint = Blueprint()
    output_blueprint_string = blueprint.serialize(
        blueprint_buildings = Building.buildings,
        blueprint_building_version = BlueprintBuildingV1
    )
    print("Smelter blueprint:\n" + output_blueprint_string)
    Building.buildings.clear()  # Clear the buildings for the next example
    
    pos = Vector(x = 0, y = 0)
    factory_routing = [
        FactoryBlockInterface(
            name = "Iron ore interface",
            item_type = "IronOre",
            direction = INGREDIENT,
            placement = BUTTOM,
            belt_index = 0,
            factory_block_index = 0,
            proliferator = ProliferatorMKIII
        ),
        FactoryBlockInterface(
            name = "Iron ingot interface",
            item_type = "IronIngot",
            direction = PRODUCT,
            placement = TOP,
            belt_index = 0,
            factory_block_index = 0,
            proliferator = ProliferatorMKIII
        ),
    ]
    recipe = Recipe.recipes["IronIngot"]
    factory_type = ArcSmelter
    belt_type = None  # Let FactoryBlock select the belt type based on throughput
    sorter_type = None  # Let FactoryBlock select the sorter type based on throughput
    block = FactoryBlock(pos, factory_routing, recipe, factory_type, belt_type, sorter_type)
    print(f"FactoryBlock created: {block}")

    blueprint = Blueprint()
    output_blueprint_string = blueprint.serialize(
        blueprint_buildings = Building.buildings,
        blueprint_building_version = BlueprintBuildingV1
    )
    print("Smelter blueprint:\n" + output_blueprint_string)
    Building.buildings.clear()  # Clear the buildings