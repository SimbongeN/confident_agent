# Constructors and Object Creation
keywords: constructor, object creation, new, default constructor, initialization, this(), overloaded constructor, instantiate
- Objects are created with the new operator, which allocates memory in the heap, initializes the instance variables, runs the constructor, and returns a reference to the object.
- A constructor has no return type (not even void) and has the same name as its class; the only modifiers allowed are the access modifiers public, private and protected (it cannot be static).
- A constructor can only be called using new; the book says constructors are technically not members of the class and are not referred to as methods.
- Steps in a constructor call: get unused heap memory; initialize instance variables (declared initial value, otherwise the default); evaluate actual parameters and assign to formal parameters; execute the body; return a reference to the object.
- Default initial values: numeric types are zero, boolean is false, char is the Unicode character with code zero, and object types (including String) are null.
- If a class has no constructor, the system supplies a default (no-argument) constructor; if the programmer writes even one constructor, no default constructor is supplied.
- A class can have several constructors if their signatures differ (different numbers or types of parameters); constructors can be overloaded but not overridden.
- A subclass constructor always begins by invoking a parent constructor; super(...) must be the first statement, and if it is omitted the compiler inserts super() with no arguments.
- If the parent has no no-argument constructor, an implicit super() causes a syntax error.
- Constructors let you guarantee that an object is properly initialized, for example forcing a Student name to be set at creation.
