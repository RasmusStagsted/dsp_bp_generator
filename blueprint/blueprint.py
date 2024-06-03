if __name__ != "__main__":
    from .md5 import MD5
    from .blueprint_area import BlueprintArea
    from .blueprint_building import BlueprintBuilding
    from .blueprint_building_header import BlueprintBuildingHeader
    from .blueprint_header import BlueprintHeader
    from .blueprint_string_header import BlueprintStringHeader
    from .packet import Packet
import base64
import gzip

class Blueprint:
    
    def __init__(self):
        pass

    def validate_hash(self):
        calculated_input_hash_value = MD5(MD5.Variant.MD5F).update(self.hashed_string.encode("utf-8")).hexdigest().upper()
        return calculated_input_hash_value == self.hash_str

    def parse(self, blueprint_string, debug = False, debug_raw_data = False):

        HASH_SIZE = 32

        # Parse and validate MD5 hash
        self.hash_str = blueprint_string[-HASH_SIZE:].upper()
        if debug_raw_data:
            print("Hash str:")
            print(self.hash_str)
            print()
        self.data_str = blueprint_string[:-HASH_SIZE]
        self.data_str = self.data_str[:-1] # Remove the extra double quote that is placed to seperate hash and data
        self.hashed_string = self.data_str
        if debug_raw_data:
            print("Data str:")
            print(self.data_str)
            print()
        
        # Parse the blue print string header
        self.data_str = self.data_str.split(",\"")
        header_str = self.data_str[0]
        if debug_raw_data:
            print("Header str:")
            print(header_str)
            print()
        self.data_str = self.data_str[1]
        if debug_raw_data:
            print("Base64 data str:")
            print(self.data_str)
            print()
        self.blueprint_string_header = BlueprintStringHeader()
        self.blueprint_string_header.parse(header_str)
        if debug:
            print(self.blueprint_string_header)

        # Base64 decode and gzip decompress the data
        compressed_data = base64.b64decode(self.data_str)
        if debug_raw_data:
            print("Compressed data:")
            print(compressed_data)
            print()
        data = gzip.decompress(compressed_data)
        if debug_raw_data:
            print("Uncompressed data:")
            print(data)
            print()
        packet = Packet(data)

        # Parse the blue print header
        self.blueprint_header = BlueprintHeader()
        self.blueprint_header.parse(packet)
        if debug:
            print(self.blueprint_header)

        # Parse all areas
        self.blueprint_areas = []
        for i in range(self.blueprint_header.area_count):
            area = BlueprintArea()
            area.parse(packet)
            self.blueprint_areas.append(area)
            if debug:
                print(area)

        # Parse building header
        self.blueprint_building_header = BlueprintBuildingHeader()
        self.blueprint_building_header.parse(packet)
        if debug:
            print(self.blueprint_building_header)

        # Parse all buildings
        self.blueprint_buildings = []
        for i in range(self.blueprint_building_header.building_count):
            blueprint_building = BlueprintBuilding()
            blueprint_building.parse(packet)
            self.blueprint_buildings.append(blueprint_building)
            if debug:
                print(blueprint_building)

        return self.blueprint_buildings

    def serialize(self, blueprint_buildings, debug = False, debug_raw_data = False):

        data = bytes()

        # Serialize buildings
        blueprint_buildings_data = bytes()
        for blueprint_building in blueprint_buildings:
            building_data = blueprint_building.serialize().data
            blueprint_buildings_data += building_data
            if debug:
                print("Blueprint building:")
                print(blueprint_building)
                print()
        data = blueprint_buildings_data + data

        # Serialize building header
        blueprint_building_header_data = self.blueprint_building_header.serialize().data
        data = blueprint_building_header_data + data
        if debug:
            print(blueprint_building_header_data)

        # Serialize areas
        blueprint_areas_data = bytes()
        for blueprint_area in self.blueprint_areas:
            blueprint_areas_data += blueprint_area.serialize().data
            if debug:
                print(blueprint_areas_data)
        data = blueprint_areas_data + data

        # Serialize blueprint header
        blueprint_header_data = self.blueprint_header.serialize().data
        data = blueprint_header_data + data
        if debug:
            print(blueprint_header_data)
        if debug_raw_data:
            print("Uncompressed data:")
            print(data)
            print()

        # Zip compress and base64 encode the data
        compressed_data = gzip.compress(data, compresslevel = 8, mtime = 0)
        if debug_raw_data:
            print("Compressed data:")
            print(compressed_data)
            print()
        temp = bytearray(compressed_data)
        temp.append(0x00)
        temp[9] = 0x0b
        compressed_data = bytes(temp)

        data_str = base64.b64encode(compressed_data).decode('utf-8')
        if debug_raw_data:
            print("Base64 data str:")
            print(data_str)
            print()

        # Append blueprint string header
        blueprint_string_header_str = self.blueprint_string_header.serialize()
        data_str = blueprint_string_header_str + "\"" + data_str
        if debug_raw_data:
            print("Header str:")
            print(blueprint_string_header_str)
            print()
        
        # Calculate and append md5 sum
        calculated_input_hash_value = MD5(MD5.Variant.MD5F).update(data_str.encode("utf-8")).hexdigest().upper()
        if debug_raw_data:
            print("Hash str:")
            print(calculated_input_hash_value)
            print()
        data_str += "\"" + calculated_input_hash_value

        # Return blueprint string
        return data_str

if __name__ == "__main__":
    from md5 import MD5
    from blueprint_area import BlueprintArea
    from blueprint_building import BlueprintBuilding
    from blueprint_building_header import BlueprintBuildingHeader
    from blueprint_header import BlueprintHeader
    from blueprint_string_header import BlueprintStringHeader
    from packet import Packet

    blueprint_string = "BLUEPRINT:0,10,0,0,0,0,0,0,0,0.10.29.000510,New%20Blueprint,\"H4sIAAAAAAAAC2NkYGBggmIQYIViEGBk+M/AcAIqzAoXhgEHTPYWJxC+zK4K1MvA8B8IGBnATKh5YNBgj9CAzEZoZsKimQnJJgdMNkLzfxhA0syMZBsDJhvqPE5nBoReVEezYHP62TM+UENMnEH4Lrs2WDnINsb/IAQxACQGACcftR9oAQAAAA==\"05AF49CF05646AC8C1DF460BA0490E6B"
    bp = Blueprint()
    bp.parse(blueprint_string)
    assert bp.validate_hash(), "Could not validate hash of input blueprint string"
    bp.serialize(self.buildings)
    assert bp.validate_hash(), "Could not validate hash of output blueprint string"    
    new_blueprint_string = bp.get_blueprint_string()
    assert new_blueprint_string == blueprint_string, "The input and output blueprint string did not match"