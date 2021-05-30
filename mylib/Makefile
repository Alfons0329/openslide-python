# Required files
SOURCE_SHARED_LIB	:=read_svs_shared_lib.cpp
TARGET				:=mylib.so

# Compilers
CC=gcc

# Libraries and flags
# Absolute path will be better on NCHC machine
LDFLAGS		=-L/usr/local/lib
INCLUDES	=-I/usr/include/ -I/usr/local/include/openslide 
LIBS		=-ldl -lrt -lopenslide -fopenmp -ljpeg
RPATH		=-Wl,-rpath=/usr/local/lib/openslide-big-tile/ #For big tile openslide build (Suggested by prof Hung on Mar. 10, 2021)
CXXFLAGS	:= -Wall $(LDFLAGS) $(INCLUDES) $(LIBS) $(RPATH)

# Rules
all: $(SOURCE_SHARED_LIB)
	$(CC) -m64 -fPIC -O2 -shared -lgomp -lomp -fopenmp $(SOURCE_SHARED_LIB) $(CXXFLAGS) -o $(TARGET)

.PHONY: clean

clean:
	rm -f mylib*so