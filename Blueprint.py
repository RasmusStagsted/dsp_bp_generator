import base64
import gzip

from MD5 import DysonSphereMD5
from BlueprintArea import BlueprintArea
from BlueprintBuilding import BlueprintBuilding
from BlueprintBuildingHeader import BlueprintBuildingHeader
from BlueprintHeader import BlueprintHeader
from BlueprintStringHeader import BlueprintStringHeader
from Packet import Packet

def validate_hash(data_str, hash_str):
    calculated_input_hash_value = DysonSphereMD5(DysonSphereMD5.Variant.MD5F).update(data_str.encode("utf-8")).hexdigest()
    if calculated_input_hash_value != hash_str.lower():
        raise "Blueprint string has invalid value."

def parse(blueprint_string, debug_level = 0):

    HASH_SIZE = 32

    # Parse and validate MD5 hash
    hash_str = blueprint_string[-HASH_SIZE:]
    data_str = blueprint_string[:-HASH_SIZE]
    data_str = data_str[:-1] # Remove the extra double quote that is placed to seperate hash and data
    validate_hash(data_str, hash_str)

    # Parse the blue print string header
    data_str = data_str.split("\"")
    header_str = data_str[0]
    data_str = data_str[1]
    blueprint_string_header = BlueprintStringHeader()
    blueprint_string_header.parse(header_str)
    if debug_level > 1:
        print(blueprint_string_header)

    # Base64 decode and gzip decompress the data
    compressed_data = base64.b64decode(data_str)
    data = gzip.decompress(compressed_data)
    packet = Packet(data)

    # Parse the blue print header
    blueprint_header = BlueprintHeader()
    blueprint_header.parse(packet)
    if debug_level > 1:
        print(blueprint_header)

    # Parse all areas
    blueprint_areas = []
    for i in range(blueprint_header.area_count):
        area = BlueprintArea()
        area.parse(packet)
        blueprint_areas.append(area)
        if debug_level > 1:
            print(area)

    # Parse building header
    blueprint_building_header = BlueprintBuildingHeader()
    blueprint_building_header.parse(packet)
    if debug_level > 1:
        print(blueprint_building_header)

    # Parse all buildings
    blueprint_buildings = []
    for i in range(blueprint_building_header.building_count):
        blueprint_building = BlueprintBuilding()
        blueprint_building.parse(packet)
        blueprint_buildings.append(blueprint_building)
        if debug_level > 1:
            print(blueprint_building)

    return {
        "blueprint_string_header": blueprint_string_header,
        "blueprint_header": blueprint_header,
        "blueprint_areas": blueprint_areas,
        "blueprint_building_header": blueprint_building_header,
        "blueprint_buildings": blueprint_buildings
    }

def serialize(blueprint_string_header, blueprint_header, blueprint_areas, blueprint_building_header, blueprint_buildings, debug_level = 0):

    data = bytes()

    # Serialize buildings
    blueprint_buildings_data = bytes()
    for blueprint_building in blueprint_buildings:
        blueprint_buildings_data += blueprint_building.serialize().data
        if debug_level > 1:
            print(blueprint_buildings_data)
    data = blueprint_buildings_data + data

    # Serialize building header
    blueprint_building_header_data = blueprint_building_header.serialize().data
    data = blueprint_building_header_data + data
    if debug_level > 1:
        print(blueprint_building_header_data)

    # Serialize areas
    blueprint_areas_data = bytes()
    for blueprint_area in blueprint_areas:
        blueprint_areas_data += blueprint_area.serialize().data
        if debug_level > 1:
            print(blueprint_areas_data)
    data = blueprint_areas_data + data

    # Serialize blueprint header
    blueprint_header_data = blueprint_header.serialize().data
    data = blueprint_header_data + data
    if debug_level > 1:
        print(blueprint_header_data)

    # Zip compress and base64 encode the data
    compressed_data = gzip.compress(data, compresslevel = 8, mtime = 0)
    temp = bytearray(compressed_data)
    temp.append(0x00)
    temp[9] = 0x0b
    compressed_data = bytes(temp)

    data_str = base64.b64encode(compressed_data).decode('utf-8')

    # Append blueprint string header
    data_str = blueprint_string_header.serialize() + ",\"" + data_str
    
    # Calculate, validate and append md5 sum
    calculated_input_hash_value = DysonSphereMD5(DysonSphereMD5.Variant.MD5F).update(data_str.encode("utf-8")).hexdigest()
    validate_hash(data_str, calculated_input_hash_value)
    data_str += "\"" + calculated_input_hash_value.upper()

    # Return blueprint string
    return data_str