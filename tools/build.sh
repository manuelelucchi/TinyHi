clang \
    -Wno-varargs \
    -Wno-deprecated-declarations \
    -shared \
    -o bin/tiny_hi_core.dylib \
    -O3 \
    -I ./ \
    stdlib/hi_math.c \
    stdlib/hi_compare.c \
    stdlib/hi_io.c \
    stdlib/hi_assign.c \
    stdlib/hi_enumeration.c \
    stdlib/hi_memory.c

cd bin

rm -rf *.lib *.exp

cd ..