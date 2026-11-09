# Open-Closed Principle
keywords: Open-Closed Principle, Open/Closed Principle, open closed, OCP, open for extension, closed for modification

- The Open-Closed Principle states that a software entity should be open for extension but closed for modification.
- “Open for extension” means that new behaviour can be added when requirements change.
- “Closed for modification” means existing, tested source code should not need repeated edits for every new variation.
- Abstractions and polymorphism can let a program support new implementations through a stable interface.
- A common approach is to define an interface and provide separate implementations for different behaviours.
- For example, a payment service can depend on a `PaymentMethod` interface so that a new payment type can be added as another implementation.
- OCP does not mean that code must never change; it means likely points of variation should be designed to accommodate extensions.
- Applying OCP everywhere can add unnecessary abstractions, so it is most useful where change or new variants are reasonably expected.
