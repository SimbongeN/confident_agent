# Event Handling and Listeners
keywords: event, listener, event handling, ActionListener, MouseListener, GUI, anonymous handler, Swing, JButton, callback, adapter class
- GUI programs are event-driven: the program waits for and responds to events (mouse clicks, key presses) that occur at unpredictable times; the main method typically just creates and shows the GUI components.
- Events are objects (e.g. MouseEvent, KeyEvent, ActionEvent) carrying information such as the source component, coordinates, time and which button; the system runs an event loop that waits for an event and calls a handler method, and the loop is not programmed explicitly.
- Three objects take part: the component that generates the event (the source, e.g. a button), the event object, and the event handler (listener).
- A listener is an object with event-handling methods; to listen, its class must be declared to implement the listener interface (e.g. ActionListener with actionPerformed, MouseListener) and define every method in it.
- Merely having the methods is not enough; the class must be declared to implement the interface.
- A listener must be registered with the component, e.g. button.addActionListener(listener) or comp.addMouseListener(listener); without registration the component does not know about it.
- Steps for mouse events: import java.awt.event.*; implement the listener interface; define its methods; register the listener object with the component.
- Any object can be a listener, including the component itself (addMouseListener(this)), a containing panel, a separate class, or a named nested class.
- MouseListener has five methods (mousePressed, mouseReleased, mouseClicked, mouseEntered, mouseExited) and all must be defined, with empty bodies if unused; the book advises mousePressed over mouseClicked.
- Anonymous inner classes are a common way to define listeners; an adapter class (such as MouseAdapter) provides empty definitions of all interface methods, so an anonymous subclass overrides only the methods needed.
