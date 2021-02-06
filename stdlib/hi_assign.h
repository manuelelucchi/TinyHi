#ifndef HI_ASSIGN_H
#define HI_ASSIGN_H

#include "hi_object.h"

// Assign -1 to the type
tiny_hi_call tiny_hi_object *assign_empty();

// Copy the value of the given object
tiny_hi_call tiny_hi_object *assign_object(tiny_hi_object *from);

// Set int as the type and copy the value of the input
tiny_hi_call tiny_hi_object *assign_int(c_int from);

// Set string as the type and copy the value of the input
tiny_hi_call tiny_hi_object *assign_string(c_str from);

// Set vector as the type and copy the value of the input
tiny_hi_call tiny_hi_object *assign_vector(c_int *data, c_int len);

// Set vector or string as the type and copy the values of the input
tiny_hi_call tiny_hi_object *assign_concatenation(int number, ...);

#endif