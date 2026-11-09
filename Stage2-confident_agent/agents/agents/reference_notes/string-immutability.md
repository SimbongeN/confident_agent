# String Immutability in Java
keywords: String, immutability, immutable object, string pool, concatenation, equals, thread safety

- Java `String` objects are immutable: once a `String` object has been created, its character sequence cannot be changed.
- Operations such as `toUpperCase()` and `replace()` return a result string rather than changing the original object.
- Assigning the result of a string operation back to a variable changes the variable's reference, not the existing string object.
- String literals can be shared through the string pool, which is safe because their contents cannot be mutated.
- Immutability helps make strings suitable for use as map keys because their hash-relevant contents do not change.
- The `String` class provides methods that produce new strings when a different sequence is needed.
- For repeated mutable text construction, `StringBuilder` is often more suitable than creating many intermediate strings.
- A variable declared as `String` can be reassigned to another string even though each individual `String` object is immutable.
