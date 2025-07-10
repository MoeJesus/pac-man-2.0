import pyxel
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from pellets import PelletGroup
from ghosts import GhostGroup
from fruit import Fruit


class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, display_scale=2, title="Pac-Man", fps=60)
        pyxel.load("assets/resources.pyxres")
        self.start_game()
        self.pause = Pause(True)
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
        self.ghosts.blinky.set_start_node(self.nodes.get_node_from_tiles(2+11.5, 0+14))
        self.ghosts.pinky.set_start_node(self.nodes.get_node_from_tiles(2+11.5, 3+14))
        self.ghosts.inky.set_start_node(self.nodes.get_node_from_tiles(0+11.5, 3+14))
        self.ghosts.clyde.set_start_node(self.nodes.get_node_from_tiles(4+11.5, 3+14))
        self.ghosts.set_spawn_node(self.nodes.get_node_from_tiles(2+11.5, 3+14))

    def show_entities(self):
        self.pacman.visible = True
        self.ghosts.show()

    def hide_entities(self):
        self.pacman.visible = False
        self.ghosts.hide()
    
    def check_events(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        elif pyxel.btnp(pyxel.KEY_SPACE):
            self.pause.set_pause(player_paused=True)
            if not self.pause.paused:
                self.show_entities()
            else:
                self.hide_entities()

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
                    self.pacman.visible = False
                    ghost.visible = False
                    self.pause.set_pause(pause_time=60, func=self.show_entities)
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
        if not self.pause.paused:
            self.pacman.update()
            self.ghosts.update()
            self.pellets.update()
            if self.fruit is not None:
                self.fruit.update()
            self.check_pellet_events()
            self.check_ghost_events()
            self.check_fruit_events()
        after_pause = self.pause.update()
        if after_pause is not None:
            after_pause()
        self.check_events()

    def draw(self):
        pyxel.cls(0)
        #self.nodes.draw()
        pyxel.bltm(0, 0, 0, 0, 0, pyxel.width, pyxel.height, 0)
        self.pellets.draw()
        if self.fruit is not None:
            self.fruit.draw()
        self.pacman.draw()
        self.ghosts.draw()


# Adds the ability to pause the game
class Pause():
    def __init__(self, paused=False):
        self.paused = paused
        self.timer = 0
        self.pause_time = None
        self.func = None

    # Switches the state
    def flip(self):
        self.paused = not self.paused

    # Sets the pause effect
    def set_pause(self, player_paused=False, pause_time=None, func=None):
        self.timer = 0
        self.func = func
        self.pause_time = pause_time
        self.flip()

    def update(self):
        if self.pause_time is not None:
            self.timer += 1
            if self.timer >= self.pause_time:
                self.timer = 0
                self.paused = False
                self.pause_time = None
                return self.func
        return None


App()

# https://pacmancode.com/level-advancing