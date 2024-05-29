from ItemEnum import ItemEnum

class Recipe:
    def __init__(self, name, input_items, output_items, time, tool, recipe_id):
        self.name = name
        self.input_items = input_items
        self.output_items = output_items
        self.time = time
        self.tool = tool
        self.recipe_id = recipe_id

    def __str__(self):
        return f'Name: {self.name} - Input item: {self.input_items} - Output items: {self.output_items} - Time: {self.time}s - Tool: {self.tool} - Recipe id: {self.recipe_id}'

recipes = {

    # Smelting Facility
    ItemEnum.IronIngot: Recipe(ItemEnum.IronIngot, {ItemEnum.IronOre: 1}, {ItemEnum.IronIngot: 1}, 1, "Smelting Facility", 1),
    ItemEnum.CopperIngot: Recipe(ItemEnum.CopperIngot, {ItemEnum.CopperOre: 1}, {ItemEnum.CopperIngot: 1}, 1, "Smelting Facility", 3),
    ItemEnum.StoneBrick: Recipe(ItemEnum.StoneBrick, {ItemEnum.Stone: 1}, {ItemEnum.StoneBrick: 1}, 1, "Smelting Facility", None),
    ItemEnum.EnergeticGraphite: Recipe(ItemEnum.EnergeticGraphite, {ItemEnum.Coal: 2}, {ItemEnum.EnergeticGraphite: 1}, 2, "Smelting Facility", None),
    ItemEnum.HighPuritySilicon : Recipe(ItemEnum.HighPuritySilicon, {ItemEnum.SiliconOre: 2}, {ItemEnum.HighPuritySilicon: 1}, 2, "Smelting Facility", 59),
    ItemEnum.TitaniumIngot: Recipe(ItemEnum.TitaniumIngot, {ItemEnum.TitaniumOre: 2}, {ItemEnum.TitaniumIngot: 1}, 2, "Smelting Facility", None),

    ItemEnum.Magnet: Recipe(ItemEnum.Magnet, {ItemEnum.IronOre: 1}, {ItemEnum.Magnet: 1}, 1.5, "Smelting Facility", 2),
    ItemEnum.MagneticCoil: Recipe(ItemEnum.MagneticCoil, {ItemEnum.Magnet: 2, ItemEnum.CopperIngot: 1}, {ItemEnum.MagneticCoil: 2}, 1, "Assembling machine", 6),
    ItemEnum.Glass: Recipe(ItemEnum.Glass, {ItemEnum.Stone: 2}, {ItemEnum.Glass: 1}, 2, "Smelting Facility", None),
    ItemEnum.Diamond: Recipe(ItemEnum.Diamond, {ItemEnum.EnergeticGraphite: 1}, {ItemEnum.Diamond: 1}, 2, "Smelting Facility", None),
    ItemEnum.CrystalSilicon: Recipe(ItemEnum.CrystalSilicon, {ItemEnum.HighPuritySilicon: 1}, {ItemEnum.CrystalSilicon: 1}, 2, "Smelting Facility", 37),
    ItemEnum.TitaniumAlloy: Recipe(ItemEnum.TitaniumAlloy, {ItemEnum.TitaniumIngot: 4, ItemEnum.Steel: 4, "Sulfuric Acid": 8}, {ItemEnum.TitaniumAlloy: 4}, 12, "Smelting Facility", None),
    
    ItemEnum.Steel: Recipe(ItemEnum.Steel, {ItemEnum.IronIngot: 3}, {ItemEnum.Steel: 1}, 3, "Smelting Facility", 63),
    ItemEnum.CircuitBoard: Recipe(ItemEnum.CircuitBoard, {ItemEnum.IronIngot: 2, ItemEnum.CopperIngot: 1}, {ItemEnum.CircuitBoard: 2}, 1, "Assembling machine", None),
    ItemEnum.Prism: Recipe(ItemEnum.Prism, {ItemEnum.Glass: 3}, {ItemEnum.Prism: 2}, 2, "Assembling machine", None),
    ItemEnum.ElectricMotor: Recipe(ItemEnum.ElectricMotor, {ItemEnum.IronIngot: 2, ItemEnum.Gear: 1, ItemEnum.MagneticCoil: 1}, {ItemEnum.ElectricMotor: 1}, 2, "Assembling machine", None),
    ItemEnum.MicrocrystallineComponent: Recipe(ItemEnum.MicrocrystallineComponent, {ItemEnum.HighPuritySilicon: 2, ItemEnum.CopperIngot: 1}, {ItemEnum.MicrocrystallineComponent: 1}, 2, "Assembling machine", None),
    ItemEnum.ProliferatorMkI: Recipe(ItemEnum.ProliferatorMkI, {ItemEnum.Coal: 1}, {ItemEnum.ProliferatorMkI: 1}, 0.5, "Assembling machine", None),

    ItemEnum.Gear: Recipe(ItemEnum.Gear, {ItemEnum.IronIngot: 1}, {ItemEnum.Gear: 1}, 1, "Assembling machine", 5),
    ItemEnum.PlasmaExciter: Recipe(ItemEnum.PlasmaExciter, {ItemEnum.MagneticCoil: 4, ItemEnum.Prism: 2}, {ItemEnum.PlasmaExciter: 1}, 2, "Assembling machine", None),
    ItemEnum.PhotonCombiner: Recipe(ItemEnum.PhotonCombiner, {ItemEnum.Prism: 2, ItemEnum.CircuitBoard: 1}, {ItemEnum.PhotonCombiner: 1}, 3, "Assembling machine", None),
    ItemEnum.ElectromagneticTurbine: Recipe(ItemEnum.ElectromagneticTurbine, {ItemEnum.Gear: 2, ItemEnum.MagneticCoil: 2}, {ItemEnum.ElectromagneticTurbine: 1}, 2, "Assembling machine", None),
    ItemEnum.Processor: Recipe(ItemEnum.Processor, {ItemEnum.CircuitBoard: 2, ItemEnum.MicrocrystallineComponent: 2}, {ItemEnum.Processor: 1}, 3, "Assembling machine", None),
    ItemEnum.ProliferatorMkII: Recipe(ItemEnum.ProliferatorMkII, {ItemEnum.ProliferatorMkI: 2, ItemEnum.Diamond: 1}, {ItemEnum.ProliferatorMkII: 1}, 1, "Assembling machine", None),

    ItemEnum.Engine: Recipe(ItemEnum.Engine, {ItemEnum.MagneticCoil: 2, ItemEnum.CopperIngot: 1}, {ItemEnum.Engine: 1}, 3, "Assembling machine", None),
    ItemEnum.Thruster: Recipe(ItemEnum.Thruster, {ItemEnum.Steel: 2, ItemEnum.CopperIngot: 3}, {ItemEnum.Thruster: 1}, 4, "Assembling machine", None),
    ItemEnum.ReinforcedThruster: Recipe(ItemEnum.ReinforcedThruster, {ItemEnum.TitaniumAlloy: 5, ItemEnum.ElectromagneticTurbine: 5}, {ItemEnum.ReinforcedThruster: 1}, 8, "Assembling machine", None),
    ItemEnum.SuperMagneticRing: Recipe(ItemEnum.SuperMagneticRing, {ItemEnum.ElectromagneticTurbine: 2, ItemEnum.Magnet: 3, ItemEnum.EnergeticGraphite: 1}, {ItemEnum.SuperMagneticRing: 1}, 3, "Assembling machine", None),
    ItemEnum.ParticleContainer: Recipe(ItemEnum.ParticleContainer, {ItemEnum.ElectromagneticTurbine: 2, ItemEnum.IronIngot: 2, "Graphene": 2}, {ItemEnum.ParticleContainer: 1}, 4, "Assembling machine", None),
    ItemEnum.ProliferatorMkIII: Recipe(ItemEnum.ProliferatorMkIII, {ItemEnum.ProliferatorMkII: 2, "Carbon Nanotube": 1}, {ItemEnum.ProliferatorMkIII: 1}, 2, "Assembling machine", None),

    # Reserved for Logistic bot
    # Reserved for Logistic drone
    # Reserved for Interstellar Logistic Vessel
    # Reserved for Space warper
    ItemEnum.GravitationLens: Recipe(ItemEnum.GravitationLens, {ItemEnum.Diamond: 4, "Strange Matter": 1}, {ItemEnum.GravitationLens: 1}, 6, "Assembling machine", None),
    ItemEnum.Foundation: Recipe(ItemEnum.Foundation, {ItemEnum.StoneBrick: 3, ItemEnum.Steel: 1}, {ItemEnum.Foundation: 1}, 1, "Assembling machine", None),
    
    ItemEnum.ElectromagneticMatrix: Recipe(ItemEnum.ElectromagneticMatrix, {ItemEnum.MagneticCoil: 1, "Electronic Circuit": 1}, {ItemEnum.ElectromagneticMatrix: 1}, 3, "Assembling machine", None),
    ItemEnum.EnergyMatrix: Recipe(ItemEnum.EnergyMatrix, {ItemEnum.EnergeticGraphite: 2, ItemEnum.Hydrogen: 2}, {ItemEnum.EnergyMatrix}, 6, "Research facility", None),


    ItemEnum.SorterMKI: Recipe(ItemEnum.SorterMKI, {ItemEnum.IronIngot: 1, ItemEnum.CircuitBoard: 1}, {ItemEnum.SorterMKI: 2}, 1, "Assembing machine", None),
    ItemEnum.SorterMKII: Recipe(ItemEnum.SorterMKII, {ItemEnum.ElectricMotor: 2, ItemEnum.ElectricMotor: 1}, {ItemEnum.SorterMKII: 2}, 1, "Assembing machine", None),
    ItemEnum.SorterMKIII: Recipe(ItemEnum.SorterMKIII, {ItemEnum.SorterMKII: 2, ItemEnum.ElectromagneticTurbine: 1}, {ItemEnum.SorterMKIII: 2}, 1, "Assembing machine", None),
    ItemEnum.PileSorter: Recipe(ItemEnum.PileSorter, {ItemEnum.SorterMKIII: 2, ItemEnum.SuperMagneticRing: 1, ItemEnum.Processor: 1}, {ItemEnum.PileSorter: 1}, 1, "Assembling machine", None),
}
# Reserved for Structure matrix
# Reserved for Information matrix
# Reserved for Gravity matrix
# Reserved for Universe matrix

