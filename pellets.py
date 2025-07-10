import pyxel
from vector import Vector2
from constants import *
import numpy as np


# Creates pellets
class Pellet(object):
    def __init__(self, row, column):
        self.name = PELLET
        self.position = Vector2(column*TILE_WIDTH, row*TILE_HEIGHT)
        self.sprite_x = 8
        self.sprite_y = 0
        self.collide_radius = 2
        self.points = 10
        self.visible = True

    def draw(self):
        if self.visible:
            p = self.position.as_int()
            pyxel.blt(self.position.x, self.position.y, 0, self.sprite_x, self.sprite_y, TILE_WIDTH, TILE_HEIGHT)


# Using the pellet class, power pellets are also created
class PowerPellet(Pellet):
    def __init__(self, row, column):
        Pellet.__init__(self, row, column)
        self.name = POWER_PELLET
        self.sprite_y = 8
        self.points = 50

    def update(self):
        if pyxel.frame_count % 16 < 8:
            self.visible = False
        if pyxel.frame_count % 16 >= 8:
            self.visible = True


# Places pellets on the tilemap
class PelletGroup(object):
    def __init__(self, pellet_file):
        self.pellet_list = []
        self.power_pellets = []
        self.create_pellet_list(pellet_file)
        self.num_eaten = 0

    # Reads the maze file
    def read_pellet_file(self, text_file):
        return np.loadtxt(text_file, dtype='<U1')

    # Places all of the pellets onto the tilemap
    def create_pellet_list(self, pellet_file):
        data = self.read_pellet_file(pellet_file)
        for row in range(data.shape[0]):
            for col in range(data.shape[1]):
                if data[row][col] in ['.', '+']:
                    self.pellet_list.append(Pellet(row, col))
                elif data[row][col] in ['P', 'p']:
                    pp = PowerPellet(row, col)
                    self.pellet_list.append(pp)
                    self.power_pellets.append(pp)

    # Checks to see if all pellets are eaten
    def is_empty(self):
        if len(self.pellet_list) == 0:
            return True
        return False

    def update(self):
        for power_pellet in self.power_pellets:
            power_pellet.update()

    def draw(self):
        for pellet in self.pellet_list:
            pellet.draw()