# Required files
SOURCE_SHARED_LIB:=read_svs_shared_lib.cpp
SOURCE_READ_SVS:=read_svs.cpp

TARGET_SHARED_LIB_METHOD03:=lib_read_svs_method03.so
TARGET_SHARED_LIB_METHOD12:=lib_read_svs_method12.so
TARGET_SHARED_LIB_METHOD4:= lib_read_svs_method4.so
TARGET_SHARED_LIB_METHOD5:= lib_read_svs_method5.so

TARGET_READ_SVS_METHOD03_DBG:=	read_svs_method03_dbg.o
TARGET_READ_SVS_METHOD12_DBG:=	read_svs_method12_dbg.o
TARGET_READ_SVS_METHOD4_DBG:= 	read_svs_method4_dbg.o
TARGET_READ_SVS_METHOD5_DBG:= 	read_svs_method5_dbg.o

# Compilers
CC=gcc

# Libraries and flags
# Absolute path will be better on NCHC machine
LDFLAGS=-L/usr/local/lib
INCLUDES=-I/usr/include/ -I/usr/local/include/openslide 
INCLUDES_PROFILER=-I/usr/local/include/gperftools/ -I/usr/local/include/google/
LIBS=-ldl -lrt -lopenslide -lstdc++fs -fopenmp -ljpeg
LIBS_PROFILER=

RPATH_METHOD03=	-Wl,-rpath=/usr/local/lib/openslide/ # For serial, baseline openslide build
RPATH_METHOD12=	-Wl,-rpath=/usr/local/lib/openslide-omp/ # For parallel, OpenMP openslide build
RPTAH_METHOD4=	-Wl,-rpath=/usr/local/lib/openslide-big-tile/ #For big tile openslide build (Suggested by prof Hung on Mar. 10, 2021)
RPATH_METHOD5=	-Wl,-rpath=/usr/local/lib/openslide-cylin/ #For big tile + cylin method openslide build (Suggested by prof Hung on Mar. 10, 2021)

CXXFLAGS_METHOD03:= -std=c++17 -Wall $(LDFLAGS) $(INCLUDES) $(INCLUDES_PROFILER) $(LIBS) $(RPATH_METHOD03) # For serial, baseline openslide build
CXXFLAGS_METHOD12:= -std=c++17 -Wall $(LDFLAGS) $(INCLUDES) $(INCLUDES_PROFILER) $(LIBS) $(RPATH_METHOD12) # For parallel, OpenMP openslide build
CXXFLAGS_METHOD4:=  -std=c++17 -Wall $(LDFLAGS) $(INCLUDES) $(INCLUDES_PROFILER) $(LIBS) $(RPTAH_METHOD4) #For big tile openslide build 
CXXFLAGS_METHOD5:=  -std=c++17 -Wall $(LDFLAGS) $(INCLUDES) $(INCLUDES_PROFILER) $(LIBS) $(RPATH_METHOD5) #For big tile openslide build 

# Rules
all: shared_lib read_svs_dbg
shared_lib: shared_lib_method03 shared_lib_method12 shared_lib_method4 shared_lib_method5
read_svs_dbg: read_svs_method03_dbg read_svs_method12_dbg read_svs_method4_dbg read_svs_method5_dbg

# This generated the shared object without undefiend symbols
shared_lib_method03: $(SOURCE_SHARED_LIB)
	$(CC) -m64 -fPIC -O2 -shared -lgomp -lomp -fopenmp $(SOURCE_SHARED_LIB) $(CXXFLAGS_METHOD03) -o $(TARGET_SHARED_LIB_METHOD03)

shared_lib_method12: $(SOURCE_SHARED_LIB)
	$(CC) -m64 -fPIC -O2 -shared -lgomp -lomp -fopenmp $(SOURCE_SHARED_LIB) $(CXXFLAGS_METHOD12) -o $(TARGET_SHARED_LIB_METHOD12)

shared_lib_method4: $(SOURCE_SHARED_LIB)
	$(CC) -m64 -fPIC -O2 -shared -lgomp -lomp -fopenmp $(SOURCE_SHARED_LIB) $(CXXFLAGS_METHOD4) -o $(TARGET_SHARED_LIB_METHOD4)

shared_lib_method5: $(SOURCE_SHARED_LIB)
	$(CC) -m64 -fPIC -O2 -shared -lgomp -lomp -fopenmp $(SOURCE_SHARED_LIB) $(CXXFLAGS_METHOD4) -o $(TARGET_SHARED_LIB_METHOD5)

################################################# DBG #################################################
read_svs_method03_dbg: $(SOURCE_READ_SVS)
	g++ -m64 -O0 -lgomp -lomp -fopenmp $(SOURCE_READ_SVS) $(CXXFLAGS_METHOD03) 	-o $(TARGET_READ_SVS_METHOD03_DBG) $(LIBS_PROFILER)

read_svs_method12_dbg: $(SOURCE_READ_SVS)
	g++ -m64 -O0 -lgomp -lomp -fopenmp $(SOURCE_READ_SVS) $(CXXFLAGS_METHOD12) 	-o $(TARGET_READ_SVS_METHOD12_DBG) $(LIBS_PROFILER)

read_svs_method4_dbg: $(SOURCE_READ_SVS)
	g++ -m64 -O0 -lgomp -lomp -fopenmp $(SOURCE_READ_SVS) $(CXXFLAGS_METHOD4) 	-o $(TARGET_READ_SVS_METHOD4_DBG) $(LIBS_PROFILER)

read_svs_method5_dbg: $(SOURCE_READ_SVS)
	g++ -m64 -O0 -lgomp -lomp -fopenmp $(SOURCE_READ_SVS) $(CXXFLAGS_METHOD5) 	-o $(TARGET_READ_SVS_METHOD5_DBG) $(LIBS_PROFILER)


.PHONY: clean

clean:
	rm -f lib_read_svs*so
	rm -f read_svs_method*o
	rm -f read_svs_shared_lib*o
