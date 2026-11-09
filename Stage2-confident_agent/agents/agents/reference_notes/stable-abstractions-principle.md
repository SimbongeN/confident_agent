# Stable Abstractions Principle (SAP) and Main Sequence
keywords: SAP, stable abstractions, abstractness, main sequence, A vs I plot, zone of pain, zone of uselessness, abstractness metric
- A stable package should be abstract so that its stability does not prevent it from being extended; stability implies abstraction.
- Stable packages contain high-level design; making them abstract opens them to extension but closes them to modification (OCP).
- An unstable package should be concrete so its instability lets the concrete code be changed easily.
- Abstractness A = Na / Nc, where Na is the number of abstract classes in the package and Nc the number of classes; A has range [0,1] and A = 0 means no abstract classes.
- Abstract packages should be responsible and independent (stable); concrete packages should be irresponsible and dependent (unstable).
- On the A vs I plot: abstract and stable (I=0, A=1) is good; unstable and concrete (I=1, A=0) is good; abstract and unstable is probably useless; stable and concrete (I=0, A=0) is problematic (examples: database schema, STL).
- Packages should lie close to the main sequence, the line between (0,1) and (1,0); a package on it is neither too abstract for its stability nor too unstable for its abstractness.
- Metrics I and A help quantify code quality; other metrics include code volume and growth rate, and bug discovery and extinction rate.
