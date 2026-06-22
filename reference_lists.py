import os

cubyzListofItems = []
cubyzBlockList = []

def refreshCubyzItemList(cubyzPath):
	cubyzListofItems = []
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
	cubyzBlockList = []
	pathSearching = cubyzPath + "/assets/cubyz/items"
	with os.scandir(pathSearching) as list:
		for thing in list:
			if thing.is_file():
				if thing.name == "_migrations.zig.zon": continue
				if thing.name == "_defaults.zig.zon": continue
				cubyzListofItems.append(thing)
			elif thing.is_dir():
				if thing.name == "textures": continue
				searchThroughChildren(thing.path, cubyzBlockList)
			else:
				print("Error in getting item list: found a weird filetype")
	pathSearching = cubyzPath + "/assets/cubyz/blocks"
	with os.scandir(pathSearching) as list:
		for thing in list:
			if thing.is_file():
				if thing.name == "_migrations.zig.zon": continue
				if thing.name == "_defaults.zig.zon": continue
				cubyzBlockList.append(thing)
			elif thing.is_dir():
				if thing.name == "textures": continue
				searchThroughChildren(thing.path, cubyzListofItems)
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

def RefreshAllLists(cubyzPath):

	refreshCubyzItemList(cubyzPath)
	refreshCubyzBlockList(cubyzPath)


def getItemList():
	return cubyzListofItems

def getBlockList():
	return cubyzBlockList
