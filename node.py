__author__ = 'Vi'


from movement import Move
from board import Board
from cell import CellType

import copy


class Node(object):

    def __init__(self, table):
        self.children = list()

        self.table = table.copy()
        self.table.moves.table = self.table

        for x in range(table.TableWidth):
            for y in range(table.TableWidth):
                self.table.grid[x][y] = table.grid[x][y]

        self.availableMoves = self.table.moves.get_available_moves()

        if self.availableMoves is []:
            self.alive = False
        else:
            self.alive = True

        self.weight = 0

    def __cmp__(self, other):
        if self.weight < other.weight:
            return False
        else:
            return True

    def __repr__(self):
        return '{Node: ' + str(self.availableMoves) + '}'

    def get_status(self):
        if self.alive:
            for child in self.children:
                if child.availableMoves is not [] and child.get_status() is True:
                    self.alive = True
        else:
            self.alive = False
        return self.alive

    # need to make it asynchronous
    def get_children(self):
        for move in self.availableMoves:
            child = Node(self.table.copy())
            child.table.moves.try_move(move, None)
            child.availableMoves = child.table.moves.get_available_moves()
            # print(child.table.get_nr_alive_cells())
            # child.weight = child.compute_weight()
            self.children.append(child)
        return self.children

    def async_get_children(self):
        number_of_threads = 5
        division_step = len(self.availableMoves) // number_of_threads
        if division_step > 1:
            # print(division_step)
            from concurrent.futures import ThreadPoolExecutor as Pool
            pool = Pool(max_workers=number_of_threads)

            chunks = [self.availableMoves[x:x + division_step] for x in range(0, len(self.availableMoves), division_step)]

            for movements in chunks:
                future = pool.submit(self.helper_method, self.table.copy(), movements)
                future.add_done_callback(self.append_callback)
            return self.children
        else:
            return self.get_children()

    @staticmethod
    def helper_method(table, movements):
        children = []
        for movement in movements:
            child = Node(table)
            child.table.moves.try_move(movement, None)
            child.availableMoves = child.table.moves.get_available_moves()
            children.append(child)
        return children

    def append_callback(self, future):
        self.children.extend(future.result())

    def compute_weight(self):
        value = 0
        a = 0
        b = 0

        for x in range(self.table.TableWidth):
            for y in range(self.table.TableHeight):
                if self.table.cell_at((x, y)).cell_type is CellType.LivingCell:
                    if x <= (self.table.TableWidth - 1) / 2:
                        a = x
                    else:
                        a = self.table.TableWidth - x - 1
                    if y <= (self.table.TableHeight - 1) / 2:
                        b = y
                    else:
                        b = self.table.TableHeight - y - 1
                    value += (a * b)
        return value / (self.table.aliveCells + value)
