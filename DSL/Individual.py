## All the Individual Object constraint functions are defined here

def next_to_wall(positions, room, object, cardinal_direction = None, side = None):
    """ The function next_to_wall ensures an object is next to a wall in a room. 
        If cardinal_direction is given, a specific wall will be used. If side is given, 
        the specific side of the object will be used.
        
        Args:
        room: rectangular Room object
        object: Object object to check 
        cardinal_direction: string, one of 'N', 'S', 'E', 'W', defines which wall to check
        side: string, one of 'top' or 'back', 'bottom' or 'front', 'left', 'right', defines which side of the object to check
    """
    return 

def next_to_fixed_object(positions, room, object, fixed_object_type, side = None):
    """ The function next_to_fixed_object ensures an object is next to a fixed object in a room. 
        If side is given, the specific side of the object will be used.
        
        Args:
        room: rectangular Room object
        object: Object object to check
        fixed_object_type: string, type of fixed object to check. One of 'window', 'door', 'plug'
        side: string, one of 'top' or 'back', 'bottom' or 'front', 'left', 'right', defines which side of the object to check
    """
    return

def accessible(positions, room, object, sides):
    """ The function accessible ensures that an object is accessible from given sides. 
        
        Args:
        room: rectangular Room object
        object: Object object to check
        sides: a list of strings, one of 'top' or 'back', 'bottom' or 'front', 'left', 'right', defines which side of the object to check
    """
    return

def central(positions, room, object):
    """ The function central ensures that an object is centrally placed in the room. 

        Args:
        room: rectangular Room object
        object: Object object to check
    """
    return

def in_region(positions, room, object_index, region_name):
    """ The function in_region ensures that an object is in a given region. 
        
        Args:
        room: rectangular Room object
        object: Object object to check
        region_name: string, name of the region for the object to be in 
    """
    regions = room.regions
    region_index = room.find_region_index(region_name)

    value = 0 
    pos = 
    return