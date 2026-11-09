# Facade
keywords: facade, facade pattern, unified interface, subsystem, simplify interface
- Intent: provide a unified interface to a set of interfaces in a subsystem; defines a higher-level interface that makes the subsystem easier to use. Object structural.
- Use to provide a simple interface to a complex subsystem; a facade gives a simple default view good enough for most clients, while those needing more customizability can look beyond it.
- Use when there are many dependencies between clients and the implementation classes of an abstraction; a facade decouples the subsystem from clients and other subsystems, promoting independence and portability.
- Use to layer subsystems: define an entry point to each level, so dependent subsystems communicate solely through their facades.
- Participants: Facade (knows which subsystem classes handle a request; delegates client requests), subsystem classes (implement the functionality; have no knowledge of the facade and keep no reference to it).
- Benefits: shields clients from subsystem components; promotes weak coupling between subsystem and clients (can remove circular dependencies, reduce compilation dependencies, ease porting); does not prevent clients from using subsystem classes directly if needed.
- Known uses: the compiler example (a Compiler class fronting Scanner, Parser, etc.); ET++ ProgrammingEnvironment; Choices operating system (FileSystemInterface, Domain).
- Distinguishing (book): Mediator is similar in abstracting existing classes, but a mediator abstracts arbitrary communication between colleagues, centralizes functionality, and colleagues know the mediator; a facade only simplifies the interface to subsystem objects, adds no new functionality, and subsystem classes do not know about it.
- Related: Abstract Factory can be used with Facade to create subsystem objects, or as an alternative to Facade to hide platform-specific classes; usually one Facade is needed, so facades are often Singletons.
- Structural discussion: a facade can be thought of as an adapter to a set of objects, but it defines a new interface whereas an adapter reuses an old one.
