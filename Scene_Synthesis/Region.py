## All the constraint functions for the regions are defined here.
import numpy as np 


def reg_close_to_reg(positions, room, region1_name, region2_name):
    """ This function ensures that two regions are close to each other.
        
        Args:
        positions: numpy array, positions of all the regions in the room
        room: rectangular Room object
        region1_name: a str, name of region
        region2_name: a str, name of region
    """

    ## For this function, since I don't want the regions to be on top of each other, I only 
    ## want to ensure that these regions are closer than other regions. 
    region_index_1 = room.find_region_index(region1_name)
    region_index_2 = room.find_region_index(region2_name)

    if region_index_1 == None or region_index_2 == None: 
        print("Error in inputs for reg_close_to_reg")
        return 0 

    region_position_1 = positions[2*region_index_1:2*region_index_1 + 2]
    region_position_2 = positions[2*region_index_2:2*region_index_2 + 2]

    d1d2 = np.linalg.norm(region_position_1 - region_position_2)
    d1di = [np.linalg.norm(region_position_1 - positions[2*i:2*i + 2]) for i in range(len(room.regions))]
    d2di = [np.linalg.norm(region_position_2 - positions[2*i:2*i + 2]) for i in range(len(room.regions))]
    
    value = 0
    # Want d1d2 < d1di and d1d2 < d2di for all i
    for i in range(len(room.regions)):
        if i != region_index_1 and i != region_index_2:
            value += max(0, d1d2 - d1di[i])**2 + max(0, d1d2 - d2di[i])**2

    return value/len(room.regions)

def reg_away_from_reg(positions, room, region1_name, region2_name):
    """ This function returns a cost function that can be minimized to ensure that two regions are away from each other.
        
        Args:
        positions: numpy array, positions of all the regions in the room
        room: rectangular Room object
        region1_name: string, region name for a Region region1
        region2_name: string, region name for a Region region2
    """
    ## For this function, since I don't want the regions to be in the corners I only 
    ## want to ensure that these regions are not the closest to each other. 
    region_index_1 = room.find_region_index(region1_name)
    region_index_2 = room.find_region_index(region2_name)

    if region_index_1 == None or region_index_2 == None: 
        print("Error in inputs for reg_away_from_reg")
        return 0 

    region_position_1 = positions[2*region_index_1:2*region_index_1 + 2]
    region_position_2 = positions[2*region_index_2:2*region_index_2 + 2]

    d1d2 = np.linalg.norm(region_position_1 - region_position_2)
    d1di = [np.linalg.norm(region_position_1 - positions[2*i:2*i + 2]) for i in range(len(room.regions))]
    d2di = [np.linalg.norm(region_position_2 - positions[2*i:2*i + 2]) for i in range(len(room.regions))]
    
    value = 0
    # Want d1d2 > d1di and d1d2 > d2di for all i
    for i in range(len(room.regions)):
        if i != region_index_1 and i != region_index_2:
            value += max(0, d1di[i] - d1d2)**2 + max(0, d2di[i] - d1d2)**2

    return value/len(room.regions)

