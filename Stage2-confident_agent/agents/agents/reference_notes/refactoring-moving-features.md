# Refactoring: Moving Features Between Objects
keywords: move method, move field, extract class, inline class, hide delegate, remove middle man, introduce foreign method, introduce local extension
- Move Method: move a method used more in another class into that class and make the original delegate or remove it.
- Move Field: move a field used more in another class and redirect users.
- Extract Class: when one class does the work of two, create a new class for the extra fields and methods.
- Inline Class: when a class does almost nothing and no more responsibility is planned, move its features to another class.
- Hide Delegate: when a client gets object B via object A and calls B, add a method in A that delegates to B so the client does not depend on B.
- Remove Middle Man: when a class has too many methods that simply delegate, remove the delegation.
- Introduce Foreign Method: when a utility class lacks a method and cannot be changed, add the method to a client class and pass the utility object as an argument.
- Introduce Local Extension: create a new class with the missing methods as a child or wrapper of the utility class.
