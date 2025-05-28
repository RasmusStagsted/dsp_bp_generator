import math

PLANET_RADIUS = 400 # [m]

class Vector:

    def __init__(self, x = 0.0, y = 0.0, z = 0.0):
        self.x = x
        self.y = y
        self.z = z

    def move(self, offset):
        self.x += offset.x
        self.y += offset.y
        self.z += offset.z

    def get_distance(self, pos):
        return math.sqrt(math.pow(pos.x - self.x, 2) + math.pow(pos.y - self.y, 2) + math.pow(pos.z - self.z, 2))

    def __add__(pos1, pos2):
        return Vector(
            x = pos1.x + pos2.x,
            y = pos1.y + pos2.y,
            z = pos1.z + pos2.z
        )

    def __sub__(pos1, pos2):
        return Vector(
            x = pos1.x - pos2.x,
            y = pos1.y - pos2.y,
            z = pos1.z - pos2.z
        )
        
    def __str__(self):
        return f"x: {self.x}\ny: {self.y}\nz: {self.z}\n"

    def theta(self):
        if self.x == 0 and self.y == 0:
            return 0
        theta = math.degrees(math.atan2(self.y, self.x))
        if theta < 0:
            theta += 360
        return theta
    
    def phi(self):
        if self.x == 0 and self.y == 0 and self.z == 0:
            return 0
        phi = math.degrees(math.atan2(self.z, math.sqrt(self.x ** 2 + self.y ** 2)))
        if phi < 0:
            phi += 360
        return phi
    
    def r(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

class Yaw:
    North = 0.0
    NorthEast = 45.0
    East = 90.0
    SouthEast = 135.0
    South = 180.0
    SouthWest = 225.0
    West = 270.0
    NorthWest = 315.0
    Unknown = None

    def get_neares_90_degree(pos1: Vector, pos2: Vector):
        angle = Yaw.get_angle(pos1, pos2)
        if angle == None:
            return None
        angle = ((angle + 45) // 90) * 90
        if angle == 360.00:
            angle = 0
        return angle

    def get_angle(pos1, pos2):
        delta_x = pos2.x - pos1.x
        delta_y = pos2.y - pos1.y
        
        if delta_x == 0:
            if delta_y > 0:
                return Yaw.North
            elif delta_y < 0:
                return Yaw.South
            else:
                return Yaw.Unknown
        angle = math.degrees(math.atan2(delta_x, delta_y))
        
        if angle < 0.0:
            angle += 360.0
        return angle
            
    def direction_average(dir1, dir2):
        if (dir1 == Yaw.North and dir2 == Yaw.East) or (dir1 == Yaw.East and dir2 == Yaw.North):
            return Yaw.NorthEast
        elif (dir1 == Yaw.East and dir2 == Yaw.South) or (dir1 == Yaw.South and dir2 == Yaw.East):
            return Yaw.SouthEast
        elif (dir1 == Yaw.South and dir2 == Yaw.West) or (dir1 == Yaw.West and dir2 == Yaw.South):
            return Yaw.SouthWest
        elif (dir1 == Yaw.West and dir2 == Yaw.North) or (dir1 == Yaw.North and dir2 == Yaw.West):
            return Yaw.NorthWest
        else:
            return None

    def direction_to_unit_vector(direction):
        if direction == Yaw.North:
            return Vector(0.0, 1.0)
        elif direction == Yaw.NorthEast:
            return Vector(math.sqrt(2), math.sqrt(2))
        elif direction == Yaw.East:
            return Vector(1.0, 0.0)
        elif direction == Yaw.SouthEast:
            return Vector(math.sqrt(2), -math.sqrt(2))
        elif direction == Yaw.South:
            return Vector(0.0, -1.0)
        elif direction == Yaw.SouthWest:
            return Vector(-math.sqrt(2), -math.sqrt(2))
        elif direction == Yaw.West:
            return Vector(-1.0, 0.0)
        elif direction == Yaw.NorthWest:
            return Vector(-math.sqrt(2), math.sqrt(2))
        return None

if __name__ == "__main__":
    
    # Test angle calculation
    string = ""
    for i in range(11):
        for j in range(11):
            angle = Yaw.get_angle(Vector(5, 5), Vector(j, 10 - i))
            if angle != None:
                string += "{:.2f} \t".format(angle)
            else:
                string += "{} \t".format("   ")
        string += "\n"
    print(string)
    
    # Test nearest 90 degree calculation
    string = ""
    for i in range(11):
        for j in range(11):
            angle = Yaw.get_neares_90_degree(Vector(5, 5), Vector(j, 10 - i))
            if angle != None:
                string += "{:.2f}\t".format(angle)
            else:
                string += "{:.2f}\t".format(0)
        string += "\n"
    print(string)
    
    # Test direction to unit vector
    cases = {
        Yaw.North: Vector(0, 1, 0),
        Yaw.NorthEast: Vector(math.sqrt(2), math.sqrt(2), 0),
        Yaw.East: Vector(1, 0, 0),
        Yaw.SouthEast: Vector(math.sqrt(2), -math.sqrt(2), 0),
        Yaw.South: Vector(0, -1, 0),
        Yaw.SouthWest: Vector(-math.sqrt(2), -math.sqrt(2), 0),
        Yaw.West: Vector(-1, 0, 0),
        Yaw.NorthWest: Vector(-math.sqrt(2), math.sqrt(2), 0),
    }
    for key, val in cases.items():
        dir = Yaw.direction_to_unit_vector(key)
        if (dir.x != val.x or dir.y != val.y or dir.z != val.z):
            print("Failed " + str(key))
    
    