__author__ = 'Vi'


from movement import Move
from board import Board


class Node(object):

    def __init__(self, parent, move, table):
        self.parent = parent
        self.move = move
        self.children = list()

        if parent is not None:
            self.table = parent.board.table
            self.table.moves.tryMove(move)
        else:
            self.table = table

        self.availableMoves = self.table.moves.getAvailableMoves()

        if self.availableMoves is []:
            self.alive = False
        else:
            self.alive = True

    def __repr__(self):
        return str(self.move)

    def getStatus(self):
        if self.alive:
            for child in self.children:
                if child.availableMoves is not [] and child.status is True:
                    self.alive = True
        else:
            self.alive = False
        return self.alive

    def getChildren(self):
        for move in self.availableMoves:
            self.children.append(Node(self, move))



