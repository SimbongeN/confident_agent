# Observer
keywords: observer, observer pattern, publish-subscribe, subject, notify, update, dependents, one-to-many, model-view-controller, MVC
- Intent: define a one-to-many dependency so that when one object (the subject) changes state, all its dependents (observers) are notified and updated automatically. Also known as Dependents, Publish-Subscribe.
- Use when an abstraction has two aspects, one dependent on the other, and you want them in separate objects so they can vary and be reused independently.
- Use when a change to one object requires changing others and you do not know how many; or when an object should notify others without assuming who they are (i.e. without tight coupling).
- Participants: Subject (knows its observers; provides attach/detach), Observer (defines the updating interface), ConcreteSubject (stores state of interest; notifies observers on change), ConcreteObserver (holds a reference to the ConcreteSubject, keeps its state consistent, implements update).
- Collaboration: after being notified, a ConcreteObserver may query the subject for information to reconcile its state. Notify is not always called by the subject; an observer or another object can call it.
- Consequence: subjects and observers vary independently; observers can be added without modifying the subject. Coupling is abstract and minimal (the subject only knows a list of objects conforming to the Observer interface), so they can sit in different layers of abstraction.
- Consequence: supports broadcast communication; the notification names no receiver, and observers can be added/removed at any time.
- Liability: unexpected updates. Observers do not know about each other, so a seemingly harmless change to the subject can cause a cascade of updates; the simple update protocol also does not say what changed.
- Known use: Smalltalk Model/View/Controller (Model is the Subject, View is the base class for observers); also Interviews, Andrew Toolkit, Unidraw.
- Related: Mediator (a ChangeManager encapsulating complex update semantics acts as a mediator between subjects and observers); Singleton (a ChangeManager may be a Singleton).
- Distinguishing from Mediator (Ch. 5 discussion): Observer distributes communication among Subject and Observer objects, Mediator centralizes it; Observers/Subjects are easier to make reusable, but Mediator's communication flow is easier to understand. Observer is best for decoupling when there are data dependencies, and its sender-receiver binding is looser than Command's.
