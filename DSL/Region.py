## All the constraint functions for the regions are defined here.
import numpy as np 


def close_to(positions, room, region1, region2):
    """ The function close_to returns a cost function that can be minimized to ensure that two regions are close to each other.
        
        Args:
        positions: numpy array, positions of all the regions in the room
        room: rectangular Room object
        region1: a Region region1
        region2: a Region region2
    """

    ## For this function, since I don't want the regions to be on top of each other, I only 
    ## want to ensure that these regions are closer than other regions. 
    region_index_1 = room.find_region_index(region1)
    region_index_2 = room.find_region_index(region2)

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

def away_from(positions, room, region1, region2):
    """ The function close_to returns a cost function that can be minimized to ensure that two regions are away from each other.
        
        Args:
        positions: numpy array, positions of all the regions in the room
        room: rectangular Room object
        region1: string, region name for a Region region1
        region2: string, region name for a Region region2
    """
    ## For this function, since I don't want the regions to be in the corners I only 
    ## want to ensure that these regions are not the closest to each other. 
    region_index_1 = room.find_region_index(region1)
    region_index_2 = room.find_region_index(region2)

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

def include_focal_point(positions, room, region, window = None, longest_wall = False):

    """ The function focal_point finds the focal point of a room and ensures that a region is close to it. 
        If a window is given, that window will be made the focal point. If longest_wall is True, then the 
        longest wall will be made the focal point. 
        
        Args:
        positions: numpy array, positions of all the regions in the room
        room: rectangular Room object
        region: region to be close to the focal point
        window: Window object, window to be made the focal point (optional)
        longest_wall: bool, whether the longest wall should be made the focal point (optional)
    """
    return 0

def close_to_wall(positions, room, region, cardinal_direction = None):
    """ The function close_to_wall ensures that a region is close to a wall in a room. 
        If cardinal_direction is given, a specific wall will be checked.
        
        Args:
        positions: numpy array, positions of all the regions in the room
        room: rectangular Room object
        region: string, region name to be close to the wall
        cardinal_direction: string, one of 'N', 'S', 'E', 'W', defines which wall to check
    """

    region_index = room.find_region_index(region)
    region_position = positions[2*region_index:2*region_index + 2]

    if cardinal_direction == 'N':
        wall_distances = (region_position[1] - room.length)**2
    elif cardinal_direction == 'S':
        wall_distances = region_position[1]**2
    elif cardinal_direction == 'E':
        wall_distances = (region_position[0] - room.width)**2
    elif cardinal_direction == 'W':
        wall_distances = region_position[0]**2
    else:
        wall_distances = [region_position[1]**2, (region_position[1] - room.length)**2, region_position[0]**2, (region_position[0] - room.width)**2]

    return min(wall_distances)/max((room.width/2)**2, (room.length/2)**2)

def close_to_fixed_object(positions, room, region_name, fixed_object_type, maximum_distance = 1.5):
    """ The function close_to_fixed_object ensures that a region is close to a fixed object in a room. 
        
        Args:
        positions: numpy array, positions of all the regions in the room
        room: rectangular Room object
        region: string, region name to be close to the fixed object
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


def away_from_fixed_object(positions, room, region_name, fixed_object_type, minimum_distance = 2.5):
    """ The function close_to_fixed_object ensures that a region is away from a fixed object type in a room. 
        
        Args:
        positions: numpy array, positions of all the regions in the room
        room: rectangular Room object
        region: region to be away from the fixed object
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

def in_corner(positions, room, region, maximum_distance = 1.5):
    """ The function in_corner ensures that a region is in a corner of a room. 
        
        Args:
        positions: numpy array, positions of all the regions in the room
        room: rectangular Room object
        region: region to be in the corner
    """

    corners = [[0, 0], [0, room.length], [room.width, 0], [room.width, room.length]]
    region_index = room.find_region_index(region)
    region_position = positions[2*region_index:2*region_index + 2]

    distances = [np.linalg.norm(region_position - corner) for corner in corners]
    if min(distances) < maximum_distance:
        return 0
    else: 
        return (min(distances) - maximum_distance)**2/(np.sqrt(room.width**2 + room.length**2) - maximum_distance)**2


def opposite(positions, room, region1, region2):
    """ The function opposite ensures that two regions are opposite to each other in a room. 
        
        Args:
        positions: numpy array, positions of all the regions in the room
        room: rectangular Room object
        region1: a Region region1
        region2: a Region region2
    """
    return 0

def central(positions, room, region):
    """ The function central ensures that a region is centrally placed in the room. 
        
        Args:
        positions: numpy array, positions of all the regions in the room
        room: rectangular Room object
        region: region to be centrally placed
    """
    return 0 

def between(positions, room, region, region1, region2):
    """ The function between ensures that a region is between two other regions. 
        
        Args:
        room: rectangular Room object
        region: region to be between the other two regions
        region1: a Region region1
        region2: a Region region2
    """

    ## region should be closer to region1 and region2 than any other regions, and region1 and region2 should be further than region to eithe of them.
    return 0 

def region_centrality(positions, room):
    """ The function region_centrality ensures that all of the regions are not against the walls. 
        
        Args:
        positions: numpy array, positions of all the regions in the room
        room: rectangular Room object
        region: region to be between the other two regions
        region1: a Region region1
        region2: a Region region2
    """
    return 0

def distinct_regions(positions, room, thresh = 2):
    """ The function distinct_regions should be used with every region constraint problem in addition to
        all other constraints. It ensures that all of the regions are separate from each other.
        
        Args:
        positions: numpy array, positions of all the regions in the room
        room: rectangular Room object
        region: region to be between the other two regions
        region1: a Region region1
        region2: a Region region2
    """

    # Decided to penalise any region positions that are within 1 meter of each other.
    maximum_dist = np.sqrt(room.width**2 + room.length**2)
    pos = positions.reshape(-1, 2)
    n = pos.shape[0]
    val = 0
    for i in range(n):
        for j in range(i + 1, n):
            dist = np.linalg.norm(pos[i, :] - pos[j, :])
            if dist < thresh:
                val += (thresh - dist)**2/(maximum_dist - thresh)**2

    return val 





