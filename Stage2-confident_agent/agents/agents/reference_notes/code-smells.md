# Code smells
keywords: code smell, bad smell, long method, large class, god object, duplicated code, feature envy, shotgun surgery, divergent change, data clumps, refused bequest, refactoring, bloaters, couplers
- A code smell is a characteristic of source code hinting at a deeper design problem; usually not a bug, but can slow development or raise risk of bugs.
- Long Method: a method contains too many lines of code; sourcemaking suggests longer than ten lines should prompt questions.
- Large Class: a class contains many fields, methods or lines of code (Wikipedia: a "god object" with many unrelated methods).
- Duplicate Code: two code fragments look almost identical; it often arises from several programmers working in parallel or copying to meet a deadline.
- Feature Envy: a method accesses the data of another object more than its own data.
- Shotgun Surgery: a single change must be made to multiple classes simultaneously.
- Divergent Change is the opposite of Shotgun Surgery: many different kinds of changes land in one class.
- Data Clumps: a group of variables repeatedly passed around together, which likely should be one object.
- Long Parameter List (too many parameters): hard to read and test, may indicate poorly assigned responsibilities.
- Refused Bequest: a subclass overrides a base-class method in a way that breaks its contract (violating Liskov substitution).
- Magic numbers: raw literals that should be named constants.
- Sourcemaking groups smells as Bloaters (Long Method, Large Class, Primitive Obsession, Long Parameter List, Data Clumps), Object-Orientation Abusers, Change Preventers, Dispensables and Couplers (Feature Envy, Inappropriate Intimacy, Message Chains, Middle Man).
