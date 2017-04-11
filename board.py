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
        self.init_board()

    def init_board(self):
        self.timer = QBasicTimer()
        self.table = Table()
        self.setFocusPolicy(Qt.StrongFocus)
        self.isStarted = False
        self.isPaused = False

    def square_width(self):
        return self.contentsRect().width() // Table.TableWidth

    def square_height(self):
        return self.contentsRect().height() // Table.TableHeight

    def start(self):
        if self.isPaused:
            return
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

        boardTop = rect.bottom() - Table.TableHeight * self.square_height()

        for i in range(Table.TableHeight):
            for j in range(Table.TableWidth):
                cell = self.table.cell_at((j, i))
                self.draw_square(painter, rect.left() + j * self.square_width(),
                                 boardTop + i * self.square_height(), cell)

        # Paint event after the mouse event

    def draw_square(self, painter, x, y, cell):
        colorTable = [0xEEEEEE, 0x505050, 0xAAAAAA, 0xDADADA, 0x444444]

        color = QColor(colorTable[cell.cell_type])
        painter.fillRect(x + 1, y + 1, self.square_width() - 2,
                         self.square_height() - 2, color)

        painter.setPen(color.lighter())
        painter.drawLine(x, y + self.square_height() - 1, x, y)
        painter.drawLine(x, y, x + self.square_width() - 1, y)

        painter.setPen(color.darker())
        painter.drawLine(x + 1, y + self.square_height() - 1,
                         x + self.square_width() - 1, y + self.square_height() - 1)
        painter.drawLine(x + self.square_width() - 1,
                         y + self.square_height() - 1, x + self.square_width() - 1, y + 1)

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
                self.table.set_cell_at((self.table.moves.passedX, self.table.moves.passedY), Cell(CellType.EmptyCell))
            self.msg2Statusbar.emit(str(self.table.aliveCells))
            self.timer.stop()
            self.update()
        return

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos = ((event.pos().x() - 2) // self.square_width(), (event.pos().y() - 8) // self.square_height())

            if self.table.cell_at(pos).cell_type == CellType.Wall:
                print("Illegal selection of a wall.")
                return

            if self.table.isSelected:
                if pos[0] == self.table.moves.curX and pos[1] == self.table.moves.curY:
                    print("Trying to select the same cell")
                    self.table.deselect_cell()
                    self.update()
                    return

                self.table.moves.curMove.set_to_pos(pos)

                if not self.table.moves.try_move(self.table.moves.curMove, self):
                    # print("Impossible to move")
                    self.table.deselect_cell()
                    self.update()
                    return

                self.msg2Statusbar.emit(str(self.table.aliveCells))
                self.update()

            else:
                self.table.select_cell_at(pos)
                self.table.moves.curMove = Move(pos, None)
                self.update()

            # print(pos)
        else:
            super(Board, self).mousePressEvent(event)
        return
