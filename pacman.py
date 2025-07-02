import pyxel
from vector import Vector2
from constants import *

class Pacman(object):
    def __init__(self):
        self.name = Pacman
        self.position = Vector2(100, 200)
        self.directions = {STOP:Vector2(), UP:Vector2(0, -1), DOWN:Vector2(0, 1), LEFT:Vector2(-1, 0), RIGHT:Vector2(1,0)}
        self.direction = STOP
        self.speed = 1 * TILEWIDTH / 16
        self.player_image = [32, 48, 16, 16]  # u, v, w, h

    def update(self, dt):
        self.position += self.directions[self.direction] * self.speed * dt
        direction = self.get_valid_key()
        self.direction = direction

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
            
        pyxel.blt(self.position.x, self.position.y, 0, sprite_x, sprite_y, width, height)