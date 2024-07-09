## All the Individual Object constraint functions are defined here
from Class_Structures import *
from shapely.geometry import Polygon

def ind_next_to_wall(positions, room, object_index, cardinal_direction = None, side = None):
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

    return
    
def ind_close_to_fixed_object(positions, room, object_index, fixed_object_type, side = None, max_dist = 0.5):
    """ This function ensures an object is next to a fixed object in a room. 
        If side is given, the specific side of the object will be used.
        
        Args:
        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
        object_index: int, index of the object in the room's object list
        fixed_object_type: string, type of fixed object to check. One of 'window', 'door', 'plug'
        side: string, one of 'top' or 'back', 'bottom' or 'front', 'left', 'right', defines which side of the object to check
    """

    return

def ind_away_from_fixed_object(positions, room, object_index, fixed_object_type, min_dist = 2):
    """ This function ensures an object is not near to a fixed object in a room. 
        
        Args:
        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
        object_index: int, index of the object in the room's object list
        fixed_object_type: string, type of fixed object to check. One of 'window', 'door', 'plug'
        min_dist: float, minimum distance between the object and the fixed object to be considered away from it 
    """

    return

def ind_accessible(positions, room, object_index, sides):
    """ This function ensures that an object is accessible from given sides. 
        
        Args:
        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
        object_index: int, index of the object in the room's object list
        sides: a list of strings, one of 'top' or 'back', 'bottom' or 'front', 'left', 'right', defines which side of the object to check
    """
    return 

def ind_central(positions, room, object_index):
    """ This function ensures that an object is centrally placed in the room. 
        Args:
        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
        object_index: int, index of the object in the room's object list
    """

    return

def ind_in_region(positions, room, object_index, region_name):
    """ This function ensures that an object is in a given region. 
        
        Args:
        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
        object_index: int, index of the object in the room's object list
        region_name: string, name of the region for the object to be in 
    """
    return

def ind_in_bounds(positions, room): 

    """ This function ensures that all objects are within the room. This must be used in every constraint solving problem for Individual constraint types.
        
        Args:
        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
    """
    return

def ind_no_overlap(positions, room):
    """ This function ensures that no objects overlap in the room. This should be used in every constraint satisfaction problem.
        
        Args:
        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
    """
    return
                
















