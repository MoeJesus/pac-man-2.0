import pyxel
from vector import Vector2
from constants import *
from random import randint


class Entity(object):
    def __init__(self, node):
        self.name = None
        self.directions = {STOP:Vector2(), UP:Vector2(0, -1), DOWN:Vector2(0, 1), LEFT:Vector2(-1, 0), RIGHT:Vector2(1,0)}
        self.direction = STOP
        self.set_speed(1)
        self.collide_radius = 4
        self.visible = True
        self.disable_portal = False
        self.goal = None
        self.direction_method = self.random_direction
        self.set_start_node(node)

    # Sets the starting position
    def set_start_node(self, node):
        self.node = node
        self.start_node = node
        self.target = node
        self.set_position()

    # Copies the node position to the entity's position
    def set_position(self):
        self.position = self.node.position.copy()

    # Allows entities to be set between two nodes
    def set_between_nodes(self, direction):
        if self.node.neighbors[direction] is not None:
            self.target = self.node.neighbors[direction]
            self.position = (self.node.position + self.target.position) / 2.0

    # These two functions check to see if the entity can move and go a certain direction
    def valid_direction(self, direction):
        if direction is not STOP:
            if self.node.neighbors[direction] is not None:
                return True
        return False

    def get_new_target(self, direction):
        if self.valid_direction(direction):
            return self.node.neighbors[direction]
        return self.node

    # These three functions are used for non-player entities to chose what direction to go
    def valid_directions(self):
        directions = []
        for key in [UP, DOWN, LEFT, RIGHT]:
            if self.valid_direction(key):
                if key != self.direction * -1:
                    directions.append(key)
        if len(directions) == 0:
            directions.append(self.direction * -1)
        return directions

    def random_direction(self, directions):
        return directions[randint(0, len(directions) - 1)]

    def goal_direction(self, directions):
        distances = []
        for direction in directions:
            vec = self.node.position + self.directions[direction] * TILEWIDTH - self.goal
            distances.append(vec.magnitude_squared())
        index = distances.index(min(distances))
        return directions[index]

    # Checks to see if the entity overshoots a node
    def overshot_target(self):
        if self.target is not None:
            vec1 = self.target.position - self.node.position
            vec2 = self.position - self.node.position
            node_to_target = vec1.magnitude_squared()
            node_to_self = vec2.magnitude_squared()
            return node_to_self >= node_to_target
        return False

    # These two functions allow the entity to move opposite from its current movement if it can
    def reverse_direction(self):
        self.direction *= -1
        temp = self.node
        self.node = self.target
        self.target = temp

    def opposite_direction(self, direction):
        if direction is not STOP:
            if direction == self.direction * -1:
                return True
        return False

    # Sets the speed of the entity
    def set_speed(self, speed):
        self.speed = speed * TILEWIDTH / 8

    def update(self):
        self.position += self.directions[self.direction] * self.speed
        if self.overshot_target():
            self.node = self.target
            directions = self.valid_directions()
            direction = self.direction_method(directions)
            if not self.disable_portal:
                if self.node.neighbors[PORTAL] is not None:
                    self.node = self.node.neighbors[PORTAL]
            self.target = self.get_new_target(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.get_new_target(self.direction)
            self.set_position()

    def draw(self):
        sprite_x = self.entity_image[0]
        sprite_y = self.entity_image[1]
        width = self.entity_image[2]
        height = self.entity_image[3]

        if self.visible:
            if self.direction == UP:
                sprite_x = ((pyxel.frame_count // 8 % 2) + 2) * 16
            elif self.direction == DOWN:
                sprite_x = ((pyxel.frame_count // 8 % 2) + 4) * 16
            elif self.direction == LEFT:
                sprite_x = pyxel.frame_count // 8 % 2 * 16
                width = width * -1
            elif self.direction == RIGHT:
                sprite_x = pyxel.frame_count // 8 % 2 * 16

            pyxel.blt(self.position.x-(TILEWIDTH/2), self.position.y-(TILEWIDTH/2), 0, sprite_x, sprite_y, width, height, 0)