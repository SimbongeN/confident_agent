# Refactoring: Organizing Data
keywords: self encapsulate field, encapsulate field, encapsulate collection, replace magic number with symbolic constant, replace type code with class, replace type code with subclasses, replace type code with state strategy, replace data value with object
- Self Encapsulate Field: use getters and setters even inside the class instead of direct access to private fields.
- Encapsulate Field: make a public field private and add access methods.
- Encapsulate Collection: return a read-only view from the getter and provide add/remove methods.
- Replace Data Value with Object: move a field with its own behaviour and data into a new class.
- Change Value to Reference: replace many identical instances with a single object; Change Reference to Value does the reverse for small, rarely changed objects.
- Replace Array with Object: an array of mixed data becomes an object with separate fields.
- Duplicate Observed Data: separate domain data from GUI classes and keep them synchronised.
- Change Unidirectional Association to Bidirectional, and the reverse, add or remove an association as needed.
- Replace Magic Number with Symbolic Constant: use a named constant.
- Replace Type Code with Class (value does not affect behaviour), with Subclasses (it drives conditionals; use polymorphism) or with State/Strategy (when subclasses cannot be used); Replace Subclass with Fields when subclasses differ only in constant-returning methods.
