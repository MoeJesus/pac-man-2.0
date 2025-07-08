import pyxel
from entity import Entity
from constants import *


class Fruit(Entity):
    def __init__(self, node):
        Entity.__init__(self, node)
        self.name = Fruit
        self.lifespan = 300
        self.timer = 0
        self.destroy = False
        self.points = 100
        self.set_between_nodes(RIGHT)

    def update(self):
        self.timer += 1
        if self.timer >= self.lifespan:
            self.destroy = True