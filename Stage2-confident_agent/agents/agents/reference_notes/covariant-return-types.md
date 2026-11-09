# Covariant Return Types
keywords: covariant return type, covariant return, return type substitutability, overriding return type

- A covariant return type allows an overriding method to return a more specific reference type than the method it overrides.
- The overriding method's return type must be return-type-substitutable for the inherited method's return type.
- For reference types, this commonly means the overriding method returns a subtype of the original return type.
- For example, if a superclass method returns `Animal`, an overriding subclass method may return `Dog` when `Dog` extends `Animal`.
- Covariant return types apply to overriding, not to distinguishing overloaded methods.
- A primitive return type cannot be replaced by a different primitive type merely because one type seems narrower.
- Java has supported covariant return types for overridden methods since Java 5.
- A covariant return type lets callers using the subclass type receive a more specific result without an explicit cast.
