# Objects and Classes
keywords: object, class, instance, object-oriented programming, OOP, state and behavior, instance variable, method, paradigm
- An object is a software bundle of variables (its state) and related methods (its behavior); an object is also called an instance.
- A class is a blueprint that defines the variables and methods common to all objects of a certain kind; many objects can be created from one class.
- Each object has its own copy of the instance variables, so different objects of the same class can hold different values; the class determines the variable types, but the data lives in the individual objects.
- Encapsulation means packaging an object's variables inside the protection of its methods; the book lists two benefits: modularity and information hiding.
- Objects communicate by messages; a message has three parts: the receiving object, the method name, and any parameters.
- Every class defines a new type; a type is a set of values plus the operations applicable to them. Java has two kinds of types: primitive types and reference (class) types.
- A variable never holds an object, only a reference to it; objects live in the heap, and declaring a variable does not create an object.
- Assigning one object variable to another copies only the reference, not the object; == on object variables tests whether they refer to the same object, so use equals (not ==) to compare String contents.
- A final object variable keeps referring to the same object, but the object's data can still change. A method receiving an object gets a copy of the reference, so it can change the object's data but not the caller's variable.
- A variable that refers to no object holds null; using an instance variable or method through null causes a null pointer exception.
