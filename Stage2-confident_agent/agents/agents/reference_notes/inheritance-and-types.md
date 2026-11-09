# Inheritance and Types
keywords: polymorphism, type checking, typecasting, upcast, downcast, instanceof, dynamic binding, static type, runtime type, substitutability
- Inheritance gives is-a relationships: a MusicVideo is-a Video, so a subclass object is automatically an object of the superclass type.
- Substitution principle: a variable that can hold a reference to class A can also hold a reference to an object of any subclass of A; this also applies to method parameters and arrays (a Video array can hold Movie and MusicVideo objects).
- A subclass reference can be assigned to a superclass variable, but not the reverse; the book says this is illegal even if the superclass variable currently refers to a subclass object, because not every Video is a Movie.
- Java is strongly typed: the compiler checks assignments and method calls against the declared type of the variable, not the type of the object it refers to; calling a subclass-only method through a superclass variable is a compile error.
- Typecasting converts one type to another; widening conversions (int to double) are implicit; narrowing (double to int) needs an explicit cast.
- For objects, an explicit cast such as (Movie)myVideo tells the compiler to treat the object as that type; casts of object types are checked, so casting a MusicVideo reference to Movie produces an error. Parentheses are needed to cast before accessing a member, e.g. ((Movie)v).director.
- instanceof tests whether the object actually referenced is an instance of a class (it checks the object's class, not the variable's declared type), and can guard a cast.
- Polymorphism: calling an overridden method through a superclass variable runs the version in the actual object's class (e.g. s.redraw() runs the Rectangle version); the book also describes the reference to the abstract readChar() in an interface default method as polymorphic.
- OO concepts the book lists: objects and classes, inheritance, polymorphism and dynamic binding.
