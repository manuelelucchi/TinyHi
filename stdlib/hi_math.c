#include "hi_math.h"
#include "hi_assign.h"
#include <limits.h>

tiny_hi_object *negate(tiny_hi_object *right)
{
    check_not_null(right);
    if (is_int(right))
    {
        return assign_int(-as_int(right));
    }
    if (is_vector(right))
    {
        int *new = malloc(sizeof(int) * as_vector(right).length);
        foreach (i, right)
        {
            new[i] = -as_vector(right).data[i];
        }
        return assign_vector(new, as_vector(right).length);
    }
    raise_type_error(VECTOR_INT_TYPE_NAME, STRING_TYPE_NAME);
    return NULL;
}

void check_sum_overflow(int x, int y)
{
    if ((y > 0 && x > INT_MAX - y) || (y < 0 && x < INT_MIN - y))
    {
        raise_overflow_error(x, "+", y);
    }
}

void broadcast_sum(int *output, int len, int arg1, int arg1_sign, int *arg2, int arg2_sign)
{
    int i;
    for (i = 0; i < len; i++)
    {
        output[i] = arg2[i] * arg2_sign + arg1 * arg1_sign;
    }
}

tiny_hi_object *sum(tiny_hi_object *left, tiny_hi_object *right)
{
    check_not_null(left);
    check_not_null(right);
    if (is_int(left) && is_int(right))
    {
        check_sum_overflow(as_int(left), as_int(right));
        return assign_int(as_int(left) + as_int(right));
    }
    if (is_vector(left) && is_vector(right))
    {
        if (equal_size(left, right))
        {
            int len = as_vector(right).length;
            int *values = malloc(sizeof(c_int) * len);
            foreach (i, right)
            {
                int l = as_vector(left).data[i];
                int r = as_vector(right).data[i];
                check_sum_overflow(l, r);
                values[i] = l + r;
            }
            return assign_vector(values, len);
        }
        else
        {
            raise_size_error(as_vector(left).length, as_vector(right).length);
            return NULL;
        }
    }
    if (is_vector(left) && is_int(right))
    {
        int *out = malloc(sizeof(int) * as_vector(left).length);
        int len = as_vector(left).length;
        broadcast_sum(out, len, as_int(right), 1, as_vector(left).data, 1);
        return assign_vector(out, len);
    }
    if (is_int(left) && is_vector(right))
    {
        int *out = malloc(sizeof(int) * as_vector(right).length);
        int len = as_vector(right).length;
        broadcast_sum(out, len, as_int(left), 1, as_vector(right).data, 1);
        return assign_vector(out, len);
    }
    raise_type_error(VECTOR_INT_TYPE_NAME, STRING_TYPE_NAME);
    return NULL;
}

void check_sub_overflow(int x, int y)
{
    y = -y;
    if ((y > 0 && x > INT_MAX - y) || (y < 0 && x < INT_MIN - y))
    {
        raise_overflow_error(x, "-", y);
    }
}

tiny_hi_object *sub(tiny_hi_object *left, tiny_hi_object *right)
{
    check_not_null(left);
    check_not_null(right);
    if (is_int(left) && is_int(right))
    {
        check_sub_overflow(as_int(left), as_int(right));
        return assign_int(as_int(left) - as_int(right));
    }
    if (is_vector(left) && is_vector(right))
    {
        if (equal_size(left, right))
        {
            int len = as_vector(right).length;
            int *values = malloc(sizeof(int) * len);
            foreach (i, right)
            {
                int l = as_vector(left).data[i];
                int r = as_vector(right).data[i];
                check_sub_overflow(l, r);
                values[i] = l - r;
            }
            return assign_vector(values, len);
        }
        else
        {
            raise_size_error(as_vector(left).length, as_vector(right).length);
            return NULL;
        }
    }
    if (is_vector(left) && is_int(right))
    {
        int *out = malloc(sizeof(int) * as_vector(left).length);
        int len = as_vector(left).length;
        broadcast_sum(out, len, as_int(right), -1, as_vector(left).data, 1);
        return assign_vector(out, len);
    }
    if (is_int(left) && is_vector(right))
    {
        int *out = malloc(sizeof(int) * as_vector(right).length);
        int len = as_vector(right).length;
        broadcast_sum(out, len, as_int(left), 1, as_vector(right).data, -1);
        return assign_vector(out, len);
    }
    raise_type_error(VECTOR_INT_TYPE_NAME, STRING_TYPE_NAME);
    return NULL;
}

