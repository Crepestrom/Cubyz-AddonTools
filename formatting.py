from zon_object_types import *
import os

def is_float(value):
	try:
		float(value)
		return True
	except ValueError:
		return False


def InterperetFormattingLine(Line):
	
	# each zonThing is formatted like this
	# .nameOfThing = typeOfThing,
	currentState = "Tabs"
	nameBuffer = ""
	varBuffer = ""
	isZon = False

	for Character in Line:
		if (Character != "}") or (Character != "{"): # zon detector
			isZon = True
		if currentState == "Tabs":
			if Character != "	":
				currentState = "ReadName"
		
		if currentState == "ReadName":
			if Character == " ":
				currentState = "InbetweenVarRead"
			else:
				if (Character == "."): continue
				nameBuffer = nameBuffer + Character
		elif currentState == "InbetweenVarRead":
			if (Character != " ") and (Character != "="):
				currentState = "ReadVar"
		if currentState == "ReadVar":
			if Character == ",":
				currentState = "EndValue"
				break
			else:
				varBuffer = varBuffer + Character
	# end of text processing
	if nameBuffer == "},":
		nameBuffer = ""
		varBuffer = "},"
	
	return nameBuffer, varBuffer, isZon

def readFormatZon(lineList, startingLine, parentZon):
	lineNumber = startingLine
	while lineNumber < len(lineList):
		line = lineList[lineNumber]
		varName, varType, isZon = InterperetFormattingLine(line)
		if varType == ".{":
			newZonObj = zonObject()
			newZonObj.name = varName
			lineNumber = readZonObject(lineList, lineNumber + 1, newZonObj)
			parentZon.children.append(newZonObj)
		else:
			createChildBasedOnInfo(varName, varType, parentZon)
			lineNumber += 1


def createChildBasedOnInfo(varName, varType, parentZon): # determines how to interperet the given format text
	if (varType == ".tags") or (varType == "0xffffffff"):
		newZonObj = zonArray()
		newZonObj.name = varName
		newZonObj.children = [varType]
		parentZon.children.append(newZonObj)
	elif (varType.isdecimal()) or (is_float(varType)) or (varType == "image.png") or (varType == ".tag") or (varType == "true") or (varType == "false") or (varType == "0x000000") or (varType == "cubyz:no_rotation"):
		newZonObj = zonValue()
		newZonObj.name = varName
		newZonObj.value = varType
		parentZon.children.append(newZonObj)
	elif (varType == "modifiers"):
		newZonObj = formatGroupZonMulti()
		newZonObj.name = varName
		newZonObj.formatGroup = createFormatGroup("formatting/modifier")
		parentZon.children.append(newZonObj)
	elif (varType == "item"):
		newZonObj = zonObject()
		newZonObj.name = varName
		newZonObj.children = readFormatFile("formatting/base_types/item.txt").children
		parentZon.children.append(newZonObj)
	elif (varType == "},"):
		return
	elif (varType == "recipies"):
		newZonObj = recipieZon()
		parentZon.children.append(newZonObj)
	else:
		print("Formatter Read Error: could not interperet the varType: " + str(varType))

def readZonObject(lineList, startingLine, parentZon):
	lineNumber = startingLine
	while lineNumber < len(lineList):
		line = lineList[lineNumber]
		varName, varType, isZon = InterperetFormattingLine(line)
		if varType == "{":
			newZonObj = zonObject()
			newZonObj.name = varName
			lineNumber = readZonObject(lineList, startingLine, newZonObj)
			parentZon.children.append(newZonObj)
		else:
			createChildBasedOnInfo(varName, varType, parentZon)
			lineNumber += 1
		
		if varName == "},":
			break

	return lineNumber #this is so it continues after its done building a zonoObject

def readFormatFile(filePath): # returns the format file in a code readable way

	documentLines = []
	CurrentZonObject = baseZonObject()
	CurrentZonObject.children = [] # i really dont understand why we have to clear this
	with open(filePath, "r") as file:
				
		while True:

			line = file.readline()
			if not line:
				break
			
			documentLines.append(line.strip())
		readFormatZon(documentLines, 0, CurrentZonObject)
	return CurrentZonObject

def createFormatGroup(filePath):
	specificFormatList = []
	for name in os.listdir(filePath):
		specificFormatList.append(filePath + "/"  + name)
	return specificFormatList





print("imported formatting.py")