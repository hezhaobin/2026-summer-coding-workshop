# Workshop notebooks

Google Colab materials distributed to students and instructors. The notebooks are also the workshop handout, so they must contain enough background, instructions, definitions, links, and interpretation guidance to remain useful after the event.

## Organization

- `morning/00_instructor_complete.ipynb`: minimal complete instructor notebook for 9:30 a.m.–12:30 p.m.; maintained on the development branch.
- `morning/python-in-biology-morning.ipynb`: paired student notebook intended for the student-facing `main` branch.
- `afternoon/00_instructor_complete.ipynb`: planned complete instructor notebook for 1:15–4:30 p.m.
- `../docs/notebook-00-instructor-complete-plan.md`: cell-level content and build plan for both halves.

Each half is self-contained and must run from top to bottom in a clean Colab runtime. The afternoon notebook must not depend on variables, imports, files, or execution state from the morning notebook.

## Instructor-first workflow

Build and verify the complete instructor notebook first, then derive the student
version with synchronized exercise identifiers and cell order. The instructor
version retains solutions and expected outputs; the student version retains
starter functions and behavior-based checks without solution code.

Every student exercise requires a synchronized instructor solution and a deterministic behavioral test. Student notebooks must not contain answer code in cells, comments, outputs, metadata, or collapsed content.

Notebooks load canonical workshop tables from `../input/processed/`; do not embed duplicate datasets or make notebooks the only implementation of data preparation. The two short example FASTA sequences used for the live SignalP/NetGPI exercise are intentionally embedded so that activity does not depend on file loading.

## Google Colab distribution

After the repository is public on GitHub, add an **Open in Colab** badge for each student notebook. The badge URL has this form:

`https://colab.research.google.com/github/OWNER/REPOSITORY/blob/main/notebooks/morning/NOTEBOOK.ipynb`

Students click the badge, sign in to Google if needed, and choose **File → Save a copy in Drive** before editing. As a fallback, they can open Colab, choose **File → Open notebook → GitHub**, and navigate to the public repository.

Do not add final badge URLs until the GitHub owner and repository name are known.

## Notebook source format

Use `.ipynb` as the sole notebook source for the initial workshop. Do not add Jupytext pairing yet. With two narrative-heavy handout notebooks, a second synchronized representation adds more process than value.

Keep reusable scientific functions in `../script/` and test them separately. Reconsider Jupytext only if notebook diffs or repeated structural edits become a real maintenance problem.
