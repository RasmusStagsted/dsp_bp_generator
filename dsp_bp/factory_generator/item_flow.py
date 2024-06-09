from .recipes import Recipe

class ItemFlow:

    def __init__(self, name, count_pr_sec):
        self.name = name
        self.count_pr_sec = count_pr_sec

    def get_needed_ingredients(self, prolifirator = None):
        
        if prolifirator == "Mk.I":
            scale = 1.0/1.125
        elif prolifirator == "Mk.II":
            scale = 1.0/1.20
        elif prolifirator == "Mk.III":
            scale = 1.0/1.25
        else:
            scale = 1

        recipe = Recipe.select(self.name)
            
        if recipe == None: # Assumes that this is a raw material
            return []

        ingredients = []

        for input_item, input_item_count in recipe["input_items"].items():
            ingredients.append(ItemFlow(input_item, input_item_count * self.count_pr_sec * scale / recipe["output_items"][self.name]))

        return ingredients
    
    def get_products(self):
        
        recipe = Recipe.select(self.name)
        
        if recipe == None: # Assumes that this is a raw material
            return []

        products = []
        for output_item, output_item_count in recipe["output_items"].items():
            products.append(ItemFlow(output_item, output_item_count * self.count_pr_sec * scale / recipe["output_items"][self.name]))

        return products