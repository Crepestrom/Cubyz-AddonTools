

filename = "test4"
filepath = "Output/" + filename + ".zig.zon"


class baseZonObject:

	children = []

	def writeWithChildren(self):
		tempTextBuffer = []

		tempTextBuffer.append(".{")

		for child in self.children:
			tempTextBuffer = child.writeWithChildren(tempTextBuffer, "	")

		tempTextBuffer.append("}")
		return tempTextBuffer
	
class zonObject:

	name = "ErrorMissingName"
	children = []

	def writeWithChildren(self, givenChildren, tabText):
		
		tempTextBuffer = givenChildren

		tempTextBuffer.append(tabText + "." + self.name + " = .{")

		for child in self.children:
			tempTextBuffer = child.writeWithChildren(tempTextBuffer, tabText +  "	")

		tempTextBuffer.append(tabText + "},")
		return tempTextBuffer


class zonValue:

	name = "ErrorMissingName"
	value = 0

	def writeWithChildren(self, givenChildren, tabText):
		
		tempTextBuffer = givenChildren

		tempTextBuffer.append(tabText + "." + self.name + " = " + str(self.value) + ",")

		return tempTextBuffer
	
def InterperetLine(Line):
    
	CurrentState = "Tabs"
	NameBuffer = ""
	VarBuffer = ""

	for Character in Line:
		if CurrentState == "Tabs":
			if Character != " ":
				CurrentState = "ReadName"
			else:
				VarBuffer = VarBuffer + Character #catches the end }, of zon files
		elif CurrentState == "ReadName":
			if Character == " ":
				CurrentState = "InbetweenVarRead"
			else:
				NameBuffer = NameBuffer + Character
		elif CurrentState == "InbetweenVarRead":
			if (Character != " ") and (Character != "="):
				CurrentState = "ReadVar"

		if CurrentState == "ReadVar":
			if Character == ",":
				CurrentState = "EndValue"
				break
			else:
				VarBuffer = VarBuffer + Character

	return NameBuffer, VarBuffer


def readFormatFile(BaseZonObject):

	with open("zonTypes/item.txt", "r") as file:
		while True:
			line = file.readline()
			if not line:
				break

			VarName, VarType = InterperetLine(line)

			if VarType == "0":

			print(VarName + VarType)


textOBJ = baseZonObject()
textOBJ.children = [zonValue(), zonObject()]
actualText = textOBJ.writeWithChildren()

with open(filepath, "w") as f:
    for line in actualText:
        f.write(line)
        f.write('\n')

ItemFormat = baseZonObject()
readFormatFile(ItemFormat)