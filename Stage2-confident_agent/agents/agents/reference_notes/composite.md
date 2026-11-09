# Composite
keywords: composite, composite pattern, tree structure, part-whole hierarchy, leaf, treat uniformly
- Intent: compose objects into tree structures to represent part-whole hierarchies; lets clients treat individual objects and compositions of objects uniformly. Object structural.
- Use when you want to represent part-whole hierarchies of objects, and want clients to ignore the difference between compositions and individual objects.
- Key idea: an abstract class represents both primitives and their containers, so clients do not need to distinguish them (e.g. Graphic with Line, Rectangle, Text leaves and Picture composite).
- Participants: Component (interface for all objects, default behavior, interface for managing children, optional parent access), Leaf (no children; defines primitive behavior), Composite (stores children; implements child-related operations), Client (uses the Component interface).
- Collaboration: if the recipient is a Leaf the request is handled directly; if a Composite it usually forwards to its children, possibly doing extra work before/after.
- Benefits: builds recursive hierarchies of primitive and composite objects; simplifies clients (no tag-and-case-statement code); new Leaf or Composite classes work with existing code.
- Liability: can make the design overly general; it is harder to restrict which components a composite may hold, so the type system cannot enforce it and run-time checks are needed.
- Known uses: original Smalltalk MVC View; ET++ VObjects; Interviews Glyphs; RTL compiler RTLExpression; portfolio of assets.
- Related: Component-parent link is often used for Chain of Responsibility; Decorator is often used with Composite (and structure diagrams are similar, Ch. 1); Flyweight lets you share components but they cannot refer to parents; Iterator traverses composites; Visitor localizes operations otherwise spread across Composite and Leaf; Command uses a MacroCommand Composite; a Composite is what Builder often builds.
- Structural discussion: Composite and Decorator have similar diagrams, but Composite focuses on representation (treating many objects as one), not embellishment; the intents are complementary and they are often used together.
