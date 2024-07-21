## All the Individual Object constraint functions are defined here
from Class_Structures import *
from shapely.geometry import Polygon

def ind_next_to_wall(positions, room, object_index, side):
    """ This function ensures an object is next to a wall in a room. 
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
    distances =  np.zeros((4, 4)) # each row a different corner, each column a different wall 
    sides = [[0, 1], [2, 3], [0, 3], [1, 2]]
    for i in range(4):
        distances[i, :] = np.array([(cs[i][1] - room.length)**2, (cs[i][0] - room.width)**2, cs[i][1]**2, cs[i][0]**2])

    distances = np.sqrt(distances)
    side_distances = np.zeros_like(distances) # columns: N, E, S, W, rows: top, bottom, left, right
    for i in range(4):
        side_distances[i, :] = distances[sides[i][0], :] + distances[sides[i][1], :]

    val = 0 

    if side == "top" or side == "back":
        wall = np.argmin(side_distances[0, :])
        ds = side_distances[:, wall]
        val += (min(side_distances[0, 0], side_distances[0, 2]) * min(side_distances[0, 1], side_distances[0, 3]))
        val += max(ds[0] - ds[1], 0.0)**2 + max(ds[0] - ds[2], 0.0)**2 + max(ds[0] - ds[3], 0.0)**2
    elif side == "bottom" or side == "front":
        wall = np.argmin(side_distances[1, :])
        ds = side_distances[:, wall]
        val += (min(side_distances[1, 0], side_distances[1, 2]) * min(side_distances[1, 1], side_distances[1, 3]))
        val += max(ds[1] - ds[0], 0.0)**2 + max(ds[1] - ds[2], 0.0)**2 + max(ds[1] - ds[3], 0.0)**2
    elif side == "left":
        wall = np.argmin(side_distances[2, :])
        ds = side_distances[:, wall]
        val += (min(side_distances[2, 0], side_distances[2, 2]) * min(side_distances[2, 1], side_distances[2, 3]))
        val += max(ds[2] - ds[0], 0.0)**2 + max(ds[2] - ds[1], 0.0)**2 + max(ds[2] - ds[3], 0.0)**2
    elif side == "right":
        wall = np.argmin(side_distances[3, :])
        ds = side_distances[:, wall]
        val += (min(side_distances[3, 0], side_distances[3, 2]) * min(side_distances[3, 1], side_distances[3, 3]))
        val += max(ds[3] - ds[0], 0.0)**2 + max(ds[3] - ds[1], 0.0)**2 + max(ds[3] - ds[2], 0.0)**2
    else: 
        print(side + " is not a valid side of an object.")
        return 0
    
    return val
    
def ind_close_to_fixed_object(positions, room, object_index, fixed_object_type, side = None, max_dist = 0.5):
    """ This function ensures an object is next to a fixed object in a room. 
        If side is given, the specific side of the object will be used.
        
        Args:
        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
        object_index: int, index of the object in the room's object list
        fixed_object_type: string, type of fixed object to check. One of 'window', 'door', 'socket'
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
    if len(f_objs) == 0: 
        print("There are no " + "fixed_object_type" + "s in the room.")
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

def ind_away_from_fixed_object(positions, room, object_index, fixed_object_type, min_dist = 2):
    """ This function ensures an object is not near to a fixed object in a room. 
        
        Args:
        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
        object_index: int, index of the object in the room's object list
        fixed_object_type: string, type of fixed object to check. One of 'window', 'door', 'plug'
        min_dist: float, minimum distance between the object and the fixed object to be considered away from it 
    """

    x, y = positions[3*object_index:3*object_index+2]
    w, l = room.moving_objects[object_index].width, room.moving_objects[object_index].length
    half_diag = (w**2 + l**2)/4
    f_objs = room.find_all(fixed_object_type)

    ## If any of the corners are within the minimum distance, return the sum of the distances
    distances = np.zeros(len(f_objs))
    for i in range(len(f_objs)):
        f_obj = f_objs[i]
        distances[i] = max(0.0, (min_dist ** 2)*(half_diag) - ((x - f_obj.position[0])**2 + (y - f_obj.position[1])**2)) 
     
    val = sum(distances)/(len(f_objs) * min_dist**2 * half_diag)
    
    return val

