#include "hi_io.h"
#include "hi_error.h"

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "hi_assign.h"

#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Wimplicit-function-declaration"

c_str scan_string()
{
    char user_input[255];
    gets(user_input);
    size_t len = strlen(user_input);
    char *buffer = malloc(sizeof(char) * len);
    strcpy(buffer, user_input);
    return buffer;
}

#pragma clang diagnostic pop

tiny_hi_object *input()
{
    return assign_string(scan_string());
}

void output(tiny_hi_object *input)
{
    if (is_int(input))
    {
        printf("%d\n", as_int(input));
        return;
    }
    if (is_vector(input))
    {
        int i = 0;
        for (; i < as_vector(input).length; i++)
        {
            printf("%d ", as_vector(input).data[i]);
        }
        printf("\n");
        return;
    }
    if (is_string(input))
    {
        printf("%s\n", as_string(input));
        return;
    }
    raise_object_undefined_error();
}