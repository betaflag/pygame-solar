import os
import ctypes.util
uname = os.uname()

if uname.sysname == "Darwin" and uname.release >= "20.":
    uname = os.uname()
    real_find_library = ctypes.util.find_library
    def find_library(name):
        if name in {"OpenGL", "GLUT"}:  # add more names here if necessary
            return f"/System/Library/Frameworks/{name}.framework/{name}"
        return real_find_library(name)
    ctypes.util.find_library = find_library