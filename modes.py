from constants import *


class MainMode(object):
    def __init__(self):
        self.timer = 0
        self.scatter()

    # Scatter mode
    def scatter(self):
        self.mode = SCATTER
        self.time = 420
        self.timer = 0

    # Chase mode
    def chase(self):
        self.mode = CHASE
        self.time = 1200
        self.timer = 0

    def update(self):
        self.timer += 1
        if self.timer >= self.time:
            if self.mode is SCATTER:
                self.chase()
            elif self.mode is CHASE:
                self.scatter()


class ModeController(object):
    def __init__(self, entity):
        self.timer = 0
        self.time = None
        self.mainmode = MainMode()
        self.current = self.mainmode.mode
        self.entity = entity

    # Sets ghosts to fright mode
    def set_fright_mode(self):
        if self.current in [SCATTER, CHASE]:
            self.timer = 0
            self.time = 420
            self.current = FRIGHT
        elif self.current is FRIGHT:
            self.timer = 0

    # Sets ghosts to spawn mode
    def set_spawn_mode(self):
        if self.current is FRIGHT:
            self.current = SPAWN

    def update(self):
        self.mainmode.update()
        if self.current is FRIGHT:
            self.timer += 1
            if self.timer >= self.time:
                self.time = None
                self.entity.normal_mode()
                self.current = self.mainmode.mode
        elif self.current in [SCATTER, CHASE]:
            self.current = self.mainmode.mode
        if self.current is SPAWN:
            if self.entity.node == self.entity.spawn_node:
                self.entity.normal_mode()
                self.current = self.mainmode.mode