import pyxel
from constants import *
from pacman import Pacman
from nodes import NodeGroup

class App:
    def __init__(self):
        pyxel.init(SCREENWIDTH, SCREENHEIGHT, display_scale = 2, title = "Pac-Man", fps = 60)
        pyxel.load("assets/resources.pyxres")
        self.start_game()
        pyxel.run(self.update, self.draw)

    def start_game(self):
        self.nodes = NodeGroup()
        self.nodes.setup_test_nodes()
        self.pacman = Pacman(self.nodes.node_list[0])

    def check_events(self):
        pass

    def update(self):
        self.pacman.update()
        self.check_events()

    def draw(self):
        pyxel.cls(0)
        self.nodes.draw()
        self.pacman.draw()

App()

# https://pacmancode.com/maze-basics