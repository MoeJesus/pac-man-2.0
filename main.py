import pyxel
from constants import *
from pacman import Pacman

class App:
    def __init__(self):
        pyxel.init(SCREENWIDTH, SCREENHEIGHT, display_scale = 2, title = "Pac-Man", fps = 60)
        pyxel.load("assets/resources.pyxres")
        self.frames = 0
        self.dt = 0
        self.pacman = Pacman()
        pyxel.run(self.update, self.draw)

    def start_game(self):
        pass

    def update(self):
        self.frames = pyxel.frame_count
        self.dt = self.frames / 60
        self.pacman.update(self.dt)

    def draw(self):
        pyxel.cls(0)
        pyxel.text(0, 0, str(self.dt), 7)
        self.pacman.draw()

App()

# https://pacmancode.com/basic-movement