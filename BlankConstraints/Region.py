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

    return

def away_from(positions, room, region1, region2):
    """ The function close_to returns a cost function that can be minimized to ensure that two regions are away from each other.
        
        Args:
        positions: numpy array, positions of all the regions in the room
        room: rectangular Room object
        region1: string, region name for a Region region1
        region2: string, region name for a Region region2
    """
    return

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
    return

def close_to_wall(positions, room, region, cardinal_direction = None):
    """ The function close_to_wall ensures that a region is close to a wall in a room. 
        If cardinal_direction is given, a specific wall will be checked.
        
        Args:
        positions: numpy array, positions of all the regions in the room
        room: rectangular Room object
        region: string, region name to be close to the wall
        cardinal_direction: string, one of 'N', 'S', 'E', 'W', defines which wall to check
    """

    return

def close_to_fixed_object(positions, room, region_name, fixed_object_type, maximum_distance = 1.5):
    """ The function close_to_fixed_object ensures that a region is close to a fixed object in a room. 
        
        Args:
        positions: numpy array, positions of all the regions in the room
        room: rectangular Room object
        region: string, region name to be close to the fixed object
        fixed_object_type: string, type of fixed object to check. E.g. 'window', 'door', 'socket'
        maximum_distance: float, maximum distance for the object to be defined as close to the object (optional)
    """
    return 


def away_from_fixed_object(positions, room, region_name, fixed_object_type, minimum_distance = 2.5):
    """ The function close_to_fixed_object ensures that a region is away from a fixed object type in a room. 
        
        Args:
        positions: numpy array, positions of all the regions in the room
        room: rectangular Room object
        region: region to be away from the fixed object
        fixed_object_type: string, type of fixed object to check. One of 'window', 'door', 'plug'
        minimum_distance: float, minimum distance to be away from the object (optional)
    """
    return 

def in_corner(positions, room, region, maximum_distance = 1.5):
    """ The function in_corner ensures that a region is in a corner of a room. 
        
        Args:
        positions: numpy array, positions of all the regions in the room
        room: rectangular Room object
        region: region to be in the corner
    """
    return 


def opposite(positions, room, region1, region2):
    """ The function opposite ensures that two regions are opposite to each other in a room. 
        
        Args:
        positions: numpy array, positions of all the regions in the room
        room: rectangular Room object
        region1: a Region region1
        region2: a Region region2
    """
    return 

def central(positions, room, region):
    """ The function central ensures that a region is centrally placed in the room. 
        
        Args:
        positions: numpy array, positions of all the regions in the room
        room: rectangular Room object
        region: region to be centrally placed
    """
    return 

def between(positions, room, region, region1, region2):
    """ The function between ensures that a region is between two other regions. 
        
        Args:
        room: rectangular Room object
        region: region to be between the other two regions
        region1: a Region region1
        region2: a Region region2
    """

    ## region should be closer to region1 and region2 than any other regions, and region1 and region2 should be further than region to eithe of them.
    return  

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

    return 






