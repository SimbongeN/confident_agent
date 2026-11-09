# Refactoring: Composing Methods
keywords: extract method, inline method, extract variable, inline temp, replace temp with query, split temporary variable, replace method with method object, substitute algorithm, remove assignments to parameters
- Extract Method: group a code fragment into a new method and replace it with a call.
- Inline Method: when a method body is more obvious than the method itself, replace calls with the body and delete the method.
- Extract Variable: put the result of a hard-to-understand expression (or parts) into self-explanatory variables.
- Inline Temp: replace a temp variable holding a simple expression with the expression itself.
- Replace Temp with Query: move the expression to a separate method and query it instead of using a local variable.
- Split Temporary Variable: use a different variable for each intermediate value, each responsible for one thing.
- Remove Assignments to Parameters: use a local variable instead of assigning to a parameter.
- Replace Method with Method Object: turn a long method with intertwined locals into its own class whose fields are the locals, then split it into methods.
- Substitute Algorithm: replace the body of the method with a new algorithm.
