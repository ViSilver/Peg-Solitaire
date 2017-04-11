__author__ = 'Vi'


class CellType(object):
    """docstring for CellType"""

    EmptyCell = 0
    PassedCell = 1
    LivingCell = 2
    SelectedCell = 3
    Wall = 4


class Cell(object):
    """docstring for Cell"""

    def __init__(self, cell_type):
        self.cell_type = cell_type

    def __repr__(self):
        return str(self.cell_type)

    def cell(self):
        return self.cell_type