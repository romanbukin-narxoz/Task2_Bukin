# Verification record

Verified on 2026-10-12 in the available Linux environment using Python 3.12.14
and the exact five runtime package versions in requirements.txt.

- Default ten-row smoke run completed with exit code 0 and three metric rows.
- A second run from a different working directory also completed.
- Quality metrics and confusion counts matched across repeated smoke runs; timings vary.
- Train and test identifiers were disjoint (six train, four test).
- Confusion counts and false positive rate arithmetic were checked.
- A separate artificial 40-row fixture exercised all three training fractions and five seeds:
  45 metric rows, with training subset sizes 8, 16 and 32. This fixture is not research evidence.

No real-corpus experiment or hypothesis test was performed. A clean installation from
PyPI and execution on the student's Windows machine have not been independently verified.
No Docker build was performed; this project uses the pinned requirements alternative.
Generated result files and validation fixtures are excluded from the distributable repository.
