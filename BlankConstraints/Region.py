## All the Individual Object constraint functions are defined here

def close_to(room, region1, region2):
    """ The function close_to returns a cost function that can be minimized to ensure that two regions are close to each other.
        
        Args:
        room: rectangular Room object
        region1: a Region region1
        region2: a Region region2
    """
    return 

def away_from(room, region1, region2):
    """ The function close_to returns a cost function that can be minimized to ensure that two regions are away from each other.
        
        Args:
        room: rectangular Room object
        region1: a Region region1
        region2: a Region region2
    """
    return 

def include_focal_point(room, region, window = None, longest_wall = False):

    """ The function focal_point finds the focal point of a room and ensures that a region is close to it. 
        If a window is given, that window will be made the focal point. If longest_wall is True, then the 
        longest wall will be made the focal point. 
        
        Args:
        room: rectangular Room object
        region: region to be close to the focal point
        window: Window object, window to be made the focal point (optional)
        longest_wall: bool, whether the longest wall should be made the focal point (optional)
    """
    return

def close_to_wall(room, region, cardinal_direction = None):
    """ The function close_to_wall ensures that a region is close to a wall in a room. 
        If cardinal_direction is given, a specific wall will be checked.
        
        Args:
        room: rectangular Room object
        region: region to be close to the wall
        cardinal_direction: string, one of 'N', 'S', 'E', 'W', defines which wall to check
    """
    return

def close_to_fixed_object(room, region, fixed_object_type):
    """ The function close_to_fixed_object ensures that a region is close to a fixed object in a room. 
        
        Args:
        room: rectangular Room object
        region: region to be close to the fixed object
        fixed_object_type: string, type of fixed object to check. One of 'window', 'door', 'plug'
    """
    return

def away_from_fixed_object(room, region, fixed_object_type):
    """ The function close_to_fixed_object ensures that a region is away from a fixed object type in a room. 
        
        Args:
        room: rectangular Room object
        region: region to be away from the fixed object
        fixed_object_type: string, type of fixed object to check. One of 'window', 'door', 'plug'
    """
    return

def specific_distance_from(room, region1, region2, min_dist, max_dist):
    """ The function specific_distance_from returns a cost function that can be minimized to ensure that two regions 
        are in a range of distances from one another. 
        
        Args:
        room: rectangular Room object
        region1: a Region region1
        region2: a Region region2
        min_dist: float, the closest two regions should be
        max_dist: float, the farthest two regions should be
    """
    return

def in_corner(room, region):
    """ The function in_corner ensures that a region is in a corner of a room. 
        
        Args:
        room: rectangular Room object
        region: region to be in the corner
    """
    return

def opposite(room, region1, region2):
    """ The function opposite ensures that two regions are opposite to each other in a room. 
        
        Args:
        room: rectangular Room object
        region1: a Region region1
        region2: a Region region2
    """
    return

def central(room, region):
    """ The function central ensures that a region is centrally placed in the room. 
        
        Args:
        room: rectangular Room object
        region: region to be centrally placed
    """
    return

def between(room, region, region1, region2):
    """ The function between ensures that a region is between two other regions. 
        
        Args:
        room: rectangular Room object
        region: region to be between the other two regions
        region1: a Region region1
        region2: a Region region2
    """
    return
