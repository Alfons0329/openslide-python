# My revision of openslide_region() using Py + C Codesign with shared library, openmp and Python ctypes

## Prequisities
* Library: OpenMP
    * libgomp:amd64, >=8.4.0 
    * libomp-dev:amd64, >= 5.0.1-1

* Library: Openslide-Python
    * Already have backend Openslide-C library installed


## Build
./autobulid.sh $path/to/openslide-c/library