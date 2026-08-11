# Python in Biology Workshop: revised plan

Status: working specification, revised 2026-08-09

Planning source: ChatGPT task “Python in Biology Workshop” (`6a637d4e-ff88-83ea-a671-c3a1bdc7bd57`) plus the 2026-08-08 feature and machine-learning revisions.

## Audience and purpose

This is a one-day, in-person workshop for students who have completed an introductory CodeHS Python course centered on Tracy the Turtle, with small bioinformatics exercises such as calculating GC content.

The primary goal is for students to use familiar Python concepts to answer a real biological question. Machine learning is a brief capstone for interpretation, not the organizing theme.

The day follows this storyline:

> protein sequence → measurable features → group differences → simple classifier → candidate interpretation

By the end, every student should be able to:

- explain how protein length and S/T frequency are calculated;
- write or complete a Python function operating on a protein sequence;
- apply a function to example proteins using provided infrastructure;
- interpret a comparison between adhesins and non-adhesins;
- explain at least one branch and one error from a shallow decision tree;
- state why a computational prediction still requires biological validation.

Independent Pandas manipulation, plotting from scratch, package installation, web automation, and model tuning are not required learning outcomes.

## Biological question

Can transparent sequence features help distinguish known fungal adhesins from other proteins, and can those features help prioritize candidate adhesins in *Candida auris*?

The reference proteomes are:

- *Saccharomyces cerevisiae* S288C — UniProt `UP000002311`
- *Candida albicans* SC5314 — UniProt `UP000000559`
- *Candida auris* B8441 — UniProt `UP000230249`

The workshop snapshot uses UniProt release `2026_02`, released 2026-06-10. UniProt
currently records *C. auris* under the accepted name *Candidozyma auris* and
retains *Candida auris* as a synonym; workshop-facing language continues to use
the familiar name *Candida auris*.

The curated positive and negative sets provide labels for teaching and evaluation. The origin and rules for the negative set must be confirmed before final model evaluation.

## Feature roles

### Screening and comparison outputs

- FungalRV continuous score: used to compare with the student model and as one component of the advanced-feature eligibility screen; never used as a student-model predictor.
- SignalP score and source prediction call: retained as localization evidence and one component of the eligibility screen.
- PredGPI Y/N call: retained as localization evidence and one component of the eligibility screen.

All raw values and calls are retained. Pass thresholds for FungalRV and SignalP must be explicitly documented; they are not inferred from the available table.

### Student-calculated features

- protein length;
- whole-protein S/T frequency;
- maximum S/T frequency in an overlapping sliding window, initially 50 amino acids.

### Optional advanced features

- beta-aggregation summaries from TANGO, if installation, licensing, parameters, runtime, and output interpretation are feasible;
- tandem-repeat summaries from XSTREAM, if installation, licensing, runtime, and output interpretation are feasible.

Initially, TANGO and XSTREAM are calculated only for proteins passing at least two of the FungalRV, SignalP, and PredGPI screens. Their missing values must not be replaced with zero. Models using these features must either be restricted to that eligible subset or wait until the features have been calculated for all labeled proteins.

NetGPI is an optional comparison, not a guaranteed pipeline component. If no supported API or batch interface exists, use manual submission plus parsing of saved output rather than automating the web form.

## Revised one-day agenda

The target day is 9:30 a.m.–4:30 p.m., with 45 minutes for lunch and two 15-minute breaks.

### 9:30–10:00 — Biological introduction and day overview

Cover fungal adhesin function, why adhesins matter, canonical architecture, secretion signal, adhesive/effector domain, S/T-rich stalk, tandem repeats, C-terminal GPI-anchor signal, prediction difficulty, and FungalRV as an existing predictor. Use the final five minutes for the schedule.

### 10:00–10:30 — Examine example proteins and use prediction servers

Compare *Candida albicans* ALS1, a known adhesin, with PHO84, a plasma-membrane phosphate transporter. Students first inspect the sequences and predict what they expect to find. They then submit the embedded sequences to the SignalP 6.0 server, using the Eukarya setting, and interpret the predicted class, probability, and cleavage site when present.

Students next use NetGPI 1.1 to evaluate appropriate secretory-pathway candidates and interpret the GPI-anchor call and predicted omega site. Explicitly teach that NetGPI assumes prior evidence for entry into the secretory pathway; a result should not be interpreted independently of SignalP or equivalent evidence. The notebook contains the server URLs, complete FASTA sequences, step-by-step submission settings, result-recording questions, and backup result examples in case the live services are unavailable.

### 10:30–11:30 — Python refresher and Challenge 1A

Begin from the for-loop knowledge shared by the class rather than assuming string methods. Students first write and test a two-input function that counts one letter in a word using a loop. They use it to calculate whole-protein S/T frequency for ALS1 and PHO84, compare the values, and inspect ALS1 by eye for uneven S/T distribution. Introduce the string `.count()` method only after this loop-based foundation.

### 11:30–11:45 — Break

### 11:45–12:30 — Sliding windows and connection to a dataset

