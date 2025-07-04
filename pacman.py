import pyxel
from vector import Vector2
from constants import *


class Pacman(object):
    def __init__(self, node):
        self.name = PACMAN
        self.directions = {STOP:Vector2(), UP:Vector2(0, -1), DOWN:Vector2(0, 1), LEFT:Vector2(-1, 0), RIGHT:Vector2(1,0)}
        self.direction = STOP
        self.speed = 1 * TILEWIDTH / 8
        self.node = node
        self.set_position()
        self.target = node
        self.player_image = [32, 48, 16, 16]  # u, v, w, h
        self.collide_radius = 5

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

    # Copies the node position to pacman's position
    def set_position(self):
        self.position = self.node.position.copy()

    # These two functions check to see if pacman can move and go a certain direction
    def valid_direction(self, direction):
        if direction is not STOP:
            if self.node.neighbors[direction] is not None:
                return True
        return False

    def get_new_target(self, direction):
        if self.valid_direction(direction):
            return self.node.neighbors[direction]
        return self.node

    # Checks to see if pacman overshoots a node
    def overshot_target(self):
        if self.target is not None:
            vec1 = self.target.position - self.node.position
            vec2 = self.position - self.node.position
            node_to_target = vec1.magnitude_squared()
            node_to_self = vec2.magnitude_squared()
            return node_to_self >= node_to_target
        return False

    # These two functions allow pacman to move opposite from his current movement if he can
    def reverse_direction(self):
        self.direction *= -1
        temp = self.node
        self.node = self.target
        self.target = temp

    def opposite_direction(self, direction):
        if direction is not STOP:
            if direction == self.direction * -1:
                return True
        return False

    # Checks to see if pacman collided with a pellet
    def eat_pellets(self, pellet_list):
        for pellet in pellet_list:
            d = self.position - pellet.position
            d_squared = d.magnitude_squared()
            r_squared = (pellet.collide_radius + self.collide_radius)**2
            if d_squared <= r_squared:
                return pellet
        return None

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

    def draw(self):
        sprite_x = self.player_image[0]
        sprite_y = self.player_image[1]
        width = self.player_image[2]
        height = self.player_image[3]

        if self.direction == UP:
            sprite_x = pyxel.frame_count // 4 % 4 * 16
            sprite_y = 32
        if self.direction == DOWN:
            sprite_x = pyxel.frame_count // 4 % 4 * 16
            sprite_y = 32
            height = height * -1
        if self.direction == LEFT:
            sprite_x = pyxel.frame_count // 4 % 4 * 16
            sprite_y = 16
            width = width * -1
        if self.direction == RIGHT:
            sprite_x = pyxel.frame_count // 4 % 4 * 16
            sprite_y = 16
        if self.direction == STOP:
            sprite_x = 48
            sprite_y = 16
            
        pyxel.blt(self.position.x - (TILEWIDTH / 2), self.position.y - (TILEWIDTH / 2), 0, sprite_x, sprite_y, width, height, 0)