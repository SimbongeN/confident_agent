# Model-View-Controller (MVC)
keywords: MVC, model, view, controller, Observer pattern, Smalltalk, separation of concerns, user interface architecture
- The Model is the application's central component, holding data and managing logic and rules independent of the user interface.
- Fowler: model objects are "completely ignorant of the UI" and hold domain logic.
- The View is a representation of information, such as a chart, diagram or table; multiple views of the same information are possible.
- The Controller accepts input and converts it into commands for the model or view.
- In classic MVC, controllers update the model rather than the view directly.
- Controller and view should (mostly) not communicate directly but through the model.
- Views and controllers observe the model; when it changes, views update themselves (Fowler calls this Observer Synchronization).
- Sourcemaking: the Observer pattern's Subject is the keeper of the data model/business logic, and Observers are the "View" part of MVC.
- Sourcemaking says Observer captures the lion's share of the MVC architecture used in the Smalltalk community.
- Observer is a one-to-many dependency where dependents are notified and updated automatically when the subject changes state.
- Fowler's drawback: observer behavior is implicit, so it is hard to follow from the code and often needs a debugger.
