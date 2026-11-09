# Garbage Collection
keywords: garbage collection, garbage collector, memory management, unreachable object, finalize, reference, destroy objects
- Objects live in the heap and can only be reached through variables holding references to them.
- An object becomes garbage when no variable refers to it any more; for example, setting the only referencing variable to null.
- An object with several references does not become garbage until all of those references have been dropped.
- Java uses garbage collection to reclaim memory from inaccessible objects automatically; the system, not the programmer, tracks which objects are garbage.
- In many other languages the programmer must delete objects; the book names two resulting errors: a dangling pointer (deleting an object that is still referenced) and a memory leak (failing to delete objects no longer in use).
- Because Java uses garbage collection, the book says dangling pointer errors and memory leaks of this kind are impossible.
- The book says garbage collection has been used since the 1960s and was once considered too slow and wasteful, but is now feasible.
