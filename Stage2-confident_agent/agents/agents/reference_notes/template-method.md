# Template Method
keywords: template method, template method pattern, skeleton of algorithm, hook, primitive operations, invariant steps
- Intent: define the skeleton of an algorithm in an operation, deferring some steps to subclasses, so subclasses can redefine certain steps without changing the algorithm's structure. Class behavioral pattern.
- Use to implement the invariant parts of an algorithm once and leave the varying behavior to subclasses.
- Use when common behavior among subclasses should be factored into a common class to avoid duplication ("refactoring to generalize": identify differences, separate them into new operations, replace with a template method calling them).
- Use to control subclass extensions: the template method calls "hook" operations at specific points, permitting extension only there.
- Participants: AbstractClass (defines abstract primitive operations and the template method that calls them), ConcreteClass (implements the primitive operations for subclass-specific steps). ConcreteClass relies on AbstractClass for the invariant steps.
- Consequence: a fundamental technique for code reuse, especially in class libraries; leads to an inverted control structure, the "Hollywood principle" ("Don't call us, we'll call you"): the parent calls the subclass's operations.
- A template method may call concrete operations, concrete AbstractClass operations, primitive (abstract) operations, factory methods, and hook operations (default behavior, often empty, that subclasses may extend).
- Template methods should distinguish hooks (may be overridden) from abstract operations (must be overridden). Wrapping a parent operation in a hook avoids relying on subclasses remembering to call the inherited operation.
- Known use: the motivating example is an application framework's Application::OpenDocument, with steps like CanOpenDocument and DoCreateDocument supplied by subclasses; the book says template methods appear in almost every abstract class.
- Related: Factory Methods are often called by template methods. Strategy: template methods use inheritance to vary part of an algorithm; strategies use delegation to vary the entire algorithm.
