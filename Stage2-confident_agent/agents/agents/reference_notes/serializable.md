# Serializable
keywords: Serializable, java.io.Serializable, object serialization, marker interface, ObjectOutputStream, ObjectInputStream, serialVersionUID

- `java.io.Serializable` is a marker interface: it declares no methods.
- Implementing `Serializable` indicates that an object's class is eligible for Java's standard object-serialization mechanism.
- `ObjectOutputStream` can write serializable object data, while `ObjectInputStream` can read serialized object data.
- The serializable state generally consists of non-static, non-transient instance fields, subject to the serialization rules.
- A field whose referenced object is not serializable can cause serialization to fail with `NotSerializableException` unless handled appropriately.
- A `transient` field is excluded from the default serialization of an object's fields.
- Declaring a `serialVersionUID` lets a class specify a version identifier used during serialization compatibility checks.
- Deserializing untrusted data can be dangerous; serialized input should not be treated as safe merely because the class implements `Serializable`.
