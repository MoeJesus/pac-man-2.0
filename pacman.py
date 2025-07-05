import pyxel
from vector import Vector2
from constants import *
from entity import Entity


class Pacman(Entity):
    def __init__(self, node):
        Entity.__init__(self, node)
        self.name = PACMAN
        self.player_image = [32, 48, 16, 16]  # u, v, w, h

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