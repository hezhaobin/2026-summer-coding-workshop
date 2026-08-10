# Plan for `00_instructor_complete`

Status: morning notebooks minimally implemented and verified, 2026-08-10;
afternoon notebook remains planned and is outside the current implementation scope

The complete instructor handout is split into two self-contained Colab notebooks:

- `notebooks/morning/00_instructor_complete.ipynb`
- `notebooks/afternoon/00_instructor_complete.ipynb`

The two-file design provides a natural lunch boundary, limits accidental notebook-state problems, and lets students reopen only the half they need. The afternoon notebook repeats its setup and the minimum context needed to stand alone.

## Design principles

Each notebook is both an activity guide and a durable handout. Do not rely on spoken instructions for essential content.

Every major section should contain:

1. a short biological or computational purpose;
2. the expected time;
3. background and definitions;
4. numbered student actions;
5. a prediction or interpretation question before revealing results;
6. a checkpoint or small automated test where code is written;
7. a concise takeaway;
8. an “If you get stuck” note when appropriate.

Use short Markdown sections, visible headings, and descriptive code-cell names. Put one main idea in each code cell. Label cells as **Read**, **Run**, **Your turn**, **Discuss**, or **Instructor note**.

The instructor notebook contains complete code, expected outputs, and teaching notes. The later student version will retain prompts, starter code, non-solution hints, and behavior-based tests while removing answer code.

## Verified external resources

- SignalP 6.0: <https://services.healthtech.dtu.dk/services/SignalP-6.0/>
- NetGPI 1.1: <https://services.healthtech.dtu.dk/services/NetGPI-1.1/>
- ALS1 UniProt entry: <https://www.uniprot.org/uniprotkb/Q5A8T4/entry>
- PHO84 UniProt entry: <https://www.uniprot.org/uniprotkb/A0A1D8PF54/entry>

Sequence identities verified through UniProt REST on 2026-08-09:

| Example | UniProt accession | Length | Teaching role |
| --- | --- | ---: | --- |
| *C. albicans* ALS1 | `Q5A8T4` | 1,260 aa | Known adhesin with an N-terminal secretion signal, extensive S/T-rich regions, and a C-terminal GPI-anchor signal |
| *C. albicans* PHO84 | `A0A1D8PF54` | 545 aa | Multi-pass phosphate transporter used as a contrasting non-adhesin membrane protein |

The current UniProt PHO84 sequence contains one `X` at residue 7. Retain and explain it as an unknown amino acid. Both SignalP 6.0 and NetGPI accept `X` in submitted sequences.

The completed morning notebook must embed both full sequences as literal FASTA text. Do not download them during the workshop. The FASTA headers should include the accession, gene, organism, and teaching label.

## Morning notebook: 9:30 a.m.–12:30 p.m.

### 1. Welcome, Colab orientation, and learning goals — 9:30–9:40

- State the biological question and the sequence-to-candidate storyline.
- Explain Markdown cells, code cells, the run button, execution order, and how to restart the runtime.
- Ask students to save their own Drive copy.
- Include a harmless “Run me” cell and its expected output.

### 2. What is a fungal adhesin? — 9:40–10:00

- Explain adhesion, cell-surface localization, and why adhesins matter.
- Introduce the common architecture: signal peptide, N-terminal adhesive domain, S/T-rich stalk, tandem repeats, and C-terminal GPI-anchor signal.
- Explain that these are useful signals rather than universal rules.
- End with a prediction prompt: what sequence evidence would students look for?

### 3. Examine ALS1 and PHO84 with SignalP and NetGPI — 10:00–10:30

#### Embedded examples

- Show a short annotation card for each protein.
- Provide each complete FASTA sequence in a separate copyable block.
- Ask students to predict which protein is secreted and which might be GPI anchored before using a server.

#### SignalP activity

Link directly to SignalP 6.0 and provide these settings:

- paste the two FASTA records;
- choose **Eukarya**;
- choose **Long/standard output** so students can inspect the graphical result;
- use **Fast** mode for the workshop;
- submit and record the predicted class, signal-peptide probability, and cleavage site if reported.

Interpretation prompts:

- Which sequence has a cleavable N-terminal signal peptide?
- What does “Other” mean in this output?
- How is a signal peptide different from one of PHO84's transmembrane helices?
- Does a signal peptide prove that a protein is an adhesin?

#### NetGPI activity

Explain before submission that NetGPI expects proteins designated for the secretory pathway and relies on prior signal-peptide evidence. It examines at most the final 100 residues.

- Submit ALS1 using long output for an interpretable graph.
- Record the GPI-anchor call, the predicted omega site if present, and the role of the sentinel `*`.
- Use PHO84 as a reasoning question: based on SignalP and its transporter architecture, should its NetGPI output be treated as meaningful evidence? The default activity should not imply that every protein should be passed blindly from one predictor to the next.

Interpretation prompts:

- What does a positive GPI-anchor prediction imply biologically?
- Why is the N-terminal SignalP result relevant before interpreting NetGPI?
- Do SignalP plus NetGPI distinguish an adhesin from every other cell-wall protein?

#### Live-service backup

Include instructor-captured result summaries or screenshots generated shortly before the workshop. If either service is unavailable or slow, students interpret the saved outputs instead. Precomputed project tables remain the authoritative data for later exercises.

### 4. Python refresher and whole-protein S/T frequency — 10:30–11:30

- Review strings, variables, `len`, `.count`, simple functions, return values, and readable loops.
- Start with a tiny manually checkable protein string.
- Students predict length and S/T count before running code.
- Build and test `st_frequency(sequence)`.
- Apply the function to ALS1 and PHO84.
- Add a zero-length guard only if it can be explained simply; do not turn the exercise into defensive-programming instruction.
- Compare results and connect composition back to adhesin architecture.

