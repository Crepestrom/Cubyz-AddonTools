from zon_object_types import *
from formatting import *

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
)

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
				#object.itemAt(i).layout().deleteLater()
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
			newZonValue = uiZonValue()
			newZonValue.addZonValueInput(child.name, baseParentLayout, child.value)
			childZonList.append(newZonValue)
		elif isinstance(child, zonArray):
			newZonArray = uiZonArray()
			newZonArray.addZonArrayInput(child.name, baseParentLayout, child.children[0])
			childZonList.append(newZonArray)
		elif isinstance(child, zonObject):
			newZonObject = uiZonObject()
			uiZonObject.children
			newZonObject.addZonObjectInput(child.name, baseParentLayout)
			readFormat(child.children, newZonObject.childUiLayout, newZonObject.children)
			childZonList.append(newZonObject)
		if isinstance(child, formatGroupZonMulti):
			newZonFormatGroup = uiFormatGroupZonMulti()
			newZonFormatGroup.addFormatGroupInput(child.name, baseParentLayout, child.formatGroup)
			childZonList.append(newZonFormatGroup)

class MainWindow(QMainWindow):
	def __init__(self, givenFormat):
		super().__init__()
		self.setWindowTitle("My App")
		
		self.editorVarsList = []
		editorVarsLayout = QVBoxLayout()
		readFormat(givenFormat, editorVarsLayout, self.editorVarsList)

		editorLayout = QVBoxLayout()
		editorLayout.addLayout(editorVarsLayout)
		
		self.filename = "test" # define this here so it could be changed at another time
		saveZonButton = QPushButton("Save")
		saveZonButton.pressed.connect(lambda: self.writeZonUiToFile(self.filename, self.readEditorOutputZon()))
		editorLayout.addWidget(saveZonButton)
		saveZonButton = QLineEdit("filename")
		saveZonButton.setPlaceholderText("put filename here")
		saveZonButton.textChanged.connect(self.changeSaveText)
		editorLayout.addWidget(saveZonButton)

		widget = QWidget()
		widget.setLayout(editorLayout)
		self.setCentralWidget(widget)

	def changeSaveText(self, text):
		self.filename = text

	def writeZonUiToFile(self, fileName, zonObject):
		filepath = "Output/" + fileName + ".zig.zon"
		writeGivenZonObjectToFile(filepath, zonObject)

	
	def readEditorOutputZon(self):

		returnZon = baseZonObject()
		returnZon.children = [] # i dont know why we have to clear it but somehow the format file passes into this

		self.recurseReadChildren(self.editorVarsList, returnZon)

		return returnZon
	
	def recurseReadChildren(self, givenList, returnZon):
		for i in range(givenList.__len__()):
			childButton = givenList[i]

			if isinstance(childButton, uiZonValue):
				self.addZonValue(childButton, returnZon)
			if isinstance(childButton, uiZonArray):
				self.addZonArray(childButton, returnZon)
			if isinstance(childButton, uiZonObject):
				self.addZonObj(childButton, returnZon)
			if isinstance(childButton, uiFormatGroupZonMulti):
				newZonObj = zonObject()
				newZonObj.children = [] # i suppose it just constantly flows over
				newZonObj.name = childButton.name
				newBaseZonObj = baseZonObject()
				newBaseZonObj.children = []
				self.recurseReadChildren(childButton.children, newBaseZonObj)
				if newBaseZonObj.children.__len__() == 0: return
				newZonObj.children = [newBaseZonObj]
				returnZon.children.append(newZonObj)
	
	def addZonValue(self, childButton, returnZon):
		if childButton.txtInput.text() == "": return
		newZonObj = zonValue()
		newZonObj.value = childButton.txtInput.text()
		newZonObj.name = childButton.name
		returnZon.children.append(newZonObj)
	
	def addZonArray(self, childButton, returnZon):
		newZonObj = zonArray()
		newZonObj.children = []
		for childTxtInput in childButton.txtInputList:
			if childTxtInput.text() == "": continue
			newZonObj.children.append(childTxtInput.text())
		if newZonObj.children.__len__() == 0: return
		newZonObj.name = childButton.name
		returnZon.children.append(newZonObj)
	
	def addZonObj(self, childButton, returnZon):
		newZonObj = zonObject()
		newZonObj.children = [] # i suppose it just constantly flows over
		newZonObj.name = childButton.name
		self.recurseReadChildren(childButton.children, newZonObj)
		if newZonObj.children.__len__() == 0: return
		returnZon.children.append(newZonObj)
	
# smaller classes for ui
class uiZonValue():

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

class uiZonArray():

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
			


# end of classes