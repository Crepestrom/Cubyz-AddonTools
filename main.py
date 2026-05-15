from zon_object_types import *
from formatting import *
from editor_ui import *

import sys




# testing code
#filename = "test4"
#filepath = "Output/" + filename + ".zig.zon"
#textOBJ = baseZonObject()
#textOBJ.children = [zonValue(), zonObject(), zonArray()]
#writeGivenZonObjectToFile(filepath, textOBJ)



ItemZonFormat = baseZonObject()
readFormatFile(ItemZonFormat)

print("running app")

#filename = "test4"
#filepath = "Output/" + filename + ".zig.zon"

app = QApplication(sys.argv)
window = MainWindow(ItemZonFormat.children)
window.show()
print(window.readEditorOutputZon())
app.exec()

