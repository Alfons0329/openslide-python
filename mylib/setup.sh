#/bin/bash
set -e

if [ $# -ne 2 ]
then
    echo "Usage: ./setup.sh $/path/to/openslide/top/folder $/path/to/writable/lib (absolute path and exclude the last /)"
    echo "I have the permission to write /usr/local/lib and my openslide top folder is /home/user/homework/openslide, then use the following: "
    echo "./setup.sh /home/user/homework/openslide /usr/local/lib"
    exit -1
fi

path_openslide=$1
path_writable_lib=$2
path_here=$(pwd)

# Overweite the original openslide source code
cat openslide.c > $path_openslide/src/openslide.c
cd $path_openslide/build 
make clean && make -j8 && sudo make install -j8

# Cp the shared object to the designated path in Makefile
sudo mkdir -p $path_writable_lib/
sudo cp /usr/local/lib/libopenslide.so* $path_writable_lib/openslide-big-tile/

# Cd back, modify Makefile and make
cd $path_here 
sed_write="RPATH=-Wl,-rpath=$path_writable_lib/openslide-big-tile/"
sed -i "13s|.*|$sed_write|" Makefile # use | as delimiter to avoid Unkonw option to `s' error (Ref: https://stackoverflow.com/questions/33914360/what-delimiters-can-you-use-in-sed)
make clean && make -j8
rpath_result=$(ldd mylib.so | grep openslide)
echo $rpath_result

if [[ $rpath_result =~ "big-tile" ]]
then
    echo "Shared object file rpath linked to $path_writable_lib/openslide-big-tile/ success!"
else
    echo "Shared object file rpath linked to $path_writable_lib/openslide-big-tile/ failed!"
    make clean
fi