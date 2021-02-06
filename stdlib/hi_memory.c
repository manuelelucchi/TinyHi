#include "hi_memory.h"
#include <memory.h>
#include <string.h>

struct _Node
{
    struct _Node *previous;
    tiny_hi_object value;
    int level;
};

typedef struct _Node Node;

struct _Stack
{
    Node *head;
};

typedef struct _Stack Stack;

static Stack *s = NULL;
static int current_level = 0;

void free_object(tiny_hi_object *o)
{
    if (is_vector(o) && as_vector(o).length > 0)
    {
        free(as_vector(o).data);
        as_vector(o).data = NULL;
        as_vector(o).length = 0;
    }
    if (is_string(o) && strlen(as_string(o)) > 0)
    {
        free(as_string(o));
        as_string(o) = NULL;
    }
    o->type = -1;
}

void activate()
{
    if (s == NULL)
    {
        s = malloc(sizeof(Stack));
        s->head = NULL;
    }
    current_level++;
}

void collect()
{
    if (s == NULL)
    {
        raise_stack_corruption_error();
        return;
    }
    Node *last = s->head;
    while (last != NULL)
    {
        if (last->level == current_level)
        {
            free_object(&(last->value));
        }
        else
        {
            s->head = last;
            break;
        }
        Node *oldLast = last;
        last = last->previous;
        free(oldLast);
    }
    current_level--;
}

void copy(tiny_hi_object *src, tiny_hi_object *dest)
{
    if (is_vector(src))
    {
        dest->type = VECTOR_TYPE_HI;
        int len = as_vector(src).length;
        as_vector(dest).data = malloc(len * sizeof(c_int));
        as_vector(dest).length = len;
        memcpy(as_vector(dest).data, as_vector(src).data, len * sizeof(c_int));
        return;
    }

    if (is_string(src))
    {
        dest->type = STRING_TYPE_HI;
        int len = strlen(as_string(src)) + 1;
        as_string(dest) = malloc(len * sizeof(c_int));
        strcpy(as_string(dest), as_string(src));
        return;
    }

    if (is_int(src))
    {
        dest->type = INT_TYPE_HI;
        as_int(dest) = as_int(src);
        return;
    }

    dest->type = -1;
}

tiny_hi_object *return_and_collect(tiny_hi_object *obj)
{
    Node *n = malloc(sizeof(Node));
    copy(obj, &(n->value));
    collect();
    n->level = current_level;
    return &(n->value);
}

tiny_hi_object *alloc()
{
    if (s == NULL)
    {
        s = malloc(sizeof(Stack));
        s->head = NULL;
    }

    Node *n = malloc(sizeof(Node));
    tiny_hi_object *ref = &(n->value);
    ref->type = -1;
    n->level = current_level;
    if (s->head == NULL)
    {
        n->previous = NULL;
    }
    else
    {
        Node *oldHead = s->head;
        n->previous = oldHead;
    }
    s->head = n;

    return ref;
}

static Stack *globals = NULL;

tiny_hi_object *alloc_global()
{
    if (globals == NULL)
    {
        globals = malloc(sizeof(Stack));
        globals->head = NULL;
    }

    Node *n = malloc(sizeof(Node));
    n->value.type = -1;
    n->level = 0;

    if (globals->head == NULL)
    {
        globals->head = n;
    }
    else
    {
        n->previous = globals->head;
        globals->head = n;
    }

    return &(n->value);
}

void collect_globals()
{
    if (globals == NULL)
    {
        return;
    }
    Node *last = globals->head;
    while (last != NULL)
    {
        free_object(&(last->value));
        Node *oldLast = last;
        last = last->previous;
        free(oldLast);
    }
    if (globals != NULL)
    {
        free(globals);
        globals = NULL;
    }
}