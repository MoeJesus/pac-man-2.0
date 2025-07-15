import pyxel

# Character list constants
N0 = 0
N1 = 1
N2 = 2
N3 = 3
N4 = 4
N5 = 5
N6 = 6
N7 = 7
N8 = 8
N9 = 9

# Character dictionary
CHARACTERS = {N0: [0, 8, 8, 8], N1:[8, 8, 8, 8], N2:[16, 8, 8, 8], N3:[24, 8, 8, 8], N4:[32, 8, 8, 8], N5:[40, 8, 8, 8], N6:[48, 8, 8, 8], N7:[56, 8, 8, 8], N8:[64, 8, 8, 8], N9:[72, 8, 8, 8], }

# Text constants
TEXT1 = [0] * 8

SCORETXT = 0


class App:
    def __init__(self):
        pyxel.init(160, 120, fps=30)
        pyxel.load("assets/resources.pyxres")
        self.text_group = TextGroup()
        self.score = 0
        self.print_score = [0] * 8
        pyxel.run(self.update, self.draw)

    def score_text(self, score):
        for i in range(8):
            self.print_score[i] = (score // (10**(7 - i))) % 10

    def update(self):
        self.score += 1
        self.score_text(self.score)
        self.text_group.update_score(self.print_score)

    def draw(self):
        pyxel.cls(0)
        self.text_group.draw()
        print(self.print_score)


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
        self.all_text[SCORETXT] = Text(TEXT1, 32, 16)

    def update_score(self, score_array):
        for i in range(len(score_array)):
            if score_array[i] == 1:
                TEXT1[i] = CHARACTERS[N1]
            elif score_array[i] == 2:
                TEXT1[i] = CHARACTERS[N2]
            elif score_array[i] == 3:
                TEXT1[i] = CHARACTERS[N3]
            elif score_array[i] == 4:
                TEXT1[i] = CHARACTERS[N4]
            elif score_array[i] == 5:
                TEXT1[i] = CHARACTERS[N5]
            elif score_array[i] == 6:
                TEXT1[i] = CHARACTERS[N6]
            elif score_array[i] == 7:
                TEXT1[i] = CHARACTERS[N7]
            elif score_array[i] == 8:
                TEXT1[i] = CHARACTERS[N8]
            elif score_array[i] == 9:
                TEXT1[i] = CHARACTERS[N9]
            else:
                TEXT1[i] = CHARACTERS[N0]

    def draw(self):
        for tkey in (self.all_text):
            self.all_text[tkey].draw()


App()