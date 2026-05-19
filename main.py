from zon_object_types import *
from formatting import *
from editor_ui import *

import sys
import os



# testing code
#filename = "test4"
#filepath = "Output/" + filename + ".zig.zon"
#textOBJ = baseZonObject()
#textOBJ.children = [zonValue(), zonObject(), zonArray()]
#writeGivenZonObjectToFile(filepath, textOBJ)



ItemZonFormat = readFormatFile("formatting/base_types/item.txt")

print("running app")

#filename = "test4"
#filepath = "Output/" + filename + ".zig.zon"

app = QApplication(sys.argv)
window = MainWindow(ItemZonFormat.children)
window.show()
print(window.readEditorOutputZon())
app.exec()
