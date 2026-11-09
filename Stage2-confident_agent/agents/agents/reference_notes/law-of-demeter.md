# Law of Demeter
keywords: Law of Demeter, principle of least knowledge, loose coupling, object navigation, delegation, train wreck

- The Law of Demeter is a design guideline often summarised as “talk only to your immediate friends.”
- A method should generally communicate with objects it directly knows, such as its parameters, its own fields, and objects it creates.
- The guideline discourages long chains of calls that navigate through several unrelated objects.
- A chain such as `order.getCustomer().getAddress().getCity()` can make the caller depend on the internal structure of several other objects.
- Encapsulating a request in a method on the nearer object can reduce knowledge of those internal relationships.
- Following the guideline can reduce coupling and make internal implementation changes less likely to affect callers.
- The Law of Demeter is a heuristic, not a strict language rule; some chained calls are harmless or expressive.
- Applying it mechanically can create many forwarding methods, so the goal is to reduce inappropriate knowledge rather than eliminate every dot in an expression.
