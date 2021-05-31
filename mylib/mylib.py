from ctypes import *
from PIL import Image

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
def _read_region_ctype(handle, slide_path, resize_ratio, thread_cnt):
    w = c_uint32()
    h = c_uint32()
    cpp_ret_code = handle.read_region_cpp(buf, c_char_p(slide_path.encode('utf-8')), float(resize_ratio), int(thread_cnt), byref(w), byref(h))
    if cpp_ret_code:
        print('read_region_cpp illegal terminate, errcode {}'.format(cpp_ret_code))
    
    print('Slide dimension: w:{} x h:{}'.format(w, h))
    ret = np.frombuffer(buf)
    ret = Image.frombuffer('RGBA', (w, h), ret, 'raw', 'RGBA', 0, 1)
    return ret