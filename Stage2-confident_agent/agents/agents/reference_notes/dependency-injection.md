# Dependency injection, inversion of control and dependency inversion
keywords: dependency injection, DI, inversion of control, IoC, dependency inversion principle, DIP, constructor injection, setter injection, interface injection, service locator, Hollywood principle
- Dependency injection (DI) is a technique where an object is handed the objects it needs instead of constructing them itself.
- DI separates building objects from using them, which leads to loosely coupled programs.
- Constructor injection passes dependencies through the class constructor; it is the most common form and Fowler's default preference.
- Setter injection exposes a setter method that accepts the dependency, so it can be changed at any time.
- Interface injection has the dependency's interface provide an injector method; Fowler finds it more invasive.
- Method injection passes a dependency to a single method only for that call.
- Inversion of control (IoC) is a design principle in which custom code receives its flow of control from an external source such as a framework: "Don't call us, we'll call you" (Hollywood Principle).
- Especially in Java communities, "inversion of control" is also used to mean DI; Fowler proposed "Dependency Injection" as a more specific name than IoC for what lightweight containers do.
- The Dependency Inversion Principle says high-level modules should not import from low-level modules, and both should depend on abstractions; abstractions should not depend on details.
- DI is often used to keep code in line with the Dependency Inversion Principle, so DIP is the principle, DI is a technique, and IoC is the broader idea of control being inverted.
- Service Locator is the alternative to DI: the class asks a registry for the services it needs. Injection makes dependencies visible in constructors and setters.