Develop the sliding-window algorithm first in words or pseudocode. Students complete a scaffolded function that returns an ordered list of S/T frequencies for every overlapping window; they may use either `.count()` or their loop-based counting function. A visible global variable stores the 50-residue teaching window. Supplied code plots each list against window-midpoint protein positions for ALS1 and PHO84. Students then use `max()` to report maximum local S/T frequency. Provided infrastructure loads and combines the frozen *S. cerevisiae* and *C. albicans* proteomes, applies the student functions, and compares the 30 validated KN known adhesins with the entire combined proteome.

### 12:30–1:15 — Lunch

### 1:15–1:35 — From biological rules to one decision tree

Begin with a human-readable rule and introduce features, labels, branches, leaves, training examples, predictions, and overfitting. Use a short external video excerpt only if it directly supports this explanation.

### 1:35–1:55 — Guided toy-tree demonstration

The instructor runs a fixed shallow tree using SignalP score and the PredGPI binary call. Contrast its output with an all-negative classifier. Explain the confusion matrix, precision, recall, and F1 score in the context of an imbalanced positive/negative dataset. Keep FungalRV out of the model and reveal it afterward as a comparison.

### 1:55–2:20 — Everyone runs and interprets the same model

Students execute supplied model code, trace example proteins through the tree, identify one correct and one incorrect prediction, and answer interpretation questions. They do not tune depth, compare algorithms, or compete on scores.

### 2:20–2:35 — Break

### 2:35–3:20 — Expanded-feature challenge

Students use a common, instructor-prepared table to ask how adding protein length, whole-protein S/T frequency, and maximum local S/T frequency changes the tree or its errors. If available, they also examine beta-aggregation and tandem-repeat summaries. Use of those selectively computed advanced features is conditional on having enough eligible labeled proteins from both classes. Otherwise, complete the challenge with length and S/T features only.

The challenge is comparison and biological reasoning, not feature-selection competition.

### 3:20–4:00 — *C. auris* candidate interpretation

Apply one provided common model or rule to a prepared *C. auris* table. Examine three to five preselected candidates using model features, SignalP, PredGPI, tandem-repeat/beta-aggregation evidence when available, and the withheld FungalRV score. Do not treat model probability or class votes as biological confidence.

### 4:00–4:30 — Synthesis, limitations, and validation

Discuss false positives such as other GPI-anchored cell-wall proteins, data leakage, class imbalance, homologous-family overlap, what the tree learned, what FungalRV agrees or disagrees with, and experiments that could validate adhesion. End with a short reflection or exit question.

## Dataset preparation plan

1. Freeze exact UniProt reference proteomes and source details for the three strains.
2. Inventory headers and create an explicit identifier mapping.
3. Import the available FungalRV, SignalP, and PredGPI files without collapsing raw fields.
4. Resolve curated positive and negative IDs against the proteomes and document every mismatch.
5. Calculate length and S/T features for every protein.
6. Document screen thresholds and derive a two-of-three eligibility list.
7. Test XSTREAM and TANGO on a small representative batch before any whole-proteome run.
8. Run optional advanced tools only where feasible, preserving raw outputs and parameters.
9. Produce separate instructor, student, and unlabeled *C. auris* candidate tables with a data dictionary.
10. Freeze the exact files used during the workshop and test all notebooks without live services.

## Notebook set

Prepare the complete instructor handout as two self-contained notebooks:

1. `notebooks/morning/00_instructor_complete.ipynb`: notebook orientation; adhesin background; ALS1/PHO84 comparison; guided SignalP and NetGPI submissions; Python refresher; whole-protein S/T frequency; sliding windows; and a supplied dataframe/plotting bridge.
2. `notebooks/afternoon/00_instructor_complete.ipynb`: recap and independent setup; biological rules and decision trees; one fixed SignalP/PredGPI tree; the all-negative baseline; confusion matrix, precision, recall, and F1; addition of length and S/T features; optional TANGO/XSTREAM comparison; *C. auris* candidate interpretation; and final synthesis.

Each notebook serves as both activity guide and durable handout. Background, instructions, settings, interpretation questions, definitions, and recovery steps must be understandable without relying on the instructor's spoken explanation. Each half must run independently from a clean Colab runtime and must not rely on notebook state from the other half.

Student versions will be derived from the complete instructor notebooks after the instructor workflow is verified. Provide data-loading, BioPython/Pandas, plotting, splitting/cross-validation, and scikit-learn syntax. Students should write or complete the biologically meaningful sequence functions and interpretation answers.

## Decisions still required

- Storage and distribution policy for the frozen raw proteomes (ordinary Git,
  Git LFS, or separately distributed workshop inputs).
- Source and curation criteria for the negative set.
- Approved FungalRV pass rule.
- Which SignalP value/call defines a pass and how version/model settings are represented.
- Confirmation that the current GPI field is PredGPI, including version and parameters.
- TANGO scientific parameters and the summary statistic to teach.
- XSTREAM parameters and the repeat statistic to teach.
- Whether the expanded-feature model will use only eligible proteins or whether advanced features will be calculated for all labeled proteins.
- Whether the expanded tree should retain SignalP and PredGPI alongside sequence-derived features or compare a sequence-only tree with the toy localization tree.

Until these are resolved, Codex should preserve raw information, expose the uncertainty, and avoid silently choosing defaults.
