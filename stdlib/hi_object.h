#ifndef HI_OBJECT_H
#define HI_OBJECT_H

#include "hi_common.h"
#include "hi_error.h"

struct tiny_hi_vector_s
{
    int length;
    int *data;
};

typedef struct tiny_hi_vector_s tiny_hi_vector;

union tiny_hi_data_u
{
    int integer;
    tiny_hi_vector vector;
    c_str string;
};

typedef union tiny_hi_data_u tiny_hi_data;

struct tiny_hi_object_s
{
    tiny_hi_data data;
    tiny_hi_type type;
};

typedef struct tiny_hi_object_s tiny_hi_object;

#define is_int(arg) (arg->type == INT_TYPE_HI)
#define is_vector(arg) (arg->type == VECTOR_TYPE_HI)
#define is_string(arg) (arg->type == STRING_TYPE_HI)
#define is_empty(arg) (arg->type != INT_TYPE_HI && arg->type != VECTOR_TYPE_HI && arg->type != STRING_TYPE_HI)

#define foreach(i, in) \
    int i;             \
    for (i = 0; i < as_vector(in).length; i++)

#define as_vector(input) input->data.vector
#define as_int(input) input->data.integer
#define as_string(input) input->data.string

#define equal_size(arg1, arg2) (as_vector(arg1).length == as_vector(arg2).length)

// Returns a string representing the type of the object
inline c_str get_type(tiny_hi_object *value)
{
    return type_to_name(value->type);
}

// Check if the object is null
inline void check_not_null(tiny_hi_object *value)
{
    if (is_empty(value))
    {
        raise_object_undefined_error();
    }
}

#endif