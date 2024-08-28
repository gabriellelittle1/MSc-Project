import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy.spatial import Voronoi, voronoi_plot_2d
import scipy as sp
import sys
import copy
from shapely.geometry import Polygon, Point
from Individual import get_position

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

def medial_axis(room, draw = False):

        final_points = []

        # Draw the room
        rect = patches.Rectangle((0, 0), room.width, room.length, linewidth=2, edgecolor='black', facecolor='none', label='_nolegend_')

        points = []
        cs = rect.get_corners()
        num_points = int(np.ceil(2 * (5 * room.width + 5 * room.length)))
        for i in range(num_points):
            points.append(cs[0] + (cs[1] - cs[0]) * i / num_points)  # Bottom side
            points.append(cs[1] + (cs[2] - cs[1]) * i / num_points)  # Right side
            points.append(cs[2] + (cs[3] - cs[2]) * i / num_points)  # Top side
            points.append(cs[3] + (cs[0] - cs[3]) * i / num_points)  # Left side
        final_points.append(points)

        rug_names = ['rug', 'mat', 'Rug', 'Mat', 'RUG', 'MAT', 'carpet', 'Carpet']
        if room.moving_objects:
            for obj in room.moving_objects:
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
                num_points = int(np.ceil(2 * (5 * obj.width + 5 * obj.length)))
                for i in range(num_points):
                    points.append(cs[0] + (cs[1] - cs[0]) * i / num_points)
                    points.append(cs[1] + (cs[2] - cs[1]) * i / num_points)
                    points.append(cs[2] + (cs[3] - cs[2]) * i / num_points)
                    points.append(cs[3] + (cs[0] - cs[3]) * i / num_points)
                
                points = np.array(points)
                final_points.append(points)

        if room.fixed_objects:
            for obj in room.fixed_objects:
                if obj.name == 'door':

                    wedge = patches.Wedge(center=obj.position[:2], r=obj.width, 
                                            theta1=np.rad2deg(obj.position[2]), theta2=np.rad2deg(obj.position[2]) + 90, linewidth=3, edgecolor='r', facecolor='none')
                    
                    points = wedge.get_path().vertices
                    if obj.position[2] == 0:
                        points = [i for i in points if np.isclose(i[1], 0)]
                        points = np.unique(points, axis = 0)
                        min_x, max_x = sorted([i[0] for i in points])
                        crit = lambda x: np.isclose(x[1], 0) and (min_x < x[0]) and (x[0] < max_x)
                        crit2 = lambda x: np.isclose(x[1], 0)
                    elif obj.position[2] == np.pi/2:
                        points = [i for i in points if np.isclose(i[0], room.width)]
                        points = np.unique(points, axis = 0)
                        min_y, max_y = sorted([i[1] for i in points])
                        crit = lambda x: np.isclose(x[0], room.width) and( min_y < x[1]) and (x[1] < max_y ) 
                        crit2 = lambda x: np.isclose(x[0], room.width) 
                    elif obj.position[2] == np.pi:
                        points = [i for i in points if np.isclose(i[1], room.length)]
                        points = np.unique(points, axis = 0)
                        min_x, max_x = sorted([i[0] for i in points])
                        crit = lambda x: np.isclose(x[1], room.length) and (min_x < x[0]) and (x[0] < max_x)
                        crit2 = lambda x: np.isclose(x[1], room.length)
                    elif obj.position[2] == 3*np.pi/2:
                        points = [i for i in points if np.isclose(i[0], 0)]
                        points = np.unique(points, axis = 0)
                        min_y, max_y = sorted([i[1] for i in points])
                        crit = lambda x: np.isclose(x[0], 0) and (min_y < x[1]) and (x[1] < max_y ) 
                        crit2 = lambda x: np.isclose(x[0], 0)
                    final_points.append(points)

        final_points = np.concatenate(final_points)

        door_points = []
        for point in final_points:
            if crit(point):
                door_points += [point]
                final_points = np.delete(final_points, np.where(np.all(final_points == point, axis = 1)), axis = 0)
        vor = Voronoi(final_points)

        new_edges = []
        new_ridge_points = []

        ## find the door ridge 
        ridge_points = vor.ridge_points
        for i in range(len(ridge_points)): 
            edge = ridge_points[i]
            p1, p2 = vor.points[edge]
            if crit2(p1) and crit2(p2) and np.linalg.norm(p1 - p2) > 0.4:
                new_edges.append(vor.ridge_vertices[i])
                new_ridge_points.append(vor.ridge_points[i])

        for i in range(len(vor.ridge_vertices)): 
            edge = vor.ridge_vertices[i]
            remove = False
            p1 = vor.vertices[edge[0]]
            p2 = vor.vertices[edge[1]]
            if (edge[0] == -1 or edge[1] == -1):
                continue
            if p1[0] < 0 or p2[0] < 0 or p1[1] < 0 or p2[1] < 0:
                continue
            if p1[0] > room.width or p1[1] > room.length or p2[0] > room.width or p2[1] > room.length:
                continue
            for obj in room.moving_objects:
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
            

            regions = [j for j in range(len(vor.regions)) if edge[0] in vor.regions[j] and edge[1] in vor.regions[j]]
            region_vs = [[], []]
            for j in range(2): 
                region_vs[j] = [v for v in vor.regions[regions[j]] if v != edge[0] and v != edge[1]]

            dists = []
            for j in range(len(region_vs[0])): 
                for k in range(len(region_vs[1])):
                    dists.append(np.linalg.norm(vor.vertices[region_vs[0][j]] - vor.vertices[region_vs[1][k]]))
            if np.any(np.array(dists) < 1e-8): 
                continue 
            else: 
                new_edges.append(edge)  
                new_ridge_points.append(vor.ridge_points[i])  
        

        

        new_vor = Voronoi(final_points)
        new_vor.vertices = vor.vertices
        new_vor.regions = vor.regions
        new_vor.ridge_vertices = new_edges
        new_vor.ridge_points = new_ridge_points

        if draw:
            fig, ax = plt.subplots(figsize = (10, 10))
            voronoi_plot_2d(new_vor, ax=ax, show_points=True, show_vertices=False, line_colors='gray')

        return new_vor


