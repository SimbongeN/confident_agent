# Interfaces
keywords: interface, implements, default method, interface vs abstract class, multiple inheritance, contract, functional interface, interface type
- An interface is a set of requirements a class must implement: a list of constants and method declarations with no method bodies; variables are not allowed. No objects can be constructed from an interface.
- Java has single inheritance for classes, but a class can implement any number of interfaces: class X extends Parent implements InterfaceA, InterfaceB. A class with no extends clause extends Object.
- Interface methods are implicitly public and abstract; constants are implicitly public static final (a value must still be given). A method in an interface cannot be private.
- A class implementing an interface must define every method in it, declared public in the class; interface constants can be used as if defined in the class and should not be redefined.
- If two interfaces ask for the same method, one definition satisfies both; the same constant should not be defined in several interfaces.
- An interface can be used as a reference variable type; the compiler allows only the methods declared in the interface (e.g. a Taxable variable cannot call display()).
- A type cast tells the compiler a variable refers to a specific class (e.g. ((Book)item1).display()), and may be needed to move between an interface type and a class type.
- An interface can extend another interface but not a class; a class cannot extend an interface.
- Default methods (Java 8) have an implementation and are marked default; implementing classes need not override them but may. They are automatically public and cannot add instance variables, so this is not true multiple inheritance (similar to a mixin).
- Abstract class versus interface (book's table): abstract class variables have no restrictions and it has constructors (invoked via constructor chaining); interface variables must be public static final, it has no constructors, and methods are public abstract instance methods. Neither can be instantiated with new.
