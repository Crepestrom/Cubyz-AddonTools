from zon_object_types import *
from formatting import *

import reference_lists

from PyQt6.QtCore import Qt
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
	QComboBox,
	QScrollArea,
	QFileDialog,
)
from pathlib import Path


class Color(QWidget):
	def __init__(self, color):
		super().__init__()
		self.setAutoFillBackground(True)

		palette = self.palette()
		palette.setColor(QPalette.ColorRole.Window, QColor(color))
		self.setPalette(palette)


def deleteWithChildren(object):
	if (object == None):
		return

	if (object.layout()):
		for i in range(object.layout().count()):
			if (object.itemAt(i).widget()):
				object.itemAt(i).widget().deleteLater()
			elif (object.itemAt(i).layout()):
				if object.itemAt(i).layout().count() != 0:
					deleteWithChildren(object.itemAt(i))
				object.itemAt(i).layout().deleteLater()
			else:
				print("deleteWithChildren found a child it could not delete")
				print(object)
	elif (object.widget()):
		object.widget().deleteLater()
	else:
		print("deleteWithChildren found a child it could not delete")
		print(object)
			
def writeGivenZonObjectToFile(filepath, zonObject):
	print("Writing to " + filepath)
	actualText = zonObject.writeWithChildren([], "")
	with open(filepath, "w") as f:
		for line in actualText:
			f.write(line)
			f.write('\n')

def readFormat(givenFormat, baseParentLayout, childZonList):
	for child in givenFormat:
		if isinstance(child, zonValue):
			newZonValue = uiTxtInputZonValue()
			newZonValue.addZonValueInput(child.name, baseParentLayout, child.value)
			childZonList.append(newZonValue)
		elif isinstance(child, zonArray):
			newZonArray = uiTxtInputZonArray()
			newZonArray.addZonArrayInput(child.name, baseParentLayout, child.children[0])
			childZonList.append(newZonArray)
		elif isinstance(child, zonObject):
			newZonObject = uiZonObject()
			uiZonObject.children = []
			newZonObject.addZonObjectInput(child.name, baseParentLayout)
			readFormat(child.children, newZonObject.childUiLayout, newZonObject.children)
			childZonList.append(newZonObject)
		if isinstance(child, recipieZon):
			newUI = uiRecipieZon()
			newUI.addRecipieInput(baseParentLayout, reference_lists.getItemList())
			childZonList.append(newUI)


#MARK: UiClasses
# smaller classes for ui
class uiTxtInputZonValue():

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

class uiComboBoxZonValue():

	name = "ErrorNotDefined"
	comboBox = None

	def addZonValueInput(self, name, baseParentLayout, defaultText, givenList):
		inputsLayout = QHBoxLayout()
		
		self.name = name
		self.comboBox = QComboBox()
		self.comboBox.setPlaceholderText(defaultText)
		self.comboBox.addItem("")
		self.comboBox.addItems(givenList)
		inputsLayout.addWidget(self.comboBox)

		lineLayout = QHBoxLayout()#item 1 is always the actual value object(s)
		namelabel = QLabel(name + " = ")
		lineLayout.addWidget(namelabel)
		lineLayout.addLayout(inputsLayout)

		baseParentLayout.addLayout(lineLayout)

class uiTxtInputZonArray():

	name = "ErrorNotDefined"

	def addZonArrayInput(self, name, baseParentLayout, defaultText):
		txtInputsLayout = QHBoxLayout()
		self.txtInputList = []
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

class uiComboBoxZonArray():

	name = "ErrorNotDefined"
	updateParentFunction = None

	def addZonArrayInput(self, name, baseParentLayout, defaultText, givenList):
		self.givenList = givenList
		comboBoxLayout = QHBoxLayout()
		self.comboBoxList = []
		self.createSingleArrayInput(defaultText, comboBoxLayout)
		
		self.name = name
		lineLayout = QHBoxLayout()#item 1 is always the actual value object(s)
		namelabel = QLabel(name + " = ")
		lineLayout.addWidget(namelabel)
		lineLayout.addLayout(comboBoxLayout)

		baseParentLayout.addLayout(lineLayout)

	def createSingleArrayInput(self, defaultText, parentLayout):
		comboBoxInput = QComboBox()
		comboBoxInput.setPlaceholderText(defaultText)
		comboBoxInput.addItem("")
		comboBoxInput.addItems(self.givenList)
		comboBoxInput.currentTextChanged.connect(lambda: self.checkArrayZonChildren(defaultText, parentLayout))
		self.comboBoxList.append(comboBoxInput)
		parentLayout.addWidget(comboBoxInput)
	
	def checkArrayZonChildren(self, defaultText, parentLayout):
		
		widgetsRemovalList = []

		for i in range(parentLayout.count()):
			childButton = parentLayout.itemAt(i).widget()
			
			if (childButton.currentText() == "") and (i + 1 != parentLayout.count()):
				widgetsRemovalList.append(childButton)
			elif (childButton.currentText() != "") and (i + 1 == parentLayout.count()):
				self.createSingleArrayInput(defaultText, parentLayout)
		
		for widget in widgetsRemovalList:
			self.comboBoxList.remove(widget)
			widget.deleteLater()
		
		if self.updateParentFunction: #lets this weird structure update a parent
			self.updateParentFunction()

