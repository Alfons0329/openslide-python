# import mylib --> ImportError: dynamic module does not define module export function (PyInit_mylib)
import numpy as np
import cv2
import argparse
import time
import sys, os
from termcolor import colored
from PIL import Image
from ctypes import *
import mylib_wrapper
'''
Not import mylib
https://stackoverflow.com/questions/65356321/creating-a-python-module-using-ctypes
'''

# Argparse
parser = argparse.ArgumentParser()
parser.add_argument(
    "--slide_path",
    type=str,
)
parser.add_argument(
        "--resize_ratio",
        type=float,
        default=0.2,
)
parser.add_argument(
        "--save_img",
        type=int,
        default=0
)
parser.add_argument(
        "--thread_cnt",
        type=int,
        default=1
)
args = parser.parse_args()
slide_path      = args.slide_path
resize_ratio    = args.resize_ratio
save_img        = args.save_img
thread_cnt      = args.thread_cnt

# Init
buf = (40000 * 40000 * c_uint32)()
dir_path = os.path.dirname(os.path.realpath(__file__))
handle = CDLL(dir_path + '/mylib.so')
handle.read_region_cpp.argtypes = [POINTER(c_uint32), c_char_p, c_float, c_int32, POINTER(c_uint32), POINTER(c_uint32)]
handle.read_region_cpp.restype = c_int32

REPEAT=1

f_name = 'out_thread_'
def main():
    # Codesgin read region
    for i in range(REPEAT):
        begin = time.time()
        img_rgba = mylib_wrapper._read_region_ctype(buf, handle, slide_path, resize_ratio, thread_cnt)
        end = time.time()
        t_read_slide = end - begin
        print(colored('\t_read_region_ctype time {:.2f}s'.format(t_read_slide), 'red'))

    if save_img:
        for_save = img_rgba.copy()
        for_save.thumbnail((2560, 1440))
        for_save.save(f_name + str(thread_cnt)+ '_.png')

main()
