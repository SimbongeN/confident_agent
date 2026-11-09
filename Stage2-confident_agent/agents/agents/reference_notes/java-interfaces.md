# Java Interfaces
keywords: Java interface, implements, abstract method, default method, static method, multiple inheritance of type, interface contract

- An interface declares a reference type that classes can implement and other interfaces can extend.
- A class uses the `implements` keyword to state that it provides the interface's required behaviour.
- A class can implement more than one interface, allowing it to support multiple types without extending multiple classes.
- Ordinary abstract interface methods are implicitly `public` and abstract unless otherwise specified by the language rules.
- An interface can contain `default` methods with implementations, as well as permitted `static` and `private` methods.
- Fields declared in an interface are implicitly `public`, `static`, and `final`.
- A concrete class must implement the inherited abstract interface methods unless a suitable implementation is inherited.
- If two interfaces provide conflicting inherited default methods with the same signature, the implementing class must resolve the conflict.
- An interface cannot be instantiated directly, but a variable declared with an interface type can refer to an implementing object.
