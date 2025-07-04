import pyxel
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from pellets import PelletGroup


class App:
    def __init__(self):
        pyxel.init(SCREENWIDTH, SCREENHEIGHT, display_scale = 2, title = "Pac-Man", fps = 60)
        pyxel.load("assets/resources.pyxres")
        self.start_game()
        pyxel.run(self.update, self.draw)

    def start_game(self):
        self.nodes = NodeGroup("maze.txt")
        self.nodes.set_portal_pair((0, 17), (27, 17))
        self.pacman = Pacman(self.nodes.get_starting_temp_node())
        self.pellets = PelletGroup("maze.txt")

    def check_events(self):
        pass

    def check_pellet_events(self):
        pellet = self.pacman.eat_pellets(self.pellets.pellet_list)
        if pellet:
            self.pellets.num_eaten += 1
            self.pellets.pellet_list.remove(pellet)

    def update(self):
        self.pacman.update()
        self.pellets.update()
        self.check_events()
        self.check_pellet_events()

    def draw(self):
        pyxel.cls(0)
        #self.nodes.draw()
        pyxel.bltm(0, 0, 0, 0, 0, pyxel.width, pyxel.height, 0)
        self.pellets.draw()
        self.pacman.draw()

App()

# https://pacmancode.com/ghosts-intro