#include "hi_assign.h"
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
#include "hi_error.h"
#include <stdarg.h>
#include "hi_memory.h"
#include "hi_error.h"

tiny_hi_object *assign_empty()
{
    return alloc();
}

tiny_hi_object *assign_object(tiny_hi_object *from)
{
    if (is_int(from))
    {
        return assign_int(as_int(from));
    }
    if (is_vector(from))
    {
        return assign_vector(as_vector(from).data, as_vector(from).length);
    }
    if (is_string(from))
    {
        return assign_string(as_string(from));
    }
    if (is_empty(from))
    {
        return assign_empty();
    }
    return NULL;
}

tiny_hi_object *assign_int(c_int from)
{
    tiny_hi_object *to = alloc();
    as_int(to) = from;
    to->type = INT_TYPE_HI;
    return to;
}

tiny_hi_object *assign_string(c_str from)
{
    tiny_hi_object *to = alloc();
    as_string(to) = malloc(sizeof(char) * (strlen(from) + 1));
    strcpy(as_string(to), from);
    to->type = STRING_TYPE_HI;
    return to;
}

tiny_hi_object *assign_vector(c_int *data, c_int len)
{
    tiny_hi_object *to = alloc();
    as_vector(to).data = malloc(sizeof(c_int) * len);
    as_vector(to).length = len;
    memcpy(as_vector(to).data, data, sizeof(c_int) * len);
    to->type = VECTOR_TYPE_HI;
    return to;
}

/*
Prima di tutto controllo i tipi dei valori passati con i varargs usando gli interi che li precedono.
Inoltre conto la lunghezza di ogni input in modo da poter avere la lunghezza dell'output finale.
Se pero' tra interi e vettori si trova una stringa o viceversa, viene annullato tutto e dato errore.
Se si puo' procedere, vengono presi i valori e copiati nell'output
*/
tiny_hi_object *assign_concatenation(int number, ...)
{
    va_list ap;
    int i = 0;
    int doubleNumber = number * 2;
    va_start(ap, doubleNumber);
    bool one_is_string = false;
    bool all_string = true;
    bool one_is_empty = false;

    int vector_len = 0;
    int string_len = 0;
    for (i = 0; i < number; i++)
    {
        int type = va_arg(ap, int);
        switch (type)
        {
        case VA_INT:
        {
            int val = va_arg(ap, int);
            all_string = false;
            vector_len++;
            break;
        }
        case VA_OBJECT:
        {
            tiny_hi_object *val = va_arg(ap, tiny_hi_object *);
            if (is_string(val))
            {
                one_is_string = true;
                string_len += strlen(as_string(val));
            }
            else
            {
                if (is_vector(val))
                {
                    vector_len += as_vector(val).length;
                }
                else if (is_int(val))
                {
                    vector_len += 1;
                }
                else
                {
                    raise_object_undefined_error();
                }
                all_string = false;
            }
            break;
        }
        case VA_STRING:
        {
            char *val = va_arg(ap, char *);
            one_is_string = true;
            string_len += strlen(val);
            break;
        }
        default:
            raise_object_undefined_error();
            break;
        }
    }
    va_end(ap);

    if (one_is_empty)
    {
        raise_object_undefined_error();
    }

    if (one_is_string && !all_string)
    {
        raise_concatenation_error(VECTOR_INT_TYPE_NAME, STRING_TYPE_NAME);
    }

    if (all_string)
    {
        int counter = 0;
        int j;
        va_start(ap, doubleNumber);
        char **container = malloc(sizeof(char **) * number);
        for (j = 0; j < number; j++)
        {
            int type = va_arg(ap, int);
            char *str = NULL;
            if (type == VA_STRING)
            {
                str = va_arg(ap, char *);
            }
            if (type == VA_OBJECT)
            {
                tiny_hi_object *o = va_arg(ap, tiny_hi_object *);
                str = as_string(o);
            }
            counter += strlen(str);
            container[j] = str;
        }
        va_end(ap);

        c_str str = malloc(sizeof(char) * (counter + 1));
        int c = 0;
        for (j = 0; j < number; j++)
        {
            char *current_str = container[j];
            int current_len = strlen(current_str);
            memcpy(str + c, current_str, sizeof(char) * current_len);
            c += current_len;
        }
        if (c != string_len)
        {
            raise_size_coherence_error(c, string_len);
        }
        str[counter] = '\0';

        free(container);
        return assign_string(str);
    }

    if (!one_is_string && !all_string)
    {
        c_vec vec = malloc(sizeof(c_int) * vector_len);
        int counter = 0;
        va_start(ap, doubleNumber);
        int j;
        for (j = 0; j < number; j++)
        {
            int type = va_arg(ap, int);
            if (type == VA_INT)
            {
                vec[counter] = va_arg(ap, int);
                counter++;
                continue;
            }
            if (type == VA_OBJECT)
            {
                tiny_hi_object *v = va_arg(ap, tiny_hi_object *);
                if (is_vector(v))
                {
                    int len = as_vector(v).length;
                    memcpy(vec + counter, as_vector(v).data, len * sizeof(c_int));
                    counter += len;
                }
                if (is_int(v))
                {
                    vec[counter] = as_int(v);
                    counter++;
                }
            }
        }
        if (counter != vector_len)
        {
            raise_size_coherence_error(counter, vector_len);
        }
        return assign_vector(vec, counter);
    }
    return NULL;
}