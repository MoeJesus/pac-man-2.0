import pyxel
from vector import Vector2
from constants import *
import numpy as np


# Creates a node
class Node(object):
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.neighbors = {UP:None, DOWN:None, LEFT:None, RIGHT:None, PORTAL:None}
        self.access = {UP:[PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT], DOWN:[PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT], LEFT:[PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT], RIGHT:[PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT]}

    # Gives or takes away access to nodes
    def deny_access(self, direction, entity):
        if entity.name in self.access[direction]:
            self.access[direction].remove(entity.name)

    def allow_access(self, direction, entity):
        if entity.name not in self.access[direction]:
            self.access[direction].append(entity.name)

    def draw(self):
        for n in self.neighbors.keys():
            if self.neighbors[n] is not None:
                line_start = self.position.as_tuple()
                line_end = self.neighbors[n].position.as_tuple()
                pyxel.line(line_start[0], line_start[1], line_end[0], line_end[1], 7)
                pyxel.circ(self.position.x, self.position.y, 4, 8)


# Arranges the nodes so that they connect to each other on the tilemap
class NodeGroup(object):
    def __init__(self, level):
        self.level = level
        self.nodes_LUT = {}
        self.node_symbols = ['+', 'P', 'n']
        self.path_symbols = ['.', '-', '|', 'p']
        data = self.read_maze_file(level)
        self.create_node_table(data)
        self.connect_horizontally(data)
        self.connect_vertically(data)
        self.home_key = None

    # Reads the maze file
    def read_maze_file(self, text_file):
        return np.loadtxt(text_file, dtype='<U1')

    # Converts rows and columns to pixel values
    def construct_key(self, x, y):
        return x * TILE_WIDTH, y * TILE_HEIGHT

    # Creates the node table so that they are arranged on the tilemap
    def create_node_table(self, data, xoffset=0, yoffset=0):
        for row in list(range(data.shape[0])):
            for col in list(range(data.shape[1])):
                if data[row][col] in self.node_symbols:
                    x, y = self.construct_key(col+xoffset, row+yoffset)
                    self.nodes_LUT[(x, y)] = Node(x, y)

    # Connects neighbor nodes that share the same x value together
    def connect_horizontally(self, data, xoffset=0, yoffset=0):
        for row in list(range(data.shape[0])):
            key = None
            for col in list(range(data.shape[1])):
                if data[row][col] in self.node_symbols:
                    if key is None:
                        key = self.construct_key(col+xoffset, row+yoffset)
                    else:
                        other_key = self.construct_key(col+xoffset, row+yoffset)
                        self.nodes_LUT[key].neighbors[RIGHT] = self.nodes_LUT[other_key]
                        self.nodes_LUT[other_key].neighbors[LEFT] = self.nodes_LUT[key]
                        key = other_key
                elif data[row][col] not in self.path_symbols:
                    key = None

    # Connects neighbor nodes that share the same y value together
    def connect_vertically(self, data, xoffset=0, yoffset=0):
        data_trans = data.transpose()
        for col in list(range(data_trans.shape[0])):
            key = None
            for row in list(range(data_trans.shape[1])):
                if data_trans[col][row] in self.node_symbols:
                    if key is None:
                        key = self.construct_key(col+xoffset, row+yoffset)
                    else:
                        other_key = self.construct_key(col+xoffset, row+yoffset)
                        self.nodes_LUT[key].neighbors[DOWN] = self.nodes_LUT[other_key]
                        self.nodes_LUT[other_key].neighbors[UP] = self.nodes_LUT[key]
                        key = other_key
                elif data_trans[col][row] not in self.path_symbols:
                    key = None

    # Two useful functions to search for node locations based on pixels or tiles
    def get_node_from_pixels(self, xpixel, ypixel):
        if (xpixel, ypixel) in self.nodes_LUT.keys():
            return self.nodes_LUT[(xpixel, ypixel)]
        return None

    def get_node_from_tiles(self, col, row):
        x, y = self.construct_key(col, row)
        if (x, y) in self.nodes_LUT.keys():
            return self.nodes_LUT[(x, y)]
        return None

    # Allows pacman to move between two sides of the map when allowed to
    def set_portal_pair(self, pair1, pair2):
        key1 = self.construct_key(*pair1)
        key2 = self.construct_key(*pair2)
        if key1 in self.nodes_LUT.keys() and key2 in self.nodes_LUT.keys():
            self.nodes_LUT[key1].neighbors[PORTAL] = self.nodes_LUT[key2]
            self.nodes_LUT[key2].neighbors[PORTAL] = self.nodes_LUT[key1]

    # Sets the node for pacman's starting point
    def get_starting_temp_node(self):
        nodes = list(self.nodes_LUT.values())
        return nodes[0]

    # These two functions create home nodes for the ghosts and connects them to the rest of the nodes
    def create_home_nodes(self, xoffset, yoffset):
        home_data = np.array([['X','X','+','X','X'], ['X','X','.','X','X'], ['+','X','.','X','+'], ['+','.','+','.','+'], ['+','X','X','X','+']])
        self.create_node_table(home_data, xoffset, yoffset)
        self.connect_horizontally(home_data, xoffset, yoffset)
        self.connect_vertically(home_data, xoffset, yoffset)
        self.home_key = self.construct_key(xoffset+2, yoffset)
        return self.home_key

    def connect_home_nodes(self, home_key, other_key, direction):
        key = self.construct_key(*other_key)
        self.nodes_LUT[home_key].neighbors[direction] = self.nodes_LUT[key]
        self.nodes_LUT[key].neighbors[direction*-1] = self.nodes_LUT[home_key]

    # These 8 functions assess if an entity is allowed to enter a node
    def deny_access_list(self, col, row, direction, entities):
        for entity in entities:
            self.deny_access(col, row, direction, entity)

    def allow_access_list(self, col, row, direction, entities):
        for entity in entities:
            self.allow_access(col, row, direction, entity)

    def deny_access(self, col, row, direction, entity):
        node = self.get_node_from_tiles(col, row)
        if node is not None:
            node.deny_access(direction, entity)

    def allow_access(self, col, row, direction, entity):
        node = self.get_node_from_tiles(col, row)
        if node is not None:
            node.allow_access(direction, entity)

    def deny_home_access_list(self, entities):
        for entity in entities:
            self.deny_home_access(entity)

    def allow_home_access_list(self, entities):
        for entity in entities:
            self.allow_home_access(entity)

    def deny_home_access(self, entity):
        self.nodes_LUT[self.home_key].deny_access(DOWN, entity)

    def allow_home_access(self, entity):
        self.nodes_LUT[self.home_key].allow_access(DOWN, entity)

    def draw(self):
        for node in self.nodes_LUT.values():
            node.draw()