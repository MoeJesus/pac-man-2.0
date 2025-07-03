import pyxel
from vector import Vector2
from constants import *

class Node(object):
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.neighbors = {UP:None, DOWN:None, LEFT:None, RIGHT:None}

    def draw(self):
        for n in self.neighbors.keys():
            if self.neighbors[n] is not None:
                line_start = self.position.as_tuple()
                line_end = self.neighbors[n].position.as_tuple()
                pyxel.line(line_start[0], line_start[1], line_end[0], line_end[1], 7)
                pyxel.circ(self.position.x, self.position.y, 4, 8)


class NodeGroup(object):
    def __init__(self):
        self.node_list = []

    def setup_test_nodes(self):
        nodeA = Node(40, 40)
        nodeB = Node(80, 40)
        nodeC = Node(40, 80)
        nodeD = Node(80, 80)
        nodeE = Node(104, 80)
        nodeF = Node(40, 160)
        nodeG = Node(104, 160)
        nodeA.neighbors[RIGHT] = nodeB
        nodeA.neighbors[DOWN] = nodeC
        nodeB.neighbors[LEFT] = nodeA
        nodeB.neighbors[DOWN] = nodeD
        nodeC.neighbors[UP] = nodeA
        nodeC.neighbors[RIGHT] = nodeD
        nodeC.neighbors[DOWN] = nodeF
        nodeD.neighbors[UP] = nodeB
        nodeD.neighbors[LEFT] = nodeC
        nodeD.neighbors[RIGHT] = nodeE
        nodeE.neighbors[LEFT] = nodeD
        nodeE.neighbors[DOWN] = nodeG
        nodeF.neighbors[UP] = nodeC
        nodeF.neighbors[RIGHT] = nodeG
        nodeG.neighbors[UP] = nodeE
        nodeG.neighbors[LEFT] = nodeF
        self.node_list = [nodeA, nodeB, nodeC, nodeD, nodeE, nodeF, nodeG]

    def draw(self):
        for node in self.node_list:
            node.draw()