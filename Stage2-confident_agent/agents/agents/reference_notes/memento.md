# Memento
keywords: memento, memento pattern, snapshot, save state, restore state, originator, caretaker, undo
- Intent: without violating encapsulation, capture and externalize an object's internal state so the object can be restored to this state later. Also known as Token. Object behavioral.
- Use when a snapshot of (some portion of) an object's state must be saved for later restoration, and a direct interface to obtain the state would expose implementation details and break encapsulation.
- Motivation: needed for checkpoints and undo; the book's example is a ConstraintSolver whose public interface cannot precisely reverse its effects, so it hands out a memento (SolverState) instead of exposing internals.
- Participants: Memento (stores originator's internal state at the originator's discretion; has a narrow interface for others and a wide one for the originator), Originator (creates a memento of its state and uses it to restore itself), Caretaker (keeps the memento safe; never operates on or examines its contents).
- Collaboration: the caretaker requests a memento, holds it, and passes it back to the originator (sometimes never, if no revert is needed). Mementos are passive; only the originator assigns or retrieves their state.
- Benefits: preserves encapsulation boundaries; simplifies Originator, since clients manage the saved state.
- Liabilities: mementos might be expensive (copying large state or frequent use); it may be difficult in some languages to guarantee only the originator can access memento state (narrow vs wide interface); hidden costs for the caretaker, which does not know how much state a memento holds.
- Known uses: Unidraw connectivity (CSolver); Dylan collections' iteration state objects; QOCA constraint solver storing incremental state in mementos.
- Related: Command can use mementos to keep state for undoable operations; Iterator can use mementos to capture iteration state.
