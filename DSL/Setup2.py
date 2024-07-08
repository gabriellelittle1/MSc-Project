import numpy as np
from Class_Structures import Object, Room, Region


def create_object(room, name, width, length, region_name):
    """ A function that creates an object.
        Inputs:
        room: Room for the object to be put in
        name: str, name of the object all lowercase. E.g. 'window'
        width: float, width of the object (m)
        length: float, length of the object (m)
        region_name: str, name of the region where the object is to be placed
    """
    
    region_index = room.find_region_index(region_name)

    # Ensure the initial position is within the room 
    if room.regions[region_index].x + width/2 > room.width:
        obj_x = room.width - width/2
    elif room.regions[region_index].x  - width/2 < 0:
        obj_x = width/2
    else: 
        obj_x = room.regions[region_index].x

    if room.regions[region_index].y + length/2 > room.length:
        obj_y = room.length - length/2
    elif room.regions[region_index].y - length/2 < 0:
        obj_y = length/2
    else:
        obj_y = room.regions[region_index].y

    new_object = Object(name, width, length, (obj_x, obj_y, 0))
    room.moving_objects += [new_object]

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

