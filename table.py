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
        self.clear_board()
        self.set_walls()
        self.new_empty_cell(4, 4)
        # self.set_testing_env()
        self.aliveCells = self.get_nr_alive_cells()
        self.moves = Moves(self)

    def cell_at(self, pos):
        return self.grid[pos[0]][pos[1]]

    def set_cell_at(self, pos, cell):
        self.grid[pos[0]][pos[1]] = cell

    def clear_board(self):
        self.grid = [list(range(self.TableHeight)) for x in range(self.TableWidth)]
        self.grid = [list(map(lambda x: Cell(CellType.LivingCell), row)) for row in self.grid]

    def select_cell_at(self, pos):
        if self.cell_at(pos).cell_type == CellType.Wall or self.cell_at(pos).cell_type == CellType.EmptyCell:
            # print("Illegal selection.")
            return False
        elif self.cell_at(pos).cell_type == CellType.LivingCell:
            self.moves.curX = pos[0]
            self.moves.curY = pos[1]
            self.set_cell_at(pos, Cell(CellType.SelectedCell))
            self.isSelected = True
            return True

    def deselect_cell(self):
        # print("Deselecting", (self.moves.curX, self.moves.curY))
        self.set_cell_at((self.moves.curX, self.moves.curY), Cell(CellType.LivingCell))
        self.isSelected = False

    def new_empty_cell(self, x, y):
        self.curSelected = Cell(CellType.EmptyCell)
        self.set_cell_at((x, y), self.curSelected)

    def set_walls(self):
        for i in range(3):
            for j in range(3):
                # Bottom left
                self.set_cell_at((j, i), Cell(CellType.Wall))
                # Top left
                self.set_cell_at((j, -i - 1), Cell(CellType.Wall))
                # Bottom right
                self.set_cell_at((-j - 1, i), Cell(CellType.Wall))
                # Top right
                self.set_cell_at((-j - 1, -i - 1), Cell(CellType.Wall))

        for i in range(9):
            self.set_cell_at((0, i), Cell(CellType.Wall))
            self.set_cell_at((self.TableWidth - 1, i), Cell(CellType.Wall))
            self.set_cell_at((i, 0), Cell(CellType.Wall))
            self.set_cell_at((i, self.TableHeight - 1), Cell(CellType.Wall))

    def getMoves(self, pos):
        moves = list()

        # Checking for a move to 'east'
        if (pos[0] > 1 and self.cell_at((pos[0] - 1, pos[1])).cell_type is CellType.LivingCell
                    and self.cell_at((pos[0] - 2, pos[1])).cell_type is CellType.EmptyCell):
            moves.append(Move(pos, (pos[0] - 2, pos[1])))

        # Checking for a move to 'west'
        if (pos[0] < self.TableWidth - 2 and self.cell_at((pos[0] + 1, pos[1])).cell_type is CellType.LivingCell
                    and self.cell_at((pos[0] + 2, pos[1])).cell_type is CellType.EmptyCell):
            moves.append(Move(pos, (pos[0] + 2, pos[1])))

        # Checking for a move to 'north'
        if (pos[1] > 1 and self.cell_at((pos[0], pos[1] - 1)).cell_type is CellType.LivingCell
                    and self.cell_at((pos[0], pos[1] - 2)).cell_type is CellType.EmptyCell):
            moves.append(Move(pos, (pos[0], pos[1] - 2)))

        # Checking for a move to 'south'
        if (pos[1] < self.TableHeight - 2 and self.cell_at((pos[0], pos[1] + 1)).cell_type is CellType.LivingCell
            and self.cell_at((pos[0], pos[1] + 2)).cell_type is CellType.EmptyCell):
            moves.append(Move(pos, (pos[0], pos[1] + 2)))

        map(lambda x: x.get_direction(), moves)
        return moves

    def get_nr_alive_cells(self):
        counter = 0
        for row in self.grid:
            for cell in row:
                if cell.cell_type is CellType.LivingCell:
                    counter += 1
        return counter

    def copy(self):
        copy = Table()

        for x in range(self.TableWidth):
            for y in range(self.TableHeight):
                copy.grid[x][y] = self.grid[x][y]

        copy.aliveCells = self.aliveCells
        copy.moves = self.moves.get_copy()
        return copy

    def set_testing_env(self):
        for x in range(self.TableWidth):
            for y in range(self.TableHeight):
                self.set_cell_at((x, y), Cell(CellType.EmptyCell))
        self.set_walls()
        self.set_cell_at((3, 4), Cell(CellType.LivingCell))
        self.set_cell_at((4, 4), Cell(CellType.LivingCell))
        self.set_cell_at((6, 4), Cell(CellType.LivingCell))

    def print_grid(self):
        for x in self.grid:
            print(x)