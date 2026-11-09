# Java String Is Not Mutable
keywords: immutable String, mutable variable, String methods, StringBuilder, reassignment, object state

- The claim that Java `String` objects are mutable is false: a `String` object's character sequence cannot be modified after construction.
- A method such as `concat()` returns a string containing the combined characters and does not mutate the receiver.
- If the returned value is ignored, the original string variable continues to refer to its original string.
- Reassigning a variable such as `s = s.concat("!")` makes `s` refer to the returned string; it does not alter the old object.
- `StringBuilder` is mutable and provides methods such as `append()` that modify its current character sequence.
- Immutability concerns the state of an object, not whether a variable can be assigned a different reference.
- The immutability of strings supports safe sharing and use of string literals.
- A `final String` reference cannot be reassigned after initialization, while a non-final `String` reference can be reassigned; neither case makes the String object mutable.
