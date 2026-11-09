# Abstract Classes
keywords: abstract class, abstract method, cannot instantiate, partial implementation, abstract keyword, concrete subclass
- An abstract class is never instantiated; it exists to express the common properties of its subclasses and to be a parent to related classes. It is declared with the abstract modifier in the class header.
- A class that is not abstract is a concrete class.
- Abstract classes cannot be instantiated with new, but can be used as variable types (a Shape variable can refer to a Rectangle).
- An abstract method has no implementation: modifiers, abstract, return type, signature, then a semicolon, with no braces or body. It is not the same as an empty method with braces.
- If a class has one or more abstract methods, it must be declared abstract; an abstract class may also contain fields and ordinary (concrete) methods that subclasses inherit.
- A non-abstract subclass must override every inherited abstract method with the same signature and same return type.
- A subclass that leaves some abstract methods undefined must itself be declared abstract; an abstract child of an abstract parent is fine.
- Defining a method with the parent's name but a different signature is an overload, not an override, so the child still has the abstract method and must be abstract.
- Same signature but a different return type from the parent's abstract method is an error.
- Abstract methods let calls such as shape.redraw() compile on the general type, while each concrete subclass supplies its own version.
