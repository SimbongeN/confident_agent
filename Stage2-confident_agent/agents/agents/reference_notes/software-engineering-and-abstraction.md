# Software Engineering and Abstraction
keywords: software engineering, abstraction, information hiding, life cycle, waterfall, encapsulation, modularity, object-oriented analysis and design
- Software engineering is the systematic approach to programming using accepted principles of good design; it aims to build programs that verifiably meet their specifications and are easy to modify.
- The software life cycle stages: specification, analysis, design, coding, testing and debugging, then a long maintenance period; in practice the stages are seldom strictly consecutive (e.g. a testing problem sends you back to coding or even design).
- Listed engineering tasks: requirements analysis, specification, design and architecture, coding, testing, documentation, maintenance.
- Maintenance (fixing new problems and adapting to changed requirements) can take far more time than initial development; the book says about 2/3 of software engineering work is maintenance, mostly extending systems.
- Object-oriented software engineering rests on three principles: abstraction (ignore the details), modularization (break into pieces), and information hiding (separate implementation from function).
- Information hiding hides the design decisions most likely to change behind a stable interface, so other parts of the program are protected if those decisions change.
- A method is an abstraction mechanism and a black box: the interface should be simple, well-defined and easy to understand; users need to know only the interface, not the implementation; the implementor need not know the larger system. The implementation can change if outward behavior does not.
- A method's interface has a syntactic part (how to call it) and a semantic part (what it does); together they are the method's contract.
- A precondition must be true when the method is called (an obligation of the caller, e.g. Math.sqrt needs x at least 0); a postcondition is what is true after it runs (the callee's guarantee). Write them as comments.
- A class is also a black box: its public part is the interface and the private part is hidden; users need to know what a method does (its signature), not how.
