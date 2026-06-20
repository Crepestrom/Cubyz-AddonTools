import os

cubyzListofItems = []
cubyzBlockList = []
cubyzSbbList = []
cubyzBlpList = []

#MARK: blocks and items
def refreshCubyzItemList(cubyzPath):
	cubyzListofItems.clear() # clears the array so that it can be reused
	pathSearching = cubyzPath + "/assets/cubyz/items"
	with os.scandir(pathSearching) as list:
		for thing in list:
			if thing.is_file():
				if thing.name == "_migrations.zig.zon": continue
				cubyzListofItems.append(thing)
			elif thing.is_dir():
				if thing.name == "textures": continue
				searchThroughChildren(thing.path, cubyzListofItems)
			else:
				print("Error in getting item list: found a weird filetype")
	pathSearching = cubyzPath + "/assets/cubyz/blocks"
	with os.scandir(pathSearching) as list:
		for thing in list:
			if thing.is_file():
				if thing.name == "_migrations.zig.zon": continue
				cubyzListofItems.append(thing)
			elif thing.is_dir():
				if thing.name == "textures": continue
				searchThroughChildren(thing.path, cubyzListofItems)
			else:
				print("Error in getting item from blocks list: found a weird filetype")

def refreshCubyzBlockList(cubyzPath):
	cubyzBlockList.clear()
	pathSearching = cubyzPath + "/assets/cubyz/blocks"
	with os.scandir(pathSearching) as list:
		for thing in list:
			if thing.is_file():
				if thing.name == "_migrations.zig.zon": continue
				if thing.name == "_defaults.zig.zon": continue
				cubyzBlockList.append(thing)
			elif thing.is_dir():
				if thing.name == "textures": continue
				searchThroughChildren(thing.path, cubyzBlockList)
			else:
				print("Error in getting item from blocks list: found a weird filetype")

def searchThroughChildren(path, listToAppendTo):
	with os.scandir(path) as list:
		for thing in list:
			if thing.is_file():
				if thing.name == "_defaults.zig.zon": continue 
				listToAppendTo.append(thing)
			elif thing.is_dir():
				searchThroughChildren(thing.path, listToAppendTo)
			else:
				print("Error in getting child list: found a weird filetype")

#MARK: Sbb and Blp

def refreshCubyzSbbList(cubyzPath):
	cubyzSbbList.clear()
	pathSearching = cubyzPath + "/assets/cubyz/sbb"
	with os.scandir(pathSearching) as list:
		for thing in list:
			if thing.is_file():
				if os.path.splitext(thing.path) != ".zig.zon": continue
				cubyzSbbList.append(thing)
			elif thing.is_dir():
				if thing.name == "textures": continue
				searchThroughChildrenSbb(thing.path, cubyzSbbList)
			else:
				print("Error in getting item from sbb list: found a weird filetype")

def searchThroughChildrenSbb(path, listToAppendTo):
	with os.scandir(path) as list:
		for thing in list:
			if thing.is_file():
				if os.path.splitext(thing.path) != ".zig.zon": continue
				listToAppendTo.append(thing)
			elif thing.is_dir():
				searchThroughChildrenSbb(thing.path, listToAppendTo)
			else:
				print("Error in getting child list: found a weird filetype")


def refreshCubyzBlpList(cubyzPath):
	cubyzBlpList.clear()
	pathSearching = cubyzPath + "/assets/cubyz/sbb"
	with os.scandir(pathSearching) as list:
		for thing in list:
			if thing.is_file():
				if os.path.splitext(thing.path) != ".blp": continue
				cubyzBlpList.append(thing)
			elif thing.is_dir():
				searchThroughChildrenBlp(thing.path, cubyzBlpList)
			else:
				print("Error in getting item from sbb list: found a weird filetype")

def searchThroughChildrenBlp(path, listToAppendTo):
	with os.scandir(path) as list:
		for thing in list:
			if thing.is_file():
				if os.path.splitext(thing.path) != ".blp": continue
				listToAppendTo.append(thing)
			elif thing.is_dir():
				searchThroughChildrenBlp(thing.path, listToAppendTo)
			else:
				print("Error in getting child list: found a weird filetype")


# end of cases	


def RefreshAllLists(cubyzPath):

	refreshCubyzItemList(cubyzPath)
	refreshCubyzBlockList(cubyzPath)
	refreshCubyzSbbList(cubyzPath)
	refreshCubyzBlpList(cubyzPath)


def getItemList():
	print("testing1` ")
	print(cubyzListofItems)
	print("testing2` ")
	return cubyzListofItems

def getBlockList():
	return cubyzBlockList

def getSbbList():
	return cubyzSbbList

def getBlpList():
	return cubyzBlpList
