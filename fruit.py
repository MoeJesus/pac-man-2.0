import pyxel
from entity import Entity
from constants import *


class Fruit(Entity):
    def __init__(self, node):
        Entity.__init__(self, node)
        self.name = FRUIT
        self.lifespan = 300
        self.timer = 0
        self.destroy = False
        self.points = 100
        self.entity_image = [0, 112]
        self.set_between_nodes(RIGHT)

    def check_points(self, points):
        if points == 100:
            FRUIT_POINTS.clear()
            FRUIT_POINTS.append(CHARACTERS[P100])
        elif points == 300:
            FRUIT_POINTS.clear()
            FRUIT_POINTS.append(CHARACTERS[P300])
        elif points == 700:
            FRUIT_POINTS.clear()
            FRUIT_POINTS.append(CHARACTERS[P700])
        elif points == 1000:
            FRUIT_POINTS.clear()
            FRUIT_POINTS.append(CHARACTERS[P1000])
        elif points == 2000:
            FRUIT_POINTS.clear()
            FRUIT_POINTS.append(CHARACTERS[P2000])
        else:
            FRUIT_POINTS.clear()
            FRUIT_POINTS.append(CHARACTERS[P3000])
        return FRUIT_POINTS

    def update(self):
        self.timer += 1
        if self.timer >= self.lifespan:
            self.destroy = True