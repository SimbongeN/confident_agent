# Dependency Inversion Principle (DIP)
keywords: DIP, dependency inversion, depend on abstractions, abstraction layer, high-level low-level classes, depend on interfaces, SOLID
- Depend upon abstractions and not upon concretions.
- Put an abstraction layer between high-level and low-level classes: high-level classes depend on the abstraction layer, which low-level classes implement.
- Depend on interfaces or abstract classes and functions rather than on concrete ones.
- Every dependency should target an interface; no dependency should target a concrete class.
- It is one of the five SOLID principles.
- Abstract interfaces (DIP) can be used to break cycles in package dependency graphs (Acyclic-Dependencies Principle).
