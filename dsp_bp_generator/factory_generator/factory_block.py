from ..enums import Item
from ..utils import Vector, Yaw
from ..buildings import ConveyorBeltMKI, ConveyorBeltMKII, ConveyorBeltMKIII
from ..buildings import Sorter, SorterMKI
from ..buildings import ArcSmelter, PlaneSmelter, NegentrophySmelter
from ..buildings import AssemblingMachineMKI, AssemblingMachineMKII, AssemblingMachineMKIII, ReComposingAssembler
from ..buildings import MatrixLab, SelfEvolutionLab
from ..buildings import OilRefinary
from ..buildings import ChemicalPlant, QuantumChemicalPlant

class FactoryBlock:

    def __init__(self, pos, belt_routing, factory_type, width, recipe):

        factory_pos = pos + FactoryBlock.get_factory_offset(factory_type)
        self.generate_factory(factory_pos, factory_type, width, recipe)

        top_belt_pos = pos + FactoryBlock.get_top_belt_offset(factory_type)
        buttom_belt_pos = pos + FactoryBlock.get_buttom_belt_offset(factory_type)
        self.generate_belts(belt_routing, top_belt_pos, buttom_belt_pos, self.factory, width)

    def generate_belts(self, belt_routing, top_belt_pos, buttom_belt_pos, factory, width):
        top_sorter_count = 0
        buttom_sorter_count = 0
        
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
                assert False, f"Unknown direction: {route.direction}"
            
            belts = ConveyorBeltMKI.generate_belt(
                name = "",
                pos = pos,
                yaw = yaw,
                length = width
            )
            
            # TODO: Determine the optimal sorter type
            sorter_type = SorterMKI
            
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
                assert False, f"Unknown direction: {route.direction}"

    def generate_factory(self, pos, factory_type, width, recipe):
        self.factory = factory_type(
            name = "FactoryBlock",
            pos = pos
        )
        
    def connect_to_factory_block(factory_block1, factory_block2):
        for i in range(len(factory_block1.ingredient_belts)):
            factory_block1.ingredient_belts[i][-1].connect_to_belt(factory_block2.ingredient_belts[i][0])
        for i in range(len(factory_block1.product_belts)):
            factory_block2.product_belts[i][-1].connect_to_belt(factory_block1.product_belts[i][0])
    
    def get_inserter_offset(factory_type, side, index):
        assert side == "top" or side == "buttom", "Side needs to be \"top\" or \"buttom\""
        if factory_type == Item.ArcSmelter or factory_type == Item.PlaneSmelter or factory_type == Item.NegentrophySmelter:
            return Vector(
                x = -0.8 + 0.8 * index,
                y = 1.2 if side == "top" else -1.2
            )
        elif factory_type == Item.AssemblingMachineMKI or factory_type == Item.AssemblingMachineMKII or factory_type == Item.AssemblingMachineMKIII or factory_type == Item.ReComposingAssembler:
            return Vector(
                x = -0.8 + 0.8 * index,
                y = 1.2 if side == "buttom" else -1.2    
            )
        elif factory_type == Item.MatrixLab or factory_type == Item.SelfEvolutionLab:
            assert True, "Matrix labs isn't supported yet"
        elif factory_type == Item.OilRefinary:
            assert True, "Oil refinaries isn't supported yet"
        elif factory_type == Item.ChemicalPlant or factory_type == Item.QuantumChemicalPlant:
            assert True, "Chemical plants labs isn't supported yet"
        else:
            assert True, "Unsupported factory type: " + factory_type
    
    def get_inserter_slot(factory_type, side, index):
        assert side == "top" or side == "buttom" or side == "left" or side == "right", "Side needs to be \"top\", \"buttom\", \"left\" or \"right\""
        if factory_type == Item.ArcSmelter or factory_type == Item.PlaneSmelter or factory_type == Item.NegentrophySmelter:
            if side == "top":
                return index
            else:
                return 8 - index
        elif factory_type == Item.AssemblingMachineMKI or factory_type == Item.AssemblingMachineMKII or factory_type == Item.AssemblingMachineMKIII or factory_type == Item.ReComposingAssembler:
            if side == "buttom":
                return index
            else:
                return 8 - index
        elif factory_type == Item.MatrixLab or factory_type == Item.SelfEvolutionLab:
            assert True, "Matrix labs isn't supported yet"
        elif factory_type == Item.OilRefinary:
            assert True, "Oil refinaries isn't supported yet"
        elif factory_type == Item.ChemicalPlant or factory_type == Item.QuantumChemicalPlant:
            assert True, "Chemical plants labs isn't supported yet"
        else:
            assert True, "Unsupported factory type: " + factory_type
    
    def get_belt_index_offset(factory_type):
        if factory_type == Item.ArcSmelter or factory_type == Item.PlaneSmelter or factory_type == Item.NegentrophySmelter:
            return 0
        elif factory_type == Item.AssemblingMachineMKI or factory_type == Item.AssemblingMachineMKII or factory_type == Item.AssemblingMachineMKIII or factory_type == Item.ReComposingAssembler:
            return 0
        elif factory_type == Item.MatrixLab or factory_type == Item.SelfEvolutionLab:
            assert True, "Matrix labs isn't supported yet"
        elif factory_type == Item.OilRefinary:
            assert True, "Oil refinaries isn't supported yet"
        elif factory_type == Item.ChemicalPlant or factory_type == Item.QuantumChemicalPlant:
            assert True, "Chemical plants labs isn't supported yet"
        else:
            assert True, "Unsupported factory type: " + factory_type
    
    def get_belt_offset(factory_type, side):
        if side == "top":
            return Vector(y = self.get_top_belt_y_offset(factory_type))
        elif side == "buttom":
            return Vector(y = self.get_buttom_belt_y_offset(factory_type))
    
    def get_top_belt_offset(factory_type):
        if factory_type == ArcSmelter or factory_type == PlaneSmelter or factory_type == NegentrophySmelter:
            return Vector(y = 2)
        elif factory_type == AssemblingMachineMKI or factory_type == AssemblingMachineMKII or factory_type == AssemblingMachineMKIII or factory_type == ReComposingAssembler:
            return Vector(y = 2)
        elif factory_type == MatrixLab or factory_type == SelfEvolutionLab:
            assert True, "Matrix labs isn't supported yet"
        elif factory_type == OilRefinary:
            assert True, "Oil refinaries isn't supported yet"
        elif factory_type == ChemicalPlant or factory_type == QuantumChemicalPlant:
            assert True, "Chemical plants labs isn't supported yet"
        else:
            assert True, "Unsupported factory type: " + factory_type
    
    def get_buttom_belt_offset(factory_type):
        if factory_type == ArcSmelter or factory_type == PlaneSmelter or factory_type == NegentrophySmelter:
            return Vector(y = -2)
        elif factory_type == AssemblingMachineMKI or factory_type == AssemblingMachineMKII or factory_type == AssemblingMachineMKIII or factory_type == ReComposingAssembler:
            return Vector(y = -2)
        elif factory_type == MatrixLab or factory_type == SelfEvolutionLab:
            assert True, "Matrix labs isn't supported yet"
        elif factory_type == OilRefinary:
            assert True, "Oil refinaries isn't supported yet"
        elif factory_type == ChemicalPlant or factory_type == QuantumChemicalPlant:
            assert True, "Chemical plants labs isn't supported yet"
        else:
            assert True, "Unsupported factory type: " + factory_type
        
    def get_factory_offset(factory_type):
        if factory_type == ArcSmelter or factory_type == PlaneSmelter or factory_type == NegentrophySmelter:
            return Vector(x = 1)
        elif factory_type == AssemblingMachineMKI or factory_type == AssemblingMachineMKII or factory_type == AssemblingMachineMKIII or factory_type == ReComposingAssembler:
            return Vector(x = 1)
        elif factory_type == MatrixLab or factory_type == SelfEvolutionLab:
            assert True, "Matrix labs isn't supported yet"
        elif factory_type == OilRefinary:
            assert True, "Oil refinaries isn't supported yet"
        elif factory_type == ChemicalPlant or factory_type == QuantumChemicalPlant:
            assert True, "Chemical plants labs isn't supported yet"
        else:
            assert True, "Unsupported factory type: " + factory_type
    