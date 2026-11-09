# Packages and JAR Files
keywords: package, import, jar file, API, classpath, namespace, java.util, jar
- A package groups related classes; packages can contain other packages (sub-packages), e.g. java.awt is the sub-package awt of java.
- Standard Java API packages named in the book: java.lang (String, Math, Integer, Double), java.util, java.io, java.net, java.awt, java.awt.event, and javax.swing.
- A class can be used by its full name (java.awt.Color) or, after an import directive, by its simple name; the import only allows simple names and imports nothing substantial.
- import package.* imports all classes of that package but not its sub-packages (import java.* does not import everything beneath java).
- If two imported packages contain classes with the same simple name (e.g. List in java.awt and java.util), using the simple name is ambiguous and a compile error; use the full name or import individual classes.
- All classes in java.lang are automatically imported into every program.
- To put a class in a package, begin the source file with a package declaration (before any import); the file must be in a folder with the same name as the package. A class automatically has access to other classes in its own package.
- A class not placed in a package is in the default package, which has no name.
- A jar (Java archive) file is a single file that can contain many classes; programs are generally distributed as jar files.
- An executable jar needs a manifest naming the main class (a Main-Class line); jar files are created with the jar command (e.g. cf for plain, cmf with a manifest) or an IDE export, and an executable jar runs with java -jar.
