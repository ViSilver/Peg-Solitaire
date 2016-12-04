__author__ = 'Vi'


from cell import CellType
# from board import Board

class Moves(object):
	"""docstring for Moves"""

	def __init__(self, board):
		self.board = board
		self.queueOfMoves = list()
		self.moveId = 0
		self.curMove = None
		self.curX = 0
		self.curY = 0
		self.passedX = None
		self.passedY = None


	def getDirection(self, newX, newY):
		if newX == self.curX:
			if newY > self.curY:
				return 'north'
			elif newY < self.curY:
				return 'south'
		elif newY == self.curY:
			if newX > self.curX:
				return 'east'
			if newX < self.curX:
				return 'west'
		else:
			return ''


	def tryMove(self, move):
		newX = move.toPos[0]
		newY = move.toPos[1]

		if self.board.cellAt(move.toPos) is not CellType.EmptyCell:
			print(move.toPos, " it's not an empty cell")
			return False
		elif abs(self.curX - newX) == 0 and abs(self.curY - newY) != 2:
			print("Distance on y is not 2")
			return False
		elif abs(self.curX - newX) != 2 and abs(self.curY - newY) == 0:
			print("Distance on y is not 2")
			return False
		elif abs(self.curX - newX) != 2 and abs(self.curY - newY) != 2:
			print("Moving on diagonal")
			return False
		elif (newX > 5 or newX < 3) and (newY > 5 or newY < 3):
			return False
		elif (newX > 8 or newX < 0) and (newY > 8 or newY < 0):
			return False
		else:
			direct = self.getDirection(newX, newY)
			if direct == '':
				return False
			print('Move: -> ', direct)

			if direct == 'east':
				if self.board.cellAt((newX - 1, newY)) != CellType.LivingCell:
					print("Jumping over an empty cell.")
					return False
				self.board.setCellAt((newX - 1, newY), CellType.PassedCell)
				self.passedX = newX - 1
				self.passedY = newY
			elif direct == 'west':
				if self.board.cellAt((newX + 1, newY)) != CellType.LivingCell:
					print("Jumping over an empty cell.")
					return False
				self.board.setCellAt((newX + 1, newY), CellType.PassedCell)
				self.passedX = newX + 1
				self.passedY = newY
			elif direct == 'south':
				if self.board.cellAt((newX, newY + 1)) != CellType.LivingCell:
					print("Jumping over an empty cell.")
					return False
				self.board.setCellAt((newX, newY + 1), CellType.PassedCell)
				self.passedX = newX
				self.passedY = newY + 1
			elif direct == 'north':
				if self.board.cellAt((newX, newY - 1)) != CellType.LivingCell:
					print("Jumping over an empty cell.")
					return False
				self.board.setCellAt((newX, newY - 1), CellType.PassedCell)
				self.passedX = newX
				self.passedY = newY - 1

			self.board.deselectCell()
			self.board.setCellAt(move.fromPos, CellType.EmptyCell)
			self.board.aliveCells -= 1
			self.board.update()
			self.board.timer.start(self.board.Speed, self.board)
			self.board.setCellAt(move.toPos, CellType.LivingCell)
			self.lastMove = move
			self.queueOfMoves[self.moveId:] = []
			self.moveId += 1
			self.queueOfMoves.append(move)
			print("Queue (inside tryMove): ", self.queueOfMoves)
			self.board.update()

			return True


	def undo(self):
		print("Try to undo to", self.moveId - 1)
		if self.moveId > 0:
			self.moveId -= 1
			self.lastMove = self.queueOfMoves[self.moveId - 1]
			move = self.queueOfMoves[self.moveId]
			self.makeMoveBack(move.reverse())
			print("Queue(undo): ", self.queueOfMoves)
		return


	def makeMoveBack(self, move):
		print("moving back to movement id ", self.moveId)
		self.curX = move.toPos[0]
		self.curY = move.toPos[1]
		self.board.setCellAt(move.toPos, CellType.LivingCell)
		self.board.setCellAt(move.fromPos, CellType.EmptyCell)

		direct = self.getDirection(move.fromPos[0], move.fromPos[1])

		if direct == 'east':
			self.board.setCellAt((self.curX + 1, self.curY), CellType.LivingCell)
		elif direct == 'west':
			self.board.setCellAt((self.curX - 1, self.curY), CellType.LivingCell)
		elif direct == 'north':
			self.board.setCellAt((self.curX, self.curY + 1), CellType.LivingCell)
		elif direct == 'south':
			self.board.setCellAt((self.curX, self.curY - 1), CellType.LivingCell)

		self.board.update()
		return


	def redo(self):
		print("Try to redo to ", self.moveId + 1)
		if self.moveId < len(self.queueOfMoves):
			self.lastMove = self.queueOfMoves[self.moveId]
			self.moveId += 1
			self.board.setCellAt(self.lastMove.toPos, CellType.LivingCell)
			self.curX = self.lastMove.fromPos[0]
			self.curY = self.lastMove.fromPos[1]
			self.board.setCellAt(self.lastMove.fromPos, CellType.EmptyCell)

			direct = self.getDirection(self.lastMove.toPos[0], self.lastMove.toPos[1])

			if direct == 'east':
				print("east")
				self.board.setCellAt((self.curX + 1, self.curY), CellType.EmptyCell)
			elif direct == 'west':
				print("west")
				self.board.setCellAt((self.curX - 1, self.curY), CellType.EmptyCell)
			elif direct == 'north':
				print('north')
				self.board.setCellAt((self.curX, self.curY + 1), CellType.EmptyCell)
			elif direct == 'south':
				print('south')
				self.board.setCellAt((self.curX, self.curY - 1), CellType.EmptyCell)

			self.board.update()
			print("Queue(redo): ", self.queueOfMoves)
		return


class Move(object):
	"""docstring for Movement"""

	def __init__(self, fromPos, toPos):
		self.fromPos = fromPos
		self.toPos = toPos
		self.step = (self.fromPos, self.toPos)

	def __repr__(self):
		return str((self.fromPos, self.toPos))

	def setToPos(self, toPos):
		self.toPos = toPos

	def reverse(self):
		newMove = Move(self.toPos, self.fromPos)
		return newMove
