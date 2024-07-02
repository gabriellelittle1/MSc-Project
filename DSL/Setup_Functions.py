import numpy as np
from Class_Structures import Object, Room

def create_room(width, length):
    """ A function that creates an empty room.
        Inputs:
        width: float, width of the room (meters)
        length: float, length of the room (meters)
        Outputs:
        room: Room, an empty room with the specified dimensions
    """

    new_room = Room(width, length)
    new_room.fixed_objects = []

    return new_room

def create_fixed_object(room, name, width, length, wall, position = None):
    """ A function that creates an object.
        Inputs:
        room: Room for the object to be put in
        name: str, name of the object all lowercase. E.g. 'window'
        width: float, width of the object (m)
        length: float, length of the object (m)
        wall: wall for the object to be put on, one of 'north', 'east', 'south', 'west'
        position: float object (between 0 and 1) that determines where on the wall it is placed. E.g if wall is 'north', 
                  position might be 0.5, which means the object is at position (0.5*room.width, room.length).
    """
    
    if wall not in ['north', 'east', 'south', 'west']:
        print("Invalid wall entered. Please enter one of 'north', 'east', 'south', 'west'.")
        return 
    
    elif wall == 'north':
        x = position*room.width
        y = room.length
        theta = np.pi
    
    elif wall == 'east':
        x = room.width
        y = position*room.length
        theta = np.pi/2
    
    elif wall == 'south':
        x = position*room.width
        y = 0
        theta = 0

    else:
        x = 0
        y = position*room.length
        theta = 3*np.pi/2
    
    room.fixed_objects += [Object(name, width, length, (x, y, theta))]
    return 


def remove_object(room, obj):
    """ A function that removes an object from the room.
        Inputs:
        room: Room, the room from which the object is to be removed
        object: Object, the object to be removed
    """
    if obj in room.fixed_objects:
        room.fixed_objects.remove(obj)
    elif obj in room.movable_objects:
        room.moving_objects.remove(obj)
    return

def region_setup(room, name):

    """ A function that initialises the regions in a room randomly.
        Inputs:
        room: Room, the room from which the object is to be removed
        name: str, the name of the region e.g 'sleeping'
    """

    x = np.random.uniform(0, room.width)
    y = np.random.uniform(0, room.length)
    
    room.regions += [(name, x, y)]

    return 


