import numpy as np
from Class_Structures import Object, Room, Region

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
        if name == 'door':
            x = width + position*(room.width - width)
            y = room.length
            theta = np.pi
        else: 
            x = width/2 + position*(room.width - width)
            y = room.length
            theta = np.pi
    
    elif wall == 'east':
        
        if name == 'door':
            x = room.width
            y = position*(room.length - width)
            theta = np.pi/2
        else:
            x = room.width
            y = width/2 + position*(room.length - width)
            theta = np.pi/2
    
    elif wall == 'south':

        if name == 'door':
            x = position*(room.width - width)
            y = 0
            theta = 0
        else:
            x = width/2 + position*(room.width - width)
            y = 0
            theta = 0

    else:

        if name == 'door':
            x = 0
            y = width + position*(room.length - width)
            theta = 3*np.pi/2
        else: 
            x = 0
            y = width/2 + position*(room.length - width)
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

def region_setup(room, name, index):

    """ A function that initialises the regions in a room randomly.
        Inputs:
        room: Room, the room from which the object is to be removed
        name: str, the name of the region e.g 'sleeping'
        index: int, the index of the region (0, 1, 2, ...). First one must be 0, and the rest must be in order.
    """

    x = np.random.uniform(0, room.width)
    y = np.random.uniform(0, room.length)

    region = Region(name, x, y, index)
    room.regions += [region]

    return region


