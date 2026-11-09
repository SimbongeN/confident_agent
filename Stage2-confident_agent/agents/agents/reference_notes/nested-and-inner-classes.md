# Nested and Inner Classes
keywords: nested class, inner class, static nested class, anonymous class, anonymous inner class, local class, outer class
- A nested class is any class defined inside another class (it can even be inside a method); nested classes are named or anonymous, and a named nested class is static or non-static.
- A static nested class has the static modifier and is part of the static structure of the containing class; outside the container its name is qualified, e.g. WireFrameModel.Line, and inside it is created with new Line().
- A static nested class has full access to the container's static members, even private ones, and the containing class has full access to the nested class's members, even private ones; a nested class can itself be private.
- A nested class compiles to a separate class file, e.g. WireFrameModel$Line.class.
- Non-static nested classes are called inner classes; they are associated with an object of the containing class, which has its own copy of the inner class with access to that object's instance variables and methods, even private ones.
- Rule of thumb: if the nested class needs instance variables or instance methods of the containing class, make it non-static; otherwise make it static.
- To create an inner class object you need an object of the containing class; from outside it is created as game.new Player(), while inside an instance method plain new Player() works.
- An anonymous inner class is defined and instantiated in one expression: new SuperclassOrInterface(parameters) { members }; it creates an unnamed class and one object of it.
- If based on an interface, the anonymous class must implement all the interface's methods and the parameter list must be empty; if based on a class, the parameters go to a superclass constructor.
- Anonymous classes are often used for actual parameters and for GUI event handling; each compiles to its own file such as MainClass$1.class.
