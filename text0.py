import pyxel
from vector import Vector2
from constants import *


class Text(object):
    def __init__(self, text, x, y, time=None, id=None, visible=True):
        self.id = id
        self.text = text
        self.visible = visible
        self.position = Vector2(x, y)
        self.timer = 0
        self.lifespan = time
        self.label = None
        self.destroy = False

    def update(self):
        if self.lifespan is not None:
            self.timer += 1
            if self.timer >= self.lifespan:
                self.timer = 0
                self.lifespan = None
                self.destroy = True

    def draw(self):
        if self.visible:
            pyxel.blt(self.position.x, self.position.y, 0, a, b, c, d, 0)


class TextGroup(object):
    def __init__(self):
        self.next_id = 10
        self.all_text = {}
        self.setup_text()
        self.show_text(READYTXT)

    def add_text(self, text, x, y, time=None, id=None):
        self.next_id += 1
        self.add_text[self.next_id] = Text(text, x, y, time=time, id=id)
        return self.next_id

    def setup_text(self):
        self.all_text[READYTXT] = Text(READY, 11.25*TILE_WIDTH, 20*TILE_HEIGHT, visible=False)
        self.add_text(SCORE, 0, 0)
        self.add_text(LEVEL, 23*TILE_WIDTH, 0)

    def remove_text(self, id):
        self.all_text.pop(id)

    def hide_text():
        self.all_text[READYTXT].visible = False

    def show_text(self, id):
        self.hide_text()
        self.all_text[id].visible = True

    def update(self):
        for tkey in list(self.all_text.keys()):
            self.all_text[tkey].update()
            if self.all_text[tkey].destroy:
                self.remove_text(tkey)

    def draw(self):
        for tkey in list(self.all_text.keys()):
            self.all_text[tkey].draw()