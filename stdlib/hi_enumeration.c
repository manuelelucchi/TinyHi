#include "hi_enumeration.h"
#include <stdarg.h>
#include <stdbool.h>
#include "hi_assign.h"
#include "hi_error.h"
#include "string.h"

int _length(tiny_hi_object *input)
{
    if (is_int(input))
    {
        return 1;
    }
    if (is_vector(input))
    {
        return as_vector(input).length;
    }
    if (is_string(input))
    {
        return strlen(as_string(input));
    }
    raise_object_undefined_error();
    return 0;
}

tiny_hi_object *length(tiny_hi_object *input)
{
    check_not_null(input);
    int len = _length(input);
    return assign_int(len);
}

tiny_hi_object *subscribe(tiny_hi_object *input, int number, ...)
{
    check_not_null(input);
    if (is_empty(input))
    {
        raise_object_undefined_error();
    }
    if (is_int(input))
    {
        raise_subscripting_on_int_error();
    }
    va_list ap;
    int i = 0;
    int doubleNumber = number * 2;
    va_start(ap, doubleNumber);
    int *indexes = malloc(sizeof(int) * number);
    for (i = 0; i < number; i++)
    {
        int type = va_arg(ap, int);
        switch (type)
        {
        case VA_INT:
        {
            int val = va_arg(ap, int);
            indexes[i] = val;
            break;
        }
        case VA_OBJECT:
        {
            tiny_hi_object *val = va_arg(ap, tiny_hi_object *);
            if (is_int(val))
            {
                indexes[i] = as_int(val);
            }
            else
            {
                raise_subscripting_with_enumerable_error(type_to_name(val->type));
            }
            break;
        }
        default:
            raise_object_undefined_error();
            break;
        }
    }
    va_end(ap);

    if (is_vector(input))
    {
        int j;
        int *out = malloc(sizeof(int) * number);
        int inputLen = as_vector(input).length;
        for (j = 0; j < number; j++)
        {
            int oldIndex = indexes[j];
            int index = oldIndex - 1;
            if (index >= inputLen)
            {
                raise_index_out_of_bound_error(inputLen, oldIndex);
            }
            out[j] = as_vector(input).data[index];
        }
        return assign_vector(out, number);
    }
    if (is_string(input))
    {
        int j;
        char *out = malloc(sizeof(char) * (number + 1));
        int inputLen = strlen(as_string(input));
        for (j = 0; j < number; j++)
        {
            int oldIndex = indexes[j];
            int index = oldIndex - 1;
            if (index >= inputLen)
            {
                raise_index_out_of_bound_error(inputLen, oldIndex);
            }
            out[j] = as_string(input)[index];
        }
        out[number] = '\0';
        return assign_string(out);
    }
    free(indexes);
    return NULL;
}