import numpy as np 

def next_to(room, object1, object2, side1 = None, side2 = None):
    """ The function next_to ensures that two objects are next to each other in a room. 
        If side1 is given, the specific side of object1 will be used. If side2 is given, 
        the specific side of object2 will be used. E.g. the 'front' of the chair should be next to the 'back' of the desk. 
        
        Args:
        room: rectangular Room object
        object1: Object object
        object2: Object object
        side: string, one of 'top' or 'back', 'bottom' or 'front', 'left', 'right', defines which side of the object to check
    """
    return

def away_from(room, object1, object2):
    """ The function away_from ensures that two objects are away from each other in a room.
        
        Args:
        room: rectangular Room object
        object1: Object object
        object2: Object object
    """
    return 

def aligned(room, object1, object2, center = None):
    """ The function aligned ensures that two objects are aligned in a room. 
        If center is given, the objects will be aligned about that point. For example, 
        2 nightstands should be aligned about the bed. If center is not given, the objects will 
        be made close together with their orientations the same. 
        
        Args:
        room: rectangular Room object
        object1: Object object
        object2: Object object
        center: tuple, (x, y), point to be parallel to
    """
    return


def facing(room, object1, object2, both = False):
    """ The function facing ensures that object1 is facing object2 in a room.
        If both is True, then object2 will also be facing object1.
        
        Args:
        room: rectangular Room object
        object1: Object object
        object2: Object object
    """
    return

def under(room, object1, object2):
    """ The function under ensures that object1 is underneath object2. 
        
        Args:
        room: rectangular Room object
        object1: Object object
        object2: Object object
    """
    return