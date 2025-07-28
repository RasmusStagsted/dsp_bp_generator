import pytest
from .recipes import Recipe

# test_recipes.py

def test_recipe_creation_and_str():
    recipe = Recipe(
        name="Test Recipe",
        input_items=["item1", "item2"],
        output_items=["item3"],
        time=10,
        tool="Assembler",
        recipe_id=123
    )
    assert recipe.name == "Test Recipe"
    assert recipe.input_items == ["item1", "item2"]
    assert recipe.output_items == ["item3"]
    assert recipe.time == 10
    assert recipe.tool == "Assembler"
    assert recipe.recipe_id == 123
    expected_str = "Name: Test Recipe - Input item: ['item1', 'item2'] - Output items: ['item3'] - Time: 10s - Tool: Assembler - Recipe id: 123"
    assert str(recipe) == expected_str

def test_select(monkeypatch):
    # Mock recipes dictionary
    mock_recipe = Recipe("Mock", [], [], 1, "Tool", 1)
    Recipe.recipes = {"mock_item": mock_recipe}
    selected = Recipe.select("mock_item")
    assert selected is mock_recipe

def test_load_from_yaml(monkeypatch):
    # Mock pkgutil.get_data to return YAML bytes
    sample_yaml = b"""
test_recipe:
  name: Test
  input_items: [a]
  output_items: [b]
  time: 1
  tool: Tool
  recipe_id: 1
"""
    monkeypatch.setattr("pkgutil.get_data", lambda package, filename: sample_yaml)
    data = Recipe.load_from_yaml("dummy.yaml")
    assert "test_recipe" in data
    assert data["test_recipe"]["name"] == "Test"