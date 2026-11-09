# Everything Is Not an Object (Primitives)
keywords: primitive type, primitive, int, boolean, wrapper class, autoboxing, not an object, value type
- Java has primitive types (e.g. int, double, char, boolean) and object (class) types; primitive values are not objects.
- The book says primitives were kept as non-objects for memory and processing efficiency, since an int takes less memory than an object.
- Wrapper classes (Integer, Double, Character, Long, Short, Byte, Float, Boolean) contain a single primitive value so it can be treated as an object.
- Collections can only hold objects, so a primitive must be put in a wrapper object first.
- Autoboxing (Java 5.0) automatically converts a primitive to its wrapper object where an object is required; unboxing converts back, e.g. a Double used in an arithmetic expression.
- Wrapper classes hold static methods such as Double.parseDouble (convert strings to numbers) and constants such as Integer.MIN_VALUE and Integer.MAX_VALUE.
- For Double (and Float), MIN_VALUE is the smallest positive value, not the most negative.
- Double has special values POSITIVE_INFINITY, NEGATIVE_INFINITY and NaN; real-number operations never throw an exception but may give these values.
- Use Double.isNaN(x) to test for NaN; x == Double.NaN and x != Double.NaN are both false for every x.
- Primitive parameters are passed by copying the value, so a method cannot change the caller's primitive variable.