class uiZonObject():

	name = "ErrorNotDefined"
	children = []
	childUiLayout = None

	def addZonObjectInput(self, name, baseParentLayout):
		self.childUiLayout = QVBoxLayout()
		
		self.name = name

		lineLayout = QHBoxLayout()#item 1 is always the actual value object(s)
		namelabel = QLabel(name + " = ")
		lineLayout.addWidget(namelabel)
		lineLayout.addLayout(self.childUiLayout)

		baseParentLayout.addLayout(lineLayout)

class uiFormatGroupZonMulti():
	name = "ErrorNotDefined"
	givenFormatGroup = []
	dropdownBox = None
	children = []

	def addFormatGroupInput(self, name, baseParentLayout, givenFormatGroup):
		print("added format group input")
		self.childUiLayout = QVBoxLayout()
		self.createDropdownInput(givenFormatGroup, self.childUiLayout)
		self.name = name
		self.givenFormatGroup = givenFormatGroup
		
		lineLayout = QHBoxLayout()#item 1 is always the actual value object(s)
		namelabel = QLabel(name + " = ")
		lineLayout.addWidget(namelabel)
		lineLayout.addLayout(self.childUiLayout)

		baseParentLayout.addLayout(lineLayout)

	def createDropdownInput(self, givenFormatGroup, parentLayout):
		dropdownInput = QComboBox()
		
		dropdownInput.addItem("")
		dropdownInput.addItems(givenFormatGroup)
		dropdownInput.currentTextChanged.connect(lambda: self.checkDropdownChildren(parentLayout))
		self.dropdownBox = (dropdownInput)

		parentLayout.addWidget(dropdownInput)
	
	def checkDropdownChildren(self, parentLayout):
		removalList = []
		for i in range(parentLayout.count()):
			removalList.append(parentLayout.itemAt(i).layout())

		self.children = []
		for thing in removalList:
			deleteWithChildren(thing)
		
		childUiZonLayout = QVBoxLayout()# we seperate it like this so that the children can be deleted without the dropdown deleting itself
		parentLayout.addLayout(childUiZonLayout)

		text = self.dropdownBox.currentText()
		if text != "":
			readFormat(readFormatFile(text).children, parentLayout, self.children)

class uiRecipieZon():

	children = []

	def addRecipieInput(self, baseParentLayout, listOfItems):
		self.childUiLayout = QVBoxLayout()

		self.itemNameList = []
		for selectableItem in listOfItems:
			self.itemNameList.append(selectableItem.name)
		
		self.addSingleRecipieInput(baseParentLayout)

	def addSingleRecipieInput(self, baseParentLayout):
		self.uiRecipieList = []
		recipieLayout = QVBoxLayout()
		recipieLayout.widget

		inputUi = uiComboBoxZonArray()
		inputUi.addZonArrayInput("input", recipieLayout, "pick a item", self.itemNameList)
		inputUi.updateParentFunction = (lambda: self.checkUiChildren(recipieLayout))
		self.uiRecipieList.append(inputUi)

		outputUi = uiComboBoxZonValue()
		outputUi.addZonValueInput("output", recipieLayout, "pick a item", self.itemNameList)
		outputUi.comboBox.currentTextChanged.connect(lambda: self.checkUiChildren(recipieLayout))
		self.uiRecipieList.append(outputUi)

		baseParentLayout.addLayout(recipieLayout)
	
	def checkUiChildren(self, parentLayout):
		
		widgetsRemovalList = []

		for i in range(int(self.uiRecipieList.__len__()/2)):
			childInputs = self.uiRecipieList[i*2]
			inputBool = (childInputs.comboBoxList[0].currentText() == "")

			childOutputs = self.uiRecipieList[i*2+1].comboBox
			outputBool = (childOutputs.currentText() == "")
			if (inputBool) and (outputBool) and (i + 1 == parentLayout.count()):
				widgetsRemovalList.append(childInputs)
				widgetsRemovalList.append(childOutputs)
			else:
				if (i + 1 == int(self.uiRecipieList.__len__()/2)): self.addSingleRecipieInput(parentLayout)
		
		for widget in widgetsRemovalList:
			self.uiRecipieList.remove(widget)
			widget.deleteLater()