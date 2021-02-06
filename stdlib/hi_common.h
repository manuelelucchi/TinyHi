#ifndef COMMON_HI
#define COMMON_HI

#ifdef _WIN32
#define tiny_hi_call __declspec(dllexport)
#else
#define tiny_hi_call
#endif

typedef unsigned char tiny_hi_type;
typedef char *c_str;
typedef int c_int;
typedef int *c_vec;
typedef void *c_ptr;

#define NULL_HI (void *)0

#define INT_TYPE_HI 0
#define VECTOR_TYPE_HI 1
#define STRING_TYPE_HI 2

#define VA_INT 0
#define VA_OBJECT 1
#define VA_STRING 2

#define INT_TYPE_NAME "Int"
#define VECTOR_TYPE_NAME "Vector"
#define VECTOR_INT_TYPE_NAME "Vector/Int"
#define STRING_TYPE_NAME "String"
#define UNDEFINED_TYPE_NAME "Undefined"

inline c_str type_to_name(c_int type)
{
    switch (type)
    {
    case INT_TYPE_HI:
        return INT_TYPE_NAME;
    case STRING_TYPE_HI:
        return STRING_TYPE_NAME;
    case VECTOR_TYPE_HI:
        return VECTOR_TYPE_NAME;
    default:
        return UNDEFINED_TYPE_NAME;
    }
}

#endif