from .packet import Packet

class BlueprintBuildingHeader:

    def __init__(self, building_count = 0):
        self.building_count = building_count

    def parse(self, packet):
        self.building_count = packet.parse_int()

    def serialize(self):
        packet = Packet()
        packet.serialize_int(self.building_count)
        return packet

    def __str__(self):
        return f"""
Blueprint Building Header:
==========================
Binary data: {self.serialize().data}
==========================
Count: {self.building_count}
"""