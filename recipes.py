import yaml

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

def save_to_yaml(recipes, filename):
    with open(filename, 'w') as file:
        file.write("---\n")
        for recipe_name, recipe in recipes.items():
            file.write(ItemEnum(recipe_name).name + ":\n")
            if isinstance(recipe, list):
                for r in recipe:
                    file.write(f"  - name: {r.name}\n")
                    file.write(f"    inputs:\n")
                    for item_name, item_count in r.input_items.items():
                        file.write(f"      {item_name.name}: {item_count}\n")
                    file.write(f"    outputs:\n")
                    print(r.output_items)
                    for item_name, item_count in r.output_items.items():
                        print(item_name)
                        file.write(f"      {item_name.name}: {item_count}\n")
                    file.write(f"    time: {r.time}\n")
                    file.write(f"    tool: {r.tool}\n")
                    file.write(f"    recipe_id: {r.recipe_id}\n")
            else:
                if recipe == None:
                    continue
                file.write(f"  name: {recipe.name}\n")
                file.write(f"  inputs:\n")
                for item_name, item_count in recipe.input_items.items():
                    file.write(f"    {item_name.name}: {item_count}\n")
                file.write(f"  outputs:\n")
                print(recipe.output_items)
                for item_name, item_count in recipe.output_items.items():
                    print(item_name)
                    file.write(f"    {item_name.name}: {item_count}\n")
                file.write(f"  time: {recipe.time}\n")
                file.write(f"  tool: {recipe.tool}\n")
                file.write(f"  recipe_id: {recipe.recipe_id}\n")

def load_from_yaml(filename):
    with open(filename, "r") as file:
        return yaml.safe_load(file)

recipes = load_from_yaml("recipes.yaml")
    
