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
		tempTextBuffer = "{" + tempTextBuffer

		childCounter = 0

		for child in self.children:
			if childCounter == 0:
				tempTextBuffer = tempTextBuffer + child
			else:
				tempTextBuffer = ", " + tempTextBuffer + child
			childCounter += 1

		tempTextBuffer = tempTextBuffer + "}"

		tempListBuffer.append(tabText + "." + self.name + " = " + tempTextBuffer + ",")
		return tempListBuffer


class zonValue:

	name = "ErrorMissingName"
	value = 0

	def writeWithChildren(self, givenChildren, tabText):
		
		tempListBuffer = givenChildren

		tempListBuffer.append(tabText + "." + self.name + " = " + str(self.value) + ",")

		return tempListBuffer