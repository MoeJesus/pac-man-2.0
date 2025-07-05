import pyxel
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from pellets import PelletGroup
from ghosts import Ghost


class App:
    def __init__(self):
        pyxel.init(SCREENWIDTH, SCREENHEIGHT, display_scale = 2, title = "Pac-Man", fps = 60)
        pyxel.load("assets/resources.pyxres")
        self.start_game()
        pyxel.run(self.update, self.draw)

    def start_game(self):
        self.nodes = NodeGroup("maze.txt")
        self.nodes.set_portal_pair((0, 17), (27, 17))
        home_key = self.nodes.create_home_nodes(11.5, 14)
        self.nodes.connect_home_nodes(home_key, (12, 14), LEFT)
        self.nodes.connect_home_nodes(home_key, (15, 14), RIGHT)
        self.pacman = Pacman(self.nodes.get_starting_temp_node())
        self.pellets = PelletGroup("maze.txt")
        self.ghost = Ghost(self.nodes.get_starting_temp_node(), self.pacman)
        self.ghost.set_spawn_node(self.nodes.get_node_from_tiles(2 + 11.5, 3 + 14))

    def check_events(self):
        pass

    def check_pellet_events(self):
        pellet = self.pacman.eat_pellets(self.pellets.pellet_list)
        if pellet:
            self.pellets.num_eaten += 1
            self.pellets.pellet_list.remove(pellet)
            if pellet.name == POWER_PELLET:
                self.ghost.start_fright()

    def check_ghost_events(self):
        if self.pacman.collide_ghost(self.ghost):
            if self.ghost.mode.current is FRIGHT:
                self.ghost.start_spawn()

    def update(self):
        self.pacman.update()
        self.ghost.update()
        self.pellets.update()
        self.check_events()
        self.check_pellet_events()
        self.check_ghost_events()

    def draw(self):
        pyxel.cls(0)
        #self.nodes.draw()
        pyxel.bltm(0, 0, 0, 0, 0, pyxel.width, pyxel.height, 0)
        self.pellets.draw()
        self.pacman.draw()
        self.ghost.draw()

App()

# https://pacmancode.com/more-ghosts