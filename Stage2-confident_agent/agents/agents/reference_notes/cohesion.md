# Cohesion
keywords: cohesion, high cohesion, low cohesion, functional cohesion, coincidental cohesion, logical, temporal, procedural, communicational, sequential, single responsibility
- Cohesion is the degree to which the elements inside a module belong together.
- In object-oriented programming it measures how strongly a class's methods and data relate to one unifying purpose.
- It is an ordinal measure, usually described as high or low.
- High cohesion is linked to robustness, reliability, reusability and understandability.
- Low cohesion makes code harder to maintain, test, reuse or understand.
- High cohesion often correlates with loose coupling, and the reverse also tends to hold.
- Coincidental cohesion (worst): parts are grouped arbitrarily, such as in a "Utilities" class.
- Logical cohesion: parts are grouped because they fall under the same category though they work differently, such as all input-handling routines.
- Temporal cohesion: parts are grouped because they run at the same time, such as cleanup steps after an exception.
- Procedural cohesion: parts are grouped because they follow a fixed execution sequence.
- Communicational cohesion: parts operate on the same data. Sequential cohesion: one part's output feeds the next.
- Functional cohesion (strongest): parts all contribute to one well-defined task. Perfect (atomic) cohesion: the module cannot be reduced further.
