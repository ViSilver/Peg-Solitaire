#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Artificial Intelligence - BIE-ZUM, CVUT

Course Project

author: Victor Turcanu
last edited: 11/06/2015
"""


import sys
from PyQt5.QtWidgets import (QMainWindow, QDesktopWidget, QApplication,
	QPushButton)
from PyQt5.QtCore import ( QRect, QSize)

from board import Board
from node import Node
from solver import Solver1, Solver


class Solitaire(QMainWindow):
	"""docstring for Solitaire"""

	def __init__(self):
		super().__init__()

		self.initUI()


	def initUI(self):
		self.sboard = Board(self)

		self.statusbar = self.statusBar()
		self.sboard.msg2Statusbar[str].connect(self.statusbar.showMessage)

		self.resize(315, 250)
		self.setMinimumSize(QSize(350, 265))
		self.setMaximumSize(QSize(350, 265))
		self.sboard.setMinimumSize(QSize(240, 240))
		self.sboard.setMaximumSize(QSize(240, 240))

		self.center()
		self.setWindowTitle('Peg Solitaire')

		self.sboard.start()

		self.undoButton = QPushButton(self)
		self.undoButton.setGeometry(QRect(250, 10, 80, 40))
		self.undoButton.setObjectName("undoButton")
		self.undoButton.setText("Undo")
		self.undoButton.clicked.connect(self.buttonClicked)

		self.redoButton = QPushButton(self)
		self.redoButton.setGeometry(QRect(250, 60, 80, 40))
		self.redoButton.setObjectName("redoButton")
		self.redoButton.setText("Redo")
		self.redoButton.clicked.connect(self.buttonClicked)

		self.solverButton = QPushButton(self)
		self.solverButton.setGeometry(QRect(250, 110, 80, 40))
		self.solverButton.setObjectName("solveButton")
		self.solverButton.setText("Solve")
		self.solverButton.clicked.connect(self.buttonClicked)

		self.showSolutionButton = QPushButton(self)
		self.showSolutionButton.setGeometry(QRect(250, 160, 100, 40))
		self.showSolutionButton.setObjectName("showSolutionButton")
		self.showSolutionButton.setText("Show Sol")
		self.showSolutionButton.clicked.connect(self.buttonClicked)

		self.show()


	def center(self):
		screen = QDesktopWidget().screenGeometry()
		size = self.geometry()
		self.move((screen.width()-size.width())/2,
			(screen.height()-size.height())/2)

	def buttonClicked(self):
		sender = self.sender()

		if sender == self.undoButton:
			self.sboard.table.moves.undo(self.sboard)
		elif sender == self.redoButton:
			self.sboard.table.moves.redo(self.sboard)
		elif sender == self.solverButton:
			# print(Node(self.sboard.table).availableMoves)
			self.solver = Solver1(self.sboard.table)
			self.solver.solve()
		elif sender == self.showSolutionButton:
			self.solver.showNext(self.sboard)
		return



def main():
	app = QApplication([])
	solitaire = Solitaire()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()

