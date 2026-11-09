# Marker Interfaces
keywords: marker interface, empty interface, type marker, Serializable, Cloneable, runtime type check, metadata

- A marker interface is an interface with no method declarations, used to indicate that a class has a particular property or capability.
- A class marks itself by declaring that it implements the marker interface.
- Code can test whether an object has the marker type using `instanceof` or type-based APIs.
- Java's `java.io.Serializable` is a well-known marker interface that indicates that instances may be serialized under Java serialization rules.
- Java's `Cloneable` is another marker interface; it affects the behaviour of `Object.clone()`.
- A marker interface communicates its marker through the type system and can be checked by the compiler and runtime.
- An annotation can be an alternative when metadata is needed without defining a new type relationship.
- A marker interface does not automatically implement behaviour or guarantee that every operation associated with the marker will succeed.
