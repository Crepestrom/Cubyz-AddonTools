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
	QLabel,
)

class Color(QWidget):
	def __init__(self, color):
		super().__init__()
		self.setAutoFillBackground(True)

		palette = self.palette()
		palette.setColor(QPalette.ColorRole.Window, QColor(color))
		self.setPalette(palette)



class MainWindow(QMainWindow):
	def __init__(self, givenFormat):
		super().__init__()
		self.setWindowTitle("My App")

		editorLayout = QVBoxLayout()

		self.readFormat(givenFormat, editorLayout)

		widget = QWidget()
		widget.setLayout(editorLayout)
		self.setCentralWidget(widget)
		editorLayout.addWidget(Color("red"))

	def readFormat(self, givenFormat, baseParentLayout):
		for child in givenFormat:
			if isinstance(child, zonValue):
				self.addZonValueInput(child.name, baseParentLayout, child.value)
			elif isinstance(child, zonArray):
				print()
				self.addZonArrayInput(child.name, baseParentLayout, child.children[0])

	def addZonValueInput(self, name, baseParentLayout, defaultText):
		txtInputsLayout = QHBoxLayout()
		
		txtInput = QLineEdit()
		txtInput.setPlaceholderText(defaultText)
		txtInputsLayout.addWidget(txtInput)

		lineLayout = QHBoxLayout()#item 1 is always the actual value object(s)
		namelabel = QLabel("." + name + " = ")
		lineLayout.addWidget(namelabel)
		lineLayout.addLayout(txtInputsLayout)

		baseParentLayout.addLayout(lineLayout)

	def addZonArrayInput(self, defaultText, baseParentLayout, name):
		txtInputsLayout = QHBoxLayout()
		self.createSingleArrayInput(defaultText, txtInputsLayout)
		
		lineLayout = QHBoxLayout()#item 1 is always the actual value object(s)
		namelabel = QLabel("." + name + " = ")
		lineLayout.addWidget(namelabel)
		lineLayout.addLayout(txtInputsLayout)

		baseParentLayout.addLayout(lineLayout)
	
	# end of button aditions

	
	def checkArrayZonChildren(self, defaultText, parentLayout):
		
		widgetsRemovalList = []

		for i in range(parentLayout.count()):
			childButton = parentLayout.itemAt(i).widget()
			print(i)
			if (childButton.text() == "") and (i + 1 != parentLayout.count()):
				widgetsRemovalList.append(childButton)
				print("removeOldthings")
			elif (childButton.text() != "") and (i + 1 == parentLayout.count()):
				print("attempt to create")
				self.createSingleArrayInput(defaultText, parentLayout)
		
		for widget in widgetsRemovalList:
			widget.deleteLater()
	
	def createSingleArrayInput(self, defaultText, parentLayout):
		txtInput = QLineEdit()
		txtInput.setPlaceholderText(defaultText)
		txtInput.textChanged.connect(lambda: self.checkArrayZonChildren(defaultText, parentLayout))
		parentLayout.addWidget(txtInput)





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

print("running app")

app = QApplication(sys.argv)
window = MainWindow(ItemZonFormat.children)
window.show()
app.exec()

