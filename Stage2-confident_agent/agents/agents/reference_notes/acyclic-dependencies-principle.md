# Acyclic Dependencies Principle (ADP)
keywords: ADP, acyclic dependencies, dependency cycle, directed acyclic graph, DAG, package dependency graph, break cycles
- No cycles are allowed in the package dependency graph; the package structure should be a directed acyclic graph (DAG).
- It allows a project to be stabilised and released in pieces and organises package dependencies in a top-down hierarchy.
- Cycles cause the 'morning after' problem: a package that worked yesterday breaks because a package it depends on changed; when this happens often, developers interfere with each other and the project is hard to stabilise and release.
- The example is a cycle between the MyDialogs and MyApplication packages.
- Cycles can be broken with abstract interfaces (DIP), by splitting packages (CRP) or by reorganising packages, e.g. creating a new package on which both depend.