void check_mul_overflow(int left, int right)
{
    int res = left * right;
    if (left != 0 && res / left != right)
    {
        raise_overflow_error(left, "*", right);
    }
}

void broadcast_mul(int *output, int len, int arg1, int *arg2)
{
    int i;
    for (i = 0; i < len; i++)
    {
        output[i] = arg2[i] * arg1;
    }
}

tiny_hi_object *mul(tiny_hi_object *left, tiny_hi_object *right)
{
    check_not_null(left);
    check_not_null(right);
    if (is_int(left) && is_int(right))
    {
        check_mul_overflow(as_int(left), as_int(right));
        return assign_int(as_int(left) * as_int(right));
    }
    if (is_vector(left) && is_vector(right))
    {
        if (equal_size(left, right))
        {
            int len = as_vector(right).length;
            int *values = malloc(sizeof(int) * len);
            foreach (i, right)
            {
                int l = as_vector(left).data[i];
                int r = as_vector(right).data[i];
                check_mul_overflow(l, r);
                values[i] = l * r;
            }
            return assign_vector(values, len);
        }
        else
        {
            raise_size_error(as_vector(left).length, as_vector(right).length);
            return NULL;
        }
    }
    if (is_vector(left) && is_int(right))
    {
        int *out = malloc(sizeof(int) * as_vector(left).length);
        int len = as_vector(left).length;
        broadcast_mul(out, len, as_int(right), as_vector(left).data);
        return assign_vector(out, len);
    }
    if (is_int(left) && is_vector(right))
    {
        int *out = malloc(sizeof(int) * as_vector(right).length);
        int len = as_vector(right).length;
        broadcast_mul(out, len, as_int(left), as_vector(right).data);
        return assign_vector(out, len);
    }
    raise_type_error(VECTOR_INT_TYPE_NAME, STRING_TYPE_NAME);
    return NULL;
}

tiny_hi_object *division(tiny_hi_object *left, tiny_hi_object *right)
{
    check_not_null(left);
    check_not_null(right);
    if (is_int(left) && is_int(right))
    {
        int l = as_int(left);
        int r = as_int(right);
        if (r == 0)
        {
            raise_division_by_zero_error();
        }
        return assign_int(l / r);
    }
    if (is_vector(left) && is_vector(right))
    {
        if (equal_size(left, right))
        {
            int len = as_vector(right).length;
            int *values = malloc(sizeof(int) * len);
            foreach (i, right)
            {
                int l = as_vector(left).data[i];
                int r = as_vector(right).data[i];
                if (r == 0)
                {
                    raise_division_by_zero_error();
                }
                values[i] = l / r;
            }
            return assign_vector(values, len);
        }
        else
        {
            raise_size_error(as_vector(left).length, as_vector(right).length);
            return NULL;
        }
    }
    if (is_vector(left) && is_int(right))
    {
        int *out = malloc(sizeof(int) * as_vector(left).length);
        int len = as_vector(left).length;
        int i;
        for (i = 0; i < len; i++)
        {
            out[i] = as_vector(left).data[i] / as_int(right);
        }
        return assign_vector(out, len);
    }
    if (is_int(left) && is_vector(right))
    {
        int *out = malloc(sizeof(int) * as_vector(right).length);
        int len = as_vector(right).length;
        int i;
        for (i = 0; i < len; i++)
        {
            out[i] = as_int(left) / as_vector(right).data[i];
        }
        return assign_vector(out, len);
    }
    raise_type_error(VECTOR_INT_TYPE_NAME, STRING_TYPE_NAME);
    return NULL;
}