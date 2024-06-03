from ItemEnum import ItemEnum
from utils import Pos, Yaw
import buildings

class FactoryBlock:
    
    def __init__(self, pos, input_count, output_count, factory_type, width, recipe):

        input_belt_pos = pos + FactoryBlock._get_top_belt_offset(factory_type)
        self.generate_input_belts(input_belt_pos, input_count, width)

        output_belt_pos = pos + FactoryBlock._get_buttom_belt_offset(factory_type)
        self.generate_output_belts(output_belt_pos, output_count, width)

        factory_pos = pos + FactoryBlock._get_factory_offset(factory_type)
        self.generate_factory(factory_pos, factory_type, width, recipe)

        for i in range(input_count):
            belt = self.input_belts[i][i]
            #sorter = Buildings.Sorter.generate_sorter_from_belt_to_factory("InputSorter:{i}", belt, self.factory)

    def generate_input_belts(self, pos, input_count, width):
        self.input_belts = []
        for i in range(input_count):
            belts = Buildings.Belt.generate_belt(
                name = f"FactoryBlock:InputBelt:{i}",
                pos = pos,
                yaw = Yaw.East,
                length = width
            )
            self.input_belts.append(belts)
            pos += Pos(y = 1)
    
    def generate_output_belts(self, pos, output_count, width):
        self.output_belts = []
        pos += Pos(x = width - 1)
        for i in range(output_count):
            belts = Buildings.Belt.generate_belt(
                name = "FactoryBlockOutputBelt",
                pos = pos,
                yaw = Yaw.West,
                length = width
            )
            self.output_belts.append(belts)
            pos -= Pos(y = 1)
    
    def generate_factory(self, pos, factory_type, width, recipe):
        self.factory = Buildings.Smelter(
            name = "FactoryBlock",
            pos = pos
        )
    
    def generate_input_sorters(self):
        pass
    
    def connect_to_factory_block(factory_block1, factory_block2):
        for i in range(len(factory_block1.input_belts)):
            factory_block1.input_belts[i][-1].connect_to_belt(factory_block2.input_belts[i][0])
        for i in range(len(factory_block1.output_belts)):
            factory_block2.output_belts[i][-1].connect_to_belt(factory_block1.output_belts[i][0])
    
    def _get_inserter_offset(factory_type, side, index):
        assert side == "top" or side == "buttom", "Side needs to be \"top\" or \"buttom\""
        if factory_type == ItemEnum.ArcSmelter or factory_type == ItemEnum.PlaneSmelter or factory_type == ItemEnum.NegentrophySmelter:
            return Pos(
                x = -0.8 + 0.8 * index,
                y = 1.2 if side == "top" else -1.2
            )
        elif factory_type == ItemEnum.AssemblingMachineMkI or factory_type == ItemEnum.AssemblingMachineMkII or factory_type == ItemEnum.AssemblingMachineMkIII or factory_type == ItemEnum.ReComposingAssembler:
            return Pos(
                x = -0.8 + 0.8 * index,
                y = 1.2 if side == "buttom" else -1.2    
            )
        elif factory_type == ItemEnum.MatrixLab or factory_type == ItemEnum.SelfEvolutionLab:
            assert True, "Matrix labs isn't supported yet"
        elif factory_type == ItemEnum.OilRefinary:
            assert True, "Oil refinaries isn't supported yet"
        elif factory_type == ItemEnum.ChemicalPlant or factory_type == ItemEnum.QuantumChemicalPlant:
            assert True, "Chemical plants labs isn't supported yet"
        else:
            assert True, "Unsupported factory type: " + factory_type
    
    def _get_inserter_slot(factory_type, side, index):
        assert side == "top" or side == "buttom" or side == "left" or side == "right", "Side needs to be \"top\", \"buttom\", \"left\" or \"right\""
        if factory_type == ItemEnum.ArcSmelter or factory_type == ItemEnum.PlaneSmelter or factory_type == ItemEnum.NegentrophySmelter:
            if side == "top":
                return index
            else:
                return 8 - index
        elif factory_type == ItemEnum.AssemblingMachineMkI or factory_type == ItemEnum.AssemblingMachineMkII or factory_type == ItemEnum.AssemblingMachineMkIII or factory_type == ItemEnum.ReComposingAssembler:
            if side == "buttom":
                return index
            else:
                return 8 - index
        elif factory_type == ItemEnum.MatrixLab or factory_type == ItemEnum.SelfEvolutionLab:
            assert True, "Matrix labs isn't supported yet"
        elif factory_type == ItemEnum.OilRefinary:
            assert True, "Oil refinaries isn't supported yet"
        elif factory_type == ItemEnum.ChemicalPlant or factory_type == ItemEnum.QuantumChemicalPlant:
            assert True, "Chemical plants labs isn't supported yet"
        else:
            assert True, "Unsupported factory type: " + factory_type
    
    def _get_belt_index_offset(factory_type):
        if factory_type == ItemEnum.ArcSmelter or factory_type == ItemEnum.PlaneSmelter or factory_type == ItemEnum.NegentrophySmelter:
            return 0
        elif factory_type == ItemEnum.AssemblingMachineMkI or factory_type == ItemEnum.AssemblingMachineMkII or factory_type == ItemEnum.AssemblingMachineMkIII or factory_type == ItemEnum.ReComposingAssembler:
            return 0
        elif factory_type == ItemEnum.MatrixLab or factory_type == ItemEnum.SelfEvolutionLab:
            assert True, "Matrix labs isn't supported yet"
        elif factory_type == ItemEnum.OilRefinary:
            assert True, "Oil refinaries isn't supported yet"
        elif factory_type == ItemEnum.ChemicalPlant or factory_type == ItemEnum.QuantumChemicalPlant:
            assert True, "Chemical plants labs isn't supported yet"
        else:
            assert True, "Unsupported factory type: " + factory_type
    
    def _get_belt_offset(factory_type, side):
        if side == "top":
            return Pos(y = self.get_top_belt_y_offset(factory_type))
        elif side == "buttom":
            return Pos(y = self.get_buttom_belt_y_offset(factory_type))
    
    def _get_top_belt_offset(factory_type):
        if factory_type == ItemEnum.ArcSmelter or factory_type == ItemEnum.PlaneSmelter or factory_type == ItemEnum.NegentrophySmelter:
            return Pos(y = 2)
        elif factory_type == ItemEnum.AssemblingMachineMkI or factory_type == ItemEnum.AssemblingMachineMkII or factory_type == ItemEnum.AssemblingMachineMkIII or factory_type == ItemEnum.ReComposingAssembler:
            return Pos(y = 2)
        elif factory_type == ItemEnum.MatrixLab or factory_type == ItemEnum.SelfEvolutionLab:
            assert True, "Matrix labs isn't supported yet"
        elif factory_type == ItemEnum.OilRefinary:
            assert True, "Oil refinaries isn't supported yet"
        elif factory_type == ItemEnum.ChemicalPlant or factory_type == ItemEnum.QuantumChemicalPlant:
            assert True, "Chemical plants labs isn't supported yet"
        else:
            assert True, "Unsupported factory type: " + factory_type
    
    def _get_buttom_belt_offset(factory_type):
        if factory_type == ItemEnum.ArcSmelter or factory_type == ItemEnum.PlaneSmelter or factory_type == ItemEnum.NegentrophySmelter:
            return Pos(y = -2)
        elif factory_type == ItemEnum.AssemblingMachineMkI or factory_type == ItemEnum.AssemblingMachineMkII or factory_type == ItemEnum.AssemblingMachineMkIII or factory_type == ItemEnum.ReComposingAssembler:
            return Pos(y = -2)
        elif factory_type == ItemEnum.MatrixLab or factory_type == ItemEnum.SelfEvolutionLab:
            assert True, "Matrix labs isn't supported yet"
        elif factory_type == ItemEnum.OilRefinary:
            assert True, "Oil refinaries isn't supported yet"
        elif factory_type == ItemEnum.ChemicalPlant or factory_type == ItemEnum.QuantumChemicalPlant:
            assert True, "Chemical plants labs isn't supported yet"
        else:
            assert True, "Unsupported factory type: " + factory_type
        
    def _get_factory_offset(factory_type):
        if factory_type == ItemEnum.ArcSmelter or factory_type == ItemEnum.PlaneSmelter or factory_type == ItemEnum.NegentrophySmelter:
            return Pos(x = 1)
        elif factory_type == ItemEnum.AssemblingMachineMkI or factory_type == ItemEnum.AssemblingMachineMkII or factory_type == ItemEnum.AssemblingMachineMkIII or factory_type == ItemEnum.ReComposingAssembler:
            return Pos(x = 1)
        elif factory_type == ItemEnum.MatrixLab or factory_type == ItemEnum.SelfEvolutionLab:
            assert True, "Matrix labs isn't supported yet"
        elif factory_type == ItemEnum.OilRefinary:
            assert True, "Oil refinaries isn't supported yet"
        elif factory_type == ItemEnum.ChemicalPlant or factory_type == ItemEnum.QuantumChemicalPlant:
            assert True, "Chemical plants labs isn't supported yet"
        else:
            assert True, "Unsupported factory type: " + factory_type
    