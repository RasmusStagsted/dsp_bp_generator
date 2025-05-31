import yaml

import pkgutil 

class Recipe:

    recipes = None

    def __init__(self, name, input_items, output_items, time, tool, recipe_id):
        self.name = name
        self.input_items = input_items
        self.output_items = output_items
        self.time = time
        self.tool = tool
        self.recipe_id = recipe_id

    def __str__(self):
        return f'Name: {self.name} - Input item: {self.input_items} - Output items: {self.output_items} - Time: {self.time}s - Tool: {self.tool} - Recipe id: {self.recipe_id}'

    @staticmethod
    def load_from_yaml(filename):
        data = pkgutil.get_data(__package__, filename)
        if data is not None:
            raw_recipes = yaml.safe_load(data)
            recipes = {}
            for key, value in raw_recipes.items():
                if value is None:
                    #print(f"Warning: Recipe for '{key}' is None and will be skipped.")
                    continue
                if isinstance(value, list):
                    value = value[0] if value else None
                if value is None:
                    #print(f"Warning: Recipe for '{key}' is an empty list and will be skipped.")
                    continue
                recipes[key] = Recipe(
                    name = value.get('name', key),
                    input_items = value.get('input_items', {}),
                    output_items = value.get('output_items', {}),
                    time = value.get('time', 1),
                    tool = value.get('tool', ''),
                    recipe_id = value.get('recipe_id', None)
                )
            return recipes
        else:
            raise FileNotFoundError(f'{filename} not found in package')

    def get_item_from_recipe(self, item_name):
        # Accept both enum value and key (string)
        # Try to match by key (string)
        if isinstance(item_name, str):
            # Try direct string match
            if item_name in self.input_items:
                return (item_name, self.input_items[item_name])
            if item_name in self.output_items:
                return (item_name, self.output_items[item_name])
            # Try enum key match (case-insensitive)
            for k, v in self.input_items.items():
                if hasattr(k, 'name') and k.name.lower() == item_name.lower():
                    return (k, v)
            for k, v in self.output_items.items():
                if hasattr(k, 'name') and k.name.lower() == item_name.lower():
                    return (k, v)
        # Try enum value match
        for k, v in self.input_items.items():
            if item_name == k:
                return (k, v)
            if hasattr(k, 'value') and item_name == k.value:
                return (k, v)
        for k, v in self.output_items.items():
            if item_name == k:
                return (k, v)
            if hasattr(k, 'value') and item_name == k.value:
                return (k, v)
        return None

    def select(item_name):
        recipe = Recipe.recipes[item_name]
        if recipe == None:
            print("Recipe not found: " + item_name)
        return Recipe.recipes[item_name]

Recipe.recipes = Recipe.load_from_yaml("data/recipes.yaml")

if __name__ == "__main__":
    print(Recipe.recipes["Gear"])
    print(Recipe.recipes["Gear"].get_item_from_recipe("IronIngot"))