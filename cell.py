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


	def __init__(self):

		# self.cellType = CellType.EmptyCell
		self.setCell(CellType.EmptyCell)


	def cell(self):
		return self.cellType


	def setCell(self, cell):
		self.cellType = cell