def ind_accessible(positions, room, object_index, sides):
    """ This function ensures that an object is accessible from given sides. 
        
        Args:
        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
        object_index: int, index of the object in the room's object list
        sides: a list of strings, each one one of 'top' or 'back', 'bottom' or 'front', 'left', 'right', defines which side of the object to check
    """
    
    val = 0.0 # initialise output value 

    obj = room.moving_objects[object_index]

    if obj.name == 'rug':
        return 0.0
    
    x, y, theta = positions[3*object_index:3*object_index+3]
    TL, TR, BR, BL = corners(x, y, theta, obj.width, obj.length)
    polys = []

    def project(point1, point2, distance = min(1, np.max([obj.width, obj.length, 0.5]))):
        direction = np.array([point1[0] - point2[0], point1[1] - point2[1]])
        direction /= np.linalg.norm(direction)
        return [point1[0], point1[1]] + distance * direction
    
    def wall_bounds(point):
        if point[0] < 0 or point[0] > room.width or point[1] < 0 or point[1] > room.length:
            return min(0.0, point[0])**2 + min(0.0, point[1])**2 + max(0.0, point[0] - room.width)**2 + max(0.0, point[1] - room.length)**2
        return 0.0
    
    for side in sides: 
        if side == 'top' or side == 'back':
            new_pointL = project(TL, BL)
            new_pointR = project(TR, BR)
            if np.isnan(new_pointL.any()) or np.isnan(new_pointR.any()):
                continue
            polys += [Polygon([TL, TR, new_pointR, new_pointL])]
            val += wall_bounds(new_pointL) + wall_bounds(new_pointR)
        elif side == 'bottom' or side == 'front':
            new_pointL = project(BL, TL) 
            new_pointR = project(BR, TR)
            if np.isnan(new_pointL.any()) or np.isnan(new_pointR.any()):
                continue
            polys += [Polygon([new_pointL, new_pointR, BR, BL])]
            val += wall_bounds(new_pointL) + wall_bounds(new_pointR)
        elif side == 'left':
            new_pointT = project(TL, TR)
            new_pointB = project(BL, BR)
            if np.isnan(new_pointT.any()) or np.isnan(new_pointB.any()):
                continue
            polys += [Polygon([TL, new_pointT, new_pointB, BL])]
            val += wall_bounds(new_pointT) + wall_bounds(new_pointB)
        elif side == 'right':
            new_pointT = project(TR, TL)
            new_pointB = project(BR, BL)
            if np.isnan(new_pointT.any()) or np.isnan(new_pointB.any()):
                continue
            polys += [Polygon([new_pointT, TR, BR, new_pointB])]
            val += wall_bounds(new_pointT) + wall_bounds(new_pointB)
        else: 
            print(side + " is not a valid side of the object.")
    
    for poly in polys:
        for i in range(len(room.moving_objects)):
            if i == object_index:
                continue
            
            x, y, theta = positions[3*i:3*i+3]
            poly2 = Polygon(corners(x, y, theta, room.moving_objects[i].width, room.moving_objects[i].length))
            intersection = poly.intersection(poly2)
            if intersection.area > 1e-3:
                x = np.array([[i, j] for i, j in zip(intersection.exterior.xy[0], intersection.exterior.xy[1])])
                lengths = np.roll(x, -1, axis = 0) - x
                lengths = np.linalg.norm(lengths, axis = 1)
                val += sum(lengths**2)   
        for i in range(len(room.fixed_objects)):
            if room.fixed_objects[i].name != 'door':
                continue
            else: 
                poly2 = Polygon(room.fixed_objects[i].corners())
                intersection = poly.intersection(poly2)
                if intersection.area > 1e-3:
                    x = np.array([[i, j] for i, j in zip(intersection.exterior.xy[0], intersection.exterior.xy[1])])
                    lengths = np.roll(x, -1, axis = 0) - x
                    lengths = np.linalg.norm(lengths, axis = 1)
                    val += sum(lengths**2)

    return val

def ind_central(positions, room, object_index, both = False):
    """ This function ensures that an object is centrally placed in the room. 
        Args:
        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
        object_index: int, index of the object in the room's object list
        both: bool (optional), if True, then the object should be placed centrally in both x and y. For example for a bed, this would be False, 
              but for a dining table, it should be True..
    """

    ## want the position to be in the middle 1/3 of x or the middle 1/3 of y
    lower_x, upper_x = room.width/3, 2*room.width/3
    lower_y, upper_y = room.length/3, 2*room.length/3
    mid_x, mid_y = room.width/2, room.length/2

    x, y, theta = positions[3*object_index:3*object_index+3]
    if both: 
        val = 0
        if x < lower_x: 
            val += (lower_x - x)**2
        elif x > upper_x: 
            val += (x - upper_x)**2
        else: 
            val += 0.01*(x - mid_x)**2
        if y < lower_y:
            val += (lower_y - y)**2
        elif y > upper_y:
            val += (y - upper_y)**2
        else:
            val += 0.01*(y - mid_y)**2
    else: 

        val = (min(x - lower_x, 0.0) + min(upper_x - x, 0.0))*(min(y - lower_y, 0.0) + min(upper_y - y, 0.0))

    return val

