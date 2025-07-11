import pyxel
from vector import Vector2
from constants import *

class Text(object):
    def __init__(self, text, x, y):
        self.text  = text
        self.position = Vector2(x, y)

    def setup_text(self):
        pass

    def draw(self):
        for _ in text:
            pyxel.blt(x + (i * 8), y, 0, text[i][0], text[i][1], text[i][2], text[i][3])