# State
keywords: state, state pattern, state machine, behavior changes with state, context, finite state
- Intent: allow an object to alter its behavior when its internal state changes, so that the object appears to change its class. Also known as Objects for States.
- Use when an object's behavior depends on its state and must change at run-time accordingly.
- Use when operations contain large, multipart conditionals (often on enumerated constants, often repeated across operations); State puts each branch in a separate class so the state becomes an object in its own right.
- Participants: Context (interface for clients; keeps an instance of a ConcreteState subclass defining the current state), State (interface encapsulating behavior for a particular state), ConcreteState subclasses (each implements the behavior of one state).
- Collaborations: Context delegates state-specific requests to the current ConcreteState and may pass itself to it; either the Context or the ConcreteState subclasses can decide which state succeeds another.
- Consequence: localizes state-specific behavior and partitions it per state; new states and transitions are added by adding subclasses. Cost: more classes and less compactness than one class, but better than large conditionals when there are many states.
- Consequence: makes state transitions explicit and atomic (rebinding one variable, the Context's state object), protecting the Context from inconsistent internal states.
- State objects can be shared if they have no instance variables (state encoded in their type); they are then essentially flyweights with no intrinsic state.
- Known uses: TCPConnection with TCPState subclasses (TCPEstablished, TCPListen, TCPClosed), the motivating example; drawing-editor Tool objects in HotDraw and Unidraw.
- Related: Flyweight explains when State objects can be shared; State objects are often Singletons. Coplien's Envelope-Letter idiom also changes an object's class at run-time; State is more specific.
- Distinguishing from Strategy (Ch. 1, Delegation): both change an object's behavior by changing the object it delegates to; an object has only one state at a time, but can have many strategies for different requests.
