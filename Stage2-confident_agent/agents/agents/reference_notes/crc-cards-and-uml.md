# CRC Cards and UML
keywords: CRC cards, class-responsibility-collaboration, UML, class diagram, unified modelling language, responsibilities, collaborators, association, multiplicity
- A simple analysis approach: describe the problem, underline the nouns (candidate classes or objects) and the verbs (candidate methods).
- Design goals stated: responsibility-driven design (each class responsible for its own data), loose coupling (classes largely independent, communicating via a small well-defined interface), and cohesion (each class performs one task).
- CRC (Class-Responsibility-Collaboration) cards are a brainstorming tool proposed by Ward Cunningham, used when first deciding which classes are needed and how they interact.
- A CRC card (an index card) records the class name, the package name (if applicable), the class's responsibilities, and the other classes it collaborates with.
- A team walks through usage scenarios against the cards to check that the responsibilities cover them; the small card keeps the design simple and stops a class getting too many responsibilities.
- UML (Unified Modelling Language) is a notation to specify, visualize and document object-oriented models; it is not a development method and does not say what to do first.
- Class diagrams show classes and their static relationships (not method calls); a class is a rectangle with name, attributes and operations compartments. Visibility markers: + public, # protected, - private.
- Relationships: generalization (inheritance, arrow to the base class), association (with roles and multiplicity), aggregation (whole-part, open rhombus on the whole's side), composition (stronger whole-part where parts die with the whole, solid rhombus).
- Use case diagrams show actors and use cases (what the system should do, not how); sequence diagrams show the order of messages between objects over time (dashed vertical lifelines, time running downwards).
