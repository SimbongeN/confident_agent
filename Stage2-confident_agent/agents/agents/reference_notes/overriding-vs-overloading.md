# Overriding vs Overloading
keywords: overriding, overloading, override, overload, @Override, method signature, polymorphism, redefine method
- A child's method overrides a parent's method when it has the same signature (method name plus parameter list); parameter names do not matter, only types.
- Overridden: the version in the child's class is the one used by child objects; the parent's own objects keep the parent's version.
- Inside an overriding method, super.method() calls the parent version; unlike super(...) in a constructor, it need not be the first statement. This avoids duplicating code and picks up changes to the parent.
- Overriding rules: argument list must exactly match; return type must exactly match; the access level must not be more restrictive than the overridden method's (it may be less restrictive).
- Overloading: same method name with a different argument list; the compiler chooses which to invoke based on the arguments.
- Overloading rules: must change the argument list; may change the return type; may change the access modifier; may occur in the same class or in a subclass.
- Constructors can be overloaded but not overridden; methods can be either.
- Same name and parameters but a different return type is neither a valid override nor an overload, and is an error.
- Book's table: same types in different order (compute(String, int) vs compute(int, String)) is an overload; changing only the name (Compute vs compute) gives an additional, unrelated method.
