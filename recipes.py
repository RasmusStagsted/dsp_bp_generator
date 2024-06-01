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

def load_from_yaml(filename):
    with open(filename, "r") as file:
        return yaml.safe_load(file)

recipes = load_from_yaml("recipes.yaml")
    
if __name__ == "__main__":
    filename = "recipes.yaml"
    save_to_yaml(recipes, filename)
    recipes = load_from_yaml(filename)
    print(recipes)