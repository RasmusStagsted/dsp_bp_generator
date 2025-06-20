from dsp_bp_generator.factory_generator.recipes import Recipe

class Proliferator:
    NUMBER_OF_SPRAYS = 0
    PRODUCTIVITY = 1.0
    SPEED = 1.0
    ENERGY_CONSUMPTION = 1.0
    
class ProliferatorMKI(Proliferator):
    NUMBER_OF_SPRAYS = 13
    PRODUCTIVITY = 1.125
    SPEED = 1.25
    ENERGY_CONSUMPTION = 1.3
    
class ProliferatorMKII(Proliferator):
    NUMBER_OF_SPRAYS = 24
    PRODUCTIVITY = 1.2
    SPEED = 1.5
    ENERGY_CONSUMPTION = 1.7
    
class ProliferatorMKIII(Proliferator):
    NUMBER_OF_SPRAYS = 60
    PRODUCTIVITY = 1.25
    SPEED = 2
    ENERGY_CONSUMPTION = 2.5

if __name__ == "__main__":
    
    # Example usage
    recipe = Recipe.select("IronIngot")

    proliferator = ProliferatorMKI
    througput_mk1 = proliferator.SPEED * recipe.input_items["IronOre"]
    print(f"Ingredient throughput with Proliferator MKI: {througput_mk1} items/s")
    product_throughput_mk1 = proliferator.SPEED * proliferator.PRODUCTIVITY * recipe.output_items["IronIngot"]
    print(f"Product throughput with Proliferator MKI: {product_throughput_mk1} items/s")
    
    proliferator_mk2 = ProliferatorMKII
    througput_mk2 = ProliferatorMKII.SPEED * recipe.input_items["IronOre"]
    print(f"Ingredient throughput with Proliferator MKII: {througput_mk2} items/s")
    product_throughput_mk2 = ProliferatorMKII.SPEED * ProliferatorMKII.PRODUCTIVITY * recipe.output_items["IronIngot"]
    print(f"Product throughput with Proliferator MKII: {product_throughput_mk2} items/s")
    
    proliferator_mk3 = ProliferatorMKIII
    througput_mk3 = ProliferatorMKIII.SPEED * recipe.input_items["IronOre"]
    print(f"Ingredient throughput with Proliferator MKIII: {througput_mk3} items/s")
    product_throughput_mk3 = ProliferatorMKIII.SPEED * ProliferatorMKIII.PRODUCTIVITY * recipe.output_items["IronIngot"]
    print(f"Product throughput with Proliferator MKIII: {product_throughput_mk3} items/s")