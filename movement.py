from copy import deepcopy

from cell import CellType, Cell
# from board import Board


class Moves(object):
    """docstring for Moves"""

    def __init__(self, table):
        self.table = table
        self.queueOfMoves = list()
        self.moveId = 0
        self.curMove = None
        self.curX = 0
        self.curY = 0
        self.passedX = None
        self.passedY = None
        self.lastMove = None

    def try_move(self, move, board):
        new_x = move.toPos[0]
        new_y = move.toPos[1]
        self.curX = move.fromPos[0]
        self.curY = move.fromPos[1]

        if self.table.cell_at(move.toPos).cell_type is not CellType.EmptyCell:
            print(move.toPos, " it's not an empty cell. It is ", self.table.cell_at(move.toPos).cell_type)
            return False
        elif abs(self.curX - new_x) == 0 and abs(self.curY - new_y) != 2:
            print("Distance on y is not 2", move)
            return False
        elif abs(self.curX - new_x) != 2 and abs(self.curY - new_y) == 0:
            print("Distance on x is not 2", move)
            return False
        elif abs(self.curX - new_x) != 2 and abs(self.curY - new_y) != 2:
            print("Moving on diagonal", move)
            return False
        elif (new_x > 5 or new_x < 3) and (new_y > 5 or new_y < 3):
            return False
        elif (new_x > 8 or new_x < 0) and (new_y > 8 or new_y < 0):
            return False
        else:
            # print(move.toPos)
            direct = move.get_direction()
            if direct == '':
                return False
            # print('Move: -> ', direct)

            if direct == 'east':
                if self.table.cell_at((new_x - 1, new_y)).cell_type is not CellType.LivingCell:
                    print("Jumping over an empty cell.", move)
                    return False
                self.table.set_cell_at((new_x - 1, new_y), Cell(CellType.PassedCell))
                self.passedX = new_x - 1
                self.passedY = new_y
            elif direct == 'west':
                if self.table.cell_at((new_x + 1, new_y)).cell_type is not CellType.LivingCell:
                    print("Jumping over an empty cell.", move)
                    return False
                self.table.set_cell_at((new_x + 1, new_y), Cell(CellType.PassedCell))
                self.passedX = new_x + 1
                self.passedY = new_y
            elif direct == 'north':
                if self.table.cell_at((new_x, new_y + 1)).cell_type is not CellType.LivingCell:
                    print("Jumping over an empty cell.")
                    return False
                self.table.set_cell_at((new_x, new_y + 1), Cell(CellType.PassedCell))
                self.passedX = new_x
                self.passedY = new_y + 1
            elif direct == 'south':
                if self.table.cell_at((new_x, new_y - 1)).cell_type is not CellType.LivingCell:
                    print("Jumping over an empty cell.")
                    return False
                self.table.set_cell_at((new_x, new_y - 1), Cell(CellType.PassedCell))
                self.passedX = new_x
                self.passedY = new_y - 1

            self.table.deselect_cell()
            self.table.set_cell_at(move.fromPos, Cell(CellType.EmptyCell))
            self.table.aliveCells -= 1
            # board.update()
            if board is not None:
                board.timer.start(board.Speed, board)
            else:
                self.table.set_cell_at((self.passedX, self.passedY), Cell(CellType.EmptyCell))
            self.table.set_cell_at(move.toPos, Cell(CellType.LivingCell))
            self.lastMove = move
            self.queueOfMoves[self.moveId:] = []
            self.moveId += 1
            self.queueOfMoves.append(move)
            # print("Queue (inside try_move[]): ", len(self.queueOfMoves),
            # 			self.queueOfMoves)
            # print(self.table.aliveCells)
            # board.update()
            return True

    def undo(self, board):
        print("Try to undo to", self.moveId - 1)
        if self.moveId > 0:
            self.moveId -= 1
            self.lastMove = self.queueOfMoves[self.moveId - 1]
            move = self.queueOfMoves[self.moveId]
            self.make_move_back(move.reverse(), board)
            print("Queue(undo): ", self.queueOfMoves)
        return

    def make_move_back(self, move, board):
        print("moving back to movement id ", self.moveId)
        self.curX = move.toPos[0]
        self.curY = move.toPos[1]
        self.table.set_cell_at(move.toPos, Cell(CellType.LivingCell))
        self.table.set_cell_at(move.fromPos, Cell(CellType.EmptyCell))

        direct = move.get_direction()
        print('Direction for undoing ->', direct)
        print('Undoing from: ', move.fromPos, ', to: ', move.toPos)

        if direct == 'east':
            self.table.set_cell_at((self.curX - 1, self.curY), Cell(CellType.LivingCell))
        elif direct == 'west':
            self.table.set_cell_at((self.curX + 1, self.curY), Cell(CellType.LivingCell))
        elif direct == 'north':
            self.table.set_cell_at((self.curX, self.curY + 1), Cell(CellType.LivingCell))
        elif direct == 'south':
            self.table.set_cell_at((self.curX, self.curY - 1), Cell(CellType.LivingCell))

        self.table.aliveCells = self.table.get_nr_alive_cells()
        board.msg2Statusbar.emit(str(self.table.aliveCells))
        board.update()
        return

    def redo(self, board):
        print("Try to redo to ", self.moveId + 1)
        if self.moveId < len(self.queueOfMoves):
            self.lastMove = self.queueOfMoves[self.moveId]
            self.moveId += 1
            self.table.set_cell_at(self.lastMove.toPos, Cell(CellType.LivingCell))
            self.curX = self.lastMove.fromPos[0]
            self.curY = self.lastMove.fromPos[1]
            self.table.set_cell_at(self.lastMove.fromPos, Cell(CellType.EmptyCell))

            direct = self.lastMove.get_direction()
            print('Direction for redoing -> ', direct)
            # print('Redoing from: ', self.lastMove.fromPos, ', to: ', self.lastMove.toPos)

            if direct == 'east':
                print("east")
                self.table.set_cell_at((self.curX + 1, self.curY), Cell(CellType.EmptyCell))
            elif direct == 'west':
                print("west")
                self.table.set_cell_at((self.curX - 1, self.curY), Cell(CellType.EmptyCell))
            elif direct == 'south':
                print('south')
                self.table.set_cell_at((self.curX, self.curY + 1), Cell(CellType.EmptyCell))
            elif direct == 'north':
                print('north')
                self.table.set_cell_at((self.curX, self.curY - 1), Cell(CellType.EmptyCell))

            self.table.aliveCells = self.table.get_nr_alive_cells()
            board.msg2Statusbar.emit(str(self.table.aliveCells))
            board.update()
            # print("Queue(redo): ", self.queueOfMoves)
        return

    def get_available_moves(self):
        av_moves = list()
        for x in range(self.table.TableHeight):
            for y in range(self.table.TableWidth):
                if self.table.cell_at((x, y)).cell_type is CellType.LivingCell:
                    av_moves.extend(self.table.get_moves((x, y)))
        # print(av_moves)
        return av_moves

    def get_copy(self):
        copy = Moves(self.table)
        copy.queueOfMoves = deepcopy(self.queueOfMoves)
        copy.curMove = self.curMove
        copy.curX = self.curX
        copy.curY = self.curY
        copy.moveId = self.moveId
        copy.lastMove = self.lastMove
        copy.passedY = self.passedY
        copy.passedX = self.passedX
        return copy


class Move(object):
    """docstring for Movement"""

    def __init__(self, fromPos, toPos):
        self.fromPos = fromPos
        self.toPos = toPos
        self.step = (self.fromPos, self.toPos)
        self.direction = ''

    def __repr__(self):
        return '{Movement: [from: ' + str(self.fromPos) + ', to: ' + str(self.toPos) + ']}'

    def set_to_pos(self, toPos):
        self.toPos = toPos

    def reverse(self):
        return Move(self.toPos, self.fromPos)

    def get_direction(self):
        if self.toPos[0] == self.fromPos[0]:
            if self.toPos[1] > self.fromPos[1]:
                self.direction = 'south'
            elif self.toPos[1] < self.fromPos[1]:
                self.direction = 'north'
        elif self.toPos[1] == self.fromPos[1]:
            if self.toPos[0] > self.fromPos[0]:
                self.direction = 'east'
            if self.toPos[0] < self.fromPos[0]:
                self.direction = 'west'
        else:
            self.direction = ''
        return self.direction

    def get_copy(self):
        copy = Move(self.fromPos, self.toPos)
        copy.get_direction()
        return copy
