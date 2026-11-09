# Design patterns overview
keywords: design patterns, GoF, Gang of Four, creational, structural, behavioral, Christopher Alexander, anti-pattern, pattern criticism
- A design pattern is a reusable solution to a commonly needed behavior in software; a template, not code to copy.
- Object-oriented patterns usually describe relationships and interactions between classes or objects without naming the final application classes.
- Christopher Alexander introduced patterns in architecture in A Pattern Language (1977).
- Kent Beck and Ward Cunningham began applying patterns to programming in 1987.
- Patterns became widely popular after the 1994 book Design Patterns: Elements of Reusable Object-Oriented Software by the Gang of Four (Gamma, Helm, Johnson, Vlissides).
- Creational patterns create objects (e.g. Abstract Factory, Builder, Factory Method, Singleton).
- Structural patterns organize classes and objects into larger structures (e.g. Adapter, Composite, Decorator, Facade, Proxy).
- Behavioral patterns describe collaboration between objects (e.g. Observer, Strategy, State, Command, Iterator).
- Benefits: proven solutions speed development, help prevent subtle issues, and improve readability for developers who know the patterns.
- Criticism: inappropriate use may unnecessarily increase complexity, and flexibility often adds indirection that complicates design and reduces runtime performance.
- Criticism: a pattern must be reimplemented in each application; some argue needing a pattern signals a missing language feature (Norvig: 16 of 23 GoF patterns are simplified or eliminated in Lisp or Dylan).
- Some patterns can be anti-patterns in certain contexts, e.g. double-checked locking can be unsafe in some language and hardware combinations.
