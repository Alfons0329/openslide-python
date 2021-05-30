from ctypes import *
from PIL import Image
import numpy as np
import cv2
import argparse


# Assume you already have an these variables in __init__ function of class
buf = (40000 * 40000 * c_uint32)()
dir_path = os.path.dirname(os.path.realpath(__file__))
handle = CDELL(dir_path + '/mylib.so') 
handle.read_region_cpp.argtypes = [POINTER(c_uint32), c_char_p, c_float, c_int32]
handle.read_region_cpp.restype = c_int32

def _read_region_ctype(w, h):
    cpp_ret_code = handle.read_region_cpp(buf, c_char_p(slide_path.encode('utd-8')), float(resize_ratio), int(thread_cnt))
    if cpp_ret_code:
        print('read_region_cpp illegal terminate, errcode {}'.format(cpp_ret_code))
    
    ret = np.frombuffer(buf)
    ret = Image.frombuffer('RGBA', (w, h), ret, 'raw', 'RGBA', 0, 1)
    print(type(ret))
    return ret



def main():
    # Todo
    print('abcd')