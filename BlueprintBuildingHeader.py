from Packet import Packet

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

if __name__ == "__main__":
    from Packet import Packet
    header = BlueprintBuildingHeader()
    input_data = b'\x01\x00\x00\x00'
    input_packet = Packet(input_data)
    header.parse(input_packet)
    
    output_data = header.serialize().data
    
    print("Input data: ", input_data)
    print("Output data:", output_data)
    print(header)
    print("Remaining data:", input_packet.data)
    assert(len(input_packet.data) == 0)
    assert(input_data == output_data)