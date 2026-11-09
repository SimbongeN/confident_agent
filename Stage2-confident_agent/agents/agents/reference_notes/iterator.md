# Iterator
keywords: iterator, iterator pattern, aggregate, traversal, cursor, sequential access, internal iterator, external iterator
- Intent: provide a way to access the elements of an aggregate object sequentially without exposing its underlying representation. Also known as Cursor. Object behavioral.
- Key idea: take responsibility for access and traversal out of the aggregate and put it into an iterator object, which tracks the current element (First, Next, IsDone, CurrentItem in the book's List example).
- Use to access an aggregate's contents without exposing its internal representation; to support multiple traversals of aggregates; to provide a uniform interface for traversing different aggregate structures (polymorphic iteration).
- Participants: Iterator (interface for access and traversal), ConcreteIterator (implements it; tracks current position), Aggregate (interface for creating an Iterator), ConcreteAggregate (returns the proper ConcreteIterator).
- Polymorphic iteration: an abstract list and abstract iterator make traversal independent of the concrete aggregate; lists create their iterators through a CreateIterator factory method, which connects the two hierarchies.
- Consequences: supports variations in traversal (swap the iterator, or subclass for new traversals); simplifies the Aggregate interface; more than one traversal can be pending since each iterator keeps its own state.
- Known uses: most collection class libraries (Booch components, ET++ containers, ObjectWindows); Smalltalk collections use an internal iterator (do:) and ReadStream acts as an external iterator.
- Related: Iterators are often applied to Composite structures; polymorphic iterators rely on Factory Method; Memento is often used with Iterator to capture iteration state. Visitor (per the book) can traverse across structures with no common element parent, which an iterator cannot.
