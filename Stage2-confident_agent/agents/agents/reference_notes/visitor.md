# Visitor
keywords: visitor, visitor pattern, double dispatch, accept, visit, operations on object structure
- Intent: represent an operation to be performed on the elements of an object structure; lets you define a new operation without changing the classes of the elements it operates on.
- Use when an object structure has many classes with differing interfaces and operations depend on the concrete class.
- Use when many distinct, unrelated operations must be performed on the structure and you want to avoid polluting the element classes; related operations are kept together in one visitor class.
- Use when the structure's classes rarely change but you often add operations. If element classes change often, define the operations in those classes instead.
- Participants: Visitor (a Visit operation per ConcreteElement class), ConcreteVisitor (implements each Visit; stores local state, often accumulating results), Element (defines Accept taking a visitor), ConcreteElement (implements Accept), ObjectStructure (can enumerate its elements; may be a Composite or a collection such as a list or set).
- Collaboration: the client creates a ConcreteVisitor and traverses the structure; each element calls the Visit operation matching its class, passing itself as the argument.
- Benefit: adding a new operation is easy (add a new visitor); related behavior is localized and unrelated behavior separated. Visitors can accumulate state during traversal, and can visit objects with no common parent class (unlike an Iterator, which needs a common Item type).
- Liabilities: adding new ConcreteElement classes is hard (each requires a new Visit operation in every ConcreteVisitor); may break encapsulation by forcing public operations that expose element state.
- Known uses: Smalltalk-80 compiler's ProgramNodeEnumerator; IRIS Inventor "actions" (rendering, event handling, searching, etc.); the motivating example is operations over compiler abstract syntax trees.
- Related: Composite (visitors can apply an operation over a Composite structure); Interpreter (Visitor may be applied to do the interpretation). The book notes the Visitor object is always passed as an argument to Accept and is not considered part of the elements.
