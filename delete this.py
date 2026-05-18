from formatting import *
import os

def createFormatGroup(filePath):
	specificFormatList = []
	for name in os.listdir(filePath):
		formatZon = readFormatFile(filePath + "/"  + name)
		specificFormatList.append(formatZon)
	return specificFormatList

class formatGroups:
	biome = None
	block = None
	sbb = None
	item = formatter.readFormatFile(formatter, "formatting/base_types/item.txt")

	def createFormatGroup(self, filePath):
		specificFormatList = []
		for name in os.listdir(filePath):
			formatZon = formatter.readFormatFile(filePath + "/"  + name)
			specificFormatList.append(formatZon)
		return specificFormatList

	modifiers = createFormatGroup("formatting/modifier")