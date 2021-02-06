#ifndef HI_ENUMERATION_H
#define HI_ENUMERATION_H

#include "hi_object.h"

// Returns the length of the string, vector or 1 if it's an integer
tiny_hi_call tiny_hi_object *length(tiny_hi_object *input);

// Returns a vector or string with the elements subscribed from the input indexes
tiny_hi_call tiny_hi_object *subscribe(tiny_hi_object *input, int number, ...);

#endif