from zon_object_types import *
from formatting import *
from ui_classes import *

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

globalCubyzPath = ""

#MARK: MainWindow
class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("My App")
		
		self.cubyzPath = ""
		self.getCubyzDirectoryDialog()
		
		self.editorVarsList = []
		scrollBar = QScrollArea()
		scrollBar.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
		scrollBar.setWidgetResizable(True)


		editorLayout = QVBoxLayout()
		
		self.filename = "test" # define this here so it could be changed at another time
		self.zonTypeDropdown = QComboBox()
		self.zonTypeDropdown.setPlaceholderText("Select a Format")
		self.zonTypeDropdown.addItem("")
		self.zonTypeDropdown.addItems(["formatting/base_types/item.txt", "formatting/base_types/block.txt", "formatting/base_types/recipie.txt"])
		self.zonTypeDropdown.currentTextChanged.connect(lambda: self.setScrollAreaLayout(scrollBar))
		editorLayout.addWidget(self.zonTypeDropdown)

		editorLayout.addWidget(scrollBar)

		saveZonButton = QPushButton("Save")
		saveZonButton.pressed.connect(lambda: self.writeZonUiToFile(self.filename, self.readEditorOutputZon()))
		editorLayout.addWidget(saveZonButton)

		saveZonButton = QLineEdit()
		saveZonButton.setPlaceholderText("put filename here")
		saveZonButton.textChanged.connect(self.changeSaveText)
		editorLayout.addWidget(saveZonButton)

		widget = QWidget()
		widget.setLayout(editorLayout)
		self.setCentralWidget(widget)
		

	def getCubyzDirectoryDialog(self):
		dialog = QFileDialog(self)
		print("Please select a cubyz directory")
		print("this is so we can reference its files")
		dialog.setDirectory(r'C:\Downloads')
		dialog.setFileMode(QFileDialog.FileMode.Directory)
		dialog.setViewMode(QFileDialog.ViewMode.List)
		if dialog.exec():
			print(dialog.directory().path())
			globalCubyzPath = dialog.directory().path()
			reference_lists.RefreshAllLists(globalCubyzPath)


	def setScrollAreaLayout(self, ScrollObj):

		givenFormatName = self.zonTypeDropdown.currentText()
		givenFormat = readFormatFile(givenFormatName).children

		self.editorVarsList = []
		editorVarsLayout = QVBoxLayout()

		tempWidget = QWidget()
		tempWidget.setLayout(editorVarsLayout)

		readFormat(givenFormat , editorVarsLayout, self.editorVarsList)

		ScrollObj.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
		ScrollObj.setWidget(tempWidget)


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

			if isinstance(childButton, uiTxtInputZonValue):
				self.addZonValue(childButton, returnZon)
			if isinstance(childButton, uiComboBoxZonValue):
				if childButton.comboBox.currentText() == "": continue
				newZonObj = zonValue()
				newZonObj.value = childButton.comboBox.currentText()
				newZonObj.name = childButton.name
				returnZon.children.append(newZonObj)
			if isinstance(childButton, uiTxtInputZonArray):
				self.addZonArray(childButton, returnZon)
			if isinstance(childButton, uiComboBoxZonArray):
				newZonObj = zonArray()
				newZonObj.children = []
				for childComboBox in childButton.comboBoxList:
					if childComboBox.currentText() == "": continue
					newZonObj.children.append(childComboBox.currentText())
				if newZonObj.children.__len__() == 0: return
				newZonObj.name = childButton.name
				returnZon.children.append(newZonObj)
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
			if isinstance(childButton, uiRecipieZon):
				newBaseZonObj = baseZonObject()
				newBaseZonObj.children = []
				for recipie in childButton.children:
					self.recurseReadChildren(recipie, newBaseZonObj)
				returnZon.children.append(newBaseZonObj)
			

	
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


# end of classes