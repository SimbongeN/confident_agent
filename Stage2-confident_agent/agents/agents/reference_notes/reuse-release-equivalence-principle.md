# Reuse-Release Equivalence Principle (REP)
keywords: REP, reuse release equivalence, granule of reuse, granule of release, releasable package, package versioning, release numbers
- The granule of reuse is the granule of release: only components released through a tracking system can be effectively reused, and that granule is the package.
- If a package contains software that should be reused, it should not also contain software that is not designed for reuse; either all classes in the package are reusable or none are.
- Reusers expect complete, accurate, up-to-date documentation; maintenance (enhancements and bug fixes); reliability (no major bugs, no sudden unexpected changes, proven versions that stay long).
- Requirements for reusable software: place reusable components in a package, track package versions, assign release numbers to stable releases, write release notes, and allow portability to legacy releases for a while.
- Classes within a package must form a reusable and releasable unit: coherent functionality, controlled dependencies on other packages, requirements on other packages specified; this reduces the reuser's work.
- REP groups packages for code reusers (REP and CCP form a triangle of tensions with CRP: REP group for reusers, CCP group for maintainers, CRP split for common reuse).
