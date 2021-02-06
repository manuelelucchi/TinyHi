#include "hi_compare.h"
#include "hi_error.h"
#include <string.h>
#include <limits.h>

// Utils

int vector_max(int *val, int len)
{
    int max = INT_MIN;
    int i = 0;
    for (; i < len; i++)
    {
        int v = val[i];
        max = max < v ? v : max;
    }
    return max;
}

int string_max(char *val)
{
    int len = strlen(val);
    int max = INT_MIN;
    int i = 0;
    for (; i < len; i++)
    {
        int v = val[i];
        max = max < v ? v : max;
    }
    return max;
}

bool mt(tiny_hi_object *left, tiny_hi_object *right)
{
    check_not_null(left);
    check_not_null(right);
    if (is_int(left) && is_int(right))
    {
        return as_int(left) > as_int(right);
    }
    if (is_string(left) && is_string(right))
    {
        return string_max(as_string(left)) > string_max(as_string(right));
    }
    if (is_vector(left) && is_vector(right))
    {
        return vector_max(as_vector(left).data, as_vector(left).length) > vector_max(as_vector(right).data, as_vector(right).length);
    }
    raise_compare_error(get_type(left), get_type(right));
    return false;
}

bool meq(tiny_hi_object *left, tiny_hi_object *right)
{
    return (mt(left, right) || eq(left, right));
}

bool lt(tiny_hi_object *left, tiny_hi_object *right)
{
    return !(mt(left, right) || eq(left, right));
}

bool leq(tiny_hi_object *left, tiny_hi_object *right)
{
    return !mt(left, right);
}

bool eq(tiny_hi_object *left, tiny_hi_object *right)
{
    check_not_null(left);
    check_not_null(right);
    if (is_int(left) && is_int(right))
    {
        return as_int(left) == as_int(right);
    }
    if (is_string(left) && is_string(right))
    {
        if (strlen(as_string(left)) == strlen(as_string(right)))
        {
            int i = 0;
            for (; i < strlen(as_string(left)); i++)
            {
                if (as_string(left)[i] != as_string(right)[i])
                {
                    return false;
                }
            }
            return true;
        }
        return false;
    }
    if (is_vector(left) && is_vector(right))
    {
        if (as_vector(left).length == as_vector(right).length)
        {
            foreach (i, left)
            {
                if (as_vector(left).data[i] != as_vector(right).data[i])
                {
                    return false;
                }
                return true;
            }
        }
        return false;
    }
    return false;
}

bool neq(tiny_hi_object *left, tiny_hi_object *right)
{
    return !eq(left, right);
}