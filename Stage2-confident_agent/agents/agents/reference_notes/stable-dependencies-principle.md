# Stable Dependencies Principle (SDP) and Instability Metric
keywords: SDP, stable dependencies, instability, stability, afferent coupling, efferent coupling, Ca, Ce, instability metric, I = Ce/(Ca+Ce)
- Dependencies should point in the direction of stability: modules intended to be easy to change should not be depended on by modules that are hard to change.
- Stability corresponds to the effort required to change a package: a package with many incoming dependencies is stable (hard to change); a package with many outgoing dependencies is unstable.
- Afferent coupling (Ca) is the number of classes outside the package that depend on classes inside it (incoming dependencies).
- Efferent coupling (Ce) is the number of classes inside the package that depend on classes outside it (outgoing dependencies).
- Instability I = Ce / (Ca + Ce), with range [0,1].
- I = 0 means a maximally stable package; I = 1 means a maximally unstable package.
- Worked example: Ca = 3, Ce = 1 gives I = 1 / (3 + 1) = 0.25.
