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

    return

def reg_away_from_reg(positions, room, region1_name, region2_name):
    """ This function returns a cost function that can be minimized to ensure that two regions are away from each other.
        
        Args:
        positions: numpy array, positions of all the regions in the room
        room: rectangular Room object
        region1_name: string, region name for a Region region1
        region2_name: string, region name for a Region region2
    """
    return

def reg_include_focal_point(positions, room, region_name, window_index = None):

    """ This function finds the focal point of a room and ensures that a region is close to it. 
        If a window is given, that window will be made the focal point, otherwise, the longest wall will be made the focal point.
        This function should only be called once in each optimization function as there is only ONE focal point, and only one region can have it.
        
        Args:
        positions: numpy array, positions of all the regions in the room
        room: rectangular Room object
        region_name: str, name of region to be close to the focal point
        window: int, index of room.fixed_objects that is the window for a focal point (optional)
        longest_wall: bool, whether the longest wall should be made the focal point (optional)
    """
    return

def reg_close_to_wall(positions, room, region_name, cardinal_direction = None):
    """ This function ensures that a region is close to a wall in a room. 
        If cardinal_direction is given, a specific wall will be checked.
        
        Args:
        positions: numpy array, positions of all the regions in the room
        room: rectangular Room object
        region_name: string, region name to be close to the wall
        cardinal_direction: string, one of 'N', 'S', 'E', 'W', defines which wall to check
    """

    return

def reg_close_to_fixed_object(positions, room, region_name, fixed_object_type, maximum_distance = 1.5):
    """ This function ensures that a region is close to a fixed object in a room. 
        
        Args:
        positions: numpy array, positions of all the regions in the room
        room: rectangular Room object
        region_name: string, region name to be close to the fixed object
        fixed_object_type: string, type of fixed object to check. E.g. 'window', 'door', 'socket'
        maximum_distance: float, maximum distance for the object to be defined as close to the object (optional)
    """

    return


def reg_away_from_fixed_object(positions, room, region_name, fixed_object_type, minimum_distance = 2.5):
    """ This function ensures that a region is away from a fixed object type in a room. 
        
        Args:
        positions: numpy array, positions of all the regions in the room
        room: rectangular Room object
        region_name: string, name of region to be away from the fixed object
        fixed_object_type: string, type of fixed object to check. One of 'window', 'door', 'plug'
        minimum_distance: float, minimum distance to be away from the object (optional)
    """
    return

def reg_in_corner(positions, room, region_name, maximum_distance = 1.5):
    """ This function ensures that a region is in a corner of a room. 
        
        Args:
        positions: numpy array, positions of all the regions in the room
        room: rectangular Room object
        region_name: region to be in the corner
    """

    return


def reg_opposite(positions, room, region1_name, region2_name):
    """ This function ensures that two regions are opposite to each other in a room. 
        
        Args:
        positions: numpy array, positions of all the regions in the room
        room: rectangular Room object
        region1_name: string, name of region1
        region2_name: string, name of region2
    """
    return

def reg_central(positions, room, region_name):
    """ This function ensures that a region is centrally placed in the room. 
        
        Args:
        positions: numpy array, positions of all the regions in the room
        room: rectangular Room object
        region_name: string, name of region to be centrally placed
    """
    return

def reg_between(positions, room, region_name, region1_name, region2_name):
    """ The function reg_between ensures that a region is between two other regions. 
        
        Args:
        room: rectangular Room object
        region_name: string, name of region to be between region1 and region2
        region1_name: string, name of region1
        region2_name: string, name of region2
    """

    return

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
    return

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
    return