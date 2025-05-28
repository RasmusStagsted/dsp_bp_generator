from ..enums import Item
from ..utils import Vector, Yaw
from ..factory_generator.recipes import Recipe
from ..blueprint import Blueprint, BlueprintBuildingV1
from ..buildings import Building
from ..buildings import ConveyorBeltMKI, ConveyorBeltMKII, ConveyorBeltMKIII
from ..buildings import Sorter, SorterMKI
from ..buildings import ArcSmelter, PlaneSmelter, NegentrophySmelter
from ..buildings import AssemblingMachineMKI, AssemblingMachineMKII, AssemblingMachineMKIII, ReComposingAssembler
from ..buildings import MatrixLab, SelfEvolutionLab
from ..buildings import OilRefinary
from ..buildings import ChemicalPlant, QuantumChemicalPlant

"""
A factory block consist of:
 - A single factory of any type
 - One to three input belts
 - One to three input sorters
 - One to three output belts
 - One to three output sorters
"""

class FactoryBlock:
    """Represents a block of factory buildings with belt and sorter routing."""

    def __init__(self, pos, belt_routing, factory_type, recipe):
        """Initialize the factory block and generate its components."""
        factory_pos = pos + FactoryBlock.get_factory_offset(factory_type)
        self.generate_factory(factory_pos, factory_type, recipe)
        top_belt_pos = pos + FactoryBlock.get_top_belt_offset(factory_type)
        buttom_belt_pos = pos + FactoryBlock.get_buttom_belt_offset(factory_type)
        self.generate_belts(belt_routing, top_belt_pos, buttom_belt_pos, self.factory)

    def generate_belts(self, belt_routing, top_belt_pos, buttom_belt_pos, factory):
        """Generate ingredient and product belts and connect them to the factory."""
        width = int(type(factory).get_size().x)
        self.ingredient_belts = []
        self.product_belts = []
        for route in belt_routing:
            if route.placement == "top":
                pos = top_belt_pos + Vector(y = route.belt_index)
            else:
                pos = buttom_belt_pos - Vector(y = route.belt_index)
            if route.direction == "product":
                yaw = Yaw.West
                pos += Vector(x = width - 1)
            elif route.direction == "ingredient":
                yaw = Yaw.East
            else:
                raise ValueError(f"Unknown direction: {route.direction}")
            belts = ConveyorBeltMKI.generate_belt(
                name = "",
                pos = pos,
                yaw = yaw,
                length = width
            )
            sorter_type = SorterMKI # TODO: Determine the optimal sorter type
            if route.direction == "product":
                sorter_belt_index = width - 1 - route.belt_index
                sorter_type.generate_sorter_from_belt_to_building(
                    name = "Sorter",
                    belt = belts[sorter_belt_index],
                    building = factory
                )
                self.product_belts.append(belts)
            elif route.direction == "ingredient":
                sorter_belt_index = route.belt_index
                sorter_type.generate_sorter_from_building_to_belt(
                    name = "Sorter",
                    building = factory,
                    belt = belts[sorter_belt_index]
                )
                self.ingredient_belts.append(belts)
            else:
                raise ValueError(f"Unknown direction: {route.direction}")

    def generate_factory(self, pos, factory_type, recipe):
        """Instantiate the factory building for this block."""
        self.factory = factory_type(
            name = "FactoryBlock",
            pos = pos,
            recipe_id = recipe["recipe_id"],
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
    # Example Route class for demonstration
    class Route:
        def __init__(self, placement, direction, belt_index):
            self.placement = placement
            self.direction = direction
            self.belt_index = belt_index

    # Example usage
    pos = Vector(x = 0, y = 0)
    belt_routing = [
        Route(placement = "buttom", direction = "ingredient", belt_index = 0),
        Route(placement = "buttom", direction = "ingredient", belt_index = 1),
        Route(placement = "top", direction = "product", belt_index = 0)
    ]
    factory_type = AssemblingMachineMKI
    recipe = Recipe.recipes["MagneticCoil"]

    block = FactoryBlock(pos, belt_routing, factory_type, recipe)
    print(f"FactoryBlock created: {block}")

    blueprint = Blueprint()
    output_blueprint_string = blueprint.serialize(Building.buildings, blueprint_building_version = BlueprintBuildingV1)
    print(output_blueprint_string)