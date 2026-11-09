# Interface Segregation Principle (ISP)
keywords: ISP, interface segregation, client-specific interfaces, fat interface, general purpose interface, SOLID
- Abstraction is done in an interface.
- Many client-specific interfaces are better than one general-purpose interface.
- For a class with multiple clients, create a specific interface for each client and inherit them all into the class.
- Clients should not be forced to implement or depend on interfaces they do not need or use.
- Done right, this produces a flexible design.
- It is one of the five SOLID principles.
