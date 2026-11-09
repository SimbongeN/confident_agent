# Code Refactoring Overview
keywords: refactoring, code refactoring, restructuring code, change factoring without changing semantics, refactoring techniques, code smells, sourcemaking
- Refactoring is restructuring existing program code (changing the factoring) without changing its semantics.
- We refactor to adapt to design changes (e.g. as a result of pattern refactoring), to improve non-functional aspects of the system, or to obfuscate source code.
- The lecture groups techniques into: composing methods; moving features between objects; organising data; simplifying conditional expressions; simplifying method calls; and dealing with generalisation.
- Composing methods streamlines methods, removes duplication and paves the way for future improvements.
- Moving features between objects safely moves functionality between classes, creates new classes and hides implementation details.
- Organising data improves data handling, replaces primitives with rich class functionality and untangles class associations (decoupling).
- Simplifying method calls simplifies the interfaces for interaction between classes.
- Dealing with generalisation moves functionality along the inheritance hierarchy and can replace inheritance with delegation and vice versa.
