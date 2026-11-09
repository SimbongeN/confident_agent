# Common Reuse Principle (CRP)
keywords: CRP, common reuse, classes reused together, package dependency, revalidation, rerelease, inseparable classes
- The classes in a package are reused together: if you reuse one class in a package, you reuse them all.
- Classes that tend to be reused together belong in the same package; classes not tightly bound by class relationships should be in separate packages.
- When one package uses another a dependency is created between packages, and it is not weakened even if only one class of the called package is used.
- Every time the called package is released, the calling package must be revalidated and rereleased.
- A dependency on a package is a dependency on every class in it, so the classes are inseparable; otherwise more is revalidated and redistributed than necessary, wasting effort.
- CRP helps avoid recompiling, relinking and retesting user code after a new release when the classes it actually uses did not change.
- CRP can be used to break package cycles by splitting packages.
