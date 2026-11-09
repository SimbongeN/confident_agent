# Refactoring: Simplifying Conditional Expressions
keywords: decompose conditional, consolidate conditional expression, guard clauses, replace conditional with polymorphism, introduce null object, introduce assertion
- Decompose Conditional: extract the condition, then and else parts into separate methods.
- Consolidate Conditional Expression: combine multiple conditionals leading to the same result into one expression.
- Consolidate Duplicate Conditional Fragments: move identical code found in all branches outside the conditional.
- Replace Nested Conditional with Guard Clauses: put special checks and edge cases first as a flat list of conditionals.
- Replace Conditional with Polymorphism: create subclasses matching the branches and move each branch into an overriding method.
- Introduce Null Object: return an object with default behaviour instead of null to remove null checks.
- Introduce Assertion: replace assumptions about required conditions with explicit assertion checks.
