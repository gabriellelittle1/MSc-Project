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
    cs1 = np.array(corners(x1, y1, theta1, obj1.width, obj1.length)) # TL, TR, BR, BL
    cs2 = np.array(corners(x2, y2, theta2, obj2.width, obj2.length)) # TL, TR, BR, BL

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
        min_side_dist = np.inf
        sides = ['front', 'back', 'left', 'right']
        for i in range(4): 
            side_value = p_next_to(positions, room, object1_index, object2_index, side1 = side1, side2 = sides[i])
            min_side_dist = min(min_side_dist, side_value)
        val += min_side_dist
                
        # mid_point = (point1 + point2)/2 
        # ## Want to minimise the distance of this side from the center??? of object2
        # side_dist = (np.linalg.norm(point1 - np.array([x2, y2])) + np.linalg.norm(point2 - np.array([x2, y2])) + np.linalg.norm(mid_point - np.array([x2, y2])))/3
        # other_dists = np.sqrt(np.sum((cs1 - np.array([x2, y2]))**2, axis = 0))
        # val = sum(np.clip(side_dist - other_dists, 0.0, np.inf)**2)
        return val 
    if side2 and not side1:     
        min_side_dist = np.inf
        sides = ['front', 'back', 'left', 'right']
        for i in range(4): 
            side_value = p_next_to(positions, room, object1_index, object2_index, side1 = sides[i], side2 = side2)
            min_side_dist = min(min_side_dist, side_value)
        val += min_side_dist

        return val 
    if not side2 and not side1: 
        ### If no sides are given, we want the two objects to be close to each other as possible from any direction
        ### Want the distance between the two objects to be minimized but also to not be overlapping 

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
    val = 0.0

    object1, object2 = room.moving_objects[object1_index], room.moving_objects[object2_index]
    x1, y1, theta1 = positions[3*object1_index:3*object1_index + 3]
    x2, y2, theta2 = positions[3*object2_index:3*object2_index + 3]

    cs1 = np.array(corners(x1, y1, theta1, object1.width, object1.length))# TL, TR, BR, BL
    tl1, tr1, br1, bl1 = cs1
    dir1 = np.array([bl1[0] - tl1[0], bl1[1] - tl1[1]])
    dir1 /= np.linalg.norm(dir1)

    distances = np.linalg.norm(cs1 - np.array([x2, y2]), axis = 1) 
    ## want front right to be closer than back right, and front left to be closer than back left 
    val += min(0.0, distances[0] - distances[3])**2 + min(0.0, distances[1] - distances[2])**2
    ## Line 1 goes from front left corner onward, line 2 goes from front right corner 
    ## distance of object2 from line1
    dist1 = abs((bl1[1] - tl1[1])*x2 - (bl1[0] - tl1[0])*y2 + bl1[0]*tl1[1] - bl1[1]*tl1[0])/np.sqrt((bl1[0] - tl1[0])**2 + (bl1[1] - tl1[1])**2)
    ## distance of object2 from line2
    dist2 = abs((br1[1] - tr1[1])*x2 - (br1[0] - tr1[0])*y2 + br1[0]*tr1[1] - br1[1]*tr1[0])/np.sqrt((br1[0] - tr1[0])**2 + (br1[1] - tr1[1])**2)
    ## distance between the two lines is width, therefore want dist1 + dist2 = width 
    val += (dist1 + dist2 - object1.width)**2
    if both: 
        val += p_facing(positions, room, object2_index, object1_index)
        cs2 = np.array(corners(x2, y2, theta2, object2.width, object2.length))# TL, TR, BR, BL
        dir2 = np.array([cs2[3][0] - cs2[0][0], cs2[3][1] - cs2[0][1]])
        dir2 /= np.linalg.norm(dir2)
        val += (np.dot(dir1, dir2) + 1)**2
    return val 

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
    """ The function under ensures that object1 is on top of object2 (a rug) but does not ensure that it is centered.
        
        Args:
        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
        object1_index: int, index of object1 in the room
        object2_index: int, index of object2 in the room
    """

    obj2 = room.moving_objects[object2_index]   
    if obj2.name != 'rug':
        print("Only rugs can go underneath other moving objects.")
        return 0.0

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

def p_infront(positions, room, object1_index, object2_index, dist = 0.8):
    """ The function p_infront ensures that object1 is in front of object2 (both moving_objects i.e. not windows or doors). E.g a coffee table should be in front of a sofa....

        Args:
        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
        object1_index: int, Object object
        object2_index: int, Object object
        dist: float, desired distance between two objects. E.g. if its a sofa and a coffee table, the distance should be around 0.8m, 
                                                            if its a sofa and a fireplace, the distance should be around 2m/2.5m.
    """

    ## want object1 position to be in front of object2 position in the frame of object2
    x1, y1, theta1 = positions[3*object1_index:3*object1_index + 3]
    x2, y2, theta2 = positions[3*object2_index:3*object2_index + 3]

    obj1 = room.moving_objects[object1_index]
    obj2 = room.moving_objects[object2_index]

    cs2 = corners(x2, y2, theta2, obj2.width, obj2.length) # TL, TR, BR, BL
    mid_front = np.array([(cs2[2][0] + cs2[3][0])/2, (cs2[2][1] + cs2[3][1])/2])
    mid2front = np.array([mid_front[0] - x2, mid_front[1] - y1])
    mid2front /= np.linalg.norm(mid2front)

    projection = mid_front + (dist + min(obj1.width, obj1.length)/2) * mid2front
    val = (projection[0] - x1)**2 + (projection[1] - y1)**2
    return val

