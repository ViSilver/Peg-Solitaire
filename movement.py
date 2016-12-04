__author__ = 'Vi'


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

    def tryMove(self, move):
        newX = move.toPos[0]
        newY = move.toPos[1]

        if self.table.cellAt(move.toPos).cellType is not CellType.EmptyCell:
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
            print(move.toPos)
            direct = move.getDirection()
            if direct == '':
                return False
            print('Move: -> ', direct)

            if direct == 'east':
                if self.table.cellAt((newX - 1, newY)).cellType is not CellType.LivingCell:
                    print("Jumping over an empty cell.")
                    return False
                self.table.setCellAt((newX - 1, newY), Cell(CellType.PassedCell))
                self.passedX = newX - 1
                self.passedY = newY
            elif direct == 'west':
                if self.table.cellAt((newX + 1, newY)).cellType is not CellType.LivingCell:
                    print("Jumping over an empty cell.")
                    return False
                self.table.setCellAt((newX + 1, newY), Cell(CellType.PassedCell))
                self.passedX = newX + 1
                self.passedY = newY
            elif direct == 'north':
                if self.table.cellAt((newX, newY + 1)).cellType is not CellType.LivingCell:
                    print("Jumping over an empty cell.")
                    return False
                self.table.setCellAt((newX, newY + 1), Cell(CellType.PassedCell))
                self.passedX = newX
                self.passedY = newY + 1
            elif direct == 'south':
                if self.table.cellAt((newX, newY - 1)).cellType is not CellType.LivingCell:
                    print("Jumping over an empty cell.")
                    return False
                self.table.setCellAt((newX, newY - 1), Cell(CellType.PassedCell))
                self.passedX = newX
                self.passedY = newY - 1

            self.table.deselectCell()
            self.table.setCellAt(move.fromPos, Cell(CellType.EmptyCell))
            self.table.aliveCells -= 1
            # board.update()
            # self.timer.start(self.board.Speed, self.board)  							# Comment for no animation
            self.table.setCellAt((self.passedX, self.passedY), Cell(CellType.EmptyCell))  # Comment for animation
            self.table.setCellAt(move.toPos, Cell(CellType.LivingCell))
            self.lastMove = move
            self.queueOfMoves[self.moveId:] = []
            self.moveId += 1
            self.queueOfMoves.append(move)
            print("Queue (inside tryMove): ", self.queueOfMoves)
            # board.update()
            return True

    def undo(self, board):
        print("Try to undo to", self.moveId - 1)
        if self.moveId > 0:
            self.moveId -= 1
            self.lastMove = self.queueOfMoves[self.moveId - 1]
            move = self.queueOfMoves[self.moveId]
            self.makeMoveBack(move.reverse(), board)
            print("Queue(undo): ", self.queueOfMoves)
        return

    def makeMoveBack(self, move, board):
        print("moving back to movement id ", self.moveId)
        self.curX = move.toPos[0]
        self.curY = move.toPos[1]
        self.table.setCellAt(move.toPos, Cell(CellType.LivingCell))
        self.table.setCellAt(move.fromPos, Cell(CellType.EmptyCell))

        direct = move.getDirection()
        print('Direction for undoing ->', direct)
        print('Undoing from: ', move.fromPos, ', to: ', move.toPos)

        if direct == 'east':
            self.table.setCellAt((self.curX - 1, self.curY), Cell(CellType.LivingCell))
        elif direct == 'west':
            self.table.setCellAt((self.curX + 1, self.curY), Cell(CellType.LivingCell))
        elif direct == 'north':
            self.table.setCellAt((self.curX, self.curY + 1), Cell(CellType.LivingCell))
        elif direct == 'south':
            self.table.setCellAt((self.curX, self.curY - 1), Cell(CellType.LivingCell))

        board.update()
        return

    def redo(self, board):
        print("Try to redo to ", self.moveId + 1)
        if self.moveId < len(self.queueOfMoves):
            self.lastMove = self.queueOfMoves[self.moveId]
            self.moveId += 1
            self.table.setCellAt(self.lastMove.toPos, Cell(CellType.LivingCell))
            self.curX = self.lastMove.fromPos[0]
            self.curY = self.lastMove.fromPos[1]
            self.table.setCellAt(self.lastMove.fromPos, Cell(CellType.EmptyCell))

            direct = self.lastMove.getDirection()
            print('Direction for redoing -> ', direct)
            print('Redoing from: ', self.lastMove.fromPos, ', to: ', self.lastMove.toPos)

            if direct == 'east':
                print("east")
                self.table.setCellAt((self.curX + 1, self.curY), Cell(CellType.EmptyCell))
            elif direct == 'west':
                print("west")
                self.table.setCellAt((self.curX - 1, self.curY), Cell(CellType.EmptyCell))
            elif direct == 'south':
                print('south')
                self.table.setCellAt((self.curX, self.curY + 1), Cell(CellType.EmptyCell))
            elif direct == 'north':
                print('north')
                self.table.setCellAt((self.curX, self.curY - 1), Cell(CellType.EmptyCell))

            board.update()
            print("Queue(redo): ", self.queueOfMoves)
        return

    def getAvailableMoves(self):
        avMoves = list()
        for x in range(self.table.TableHeight):
            for y in range(self.table.TableWidth):
                if self.table.cellAt((x, y)).cellType is CellType.LivingCell:
                    avMoves.extend(self.table.getMoves((x, y)))
        print(avMoves)
        return avMoves


class Move(object):
    """docstring for Movement"""

    def __init__(self, fromPos, toPos):
        self.fromPos = fromPos
        self.toPos = toPos
        self.step = (self.fromPos, self.toPos)
        self.direction = ''

    def __repr__(self):
        return str((self.fromPos, self.toPos))

    def setToPos(self, toPos):
        self.toPos = toPos

    def reverse(self):
        newMove = Move(self.toPos, self.fromPos)
        return newMove

    def getDirection(self):
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
