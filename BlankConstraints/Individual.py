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

    return
    
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

    return

def ind_away_from_fixed_object(positions, room, object_index, fixed_object_type, min_dist = 2):
    """ This function ensures an object is not near to a fixed object in a room. 
        
        Args:
        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
        object_index: int, index of the object in the room's object list
        fixed_object_type: string, type of fixed object to check. One of 'window', 'door', 'socket'
        min_dist: float, minimum distance between the object and the fixed object to be considered away from it 
    """

    return

def ind_accessible(positions, room, object_index, sides):
    """ This function ensures that an object is accessible from given sides. 
        
        Args:
        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
        object_index: int, index of the object in the room's object list
        sides: a list of strings, each one one of 'top' or 'back', 'bottom' or 'front', 'left', 'right', defines which side of the object to check
    """
    
    return

def ind_central(positions, room, object_index, both = False):
    """ This function ensures that an object is centrally placed in the room. 
        Args:
        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
        object_index: int, index of the object in the room's object list
        both: bool (optional), if True, then the object should be placed centrally in both x and y. For example for a bed, this would be False, 
              but for a dining table, it should be True..
    """

    return

def ind_in_bounds(positions, room, weight = 15): 

    """ This function ensures that all objects are within the room. THIS SHOULD BE USED IN EVERY OPTIMISATION FUNCTION.
        
        Args:
        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
    """
    return

def ind_no_overlap(positions, room, position_fixing = []):
    """ This function ensures that no objects overlap in the room. THIS SHOULD BE USED IN EVERY OPTIMISATION FUNCTION.
        
        Args:
        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
    """

    return

def ind_not_block_fixed_object(positions, room, object_index, fixed_object_type):

    """ This function ensures that an object does not block a fixed object in the room. 
        E.g. a wardrobe shouldn't block a window.
        
        Args:
        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
        object_index: int, index of the object in the room's object list
        fixed_object_type: string, type of fixed object to check. E.g one of 'window', 'door', 'plug'
    """

    return

def ind_under_window(positions, room, object_index):

    """ This function ensures that the object (object_index) will be placed underneath a window.
        For example, you might want a desk or a dresser below (but not blocking) a window. You would not use this for any 
        objects that would be tall, for example a wardrobe or a fridge.
        
        Args:
        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
    """ 

    return

def ind_aligned(positions, room):
    """ ind_aligned is a function that penalises orientations that are not one of the cardinal directions.
        Since most furniture in a room is in one of the cardinal directions, we want to encourage this. 
        This constraint is quite week in order to not prevent rotations. This should be used in all rooms.

        Args: 
        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
    """

    return







                
















