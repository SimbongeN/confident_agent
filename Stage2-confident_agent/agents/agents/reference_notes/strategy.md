# Strategy
keywords: strategy, strategy pattern, interchangeable algorithms, context, policy, algorithm family
- Intent: define a family of algorithms, encapsulate each one, and make them interchangeable, letting the algorithm vary independently of the clients that use it. Also known as Policy.
- Use when many related classes differ only in behavior; when you need variants of an algorithm (e.g. different space/time trade-offs); when an algorithm uses data clients should not know about; or when a class has many behaviors expressed as multiple conditional statements.
- Participants: Strategy (common interface for all algorithms), ConcreteStrategy (implements the algorithm), Context (configured with a ConcreteStrategy, holds a reference to a Strategy, may expose an interface for the strategy to access its data).
- Collaboration: the context either passes all required data to the strategy or passes itself as an argument so the strategy can call back. Clients usually create the ConcreteStrategy, pass it to the context, and thereafter deal only with the context.
- Consequence: an alternative to subclassing the Context. Subclassing hard-wires the behavior, mixes algorithm with Context, and prevents varying the algorithm dynamically; Strategy lets it vary independently and be switched.
- Consequence: eliminates conditional (switch-style) statements for selecting behavior; many conditionals often signal a need for Strategy.
- Liabilities: clients must understand how strategies differ before choosing; communication overhead because all strategies share one interface (some get unused parameters); more objects in the application.
- The object count can be reduced by making strategies stateless objects shared by contexts (Flyweight); residual state stays in the context.
- Known uses: line-breaking algorithms in ET++ and Interviews (Composition and Compositor classes, the motivating example); RTL compiler register allocation; Borland ObjectWindows Validators for dialog entry fields.
- Related: Flyweight (Strategy objects often make good flyweights).
- Distinguishing from State (Ch. 1, Delegation): both change behavior by changing the object delegated to; an object will have only one state but can have many strategies for different requests. Strategy vs Template Method: strategies use delegation to vary the entire algorithm, template methods use inheritance to vary part of it.
