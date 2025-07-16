import pyxel
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from pellets import PelletGroup
from ghosts import GhostGroup
from fruit import Fruit
from text import TextGroup


class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, display_scale=2, title="Pac-Man", fps=60)
        pyxel.load("assets/resources.pyxres")
        self.start_game()
        self.level = 0
        self.lives = 5
        self.pause = Pause(True)
        self.fruit = None
        self.score = 0
        self.printed_score = {}
        self.text_group = TextGroup()
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
        self.nodes.deny_home_access(self.pacman)
        self.nodes.deny_home_access_list(self.ghosts)
        self.nodes.deny_access_list(2+11.5, 3+14, LEFT, self.ghosts)
        self.nodes.deny_access_list(2+11.5, 3+14, RIGHT, self.ghosts)
        self.ghosts.inky.start_node.deny_access(RIGHT, self.ghosts.inky)
        self.ghosts.clyde.start_node.deny_access(LEFT, self.ghosts.clyde)
        self.nodes.deny_access_list(12, 14, UP, self.ghosts)
        self.nodes.deny_access_list(15, 14, UP, self.ghosts)
        self.nodes.deny_access_list(12, 26, UP, self.ghosts)
        self.nodes.deny_access_list(15, 26, UP, self.ghosts)

    def next_level(self):
        self.show_entities()
        self.level += 1
        self.pause.paused = True
        self.start_game()

    def reset_level(self):
        self.pause.paused = True
        self.pacman.reset()
        self.ghosts.reset()
        self.fruit = None
        self.text_group.show_text(READYTXT)

    def restart_game(self):
        self.lives = 5
        self.level = 0
        self.pause.paused = True
        self.fruit = None
        self.score = 0
        self.text_group.update_score(self.score)
        self.text_group.show_text(READYTXT)
        self.start_game()
    
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
            if self.pacman.alive:
                self.pause.set_pause(player_paused=True)
                if not self.pause.paused:
                    self.text_group.hide_text()
                    self.show_entities()
                else:
                    self.text_group.show_text(PAUSETXT)
                    self.hide_entities()

    def check_pellet_events(self):
        pellet = self.pacman.eat_pellets(self.pellets.pellet_list)
        if pellet:
            self.pellets.num_eaten += 1
            self.update_score(pellet.points)
            if self.pellets.num_eaten == 30:
                self.ghosts.inky.start_node.allow_access(RIGHT, self.ghosts.inky)
            if self.pellets.num_eaten == 70:
                self.ghosts.clyde.start_node.allow_access(LEFT, self.ghosts.clyde)
            self.pellets.pellet_list.remove(pellet)
            if pellet.name == POWER_PELLET:
                self.ghosts.start_fright()
            if self.pellets.is_empty():
                self.hide_entities()
                self.pause.set_pause(pause_time=180, func=self.next_level)

    def check_ghost_events(self):
        for ghost in self.ghosts:
            if self.pacman.collide_ghost(ghost):
                if ghost.mode.current is FRIGHT:
                    self.pacman.visible = False
                    ghost.visible = False
                    self.update_score(ghost.points)
                    self.text_group.add_text(self.ghosts.check_points(ghost.points), ghost.position.x - 4, ghost.position.y, time = 60)
                    self.ghosts.update_points()
                    self.pause.set_pause(pause_time=60, func=self.show_entities)
                    ghost.start_spawn()
                    self.nodes.allow_home_access(ghost)
                elif ghost.mode.current is not SPAWN:
                    if self.pacman.alive:
                        self.lives -= 1
                        self.pacman.die()
                        self.ghosts.hide()
                        if self.lives <= 0:
                            self.text_group.show_text(GAMEOVERTXT)
                            self.pause.set_pause(pause_time=180, func=self.restart_game)
                        else:
                            self.pause.set_pause(pause_time=180, func=self.reset_level)

    def check_fruit_events(self):
        if self.pellets.num_eaten == 50 or self.pellets.num_eaten == 140:
            if self.fruit is None:
                self.fruit = Fruit(self.nodes.get_node_from_tiles(9, 20))
        if self.fruit is not None:
            if self.pacman.collide_check(self.fruit):
                self.update_score(self.fruit.points)
                self.text_group.add_text(self.fruit.check_points(self.fruit.points), self.fruit.position.x - 4, self.fruit.position.y, time = 60)
                self.fruit = None
            elif self.fruit.destroy:
                self.fruit = None

    def update_score(self, points):
        self.score += points
        for i in range(len(str(self.score))):
            self.printed_score[i] = (self.score // (10**(len(str(self.score)) - i - 1))) % 10
        self.text_group.update_score(self.printed_score)

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
        self.text_group.update()
        self.check_events()

    def draw(self):
        pyxel.cls(0)
        #self.nodes.draw()
        pyxel.bltm(0, 0, 0, 0, 0, pyxel.width, pyxel.height, 0)
        self.pellets.draw()
        self.text_group.draw()
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

# https://pacmancode.com/text
# https://github.com/blinklet/learning-pyxel