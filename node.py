__author__ = 'Vi'


from movement import Move
from board import Board
from cell import CellType
import copy


class Node(object):

	def __init__(self, table):
		self.children = list()

		self.table = copy.deepcopy(table)
		self.table.moves.table = self.table

		for x in range(table.TableWidth):
			for y in range(table.TableWidth):
				self.table.grid[x][y] = table.grid[x][y]

		self.availableMoves = self.table.moves.getAvailableMoves()

		if self.availableMoves is []:
			self.alive = False
		else:
			self.alive = True

		self.weight = 0


	def __cmp__(self, other):
		if self.weight < other.weight:
			return self
		else:
			return other


	def getStatus(self):
		if self.alive:
			for child in self.children:
				if child.availableMoves is not [] and \
								child.getStatus() is True:
					self.alive = True
		else:
			self.alive = False
		return self.alive


	def getChildren(self):
		for move in self.availableMoves:
			child = Node(self.table.copy())
			child.table.moves.tryMove(move, None)
			child.availableMoves = child.table.moves.\
				getAvailableMoves()
			# print(child.table.getNrAliveCells())
			child.weight = child.computeWeight()
			self.children.append(child)
		return self.children


	def computeWeight(self):
		value = 0
		a = 0
		b = 0

		for x in range(self.table.TableWidth):
			for y in range(self.table.TableHeight):
				if self.table.cellAt((x, y)).cellType is \
						CellType.LivingCell:
					if x <= (self.table.TableWidth - 1)/2:
						a = x
					else:
						a = self.table.TableWidth - x - 1
					if y <= (self.table.TableHeight - 1)/2:
						b = y
					else:
						b = self.table.TableHeight - y - 1
					value += (a * b)
		return value/(self.table.aliveCells + value)
