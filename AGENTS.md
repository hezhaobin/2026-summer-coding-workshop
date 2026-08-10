# Codex project instructions

## Project purpose

This repository supports a one-day, in-person Python-in-biology workshop for students who have completed an introductory CodeHS course using Tracy the Turtle. Build a reproducible fungal-adhesin data pipeline and beginner-friendly Google Colab materials.

The authoritative pedagogical specification is `docs/workshop_plan.md`. Preserve its scope and learning objectives. If a requested implementation conflicts with that document, explain the conflict before changing the design.

## Scientific scope

Work with these reference strains:

- *Saccharomyces cerevisiae* S288C
- *Candida albicans* SC5314
- *Candida auris* B8441

The project distinguishes three kinds of variables:

1. Curated outcome labels: adhesin positive, negative, or unlabeled.
2. Screening outputs: FungalRV score, SignalP score/call, and PredGPI binary call.
3. Sequence-derived teaching features: protein length, whole-protein S/T frequency, maximum sliding-window S/T frequency, and—if feasible—beta-aggregation and tandem-repeat features.

FungalRV is a comparison benchmark and screening input, never a predictor in the student decision tree. Keep raw predictor outputs separate from derived pass/fail calls. Do not invent FungalRV or SignalP thresholds: record approved thresholds and their sources in a configuration file before calculating a two-of-three screen.

PredGPI and NetGPI are not interchangeable. Preserve the tool name, version, parameters, raw output, and parsed field names for every result.

## Non-negotiable data rules

- Treat downloaded proteomes and third-party tool outputs as immutable raw data. Never edit them in place.
- Record source URL, query or proteome accession, strain, download timestamp, database release when available, file checksum, and script/tool version.
- Use frozen local files for the workshop. Live UniProt access may be demonstrated but must not be required during class.
- Retain original protein identifiers and descriptions. Create an explicit ID-mapping table rather than silently rewriting identifiers.
- Validate every curated positive and negative ID against the frozen proteomes. Report unmatched, duplicated, obsolete, and ambiguous IDs.
- Do not infer undocumented negative labels. The origin and curation rule for the negative set must be documented before it is used for model evaluation.
- Never treat an uncomputed feature as zero. Use a missing value plus a computation-status column.
- Keep student-facing data free of unnecessary hidden answers and columns that directly disclose the label.

## Selective feature computation and leakage guard

TANGO and XSTREAM may initially be run only for proteins passing at least two of the following three screens: FungalRV, SignalP, and PredGPI.

This creates structurally missing data. Therefore:

- retain `fungalrv_pass`, `signalp_pass`, `predgpi_pass`, `screen_pass_count`, and `advanced_features_computed` as explicit source-tracking fields;
- never fill missing TANGO or XSTREAM values with zero;
- never train a full-proteome model on selectively computed TANGO/XSTREAM values, because computation status would reveal the upstream screen;
- use beta-aggregation or tandem-repeat features only in an analysis restricted to the same eligible two-of-three subset, unless those features are later computed for every labeled protein;
- report the eligible sample size and class counts before fitting any restricted model.

If the restricted labeled set is too small or contains only one class, stop and report that the expanded-feature challenge is not statistically usable. Keep the base exercise with length and S/T features.

## Repository organization

Use the following canonical directories. Do not create a new top-level directory when one of these already fits:

- `input/raw/`: frozen proteomes, curated label lists, and untouched third-party outputs. Organize them under `proteomes/`, `labels/`, and `predictors/` as appropriate.
- `input/interim/`: normalized FASTA files, ID maps, eligibility lists, and parser intermediates.
- `input/processed/`: validated, reusable analysis-ready and student-facing tables consumed by notebooks or scripts.
- `script/`: small command-line programs for download, validation, feature calculation, parsing, and table assembly.
- `analysis/`: instructor-only exploratory work, quality-control investigations, and model-development notes; do not distribute it as workshop material.
- `notebooks/`: paired, distributable student and instructor-solution Colab notebooks; do not use notebooks as the only implementation of the data pipeline.
- `output/`: regenerable figures, reports, candidate tables, and logs from a particular run; reusable tables belong in `input/processed/` instead.
- `config/`: species metadata, tool parameters, and approved screening thresholds.
- `tests/`: unit tests and small fixtures that do not duplicate full proteomes.
- `docs/`: workshop plan, data dictionary, source documentation, and instructor notes.

Each file must have one canonical home. Do not copy raw or processed datasets into `analysis/`, `notebooks/`, or `output/`; load them from `input/`. Do not maintain duplicate implementations in notebooks and scripts: reusable scientific logic belongs in `script/`, while notebooks import or demonstrate it at the appropriate student level.

Do not commit credentials, session cookies, licensed software, or restricted third-party data. Before adding large files, check repository policy and discuss whether Git LFS or documented download scripts are preferable.

