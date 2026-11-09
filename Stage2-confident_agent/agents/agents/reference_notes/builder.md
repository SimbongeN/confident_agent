# Builder
keywords: builder, builder pattern, director, construct complex object, step-by-step construction
- Intent: separate the construction of a complex object from its representation so the same construction process can create different representations. Object creational.
- Use when the algorithm for creating a complex object should be independent of the parts that make it up and how they are assembled.
- Use when the construction process must allow different representations of the constructed object.
- Participants: Builder (abstract interface for creating parts of a Product), ConcreteBuilder (assembles parts, keeps track of the representation, provides a way to retrieve the product), Director (constructs an object using the Builder interface), Product (the complex object under construction).
- Collaboration: the client creates a Director and configures it with a Builder; the Director notifies the builder when to build each part; the builder adds parts; the client retrieves the product from the builder.
- Benefits: lets you vary a product's internal representation (define a new builder); isolates construction code from representation so different Directors can reuse the same builders; gives finer, step-by-step control over construction (unlike patterns that construct in one shot).
- Known uses: ET++ RTF converter (RTFReader as Director, TextConverter as Builder, with ASCIIConverter, TeXConverter, TextWidgetConverter as ConcreteBuilders); Smalltalk-80 Parser with ProgramNodeBuilder; ACE Service Configurator.
- Related: Abstract Factory also may build complex objects, but Builder focuses on step-by-step construction and returns the product at the end, while Abstract Factory emphasizes families of products and returns them immediately. A Composite is what the builder often builds.
