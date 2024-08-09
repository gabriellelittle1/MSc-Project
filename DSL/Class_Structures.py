import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy.spatial import Voronoi, voronoi_plot_2d
import scipy as sp
import sys
import copy
from shapely.geometry import Polygon, Point

def TR(x, y, theta, w, l):
    return (x + w/2 * np.cos(theta) + l/2 * np.sin(theta), y + w/2 * np.sin(theta) - l/2 * np.cos(theta))

def TL(x, y, theta, w, l):
    return (x - w/2 * np.cos(theta) + l/2 * np.sin(theta), y - w/2 * np.sin(theta) - l/2 * np.cos(theta))

def BR(x, y, theta, w, l):
    return (x + w/2 * np.cos(theta) - l/2 * np.sin(theta), y + w/2 * np.sin(theta) + l/2 * np.cos(theta))

def BL(x, y, theta, w, l):
    return (x - w/2 * np.cos(theta) - l/2 * np.sin(theta), y - w/2 * np.sin(theta) + l/2 * np.cos(theta))

def corners(x, y, theta, w, l): # TL, TR, BR, BL
    return [TL(x, y, theta, w, l), TR(x, y, theta, w, l), BR(x, y, theta, w, l), BL(x, y, theta, w, l)]

def back_corners(x, y, theta, w, l):
    return [TL(x, y, theta, w, l), TR(x, y, theta, w, l), ]

class Object:

    def __init__(self, name, width, length, region = None, index = None, position = (0, 0, 0)):
        """ Initialization of an object in a scene. 
            Inputs: 
            name: str, name of the object all lowercase
            width: float, width of the object
            length: float, length of the object
            index : int, index of the object in the room's object list (optional, only used for moving_objects)
            position: tuple (x, y, theta), where x, y are the coordinates of the center of the 
                      object and theta is the orientation of the object in radians.
        """

        self.position = position
        self.name = name
        self.width = width 
        self.length = length
        self.index = index
        if region: 
            self.region = region
        else: 
            self.region = None

    def TR(self):
        x, y, theta = self.position
        return TR(x, y, theta, self.width, self.length)

    def TL(self):  
        x, y, theta = self.position
        return TL(x, y, theta, self.width, self.length)

    def BR(self):
        x, y, theta = self.position
        return BR(x, y, theta, self.width, self.length)

    def BL(self):
        x, y, theta = self.position
        return BL(x, y, theta, self.width, self.length)
    
    def corners(self):


        if self.name != 'door' and self.name != 'window':
            return [self.TL(), self.TR(), self.BR(), self.BL()]
        elif self.name == 'door': 
            if self.position[2] == 0: 
                BL = [self.position[0] - self.width, self.position[1] - 0.2]
                BR = [self.position[0] + self.width + 0.2, self.position[1] - 0.2]
                TR = [self.position[0] + self.width + 0.2, self.position[1] + self.width + 0.2]
                TL = [self.position[0] - self.width, self.position[1] + self.width + 0.2]    
            elif self.position[2] == np.pi/2:
                BL = [self.position[0] + 0.2, self.position[1] - self.width]
                BR = [self.position[0] + 0.2, self.position[1] + self.width + 0.2]
                TR = [self.position[0] - self.width - 0.2, self.position[1] + self.width + 0.2]
                TL = [self.position[0] - self.width - 0.2, self.position[1] - self.width]
            elif self.position[2] == np.pi:
                BL = [self.position[0] + self.width + 0.2, self.position[1]]
                BR = [self.position[0] - self.width - 0.2, self.position[1]]
                TR = [self.position[0] - self.width - 0.2, self.position[1] - self.width - 0.2]
                TL = [self.position[0] + self.width + 0.2, self.position[1] - self.width - 0.2]
            elif self.position[2] == 3*np.pi/2:
                BL = [self.position[0] - 0.2, self.position[1] + self.width ]
                BR = [self.position[0] - 0.2, self.position[1] - self.width - 0.2]
                TR = [self.position[0] + self.width + 0.2, self.position[1] - self.width - 0.2]
                TL = [self.position[0] + self.width + 0.2, self.position[1] + self.width]

            return [TL, TR, BR, BL]
        else: 
            return corners(self.position[0], self.position[1], self.position[2], self.width + 0.1, 1)

    
    def back_corners(self):
        return [self.TL(), self.TR()]
