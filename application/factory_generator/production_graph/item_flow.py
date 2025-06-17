from .connection import Connection
from ..proliferator import ProliferatorNone

from .graphical_node import GraphicalNode

class ItemFlow(GraphicalNode):

    def __init__(self, name: str, count_per_second: float = 0, proliferator: str = ProliferatorNone):
        self.name = name
        self.count_per_second = count_per_second
        self.proliferator = proliferator
        self.input_connections = []
        self.output_connections = []

    def get_total_output_throughput(self):
        count_per_sec = 0.0
        for connection in self.output_connections:
            count_per_sec += connection.count_per_sec
        return count_per_sec
    
    def get_total_input_throughput(self):
        count_per_sec = 0.0
        for connection in self.input_connections:
            count_per_sec += connection.count_per_sec
        return count_per_sec






    def add_destination(self, destination):
        if destination.__hash__() in [conn.destination.__hash__() for conn in self.output_connections]:
            raise ValueError(f"Destination {destination.name} already exists in output connections.")
        else:
            self.input_connections.append(Connection(
                name = self.name + " to " + destination.name,
                source = self,
                destination = destination
            ))
    
    def add_source(self, source):
        if source not in self.input_connections:
            self.input_connections.append(source)
    
    def update(self, throughput_diff: float): # Depending
        self.count_per_sec += throughput_diff
        if len(self.input_connections) > 0:
            self.input_connections[0].update(self)
    
    def set_proliferator(self, proliferator):
        self.proliferator = proliferator
        for process in self.output_connections:
            process.update_
    
    def exists_in(self, item_flow_list): # Done
        return self.__hash__() in item_flow_list.keys()
        
    def __str__(self):
        return (
            f"[ItemFlow] {self.name}\n"
            f"  Proliferator: {str(self.proliferator)}\n"
            f"  Input connections: {', '.join([connection.name for connection in self.input_connections]) if self.input_connections else 'None'}\n"
            f"  Output connections: {', '.join([connection.name for connection in self.output_connections]) if self.output_connections else 'None'}"
        )
        
    def __hash__(self):
        return hash((self.name, self.proliferator))
    