def find_corner_points(points): 
    """ A function to find the points that are inner corners (with three different directions of edges) in a set of points. 
        Inputs: 
        points: np.array, a set of points
        Outputs: 
        c_inds: list, indices of the corner points
    """

    c_inds =[]
    neighbour_inds = []
    for i in range(points.shape[0]): 
        dists = np.linalg.norm(points - points[i], axis = 1)
        inds = [j for j in np.where(dists < 0.15)[0] if j != i]
        neighbours = points[inds]
        ds = []
        for n in neighbours:
            direction = n - points[i]
            if np.isnan(direction[0]/np.linalg.norm(direction)) or np.isnan(direction[1]/np.linalg.norm(direction)):
                continue
            ds += [direction / np.linalg.norm(direction)]
        for j in range(len(ds) - 1): 
            angles = np.arccos(np.clip(np.dot(ds[j+1:], ds[j]), -1, 1))
            if (np.any(np.isclose(angles, np.pi/2)) or np.any(np.isclose(angles, -np.pi/2))):
                neighbour_inds += [inds]
                c_inds.append(i)
                break
    
    copy_inds = c_inds.copy()
    for ind in range(len(copy_inds)): 
        num = 0
        new_ind = copy_inds[ind]
        neighbours = points[neighbour_inds[ind]]
        diff = (neighbours - points[new_ind])/np.linalg.norm(points[new_ind] - neighbours, axis = 1)[:, None]
        for i in range(diff.shape[0]): 
            new_diff = np.dot(np.concatenate([diff[:i], diff[i + 1:]]), diff[i])
            if not np.any(new_diff < -0.9):
                num += 1
        if num == len(neighbours): 
            c_inds.remove(new_ind)
    
    corner1 = np.argmin(points[:, 0] + points[:, 1])
    corner2 = np.argmax(points[:, 0] + points[:, 1])
    corner3 = np.argmax(points[:, 0] - points[:, 1])
    corner4 = np.argmin(points[:, 0] - points[:, 1])
    if corner1 not in c_inds: 
        c_inds.append(corner1)
    if corner2 not in c_inds:
        c_inds.append(corner2)
    if corner3 not in c_inds:
        c_inds.append(corner3)
    if corner4 not in c_inds:
        c_inds.append(corner4)

    return c_inds