## Pipeline expectations

Implement the work as small, restartable stages:

1. Resolve and document exact UniProt reference-proteome accessions for the three strains.
2. Download frozen FASTA files and write source details and checksums.
3. Normalize and inventory IDs without altering raw FASTA files.
4. Import FungalRV, SignalP, and PredGPI results while preserving raw values.
5. Validate curated labels and produce an ID-resolution report.
6. Calculate protein length and S/T features with tested Python functions.
7. Derive the two-of-three eligibility list only from documented pass definitions.
8. Pilot XSTREAM and TANGO on a tiny representative set, then scale only after outputs are validated.
9. Parse optional NetGPI results only from an allowed interface or user-supplied saved output.
10. Assemble instructor and student tables with a complete data dictionary.
11. Generate and execute the Colab notebooks from a clean runtime.

Each stage must be idempotent, log its inputs and parameters, fail clearly on schema changes, and avoid network access when a validated cached input exists.

All derived datasets, eligibility lists, figures, and model inputs must be reproducible from version-controlled scripts and documented configuration. Do not create a required workshop file through an undocumented manual spreadsheet or notebook edit.

## Right-sized engineering

This is an academic and pedagogical project, not a production software service. Write code for biologists with solid computational experience who may not be software developers.

- Prefer the simplest readable implementation that correctly handles the known workshop data and scientific workflow.
- Preserve the safeguards that matter scientifically: immutable raw data, recorded source details and parameters, deterministic results, explicit missing values, validated joins, and tests of core calculations.
- Handle realistic expected inputs and fail with a short, useful message when a required file, column, or parameter is missing. Do not spend substantial effort defending against unlikely hypothetical edge cases.
- Use small scripts and straightforward functions. A linear top-to-bottom script is acceptable when it is clearer than introducing extra abstractions.
- Add a function when it names a meaningful operation, is reused, or needs focused testing. Do not create classes, factories, registries, or generic frameworks merely to organize a short pipeline.
- Avoid elaborate command-line interfaces, configuration systems, logging frameworks, workflow engines, plugin architectures, concurrency, caching layers, automatic retry systems, and premature performance optimization unless a concrete project need justifies them.
- Keep dependencies minimal and familiar. Prefer Python's standard library and the scientific packages already needed for the workshop.
- Write comments and docstrings that explain biological meaning, assumptions, units, and non-obvious decisions. Do not narrate self-evident syntax.
- Test scientific correctness and the transformations most likely to fail. A few clear representative tests are preferable to exhaustive testing of implausible cases.
- Refactor after actual duplication or confusion appears, not in anticipation of a future generalized system.
- For a small one-time data check, prefer a short direct command and record the
  conclusion. Create a permanent script only when the check must be rerun, feeds
  a later pipeline stage, or produces a required reusable file. Do not add a
  dedicated test for straightforward file inspection with no reusable logic.

When safety, reproducibility, and simplicity pull in different directions, protect the raw data and scientific validity first, then choose the most readable solution. Briefly flag any case where a more complex design is genuinely necessary before implementing it.

## Git workflow

Prepare one commit after each meaningful, verified block of work. Keep unrelated
changes in separate commits and propose a concise descriptive commit message.
Before running every `git commit`, summarize the files to be included and the
verification performed, then ask the user for explicit approval. A general request
to implement or finish work is not commit approval. Do not push unless explicitly
asked.

## Naming conventions

Use terminology familiar to computational biology. Avoid `manifest` and
`provenance` in filenames, table names, and user-facing descriptions. Prefer
specific names such as `source-info`, `download-info`,
`sequence-header-info-extract`, `id-mapping`, or `data-source-details`.

Continue recording source URLs, versions, parameters, dates, and checksums where
scientifically required; only the terminology changes.

Prefer hyphens (`-`) rather than underscores (`_`) as word separators in
human-facing data and report filenames. Keep underscores when required by a tool,
language convention, external identifier, or unchanged source filename. For
example, preserve the official UniProt release identifier `2026_02` and use
underscores in importable Python module names.

## External tools and web services

Before installing or running XSTREAM, TANGO, SignalP, PredGPI, or NetGPI:

- verify the authoritative distribution source, license/terms, supported platform, citation, version, input limits, and expected output format;
- do not redistribute licensed executables or restricted models;
- pin and record all scientifically meaningful parameters;
- run a small positive/negative pilot and manually inspect parsed results;
- preserve raw stdout/output files and parser logs.

Do not automate a web form unless the service explicitly permits automation. If NetGPI has no supported API or batch interface, prepare validated FASTA batches and a parser for manually downloaded results, then ask the user to perform the submission. Never bypass rate limits, access controls, CAPTCHAs, or terms of service.

## Feature definitions

