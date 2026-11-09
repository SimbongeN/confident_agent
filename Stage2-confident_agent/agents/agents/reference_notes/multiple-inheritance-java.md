# Multiple Inheritance in Java
keywords: multiple inheritance, Java classes, interfaces, extends, implements, default method conflict

- Java classes cannot directly extend more than one class.
- A Java class may implement multiple interfaces by listing them after `implements`.
- Implementing multiple interfaces allows a class to inherit multiple type contracts without inheriting state and implementation from multiple classes.
- An interface may extend more than one interface.
- Since Java 8, interfaces can declare default methods that include implementations.
- If a class inherits conflicting default implementations from unrelated interfaces, Java requires the conflict to be resolved explicitly.
- A class method implementation takes precedence over an interface default method in the relevant inheritance rules.
- Saying “Java does not support multiple inheritance” without qualification is imprecise: it prohibits multiple class inheritance but supports implementing multiple interfaces.
