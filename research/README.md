# research/

Quarterly deep-dive reports that use the Index's data to answer specific research questions. This is the "Thesis Repository" half of the project.

## Why research reports

The 115-leader list is interesting. The patterns across the list are more interesting. Each quarterly report picks one question the data can answer rigorously, digs in, and publishes findings along with the reproducible notebook used to produce them.

Reports are written for journalists, researchers, and policy-makers who want defensible numbers on questions like:

- Where did the 20 Indian frontier women train?
- How does capital-per-woman-founder compare across the US, India, and Europe?
- Which institutions produced the most Tier 2+ leaders in the last decade?
- What is the typical career arc from first major publication to founding role?
- What share of foundational AI papers of the 2010s had a woman as first author?

## Structure of a report

Each report lives in its own folder: `research/<YYYY-QN>-<slug>/`.

Inside:
- `report.md` — the written analysis (typically 2000-4000 words)
- `report.pdf` — typeset version (generated from the markdown)
- `figures/` — charts and visualizations used in the report
- `notebook.ipynb` — the Jupyter notebook that produced the numbers, runnable against `data/`
- `data-snapshot.csv` — a frozen copy of the data used, for reproducibility

## Planned reports

| Quarter  | Title                                                                  | Status     |
|----------|------------------------------------------------------------------------|------------|
| Q2 2026  | Where did the 20 Indian frontier women train?                          | Planned    |
| Q3 2026  | Institutional lineage: which labs produced the most Tier 2+ leaders?   | Planned    |
| Q4 2026  | The capital geography of women-founded frontier companies              | Planned    |
| Q1 2027  | From first paper to founding role: career arcs across BioIntelligence  | Under consideration |

Each report is announced in `CHANGELOG.md` when published and shared via the project's Substack.

## Proposing a report

If you have a research question the Index's data could answer, open an issue tagged `research-proposal`. Tell us:

- The specific question
- Why it matters (who benefits from knowing the answer)
- What the Index's data would need for you to answer it
- Whether the needed data already exists, or what would need to be collected first

Maintainers pick roughly one research question per quarter. Contributor-proposed reports are credited with co-authorship.

## Reproducibility

Every report must be reproducible from the committed notebook and the data snapshot. This is a hard rule. A report that can't be reproduced is a press release, not research.
