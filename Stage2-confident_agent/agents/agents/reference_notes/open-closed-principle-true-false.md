# Open-Closed Principle: True or False
keywords: OCP, open-closed principle, extension, modification, abstraction, polymorphism, design principle

- The Open-Closed Principle says that software entities should be open for extension and closed for modification.
- The principle is a design guideline, not a syntax rule enforced directly by the Java compiler.
- Adding a new implementation behind an existing interface can extend behaviour without changing the code that uses the interface.
- OCP does not claim that source code can never be modified; bug fixes and changed requirements can still require edits.
- A design that uses a large chain of conditionals for every new type may be harder to extend without modification.
- Polymorphism can move type-specific behaviour into separate implementations and reduce repeated edits to central logic.
- The principle does not require an interface for every class; abstractions are most useful around likely variation points.
- A statement that OCP forbids all code changes is therefore an inaccurate interpretation of the principle.
