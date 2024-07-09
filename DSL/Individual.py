## All the Individual Object constraint functions are defined here
from Class_Structures import *
from shapely.geometry import Polygon

def next_to_wall(positions, room, object_index, cardinal_direction = None, side = None):
    """ The function next_to_wall ensures an object is next to a wall in a room. 
        If cardinal_direction is given, a specific wall will be used. If side is given, 
        the specific side of the object will be used.
        
        Args:
        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
        object_index: int, index of the object in the room's object list
        cardinal_direction: string, one of 'N', 'S', 'E', 'W', defines which wall to check
        side: string, one of 'top' or 'back', 'bottom' or 'front', 'left', 'right', defines which side of the object to check e.g back of bed 
    """

    x, y, theta = positions[3*object_index:3*object_index+3]
    cs = np.array(corners(x, y, theta, room.moving_objects[object_index].width, room.moving_objects[object_index].length)) # TL, TR, BR, BL
    if side:
        if side == "top" or side == "back":
            cs = [cs[0], cs[1]]
        elif side == "bottom" or side == "front":
            cs = [cs[2], cs[3]]
        elif side == "left":
            cs = [cs[0], cs[3]]
        elif side == "right":
            cs = [cs[1], cs[2]]
    
    ## North: y = room.length, East: x = room.width, South: y = 0, West: x = 0
    if cardinal_direction:
        if cardinal_direction == "N":
            distances = [(i - room.length)**2 for i in cs[:, 1]]
        elif cardinal_direction == "E":
            distances = [(i - room.width)**2 for i in cs[:, 0]]
        elif cardinal_direction == "S":
            distances = [i**2 for i in cs[:, 1]]
        elif cardinal_direction == "W":
            distances = [i**2 for i in cs[:, 0]]
        
        if len(cs) == 2:
            return sum(distances)
        else: 
            dists = [distances[0] + distances[2], distances[1] + distances[3], distances[0] + distances[3], distances[1] + distances[2]]
            return min(dists)
    else: 
        if side:
            distances = np.zeros(4)
            for corner in cs:
                distances += np.array([(corner[1] - room.length)**2, (corner[0] - room.width)**2, corner[1]**2, corner[0]**2])
            return min(distances)
        else: 
            distances = np.zeros((4, 4))
            sides = [[cs[0], cs[2]], [cs[1], cs[3]], [cs[0], cs[3]], [cs[1], cs[2]]]
            for i in range(4):
                c1, c2 = sides[i]
                distances[i, :] = [(c1[1] - room.length)**2, (c1[0] - room.width)**2, c1[1]**2, c1[0]**2]
                distances[i, :] += [(c2[1] - room.length)**2, (c2[0] - room.width)**2, c2[1]**2, c2[0]**2]

            return min(distances.flatten())
    
def object_close_to_fixed_object(positions, room, object_index, fixed_object_type, side = None, max_dist = 0.5):
    """ The function next_to_fixed_object ensures an object is next to a fixed object in a room. 
        If side is given, the specific side of the object will be used.
        
        Args:
        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
        object_index: int, index of the object in the room's object list
        fixed_object_type: string, type of fixed object to check. One of 'window', 'door', 'plug'
        side: string, one of 'top' or 'back', 'bottom' or 'front', 'left', 'right', defines which side of the object to check
    """

    x, y, theta = positions[3*object_index:3*object_index+3]
    cs = np.array(corners(x, y, theta, room.moving_objects[object_index].width, room.moving_objects[object_index].length)) # TR, BR, TL, BL
    if side == "top" or side == "back":
        cs = [cs[0], cs[1]]
    elif side == "bottom" or side == "front":
        cs = [cs[2], cs[3]]
    elif side == "left":
        cs = [cs[0], cs[3]]
    elif side == "right":
        cs = [cs[1], cs[2]]
    
    
    f_objs = room.find_all(fixed_object_type)
    if side: 
        dist = np.inf
        point = [(cs[0][0] + cs[1][0])/2, (cs[0][1] + cs[1][1])/2]
        for i in range(len(f_objs)):
            f_obj = f_objs[i]
            new_dist = (point[0] - f_obj.position[0])**2 + (point[1] - f_obj.position[1])**2
            if new_dist < dist: 
                dist = new_dist
        return max(dist - max_dist**2, 0.0)
    else:
        distances = np.zeros((len(f_objs), 4))
        for i in range(len(f_objs)):
            for j in range(4): 
                distances[i, j] = (cs[j][0] - f_objs[i].position[0])**2 + (cs[j][1] - f_objs[i].position[1])**2
        return max(min(distances.flatten()) - max_dist**2, 0.0)

