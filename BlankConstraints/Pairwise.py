import numpy as np 
from Class_Structures import * 
from shapely.geometry import Polygon

### Throughout, the sides of the objects are defined as follows:
# 'top' or 'back' of the object would be the headboard of a bed, or the back of a chair
# 'front' or 'bottom' of the object would be the foot of a bed, or the front of a wardrobe (the side with the doors)
# 'left' would be the left side of the object, when standing behind it
# 'right' would be the right side of the object, when standing behind it


def p_next_to(positions, room, object1_index, object2_index, side1 = None, side2 = None):
    """ The function next_to ensures that two objects are next to each other in a room. 
        This should only be used when necessary e.g. for nightstands and a bed, or a desk and desk chair. 
        If side1 is given, the specific side of object1 will be used. If side2 is given, 
        the specific side of object2 will be used. E.g. the 'front' of the chair should be next to the 'back' of the desk. 
        If no side is given, then any of the sides will be used.
        
        Args:
        room: rectangular Room object
        object1: Object object
        object2: Object object
        side1: string, one of 'top' or 'back', 'bottom' or 'front', 'left', 'right', defines which side of object1 to use
        side2: string, one of 'top' or 'back', 'bottom' or 'front', 'left', 'right', defines which side of object2 to use
    """
    return

def p_away_from(positions, room, object1_index, object2_index, min_dist = 2.0):
    """ The function p_away_from ensures that two objects are away from each other in a room.
        
        Args:
        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
        object1_index: int, index of object1 in the room
        object2_index: int, index of object2 in the room
        min_dist: float, minimum distance between the two objects. Please write this as a float, e.g. 2.0.

    """
    return

def p_near(positions, room, object1_index, object2_index, max_dist = 3.0):
    """ The function next_to ensures that two objects are within a certain distance to each other. 
        They are not necessarily next to each other, but they are close.
        
        Args:
        room: rectangular Room object
        object1_index: Object object
        object2_index: Object object
        max_dist: furthest distance between the two objects. Please write this as a float, e.g. 3.0.

    """
    return 

def p_aligned(positions, room, object1_index, object2_index, center_object_info = None, max_dist = 2.0):
    """ The function aligned ensures that two objects are parallel (if no center object given) or aligned about a center object.
        If center is given, the objects will be aligned about that point. For example, 
        2 nightstands should be aligned about the bed. If center is not given, the objects will 
        be made close together with their orientations the same. 
        
        Args:

        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
        object1_index: int, index of object1 in the room
        object2_index: int, index of object2 in the room
        center_object_info: optional list where first element is the name of the object e.g. 'window' or 'bed' and the second element is the object index.
        max_dist: float, maximum distance between the two objects. Please write this as a float, e.g. 2.0.
    """
    return

def p_facing(positions, room, object1_index, object2_index, both = False):
    """ The function facing ensures that object1 is facing object2 in a room.
        If both is True, then object2 will also be facing object1.
        
        Args:
        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
        object1_index: int, index of object1 in the room
        object2_index: int, index of object2 in the room
    """
    return

def p_under_central(positions, room, object1_index, object2_index):
    """ The function under ensures that object1 (a rug) is underneath object2 (any moving_object) and centered.
        object1 MUST be a rug.
        
        Args:
        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
        object1_index: int, index of object1 in the room
        object2_index: int, index of object2 in the room
    """

    return

def p_on_top_of(positions, room, object1_index, object2_index):
    """ The function under ensures that object1 is on top of object2 (a rug)but does not ensure that it is centered.
        object2 MUST be a rug. 

        Args:
        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
        object1_index: int, index of object1 in the room
        object2_index: int, index of object2 in the room
    """

    return

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

    return

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

    return

def p_surround(positions, room, central_object_index, object_indices):
    """ The function p_surroudn ensures that central_object is surrounded by all the objects in object_indices.
        This would be used for chairs around a dining table.

        Args:
        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
        central_object_index: int, Object object
        object_indices: list of ints, indices of Object objects
    """

    return

def p_not_facing(positions, room, object1_index, object2_index):
    """ The function facing ensures that object1 is NOT facing object2 in a room.
        
        Args:
        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
        object1_index: int, index of object1 in the room
        object2_index: int, index of object2 in the room
    """
    return 

def p_between(positions, room, object1_index, object2_index, object3_index): 
    
    """ The function p_between ensures that object1 is in between the two objects object2 and object3. 
        This would be used for something like a side table being between two chairs, or maybe a bed being between two nightstands. 
        Or even a nightstand going between two beds.
        
        Args: 
        positions: list of floats, x, y, theta values for all objects in the room
        room: rectangular Room object
        object1_index: int, index of object1 in the room (** this is the object that will go in between the other two objects)
        object2_index: int, index of object2 in the room
        object3_index: int, index of object3 in the room
    """
    return 