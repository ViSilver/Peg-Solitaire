__author__ = 'Vi'


from movement import Move
from board import Board


class Node(object):

	def __init__(self, parent, move):
		self.parent = parent
		self.move = move
		self.children = list()
		self.board = parent.board.moves.tryMove(move)
		self.availableMoves = self.board.moves.getAvailableMoves()
		self.alive = True


	def __repr__(self):
		return str(self.move)


	def getStatus(self):
		for child in self.children:
			if child.availableMoves is not [] and child.status is True:
				return True
		return False


