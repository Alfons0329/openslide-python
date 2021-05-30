# import mylib --> ImportError: dynamic module does not define module export function (PyInit_mylib)
import numpy as np
import cv2
import argparse
import time
import sys, os
import openslide
from termcolor import colored
from PIL import Image
from ctypes import *

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
handle.read_region_cpp.argtypes = [POINTER(c_uint32), c_char_p, c_float, c_int32]
handle.read_region_cpp.restype = c_int32

# Parallel openslide_read_region() using ctypes with low-level C
'''
Input args: 
    handle: ctypes DLL handle
    slide_path: path/to/certain/slide
    resize_ratio: as title
    thread_cnt: how many thread to use at once to accelerate
    w: slide width
    h: slide height
Return args: ndarray RGBA image
'''
def _read_region_ctype(handle, slide_path, resize_ratio, thread_cnt, w, h):
    cpp_ret_code = handle.read_region_cpp(buf, c_char_p(slide_path.encode('utf-8')), float(resize_ratio), int(thread_cnt))
    if cpp_ret_code:
        print('read_region_cpp illegal terminate, errcode {}'.format(cpp_ret_code))
    
    ret = np.frombuffer(buf)
    ret = Image.frombuffer('RGBA', (w, h), ret, 'raw', 'RGBA', 0, 1)
    print(type(ret))
    return ret

f_name = 'out_thread_'
def main():
    slide = openslide.open_slide(slide_path)
    # Required, (w, h) needed to be acquired from openslide pyton setup functions for suitable size in Image.frombugger in PIL
    target_level = 0
    for level in range(len(slide.level_downsamples)):
        if slide.level_downsamples[level] <= 1.0 / resize_ratio:
            target_level = level

    target_width, target_height = slide.level_dimensions[target_level]

    # Codesgin read region
    begin = time.time()
#     img_rgba = mylib._read_region_ctype(handle, target_width, target_height)
    img_rgba = _read_region_ctype(handle, slide_path, resize_ratio, thread_cnt, target_width, target_height)
    end = time.time()
    t_read_slide = end - begin
    print(colored('\t_read_region_ctype time {:.2f}s'.format(t_read_slide), 'red'))

    if save_img:
        for_save = img_rgba.copy()
        for_save.thumbnail((3840, 2160))
        for_save.save(f_name + str(thread_cnt)+ '_.png')

main()