from .recipes import recipes

class ItemFlow:

    def __init__(self, name, count_pr_sec):
        self.name = name
        self.count_pr_sec = count_pr_sec

    def get_ingredients(self, prolifirator = None):

        if prolifirator == "Mk.I":
            scale = 1/0.95
        elif prolifirator == "Mk.II":
            scale = 1/0.88
        elif prolifirator == "Mk.III":
            scale = 1/0.8
        else:
            scale = 1
        
        recipe = recipes[self.name]
            
        if recipe == None: # Assumes that is a raw material
            return []

        ingredients = []

        for input_item, input_item_count in recipe["input_items"].items():
            ingredients.append(ItemFlow(input_item, input_item_count * self.count_pr_sec * scale / recipe["output_items"][self.name]))

        return ingredients
    
    def get_waste_products(self):
        assert "Does not support recipes with multyple outputs"
        return []
