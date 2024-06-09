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

    def __init__(self, pos, input_belt_types, output_belt_types, factory_type, width, recipe):

        input_belt_pos = pos + FactoryBlock._get_top_belt_offset(factory_type)
        self.generate_input_belts(input_belt_pos, input_belt_types, width)

        output_belt_pos = pos + FactoryBlock._get_buttom_belt_offset(factory_type)
        self.generate_output_belts(output_belt_pos, output_belt_types, width)

        factory_pos = pos + FactoryBlock._get_factory_offset(factory_type)
        self.generate_factory(factory_pos, factory_type, width, recipe)

        self.generate_input_sorters(input_belt_types)
        self.generate_output_sorters(output_belt_types)

    def generate_input_belts(self, pos, belt_types, width):
        self.input_belts = []
        for i in range(len(belt_types)):
            belts = belt_types[i].generate_belt(
                name = f"FactoryBlock:InputBelt:{i}",
                pos = pos,
                yaw = Yaw.East,
                length = int(width)
            )
            self.input_belts.append(belts)
            pos += Vector(y = 1)
    
    def generate_output_belts(self, pos, belt_types, width):
        self.output_belts = []
        pos += Vector(x = width - 1)
        for i in range(len(belt_types)):
            belts = belt_types[i].generate_belt(
                name = "FactoryBlockOutputBelt",
                pos = pos,
                yaw = Yaw.West,
                length = int(width)
            )
            self.output_belts.append(belts)
            pos -= Vector(y = 1)
    
    def generate_factory(self, pos, factory_type, width, recipe):
        self.factory = factory_type(
            name = "FactoryBlock",
            pos = pos
        )
    
    def generate_input_sorters(self, input_belt_types):
        for i in range(len(input_belt_types)):
            belt = self.input_belts[i][i]
            sorter = Sorter.generate_sorter_from_belt_to_factory(
                name = "InputSorter:{i}",
                belt = belt,
                factory = self.factory,
                sorter_type = SorterMKI
            )
    
    def generate_output_sorters(self, output_belt_types):
        for i in range(len(output_belt_types)):
            belt = self.output_belts[i][-1 - i]
            sorter = Sorter.generate_sorter_from_factory_to_belt(
                name = "OutputSorter:{i}",
                belt = belt,
                factory = self.factory,
                sorter_type = SorterMKI
            )
    
    def connect_to_factory_block(factory_block1, factory_block2):
        for i in range(len(factory_block1.input_belts)):
            factory_block1.input_belts[i][-1].connect_to_belt(factory_block2.input_belts[i][0])
        for i in range(len(factory_block1.output_belts)):
            factory_block2.output_belts[i][-1].connect_to_belt(factory_block1.output_belts[i][0])
    
    def _get_inserter_offset(factory_type, side, index):
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
    
    def _get_inserter_slot(factory_type, side, index):
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
    
    def _get_belt_index_offset(factory_type):
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
    
    def _get_belt_offset(factory_type, side):
        if side == "top":
            return Vector(y = self.get_top_belt_y_offset(factory_type))
        elif side == "buttom":
            return Vector(y = self.get_buttom_belt_y_offset(factory_type))
    
    def _get_top_belt_offset(factory_type):
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
    
    def _get_buttom_belt_offset(factory_type):
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
        
    def _get_factory_offset(factory_type):
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
    