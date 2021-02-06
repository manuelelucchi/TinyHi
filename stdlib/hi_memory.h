#ifndef HI_MEMORY_H
#define HI_MEMORY_H

#include "hi_object.h"

// Increase the current scope counter by one
tiny_hi_call void activate();

// Frees and removes the references of all the variables in the current scope, then decrease by one the scope counter.
tiny_hi_call void collect();

// A dedicated version of memcpy for tiny hi objects
tiny_hi_call void copy(tiny_hi_object *src, tiny_hi_object *dest);

tiny_hi_call tiny_hi_object *return_and_collect(tiny_hi_object *obj);

// Allocs a new variable and adds it to the stack with a reference on the current scope.
tiny_hi_object *alloc();

// Allocs a new global variable and adds it to the 'globals stack'
tiny_hi_call tiny_hi_object *alloc_global();

// Frees all the globals variables and resets the 'globals stack'
tiny_hi_call void collect_globals();

#endif