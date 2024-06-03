from blueprint import Blueprint

input_blueprint_string = "BLUEPRINT:0,10,0,0,0,0,0,0,0,0.10.29.000510,New%20Blueprint,\"H4sIAAAAAAAAC2NkYGBggmIQYIViEGBk+M/AcAIqzAoXhgEHTPYWJxC+zK4K1MvA8B8IGBnATKh5YNBgj9CAzEZoZsKimQnJJgdMNkLzfxhA0syMZBsDJhvqPE5nBoReVEezYHP62TM+UENMnEH4Lrs2WDnINsb/IAQxACQGACcftR9oAQAAAA==\"05AF49CF05646AC8C1DF460BA0490E6B"
print("Input blueprint string:", input_blueprint_string)
print()
bp = Blueprint()
buildings = bp.parse(input_blueprint_string, debug = False, debug_raw_data = False)
assert bp.validate_hash(), "Could not validate hash of input blueprint string"
output_blueprint_string = bp.serialize(buildings, debug = False, debug_raw_data = False)
print("Output blueprint string:", output_blueprint_string)
print()
assert bp.validate_hash(), "Could not validate hash of output blueprint string"
assert input_blueprint_string == output_blueprint_string, "The input and output blueprint string did not match"
