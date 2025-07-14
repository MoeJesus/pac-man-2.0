import pyxel

# Character list constants
A = 0
B = 1

# Character dictionary
CHARACTERS = {A: [0, 8, 8, 8], B:[8, 8, 8, 8]}

# Text constants
TEXT1 = (CHARACTERS[A], CHARACTERS[B])
TEXT2 = (CHARACTERS[B], CHARACTERS[A])

class App:
    def __init__(self):
        pyxel.init(160, 120)
        pyxel.load("assets/resources.pyxres")
        self.text_group = TextGroup()
        pyxel.run(self.update, self.draw)

    def update(self):
        pass

    def draw(self):
        pyxel.cls(0)
        self.text_group.draw()


class Text(object):
    def __init__(self, text, x, y):
        self.text = text
        self.x = x
        self.y = y

    def draw(self):
        i = 0
        for _ in self.text:
            pyxel.blt(self.x + (i * 8), self.y, 0, self.text[i][0], self.text[i][1], self.text[i][2], self.text[i][3])
            i += 1


class TextGroup(object):
    def __init__(self):
        self.next_id = 10
        self.all_text = {}
        self.setup_text()

    def add_text(self, text, x, y):
        self.next_id += 1
        self.all_text[self.next_id] = Text(text, x, y)
        return self.next_id

    def setup_text(self):
        self.add_text(TEXT1, 32, 16)
        self.add_text(TEXT2, 32, 24)

    def draw(self):
        for tkey in (self.all_text):
            self.all_text[tkey]. draw()


App()