# Morning notebook

Current files:

- `00_instructor_complete.ipynb`: development-branch instructor version.
- `python-in-biology-morning.ipynb`: student version for the student-facing `main` branch.

Workshop time: 9:30 a.m.–12:30 p.m.

Contents: orientation, adhesin biology, ALS1/PHO84 comparison, guided SignalP
and NetGPI submissions, loop-based residue counting, whole-protein S/T
frequency, sliding-window profiles, and a supplied two-proteome comparison of
known adhesins with all proteins.

The paired notebooks implement the morning portion of
`../../docs/notebook-00-instructor-complete-plan.md`. The instructor version
contains complete solutions and expected outputs. The student version preserves
the same exercise order while replacing solution code with starter functions and
collapsed behavior-based checks.

Both notebooks use provided infrastructure to prepare pinned Biopython, load the
frozen *S. cerevisiae* S288C and *C. albicans* SC5314 proteomes plus the validated
KN known-adhesin IDs, verify SHA-256 checksums, and parse the FASTA records with
`Bio.SeqIO`. The instructor copy downloads from `dev`; the student copy downloads
from the student-facing `main` branch. Repository files are used directly during
local execution.

Both notebooks have been executed from top to bottom in clean local Jupyter
kernels. The student copy contains no solution implementations or stored feature
answers.
