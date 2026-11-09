# Command
keywords: command, command pattern, encapsulate request, undo, invoker, receiver, queue requests, macro command
- Intent: encapsulate a request as an object, letting you parameterize clients with different requests, queue or log requests, and support undoable operations. Also known as Action, Transaction. Object behavioral.
- Use to parameterize objects by an action to perform; the book calls Commands an object-oriented replacement for callbacks.
- Use to specify, queue and execute requests at different times (a command can outlive the original request and be sent to another process).
- Use to support undo (store reversing state in the command; add an Unexecute operation; keep a history list to traverse backwards/forwards for undo/redo).
- Use to log changes for re-application after a crash, and to structure a system around high-level operations built on primitives (e.g. transactions).
- Participants: Command (interface for executing), ConcreteCommand (binds a Receiver to an action; implements Execute by invoking the receiver), Client (creates a ConcreteCommand and sets its receiver), Invoker (asks the command to carry out the request, e.g. MenuItem), Receiver (knows how to perform the operations).
- Consequences: decouples the invoker from the object that knows how to perform the operation; commands are first-class objects; commands can be assembled into composite commands (MacroCommand); new Commands are easy to add without changing existing classes.
- Known uses: MacApp (undoable commands), ET++, Interviews Action, Unidraw, THINK "Tasks"; menu items configured with commands such as PasteCommand and OpenCommand (motivating example).
- Related: Composite can implement MacroCommands; Memento can keep state needed to undo; a command copied onto the history list acts as a Prototype.
- Decoupling (Ch. 5 discussion): Command decouples sender from receiver via an object defining the binding, so senders and commands are reusable; it nominally needs a subclass per sender-receiver connection.
