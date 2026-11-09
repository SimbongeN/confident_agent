# Access Control
keywords: access control, private, public, protected, package-private, default access, access modifier, visibility, getter, setter, encapsulation
- A class can be public (visible to all classes everywhere) or have no modifier (package-private: visible only within its own package).
- A member can be public, private, protected, or have no modifier (package-private).
- private: the member can only be accessed within its own class.
- No modifier (package-private): accessible from the class and other classes in the same package, but not from subclasses in other packages or the world.
- protected: accessible within its own package (as with package-private) and, in addition, by subclasses of its class even if the subclass is in another package; not accessible to the rest of the world.
- public: accessible from everywhere.
- Access is decided per class, not per instance: instances of the same class can access one another's private members.
- A subclass in a different package can use public and protected inherited members but not private or package-private ones.
- The book recommends making almost all member variables private and offering public getter (accessor) and setter (mutator) methods; these can do extra work such as validation and let the internal representation change without breaking other classes.
- A private member variable is not part of the class's public interface; only the public getters and setters are.
