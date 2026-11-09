# Flyweight
keywords: flyweight, flyweight pattern, sharing, intrinsic state, extrinsic state, fine-grained objects
- Intent: use sharing to support large numbers of fine-grained objects efficiently. Object structural.
- Key concept: intrinsic state is stored in the flyweight and is context-independent (so sharable); extrinsic state depends on context and cannot be shared, so clients pass it to the flyweight when needed.
- Apply only when all hold: the application uses a large number of objects; storage costs are high because of quantity; most object state can be made extrinsic; many groups of objects can be replaced by few shared ones; and the application does not depend on object identity (identity tests return true for conceptually distinct objects).
- Participants: Flyweight (interface receiving extrinsic state), ConcreteFlyweight (adds intrinsic state storage; must be sharable), UnsharedConcreteFlyweight (not all flyweights need sharing, e.g. Row, Column), FlyweightFactory (creates/manages flyweights, supplies an existing instance or creates one), Client (holds references; computes or stores extrinsic state).
- Clients must get ConcreteFlyweights only from the FlyweightFactory so sharing works properly.
- Consequences: run-time cost of transferring, finding or computing extrinsic state, offset by space savings that grow as more flyweights are shared; greatest savings when objects have much intrinsic and extrinsic state and the extrinsic state is computed rather than stored.
- Often combined with Composite to represent a hierarchy as a graph with shared leaves; shared leaf nodes cannot store a parent pointer (it is passed as extrinsic state).
- Known uses: Doc editor (Interviews) with one glyph per character, reportedly 480 character objects for 180,000 characters; ET++ Layout objects for look-and-feel independence (flyweights acting as strategies).
- Related: State and Strategy objects are often best implemented as flyweights; ET++ Look class is an Abstract Factory supplying Layout flyweights.