class Region: 
    def __init__(self, name, x, y, index):

        """ Initialization of a region in a scene. 
            Inputs: 
            name: str, name of the object all lowercase
            x: float, x-coordinate of the center of the region
            y: float, y-coordinate of the center of the region
        """

        self.name = name
        self.x = x
        self.y = y
        self.index = index
class Room: 

    def __init__(self, width, length, fixed_objects = []):

        self.width = width
        self.length = length
        self.fixed_objects = fixed_objects
        self.moving_objects = []
        self.fm_indices = []
        self.center = (width/2, length/2)
        self.regions = []

    def find_region_index(self, region_name):

        """ Finds a region in the room by name.
            Inputs:
            region_name: str, name of the region
            Outputs:
            region: Region, the region object
        """

        for region in self.regions:
            if region_name in region.name or region.name in region_name:
                return region.index

        print("No region with this name is in the room.")    
        return None
    
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
    
    def draw(self, draw_regions = False, buffers = False):

        """ Draws the room with all the objects in it."""
        fig, ax = plt.subplots(figsize = (10, 10))
        ax.set_xlim(-1, self.width + 1)
        ax.set_ylim(-1, self.length + 1)
        ax.set_aspect('equal')
        ax.grid(linestyle = '--')

        # Draw the room
        rect = patches.Rectangle((0, 0), self.width, self.length, linewidth=2, edgecolor='black', facecolor='none', label='_nolegend_')
        ax.add_patch(rect)
        
        if draw_regions:
            eps = sys.float_info.epsilon

            def in_box(towers, bounding_box):
                return np.logical_and(np.logical_and(bounding_box[0] <= towers[:, 0],
                                         towers[:, 0] <= bounding_box[1]),
                          np.logical_and(bounding_box[2] <= towers[:, 1],
                                         towers[:, 1] <= bounding_box[3]))
            def voronoi(towers, bounding_box):
                # Select towers inside the bounding box
                i = in_box(towers, bounding_box)
                # Mirror points
                points_center = towers[i, :]
                points_left = np.copy(points_center)
                points_left[:, 0] = bounding_box[0] - (points_left[:, 0] - bounding_box[0])
                points_right = np.copy(points_center)
                points_right[:, 0] = bounding_box[1] + (bounding_box[1] - points_right[:, 0])
                points_down = np.copy(points_center)
                points_down[:, 1] = bounding_box[2] - (points_down[:, 1] - bounding_box[2])
                points_up = np.copy(points_center)
                points_up[:, 1] = bounding_box[3] + (bounding_box[3] - points_up[:, 1])
                points = np.append(points_center,
                                np.append(np.append(points_left,
                                                    points_right,
                                                    axis=0),
                                            np.append(points_down,
                                                    points_up,
                                                    axis=0),
                                            axis=0),
                                axis=0)
                # Compute Voronoi
                vor = sp.spatial.Voronoi(points)
                # Filter regions
                regions = []
                for region in vor.regions:
                    flag = True
                    for index in region:
                        if index == -1:
                            flag = False
                            break
                        else:
                            x = vor.vertices[index, 0]
                            y = vor.vertices[index, 1]
                            if not(bounding_box[0] - eps <= x and x <= bounding_box[1] + eps and
                                bounding_box[2] - eps <= y and y <= bounding_box[3] + eps):
                                flag = False
                                break
                    if region != [] and flag:
                        regions.append(region)
                vor.filtered_points = points_center
                vor.filtered_regions = regions
                return vor
            
            # Collect points for Voronoi diagram
            points = np.array([[region.x, region.y] for region in self.regions])
            colors = plt.cm.viridis(np.linspace(0, 1, len(points)))

            # Plot the points
            for i, point in enumerate(points):
                ax.plot(point[0], point[1], 'o', markersize=10, color=colors[i], label= self.regions[i].name)
                #ax.text(point[0], point[1], self.regions[i].name, fontsize=10)

            # Extracting handles and labels
            handles, labels = ax.get_legend_handles_labels()

            # Creating the legend
            ax.legend(handles, labels, title="Regions")

            # Plot Voronoi diagram
            vor = voronoi(points, np.array([0, self.width, 0, self.length]))
            for point_index, region_index in enumerate(vor.point_region):
                if point_index >= len(self.regions):
                    break
                region = vor.regions[region_index]
                if len(region) > 0:
                    polygon = [vor.vertices[i] for i in region]
                    for vert in polygon:
                        if vert[0] < 0:
                            vert[0] = 0
                        if vert[0] > self.width:
                            vert[0] = self.width
                        if vert[1] < 0:
                            vert[1] = 0
                        if vert[1] > self.length:
                            vert[1] = self.length
                    ax.fill(*zip(*polygon), color=colors[point_index], alpha=0.2)
        
        if buffers: 
            for obj in self.fixed_objects: 
                if obj.name == 'door' or obj.name == 'window': 
                    cs = np.array(obj.corners()).reshape(4, 2)
                    bottom_left = [np.min(cs[:, 0]), np.min(cs[:, 1])]
                    top_right = [np.max(cs[:, 0]), np.max(cs[:, 1])]
                    w, l = top_right[0] - bottom_left[0], top_right[1] - bottom_left[1]
                    rect = patches.Rectangle(bottom_left, w, l, linewidth=2, edgecolor='#2fb8c4', facecolor='#2fb8c4', alpha = 0.3)
                    ax.add_patch(rect)

        # Draw the objects
        if self.moving_objects:
            for obj in self.moving_objects:
                rectangle = patches.Rectangle(obj.position[:2]  - np.array([obj.width/2, obj.length/2]), obj.width, obj.length, linewidth=2, edgecolor='none', facecolor='none', angle=np.rad2deg(obj.position[2]), rotation_point='center')
                ax.add_patch(rectangle)
                line, = plt.plot([], [], label=obj.name)  # Create an invisible line
                rectangle.set_edgecolor(line.get_color())  # Use the line's color for the rectangle
                ax.text(obj.position[0], obj.position[1], obj.name, fontsize=10)
                cs = obj.back_corners()
                for corner in cs:
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

                elif obj.name == 'socket' or obj.name == 'plug' or obj.name == 'electrical plug':
                    x, y = obj.position[:2]
                    ax.plot([x - 0.05, x + 0.05], [y - 0.05, y + 0.05], color='red', linewidth=2)
                    ax.plot([x - 0.05, x + 0.05], [y + 0.05, y - 0.05], color='red', linewidth=2)
        
        plt.show()
        return 
    
    def medial_axis(self):
        final_points = []

        # Draw the room
        rect = patches.Rectangle((0, 0), self.width, self.length, linewidth=2, edgecolor='black', facecolor='none', label='_nolegend_')
        points = []
        cs = rect.get_corners()
        num_points = 100
        for i in range(num_points):
            points.append(cs[0] + (cs[1] - cs[0]) * i / num_points)  # Bottom side
            points.append(cs[1] + (cs[2] - cs[1]) * i / num_points)  # Right side
            points.append(cs[2] + (cs[3] - cs[2]) * i / num_points)  # Top side
            points.append(cs[3] + (cs[0] - cs[3]) * i / num_points)  # Left side
        final_points.append(points)

        rug_names = ['rug', 'mat', 'Rug', 'Mat', 'RUG', 'MAT', 'carpet', 'Carpet']
        # Draw the objects
        if self.moving_objects:
            for obj in self.moving_objects:
                rug = False
                for name in rug_names: 
                    if name in obj.name:
                        rug = True
                        break
                if rug: 
                    continue 
                cs_tup = obj.corners()
                cs = [np.array(i) for i in cs_tup]
                points = []
                num_points = 25
                for i in range(num_points):
                    points.append(cs[0] + (cs[1] - cs[0]) * i / num_points)  # Bottom side
                    points.append(cs[1] + (cs[2] - cs[1]) * i / num_points)  # Right side
                    points.append(cs[2] + (cs[3] - cs[2]) * i / num_points)  # Top side
                    points.append(cs[3] + (cs[0] - cs[3]) * i / num_points)  # Left side
                
                points = np.array(points)
                final_points.append(points)

        if self.fixed_objects:
            for obj in self.fixed_objects:
                if obj.name == 'door':
                    wedge = patches.Wedge(center=obj.position[:2], r=obj.width, 
                                            theta1=np.rad2deg(obj.position[2]), theta2=np.rad2deg(obj.position[2]) + 90, linewidth=3, edgecolor='r', facecolor='none')
                    
                    points = wedge.get_path().vertices
                    if obj.position[2] == 0:
                        points = [i for i in points if np.isclose(i[1], 0)]
                        points = np.unique(points, axis = 0)
                        min_x, max_x = sorted([i[0] for i in points])
                        crit = lambda x: np.isclose(x[1], 0) and (min_x < x[0]) and (x[0] < max_x)
                    elif obj.position[2] == np.pi/2:
                        points = [i for i in points if np.isclose(i[0], self.width)]
                        points = np.unique(points, axis = 0)
                        min_y, max_y = sorted([i[1] for i in points])
                        crit = lambda x: np.isclose(x[0], self.width) and( min_y < x[1]) and (x[1] < max_y )   
                    elif obj.position[2] == np.pi:
                        points = [i for i in points if np.isclose(i[1], self.length)]
                        points = np.unique(points, axis = 0)
                        min_x, max_x = sorted([i[0] for i in points])
                        crit = lambda x: np.isclose(x[1], self.length) and (min_x < x[0]) and (x[0] < max_x)
                    elif obj.position[2] == 3*np.pi/2:
                        points = [i for i in points if np.isclose(i[0], 0)]
                        points = np.unique(points, axis = 0)
                        min_y, max_y = sorted([i[1] for i in points])
                        crit = lambda x: np.isclose(x[0], 0) and (min_y < x[1]) and (x[1] < max_y )  
                    final_points.append(points)

        final_points = np.concatenate(final_points)

        for point in final_points:
            if crit(point):
                final_points = np.delete(final_points, np.where(np.all(final_points == point, axis = 1)), axis = 0)

        vor = Voronoi(final_points)
        new_edges = []
        max_distances = []
        for edge in vor.ridge_vertices: 
            remove = False
            if edge[0] == -1 or edge[1] == -1:
                continue
            if vor.vertices[edge[0]][0] < 0 or vor.vertices[edge[1]][0] < 0 or vor.vertices[edge[0]][1] < 0 or vor.vertices[edge[1]][1] < 0:
                continue
            if vor.vertices[edge[0]][0] > self.width or vor.vertices[edge[0]][1] > self.length or vor.vertices[edge[1]][0] > self.width or vor.vertices[edge[1]][1] > self.length:
                continue
            for obj in self.moving_objects:
                rug = False
                for name in rug_names: 
                    if name in obj.name:
                        rug = True
                        break
                if rug:
                    continue
                poly = Polygon(obj.corners())
                if any([poly.contains(Point(vor.vertices[v])) for v in edge]):
                    remove = True
                    break
            if remove: 
                continue 

            regions = [i for i in range(len(vor.regions)) if edge[0] in vor.regions[i] and edge[1] in vor.regions[i]]
            region_vs = [[], []]
            for i in range(2): 
                region_vs[i] = [v for v in vor.regions[regions[i]] if v != edge[0] and v != edge[1]]

            dists = []
            for i in range(len(region_vs[0])): 
                for j in range(len(region_vs[1])):
                    dists.append(np.linalg.norm(vor.vertices[region_vs[0][i]] - vor.vertices[region_vs[1][j]]))
            if np.any(np.array(dists) < 1e-6): 
                continue 
            else: 
                max_distances.append(np.min(dists))
                new_edges.append(edge)    

        new_vor = Voronoi(final_points)
        new_vor.vertices = vor.vertices
        new_vor.regions = vor.regions
        new_vor.ridge_vertices = new_edges

        fig, ax = plt.subplots(figsize = (10, 10))
        voronoi_plot_2d(new_vor, ax=ax, show_points=True, show_vertices=False, line_colors='gray')

        return new_vor, max_distances