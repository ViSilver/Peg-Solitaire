__author__ = 'Vi'

# from board import Move
from node import Node

from queue import Queue, LifoQueue
from threading import Thread
from collections import deque
import time
import heapq



class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]


    def empty(self):
        if self._queue is []:
            return True
        else:
            return False


class Solver(object):
    def __init__(self, table):
        self.root = Node(table)
        self.solution = list()
        return

    def solve(self):
        curTime = time.time()
        index = 0
        pQueue = PriorityQueue()
        self.root.weight = self.root.computeWeight()
        pQueue.push(self.root, self.root.weight)
        while not pQueue.empty():
            index += 1
            print(index)
            current = pQueue.pop()
            print(current.weight)
            children = current.getChildren()
            for child in children:
                if child.table.aliveCells == 1:
                    self.solution.append(child)
                    print('##################', time.time() - curTime)
                    return
                elif len(child.availableMoves) > 0:
                    pQueue.push(child, child.weight)
                # print(child.availableMoves)
                # time.sleep(5)

        if len(self.solution) == 0:
            print('There are no solution for given configuration.')
        else:
            print('There are ', len(self.solution),
                  ' solutions for given configuration.')


class Solver1(object):
    def __init__(self, table):
        self.root = Node(table)
        self.solution = list()
        self.moveId = table.moves.moveId
        return

    def solve(self):
        curTime = time.time()
        index = 0
        stack = list()
        # self.root.weight = self.root.computeWeight()
        stack.append(self.root)
        while len(stack) > 0:
            index += 1
            print(index)
            current = stack.pop()

            if current.table.aliveCells == 1:
                self.solution.append(current)
                print('##################', time.time() - curTime)
                return

            children = current.getChildren()

            for child in children:
                if len(child.availableMoves) > 0:
                    stack.append(child)
                # print(child.availableMoves)
                # time.sleep(5)

        if len(self.solution) == 0:
            print('There are no solution for the given configuration.')
        else:
            print('There are ', len(self.solution),
                  ' solutions for given configuration.')

    def showSolution(self, board):
        example = self.solution[0]
        for move in example.table.moves.queueOfMoves:
            time.sleep(1)
            board.table.moves.tryMove(move, None)
            board.update()
            # time.sleep(1)
            board.timer.start(board.Speed, board)


    def showNext(self, board):
        move = self.solution[0].table.moves.queueOfMoves[self.moveId]
        board.table.moves.tryMove(move, None)
        board.update()
        self.moveId += 1




