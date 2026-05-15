from zon_object_types import *

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


def writeGivenZonObjectToFile(filepath, zonObject):
	
	actualText = zonObject.writeWithChildren()
	print(actualText)
	with open(filepath, "w") as f:
		for line in actualText:
			f.write(line)
			f.write('\n')

class MainWindow(QMainWindow):
	def __init__(self, givenFormat):
		super().__init__()
		self.setWindowTitle("My App")
		
		self.editorVarsList = []
		editorVarsLayout = QVBoxLayout()
		self.readFormat(givenFormat, editorVarsLayout)

		editorLayout = QVBoxLayout()
		editorLayout.addLayout(editorVarsLayout)
		
		self.filename = "test4" # define this here so it could be changed at another time
		saveZonButton = QPushButton("test")
		saveZonButton.pressed.connect(lambda: self.writeZonUiToFile(self.filename, self.readEditorOutputZon()))
		editorLayout.addWidget(saveZonButton)
		widget = QWidget()
		widget.setLayout(editorLayout)
		self.setCentralWidget(widget)

	def writeZonUiToFile(self, fileName, zonObject):
		filepath = "Output/" + fileName + ".zig.zon"
		writeGivenZonObjectToFile(filepath, zonObject)

	def readFormat(self, givenFormat, baseParentLayout):
		for child in givenFormat:
			if isinstance(child, zonValue):
				newZonValue = uiZonValue()
				newZonValue.addZonValueInput(child.name, baseParentLayout, child.value)
				self.editorVarsList.append(newZonValue)
			elif isinstance(child, zonArray):
				newZonArray = uiZonArray()
				newZonArray.addZonArrayInput(child.name, baseParentLayout, child.children[0])
				self.editorVarsList.append(newZonArray)

	
	def readEditorOutputZon(self):

		returnZon = baseZonObject()
		returnZon.children = [] # i dont know why we have to clear it but somehow the format file passes into this
		for i in range(self.editorVarsList.__len__()):
			childButton = self.editorVarsList[i]

			if isinstance(childButton, uiZonValue):
				if childButton.txtInput.text() == "": continue
				newZonObj = zonValue()
				newZonObj.value = childButton.txtInput.text()
				newZonObj.name = childButton.name
				returnZon.children.append(newZonObj)
			if isinstance(childButton, uiZonArray):
				newZonObj = zonArray()
				for childTxtInput in childButton.txtInputList:
					if childTxtInput.text() == "": continue
					newZonObj.children.append(childTxtInput.text())
				if newZonObj.children.__len__() == 0: continue
				newZonObj.name = childButton.name
				returnZon.children.append(newZonObj)
		return returnZon

				


# smaller classes for ui
class uiZonValue:

	name = "ErrorNotDefined"
	txtInput = None

	def addZonValueInput(self, name, baseParentLayout, defaultText):
		txtInputsLayout = QHBoxLayout()
		
		self.name = name
		self.txtInput = QLineEdit()
		self.txtInput.setPlaceholderText(defaultText)
		txtInputsLayout.addWidget(self.txtInput)

		lineLayout = QHBoxLayout()#item 1 is always the actual value object(s)
		namelabel = QLabel(name + " = ")
		lineLayout.addWidget(namelabel)
		lineLayout.addLayout(txtInputsLayout)

		baseParentLayout.addLayout(lineLayout)

class uiZonArray:

	name = "ErrorNotDefined"
	txtInputList = []

	def addZonArrayInput(self, defaultText, baseParentLayout, name):
		txtInputsLayout = QHBoxLayout()
		self.createSingleArrayInput(defaultText, txtInputsLayout)
		
		self.name = name
		lineLayout = QHBoxLayout()#item 1 is always the actual value object(s)
		namelabel = QLabel(name + " = ")
		lineLayout.addWidget(namelabel)
		lineLayout.addLayout(txtInputsLayout)

		baseParentLayout.addLayout(lineLayout)

	def createSingleArrayInput(self, defaultText, parentLayout):
		txtInput = QLineEdit()
		txtInput.setPlaceholderText(defaultText)
		txtInput.textChanged.connect(lambda: self.checkArrayZonChildren(defaultText, parentLayout))
		self.txtInputList.append(txtInput)
		parentLayout.addWidget(txtInput)
	
	def checkArrayZonChildren(self, defaultText, parentLayout):
		
		widgetsRemovalList = []

		for i in range(parentLayout.count()):
			childButton = parentLayout.itemAt(i).widget()
			
			if (childButton.text() == "") and (i + 1 != parentLayout.count()):
				widgetsRemovalList.append(childButton)
			elif (childButton.text() != "") and (i + 1 == parentLayout.count()):
				self.createSingleArrayInput(defaultText, parentLayout)
		
		for widget in widgetsRemovalList:
			self.txtInputList.remove(widget)
			widget.deleteLater()
# end of classes