__author__ = 'Vi'

import pprint

from movement import Move, Moves
from cell import Cell, CellType


class Table(object):

    TableWidth = 9
    TableHeight = 9

    def __init__(self):
        self.isSelected = False
        self.grid = list()
        self.clearBoard()
        self.setWalls()
        self.newEmptyCell(4, 4)
        # self.setTestingEnv()
        self.aliveCells = self.getNrAliveCells()
        self.moves = Moves(self)

    def cellAt(self, pos):
        return self.grid[pos[0]][pos[1]]

    def setCellAt(self, pos, cell):
        self.grid[pos[0]][pos[1]] = cell

    def clearBoard(self):
        self.grid = [list(range(self.TableHeight)) for x in range(self.TableWidth)]
        self.grid = [list(map(lambda x: Cell(CellType.LivingCell), row)) for row in self.grid]

    def selectCellAt(self, pos):
        if self.cellAt(pos).cellType == CellType.Wall or self.cellAt(pos).cellType == CellType.EmptyCell:
            # print("Illegal selection.")
            return False
        elif self.cellAt(pos).cellType == CellType.LivingCell:
            self.moves.curX = pos[0]
            self.moves.curY = pos[1]
            self.setCellAt(pos, Cell(CellType.SelectedCell))
            self.isSelected = True
            return True

    def deselectCell(self):
        # print("Deselecting", (self.moves.curX, self.moves.curY))
        self.setCellAt((self.moves.curX, self.moves.curY), Cell(CellType.LivingCell))
        self.isSelected = False

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

        for i in range(9):
            self.setCellAt((0, i), Cell(CellType.Wall))
            self.setCellAt((self.TableWidth - 1, i), Cell(CellType.Wall))
            self.setCellAt((i, 0), Cell(CellType.Wall))
            self.setCellAt((i, self.TableHeight - 1), Cell(CellType.Wall))

    def getMoves(self, pos):
        moves = list()

        # Checking for a move to 'east'
        if (pos[0] > 1 and self.cellAt((pos[0] - 1, pos[1])).cellType is CellType.LivingCell
                    and self.cellAt((pos[0] - 2, pos[1])).cellType is CellType.EmptyCell):
            moves.append(Move(pos, (pos[0] - 2, pos[1])))

        # Checking for a move to 'west'
        if (pos[0] < self.TableWidth - 2 and self.cellAt((pos[0] + 1, pos[1])).cellType is CellType.LivingCell
                    and self.cellAt((pos[0] + 2, pos[1])).cellType is CellType.EmptyCell):
            moves.append(Move(pos, (pos[0] + 2, pos[1])))

        # Checking for a move to 'north'
        if (pos[1] > 1 and self.cellAt((pos[0], pos[1] - 1)).cellType is CellType.LivingCell
                    and self.cellAt((pos[0], pos[1] - 2)).cellType is CellType.EmptyCell):
            moves.append(Move(pos, (pos[0], pos[1] - 2)))

        # Checking for a move to 'south'
        if (pos[1] < self.TableHeight - 2 and self.cellAt((pos[0], pos[1] + 1)).cellType is CellType.LivingCell
            and self.cellAt((pos[0], pos[1] + 2)).cellType is CellType.EmptyCell):
            moves.append(Move(pos, (pos[0], pos[1] + 2)))

        map(lambda x: x.getDirection(), moves)
        return moves

    def getNrAliveCells(self):
        counter = 0
        for row in self.grid:
            for cell in row:
                if cell.cellType is CellType.LivingCell:
                    counter += 1
        return counter

    def copy(self):
        copy = Table()

        for x in range(self.TableWidth):
            for y in range(self.TableHeight):
                copy.grid[x][y] = self.grid[x][y]

        copy.aliveCells = self.aliveCells
        copy.moves = self.moves.getCopy()
        return copy

    def setTestingEnv(self):
        for x in range(self.TableWidth):
            for y in range(self.TableHeight):
                self.setCellAt((x, y), Cell(CellType.EmptyCell))
        self.setWalls()
        self.setCellAt((3, 4), Cell(CellType.LivingCell))
        self.setCellAt((4, 4), Cell(CellType.LivingCell))
        self.setCellAt((6, 4), Cell(CellType.LivingCell))

    def print_grid(self):
        for x in self.grid:
            print(x)