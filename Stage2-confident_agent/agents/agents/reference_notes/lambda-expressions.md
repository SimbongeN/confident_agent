# Lambda Expressions
keywords: lambda, lambda expression, functional interface, arrow syntax, Java 8, anonymous function
- Lambda expressions are a Java 8 feature offering a shorter syntax than an anonymous class when the anonymous class implements an interface that defines just one method.
- General syntax: formal-parameter-list -> method-body.
- The body can be a single expression, a single method call, or a block of statements in braces.
- When the body is a single expression or call, its value is automatically the return value of the method being defined.
- Parameter types need not be given, though they can be; parentheses around the parameter list are optional only when there is exactly one parameter with no declared type.
- With no parameters, the parameter list is an empty set of parentheses.
- Lambdas can only be used where the compiler can infer the types; e.g. the parameter g is known to be Graphics because a Drawable is expected and its only method takes a Graphics.
- Book example: the call drawTwice(firstG, secondG, g -> g.drawOval(10,10,100,100)) replaces a new Drawable() anonymous class.
- Other forms shown: () -> System.out.println("Hello World"), (a, b) -> a + b, and a block-bodied lambda with a typed parameter (int n).
- The book gives only a brief introduction to lambda expressions.
