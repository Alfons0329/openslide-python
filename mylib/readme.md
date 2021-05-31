# My revision of openslide_region() using Py + C Codesign with shared library, openmp and Python ctypes
This is a stand-alone Openslide low-level C implementation with multithread accleration, which means there is  no need for Openslide-Python anymore.

## Prequisities
* Library: OpenMP
    * libgomp:amd64, >=8.4.0 
    * libomp-dev:amd64, >= 5.0.1-1

* Library: Openslide-Python
    * Already have backend Openslide-C library installed


## Build
* Usage: `./setup.sh $/path/to/openslide/top/folder $/path/to/writable/lib` (absolute path and exclude the last /)
* Ex: I have the sudo permission to write `/usr/local/lib` and my openslide top folder (git clone from [here](https://github.com/openslide/openslide)) is `/home/user/homework/openslide`.
  * Then use the following: `./setup.sh /home/user/homework/openslide /usr/local/lib`


## Peformance Report
* under construction