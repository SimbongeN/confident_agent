# Refactoring: Dealing with Generalisation
keywords: pull up field, pull up method, pull up constructor body, push down method, push down field, extract subclass, extract superclass, extract interface, collapse hierarchy, form template method, replace inheritance with delegation
- Pull Up Field / Pull Up Method / Pull Up Constructor Body: move identical or similar members from subclasses to the superclass.
- Push Down Method / Push Down Field: move members used by only one or few subclasses into those subclasses.
- Extract Subclass: create a subclass for features used only in certain cases.
- Extract Superclass: create a shared superclass for two classes with common fields and methods.
- Extract Interface: move the shared part of an interface used by multiple clients (or common to two classes) into its own interface.
- Collapse Hierarchy: merge a subclass that is practically the same as its superclass.
- Form Template Method: move the common algorithm structure and identical steps to a superclass, leaving differing steps in subclasses.
- Replace Inheritance with Delegation: when a subclass uses only part of its superclass, hold a superclass object in a field and delegate.
- Replace Delegation with Inheritance: when a class delegates all methods of another, make it inherit instead.
