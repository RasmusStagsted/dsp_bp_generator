from ..enums import Item
from ..utils import Vector, Yaw
from ..factory_generator.recipes import Recipe
from .factory_block_interface import FactoryBlockInterface, FactoryBlockBelt
from ..factory_generator.proliferator import ProliferatorMKI, ProliferatorMKII, ProliferatorMKIII
from ..blueprint import Blueprint, BlueprintBuildingV1
from ..buildings import Building
from ..buildings import ConveyorBelt
from ..buildings import Sorter
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

    def __init__(self, pos, interface: FactoryBlockInterface, recipe, factory_type, belt_type, sorter_type):
        """Initialize the factory block and generate its components."""
        if factory_type is None:
            factory_type = FactoryBlock.select_factory(recipe)
        factory_pos = pos + FactoryBlock.get_factory_offset(factory_type) + Vector(y = -interface.get_top_belt_count())
        self.generate_factory(factory_pos, factory_type, recipe)
        
        top_belt_pos = pos + Vector(y = 1 - interface.get_top_belt_count())
        buttom_belt_pos = pos + Vector(y = -factory_type.get_height() - interface.get_top_belt_count())
        self.generate_belts_and_sorters(interface, recipe, top_belt_pos, buttom_belt_pos, belt_type, sorter_type, self.factory)

    def generate_belts_and_sorters(self, interface, recipe, top_belt_pos, buttom_belt_pos, requested_belt_type, requested_sorter_type, factory):
        """Generate ingredient and product belts and connect them to the factory."""
        width = int(type(factory).get_size().x)
        self.ingredient_belts = []
        self.product_belts = []
        
        # Fetch lowest level of proliferator properties
        prolifirator_speedup = 1
        proliferator_productivity = 1
        for belt in interface.belts:
            if belt.proliferator == None:
                prolifirator_speedup = 1
                proliferator_productivity = 1
                break
            else:
                prolifirator_speedup = min(prolifirator_speedup, belt.proliferator.PRODUCTIVITY)
                proliferator_productivity = min(proliferator_productivity, belt.proliferator.PRODUCTIVITY)
        
        for belt in interface.belts:
            # Calculate throughput based on recipe and connection
            throughput = belt.throughput / recipe.time * prolifirator_speedup
            if belt.direction == FactoryBlockBelt.Direction.PRODUCT:
                throughput *= proliferator_productivity

            # Determine belt and sorter types based on throughput and connection properties
            if requested_belt_type is None:
                belt_type = FactoryBlock.select_belt_type(throughput)
            else:
                belt_type = requested_belt_type
            if requested_sorter_type is None:
                sorter_type = FactoryBlock.select_sorter_type(belt, recipe)
            else:
                sorter_type = requested_sorter_type

            # Generate the belt based on the connection properties
            if belt.placement == FactoryBlockBelt.Placement.TOP:
                pos = top_belt_pos + Vector(y = belt.belt_index)
            elif belt.placement == FactoryBlockBelt.Placement.BOTTOM:
                pos = buttom_belt_pos - Vector(y = belt.belt_index)
            else:
                raise ValueError(f"Unknown placement: {belt.placement}")
            if belt.direction == FactoryBlockBelt.Direction.PRODUCT:
                yaw = Yaw.West
                pos += Vector(x = width - 1)
            elif belt.direction == FactoryBlockBelt.Direction.INGREDIENT:
                yaw = Yaw.East
            else:
                raise ValueError(f"Unknown direction: {belt.direction}")
            belts = belt_type.generate_belt(
                name = "",
                pos = pos,
                yaw = yaw,
                length = width
            )
            
            # Connect the belts to the factory using sorters
            if belt.direction == FactoryBlockBelt.Direction.PRODUCT:
                sorter_belt_index = width - 1 - belt.belt_index
                sorter_type.generate_sorter_from_belt_to_building(
                    name = "Sorter",
                    belt = belts[sorter_belt_index],
                    building = factory
                )
                self.product_belts.append(belts)
            elif belt.direction == FactoryBlockBelt.Direction.INGREDIENT:
                sorter_belt_index = belt.belt_index
                sorter_type.generate_sorter_from_building_to_belt(
                    name = "Sorter",
                    building = factory,
                    belt = belts[sorter_belt_index]
                )
                self.ingredient_belts.append(belts)
            else:
                raise ValueError(f"Unknown direction: {belt.direction}")

    def generate_factory(self, pos, factory_type, recipe):
        """Instantiate the factory building for this block."""
        self.factory = factory_type(
            name = "FactoryBlock",
            pos = pos,
            recipe_id = recipe.recipe_id,
        )

    def get_height(self):
        return 0#int(self.factory.get_size().y + max(self.))

    @staticmethod
    def select_belt_type(required_throughput):
        return ConveyorBelt.get_minimum_required_belt_type(required_throughput)
    
    @staticmethod
    def select_sorter_type(belt, recipe):
        distance = belt.belt_index + 1
        speed = 1 if belt.proliferator is None else belt.proliferator.SPEED
        productivity = 1 if belt.proliferator is None else belt.proliferator.PRODUCTIVITY
        
        if belt.direction == FactoryBlockBelt.Direction.INGREDIENT:
            throughput = recipe.input_items[belt.item_type] * speed / recipe.time
        elif belt.direction == FactoryBlockBelt.Direction.PRODUCT:
            throughput = recipe.output_items[belt.item_type] * speed * productivity / recipe.time            
        else:
            raise ValueError(f"Unknown direction: {belt.direction} for belt: {belt.name}")
        return Sorter.get_minimum_required_sorter_type(
            required_throughput = throughput,
            distance = distance
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
            return Vector(x = 1, y = -1)
        elif factory_type in (MatrixLab, SelfEvolutionLab):
            raise NotImplementedError("Labs aren't supported yet")
        elif factory_type == OilRefinary:
            raise NotImplementedError("Oil refinaries aren't supported yet")
        elif factory_type in (ChemicalPlant, QuantumChemicalPlant):
            raise NotImplementedError("Chemical plants aren't supported yet")
        else:
            raise NotImplementedError(f"Unsupported factory type: {factory_type}")

if __name__ == "__main__":
    INGREDIENT = FactoryBlockBelt.Direction.INGREDIENT
    PRODUCT = FactoryBlockBelt.Direction.PRODUCT
    BUTTOM = FactoryBlockBelt.Placement.BOTTOM
    TOP = FactoryBlockBelt.Placement.TOP
    
    pos = Vector(x = 0, y = 0)
    interface = FactoryBlockInterface(belts = [
        FactoryBlockBelt(
            name = "Magnet interface",
            item_type = "Magnet",
            direction = INGREDIENT,
            placement = BUTTOM,
            throughput = 2.0,
            belt_index = 0,
            proliferator = ProliferatorMKIII
        ),
        FactoryBlockBelt(
            name = "Copper interface",
            item_type = "CopperIngot",
            direction = INGREDIENT,
            placement = BUTTOM,
            throughput = 1.0,
            belt_index = 1,
            proliferator = ProliferatorMKIII
        ),
        FactoryBlockBelt(
            name = "MagneticCoil interface",
            item_type = "MagneticCoil",
            direction = PRODUCT,
            placement = TOP,
            throughput = 2.0,
            belt_index = 0,
            proliferator = ProliferatorMKIII
        ),
    ])
    recipe = Recipe.recipes["MagneticCoil"]
    factory_type = AssemblingMachineMKI
    belt_type = None  # Let FactoryBlock select the belt type based on throughput
    sorter_type = None  # Let FactoryBlock select the sorter type based on throughput
    block = FactoryBlock(pos, interface, recipe, factory_type, belt_type, sorter_type)

    blueprint = Blueprint()
    output_blueprint_string = blueprint.serialize(
        blueprint_buildings = Building.buildings,
        blueprint_building_version = BlueprintBuildingV1
    )
    print(f"\nAssembly block created:\n{output_blueprint_string}\n")
    Building.buildings.clear()  # Clear the buildings for the next example
    
    pos = Vector(x = 0, y = 0)
    interface = FactoryBlockInterface(belts = [
        FactoryBlockBelt(
            name = "Iron ore interface",
            item_type = "IronOre",
            direction = INGREDIENT,
            placement = BUTTOM,
            throughput = 1.0,
            belt_index = 0,
            proliferator = ProliferatorMKIII
        ),
        FactoryBlockBelt(
            name = "Iron ingot interface",
            item_type = "IronIngot",
            direction = PRODUCT,
            placement = TOP,
            throughput = 1.0,
            belt_index = 0,
            proliferator = ProliferatorMKIII
        ),
    ])
    recipe = Recipe.recipes["IronIngot"]
    factory_type = ArcSmelter
    belt_type = None  # Let FactoryBlock select the belt type based on throughput
    sorter_type = None  # Let FactoryBlock select the sorter type based on throughput
    interface = FactoryBlockInterface.generate_interface(recipe = recipe)
    block = FactoryBlock(pos, interface, recipe, factory_type, belt_type, sorter_type)

    blueprint = Blueprint()
    print(2)
    output_blueprint_string = blueprint.serialize(
        blueprint_buildings = Building.buildings,
        blueprint_building_version = BlueprintBuildingV1
    )
    print(1)
    print(f"Smeltery block created:\n{output_blueprint_string}")
    Building.buildings.clear()  # Clear the buildings