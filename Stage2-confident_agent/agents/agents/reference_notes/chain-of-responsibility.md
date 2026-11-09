# Chain of Responsibility
keywords: chain of responsibility, handler, request chain, successor, pass request along
- Intent: avoid coupling the sender of a request to its receiver by giving more than one object a chance to handle it; chain the receivers and pass the request along until an object handles it. Object behavioral.
- Use when more than one object may handle a request and the handler is not known a priori (it should be ascertained automatically).
- Use when you want to issue a request to one of several objects without specifying the receiver explicitly, or when the set of handlers should be specified dynamically.
- Participants: Handler (interface for handling requests; optionally implements the successor link), ConcreteHandler (handles requests it is responsible for, can access its successor, otherwise forwards), Client (initiates the request to a ConcreteHandler on the chain).
- The request has an implicit receiver; each object on the chain shares a common interface for handling requests and accessing its successor (the book's example is HelpHandler/HandleHelp for context-sensitive help).
- Benefits: reduced coupling (sender and receiver have no explicit knowledge of each other; each object keeps one reference to its successor); added flexibility in assigning responsibilities (change the chain at run-time).
- Liability: receipt is not guaranteed; a request can fall off the end of the chain unhandled, or go unhandled if the chain is misconfigured.
- Known uses: event handling in class libraries (MacApp/ET++ EventHandler, Symantec TCL Bureaucrat, NeXT AppKit Responder); Unidraw Command forwarding; ET++ InvalidateRect forwarded to enclosing containers up to the Window.
- Related: often used with Composite, where a component's parent can act as its successor. The Ch. 5 intro says Chain of Responsibility provides even looser coupling than Mediator.
- Decoupling (Ch. 5 discussion): good when the chain is already part of the system's structure and one of several objects may handle the request; the fixed interface may need a custom dispatching scheme, with the same type-safety drawbacks as Mediator.