def p_perpendicular_aligned(positions, room, object1_index, object2_index, center_object_index = None):
    """ The function p_perpendicular_aligned ensures that two objects are aligned in a room perpendicularly. 
        If center is given, the objects will be aligned about that point. For example, 
        a sofa and chair might be aligned perpendicularly about a coffee table or a side table. Or a chair at the head of the table 
        might be aligned perpendicularly with the chairs closest to it on the sides of the table. 

        
        Args:

        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
        object1_index: int, index of object1 in the room
        object2_index: int, index of object2 in the room
        center_object_index: int, index of object in room.moving_objects to be used as the pivot for the alignment (e.g. a coffee table or a table)
    """

    val = 0.0
    obj1, obj2 = room.moving_objects[object1_index], room.moving_objects[object2_index]
    x1, y1, theta1 = positions[3*object1_index:3*object1_index + 3]
    x2, y2, theta2 = positions[3*object2_index:3*object2_index + 3]

    cs1 = np.array(corners(x1, y1, theta1, obj1.width, obj1.length))# TL, TR, BR, BL
    cs2 = np.array(corners(x2, y2, theta2, obj2.width, obj2.length))

    mid_front1 = (cs1[2, :] + cs1[3, :])/2
    mid_front2 = (cs2[2, :] + cs2[3, :])/2

    dir1 = (cs1[3, :] - cs1[0, :])/np.linalg.norm(cs1[3, :] - cs1[0, :])
    dir2 = (cs2[3, :] - cs2[0, :])/np.linalg.norm(cs2[3, :] - cs2[0, :])

    ### Find t1, and t2 (intersection line lengths - want there to be a right angled triangle between each object)
    BA = mid_front2 - mid_front1
    t1 = np.dot(np.array([dir2[1], -dir2[0]]), BA) / np.dot(np.array([dir2[1], -dir2[0]]), dir1)
    t2 = np.dot(np.array([dir1[1], -dir1[0]]), BA) / np.dot(np.array([dir2[1], -dir2[0]]), dir1)
    
    if not center_object_index:
        val += (np.linalg.norm(BA) - np.sqrt((t1**2 + t2**2)))**2 
        val += min(0.0, t1)**2 + min(0.0, t2)**2 # t1 and t2 should be bigger than 0 
        val += min(0.0, np.sqrt((0.8*obj1.width)**2 + (0.8*obj2.width)**2) - np.sqrt(t1**2+ t2**2))**2 # t1 and t2 should not be too big
        val += ((max(theta1, theta2) - min(theta1, theta2)) - np.pi/2)**2 ## thetas should be pi/2 apart
    else: 
        center_obj = room.moving_objects[center_object_index]
        x3, y3, theta3 = positions[3*center_object_index:3*center_object_index + 3]
        val += (np.linalg.norm(BA) - np.sqrt((t1**2 + t2**2)))**2 ## mid_front1, mid_front2, and intersection point should make a right angled triangle 
        val += min(0.0, t1 * t2)**2 # t1 and t2 should either both be positive or both be negative 
        C = np.array([x1, y1]) + t1 * dir1 
        val += (C[0] - x3)**2 + (C[1] - y3)**2 # C should be the center of the center object
        val += min(0.0, np.sqrt((center_obj.width)**2 + (center_obj.width)**2) - np.sqrt(t1**2+ t2**2))**2 # t1 and t2 should not be too big
        val += ((max(theta1, theta2) - min(theta1, theta2)) - np.pi/2)**2 ## thetas should be pi/2 apart
    return val

def p_parallel_aligned(positions, room, object1_index, object2_index, center_info):
    return 0

def p_surround(positions, room, central_object_index, object_indices):
    """ The function p_surroudn ensures that central_object is surrounded by all the objects in object_indices.
        This would be used for chairs around a dining table.

        Args:
        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
        central_object_index: int, Object object
        object_indices: list of ints, indices of Object objects
    """

    val = 0

    center_x, center_y = positions[3*central_object_index:3*central_object_index + 2]

    pos = np.array(positions).reshape(-1, 3)
    pos = pos[object_indices, :]

    center_of_mass = np.mean(pos[:, :2], axis = 0)
    val += (center_of_mass[0] - center_x)**2 + (center_of_mass[1] - center_y)**2 # center of mass of all the objects
    for i in range(len(object_indices)):
        val += p_facing(positions, room, object_indices[i], central_object_index)

    return val