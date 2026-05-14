from zon_object_types import *
from formatting import *

import sys

import sys
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import (
	QApplication,
	QHBoxLayout,
	QMainWindow,
	QPushButton,
	QStackedLayout,
	QVBoxLayout,
	QWidget,
	QLineEdit,
)

class Color(QWidget):
	def __init__(self, color):
		super().__init__()
		self.setAutoFillBackground(True)

		palette = self.palette()
		palette.setColor(QPalette.ColorRole.Window, QColor(color))
		self.setPalette(palette)



class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("My App")

		pagelayout = QVBoxLayout()

		self.addInputLine("test", pagelayout)
		self.addInputLine("test1", pagelayout)
		self.addInputLine("test2", pagelayout)
		self.addInputLine("test3", pagelayout)
		self.addInputLine("test4", pagelayout)

		widget = QWidget()
		widget.setLayout(pagelayout)
		self.setCentralWidget(widget)
		pagelayout.addWidget(Color("red"))

	def text_changed(self, name, parentButton):
		print("Selection changed"+ name)
		txtInput = QLineEdit()
		txtInput.setPlaceholderText("extra")
		parentButton.addWidget(txtInput)

	def addInputLine(self, Name, Layout):

		#self.addArrayZonInput(Name, Layout)
	
	
	def addArrayZonInput(self, defaultText, baseParentLayout):
		txtInputsLayout = QHBoxLayout()
		self.createSingleArrayInput(defaultText, txtInputsLayout)
		
		baseParentLayout.addLayout(txtInputsLayout)



	def checkArrayZonChildren(self, defaultText, parentLayout):
		
		for i in range(parentLayout.count()):
			childButton = parentLayout.itemAt(0)
			print(childButton)
			if (childButton.text() == "") and (i != parentLayout.count()):
				parentLayout.removeWidget(childButton)
				print("removeOldthings")
			if (childButton.text() != "") and (i == parentLayout.count()):
				print("attempt to create")
				self.createSingleArrayInput(defaultText, parentLayout)
	
	def createSingleArrayInput(self, defaultText, parentLayout):
		txtInput = QLineEdit()
		txtInput.setPlaceholderText(defaultText)
		txtInput.textChanged.connect(lambda: self.checkArrayZonChildren(defaultText, parentLayout))
		parentLayout.addWidget(txtInput)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()



filename = "test4"
filepath = "Output/" + filename + ".zig.zon"



textOBJ = baseZonObject()
textOBJ.children = [zonValue(), zonObject(), zonArray()]
actualText = textOBJ.writeWithChildren()

with open(filepath, "w") as f:
	for line in actualText:
		f.write(line)
		f.write('\n')

ItemZonFormat = baseZonObject()
readFormatFile(ItemZonFormat)

