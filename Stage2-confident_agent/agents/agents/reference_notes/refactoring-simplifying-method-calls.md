# Refactoring: Simplifying Method Calls
keywords: rename method, add parameter, remove parameter, separate query from modifier, parameterize method, preserve whole object, introduce parameter object, replace constructor with factory method, replace error code with exception, hide method
- Rename Method: rename a method whose name does not explain what it does.
- Add Parameter / Remove Parameter: add a parameter for missing data or remove an unused one.
- Separate Query from Modifier: split a method that returns a value and also changes the object into two methods.
- Parameterise Method: merge similar methods that differ only in internal values by using a parameter.
- Replace Parameter with Explicit Methods: split a method whose parts run depending on a parameter value into separate methods.
- Preserve Whole Object: pass the whole object instead of several of its values.
- Replace Parameter with Method Call: let the called method obtain the value itself.
- Introduce Parameter Object: replace a repeating group of parameters with an object.
- Remove Setting Method: if a field should only be set at creation, remove its setter.
- Hide Method: make a method private or protected if not used by other classes.
- Replace Constructor with Factory Method: use a factory method for a complex constructor.
- Replace Error Code with Exception; Replace Exception with Test when a simple condition check suffices.
