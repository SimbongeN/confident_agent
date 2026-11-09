# Coupling: types and metrics
keywords: coupling, tight coupling, loose coupling, content coupling, common coupling, control coupling, stamp coupling, data coupling, external coupling, fan-in, fan-out, low coupling high cohesion
- Coupling is the degree of interdependence between software modules: how closely two routines or modules are connected.
- Low coupling is generally seen as a sign of good design, especially when paired with high cohesion.
- Loose (low) coupling: modules interact through simple, stable interfaces without depending on each other's internals.
- Tight (high) coupling: a change in one module often forces changes in others, and the modules are harder to reuse, test and assemble.
- Content coupling (highest): one module relies on another's internal code; it breaks information hiding.
- Common coupling: several modules access the same global data, which can spread errors and cause side effects.
- External coupling: modules share an imposed data format, protocol or device interface.
- Control coupling: one module directs another's behavior by passing a flag or instruction.
- Stamp (data-structured) coupling: modules pass a composite structure but use only part of it.
- Data coupling: modules share only elementary values through parameters. Other types listed: subclass and temporal coupling.
- Pressman-style metrics count data and control flow parameters, global variables, and fan-in and fan-out (environmental coupling).
- Coupling measures dependence between modules; cohesion measures how related the functions inside one module are. Low coupling often goes with high cohesion.
