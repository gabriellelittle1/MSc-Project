import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from DSL import *

def next_to_wall(room, object, cardinal_direction = None, threshold = 0.2):

    """ A function to determine whether an object is next to any wall in the room. 
        Inputs:
        room: Room, the room object
        object: Object, the object to be checked. 
        cardinal_direction: 'N', 'S', 'E', 'W'. If specified, the function will check if the object is next to the wall in the specified direction.
        threshold: float, the maximum distance between the object and the wall to be classified as next to the wall.
    """
    corners = object.corners()
    minimum_distance = np.inf

    if not cardinal_direction:
        for corner in corners: 
            distances = [corner[0], corner[1], room.width - corner[0], room.length - corner[1]]
            distances = [i**2 for i in distances]
            if min(distances) < minimum_distance:
                minimum_distance = min(distances)
    elif cardinal_direction == 'N':
        for corner in corners:
            distance = (room.length - corner[1])**2
            if distance < minimum_distance:
                minimum_distance = distance
    elif cardinal_direction == 'S':
        for corner in corners:
            distance = corner[1]**2
            if distance < minimum_distance:
                minimum_distance = distance
    elif cardinal_direction == 'E':
        for corner in corners:
            distance = (room.width - corner[0])**2
            if distance < minimum_distance:
                minimum_distance = distance
    elif cardinal_direction == 'W':
        for corner in corners:
            distance = corner[0]**2
            if distance < minimum_distance:
                minimum_distance = distance
    
    return minimum_distance

def side_next_to_wall(room, object, side, cardinal_direction = None, threshold = 0.2):

    """ A function to determine whether a specific side of an object is next to a wall.
        Inputs:
        room: Room, the room object
        object: Object, the object to be checked.
        side: 'left', 'right', 'top' or 'back', 'bottom' or 'front'. Determines which side of the object to check. 
        cardinal_direction: 'N', 'S', 'E', 'W'. If specified, the function will check if the object is next to the wall in the specified direction.
        threshold: float, the maximum distance between the object and the wall to be classified as next to the wall.
    """
    all_corners = object.corners() # TR, BR, TL, BL
    if side == 'left':
        corners = all_corners[2:4]
        other_corners = all_corners[0:2]
    elif side == 'right':
        corners = all_corners[0:2]
        other_corners = all_corners[2:4]
    elif side == 'top' or side == 'back':
        corners = [all_corners[0], all_corners[2]]
        other_corners = [all_corners[1], all_corners[3]]
    elif side == 'bottom' or side == 'front':
        corners = [all_corners[1], all_corners[3]]
        other_corners = [all_corners[0], all_corners[2]]
    else:
        raise ValueError("Side must be one of 'left', 'right', 'top', 'back', 'bottom', 'front'.")

    if not cardinal_direction:        
        distances = np.zeros((2, 4))
        for i in range(2):
            distances[i, :] = [corners[i][0], corners[i][1], room.width - corners[i][0], room.length - corners[i][1]]
            distances[i, :] = [j**2 for j in distances[i, :]]
        
        return max(np.min(distances[0, :]), np.min(distances[1, :])) + (np.argmin(distances[0, :]) - np.argmin(distances[1, :]))**2 # and max(np.min(distances[0, :]), np.min(distances[1, :])) <= threshold**2

    else:
        if cardinal_direction == 'N':
            ds = [(room.length - corner[1])**2 for corner in corners]
            other_ds =  [(room.length - corner[1])**2 for corner in other_corners]
        elif cardinal_direction == 'S':
            ds = [corner[1]**2 for corner in corners]
            other_ds = [corner[1]**2 for corner in other_corners]
        elif cardinal_direction == 'E':
            ds = [(room.width - corner[0])**2 for corner in corners]
            other_ds = [(room.width - corner[0])**2 for corner in other_corners]
        elif cardinal_direction == 'W':
            ds = [corner[0]**2 for corner in corners]
            other_ds = [corner[0]**2 for corner in other_corners]
        else: 
            raise ValueError("If specified, Cardinal direction must be one of N, E, S, W.") 
        
        closest_penalty = 0
        for i in range(2):
            for j in range(2):
                closest_penalty += max((ds[i] - other_ds[j]), 0.0)**2
                
        return closest_penalty + ds[0]**2 + ds[1]**2
    


        

