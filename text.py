import pyxel
from vector import Vector2
from constants import *

class Text(object):
    def __init__(self, text, x, y, color=WHITE, flash=False, id=None, visible=True):
        self.text = text
        self.position = Vector2(x, y)
        self.color = color
        self.flash = flash
        self.id = id
        self.visible = visible
        self.destroy = False

    def update(self):
        if self.flash == True:
            if pyxel.frame_count % 32 < 16:
                self.visible = False
            if pyxel.frame_count % 32 >= 16:
                self.visible = True

    def draw(self):
        if self.visible:
            if self.color == YELLOW:
                pyxel.pal(7, 10)
            else:
                pyxel.pal()
                
            i = 0
            for _ in self.text:
                pyxel.blt(self.position.x + (i * 8), self.position.y, 0, self.text[i][0], self.text[i][1], self.text[i][2], self.text[i][3])
                i += 1


class TextGroup(object):
    def __init__(self):
        self.next_id = 10
        self.all_text = {}
        self.setup_text()
        self.show_text(READYTXT)

    def add_text(self, text, x, y, color=WHITE, flash=False, id=None):
        self.next_id += 1
        self.all_text[self.next_id] = Text(text, x, y, color=WHITE, flash=flash, id=id)
        return self.next_id

    def remove_text(self, id):
        self.all_text.pop(id)

    def setup_text(self):
        self.all_text[READYTXT] = Text(READY, 11*TILE_WIDTH, 20*TILE_HEIGHT, YELLOW, visible=False)
        self.all_text[PAUSETXT] = Text(PAUSE, 10.5*TILE_WIDTH, 20*TILE_HEIGHT, YELLOW, visible=False)
        self.all_text[GAMEOVERTXT] = Text(GAMEOVER, 9*TILE_WIDTH, 20*TILE_HEIGHT, YELLOW, visible=False)
        self.all_text[SCORETXT] = Text(SCORE_ARRAY, 16, 8)
        self.add_text(PLAYER_1, 3*TILE_WIDTH, 0, flash=True)
        self.add_text(HIGH_SCORE, 9*TILE_WIDTH, 0)

    def hide_text(self):
        self.all_text[READYTXT].visible = False
        self.all_text[PAUSETXT].visible = False
        self.all_text[GAMEOVERTXT].visible = False

    def show_text(self, id):
        self.hide_text()
        self.all_text[id].visible = True

    def update_score(self, score_array):
        for i in range(len(score_array)):
            if score_array[i] == 1:
                SCORE_ARRAY[i] = CHARACTERS[N1]
            elif score_array[i] == 2:
                SCORE_ARRAY[i] = CHARACTERS[N2]
            elif score_array[i] == 3:
                SCORE_ARRAY[i] = CHARACTERS[N3]
            elif score_array[i] == 4:
                SCORE_ARRAY[i] = CHARACTERS[N4]
            elif score_array[i] == 5:
                SCORE_ARRAY[i] = CHARACTERS[N5]
            elif score_array[i] == 6:
                SCORE_ARRAY[i] = CHARACTERS[N6]
            elif score_array[i] == 7:
                SCORE_ARRAY[i] = CHARACTERS[N7]
            elif score_array[i] == 8:
                SCORE_ARRAY[i] = CHARACTERS[N8]
            elif score_array[i] == 9:
                SCORE_ARRAY[i] = CHARACTERS[N9]
            else:
                SCORE_ARRAY[i] = CHARACTERS[N0]

    def update(self):
        for tkey in list(self.all_text.keys()):
            self.all_text[tkey].update()
            if self.all_text[tkey].destroy:
                self.remove_text(tkey)

    def draw(self):
        for tkey in list(self.all_text.keys()):
            self.all_text[tkey].draw()