import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Object:

    def __init__(self, name, width, length, position = None):

        """ Initialization of an object in a scene. 
            Inputs: 
            name: str, name of the object all lowercase
            width: float, width of the object
            length: float, length of the object
            position: tuple (x, y, theta), where x, y are the coordinates of the center of the 
                      object and theta is the orientation of the object in radians.
        """

        if position:
            self.x, self.y, self.orientation = position 
            self.position = position
        
        if not position: 
            self.x = 0
            self.y = 0
            self.orientation = 0
            self.position = (0, 0, 0)
            position = self.position

        self.name = name
        self.width = width 
        self.length = length

    def TR(self):
        x, y, theta = self.position
        w, l = self.width, self.length
        return (x + w/2 * np.cos(theta) + l/2 * np.sin(theta), y + w/2 * np.sin(theta) - l/2 * np.cos(theta))
    
    def TL(self):
        x, y, theta = self.position
        w, l = self.width, self.length
        return (x - w/2 * np.cos(theta) + l/2 * np.sin(theta), y - w/2 * np.sin(theta) - l/2 * np.cos(theta))

    def BR(self):
        x, y, theta = self.position
        w, l = self.width, self.length
        return (x + w/2 * np.cos(theta) - l/2 * np.sin(theta), y + w/2 * np.sin(theta) + l/2 * np.cos(theta))

    def BL(self):
        x, y, theta = self.position
        w, l = self.width, self.length
        return (x - w/2 * np.cos(theta) - l/2 * np.sin(theta), y - w/2 * np.sin(theta) + l/2 * np.cos(theta))
    
    def corners(self):
        return [self.TR(), self.BR(), self.TL(), self.BL()]
    
    def back_corners(self):
        return [self.TR(), self.TL()]


class Room: 

    def __init__(self, width, length, fixed_objects = [], moving_objects = []):

        self.width = width
        self.length = length
        self.fixed_objects = fixed_objects
        self.moving_objects = moving_objects
        self.center = (width/2, length/2)
        self.regions = []
    
    def windows_on_wall(self, cardinal_direction):

        """ Returns the number of windows on a given wall of the room.
            Inputs: 
            cardinal_direction: str, one of N, S, E, W
            Outputs:
            num_windows: int, number of windows on the wall
        """

        num_windows = 0
        if cardinal_direction == 'S':
            crit = lambda obj: obj.y == 0
        elif cardinal_direction == 'N':
            crit = lambda obj: obj.y == self.length
        elif cardinal_direction == 'E':
            crit = lambda obj: obj.x == self.width
        elif cardinal_direction == 'W':
            crit = lambda obj: obj.x == 0
        else:
            raise ValueError('Invalid Cardinal Direction. Please enter one of N, S, E, W.')

        if self.fixed_objects:
            for obj in self.fixed_objects:
                if obj.name in ['window', 'Window']:
                    if crit(obj):
                        num_windows += 1
        
        return num_windows 
    
    def add_object(self, obj):

        """ Adds an object to the room.
            Inputs:
            obj: Object, object to be added to the room
        """

        if obj.name in ['door', 'Doors', 'plug', 'Plug', 'window', 'Window']:
            if not obj.position:
                raise ValueError('Position of fixed objects must be specified.')
            self.fixed_objects.append(obj)
        else:
            if obj.position == (0, 0, 0):
                obj = Object(obj.name, obj.width, obj.length, (self.center[0], self.center[1], 0))
            self.moving_objects.append(obj)
        return 
    
    def doors_on_wall(self, cardinal_direction):

        """ Returns the number of doors on a given wall of the room.
            Inputs: 
            cardinal_direction: str, one of N, S, E, W
            Outputs:
            num_doors: int, number of doors on the wall
        """

        num_doors = 0
        if cardinal_direction == 'S': # South wall
            crit = lambda obj: obj.y == 0
        elif cardinal_direction == 'N': # North wall
            crit = lambda obj: obj.y == self.length
        elif cardinal_direction == 'E': # East wall
            crit = lambda obj: obj.x == self.width
        elif cardinal_direction == 'W': # West wall
            crit = lambda obj: obj.x == 0
        else:
            raise ValueError('Invalid Cardinal Direction. Please enter one of N, S, E, W.')

        if self.fixed_objects:
            for obj in self.fixed_objects:
                if obj.name in ['door', 'Doors']:
                    if crit(obj):
                        num_doors += 1
        
        return num_doors 
    
    def find(self, name):
        for obj in self.fixed_objects + self.moving_objects:
            if obj.name == name:
                return obj
        return None
    
    def find_all(self, name):
        objects = []
        for obj in self.fixed_objects + self.moving_objects:
            if obj.name == name:
                objects.append(obj)
        return objects
    
    def count(self, name):
        counter = 0
        for obj in self.fixed_objects + self.moving_objects:
            if obj.name == name:
                counter += 1
        return counter
    
    def draw(self, draw_regions = False):

        """ Draws the room with all the objects in it."""
        fig, ax = plt.subplots(figsize = (10, 10))
        ax.set_xlim(-1, self.width + 1)
        ax.set_ylim(-1, self.length + 1)
        ax.set_aspect('equal')
        ax.grid(linestyle = '--')

        # Draw the room
        rect = patches.Rectangle((0, 0), self.width, self.length, linewidth=2, edgecolor='black', facecolor='none')
        ax.add_patch(rect)

        # Draw the objects
        if self.moving_objects:
            for obj in self.moving_objects:
                rectangle = patches.Rectangle(obj.position[:2]  - np.array([obj.width/2, obj.length/2]), obj.width, obj.length, linewidth=2, edgecolor='none', facecolor='none', angle=np.rad2deg(obj.position[2]), rotation_point='center')
                ax.add_patch(rectangle)
                line, = plt.plot([], [], label=obj.name)  # Create an invisible line
                rectangle.set_edgecolor(line.get_color())  # Use the line's color for the rectangle
                ax.text(obj.position[0], obj.position[1], obj.name, fontsize=10)
                corners = obj.back_corners()
                for corner in corners:
                    ax.plot(corner[0], corner[1], color = line.get_color(), marker = 'o')
        
        if self.fixed_objects:
            for obj in self.fixed_objects:
                if obj.name == 'window':
                    rect = patches.Rectangle(obj.position[:2] - np.array([obj.width/2, obj.length/2]), obj.width, obj.length, linewidth=5, edgecolor='r', facecolor='none', angle=np.rad2deg(obj.position[2]), rotation_point='center')
                    ax.add_patch(rect)
                    #ax.text(obj.position[0], obj.position[1], obj.name, fontsize=10)
                elif obj.name == 'door':
                    wedge = patches.Wedge(center=obj.position[:2], r=obj.width, 
                                          theta1=np.rad2deg(obj.position[2]), theta2=np.rad2deg(obj.position[2]) + 90, linewidth=3, edgecolor='r', facecolor='none')
                    ax.add_patch(wedge)
                    #ax.text(obj.position[0], obj.position[1], obj.name, fontsize=10, color='red')
                elif obj.name == 'socket':
                    x, y = obj.position[:2]
                    ax.plot([x - 0.05, x + 0.05], [y - 0.05, y + 0.05], color='red', linewidth=2)
                    ax.plot([x - 0.05, x + 0.05], [y + 0.05, y - 0.05], color='red', linewidth=2)

        if draw_regions: 
            for region in self.regions:
                name, x, y = region
                ax.plot(x, y, 'o', markersize=10) 
                ax.text(x, y, name, fontsize=10)
        
        
        plt.show()



        return 