"""
recipes = {

    ################
    ## Components ##
    ################

    # Row I
    ItemEnum.IronOre: None,
    ItemEnum.CopperOre: None,
    ItemEnum.Stone: None,
    ItemEnum.Coal: None,
    ItemEnum.SiliconOre: None,
    ItemEnum.TitaniumOre: None,
    ItemEnum.Water: None,
    ItemEnum.CrudeOil: None,
    ItemEnum.Hydrogen: [
        Recipe("Gaphene (Advanced)", {ItemEnum.FireIce: 2}, {ItemEnum.Graphene: 2, ItemEnum.Hydrogen: 1}, 2, "Chemical Facility", None),
        Recipe("Deuterium Fractionation", {ItemEnum.Hydrogen: 1}, {ItemEnum.Deuterium: 0.01, ItemEnum.Hydrogen: 0.99}, 0.017, "Fractionation Facility", None),
        Recipe("Mass-Energy Storage", {ItemEnum.CriticalPhoton: 2}, {ItemEnum.Antimatter: 2, ItemEnum.Hydrogen: 2}, 2, "Particle Collider", None),
        Recipe("Plasma Refining", {ItemEnum.CrudeOil: 2}, {ItemEnum.Hydrogen: 1, ItemEnum.RefinedOil: 2}, 4, "Refining Facility", None),
        Recipe("X-Ray Cracking", {ItemEnum.RefinedOil: 1, ItemEnum.Hydrogen: 2}, {ItemEnum.Hydrogen: 3, ItemEnum.EnergeticGraphite: 1}, 2, "Refining Facility", None),
    ],
    ItemEnum.Deuterium: Recipe("Deuterium Fractionation", {ItemEnum.Hydrogen: 1}, {ItemEnum.Deuterium: 0.01, ItemEnum.Hydrogen: 0.99}, 0.017, "Fractionation Facility", None),
    ItemEnum.Antimatter: Recipe("Mass-Energy Storage", {ItemEnum.CriticalPhoton: 2}, {ItemEnum.Antimatter: 2, ItemEnum.Hydrogen: 2}, 2, "Particle Collider", None),
    ItemEnum.CoreElement: None,
    ItemEnum.CriticalPhoton: None,
    ItemEnum.KimberliteOre: None,
    
    # Row II
    ItemEnum.IronIngot: Recipe("Iron Ingot", {ItemEnum.IronOre: 1}, {ItemEnum.IronIngot: 1}, 1, "Smelting Facility", 1),
    ItemEnum.CopperIngot: Recipe("Copper Ingot", {ItemEnum.CopperOre: 1}, {ItemEnum.CopperIngot: 1}, 1, "Smelting Facility", 3),
    ItemEnum.StoneBrick: Recipe("Stone Brick", {ItemEnum.Stone: 1}, {ItemEnum.StoneBrick: 1}, 1, "Smelting Facility", None),
    ItemEnum.EnergeticGraphite: Recipe("Energetic Graphite", {ItemEnum.Coal: 2}, {ItemEnum.EnergeticGraphite: 1}, 2, "Smelting Facility", None),
    ItemEnum.HighPuritySilicon : Recipe("High Purity Silicon", {ItemEnum.SiliconOre: 2}, {ItemEnum.HighPuritySilicon: 1}, 2, "Smelting Facility", 59),
    ItemEnum.TitaniumIngot: Recipe("Titanium Ingot", {ItemEnum.TitaniumOre: 2}, {ItemEnum.TitaniumIngot: 1}, 2, "Smelting Facility", None),
    ItemEnum.SulfuricAcid: Recipe("Sulfuric Acid", {ItemEnum.RefinedOil: 6, ItemEnum.Stone: 8, ItemEnum.Water: 4}, {ItemEnum.SulfuricAcid: 4}, 6, "Chemical Plant", None),
    ItemEnum.RefinedOil: [
        Recipe("Plasma Refining", {ItemEnum.CrudeOil: 2}, {ItemEnum.Hydrogen: 1, ItemEnum.RefinedOil: 2}, 4, "Refining Facility", None),
        Recipe("Reformed Refinement", {ItemEnum.RefinedOil: 2, ItemEnum.Hydrogen: 1, ItemEnum.Coal: 1}, {ItemEnum.RefinedOil: 3}, 4, "Refining Facility", None)
    ],
    ItemEnum.HydrogenFuelRod: Recipe("Hydrogen Fuel Rod", {ItemEnum.TitaniumIngot: 1, ItemEnum.Hydrogen: 10}, {ItemEnum.HydrogenFuelRod: 2}, 6, "Assembler", None),
    ItemEnum.DeuteronFuelRod: Recipe("Deuteron Fuel Rod", {ItemEnum.TitaniumAlloy: 1, ItemEnum.Deuterium: 20, ItemEnum.SuperMagneticRing: 1}, {ItemEnum.DeuteronFuelRod: 2}, 12, "Assembler", None),
    ItemEnum.AntimatterFuelRod: Recipe("Antimatter Fuel Rod", {ItemEnum.Antimatter: 12, ItemEnum.Hydrogen: 12, ItemEnum.AnnihilationConstraintSphere: 1, ItemEnum.TitaniumAlloy: 1}, {ItemEnum.AntimatterFuelRod: 2}, 24, "Assembler", None),
    ItemEnum.StrangeAnnihilationFuelRod: Recipe("Strange Annihilation Fuel Rod", {ItemEnum.AntimatterFuelRod: 8, ItemEnum.CoreElement: 1, ItemEnum.StrangeMatter: 2, ItemEnum.FrameMaterial: 1}, {ItemEnum.StrangeAnnihilationFuelRod: 1}, 32, "Assembler", None),
    ItemEnum.MissileSet: Recipe("Missile Set", {ItemEnum.CopperIngot: 6, ItemEnum.CircuitBoard: 3, ItemEnum.CombustibleUnit: 2, ItemEnum.Engine: 1}, {ItemEnum.MissileSet: 1}, 2, "Assembler", None),
    ItemEnum.FractalSilicon: None,

    # Row III
    ItemEnum.Magnet: Recipe("Magnet", {ItemEnum.IronOre: 1}, {ItemEnum.Magnet: 1}, 1.5, "Smelting Facility", 2),
    ItemEnum.MagneticCoil: Recipe("Magnetic Coil", {ItemEnum.Magnet: 2, ItemEnum.CopperIngot: 1}, {ItemEnum.MagneticCoil: 2}, 1, "Assembling machine", 6),
    ItemEnum.Glass: Recipe("Glass", {ItemEnum.Stone: 2}, {ItemEnum.Glass: 1}, 2, "Smelting Facility", None),
    ItemEnum.Diamond: Recipe("Diamond", {ItemEnum.EnergeticGraphite: 1}, {ItemEnum.Diamond: 1}, 2, "Smelting Facility", None),
    ItemEnum.CrystalSilicon: Recipe("Crystal Silicone", {ItemEnum.HighPuritySilicon: 1}, {ItemEnum.CrystalSilicon: 1}, 2, "Smelting Facility", 37),
    ItemEnum.TitaniumAlloy: Recipe("Titanium Alloy", {ItemEnum.TitaniumIngot: 4, ItemEnum.Steel: 4, ItemEnum.SulfuricAcid: 8}, {ItemEnum.TitaniumAlloy: 4}, 12, "Smelting Facility", None),
    # TODO

    # Row IV
    ItemEnum.Steel: Recipe("Steel", {ItemEnum.IronIngot: 3}, {ItemEnum.Steel: 1}, 3, "Smelting Facility", 63),
    ItemEnum.CircuitBoard: Recipe("Circuit Board", {ItemEnum.IronIngot: 2, ItemEnum.CopperIngot: 1}, {ItemEnum.CircuitBoard: 2}, 1, "Assembling machine", None),
    ItemEnum.Prism: Recipe("Prism", {ItemEnum.Glass: 3}, {ItemEnum.Prism: 2}, 2, "Assembling machine", None),
    ItemEnum.ElectricMotor: Recipe("Electric Motor", {ItemEnum.IronIngot: 2, ItemEnum.Gear: 1, ItemEnum.MagneticCoil: 1}, {ItemEnum.ElectricMotor: 1}, 2, "Assembling machine", None),
    ItemEnum.MicrocrystallineComponent: Recipe("Microcrystalline Component", {ItemEnum.HighPuritySilicon: 2, ItemEnum.CopperIngot: 1}, {ItemEnum.MicrocrystallineComponent: 1}, 2, "Assembling machine", None),
    ItemEnum.ProliferatorMkI: Recipe("Proliferator Mk.I", {ItemEnum.Coal: 1}, {ItemEnum.ProliferatorMkI: 1}, 0.5, "Assembling machine", None),
    # TODO

    # Row V
    ItemEnum.Gear: Recipe("Gear", {ItemEnum.IronIngot: 1}, {ItemEnum.Gear: 1}, 1, "Assembling machine", 5),
    ItemEnum.PlasmaExciter: Recipe("Plasma Exciter", {ItemEnum.MagneticCoil: 4, ItemEnum.Prism: 2}, {ItemEnum.PlasmaExciter: 1}, 2, "Assembling machine", None),
    ItemEnum.PhotonCombiner: Recipe("Photon Combiner", {ItemEnum.Prism: 2, ItemEnum.CircuitBoard: 1}, {ItemEnum.PhotonCombiner: 1}, 3, "Assembling machine", None),
    ItemEnum.ElectromagneticTurbine: Recipe("Electromagnetic Turbine", {ItemEnum.Gear: 2, ItemEnum.MagneticCoil: 2}, {ItemEnum.ElectromagneticTurbine: 1}, 2, "Assembling machine", None),
    ItemEnum.Processor: Recipe("Processor", {ItemEnum.CircuitBoard: 2, ItemEnum.MicrocrystallineComponent: 2}, {ItemEnum.Processor: 1}, 3, "Assembling machine", None),
    ItemEnum.ProliferatorMkII: Recipe("Proliferator Mk.II", {ItemEnum.ProliferatorMkI: 2, ItemEnum.Diamond: 1}, {ItemEnum.ProliferatorMkII: 1}, 1, "Assembling machine", None),
    # TODO

    # Row VI
    ItemEnum.Engine: Recipe("Engine", {ItemEnum.MagneticCoil: 2, ItemEnum.CopperIngot: 1}, {ItemEnum.Engine: 1}, 3, "Assembling machine", None),
    ItemEnum.Thruster: Recipe("Thruster", {ItemEnum.Steel: 2, ItemEnum.CopperIngot: 3}, {ItemEnum.Thruster: 1}, 4, "Assembling machine", None),
    ItemEnum.ReinforcedThruster: Recipe("Reinforced Thruster", {ItemEnum.TitaniumAlloy: 5, ItemEnum.ElectromagneticTurbine: 5}, {ItemEnum.ReinforcedThruster: 1}, 8, "Assembling machine", None),
    ItemEnum.SuperMagneticRing: Recipe("SuperMagnetic Ring", {ItemEnum.ElectromagneticTurbine: 2, ItemEnum.Magnet: 3, ItemEnum.EnergeticGraphite: 1}, {ItemEnum.SuperMagneticRing: 1}, 3, "Assembling machine", None),
    ItemEnum.ParticleContainer: Recipe("Particle Container", {ItemEnum.ElectromagneticTurbine: 2, ItemEnum.IronIngot: 2, ItemEnum.Graphene: 2}, {ItemEnum.ParticleContainer: 1}, 4, "Assembling machine", None),
    ItemEnum.ProliferatorMkIII: Recipe("Proliferator Mk.III", {ItemEnum.ProliferatorMkII: 2, ItemEnum.CarbonNanotube: 1}, {ItemEnum.ProliferatorMkIII: 1}, 2, "Assembling machine", None),
    # TODO

    # Row VII
    # Reserved for Logistic bot
    # Reserved for Logistic drone
    # Reserved for Interstellar Logistic Vessel
    # Reserved for Space warper
    ItemEnum.GravitationLens: Recipe("Gravitation Lens", {ItemEnum.Diamond: 4, ItemEnum.StrangeMatter: 1}, {ItemEnum.GravitationLens: 1}, 6, "Assembling machine", None),
    ItemEnum.Foundation: Recipe("Foundation", {ItemEnum.StoneBrick: 3, ItemEnum.Steel: 1}, {ItemEnum.Foundation: 1}, 1, "Assembling machine", None),
    # TODO

    # Row VIII
    ItemEnum.ElectromagneticMatrix: Recipe("Electromagnetic Matrix", {ItemEnum.MagneticCoil: 1, ItemEnum.CircuitBoard: 1}, {ItemEnum.ElectromagneticMatrix: 1}, 3, "Assembling machine", None),
    ItemEnum.EnergyMatrix: Recipe("Energy Matrix", {ItemEnum.EnergeticGraphite: 2, ItemEnum.Hydrogen: 2}, {ItemEnum.EnergyMatrix: 1}, 6, "Research facility", None),
    # TODO

    ###############
    ## Buildings ##
    ###############

    # Row I
    # TODO

    # Row II
    # TODO

    # Row III
    ItemEnum.SorterMKI: Recipe("Sorter MK.I", {ItemEnum.IronIngot: 1, ItemEnum.CircuitBoard: 1}, {ItemEnum.SorterMKI: 2}, 1, "Assembing machine", 85),
    ItemEnum.SorterMKII: Recipe("Sorter MK.II", {ItemEnum.ElectricMotor: 2, ItemEnum.ElectricMotor: 1}, {ItemEnum.SorterMKII: 2}, 1, "Assembing machine", 88),
    ItemEnum.SorterMKIII: Recipe("Sorter MK.III", {ItemEnum.SorterMKII: 2, ItemEnum.ElectromagneticTurbine: 1}, {ItemEnum.SorterMKIII: 2}, 1, "Assembing machine", 90),
    ItemEnum.PileSorter: Recipe("Pile Sorter", {ItemEnum.SorterMKIII: 2, ItemEnum.SuperMagneticRing: 1, ItemEnum.Processor: 1}, {ItemEnum.PileSorter: 1}, 1, "Assembling machine", 160),
    # TODO
    
    # Row IV
    # TODO

    # Row V
    # TODO
}
"""

if __name__ == "__main__":
    filename = "recipes.yaml"
    save_to_yaml(recipes, filename)
    recipes = load_from_yaml(filename)
    print(recipes)