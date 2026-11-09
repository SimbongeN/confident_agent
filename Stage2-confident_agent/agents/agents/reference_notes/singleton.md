# Singleton
keywords: singleton, singleton pattern, single instance, global access point, one instance
- Intent: ensure a class has only one instance, and provide a global point of access to it. Object creational.
- Use when there must be exactly one instance of a class accessible to clients from a well-known access point.
- Use also when the sole instance should be extensible by subclassing and clients should use an extended instance without modifying their code.
- Motivation: a global variable makes an object accessible but does not prevent multiple instances; a better solution makes the class itself responsible for tracking its sole instance and intercepting requests to create new ones. Examples named: one printer spooler, one file system, one window manager.
- Participants: only Singleton, which defines an Instance class operation (static in C++, class method in Smalltalk) giving access to its unique instance and may be responsible for creating it. Clients access the instance solely through Instance.
- Benefits: controlled access to the sole instance; reduced name space (improvement over global variables); permits refinement by subclassing; permits a variable number of instances (only the access operation changes); more flexible than class (static) operations, which are hard to change to multiple instances and are not virtual in C++.
- Known uses: Smalltalk-80 ChangeSet current and class/metaclass relationship; Interviews Session and WidgetKit.
- Related: many patterns can be implemented using Singleton (Abstract Factory, Builder, Prototype); a concrete factory is often a singleton; State objects are often Singletons. The text does not discuss thread safety in the portions read.
