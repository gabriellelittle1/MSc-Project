
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Object:
    
    def __init__(self, name, position, width, length, orientation = 0):
        self.name = name
        self.position = position
        self.width = width
        self.length = length
        self.orientation = orientation # in radians
    
    def get_corners(self, point = None):
        
        if not point:
            x, y = self.position
            theta = self.orientation
        else: 
            x, y, theta = point
        
        w, l = self.width, self.length
        
        TR = (x + w/2 * np.cos(theta) - l/2 * np.sin(theta), y + w/2 * np.sin(theta) + l/2 * np.cos(theta))
        BR = (x + w/2 * np.cos(theta) + l/2 * np.sin(theta), y + w/2 * np.sin(theta) - l/2 * np.cos(theta))
        TL = (x - w/2 * np.cos(theta) - l/2 * np.sin(theta), y - w/2 * np.sin(theta) + l/2 * np.cos(theta))
        BL = (x - w/2 * np.cos(theta) + l/2 * np.sin(theta), y - w/2 * np.sin(theta) - l/2 * np.cos(theta))

        return [TR, BR, TL, BL]
    
    def get_back_corners(self, point = None):
        
        if not point:
            theta = self.orientation
        else:
            theta = point[2]
        
        corners = self.get_corners(point)
        if np.cos(theta) >= 0:
            return [corners[2], corners[3]]
        else:    
            return [corners[0], corners[1]]
    

        
class Room:

    def __init__(self, width, length):
        self.width = width
        self.length = length
        self.fixed_objects = []
        self.moving_objects = []
        self.center = (width/2, length/2)

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
    
    def boundary_constraint(self, x, y, theta, object, weight = 1):

        W, L = self.width, self.length
        value = 0

        for corner in object.get_corners((x, y, theta)):

            value += np.minimum(corner[0], 0)**2 + np.maximum(corner[0] - W, 0)**2 + np.minimum(corner[1], 0)**2 + np.maximum(corner[1] - L, 0)**2
            
        return weight * value

    
    def intersection_constraint(self, x, y, theta, object, weight = 2):

        Ai = [(np.cos(theta), np.sin(theta)), (-np.sin(theta), np.cos(theta))]
        corners_i = object.get_corners((x, y, theta))

        penalty = 0

        def projection(axis, corners):
            
            minimum = 100
            maximum = -100
            for corner in corners:
                proj = corner[0] * axis[0] + corner[1] * axis[1]
                minimum = np.minimum(minimum, proj)
                maximum = np.maximum(maximum, proj)
            
            return (minimum, maximum)


        for obj in self.fixed_objects + self.moving_objects:
            if obj != object:
                xj, yj = obj.position
                theta_j = obj.orientation
                Aj = [(np.cos(theta_j), np.sin(theta_j)), (-np.sin(theta_j), np.cos(theta_j))]
                corners_j = obj.get_corners((xj, yj, theta_j))

                overlaps = []
                for axis in Ai + Aj:
                    min_i, max_i = projection(axis, corners_i)
                    min_j, max_j = projection(axis, corners_j)

                    # Calculate the overlap on this axis
                    overlaps += [max(0, min(max_i, max_j) - max(min_i, min_j))]
                    
                if np.all(overlaps) > 0:
                    penalty += weight*np.prod(overlaps)
        
        return penalty
    
    def add(self, list_of_funcs, figsize = (12, 8)):

        fig, axes = plt.subplots(1, 2, figsize = figsize)

        for ax in axes:
            ax.set_xlim(-1, self.width + 1)
            ax.set_ylim(-1, self.length + 1)
            ax.set_aspect('equal')
            ax.grid(linestyle = '--')

            rect = patches.Rectangle((0, 0), self.width, self.length, linewidth=2, edgecolor='black', facecolor='none')
            ax.add_patch(rect)

        # Draw the objects
        if self.moving_objects:
            for obj in self.moving_objects:
                rectangle = patches.Rectangle(obj.position  - np.array([obj.width/2, obj.length/2]), obj.width, obj.length, linewidth=2, edgecolor='none', facecolor='none', angle=np.rad2deg(obj.orientation), rotation_point='center')
                axes[0].add_patch(rectangle)
                line, = plt.plot([], [], label=obj.name)  # Create an invisible line
                rectangle.set_edgecolor(line.get_color())  # Use the line's color for the rectangle
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
                rectangle = patches.Rectangle(obj.position  - np.array([obj.width/2, obj.length/2]), obj.width, obj.length, linewidth=2, edgecolor='none', facecolor='none', angle=np.rad2deg(obj.orientation), rotation_point='center')
                axes[1].add_patch(rectangle)
                line, = plt.plot([], [], label=obj.name)  # Create an invisible line
                rectangle.set_edgecolor(line.get_color())  # Use the line's color for the rectangle
                axes[1].text(obj.position[0], obj.position[1], obj.name, fontsize=10)

        if self.fixed_objects:
            for obj in self.fixed_objects:
                rect = patches.Rectangle(obj.position - np.array([obj.width/2, obj.length/2]), obj.width, obj.length, linewidth=5, edgecolor='r', facecolor='none')
                axes[1].add_patch(rect)
                axes[1].text(obj.position[0] + 0.05, obj.position[1] + 0.05, obj.name, fontsize=10)

        return 
            
    def draw(self):
        fig, ax = plt.subplots()
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
                rectangle = patches.Rectangle(obj.position  - np.array([obj.width/2, obj.length/2]), obj.width, obj.length, linewidth=2, edgecolor='none', facecolor='none', angle=np.rad2deg(obj.orientation), rotation_point='center')
                ax.add_patch(rectangle)
                line, = plt.plot([], [], label=obj.name)  # Create an invisible line
                rectangle.set_edgecolor(line.get_color())  # Use the line's color for the rectangle
                ax.text(obj.position[0], obj.position[1], obj.name, fontsize=10)
        
        if self.fixed_objects:
            for obj in self.fixed_objects:
                rect = patches.Rectangle(obj.position - np.array([obj.width/2, obj.length/2]), obj.width, obj.length, linewidth=5, edgecolor='r', facecolor='none')
                ax.add_patch(rect)
                ax.text(obj.position[0] + 0.05, obj.position[1] + 0.05, obj.name, fontsize=10)

        plt.show()
        return 