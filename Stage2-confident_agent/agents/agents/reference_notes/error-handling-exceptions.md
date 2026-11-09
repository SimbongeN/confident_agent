# Error Handling (Exceptions)
keywords: exception, error handling, try, catch, throw, throws, checked exception, unchecked exception, finally, stack trace
- By default an error during execution terminates the program and prints an error message; try..catch lets the program catch the error and respond differently.
- "Exception" is used in preference to "error" because an exception is an exception to normal control flow and may not be an error at all.
- Exceptions are objects of type Exception; actual exceptions are defined by subclasses of Exception.
- NumberFormatException occurs when a string cannot be converted to a number (e.g. Integer.parseInt applied to "fred").
- IllegalArgumentException can occur when an illegal value is passed to a method; it is also thrown by an enum's valueOf when the string is not the name of one of the enum's values.
- When an exception occurs it is "thrown"; in try..catch the catch part runs if an exception of the named type occurs in the try part, skipping the rest of the try statements.
- Within the catch block the declared variable represents the exception object; afterwards execution continues with the rest of the program.
- Only the exception type named in the catch clause is caught; any other type still crashes the program. The braces in try..catch are required even for one statement.
- Catching an exception and carrying on is not always wise; sometimes it is better to let the program crash where the error occurs, but in some cases (e.g. re-asking the user for input) recovery is easy.
- Javadoc's @throws tag documents the exceptions a method may throw.
