# Package Design Principles Overview and High-Level Abstraction
keywords: package, package principles, package cohesion, package coupling, granularity, stability, REP CRP CCP ADP SDP SAP, package UML
- Classes are too fine-grained for big projects; packages (groups of classes) give a higher level of abstraction.
- A package is a unit for testing and can be a releasable component; classes in a package are often compiled together into a library, though the unit of compilation is mostly the individual class.
- In UML a package is drawn as a package symbol; a dependency between packages is a dashed arrow; a package can show its classes inside.
- Granularity (principles of package cohesion): Reuse-Release Equivalence (REP), Common-Reuse (CRP), Common-Closure (CCP).
- Stability (principles of package coupling): Acyclic-Dependencies (ADP), Stable-Dependencies (SDP), Stable-Abstractions (SAP).
- Class design principles: Single Responsibility, Open-Closed, Liskov Substitution, Dependency Inversion, Interface Segregation.
- Applying the class principles well helps in package design and in designing large software systems.
