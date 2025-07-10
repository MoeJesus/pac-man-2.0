import pyxel
from vector import Vector2
from constants import *
from entity import Entity


class Pacman(Entity):
    def __init__(self, node):
        Entity.__init__(self, node)
        self.name = PACMAN
        self.entity_image = [0, 16]  # u, v
        self.direction = LEFT
        self.set_between_nodes(LEFT)
        self.alive = True

    # Checks to see if a key is inputted for movement
    def get_valid_key(self):
        if pyxel.btn(pyxel.KEY_UP):
            return UP
        if pyxel.btn(pyxel.KEY_DOWN):
            return DOWN
        if pyxel.btn(pyxel.KEY_LEFT):
            return LEFT
        if pyxel.btn(pyxel.KEY_RIGHT):
            return RIGHT
        return STOP

    # Checks to see if pacman collided with any object
    def collide_check(self, other):
        d = self.position - other.position
        d_squared = d.magnitude_squared()
        r_squared = (self.collide_radius + other.collide_radius)**2
        if d_squared <= r_squared:
            return True
        return False

    def eat_pellets(self, pellet_list):
        for pellet in pellet_list:
            if self.collide_check(pellet):
                return pellet
        return None

    def collide_ghost(self, ghost):
        return self.collide_check(ghost)

    # If pacman dies, these functions will run
    def die(self):
        self.alive = False
        self.direction = STOP

    def reset(self):
        Entity.reset(self)
        self.direction = LEFT
        self.set_between_nodes(LEFT)
        self.alive = True

    def update(self):
        self.position += self.directions[self.direction] * self.speed
        direction = self.get_valid_key()
        if self.overshot_target():
            self.node = self.target
            if self.node.neighbors[PORTAL] is not None:
                self.node = self.node.neighbors[PORTAL]
            self.target = self.get_new_target(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.get_new_target(self.direction)

            if self.target is self.node:
                self.direction = STOP
            self.set_position()
        else:
            if self.opposite_direction(direction):
                self.reverse_direction()