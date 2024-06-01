from ItemEnum import Yaw
import Buildings

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
        return 0.0, 1.0
    elif direction == Yaw.East:
        return 1.0, 0.0
    elif direction == Yaw.South:
        return 0.0, -1.0
    elif direction == Yaw.West:
        return -1.0, 0.0
    return None

def connect_cornor_belt(belt1, belt2):
    dx1, dy1 = direction_to_unit_vector(belt1.yaw)
    belt1.output_object_index = Buildings.Building.count()
    belt1.output_to_slot = 1
    Buildings.Belt(
        x = belt1.x + dx1,
        y = belt1.y + dy1,
        z = belt1.z,
        yaw = direction_average(belt1.yaw, belt2.yaw),
        output_object_index = belt2.index,
        output_to_slot = 1
    )

def generate_belt(x, y, z, yaw, length):
    
    if type(yaw) != list:
        yaw = [yaw]
    if type(length) != list:
        length = [length]
    assert len(yaw) == len(length), "\"yaw\" and \"length\" must have the same length"

    ptr_x = x
    ptr_y = y
    
    belts = []
    for i in range(len(yaw)):
        dx, dy = direction_to_unit_vector(yaw[i])
        for j in range(length[i]):
            belt = Buildings.Belt(
                x = ptr_x,
                y = ptr_y,
                z = z,
                yaw = yaw[i],
                output_object_index = Buildings.Building.count() + 1,
                output_to_slot = 1
            )
            belts.append(belt)
            ptr_x += dx
            ptr_y += dy
        
        if (i != len(yaw) - 1):
            belt.yaw = direction_average(yaw[i], yaw[i + 1])
        else:
            belt.output_object_index = -1
            belt.output_to_slot = -1
    return belts
