from zon_object_types import *
from formatting import *
from editor_ui import *
from PyQt6.QtWidgets import QFileDialog

import sys
import os



# testing code
#filename = "test4"
#filepath = "Output/" + filename + ".zig.zon"
#textOBJ = baseZonObject()
#textOBJ.children = [zonValue(), zonObject(), zonArray()]
#writeGivenZonObjectToFile(filepath, textOBJ)

print("running app")

#filename = "test4"
#filepath = "Output/" + filename + ".zig.zon"

app = QApplication(sys.argv)
window = MainWindow()
window.show()
#print(window.readEditorOutputZon())
app.exec()
