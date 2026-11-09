# Decorator Pattern
keywords: Decorator, structural design pattern, wrapper, component interface, concrete decorator, composition, dynamic behaviour

- The Decorator pattern adds responsibilities to an individual object by wrapping it in another object.
- A decorator and the objects it wraps share a common component interface or superclass.
- A decorator stores a reference to a component and delegates the core operation to that component.
- The decorator can add behaviour before or after delegating to the wrapped component.
- Multiple decorators can be stacked to combine optional behaviours at runtime.
- Decorators can provide an alternative to creating many subclasses for every combination of optional features.
- The wrapper must preserve the component's expected interface so that clients can use decorated and undecorated objects similarly.
- A trade-off is that debugging can be harder when behaviour is spread across several nested wrappers.
