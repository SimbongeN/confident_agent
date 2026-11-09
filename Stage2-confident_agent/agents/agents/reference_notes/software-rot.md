# Software Rot: Rigidity, Fragility, Immobility, Viscosity
keywords: software rot, design rot, rigidity, fragility, immobility, viscosity, symptoms of rotting design, Robert Martin, software degradation
- Software lives only as long as it best meets user, business and system requirements; requirements and technology keep changing, so software must evolve or perish.
- Software rot (Martin 2000) has four symptoms: rigidity, fragility, immobility and viscosity. A design showing these is rotting from the inside out.
- Rigidity: it is hard to make even the simplest change; the slightest change has ripple and cascading effects; a day's work turns into a man-month's work; fear of fixing non-critical problems makes the software more rigid.
- Fragility: the sister of rigidity; the software breaks each time it is changed, often in unrelated areas; a fix may break the software in unexpected ways, and every fix creates more problems, leading to loss of control.
- Immobility: inability to reuse software from other parts of the project; parts are rewritten because they carry too much baggage; reuse has high risk.
- Viscosity has two forms: viscosity of the design and viscosity of the operating environment. When changes can be done in more than one way, hacks are easier than design-preserving methods; it is easier to do the wrong thing than the right thing.
- High viscosity of design means the design-preserving way of making a change is harder than a hack.
- Degradation happens because requirements change and the requirements specification is volatile; changes often unanticipated at design time normally violate the initial design.
