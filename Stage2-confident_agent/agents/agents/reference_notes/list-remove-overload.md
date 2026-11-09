# List Remove Overloads in Java
keywords: List.remove, remove(int index), remove(Object), overload resolution, Integer, autoboxing, element removal

- Java's `List` interface declares `remove(int index)`, which removes and returns the element at the specified position.
- `List` also declares `remove(Object o)`, which removes the first occurrence equal to the supplied object and returns a boolean.
- These are overloaded methods because they share the name `remove` but have different parameter types.
- When the compile-time argument is an `int`, `remove(int)` is selected if it is applicable.
- For a `List<Integer>`, calling `list.remove(1)` normally removes the element at index 1, not the integer value `1`.
- To remove the integer value from a `List<Integer>`, pass an `Integer` object, for example `list.remove(Integer.valueOf(1))`.
- `remove(int)` can throw `IndexOutOfBoundsException` when the index is outside the list's valid range.
- `remove(Object)` removes only the first matching occurrence; if no matching element exists, the list remains unchanged.
