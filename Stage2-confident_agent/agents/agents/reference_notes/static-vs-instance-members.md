# Static vs Instance Members
keywords: static, instance, class member, instance member, static method, static variable, static import, non-static, this
- Class members (variables and methods) are either static or non-static, depending on whether they are declared with the keyword static.
- Non-static members are instance variables and instance methods; static members are class variables and class methods.
- Each object gets its own copy of every instance variable; a static (class) variable is shared by all instances, so a change made through one object is seen by all.
- Static members belong to the class itself and can be used from the class directly (for example Math.sqrt) without creating an object; instance methods must be invoked on a particular object.
- The non-static parts of a class describe what every created object will contain; the book says instance methods are better thought of as belonging to the object, not the class.
- A class may be only static, only non-static, or mixed; instance methods may use static variables and call static methods, which effectively lets many objects share one variable.
- Static variable initialization is executed just once, when the class is first loaded; instance variable initializers run each time an object is constructed.
- Book example: a static nextUniqueID counter incremented in the Student constructor, with a private instance variable ID giving each student a unique number.
- A static import (import static package.Class.member, or .*) lets static members be used by simple name, e.g. out or sqrt; it requires a package name, so it cannot be used for a class in the default package.
