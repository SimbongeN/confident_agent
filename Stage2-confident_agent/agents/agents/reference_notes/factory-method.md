# Factory Method
keywords: factory method, factory method pattern, virtual constructor, creator, product, defer instantiation
- Intent: define an interface for creating an object, but let subclasses decide which class to instantiate; defers instantiation to subclasses. Also known as Virtual Constructor. Class creational.
- Use when a class cannot anticipate the class of objects it must create, or wants its subclasses to specify the objects it creates.
- Use when classes delegate responsibility to one of several helper subclasses and you want to localize knowledge of which helper is the delegate.
- Participants: Product (interface of objects the factory method creates), ConcreteProduct, Creator (declares the factory method, may give a default implementation, may call it), ConcreteCreator (overrides it to return a ConcreteProduct). The Creator relies on its subclasses to define the factory method.
- Benefit: removes the need to bind application-specific classes into framework code; the code deals only with the Product interface.
- Liability: clients may have to subclass the Creator just to create a particular ConcreteProduct, adding another point of evolution.
- Consequences: gives subclasses a hook for an extended version of an object (e.g. a default file dialog creator); connects parallel class hierarchies (e.g. Figure and Manipulator via CreateManipulator).
- Known uses: factory methods pervade toolkits and frameworks (MacApp and ET++ Application/Document example; Unidraw Manipulator); Smalltalk MVC View defaultControllerClass; Orbix ORB generates proxies.
- Related: Abstract Factory is often implemented with factory methods; factory methods are usually called within Template Methods; Prototype does not require subclassing the Creator but often needs an Initialize operation on Product. Book advises Factory Method is easiest to start with, and designs often evolve toward Abstract Factory, Prototype or Builder where more flexibility is needed.
