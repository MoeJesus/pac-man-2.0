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
        pyxel.run(self.update, self.draw)

    def text_maker(self, text, x, y):
        text = text
        #text_length = len(text) + 1
        x = x
        y = y
        i = 0
        for _ in text:
            pyxel.blt(x + (i * 8), y, 0, text[i][0], text[i][1], text[i][2], text[i][3])
            i += 1

    def update(self):
        pass

    def draw(self):
        pyxel.cls(0)
        Text(TEXT1, 32, 16)
        

class Text(object):
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.text = []
        setup_text()

    def setup_text(self):
        self.text[id] = [TEXT1, TEXT2]

    def draw(self):
        for _ in text:
            pass


App()