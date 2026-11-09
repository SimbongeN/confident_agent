# Inheritance
keywords: inheritance, extends, subclass, superclass, super, is-a, derived class, base class, reuse, subclass constructor
- Inheritance defines a new class (child/subclass/derived class) based on an existing class (parent/superclass/base class); the child inherits both variables and methods and can add more.
- Syntax: class Child extends Parent.
- Java has single inheritance: a class has only one parent, though a parent can have any number of children; Java avoids multiple inheritance problems this way.
- Inheritance is "is-a" and goes one way only (a parent does not inherit from its child); it is between classes, not between objects. A child inherits only from its parent and ancestors, not from siblings.
- Every class has Object as its ultimate ancestor; a class that does not extend anything automatically extends Object, and inheritance loops (A extends B, B extends A) are not allowed.
- A subclass constructor always starts by invoking a parent constructor; super(args) calls the parent constructor whose parameter list matches and must be the first statement.
- If super(...) is not written, the compiler inserts a call to super() (no arguments); this is a syntax error if the parent has no no-argument constructor.
- A default no-argument constructor is supplied only if the programmer writes no constructors; writing even one removes it.
- Constructing an object invokes a chain of constructors starting with Object's and ending with the requested class.
- Fixing or extending the parent class affects all children; the parent does not need recompiling when a new child is derived.
