import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Object:
    
    def __init__(self, name, position, width, length):
        self.name = name
        self.position = position
        self.width = width
        self.length = length
        
class Room:

    def __init__(self, width, length):
        self.width = width
        self.length = length
        self.fixed_objects = []
        self.moving_objects = []
        self.center = (width/2, length/2)

    def find(self, name):

        """ Find an object by name in the room."""
        for obj in self.fixed_objects + self.moving_objects:
            if obj.name == name:
                return obj
        return None
    
    def find_all(self, name):
        
        """ Find all objects by name in the room."""

        objects = []
        for obj in self.fixed_objects + self.moving_objects:
            if obj.name == name:
                objects.append(obj)
        return objects
    
    def count(self, name):

        """ Count the number of objects by name in the room."""

        counter = 0
        for obj in self.fixed_objects + self.moving_objects:
            if obj.name == name:
                counter += 1
        return counter
    
    def boundary_constraint(self, x, y, object, weight = 3):

        """ Constraint: Boundary Constraint (Room Walls) """

        w, l = object.width, object.length
        W, L = self.width, self.length
        
        return weight * (np.maximum(0, w/2 - x)**2 + np.maximum(0, x + w/2 - W)**2 + np.maximum(0, l/2 - y)**2 + np.maximum(0, y + l/2 - L)**2)
    
    def intersection_constraint(self, x, y, object, weight = 2):

        """ Constraint: Intersection Constraint """

        value = 0
        w, l = object.width, object.length

        for obj in self.fixed_objects + self.moving_objects:
            if obj != object:
                xi, yi = obj.position
                wi, li = obj.width, obj.length
                value += np.maximum(0, w/2 + wi/2 - np.abs(x - xi)) * np.maximum(0, l/2 + li/2 - np.abs(y - yi))

        return weight * value
    
    def balance_constraint(self, x, y, object, weight = 1):

        """ Constraint: Room Balance """

        center_of_mass = object.width*object.length*np.array([x, y])
        total_weight = object.width*object.length
        
        for obj in self.moving_objects:
            if obj != object:
                center_of_mass += obj.width * obj.length * np.array(obj.position)
                total_weight += obj.width * obj.length
       
        center_of_mass /= total_weight
        c_balance = np.sum((center_of_mass - np.array([self.center[0], self.center[1]]))**2)
        return weight * c_balance
    
    def add(self, list_of_funcs, figsize = (12, 8)):

        """ Add objects to the room in a given order. """

        fig, axes = plt.subplots(1, 2, figsize = figsize)

        for ax in axes:
            ax.set_xlim(-1, self.width + 1)
            ax.set_ylim(-1, self.length + 1)
            ax.set_aspect('equal')
            ax.grid(linestyle = '--')

            rect = patches.Rectangle((0, 0), self.width, self.length, linewidth=2, edgecolor='black', facecolor='none')
            ax.add_patch(rect)

        if self.moving_objects:
            for obj in self.moving_objects:
                rect = patches.Rectangle(obj.position - np.array([obj.width/2, obj.length/2]), obj.width, obj.length, linewidth=2, edgecolor='none', facecolor='none')
                axes[0].add_patch(rect)
                line, = plt.plot([], [], label=obj.name)  # Create an invisible line
                rect.set_edgecolor(line.get_color())  # Use the line's color for the rectangle
                axes[0].text(obj.position[0], obj.position[1], obj.name, fontsize=10)

        if self.fixed_objects:
            for obj in self.fixed_objects:
                rect = patches.Rectangle(obj.position - np.array([obj.width/2, obj.length/2]), obj.width, obj.length, linewidth=5, edgecolor='r', facecolor='none')
                axes[0].add_patch(rect)
                axes[0].text(obj.position[0] + 0.05, obj.position[1] + 0.05, obj.name, fontsize=10)

        for func in list_of_funcs:
            func(self)
        
        if self.moving_objects:
            for obj in self.moving_objects:
                rect = patches.Rectangle(obj.position - np.array([obj.width/2, obj.length/2]), obj.width, obj.length, linewidth=2, edgecolor='none', facecolor='none')
                axes[1].add_patch(rect)
                line, = plt.plot([], [], label=obj.name)  # Create an invisible line
                rect.set_edgecolor(line.get_color())  # Use the line's color for the rectangle
                axes[1].text(obj.position[0], obj.position[1], obj.name, fontsize=10)

        if self.fixed_objects:
            for obj in self.fixed_objects:
                rect = patches.Rectangle(obj.position - np.array([obj.width/2, obj.length/2]), obj.width, obj.length, linewidth=5, edgecolor='r', facecolor='none')
                axes[1].add_patch(rect)
                axes[1].text(obj.position[0] + 0.05, obj.position[1] + 0.05, obj.name, fontsize=10)

        return 
            


    def draw(self):

        """ Draw the room with all objects. """
        
        fig, ax = plt.subplots()
        ax.set_xlim(-1, self.width + 1)
        ax.set_ylim(-1, self.length + 1)
        ax.set_aspect('equal')
        ax.grid(linestyle = '--')

        rect = patches.Rectangle((0, 0), self.width, self.length, linewidth=2, edgecolor='black', facecolor='none')
        ax.add_patch(rect)

        if self.moving_objects:
            for obj in self.moving_objects:
                rect = patches.Rectangle(obj.position - np.array([obj.width/2, obj.length/2]), obj.width, obj.length, linewidth=2, edgecolor='none', facecolor='none')
                ax.add_patch(rect)
                line, = plt.plot([], [], label=obj.name)  # Create an invisible line
                rect.set_edgecolor(line.get_color())  # Use the line's color for the rectangle
                ax.text(obj.position[0], obj.position[1], obj.name, fontsize=10)

        if self.fixed_objects:
            for obj in self.fixed_objects:
                rect = patches.Rectangle(obj.position - np.array([obj.width/2, obj.length/2]), obj.width, obj.length, linewidth=5, edgecolor='r', facecolor='none')
                ax.add_patch(rect)
                ax.text(obj.position[0] + 0.05, obj.position[1] + 0.05, obj.name, fontsize=10)

        plt.show()
        return
