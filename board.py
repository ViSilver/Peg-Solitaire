__author__ = 'Vi'


from PyQt5.QtGui import (QPainter, QColor)
from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import (Qt, QBasicTimer, pyqtSignal)
from cell import CellType, Cell
from movement import Move, Moves


class Board(QFrame):
	"""docstring for Board"""

	msg2Statusbar = pyqtSignal(str)

	BoardWidth = 9
	BoardHeight = 9
	Speed = 200

	def __init__(self, parent):
		super().__init__(parent)
		self.initBoard()


	def initBoard(self):
		self.timer = QBasicTimer()
		self.table = list()
		self.aliveCells = 44
		self.setFocusPolicy(Qt.StrongFocus)
		self.isStarted = False
		self.isPaused = False
		self.isSelected = False
		self.clearBoard()
		self.moves = Moves(self)


	def cellAt(self, pos):
		return self.table[pos[0]][pos[1]]


	def setCellAt(self, pos, cell):
		self.table[pos[0]][pos[1]] = cell


	def squareWidth(self):
		return self.contentsRect().width() // Board.BoardWidth


	def squareHeight(self):
		return self.contentsRect().height() // Board.BoardHeight


	def start(self):
		if self.isPaused:
			return

		self.isStarted = True
		self.aliveCells = 45
		self.clearBoard()

		self.msg2Statusbar.emit(str(self.aliveCells))

		self.newEmptyCell(4, 4)
		self.setWalls()
		self.timer.start(Board.Speed, self)


	def pause(self):
		self.isPaused = not self.isPaused

		if self.isPaused:
			self.timer.stop()
			self.msg2Statusbar.emit("Paused")
		else:
			self.timer.start(Board.Speed, self)
			self.msg2Statusbar.emit(str(self.aliveCells))

		self.update()


	def paintEvent(self, event):
		painter = QPainter(self)
		rect = self.contentsRect()

		boardTop = rect.bottom() - Board.BoardHeight * self.squareHeight()

		for i in range(Board.BoardHeight):
			for j in range(Board.BoardWidth):
				cell = self.cellAt((j, i))
				self.drawSquare(painter, rect.left() + j * self.squareWidth(),
					boardTop + i * self.squareHeight(), cell)

		# Paint event after the mouse event


	def drawSquare(self, painter, x, y, cell):
		colorTable = [0xEEEEEE, 0x505050, 0xAAAAAA, 0xDADADA, 0x444444]

		color = QColor(colorTable[cell.cellType])
		painter.fillRect(x + 1, y + 1, self.squareWidth() - 2,
			self.squareHeight() - 2, color)

		painter.setPen(color.lighter())
		painter.drawLine(x, y + self.squareHeight() - 1, x, y)
		painter.drawLine(x, y, x + self.squareWidth() - 1, y)

		painter.setPen(color.darker())
		painter.drawLine(x + 1, y + self.squareHeight() - 1,
			x + self.squareWidth() - 1, y + self.squareHeight() - 1)
		painter.drawLine(x + self.squareWidth() - 1,
			y + self.squareHeight() - 1, x + self.squareWidth() - 1, y + 1)


	def keyPressEvent(self, event):
		if not self.isStarted:
			super(Board, self).keyPressEvent(event)

		key = event.key()

		if key == Qt.Key_P:
			self.pause()
			return

		if self.isPaused:
			return
		else:
			super(Board, self).keyPressEvent(event)


	def timerEvent(self, event):
		if not event.timerId() == self.timer.timerId():
			super(Board, self).timerEvent(event)
		else:
			if self.moves.passedX is not None and self.moves.passedY is not None:
				self.setCellAt((self.moves.passedX, self.moves.passedY), Cell(CellType.EmptyCell))
			self.msg2Statusbar.emit(str(self.aliveCells))
			self.timer.stop()
			self.update()
			return


	def mousePressEvent(self, event):
		if event.button() == Qt.LeftButton:
			pos = ((event.pos().x() - 2) // self.squareWidth(), (event.pos().y() - 8) // self.squareHeight())

			if self.cellAt(pos).cellType == CellType.Wall:
				print("Illegal selection of a wall.")
				return

			if self.isSelected:
				if pos[0] == self.moves.curX and pos[1] == self.moves.curY:
					print("Trying to select the same cell")
					self.deselectCell()
					self.update()
					return

				self.moves.curMove.setToPos(pos)

				if not self.moves.tryMove(self.moves.curMove):
					print("Impossible to move")
					self.deselectCell()
					self.update()
					return

			else:
				self.selectCellAt(pos)
				self.moves.curMove = Move(pos, None)
				self.update()

			print(pos)
		else:
			super(Board, self).mousePressEvent(event)


	def selectCellAt(self, pos):
		if self.cellAt(pos).cellType == CellType.Wall or self.cellAt(pos).cellType == CellType.EmptyCell:
			print("Illegal selection.")
			return False

		elif self.cellAt(pos).cellType == CellType.LivingCell:
			self.moves.curX = pos[0]
			self.moves.curY = pos[1]
			self.setCellAt(pos, Cell(CellType.SelectedCell))
			self.isSelected = True
			return True


	def deselectCell(self):
		print("Deselecting", (self.moves.curX, self.moves.curY))
		self.setCellAt((self.moves.curX, self.moves.curY), Cell(CellType.LivingCell))
		self.isSelected = False


	def clearBoard(self):
		self.table = [list(range(self.BoardHeight)) for x in range(self.BoardWidth)]
		self.table = [list(map(lambda x: Cell(CellType.LivingCell), row)) for row in self.table]
		# map(lambda x: print(x), self.table)


	def newEmptyCell(self, x, y):
		self.curSelected = Cell(CellType.EmptyCell)
		self.setCellAt((x, y), self.curSelected)


	def setWalls(self):
		for i in range(3):
			for j in range(3):
				# Bottom left
				self.setCellAt((j, i), Cell(CellType.Wall))
				# Top left
				self.setCellAt((j, -i - 1), Cell(CellType.Wall))
				# Bottom right
				self.setCellAt((-j - 1, i), Cell(CellType.Wall))
				# Top right
				self.setCellAt((-j - 1, -i - 1), Cell(CellType.Wall))


	def getMoves(self, pos):
		moves = list()

		# Checking for a move to 'east'
		if (pos[0] > 1 and self.cellAt((pos[0] - 1, pos[1])).cellType is CellType.LivingCell and
			self.cellAt((pos[0] - 2, pos[1])).cellType is CellType.EmptyCell):
			moves.append(Move(pos, (pos[0] - 2, pos[1])))
		# Checking for a move to 'west'
		if (pos[0] < self.BoardWidth - 2 and self.cellAt((pos[0] + 1, pos[1])).cellType is CellType.LivingCell and
			self.cellAt((pos[0] + 2, pos[1])).cellType is CellType.EmptyCell):
			moves.append(Move(pos, (pos[0] + 2, pos[1])))
		# Checking for a move to 'north'
		if (pos[1] > 1 and self.cellAt((pos[0], pos[1] - 1)).cellType is CellType.LivingCell and
			self.cellAt((pos[0], pos[1] - 2)).cellType is CellType.EmptyCell):
			moves.append(Move(pos, (pos[0], pos[1] - 2)))
		# Checking for a move to 'south'
		if (pos[1] < self.BoardHeight - 2 and self.cellAt((pos[0], pos[1] + 1)).cellType is CellType.LivingCell and
			self.cellAt((pos[0], pos[1] + 2)).cellType is CellType.EmptyCell):
			moves.append(Move(pos, (pos[0], pos[1] + 2)))

		map(lambda x: x.getDirection(), moves)
		return moves
