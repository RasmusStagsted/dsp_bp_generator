import logging
from .recipes import Recipe

class ItemFlow:

    def __init__(self, name, count_pr_sec):
        self.name = name
        self.count_pr_sec = count_pr_sec

    def select_recipe(self, item_name):
        return Recipe.select(item_name)

    def get_needed_ingredients(self, proliferator = None):
        if proliferator == "Mk.I":
            scale = 1.0 / 1.125
        elif proliferator == "Mk.II":
            scale = 1.0 / 1.20
        elif proliferator == "Mk.III":
            scale = 1.0 / 1.25
        else:
            scale = 1

        if not hasattr(self, "recipe"):
            self.recipe = self.select_recipe(self.name)

        if self.recipe is None:  # Assumes that this is a raw material
            logging.warning(f"No recipe found for {self.name}")
            return []

        ingredients = []
        output_count = self.recipe["output_items"].get(self.name, 1)
        if output_count == 0:
            logging.warning(f"Output count for {self.name} is zero. Skipping ingredient calculation.")
            return []

        for input_item, input_item_count in self.recipe["input_items"].items():
            ingredients.append(ItemFlow(input_item, input_item_count * self.count_pr_sec * scale / output_count))

        return ingredients

    def get_products(self):
        if not hasattr(self, "recipe"):
            self.recipe = self.select_recipe(self.name)

        if self.recipe is None:  # Assumes that this is a raw material
            logging.warning(f"No recipe found for {self.name}")
            return []

        products = []
        output_count = self.recipe["output_items"].get(self.name, 1)
        if output_count == 0:
            logging.warning(f"Output count for {self.name} is zero. Skipping product calculation.")
            return []

        for output_item, output_item_count in self.recipe["output_items"].items():
            products.append(ItemFlow(output_item, output_item_count * self.count_pr_sec / output_count))

        return products