

filename = "test4"
filepath = "Output/" + filename + ".zig.zon"


class baseZonObject:

	children = []

	def writeWithChildren(self):
		tempListBuffer = []

		tempListBuffer.append(".{")

		for child in self.children:
			tempListBuffer = child.writeWithChildren(tempListBuffer, "	")

		tempListBuffer.append("}")
		return tempListBuffer
	
class zonObject:

	name = "ErrorMissingName"
	children = []

	def writeWithChildren(self, givenChildren, tabText):
		
		tempListBuffer = givenChildren

		tempListBuffer.append(tabText + "." + self.name + " = .{")

		for child in self.children:
			tempListBuffer = child.writeWithChildren(tempListBuffer, tabText +  "	")

		tempListBuffer.append(tabText + "},")
		return tempListBuffer
	
class zonArray:

	name = "ErrorMissingName"
	children = []

	def writeWithChildren(self, givenChildren, tabText):
		
		tempListBuffer = givenChildren
		tempTextBuffer = ""
		tempTextBuffer = tabText + "{" + tempTextBuffer

		childCounter = 0

		for child in self.children:
			if childCounter == 0:
				tempTextBuffer = tempTextBuffer + child
			else:
				tempTextBuffer = ", " + tempTextBuffer + child
			childCounter += 1

		tempTextBuffer = tempTextBuffer + "},"

		tempListBuffer.append(tempTextBuffer)
		return tempListBuffer


class zonValue:

	name = "ErrorMissingName"
	value = 0

	def writeWithChildren(self, givenChildren, tabText):
		
		tempListBuffer = givenChildren

		tempListBuffer.append(tabText + "." + self.name + " = " + str(self.value) + ",")

		return tempListBuffer
	
def InterperetLine(Line):
    
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

		varName, varType, isZon = InterperetLine(line)

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


textOBJ = baseZonObject()
textOBJ.children = [zonValue(), zonObject(), zonArray()]
actualText = textOBJ.writeWithChildren()

with open(filepath, "w") as f:
	for line in actualText:
		f.write(line)
		f.write('\n')

ItemZonFormat = baseZonObject()
readFormatFile(ItemZonFormat)

