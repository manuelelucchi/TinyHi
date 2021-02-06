#ifndef HI_ERROR_H
#define HI_ERROR_H

#include "hi_common.h"
#include <stdio.h>
#include <stdlib.h>

#define OBJECT_UNDEFINED_ERROR "ObjectUndefinedError\n"
#define OBJECT_UNDEFINED_ERROR_MESSAGE "The object was undefined\n"

inline void raise_object_undefined_error()
{
  printf(OBJECT_UNDEFINED_ERROR);
  printf(OBJECT_UNDEFINED_ERROR_MESSAGE);
  exit(1);
}

#define TYPE_ERROR "TypeError\n"
#define TYPE_ERROR_MESSAGE "Expected type %s, but %s was given\n"

inline void raise_type_error(c_str expected, c_str given)
{
  printf(TYPE_ERROR);
  printf(TYPE_ERROR_MESSAGE, expected, given);
  exit(1);
}

#define OVERFLOW_ERROR "OverflowError"
#define OVERFLOW_ERROR_MESSAGE "The operation %d %s %d results in an overflow\n"

inline void raise_overflow_error(int left, c_str op, int right)
{
  printf(OVERFLOW_ERROR);
  printf(OVERFLOW_ERROR_MESSAGE, left, op, right);
  exit(1);
}

#define DIVISION_BY_ZERO_ERROR "DivisionByZeroError\n"
#define DIVISION_BY_ZERO_ERROR_MESSAGE "Attempt to perform a division by 0\n"

inline void raise_division_by_zero_error()
{
  printf(DIVISION_BY_ZERO_ERROR);
  printf(DIVISION_BY_ZERO_ERROR_MESSAGE);
  exit(1);
}

#define INDEX_OUT_OF_BOUND_ERROR "IndexOutOfBoundError\n"
#define INDEX_OUT_OF_BOUND_ERROR_MESSAGE \
  "Trying to access an %d element array with the index %d\n"

inline void raise_index_out_of_bound_error(int len, int index)
{
  printf(INDEX_OUT_OF_BOUND_ERROR);
  printf(INDEX_OUT_OF_BOUND_ERROR_MESSAGE, len, index);
  exit(1);
}

#define SUBSCRIPTING_ERROR "SubscriptingError\n"
#define SUBSCRIPTING_ON_INT_ERROR_MESSAGE "Trying to subscribe an int\n"

inline void raise_subscripting_on_int_error()
{
  printf(SUBSCRIPTING_ERROR);
  printf(SUBSCRIPTING_ON_INT_ERROR_MESSAGE);
  exit(1);
}

#define SUBSCRIPTING_WITH_ENUMERABLE_ERROR \
  "Trying to subscribe an element using a %s\n"

inline void raise_subscripting_with_enumerable_error(c_str index_type)
{
  printf(SUBSCRIPTING_ERROR);
  printf(SUBSCRIPTING_WITH_ENUMERABLE_ERROR, index_type);
  exit(1);
}

#define CONCATENATION_ERROR "ConcatenationError\n"
#define CONCATENATION_ERROR_MESSAGE \
  "Trying to concatenate element of type %s with %s\n"

inline void raise_concatenation_error(c_str type1, c_str type2)
{
  printf(CONCATENATION_ERROR);
  printf(CONCATENATION_ERROR_MESSAGE, type1, type2);
  exit(1);
}

#define SIZE_ERROR "SizeError\n"
#define SIZE_ERROR_MESSAGE "Size mismatch between arrays of length %d and %d"

inline void raise_size_error(int right, int left)
{
  printf(SIZE_ERROR);
  printf(SIZE_ERROR_MESSAGE, right, left);
  exit(1);
}

#define COMPARE_ERROR "CompareError\n"
#define COMPARE_ERROR_MESSAGE "You can't compare %s with %s\n"

inline void raise_compare_error(c_str right, c_str left)
{
  printf(COMPARE_ERROR);
  printf(COMPARE_ERROR_MESSAGE, right, left);
  exit(1);
}

#define SIZE_COHERENCE_ERROR "SizeCoherenceError\n"
#define SIZE_COHERENCE_ERROR_MESSAGE "Different sizes while concatenating: %d != %d\n"

inline void raise_size_coherence_error(c_int right, c_int left)
{
  printf(SIZE_COHERENCE_ERROR);
  printf(SIZE_COHERENCE_ERROR_MESSAGE, right, left);
  exit(1);
}

#define STACK_CORRUPTION_ERROR "StackCorruptionError\n"
#define STACK_CORRUPTION_ERROR_MESSAGE "The stack is corrupted\n"

inline void raise_stack_corruption_error()
{
  printf(STACK_CORRUPTION_ERROR);
  printf(STACK_CORRUPTION_ERROR_MESSAGE);
  exit(1);
}

#endif