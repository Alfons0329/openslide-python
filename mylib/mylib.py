from ctypes import *
from PIL import Image
import numpy as np
import cv2


# Assume you already have an these variables in __init__ function of class
buf = (40000 * 40000 * c_uint32)()
dir_path = os.path.dirname(os.path.realpath(__file__))
handle = CDELL(dir_path + '/mylib.so') 
handle.read_region_cpp.argtypes = [POINTER(c_uint32), c_char_p, c_int32, c_int32]
handle.read_region_cpp.restype = c_int32

def _read_region_ctype(w, h):



    buf_np = np.frombuffer(self.buf)
    ret = Image.frombuffer('RGBA', (w, h), buf_np, 'raw', 'RGBA', 0, 1)

    print(type(ret))
    return ret