# Abstract Factory
keywords: abstract factory, abstract factory pattern, kit, families of related objects, product family
- Intent: provide an interface for creating families of related or dependent objects without specifying their concrete classes. Also known as Kit. Object creational.
- Use when a system should be independent of how its products are created, composed and represented; or should be configured with one of multiple product families.
- Use when a family of related products is designed to be used together and that constraint must be enforced; or when a class library should reveal only product interfaces, not implementations.
- Participants: AbstractFactory (interface for creating abstract products), ConcreteFactory (creates concrete products), AbstractProduct (interface for a product type), ConcreteProduct (created by the matching factory, implements AbstractProduct), Client (uses only the abstract interfaces).
- Collaboration: normally a single ConcreteFactory instance exists at run-time; to get different products, clients use a different concrete factory. AbstractFactory defers creation to its ConcreteFactory subclass.
- Benefits: isolates concrete classes from clients; makes exchanging whole product families easy (the concrete factory class appears once, where instantiated); promotes consistency among products of one family.
- Liability: supporting new kinds of products is difficult, since the AbstractFactory interface fixes the set of products; adding one means changing the factory class and all its subclasses.
- Known uses: Interviews' "Kit" classes (WidgetKit, DialogKit, LayoutKit); ET++ WindowSystem class for portability across window systems; motivating example is WidgetFactory with Motif and Presentation Manager look-and-feels.
- Related: factories are often implemented with Factory Methods but can use Prototype; a concrete factory is often a Singleton. Builder differs: Builder constructs a complex object step by step and returns it as a final step, while Abstract Factory emphasizes families of products and returns them immediately.
