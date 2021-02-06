#ifndef HI_COMPARE_H
#define HI_COMPARE_H

#include "hi_object.h"
#include "stdbool.h"

// Performs left > right
tiny_hi_call bool mt(tiny_hi_object *left, tiny_hi_object *right);

// Performs left >= right
tiny_hi_call bool meq(tiny_hi_object *left, tiny_hi_object *right);

// Performs left < right
tiny_hi_call bool lt(tiny_hi_object *left, tiny_hi_object *right);

// Performs left <= right
tiny_hi_call bool leq(tiny_hi_object *left, tiny_hi_object *right);

// Performs left == right
tiny_hi_call bool eq(tiny_hi_object *left, tiny_hi_object *right);

// Performs left != right
tiny_hi_call bool neq(tiny_hi_object *left, tiny_hi_object *right);

#endif