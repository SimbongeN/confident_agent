# Common Closure Principle (CCP)
keywords: CCP, common closure, closed together, package maintainability, same kinds of changes, single responsibility for packages
- Classes in a package should be closed together against the same kinds of changes.
- A change that affects a package affects all classes in that package and no other packages.
- CCP is the Single Responsibility Principle restated for packages, and is closely related to OCP for modules.
- It focuses on maintainability: when the code must change, the change should fall within one package rather than being spread across many packages.
- It minimises the workload of releasing, revalidating and redistributing the software.
- Since 100% closure is not attainable, design to be closed against the most common kinds of changes experienced; CCP groups classes open to the same types of change together.
- CCP reduces package release frequency by confining changes to only a few packages.
