import pyxel
from vector import Vector2
from constants import *
from entity import Entity
from modes import ModeController


class Ghost(Entity):
    def __init__(self, node, pacman = None, blinky = None):
        Entity.__init__(self, node)
        self.name = GHOST
        self.points = 200
        self.goal = Vector2()
        self.direction_method = self.goal_direction
        self.pacman = pacman
        self.mode = ModeController(self)
        self.blinky = blinky
        self.home_node = node

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


class Blinky(Ghost):
    def __init__(self, node, pacman = None, blinky = None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = BLINKY
        self.entity_image = [32, 48, 16, 16]


class Pinky(Ghost):
    def __init__(self, node, pacman = None, blinky = None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = PINKY
        self.entity_image = [32, 64, 16, 16]

    def scatter(self):
        self.goal = Vector2(TILEWIDTH * NCOLS, 0)

    def chase(self):
        self.goal = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4


class Inky(Ghost):
    def __init__(self, node, pacman = None, blinky = None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = INKY
        self.entity_image = [32, 80, 16, 16]

    def scatter(self):
        self.goal = Vector2(TILEWIDTH * NCOLS, TILEHEIGHT * NROWS)

    def chase(self):
        vec1 = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 2
        vec2 = (vec1 - self.blinky.position) * 2
        self.goal = self.blinky.position + vec2


class Clyde(Ghost):
    def __init__(self, node, pacman = None, blinky = None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = CLYDE
        self.entity_image = [32, 96, 16, 16]

    def scatter(self):
        self.goal = Vector2(0, TILEHEIGHT * NROWS)

    def chase(self):
        d = self.pacman.position - self.position
        ds = d.magnitude_squared()
        if ds <= (TILEWIDTH * 8) ** 2:
            self.scatter()
        else:
            self.goal = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4


class GhostGroup(object):
    def __init__(self, node, pacman):
        self.blinky = Blinky(node, pacman)
        self.pinky = Pinky(node, pacman)
        self.inky = Inky(node, pacman, self.blinky)
        self.clyde = Clyde(node, pacman)
        self.ghosts = [self.blinky, self.pinky, self.inky, self.clyde]

    def __iter__(self):
        return iter(self.ghosts)

    def set_spawn_node(self, node):
        for ghost in self:
            ghost.set_spawn_node(node)

    def update_points(self):
        for ghost in self:
            ghost.points *= 2

    def reset_points(self):
        for ghost in self:
            ghost.points = 200

    def start_fright(self):
        for ghost in self:
            ghost.start_fright()
        self.reset_points()

    def hide(self):
        for ghost in self:
            ghost.visible = False

    def show(self):
        for ghost in self:
            ghost.visible = True

    def reset(self):
        for ghost in self:
            ghost.reset()

    def update(self):
        for ghost in self:
            ghost.update()

    def draw(self):
        for ghost in self:
            ghost.draw()