def object_away_from_fixed_object(positions, room, object_index, fixed_object_type, min_dist = 2):
    """ The function away_from_fixed_object ensures an object is not near to a fixed object in a room. 
        If side is given, the specific side of the object will be used.
        
        Args:
        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
        object_index: int, index of the object in the room's object list
        fixed_object_type: string, type of fixed object to check. One of 'window', 'door', 'plug'
        side: string, one of 'top' or 'back', 'bottom' or 'front', 'left', 'right', defines which side of the object to check
    """

    x, y= positions[3*object_index:3*object_index+2]
    w, l = room.moving_objects[object_index].width, room.moving_objects[object_index].length
    half_diag = (w**2 + l**2)/4
    f_objs = room.find_all(fixed_object_type)

    ## If any of the corners are within the minimum distance, return the sum of the distances
    distances = np.zeros(len(f_objs))
    for i in range(len(f_objs)):
        f_obj = f_objs[i]
        distances[i] = max(0.0, (min_dist ** 2)*(half_diag) - ((x - f_obj.position[0])**2 + (y - f_obj.position[1])**2)) 
    
    return sum(distances)/(len(f_objs) * min_dist**2 * half_diag)

def accessible(positions, room, object_index, sides):
    """ The function accessible ensures that an object is accessible from given sides. 
        
        Args:
        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
        object_index: int, index of the object in the room's object list
        sides: a list of strings, one of 'top' or 'back', 'bottom' or 'front', 'left', 'right', defines which side of the object to check
    """
    return 0

def central(positions, room, object_index):
    """ The function central ensures that an object is centrally placed in the room. 
        Args:
        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
        object_index: int, index of the object in the room's object list
    """

    ## Minimise the distance from one of the central points of the room 
    x, y= positions[3*object_index:3*object_index+2]
    mid_x, mid_y = room.width/2, room.length/2
    return min((mid_x - x)**2, (mid_y - y)**2)

def in_region(positions, room, object_index, region_name):
    """ The function in_region ensures that an object is in a given region. 
        
        Args:
        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
        object_index: int, index of the object in the room's object list
        region_name: string, name of the region for the object to be in 
    """
    regions = room.regions
    region_index = room.find_region_index(region_name)
    x, y, theta = positions[3*object_index:3*object_index+3]
    value = 0 
    for i in range(len(regions)):
        if i == region_index:
            continue
        else:
            value += ((regions[i].x - x)**2 + (regions[i].y - y)**2) - ((regions[region_index].x - x)**2 + (regions[region_index].y - y)**2)
    return min(0, value)**2

def in_bounds(positions, room): 

    """ The function in_region ensures that all objects are within the room. This must be used in every constraint solving problem for Individual constraint types.
        
        Args:
        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
    """
    val = 0
    objs = room.moving_objects
    for i in range(len(room.moving_objects)):
        x, y, theta = positions[3*i:3*i+3]
        cs = corners(x, y, theta, objs[i].width, objs[i].length)
        for corner in cs: 
            val += (max(0, corner[0] - room.width)**2 + max(0, corner[1] - room.length)**2)
            val += (max(0, -corner[0])**2 + max(0, -corner[1])**2)
        
    return val 

def no_overlap(positions, room):
    """ The function no_overlap ensures that no objects overlap in the room. This should be used in every constraint satisfaction problem.
        
        Args:
        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
    """
    val = 0
    objs = room.moving_objects
    for i in range(len(objs)):
        for j in range(len(objs)):

            obj_i = objs[i]
            obj_j = objs[j]
            corners_i = corners(positions[3*i], positions[3*i+1], positions[3*i+2], obj_i.width, obj_i.length)
            corners_j = corners(positions[3*j], positions[3*j+1], positions[3*j+2], obj_j.width, obj_j.length)

            poly1 = Polygon(corners_i)
            poly2 = Polygon(corners_j)
            intersection = poly1.intersection(poly2)

            if intersection.area > 0:
                # diff_x = (positions[3*i] - positions[3*j])**2
                # diff_y = (positions[3*i+1] - positions[3*j+1])**2
                val += intersection.area# - diff_x - diff_y

    return val 
                
















