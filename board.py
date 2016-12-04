__author__ = 'Vi'


from PyQt5.QtGui import (QPainter, QColor)
from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import (Qt, QBasicTimer, pyqtSignal)
from cell import CellType, Cell
from movement import Move, Moves
from table import Table


class Board(QFrame):
	"""docstring for Board"""

	msg2Statusbar = pyqtSignal(str)
	Speed = 200

	def __init__(self, parent):
		super().__init__(parent)
		self.initBoard()


	def initBoard(self):
		self.timer = QBasicTimer()
		self.table = Table()
		self.setFocusPolicy(Qt.StrongFocus)
		self.isStarted = False
		self.isPaused = False


	def squareWidth(self):
		return self.contentsRect().width() // Table.TableWidth


	def squareHeight(self):
		return self.contentsRect().height() // Table.TableHeight


	def start(self):
		if self.isPaused:
			return

		self.table.isStarted = True
		self.table.clearBoard()

		self.table.newEmptyCell(4, 4)
		self.table.setWalls()
		# self.table.setTestingEnv()
		self.table.aliveCells = self.table.getNrAliveCells()
		self.msg2Statusbar.emit(str(self.table.aliveCells))
		self.timer.start(Board.Speed, self)


	def pause(self):
		self.isPaused = not self.isPaused

		if self.isPaused:
			self.timer.stop()
			self.msg2Statusbar.emit("Paused")
		else:
			self.timer.start(Board.Speed, self)
			self.msg2Statusbar.emit(str(self.table.aliveCells))

		self.update()


	def paintEvent(self, event):
		painter = QPainter(self)
		rect = self.contentsRect()

		boardTop = rect.bottom() - Table.TableHeight * self.squareHeight()

		for i in range(Table.TableHeight):
			for j in range(Table.TableWidth):
				cell = self.table.cellAt((j, i))
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
			if self.table.moves.passedX is not None and self.table.moves.passedY is not None:
				self.table.setCellAt((self.table.moves.passedX, self.table.moves.passedY), Cell(CellType.EmptyCell))
			self.msg2Statusbar.emit(str(self.table.aliveCells))
			self.timer.stop()
			self.update()
		return

	def mousePressEvent(self, event):
		if event.button() == Qt.LeftButton:
			pos = ((event.pos().x() - 2) // self.squareWidth(), (event.pos().y() - 8) // self.squareHeight())

			if self.table.cellAt(pos).cellType == CellType.Wall:
				print("Illegal selection of a wall.")
				return

			if self.table.isSelected:
				if pos[0] == self.table.moves.curX and pos[1] == self.table.moves.curY:
					print("Trying to select the same cell")
					self.table.deselectCell()
					self.update()
					return

				self.table.moves.curMove.setToPos(pos)

				if not self.table.moves.tryMove(self.table.moves.curMove, self):
					# print("Impossible to move")
					self.table.deselectCell()
					self.update()
					return

				self.msg2Statusbar.emit(str(self.table.aliveCells))
				self.update()

			else:
				self.table.selectCellAt(pos)
				self.table.moves.curMove = Move(pos, None)
				self.update()

			# print(pos)
		else:
			super(Board, self).mousePressEvent(event)
		return