def reg_include_focal_point(positions, room, region_name, window_index = None):

    """ This function finds the focal point of a room and ensures that a region is close to it. 
        If a window is given, that window will be made the focal point, otherwise, the longest wall will be made the focal point
        
        Args:
        positions: numpy array, positions of all the regions in the room
        room: rectangular Room object
        region_name: str, name of region to be close to the focal point
        window: int, index of room.fixed_objects that is the window for a focal point (optional)
        longest_wall: bool, whether the longest wall should be made the focal point (optional)
    """

    region_index = room.find_region_index(region_name)
    x, y = positions[2*region_index:2*region_index + 2]
    ## Find the focal point of the room
    if window_index: 
        window = room.fixed_objects[window_index]
        if window.name != 'window':
            print("That focal point is not a window, continuing with the longest wall method.")
            return reg_include_focal_point(positions, room, region_name)
        else: 
            focal_point = window.position[:2]
    else: 
        dws_on_walls = [[], [], [], []] # N, E, S, W
        for obj in room.fixed_objects: 
            if obj.name == 'window' or obj.name == 'door':
                if obj.position[2] == np.pi:
                    dws_on_walls[0] += [obj]
                if obj.position[2]== np.pi/2:
                    dws_on_walls[1] += [obj]
                if obj.position[2] == 0:
                    dws_on_walls[0] += [obj]
                if obj.position[2] == 3*np.pi/2:
                    dws_on_walls[3] += [obj]

        midps = [[room.width/2, room.length], [room.width, room.length/2], [room.width/2, 0], [0, room.length/2]]
        distances = [room.width, room.length, room.width, room.length]
        lambdas = [lambda x: x[1] == room.length, lambda x: x[0] == room.width, lambda x: x[1] == 0, lambda x: x[0] == 0]
        for i in range(4):
            points = [[0, 0], [0, room.length], [room.width, 0], [room.width, room.length]]
            for obj in dws_on_walls[i]:
                if i in [0, 2] and obj.name == 'window':
                    points += [[obj.position[0] - obj.width/2, obj.position[1]], [obj.position[0] + obj.width/2, obj.position[1]]]
                if i in [1, 3] and obj.name == 'window':
                    points += [[obj.position[0], obj.position[1] - obj.width/2], [obj.position[0], obj.position[1] + obj.width/2]]
                if obj.name == 'door':
                    if i == 0: 
                        points += [[obj.position[0] - obj.width, obj.position[1]], [obj.position[0], obj.position[1]]]
                    if i == 1: 
                        points += [[obj.position[0], obj.position[1]], [obj.position[0], obj.position[1] + obj.width]]
                    if i == 2: 
                        points += [[obj.position[0], obj.position[1]], [obj.position[0] + obj.width, obj.position[1]]]
                    if i == 3: 
                        points += [[obj.position[0], obj.position[1] - obj.width], [obj.position[0], obj.position[1]]]

                new_points = sorted([j[i % 2] for j in points if lambdas[i](j)])
                space = np.array(new_points[1:]) - np.array(new_points[:-1])
                index = np.argmax(space)
                midps[i][i % 2] = new_points[index] + space[index]/2
                distances[i] = space[index]

        if room.width < room.length: 
            distances[1] += (room.length - room.width)/2
            distances[3] += (room.length - room.width)/2
        if room.width > room.length:
            distances[0] += (room.width - room.length)/2
            distances[2] += (room.width - room.length)/2

        focal_point = midps[np.argmax(distances)]

    ## Now that we have the focus point, want the given region to be closer to the focus point than any of the other regions. 
    ## So want d1 < di for all i 

    val = 0
    for i in range(len(room.regions)):
        rx, ry = positions[2*i:2*i + 2]
        val += max(0,  ((focal_point[0] - x)**2 + (focal_point[1] - y)**2) - ((focal_point[0] - rx)**2 + (focal_point[1] - ry)**2))

    return val 

def reg_close_to_wall(positions, room, region_name, cardinal_direction = None):
    """ This function ensures that a region is close to a wall in a room. 
        If cardinal_direction is given, a specific wall will be checked.
        
        Args:
        positions: numpy array, positions of all the regions in the room
        room: rectangular Room object
        region_name: string, region name to be close to the wall
        cardinal_direction: string, one of 'N', 'S', 'E', 'W', defines which wall to check
    """

    region_index = room.find_region_index(region_name)
    region_position = positions[2*region_index:2*region_index + 2]

    if cardinal_direction == 'N':
        wall_distances = [(region_position[1] - room.length)**2]
    elif cardinal_direction == 'S':
        wall_distances = [region_position[1]**2]
    elif cardinal_direction == 'E':
        wall_distances = [(region_position[0] - room.width)**2]
    elif cardinal_direction == 'W':
        wall_distances = [region_position[0]**2]
    else:
        wall_distances = [region_position[1]**2, (region_position[1] - room.length)**2, region_position[0]**2, (region_position[0] - room.width)**2]

    return min(wall_distances)/max((room.width/2)**2, (room.length/2)**2)

def reg_close_to_fixed_object(positions, room, region_name, fixed_object_type, maximum_distance = 1.5):
    """ This function ensures that a region is close to a fixed object in a room. 
        
        Args:
        positions: numpy array, positions of all the regions in the room
        room: rectangular Room object
        region_name: string, region name to be close to the fixed object
        fixed_object_type: string, type of fixed object to check. E.g. 'window', 'door', 'socket'
        maximum_distance: float, maximum distance for the object to be defined as close to the object (optional)
    """

    ## Define "close to" as within 1.5 meters of the object
    max_room_distance = np.sqrt((room.width/2)**2 + (room.length/2)**2)
    region_index = room.find_region_index(region_name)
    region_position = positions[2*region_index:2*region_index + 2]

    fixed_objects = room.find_all(fixed_object_type)

    if len(fixed_objects) == 0:
        print("There are no " + fixed_object_type + "s in the room.")
        return 0
    
    fixed_object_positions = [obj.position[:2] for obj in fixed_objects]
    distances = [np.linalg.norm(region_position - obj_position) for obj_position in fixed_object_positions]
    if min(distances) < maximum_distance:
        return 0
    else:
        return (min(distances) - maximum_distance)**2/(max_room_distance - maximum_distance)**2


