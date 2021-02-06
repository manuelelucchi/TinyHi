#ifndef HI_MATH_H
#define HI_MATH_H

#include "hi_error.h"
#include "hi_object.h"

// Negate the input if it's an int or vector, raises an error if it's a string
tiny_hi_call tiny_hi_object *negate(tiny_hi_object *right);

// Sums the inputs if they are: (int,int), (vector,vector) of the same size, (vector, int), (int, vector). Raises an error in all the other cases or if it causes overflow
tiny_hi_call tiny_hi_object *sum(tiny_hi_object *left, tiny_hi_object *right);

// Subs the inputs if they are: (int,int), (vector,vector) of the same size, (vector, int), (int, vector). Raises an error in all the other cases or if it causes overflow
tiny_hi_call tiny_hi_object *sub(tiny_hi_object *left, tiny_hi_object *right);

// Multiplies the inputs if they are: (int,int), (vector,vector) of the same size, (vector, int), (int, vector). Raises an error in all the other cases or if it causes overflow
tiny_hi_call tiny_hi_object *mul(tiny_hi_object *left, tiny_hi_object *right);

// Divide the inputs if they are: (int,int), (vector,vector) of the same size, (vector, int), (int, vector). Raises an error in all the other cases or if there is a division by 0
tiny_hi_call tiny_hi_object *division(tiny_hi_object *left, tiny_hi_object *right);

#endif