from zon_object_types import *

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


def createChildBasedOnInfo(varName, varType, parentZon):
	if (varType == ".tag") or (varType == "0xffffffff"):
		newZonObj = zonArray()
		newZonObj.name = varName
		newZonObj.children = [varType]
		parentZon.children.append(newZonObj)
	elif (varType == "0") or (varType == "image.png"):
		newZonObj = zonValue()
		newZonObj.name = varName
		newZonObj.value = varType
		parentZon.children.append(newZonObj)
	else:
		varType = str(varType)
		print("Formatter Read Error: could not interperet the varType: {varType}")

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

def readFormatFile(baseZonObject): # returns the format file in a code readable way

	with open("zonTypes/item.txt", "r") as file:
		
		documentLines = []
		CurrentZonObject = baseZonObject
		
		while True:

			line = file.readline()
			if not line:
				break
			
			documentLines.append(line.strip())

		return readFormatZon(documentLines, 0, CurrentZonObject)

print("imported formatting.py")