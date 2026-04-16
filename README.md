# Frontier Women Index

A rigorously sourced, openly maintained index of women building the frontier of science and technology.

**Current scope:** 115 leaders across AI, BioIntelligence, Robotics, Quantum Computing, Space, and adjacent frontier STEM fields. 20 Indian and Indian-origin, 95 global. 7 Nobel laureates, 3 Kavli Prize winners, 6+ MacArthur Fellows.

**What makes this different from a list:**

- Every claim is either sourced with a URL or explicitly marked as unverified
- Tier assignments follow a [published methodology](./METHODOLOGY.md), not vibes
- Citation counts carry snapshot dates — the index tracks movement over time
- Every entry is a YAML file that machines and humans can both read
- Corrections are logged publicly in [`CORRECTIONS.md`](./CORRECTIONS.md)
- The data is free for anyone to use under CC-BY-SA 4.0

## Who this is for

**Journalists and researchers:** Every claim links to a primary source. Cite us, fact-check us, or build on our data. Download the full dataset as CSV or JSON from [`/data`](./data).

**Investors and founders scouting talent:** The [Signals dashboard](https://frontierwomenindex.org/signals) tracks citation movers, funding rounds, and role changes week-over-week.

**Students and aspiring women in STEM:** Each leader has an individual profile page showing their training pathway, key works, and current institutional affiliations.

## How to use this repo

```
data/leaders/             ← one YAML file per leader (the source of truth)
data/schema/              ← JSON schemas validating every entry
signals/                  ← time-series data on citations, funding, awards
research/                 ← quarterly deep-dive reports
graph/                    ← relationship data (advisor, co-author, spinout)
site/                     ← the public-facing Next.js application
scripts/                  ← automation, validation, signal collection
notebooks/                ← reproducible analysis
```

## How to contribute

- **Nominate a leader:** Open an issue using the [Nominate template](./.github/ISSUE_TEMPLATE/nominate-leader.md). Provide sourced evidence for each claim.
- **Submit a correction:** Use the [Correction template](./.github/ISSUE_TEMPLATE/correction.md). Corrections are merged within 7 days and logged in `CORRECTIONS.md`.
- **Help verify an unverified entry:** Entries marked `verification_status: unverified` need sourcing. See [`CONTRIBUTING.md`](./CONTRIBUTING.md).
- **Add a signal source:** Know of a data source that would make the index more accurate? Open a discussion.

## Methodology in one paragraph

Leaders are ranked into five tiers. Tier 1 is reserved for Nobel laureates and holders of prizes of comparable scientific weight. Tier 2 is for foundational contributions recognized by a MacArthur Fellowship, Turing Award, or equivalent, or for having authored one of the most-cited papers of the decade in their field. Tier 3 is for major institutional leaders and holders of high-impact awards (Kavli, Breakthrough, Gruber). Tier 4 is for established leaders in their field, typically with 5+ years of institutional or founding leadership. Tier 5 is for rising stars — researchers under 40 with strong early-career signals, or founders of companies with meaningful traction. Full details, including how we handle conflicts of interest and disputed entries, are in [`METHODOLOGY.md`](./METHODOLOGY.md).

## Project status

**Version 1.0 — April 2026.** Initial launch with 115 leaders. Verification status: 15 fully verified (all Tier 1 and Kavli winners), 100 partially verified.

**Roadmap:**
- Q2 2026: Verify remaining entries. Ship Research Graph view.
- Q3 2026: Publish first quarterly research report: *"Where did the 20 Indian frontier women train?"*
- Q4 2026: Open the nomination process to external contributors. Target 200+ leaders.

## Governance

The Frontier Women Index is an independent research project. The editorial direction, methodology, and inclusion decisions are made by the project maintainers and are not subject to sponsor approval.

**Founding sponsor:** [TechFondue](https://techfondue.com) — providing catalytic support for the index's development and maintenance. TechFondue does not have editorial control.

**Maintainers:** Listed in [`MAINTAINERS.md`](./MAINTAINERS.md).

## License

- **Data** (`data/`, `signals/`, `graph/`, `research/`): [Creative Commons Attribution-ShareAlike 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
- **Code** (`scripts/`, `site/`, `notebooks/`): [MIT License](./LICENSE)

Attribution: *Frontier Women Index, frontierwomenindex.org*

## Citation

If you use this data in academic work, please cite:

```bibtex
@misc{frontierwomenindex2026,
  title = {Frontier Women Index: A curated dataset of women leaders in frontier science and technology},
  author = {Frontier Women Index Contributors},
  year = {2026},
  url = {https://frontierwomenindex.org},
  note = {Version 1.0}
}
```

---

*The list was the seed. The infrastructure around it is what makes the seed grow.*
