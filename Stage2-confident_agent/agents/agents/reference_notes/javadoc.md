# Javadoc
keywords: javadoc, documentation comment, API documentation, @param, @return, doc comment
- javadoc is a Java tool that extracts specially formatted comments from source code and generates HTML documentation pages.
- A Javadoc comment looks like an ordinary block comment but begins with /** instead of /*, and immediately precedes the thing it documents (a class, method or member variable).
- By default javadoc collects information only about public classes, methods and member variables, but it can be asked to document non-public items too.
- If there is no Javadoc comment, javadoc generates one containing only syntactic information (names, types, return types, parameter lists); semantics and pragmatics must be written by the programmer.
- Javadoc comments may contain HTML markup (e.g. a paragraph tag), which is copied to the generated pages.
- Doc tags begin with the @ character; the book covers @param, @return and @throws.
- Doc tags go at the end of the comment, after the description, and may appear in any order; each description ends at the next tag or the end of the comment.
- Use a @param tag for each parameter, @throws for each exception you want to document, and @return only for a non-void method.
- Javadoc output can document a method's purpose, parameters, pre-conditions, post-conditions and exceptions; the standard Java API documentation was produced with javadoc.
- javadoc can be run from the command line or from an IDE such as Eclipse (Export, then Javadoc).
