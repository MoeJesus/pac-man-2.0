import pyxel
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from pellets import PelletGroup
from ghosts import GhostGroup
from fruit import Fruit


class App:
    def __init__(self):
        pyxel.init(SCREENWIDTH, SCREENHEIGHT, display_scale = 2, title = "Pac-Man", fps = 60)
        pyxel.load("assets/resources.pyxres")
        self.start_game()
        self.fruit = None
        pyxel.run(self.update, self.draw)

    def start_game(self):
        self.nodes = NodeGroup("assets/maze.txt")
        self.nodes.set_portal_pair((0, 17), (27, 17))
        home_key = self.nodes.create_home_nodes(11.5, 14)
        self.nodes.connect_home_nodes(home_key, (12, 14), LEFT)
        self.nodes.connect_home_nodes(home_key, (15, 14), RIGHT)
        self.pacman = Pacman(self.nodes.get_node_from_tiles(15, 26))
        self.pellets = PelletGroup("assets/maze.txt")
        self.ghosts = GhostGroup(self.nodes.get_starting_temp_node(), self.pacman)
        self.ghosts.blinky.set_start_node(self.nodes.get_node_from_tiles(2 + 11.5, 0 + 14))
        self.ghosts.pinky.set_start_node(self.nodes.get_node_from_tiles(2 + 11.5, 3 + 14))
        self.ghosts.inky.set_start_node(self.nodes.get_node_from_tiles(0 + 11.5, 3 + 14))
        self.ghosts.clyde.set_start_node(self.nodes.get_node_from_tiles(4 + 11.5, 3 + 14))
        self.ghosts.set_spawn_node(self.nodes.get_node_from_tiles(2 + 11.5, 3 + 14))

    def check_events(self):
        pass

    def check_pellet_events(self):
        pellet = self.pacman.eat_pellets(self.pellets.pellet_list)
        if pellet:
            self.pellets.num_eaten += 1
            self.pellets.pellet_list.remove(pellet)
            if pellet.name == POWER_PELLET:
                self.ghosts.start_fright()

    def check_ghost_events(self):
        for ghost in self.ghosts:
            if self.pacman.collide_ghost(ghost):
                if ghost.mode.current is FRIGHT:
                    ghost.start_spawn()

    def check_fruit_events(self):
        if self.pellets.num_eaten == 50 or self.pellets.num_eaten == 140:
            if self.fruit is None:
                self.fruit = Fruit(self.nodes.get_node_from_tiles(9, 20))
        if self.fruit is not None:
            if self.pacman.collide_check(self.fruit):
                self.fruit = None
            elif self.fruit.destroy:
                self.fruit = None

    def update(self):
        self.pacman.update()
        self.ghosts.update()
        self.pellets.update()
        if self.fruit is not None:
            self.fruit.update()
        self.check_events()
        self.check_pellet_events()
        self.check_ghost_events()
        self.check_fruit_events()

    def draw(self):
        pyxel.cls(0)
        #self.nodes.draw()
        pyxel.bltm(0, 0, 0, 0, 0, pyxel.width, pyxel.height, 0)
        self.pellets.draw()
        if self.fruit is not None:
            self.fruit.draw()
        self.pacman.draw()
        self.ghosts.draw()

App()

# https://pacmancode.com/fruit