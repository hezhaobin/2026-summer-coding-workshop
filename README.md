# Python in Biology Workshop: Morning

Student materials for the morning half of the fungal-adhesin Python workshop.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/hezhaobin/2026-summer-coding-workshop/blob/main/notebooks/morning/python-in-biology-morning.ipynb)

## Start here

1. Click **Open in Colab**.
2. In Colab, choose **File → Save a copy in Drive** before editing.
3. Run the notebook from top to bottom.
4. Read each prediction prompt before running the next cell.

The notebook contains the two example protein sequences needed for the core
coding exercises. No live protein download is required.

## Frozen proteome files

The three workshop proteomes are stored under `input/raw/proteomes/`. The
notebook's provided setup code downloads the required frozen file from this
repository into the Colab runtime, verifies its SHA-256 checksum, and then reads
it with Biopython.

If GitHub cannot be reached during class, download the required FASTA before the
workshop or use the instructor's backup copy. Upload it with Colab's **Files**
panel when prompted.

## If something goes wrong

- If cells were run out of order, choose **Runtime → Restart session**, then run
  from the top.
- If a prediction server is unavailable, continue with the coding exercises;
  the instructor will provide a saved result for interpretation.
- If a GitHub data download fails, upload the instructor-provided frozen FASTA
  through Colab's **Files** panel and rerun the loading cell.
- If your edits are lost, reopen this repository and save a new Drive copy.
