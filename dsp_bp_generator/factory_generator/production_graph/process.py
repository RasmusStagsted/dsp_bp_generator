from dataclasses import dataclass
from dsp_bp_generator.factory_generator.recipes import Recipe
from dsp_bp_generator.factory_generator.proliferator import ProliferatorNone

@dataclass
class Process:
    
    def __init__(self, name: str, recipe: Recipe, factory_count: int = 1, output_proliferator: str = ProliferatorNone):
        self.name = name
        self.recipe = recipe
        self.factory_count = factory_count
        self.output_proliferator = output_proliferator
        self.input_connections = []
        self.output_connections = []

    def update_factory_count(self):
        pass

    def add_input(self, input_flow):
        if input_flow not in self.inputs:
            self.inputs.append(input_flow)
    
    def add_output(self, output_flow):
        if output_flow not in self.outputs:
            self.outputs.append(output_flow)
    
    def set_output_proliferator(self, proliferator):
        self.output_proliferator = proliferator
        for output_flow in self.outputs:
            output_flow.set_proliferator(proliferator)
    
    def update(self, output_flow):
        pass
        # Update outputs
        
        
        # Update factory count
        
        # Update inputs
    
    def __str__(self):
        return (
            f"[Process] {self.name}\n"
            f"  Recipe: {self.recipe.name}\n"
            f"  Factory count: {self.factory_count}\n"
            f"  Output proliferator: {self.output_proliferator}\n"
            f"  Inputs: {', '.join([connection.name for connection in self.input_connections]) if self.input_connections else 'None'}\n"
            f"  Outputs: {', '.join([connection.name for connection in self.output_connections]) if self.output_connections else 'None'}"
        )