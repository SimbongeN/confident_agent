# Abstraction, encapsulation, modularity, information hiding, reuse
keywords: abstraction, encapsulation, modularity, modular programming, information hiding, code reuse, independence, data abstraction, interface, Parnas, OOP
- Abstraction provides access while hiding details that would otherwise make access harder, focusing attention on details of greater importance.
- Data abstraction separates a type's public interface from its private implementation so the implementation can change without affecting client code.
- Encapsulation means bundling data with the methods that operate on it, and may also mean limiting direct access to an object's components.
- Information hiding isolates design decisions most likely to change behind a stable interface so changes do not force changes elsewhere; David Parnas described it in 1972.
- Encapsulation and information hiding are often used interchangeably; one view is that information hiding is the principle and encapsulation is the technique.
- Modular programming organizes a codebase's functions into independent modules, each providing one aspect of the program.
- A module's interface states what it provides and requires; its implementation holds the working code.
- Modularity gives independence: modules perform logically discrete functions and interact only through well-defined interfaces, so team members can work on smaller tasks.
- Modularity gives reuse: correctly built modular systems are far more reusable than a monolithic design.
- Code reuse means building software from existing code; it can reduce effort but creates dependencies that can make maintenance harder.
- Modularity, loose coupling, high cohesion, information hiding and separation of concerns make code easier to reuse.
