from zon_object_types import *

def InterperetFormattingLine(Line):
	
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

		if varType == "tag":
			newZonObj = zonArray()
			newZonObj.name = varName
			parentZon.children.append(newZonObj)
		elif varType == "0":
			newZonObj = zonValue()
			newZonObj.name = varName
			parentZon.children.append(newZonObj)
		elif varType == "image":
			newZonObj = zonValue()
			newZonObj.name = varName
			newZonObj.value = ""
			parentZon.children.append(newZonObj)
		
		if varType == "},":
			break

		lineNumber += 1

def readFormatFile(baseZonObject):

	with open("zonTypes/item.txt", "r") as file:
		
		documentLines = []
		CurrentZonObject = baseZonObject
		
		while True:

			line = file.readline()
			if not line:
				break
			
			documentLines.append(line.strip())

		return readFormatZon(documentLines, 0, CurrentZonObject)