def ind_in_region(positions, room, object_index, region_name, weight = 5):
    """ This function ensures that an object is in a given region. 
        
        Args:
        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
        object_index: int, index of the object in the room's object list
        region_name: string, name of the region for the object to be in 
    """
    regions = room.regions
    region_index = room.find_region_index(region_name)
    x, y = positions[3*object_index:3*object_index+2]
    value = 0 
    for i in range(len(regions)):
        if i == region_index:
            continue
        else:
            value += ((regions[i].x - x)**2 + (regions[i].y - y)**2) - ((regions[region_index].x - x)**2 + (regions[region_index].y - y)**2)
    return 5*min(0, value)**2

def ind_in_bounds(positions, room, weight = 10): 

    """ This function ensures that all objects are within the room. This should not be used in the objective function.
        
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
        
    return weight * val 

def ind_no_overlap(positions, room, position_fixing = [], weight = 10):
    """ This function ensures that no objects overlap in the room. This should not be used in the objective function.
        
        Args:
        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
    """

    val = 0
    objs = room.moving_objects
    doors = room.find_all('door')
    door_polygons = [] 
    for door in doors: 
        door_corners = []
        if door.position[2] == 0:
            door_corners += [[door.position[0] - door.width, door.position[1]]]
            door_corners += [[door.position[0] + door.width, door.position[1]]]
            door_corners += [[door.position[0] + door.width, door.position[1] + door.width]]
            door_corners += [[door.position[0] - door.width, door.position[1] + door.width]]
        elif door.position[2] == np.pi/2:
            door_corners += [[door.position[0], door.position[1] - door.width]]
            door_corners += [[door.position[0] - door.width, door.position[1] - door.width]]
            door_corners += [[door.position[0] - door.width, door.position[1] + door.width]]
            door_corners += [[door.position[0], door.position[1] + door.width]]
        elif door.position[2] == np.pi:
            door_corners += [[door.position[0] + door.width, door.position[1]]]
            door_corners += [[door.position[0] + door.width, door.position[1] - door.width]]
            door_corners += [[door.position[0] - door.width, door.position[1] - door.width]]
            door_corners += [[door.position[0] - door.width, door.position[1]]]
        elif door.position[2] == 3*np.pi/2:
            door_corners += [[door.position[0], door.position[1] + door.width]]
            door_corners += [[door.position[0] + door.width, door.position[1] + door.width]]
            door_corners += [[door.position[0] + door.width, door.position[1] - door.width]]
            door_corners += [[door.position[0], door.position[1] - door.width]]

        door_poly = Polygon(door_corners)
        door_polygons += [door_poly]
        
    for i in range(len(objs)):

        obj_i = objs[i]

        if obj_i.name == 'rug':
            continue 

        corners_i = corners(positions[3*i], positions[3*i+1], positions[3*i+2], obj_i.width, obj_i.length)
        poly1 = Polygon(corners_i)

        for j in range(i + 1, len(objs)):

            obj_j = objs[j]

            if obj_j.name == 'rug':
                continue 

            corners_j = corners(positions[3*j], positions[3*j+1], positions[3*j+2], obj_j.width, obj_j.length)
            poly2 = Polygon(corners_j)

            intersection = poly1.intersection(poly2)
            
            if intersection.area > 0:
                x = np.array([[i, j] for i, j in zip(intersection.exterior.xy[0], intersection.exterior.xy[1])])
                lengths = np.roll(x, -1, axis = 0) - x
                lengths = np.linalg.norm(lengths, axis = 1)
                val += sum(lengths**2)
        
        
        for door in door_polygons:
            
            intersection = poly1.intersection(door)
    
            if intersection.area > 0:
                x = np.array([[i, j] for i, j in zip(intersection.exterior.xy[0], intersection.exterior.xy[1])])
                lengths = np.roll(x, -1, axis = 0) - x
                lengths = np.linalg.norm(lengths, axis = 1)
                val += sum(lengths**2)   

    return weight * val 

def ind_not_block_fixed_object(positions, room, object_index, fixed_object_type):

    """ This function ensures that an object does not block a fixed object in the room. 
        E.g. a wardrobe shouldn't block a window.
        
        Args:
        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
        object_index: int, index of the object in the room's object list
        fixed_object_type: string, type of fixed object to check. E.g one of 'window', 'door', 'plug'
    """

    val = 0
    fixed_objects = room.find_all(fixed_object_type)
    x, y, theta = positions[3*object_index:3*object_index+3]
    obj = room.moving_objects[object_index]
    cs = corners(x, y, theta, obj.width, obj.length)
    poly = Polygon(cs)

    for obj in fixed_objects: 
        if obj.name == 'window':
            x, y, theta = obj.position
            cs = corners(x, y, theta, obj.width, min(obj.length, 1))
            poly_fixed = Polygon(cs)
            intersection = poly.intersection(poly_fixed)
            if intersection.area > 1e-3:
                x = np.array([[i, j] for i, j in zip(intersection.exterior.xy[0], intersection.exterior.xy[1])])
                lengths = np.roll(x, -1, axis = 0) - x
                lengths = np.linalg.norm(lengths, axis = 1)
                val += sum(lengths**2)  
        elif obj.name == 'door':
            door_corners = []
            if obj.position[2] == 0:
                door_corners += [[obj.position[0] - obj.width, obj.position[1]]]
                door_corners += [[obj.position[0] + obj.width, obj.position[1]]]
                door_corners += [[obj.position[0] + obj.width, obj.position[1] + obj.width]]
                door_corners += [[obj.position[0] - obj.width, obj.position[1] + obj.width]]
            elif obj.position[2] == np.pi/2:
                door_corners += [[obj.position[0], obj.position[1] - obj.width]]
                door_corners += [[obj.position[0] - obj.width, obj.position[1] - obj.width]]
                door_corners += [[obj.position[0] - obj.width, obj.position[1] + obj.width]]
                door_corners += [[obj.position[0], obj.position[1] + obj.width]]
            elif obj.position[2] == np.pi:
                door_corners += [[obj.position[0] + obj.width, obj.position[1]]]
                door_corners += [[obj.position[0] + obj.width, obj.position[1] - obj.width]]
                door_corners += [[obj.position[0] - obj.width, obj.position[1] - obj.width]]
                door_corners += [[obj.position[0] - obj.width, obj.position[1]]]
            elif obj.position[2] == 3*np.pi/2:
                door_corners += [[obj.position[0], obj.position[1] + obj.width]]
                door_corners += [[obj.position[0] + obj.width, obj.position[1] + obj.width]]
                door_corners += [[obj.position[0] + obj.width, obj.position[1] - obj.width]]
                door_corners += [[obj.position[0], obj.position[1] - obj.width]]

            poly_fixed = Polygon(door_corners)
            intersection = poly.intersection(poly_fixed)
            if intersection.area > 1e-3:
                x = np.array([[i, j] for i, j in zip(intersection.exterior.xy[0], intersection.exterior.xy[1])])
                lengths = np.roll(x, -1, axis = 0) - x
                lengths = np.linalg.norm(lengths, axis = 1)
                val += sum(lengths**2)  

        else: 
            return 0.0
                
    return val

def ind_under_window(positions, room, object_index):

    """ This function ensures that the object (object_index) will be placed underneath a window.
        For example, you might want a desk or a dresser below (but not blocking) a window. You would not use this for any 
        objects that would be tall, for example a wardrobe or a fridge.
        
        Args:
        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
    """ 

    x, y = positions[3*object_index], positions[3*object_index + 2]
    windows = room.find_all('window')
    min_dist = np.inf
    for window in windows: 
        distance = (window.position[0] - x)**2 + (window.position[1] - y)**2 
        if distance < min_dist: 
            min_dist = distance

    return min_dist

def ind_aligned(positions, room):
    """ ind_aligned is a function that penalises orientations that are not one of the cardinal directions.
        Since most furniture in a room is in one of the cardinal directions, we want to encourage this. 
        This constraint is quite week in order to not prevent rotations. This should be used in all rooms.

        Args: 
        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
    """

    val = 0
    for i in range(len(room.moving_objects)):
        theta = positions[3*i + 2]
        val += (np.sin(2*theta)**2)/5
    return val

def FIX(positions, room, object_indices, weight = 10):
    """ FIX is a function that fixes the positions of moving_objects in the room. This should be applied to every primary object in the 
        room when optimising the position of the secondary objects...

        Args: 
        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
    """
    val = 0
    for i in object_indices: 
        val += np.linalg.norm(positions[3*i: 3*i + 3] - room.moving_objects[i].position)**2
    
    return weight*val 







                
