Put definitions and units in `docs/data_dictionary.md` and encode them once in tested functions.

- `protein_length`: number of amino-acid residues after normalization.
- `st_frequency`: `(count(S) + count(T)) / protein_length`.
- `max_st_frequency_window`: maximum S/T fraction over all windows of the configured length; default teaching window is 50 residues.

Explicitly document behavior for empty sequences, invalid residues, sequences shorter than the window, overlapping windows, and ties. Do not choose a TANGO or XSTREAM summary statistic until raw output and biological meaning have been reviewed.

## Notebook and teaching requirements

- The student notebook must run in Google Colab without local setup.
- Students write the biologically meaningful sequence functions. Provide FASTA loading, dataframe manipulation, plotting, train/test or cross-validation setup, and model-fitting syntax as scaffolded code.
- Include tiny manually checkable test sequences before real proteins.
- Every exercise must have a corresponding instructor solution and a small deterministic automated test. Tests should check behavior without revealing the implementation.
- Pair every student notebook with a fully executed instructor solution and expected outputs. Keep exercise identifiers and cell order synchronized between the two versions.
- Avoid live downloads, web-server submissions, package compilation, or long computations during the workshop.
- Provide a compact backup dataset and recovery instructions if Drive mounting or network access fails.
- Use plain language and short cells. Distinguish “code students write” from “provided infrastructure.”

### Beginner-facing code style

- Prefer readable, explicit code over compressed, clever, or advanced syntax.
- In student-written cells, use concepts already taught in the introductory course: variables, strings, `len`, `.count`, conditionals, loops, lists, and simple functions.
- Avoid list comprehensions in student-facing cells unless they have been introduced explicitly. Prefer an ordinary loop that students can trace.
- Avoid lambdas, nested comprehensions, dense method chaining, compact one-line conditionals, and unnecessary abstractions in code students must read or modify.
- Provided infrastructure may use Pandas, BioPython, scikit-learn, or a more advanced idiom when necessary, but place it in a clearly labeled setup cell and explain its purpose briefly. Do not require students to modify it.
- Keep one main idea per exercise or code cell. Use descriptive variable and function names tied to the biology.
- Mark optional extensions clearly so that completing them is not required to continue along the core notebook path.

### Notebook integrity and answer separation

- Do not rely on hidden notebook state. Put imports, configuration, data loading, and variable creation before their first use, and do not require cells to be run out of order.
- Every notebook must run from top to bottom after restarting a clean Colab runtime. Verify this using the actual student-distribution copy as well as the instructor solution.
- Use fixed random seeds for every stochastic operation, including sampling, splitting, cross-validation shuffling, and model fitting. Define seeds in one visible configuration cell.
- Do not expose answer code in student-facing cells, comments, stored outputs, collapsed sections, embedded HTML, or notebook metadata.
- Student notebooks may contain prompts, starter signatures, non-solution hints, and behavior-based tests. Complete implementations belong only in the instructor solution.
- Clear stale outputs from the distributed student notebook when they reveal answers or depend on an earlier run. Retain only intentional orientation or reference outputs.

## Machine-learning boundaries

Machine learning is a short interpretive capstone, not the main workshop theme.

- Demonstrate one shallow, reproducible decision tree.
- Have all students run the same toy model and interpret its branches, confusion matrix, precision, recall, and F1 score.
- Do not assign teams to tune competing models or search feature combinations.
- The common toy tree should use SignalP score and PredGPI binary call so students can see a small, biologically interpretable localization model.
- Keep FungalRV out of model inputs and compare it with the student model afterward.
- The expanded challenge adds protein length, whole-protein S/T frequency, and maximum local S/T frequency. It may also add TANGO and XSTREAM summaries only under the leakage rules above.
- Prefer a shallow interpretable tree over higher apparent performance.
- Use stratification for the shared evaluation. Report class counts and compare against the all-negative baseline.
- Avoid claims of generalization when homologous protein families or species overlap evaluation folds. Flag family/species leakage and use grouped evaluation if the data support it.
- Never present a team vote count or tree probability as calibrated biological confidence.

## Verification and handoff

For every material change:

- run relevant unit and integration tests;
- confirm that every exercise's automated test fails meaningfully for an incomplete or incorrect implementation and passes for the instructor solution;
- inspect row counts, class counts, missingness, duplicate IDs, value ranges, and joins;
- restart a clean Colab-compatible environment and execute both student and instructor notebooks top-to-bottom in their intended order;
- summarize files changed, commands/tests run, unresolved decisions, and source documentation added;
- do not commit or push unless explicitly asked.

Ask for user input when a scientific choice is not documented, especially screening thresholds, negative-set source and curation rules, TANGO parameters, XSTREAM summary definitions, and permission for manual web submission. Do not substitute a convenient assumption for those decisions.