def path_points(room): 

    vor = medial_axis(room)
    vor_points = vor.points
    all_points = []
    weights = []

    c_inds = find_corner_points(vor_points)
    corner_points = vor_points[c_inds]

    fig, axes = plt.subplots()
    for i in range(len(vor.ridge_vertices)): 
        mid_points = []
        edge = vor.ridge_vertices[i]
        if np.linalg.norm(vor.vertices[edge[0]] - vor.vertices[edge[1]]) > 0.1: 
            points = np.linspace(vor.vertices[edge[0]], vor.vertices[edge[1]], 25)
            verts = [i.tolist() for i in vor.vertices]
            vor.vertices = np.array(verts + points.tolist())
            mid_points = points

        min_index = np.argmin([vor.vertices[edge[0]][0], vor.vertices[edge[1]][0]])
        other_index = 1 - min_index
        direction = vor.vertices[edge[other_index]] - vor.vertices[edge[min_index]]
        direction = direction / np.linalg.norm(direction)
        perpendicular_direction = np.array([direction[1], -direction[0]])
        perpendicular_direction = perpendicular_direction / np.linalg.norm(perpendicular_direction)

        ws = np.array([1, 2, 3, 5, 3, 2, 1])
        if len(mid_points) > 0: 
            for point in mid_points: 
                mid_point = point
                dists = np.linalg.norm(corner_points - mid_point, axis = 1)
                if np.any(dists < 0.25): 
                    continue
                x = np.linspace(mid_point[0] - 0.3 * perpendicular_direction[0], mid_point[0] + 0.3 * perpendicular_direction[0], 7)
                y = np.linspace(mid_point[1] - 0.3 * perpendicular_direction[1], mid_point[1] + 0.3 * perpendicular_direction[1], 7)
                for i in range(7): 
                    all_points.append([x[i], y[i]])
                axes.scatter(x, y)
        else: 
            
            mid_point = (vor.vertices[edge[0]] + vor.vertices[edge[1]]) / 2
            dists = np.linalg.norm(corner_points - mid_point, axis = 1)
            if np.any(dists < 0.25): 
                continue

            val = False
            for point in vor.points: 
                if np.linalg.norm(point - mid_point) < 0: 
                    val = True
                    break
            if val: 
                continue

            x = np.linspace(mid_point[0] - 0.3 * perpendicular_direction[0], mid_point[0] + 0.3 * perpendicular_direction[0], 7)
            y = np.linspace(mid_point[1] - 0.3 * perpendicular_direction[1], mid_point[1] + 0.3 * perpendicular_direction[1], 7)
            for xi, yi in zip(x, y):
                all_points.append([xi, yi])
        
            
    all_points = np.array(all_points)
    weights = ws.tolist() * (all_points.shape[0]//7)
    axes.scatter(all_points[:, 0], all_points[:, 1], c = weights)
    voronoi_plot_2d(vor, ax = axes, show_points=True, show_vertices=False, line_colors='gray')

    return all_points, weights

def cost(positions, room, points, weights): 

    intersection = 0
    rug_names = ['rug', 'mat', 'Rug', 'Mat', 'RUG', 'MAT', 'carpet', 'Carpet']
    for i in range(len(room.moving_objects)): 
        rug = False
        for name in rug_names: 
            if name in room.moving_objects[i].name:
                rug = True
                break
        if rug: 
            continue 
        x, y, theta = get_position(positions, room, i)
        cs = corners(x, y, theta, room.moving_objects[i].width, room.moving_objects[i].length)
        poly = Polygon(cs)
        for j in range(points.shape[0]): 
            if poly.contains(Point(points[j, :])): 
                intersection += weights[j]*poly.exterior.distance(Point(points[j, :]))**2

    return intersection

class Object:

    def __init__(self, name, width, length, region = None, index = None, position = (0, 0, 0), tertiary = False):
        """ Initialization of an object in a scene. 
            Inputs: 
            name: str, name of the object all lowercase
            width: float, width of the object
            length: float, length of the object
            index : int, index of the object in the room's object list (optional, only used for moving_objects)
            position: tuple (x, y, theta), where x, y are the coordinates of the center of the 
                      object and theta is the orientation of the object in radians.
            tertiary: string, one of "wall" or "floor" (optional, only used for tertiary_objects) which determines the type of teriary object
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
        
        if tertiary: 
            self.tertiary = tertiary 

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
                BL = [self.position[0] - 0.2, self.position[1] - 0.2]
                BR = [self.position[0] + self.width + 0.2, self.position[1] - 0.2]
                TR = [self.position[0] + self.width + 0.2, self.position[1] + self.width + 0.2]
                TL = [self.position[0] - 0.2, self.position[1] + self.width + 0.2]    
            elif self.position[2] == np.pi/2:
                BL = [self.position[0] + 0.2, self.position[1] - 0.2]
                BR = [self.position[0] + 0.2, self.position[1] + self.width + 0.2]
                TR = [self.position[0] - self.width - 0.2, self.position[1] + self.width + 0.2]
                TL = [self.position[0] - self.width - 0.2, self.position[1] - 0.2]
            elif self.position[2] == np.pi:
                BL = [self.position[0] + 0.2, self.position[1]]
                BR = [self.position[0] - self.width - 0.2, self.position[1]]
                TR = [self.position[0] - self.width - 0.2, self.position[1] - self.width - 0.2]
                TL = [self.position[0] + 0.2, self.position[1] - self.width - 0.2]
            elif self.position[2] == 3*np.pi/2:
                BL = [self.position[0] - 0.2, self.position[1] + 0.2]
                BR = [self.position[0] - 0.2, self.position[1] - self.width - 0.2]
                TR = [self.position[0] + self.width + 0.2, self.position[1] - self.width - 0.2]
                TL = [self.position[0] + self.width + 0.2, self.position[1] + 0.2]

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
        self.tertiary_objects = []

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
    
    def draw(self, draw_regions = False, buffers = False, ax = None):

        """ Draws the room with all the objects in it."""
        show = True
        if ax is None: 
            show = False
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

        # Draw the objects
        if self.tertiary_objects:
            for obj in self.tertiary_objects:
                rectangle = patches.Rectangle(obj.position[:2]  - np.array([obj.width/2, obj.length/2]), obj.width, obj.length, linewidth=2, edgecolor='none', facecolor='none', angle=np.rad2deg(obj.position[2]), rotation_point='center')
                ax.add_patch(rectangle)
                rectangle.set_edgecolor('b')  # Use the line's color for the rectangle
                ax.text(obj.position[0], obj.position[1], obj.name, fontsize=10)
                cs = obj.back_corners()
                for corner in cs:
                    ax.plot(corner[0], corner[1], color = 'b', marker = 'o')

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

        if show: 
            plt.show()
        
        return
    


    def path_points(self): 

        vor, _ = self.medial_axis()
        vor_points = vor.points
        all_points = []
        weights = []
        mps = []

        c_inds = find_corner_points(vor_points)
        corner_points = vor_points[c_inds]

        fig, axes = plt.subplots()
        for i in range(len(vor.ridge_vertices)): 
            mid_points = []
            edge = vor.ridge_vertices[i]
            if np.linalg.norm(vor.vertices[edge[0]] - vor.vertices[edge[1]]) > 0.1: 
                points = np.linspace(vor.vertices[edge[0]], vor.vertices[edge[1]], 25)
                verts = [i.tolist() for i in vor.vertices]
                vor.vertices = np.array(verts + points.tolist())
                mid_points = points

            min_index = np.argmin([vor.vertices[edge[0]][0], vor.vertices[edge[1]][0]])
            other_index = 1 - min_index
            direction = vor.vertices[edge[other_index]] - vor.vertices[edge[min_index]]
            direction = direction / np.linalg.norm(direction)
            perpendicular_direction = np.array([direction[1], -direction[0]])
            perpendicular_direction = perpendicular_direction / np.linalg.norm(perpendicular_direction)

            ws = np.array([1, 2, 3, 5, 3, 2, 1])
            if len(mid_points) > 0: 
                for point in mid_points: 
                    mps += [point]
                    mid_point = point
                    dists = np.linalg.norm(corner_points - mid_point, axis = 1)
                    if np.any(dists < 0.25): 
                        continue
                    x = np.linspace(mid_point[0] - 0.3 * perpendicular_direction[0], mid_point[0] + 0.3 * perpendicular_direction[0], 7)
                    y = np.linspace(mid_point[1] - 0.3 * perpendicular_direction[1], mid_point[1] + 0.3 * perpendicular_direction[1], 7)
                    for i in range(7): 
                        all_points.append([x[i], y[i]])
                    axes.scatter(x, y)
            else: 
                
                mid_point = (vor.vertices[edge[0]] + vor.vertices[edge[1]]) / 2
                dists = np.linalg.norm(corner_points - mid_point, axis = 1)
                if np.any(dists < 0.25): 
                    continue
                mps += [mid_point]
                val = False
                for point in vor.points: 
                    if np.linalg.norm(point - mid_point) < 0: 
                        val = True
                        break
                if val: 
                    continue

                x = np.linspace(mid_point[0] - 0.3 * perpendicular_direction[0], mid_point[0] + 0.3 * perpendicular_direction[0], 7)
                y = np.linspace(mid_point[1] - 0.3 * perpendicular_direction[1], mid_point[1] + 0.3 * perpendicular_direction[1], 7)
                for xi, yi in zip(x, y):
                    all_points.append([xi, yi])
            
                
        all_points = np.array(all_points)
        weights = ws.tolist() * (all_points.shape[0]//7)

        inds = []
        for i in range(mps.shape[0]):
            point = mps[i]
            dists = np.linalg.norm(corner_points - point, axis = 1)
            if np.all(dists > 0.1):
                inds += [i]
  
        axes.scatter(all_points[:, 0], all_points[:, 1], c = weights)
        voronoi_plot_2d(vor, ax = axes, show_points=True, show_vertices=False, line_colors='gray')

        return all_points, weights
