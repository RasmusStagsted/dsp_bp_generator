from .graphical_edge import GraphicalEdge

class Connection(GraphicalEdge):
    
    def __init__(self, source, destination, name, count_per_sec):
        self.source = source
        self.destination = destination
        self.name = name
        self.count_per_sec = count_per_sec
        
    @staticmethod
    def connect(source, destination, name, count_per_sec):
        connection = Connection(
            source = source,
            destination = destination,
            name = name,
            count_per_sec = count_per_sec
        )
        source.output_connections.append(connection)
        destination.input_connections.append(connection)
        
    def __str__(self):
        return (
            f"[Connection] {self.name}\n"
            #f"  Source: {self.source}\n"
            #f"  Destination: {self.destination}\n"
            f"  Count per sec: {self.count_per_sec}"
        )