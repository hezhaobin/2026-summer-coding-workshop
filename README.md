# Python in Biology Workshop: Morning

Student materials for the morning half of the fungal-adhesin Python workshop.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/hezhaobin/2026-summer-coding-workshop/blob/main/notebooks/morning/python-in-biology-morning.ipynb)

## Start here

1. Click **Open in Colab**.
2. In Colab, choose **File → Save a copy in Drive** before editing.
3. Run the notebook from top to bottom.
4. Read each prediction prompt before running the next cell.

The notebook contains the two example protein sequences needed for the first
coding exercises. Later, provided code loads frozen workshop files directly
from this repository; students do not need to query UniProt during class.

## Prediction-server backup

The SignalP and NetGPI activities normally use the live DTU servers. If either
service is unavailable, open the [saved demo results](docs/demo-predictor-results.md)
when instructed. The backup contains the result tables and plots for the same
ALS1 and PHO84 sequences embedded in the notebook.

## Frozen proteome files

The three workshop proteomes are stored under `input/raw/proteomes/`. The
morning notebook downloads the frozen *S. cerevisiae* S288C and *C. albicans*
SC5314 FASTA files, verifies their SHA-256 checksums, and reads them with
Biopython. It also downloads `input/processed/morning-known-adhesins.tsv`, an
answer-free table containing the 30 validated KN known-adhesin IDs, names, and
species.

If GitHub cannot be reached during class, use the instructor's backup copies and
upload these three files with Colab's **Files** panel before running the loading
cell:

- `UP000002311-uniprot-2026_02.fasta`
- `UP000000559-uniprot-2026_02.fasta`
- `morning-known-adhesins.tsv`

## If something goes wrong

- If cells were run out of order, choose **Runtime → Restart session**, then run
  from the top.
- If a prediction server is unavailable, use the linked saved demo results to
  complete the interpretation questions, then continue with the coding exercises.
- If a GitHub data download fails, upload the three instructor-provided files
  listed above and rerun the loading cell.
- If your edits are lost, reopen this repository and save a new Drive copy.