def reg_away_from_fixed_object(positions, room, region_name, fixed_object_type, minimum_distance = 2.5):
    """ This function ensures that a region is away from a fixed object type in a room. 
        
        Args:
        positions: numpy array, positions of all the regions in the room
        room: rectangular Room object
        region_name: string, name of region to be away from the fixed object
        fixed_object_type: string, type of fixed object to check. One of 'window', 'door', 'plug'
        minimum_distance: float, minimum distance to be away from the object (optional)
    """
    ## define away from as more than 2.5 m away from the object 
    region_index = room.find_region_index(region_name)
    region_position = positions[2*region_index:2*region_index + 2]

    fixed_objects = room.find_all(fixed_object_type)

    if len(fixed_objects) == 0:
        print("There are no " + fixed_object_type + "s in the room.")
        return 0

    fixed_object_positions = [obj.position[:2] for obj in fixed_objects]
    distances = [np.linalg.norm(region_position - obj_position) for obj_position in fixed_object_positions]
    if min(distances) > minimum_distance:
        return 0
    else: 
        return (minimum_distance - min(distances))**2/(minimum_distance**2)

def reg_in_corner(positions, room, region_name, maximum_distance = 1.5):
    """ This function ensures that a region is in a corner of a room. 
        
        Args:
        positions: numpy array, positions of all the regions in the room
        room: rectangular Room object
        region_name: region to be in the corner
    """

    corners = [[0, 0], [0, room.length], [room.width, 0], [room.width, room.length]]
    region_index = room.find_region_index(region_name)
    region_position = positions[2*region_index:2*region_index + 2]

    distances = [np.linalg.norm(region_position - corner) for corner in corners]
    if min(distances) < maximum_distance:
        return 0
    else: 
        return (min(distances) - maximum_distance)**2/(np.sqrt(room.width**2 + room.length**2) - maximum_distance)**2


def reg_opposite(positions, room, region1_name, region2_name):
    """ This function ensures that two regions are opposite to each other in a room. 
        
        Args:
        positions: numpy array, positions of all the regions in the room
        room: rectangular Room object
        region1_name: string, name of region1
        region2_name: string, name of region2
    """
    return 0

def reg_central(positions, room, region_name):
    """ This function ensures that a region is centrally placed in the room. 
        
        Args:
        positions: numpy array, positions of all the regions in the room
        room: rectangular Room object
        region_name: string, name of region to be centrally placed
    """
    ## For this function, I want to ensure that the region is in the center of the room.
    ## To do this, I am going to have the point of the region be as close to either the x center or y center

    region_index = room.find_region_index(region_name)
    x, y = positions[2*region_index:2*region_index + 2]
    mid_x, mid_y = room.width/2, room.length/2
    val = min((x - mid_x)**2,  (y - mid_y)**2)

    return val

def reg_between(positions, room, region_name, region1_name, region2_name):
    """ The function reg_between ensures that a region is between two other regions. 
        
        Args:
        room: rectangular Room object
        region_name: string, name of region to be between region1 and region2
        region1_name: string, name of region1
        region2_name: string, name of region2
    """

    ## region should be closer to region1 and region2 than any other regions, and region1 and region2 should be further than region to either of them.
    region_index = room.find_region_index(region_name)
    region1_index = room.find_region_index(region1_name)
    region2_index = room.find_region_index(region2_name)

    if region_index == None or region1_index == None or region2_index == None:
        print("Error in inputs for reg_between")
        return 0

    region_position = positions[2*region_index:2*region_index + 2]
    region1_position = positions[2*region1_index:2*region1_index + 2]
    region2_position = positions[2*region2_index:2*region2_index + 2]

    d1d = np.linalg.norm(region_position - region1_position)
    d2d = np.linalg.norm(region_position - region2_position)
    d12 = np.linalg.norm(region1_position - region2_position)
    

    return 0 

def reg_centrality(positions, room):
    """ This function ensures that all of the regions are not against the walls. This function should be used with every region constraint problem in addition to
        all other constraints. 
        
        Args:
        positions: numpy array, positions of all the regions in the room
        room: rectangular Room object
        region: region to be between the other two regions
        region1: a Region region1
        region2: a Region region2
    """
    val = 0
    center = room.center
    distances = []
    for i in range(len(room.regions)): 
        x, y = positions[2*i:2*i + 2]
        distances += [(center[0] - x)**2 + (center[1] - y)**2]
    
    mean_distance = np.mean(distances)
    for distance in distances:
        val += (distance - mean_distance)**2
    
    room_center = np.array([room.width/2, room.length/2])
    region_centroid = np.mean(positions.reshape(-1, 2), axis = 0)
    val += np.linalg.norm(region_centroid - room_center)**2

    return val 

def reg_distinct_regions(positions, room, thresh = 1):
    """ This function should be used with every region constraint problem in addition to
        all other constraints. It ensures that all of the regions are separate from each other.
        
        Args:
        positions: numpy array, positions of all the regions in the room
        room: rectangular Room object
        region: region to be between the other two regions
        region1: a Region region1
        region2: a Region region2
    """

    # Decided to penalise any region positions that are within a certain distance of each other.
    pos = positions.reshape(-1, 2)
    n = pos.shape[0]
    val = 0
    for i in range(n):
        for j in range(i + 1, n):
            dist = np.linalg.norm(pos[i, :] - pos[j, :])
            if dist < thresh:
                val += (thresh - dist)**2

    return val 
