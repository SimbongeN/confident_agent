# Composition Over Inheritance
keywords: composition over inheritance, inheritance, composition, delegation, has-a relationship, reuse, flexibility

- Composition builds an object by giving it references to other objects that provide parts of its behaviour.
- Inheritance creates an “is-a” relationship in which a subclass inherits members and behaviour from a superclass.
- Composition is often preferred when a class needs to use a capability without being a specialised kind of the class providing it.
- A composed object can delegate work to a field, such as a `Car` delegating engine operations to an `Engine` object.
- Composition can allow behaviour to be changed by replacing a component, rather than creating a new subclass.
- Inheritance can create tight coupling because subclasses depend on the superclass implementation and its assumptions.
- Inheritance remains suitable when the subtype relationship is genuine and the subclass can honour the superclass contract.
- Composition and inheritance are complementary techniques; “composition over inheritance” is a design preference, not an absolute prohibition on inheritance.