"""
# Chemical Plant
ItemEnum.Plastic: Recipe(ItemEnum.Plastic, {"Refined Oil": 2, ItemEnum.EnergeticGraphite: 1}, {ItemEnum.Plastic: 1}, 3, "Chemical Plant", None),
"Sulfuric Acid": Recipe("Sulfuric Acid", {"Refined Oil": 6, ItemEnum.Stone: 8, "Water": 4}, {"Sulfuric Acid": 4}, 6, "Chemical Plant", None),
"Organic Crystal": Recipe("Organic Crystal", {ItemEnum.Plastic: 2, "Refined Oil": 1, "Water": 1}, {"Organic Crystal": 1}, 6, "Chemical Plant", None),
"Graphene": Recipe("Graphene", {ItemEnum.EnergeticGraphite: 3, "Sulfuric Acid": 1}, {"Graphene": 2}, 3, "Chemical Plant", None),
"Titanium Crystal": Recipe("Titanium Crystal", {ItemEnum.TitaniumIngot: 3, "Organic Crystal": 1}, {"Titanium Crystal": 1}, 4, "Chemical Plant", None),

# Assembling machine

# Oil Refinery
"Refined Oil": Recipe("Refined Oil", {"Crude Oil": 2}, {"Refined Oil": 2, "Hydrogen": 1}, 4, "Oil Refinery", None),

# Particle Collider
"Deuterium": Recipe("Deuterium", {"Hydrogen": 10}, {"Deuterium": 1}, 5, "Particle Collider", None),
"Strange Matter": Recipe("Strange Matter", {ItemEnum.IronIngot: 2, "Deuterium": 10, ItemEnum.ParticleContainer: 1}, {"Strange Matter": 1}, 8, "Particle Collider", None),
"""