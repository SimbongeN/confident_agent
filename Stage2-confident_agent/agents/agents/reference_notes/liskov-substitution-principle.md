# Liskov Substitution Principle (LSP)
keywords: LSP, Liskov, Liskov substitution, substitutability, subclass substitutable for base class, Rectangle Square, behavioural subtyping, SOLID
- Subclasses (derived classes) should be substitutable for their base class.
- Objects of a derived class must behave consistently with objects of the base class.
- Objects should be replaceable with instances of their subtypes without altering the correctness of the program.
- The slides' example is Rectangle and Square: both have width and height attributes, but their width behaves differently, so Square as a subclass of Rectangle is problematic.
- It is one of the five SOLID principles.