### 5. Break — 11:30–11:45

Place a clear stopping banner and the next restart point in Markdown.

### 6. Sliding-window S/T frequency — 11:45–12:15

- Motivate why a local S/T-rich region can be hidden by a whole-protein average.
- Develop the algorithm in pseudocode.
- Visualize the first two or three overlapping windows before generalizing.
- Complete a scaffolded `max_st_frequency_window(sequence, window_size=50)` function.
- Define the short-sequence behavior explicitly and simply.
- Test with a tiny sequence before applying to ALS1 and PHO84.

### 7. From two proteins to a table — 12:15–12:30

- Use provided code to create or load a small dataframe.
- Demonstrate applying student-written functions across protein rows.
- Run a supplied plot comparing known groups.
- Ask students to state one observed pattern and one reason it is not a perfect rule.
- End with a morning summary and a clean handoff to the afternoon question: can a decision tree combine evidence?

## Afternoon notebook: 1:15–4:30 p.m.

### 1. Independent setup and morning recap — 1:15–1:20

- Repeat imports, fixed random seed, data loading, and file checks.
- Recap SignalP, PredGPI, length, whole S/T frequency, and local S/T frequency.
- Do not require the morning runtime or its variables.

### 2. From biological rules to a decision tree — 1:20–1:35

- Begin with a human-readable two-feature rule.
- Define features, labels, branches, leaves, predictions, training examples, and overfitting.
- Use one small diagram or manually traceable table.

### 3. Guided toy-tree demonstration — 1:35–1:55

- Use supplied code to fit one shallow tree with SignalP score and PredGPI binary call.
- Display the tree with readable feature and class names.
- Trace ALS1 or another known example through its branches.
- Keep FungalRV out of the model and reveal it later only for comparison.

### 4. Everyone runs and interprets the same model — 1:55–2:20

- Show class counts and the all-negative baseline.
- Provide the confusion matrix and define precision, recall, and F1 in biological language.
- Students identify one correct prediction and one error.
- Students explain one tree rule in a complete sentence.
- Do not tune models or compare algorithms.

### 5. Break — 2:20–2:35

Use a visible stopping banner.

### 6. Added-feature challenge — 2:35–3:20

- Add protein length, whole-protein S/T frequency, and maximum local S/T frequency to a common prepared table.
- Ask students to predict which feature might change the tree before fitting it.
- Fit one common expanded shallow tree using supplied code.
- Compare errors and biological interpretation with the toy tree.
- Add TANGO and XSTREAM summaries only if valid data exist for enough eligible positives and negatives; otherwise omit them without treating the activity as incomplete.
- State the selective-computation leakage warning in plain language.

### 7. *Candida auris* candidate interpretation — 3:20–4:00

- Apply one provided common model or rule to a prepared candidate table.
- Examine three to five preselected candidates.
- For each candidate, connect its score to SignalP, PredGPI, length, S/T features, and optional advanced features.
- Reveal the withheld FungalRV score for comparison.
- Ask what alternative cell-wall role could produce a false positive and what experiment could test adhesion.

### 8. Synthesis and exit reflection — 4:00–4:30

- Revisit the sequence-to-candidate storyline.
- Discuss class imbalance, homologous-family overlap, selective-feature leakage, prediction versus explanation, and the need for experimental validation.
- Include a short individual exit response: one coding idea, one biological conclusion, and one limitation.
- Provide links to definitions and the two server pages for later reference.

## GitHub-to-Colab distribution

For a public GitHub repository, student access is straightforward:

1. Add an **Open in Colab** badge to each student notebook and the notebook README.
2. Use a URL of the form `https://colab.research.google.com/github/OWNER/REPOSITORY/blob/main/PATH/NOTEBOOK.ipynb`.
3. Students click the badge, sign in to Google if needed, and choose **File → Save a copy in Drive** before editing.
4. Provide the fallback path: **Colab → File → Open notebook → GitHub**, then search for the repository.
5. Keep a downloadable `.ipynb` backup and a static PDF only if accessibility or network planning requires it; the notebook remains the primary handout.

After the GitHub remote is configured, test every badge in a signed-out or private browser window and verify that the public notebook opens without repository credentials.

## Jupytext decision

Do not use Jupytext for the initial build.

Jupytext can make notebook diffs and text-editor changes easier by pairing `.ipynb` files with Markdown or percent-format Python files. For this project, however, there are only two planned instructor masters and they are narrative-heavy handouts. Maintaining paired files introduces another synchronization rule and another way for instructor and student copies to drift.

Use `.ipynb` as the single source of truth. Keep reusable scientific functions in ordinary Python modules under `script/`, and verify notebook execution directly. Reconsider Jupytext only if real maintenance problems appear, such as unreadable reviews, repeated merge conflicts, or many closely related notebook variants.

## Build and verification checklist

- Freeze the exact ALS1 and PHO84 FASTA text and source details used in the notebook.
- Capture current SignalP and NetGPI outputs shortly before the workshop.
- Confirm whether screenshots from the services may be redistributed; otherwise create an instructor-authored summary table.
- Create the morning instructor notebook and test its timing before deriving a student version.
- Create the afternoon instructor notebook with fully independent setup.
- Restart a clean Colab runtime and run each notebook top to bottom.
- Test the public GitHub-to-Colab links and **Save a copy in Drive** workflow with a non-instructor account.
- Verify that student copies contain no answer code or answer-revealing stored output.
- Keep live web submissions optional by providing saved results.
