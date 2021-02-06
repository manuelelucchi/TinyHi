#ifndef HI_IO_H
#define HI_IO_H

#include "hi_object.h"

// Reads a string from the standard input and puts it into the output variable
tiny_hi_call tiny_hi_object *input();

// Outputs the input as a string, a vector with the elements separated by a space, or as an int. In all the ways they are followed by a return.
tiny_hi_call void output(tiny_hi_object *input);

#endif