import numpy as np 
from Class_Structures import * 
from shapely.geometry import Polygon

def p_next_to(positions, room, object1_index, object2_index, side1 = None, side2 = None):
    """ The function next_to ensures that two objects are next to each other in a room. 
        If side1 is given, the specific side of object1 will be used. If side2 is given, 
        the specific side of object2 will be used. E.g. the 'front' of the chair should be next to the 'back' of the desk. 
        
        Args:
        room: rectangular Room object
        object1: Object object
        object2: Object object
        side: string, one of 'top' or 'back', 'bottom' or 'front', 'left', 'right', defines which side of the object to check
    """
    val = 0

    obj1 = room.moving_objects[object1_index]
    obj2 = room.moving_objects[object2_index]

    x1, y1, theta1 = positions[3*object1_index:3*object1_index+3]
    x2, y2, theta2 = positions[3*object2_index:3*object2_index+3]
    cs1 = corners(x1, y1, theta1, obj1.width, obj1.length) # TL, TR, BR, BL
    cs2 = corners(x2, y2, theta2, obj2.width, obj2.length) # TL, TR, BR, BL

    if side1: 
        if side1 == 'top' or side1 == 'back':
            point1, point2 = cs1[0], cs1[1]
        elif side1 == 'bottom' or side1 == 'front':
            point1, point2 = cs1[2], cs1[3]
        elif side1 == 'left':
            point1, point2 = cs1[0], cs1[3]
        elif side1 == 'right':
            point1, point2 = cs1[1], cs1[2]
        else:
            print("Invalid side for object1, continuing with no side.")
            return p_next_to(positions, room, object1_index, object2_index, side2 = side2)
    if side2: 
        if side2 == 'top' or side2 == 'back':
            point3, point4 = cs2[0], cs2[1]
        elif side2 == 'bottom' or side2 == 'front':
            point3, point4 = cs2[2], cs2[3]
        elif side2 == 'left':
            point3, point4 = cs2[0], cs2[3]
        elif side2 == 'right':
            point3, point4 = cs2[1], cs2[2]
        else:
            print("Invalid side for object2, continuing with no side.")
            return p_next_to(positions, room, object1_index, object2_index, side1 = side1)
    if side1 and side2:

        ### if two sides are given, we want the two sides to be parallel, as well as the two objects to be close to each other
        ### Want it to not matter if the centers are close per se, more that the sides are close (perpendicular distance between the two lines?)
        direction1 = np.array([point2[0] - point1[0], point2[1] - point1[1]]) # side1
        direction2 = np.array([point4[0] - point3[0], point4[1] - point3[1]]) # side2

        angle_diff = np.dot(direction1, direction2) / (np.linalg.norm(direction1) * np.linalg.norm(direction2))
        if angle_diff >= 0:
            val += max(0.0, 0.95 - angle_diff)**2
        else:
            val += max(0.0, -0.95 - angle_diff)**2

        if np.linalg.norm(direction1) > np.linalg.norm(direction2):
            point5 = np.array([(point3[0] + point4[0]) / 2, (point3[1] + point4[1]) / 2]) # point on the shorter side
            direction3 = np.array([point5[0] - point1[0], point5[1] - point1[1]])
            direction4 = np.array([point5[0] - point2[0], point5[1] - point2[1]])
            t = np.dot(direction1, direction3)/np.linalg.norm(direction1)
            direction5 = direction1
        else: 
            point5 = np.array([(point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2]) # point on the shorter side
            direction3 = np.array([point5[0] - point3[0], point5[1] - point3[1]])
            direction4 = np.array([point5[0] - point4[0], point5[1] - point4[1]])
            t = np.dot(direction2, direction3)/np.linalg.norm(direction2)
            direction5 = direction2
        if t < 0: 
            val += np.linalg.norm(direction3)**2 + (t)**2
        if t > 1: 
            val += np.linalg.norm(direction4)**2 + (t - 1)**2
        else: 
            distance = np.linalg.norm(np.cross(direction5, direction3)) / np.linalg.norm(direction5)
            val += distance**2
    
    if side1 and not side2: 
        ### Assume the opposite side each time. I.e. if object2 is  on the left of object 1, assume its the right side
        if side1 == 'left':
            return p_next_to(positions, room, object1_index, object2_index, side1 = 'left', side2 = 'right')
        elif side1 == 'right':
            return p_next_to(positions, room, object1_index, object2_index, side1 = 'right', side2 = 'left')
        elif side1 == 'top' or side1 == 'back':
            return p_next_to(positions, room, object1_index, object2_index, side1 = 'top', side2 = 'bottom')
        elif side1 == 'bottom' or side1 == 'front':
            return p_next_to(positions, room, object1_index, object2_index, side1 = 'bottom', side2 = 'top')
    if side2 and not side1:     
        if side2 == 'left':
            return p_next_to(positions, room, object1_index, object2_index, side1 = 'right', side2 = 'left')
        elif side2 == 'right':
            return p_next_to(positions, room, object1_index, object2_index, side1 = 'left', side2 = 'right')
        elif side2 == 'top' or side2 == 'back':
            return p_next_to(positions, room, object1_index, object2_index, side1 = 'bottom', side2 = 'top')
        elif side2 == 'bottom' or side2 == 'front':
            return p_next_to(positions, room, object1_index, object2_index, side1 = 'top', side2 = 'bottom')
    if not side2 and not side1: 
        ### If no sides are given, we want the two objects to be close to each other as possible from any direction
        ### Want the distance between the two objects to be minimized

        distance = np.linalg.norm(np.array([x1, y1]) - np.array([x2, y2]))
        val += distance**2

    return val 

def p_away_from(positions, room, object1_index, object2_index, min_dist = 2):
    """ The function p_away_from ensures that two objects are away from each other in a room.
        
        Args:
        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
        object1_index: int, index of object1 in the room
        object2_index: int, index of object2 in the room

    """
    x1, y1 = positions[3*object1_index:3*object1_index + 2]
    x2, y2 = positions[3*object2_index:3*object2_index + 2]

    distance = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

    return np.exp(min_dist - distance)

def p_aligned(positions, room, object1_index, object2_index, center_object_info = None, max_dist = 2):
    """ The function aligned ensures that two objects are aligned in a room. 
        If center is given, the objects will be aligned about that point. For example, 
        2 nightstands should be aligned about the bed. If center is not given, the objects will 
        be made close together with their orientations the same. 
        
        Args:

        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
        object1_index: int, index of object1 in the room
        object2_index: int, index of object2 in the room
        center_object_info: optional list where first element is the name of the object e.g. 'window' or 'bed' and the second element is the object index.
    """
    x1, y1, theta1 = positions[3*object1_index:3*object1_index + 3]
    x2, y2, theta2 = positions[3*object2_index:3*object2_index + 3]

    val = 0 

    if center_object_info: 
        name, index = center_object_info
        if name == 'window' or name == 'door' or name == 'socket':
            x, y = room.fixed_objects[index].position[:2]
        else: 
            x, y = positions[3*index:3*index + 2]

        dist1 = np.sqrt((x - x1)**2 + (y - y1)**2)
        dist2 = np.sqrt((x - x2)**2 + (y - y2)**2)
        val += (dist1 - dist2)**2

        object1, object2 = room.moving_objects[object1_index], room.moving_objects[object2_index]
        bl1, tl1 = BL(x1, y1, theta1, object1.width, object1.length), TL(x1, y1, theta1, object1.width, object1.length)
        bl2, tl2 = BL(x2, y2, theta2, object2.width, object2.length), TL(x2, y2, theta2, object2.width, object2.length)
    
        dir1 = np.array([bl1[0] - tl1[0], bl1[1] - tl1[1]])
        dir2 = np.array([bl2[0] - tl2[0], bl2[1] - tl2[1]])
        dir1 /= np.linalg.norm(dir1)
        dir2 /= np.linalg.norm(dir2)

        dir3 = np.array([x - x1, y - y1])/dist1
        dir4 = np.array([x - x2, y - y2])/dist2

        angle1 = np.arccos(np.dot(dir1, dir3))
        angle2 = np.arccos(np.dot(dir2, dir4))
        val += (angle1 - angle2)**2

    else: 
        dist = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
        val += max(0.0, dist - max_dist)**2 + (theta1 - theta2)**2
        
    return val

def p_facing(positions, room, object1_index, object2_index, both = False):
    """ The function facing ensures that object1 is facing object2 in a room.
        If both is True, then object2 will also be facing object1.
        
        Args:
        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
        object1_index: int, index of object1 in the room
        object2_index: int, index of object2 in the room
    """

    object1, object2 = room.moving_objects[object1_index], room.moving_objects[object2_index]
    x1, y1, theta1 = positions[3*object1_index:3*object1_index + 3]
    x2, y2, theta2 = positions[3*object2_index:3*object2_index + 3]

    bl1, tl1 = BL(x1, y1, theta1, object1.width, object1.length), TL(x1, y1, theta1, object1.width, object1.length)
    dir1 = np.array([bl1[0] - tl1[0], bl1[1] - tl1[1]])
    dir1 /= np.linalg.norm(dir1)

    dir2 = np.array([x2 - x1, y2 - y1])
    dir2 /= np.linalg.norm(dir2)

    if both: 

        bl2, tl2 = BL(x2, y2, theta2, object2.width, object2.length), TL(x2, y2, theta2, object2.width, object2.length)
        dir3 = np.array([bl2[0] - tl2[0], bl2[1] - tl2[1]])
        dir3 /= np.linalg.norm(dir3)

        return np.linalg.norm(dir1 + dir3)**2 + np.arccos(-np.dot(dir3, dir2))**2 + np.arccos(np.dot(dir1, dir2))**2
    else: 

        return np.arccos(np.dot(dir1, dir2))**2

def p_under_central(positions, room, object1_index, object2_index):
    """ The function under ensures that object1 (a rug) is underneath object2 (any moving_object) and centered.
        
        Args:
        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
        object1_index: int, index of object1 in the room
        object2_index: int, index of object2 in the room
    """

    obj1 = room.moving_objects[object1_index]   
    if obj1.name != 'rug':
        print("Only rugs can go underneath other moving objects.")
        return 0.0
    else:   
        ## Under basically means that their positions are the same.
        obj2 = room.moving_objects[object2_index] 
        x1, y1, theta1 = positions[3*object1_index:3*object1_index + 3]
        x2, y2, theta2 = positions[3*object2_index:3*object2_index + 3]
        cs1 = np.array(corners(x1, y1, theta1, obj1.width, obj1.width)).reshape(-1, 2) # TL, TR, BR, BL
        cs2 = np.array(corners(x2, y2, theta2, obj2.width, obj2.width)).reshape(-1, 2) 
        dists = np.zeros((4, 4))
        for i in range(4):
            for j in range(4):
                dists[i, j] = np.linalg.norm(cs1[i] - cs2[j])
        dists = np.min(dists, axis = 1)
        dists /= np.linalg.norm(dists)

        val = (x1 - x2)**2 + (y1 - y2)**2 + np.arccos(np.dot(dists, np.ones(4)/2))**2

        return val

def p_on_top_of(positions, room, object1_index, object2_index):
    """ The function under ensures that object1 is on top of object2 (a rug but does not ensure that it is centered.
        
        Args:
        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
        object1_index: int, index of object1 in the room
        object2_index: int, index of object2 in the room
    """

    obj2 = room.moving_objects[object2_index]   
    if obj2.name != 'rug':
        print("Only rugs can go underneath other moving objects.")

    else:   
        ## Under basically means that their positions are the same.
        obj1 = room.moving_objects[object1_index] 
        x1, y1, theta1 = positions[3*object1_index:3*object1_index + 3]
        x2, y2, theta2 = positions[3*object2_index:3*object2_index + 3]
        cs1 = corners(x1, y1, theta1, obj1.width, obj1.length)
        cs2 = corners(x2, y2, theta2, obj2.width, obj2.length)
        poly1 = Polygon(cs1)
        poly2 = Polygon(cs2)

        intersection = poly1.intersection(poly2)
        if intersection.area == poly1.area: 
            return 0.0

        lengths2 = np.roll(np.array(cs1), -1, axis = 0) - np.array(cs1)
        total_lengths = sum(np.linalg.norm(lengths2, axis = 1)**2)
        cs1 = np.array(cs1).reshape(-1, 2)
        cs2 = np.array(cs2).reshape(-1, 2)
        if intersection.area == 0: 
            dists = np.zeros((4, 4))
            for i in range(4):
                for j in range(4):
                    dists[i, j] = np.linalg.norm(cs1[i] - cs2[j])
            return np.min(dists) * total_lengths
        
        else: 
            x = np.array([[i, j] for i, j in zip(intersection.exterior.xy[0], intersection.exterior.xy[1])])
            lengths1 = np.roll(x, -1, axis = 0) - x
            lengths1 = np.linalg.norm(lengths1, axis = 1)
            lengths_on_rug = sum(lengths1**2)
        
            return total_lengths - lengths_on_rug

def p_infront(positions, room, object1_index, object2_index):
    """ The function p_infront ensures that object2 is in front of object1. E.g a coffee table should be in front of a sofa....


        Args:
        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
        object1_index: int, Object object
        object2_index: int, Object object
    """
    return 0.0

def p_perpendicular_aligned(positions, room, object1_index, object2_index, center_info):
    return 0

def p_parallel_aligned(positions, room, object1_index, object2_index, center_info):
    return 0
