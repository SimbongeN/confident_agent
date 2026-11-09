# Singleton as an anti-pattern
keywords: singleton, anti-pattern, global state, testability, hidden dependencies, unit testing, single responsibility, dependency injection alternative
- The Singleton is a Gang of Four pattern that restricts instantiation of a class to a single instance.
- It is useful when exactly one object is needed to coordinate actions across a system.
- Implementations typically hide constructors and expose a static method returning the single instance.
- Criticism: some consider it an anti-pattern because it introduces global state into an application, often unnecessarily.
- Criticism: it creates hidden dependencies; other objects may rely on it, so you may need to inspect implementation details to see the dependency.
- Criticism: the added coupling makes unit testing harder and can prevent concurrent use of multiple instances.
- Criticism: it violates the single-responsibility principle since the class enforces its own uniqueness as well as doing its normal job.
- Alternative: dependency injection passes dependencies in from outside so objects need not look up global state.
