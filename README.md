# TinyHi

This a very rough implementation of the TinyHi programming language, with the specifications described on the TinyHi.pdf file. Made for the LeT course at Unimi.

## Build the STL
Requirements: the clang compiler
On Windows, run the build.sh file. On MacOS, run the build.sh file. 

## Install the dependencies
Requirements: a python interpreter.
First, you need to install the libraries from the requirements.txt file. Liblet is a special case, since you also have to configure ANTLR. The best way is to look at its [documentation](https://liblet.readthedocs.io/en/v1.2.3-beta/)

## Run
Now you can just import ```tiny.run``` and call ```run(s)``` where ```s``` is a string containing some TinyHi source code. 