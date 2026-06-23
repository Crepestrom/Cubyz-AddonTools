# everything tries to format itself in a similar way to what this creates so they have similar frameworks

class baseZonObject():

	children = []

	def writeWithChildren(self, givenChildren, tabText):
		tempListBuffer = givenChildren

		tempListBuffer.append(tabText + ".{")

		for child in self.children:
			tempListBuffer = child.writeWithChildren(tempListBuffer, tabText + "	")

		if tabText == "": tempListBuffer.append(tabText + "}") 
		else: tempListBuffer.append(tabText + "},")

		return tempListBuffer
	
class zonObject(): # .something = {.thing1 = "value1", .thing2 = "value1",}

	name = "ErrorMissingName"
	children = []

	def writeWithChildren(self, givenChildren, tabText):
		
		tempListBuffer = givenChildren

		tempListBuffer.append(tabText + "." + self.name + " = .{")

		for child in self.children:
			tempListBuffer = child.writeWithChildren(tempListBuffer, tabText +  "	")

		tempListBuffer.append(tabText + "},")
		return tempListBuffer
	
class zonArray(): # .something = {"value1", "value2", "value3"},

	name = "ErrorMissingName"
	children = []

	def writeWithChildren(self, givenChildren, tabText):
		
		tempListBuffer = givenChildren
		tempTextBuffer = ""

		childCounter = 0

		for child in self.children:
			if childCounter == self.children.__len__()-1:
				tempTextBuffer = tempTextBuffer + child
			else:
				tempTextBuffer = tempTextBuffer + child + ", "
			childCounter += 1

		tempTextBuffer = ".{" + tempTextBuffer + "}"

		tempListBuffer.append(tabText + "." + self.name + " = " + tempTextBuffer + ",")
		return tempListBuffer


class zonValue(): # .something = "value",

	name = "ErrorMissingName"
	value = 0

	def writeWithChildren(self, givenChildren, tabText):
		
		tempListBuffer = givenChildren

		tempListBuffer.append(tabText + "." + self.name + " = " + str(self.value) + ",")

		return tempListBuffer

# MARK: UiZons
# used only for translating from formatting files
# never used when reading from .zig.zon files
class formatGroupZonMulti():

	name = "ErrorMissingName"
	formatGroup = []
	children = []

class recipieZon():
	name = "ErrorMissingName" # not used just defined so i can sort by classes

class blpSelect():
	name = "ErrorMissingName"
	children = []

print("imported zon_object_types.py")