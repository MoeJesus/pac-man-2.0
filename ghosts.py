import pyxel
from vector import Vector2
from constants import *
from entity import Entity
from modes import ModeController


class Ghost(Entity):
    def __init__(self, node, pacman = None):
        Entity.__init__(self, node)
        self.name = GHOST
        self.points = 200
        self.goal = Vector2()
        self.direction_method = self.goal_direction
        self.pacman = pacman
        self.mode = ModeController(self)

    # These three functions set the spawn area for the ghosts, as well as where they go after getting eaten
    def set_spawn_node(self, node):
        self.spawn_node = node

    def start_spawn(self):
        self.mode.set_spawn_mode()
        if self.mode.current == SPAWN:
            self.set_speed(1.5)
            self.direction_method = self.goal_direction
            self.spawn()

    def spawn(self):
        self.goal = self.spawn_node.position

    # Scatter mode
    def scatter(self):
        self.goal = Vector2()

    # Chase mode
    def chase(self):
        self.goal = self.pacman.position

    # Sets ghost to fright mode
    def start_fright(self):
        self.mode.set_fright_mode()
        if self.mode.current == FRIGHT:
            self.set_speed(.5)
            self.direction_method = self.random_direction

    # Sets ghosts back to their original mode
    def normal_mode(self):
        self.set_speed(1)
        self.direction_method = self.goal_direction

    def update(self):
        self.mode.update()
        if self.mode.current is SCATTER:
            self.scatter()
        elif self.mode.current is CHASE:
            self.chase()
        Entity.update(self)