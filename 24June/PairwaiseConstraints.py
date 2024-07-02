import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from DSL import *


def next_to(object1, object2, threshold = 1.5):

    """ A constraint function that determines whether two objects are next to each other from any side. 
        Inputs: 
        object1: Object, first object
        object2: Object, second object
        threshold: float, the maximum distance between the two objects to be classified as next to each other. 
    """

    distance = (object1.x - object2.x)**2 + (object1.y - object2.y)**2
    return distance


def next_to_side(object1, object2, side):

    """ A constraint function that determines whether object1 is next to object2 from a specific side.  
        Inputs: 
        object1: Object, first object
        object2: Object, second object
        side: 'left', 'right', 'top' or 'back', 'bottom' or 'front'. Determines which side of object2 to compare with. 
        threshold: float, the maximum distance between the two objects to be classified as next to each other. 
    """

    TL = object2.TL()
    TR = object2.TR()
    BL = object2.BL()
    BR = object2.BR()

    sides = [np.array([(BL[0] + TL[0])/2, (BL[1] + TL[1])/2]), np.array([(BR[0] + TR[0])/2, (BR[1] + TR[1])/2]), 
             np.array([(TR[0] + TL[0])/2, (TR[1] + TL[1])/2]), np.array([(BR[0] + BL[0])/2, (BR[1] + BL[1])/2])]

    distances = [np.sum((np.array([object1.x, object1.y]) - position)**2) for position in sides]

    if side == 'left':
        return ((np.argmin(distances) - 0)**2 + next_to(object1, object2))/2
    if side == 'right':
        return ((np.argmin(distances) - 1)**2  + next_to(object1, object2))/2
    if side == 'top':
        return ((np.argmin(distances) - 2)**2 + next_to(object1, object2))/2
    if side == 'bottom':
        return ((np.argmin(distances) - 3)**2 +  next_to(object1, object2))/2

    