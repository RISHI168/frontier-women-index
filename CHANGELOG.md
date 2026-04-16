# Changelog

All notable changes to the Frontier Women Index will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
as defined in [`METHODOLOGY.md`](./METHODOLOGY.md#versioning).

## [Unreleased]

## [1.0.0] — 2026-04-XX

Initial public release.

### Added
- 115 leader entries in `data/leaders/`, migrated from the original
  watchlist artifact
- JSON Schema at `data/schema/leader.schema.json` with full field validation
- Methodology document (`METHODOLOGY.md`) defining tiers, sourcing standards,
  conflict-of-interest handling, and governance
- Contributor documentation (`CONTRIBUTING.md`)
- Public corrections log (`CORRECTIONS.md`)
- Maintainers file with declared conflicts of interest (`MAINTAINERS.md`)
- Code of Conduct adapted from the Contributor Covenant
- Three GitHub issue templates: nominate a leader, submit a correction,
  signal update
- Data validation CI workflow (runs on every PR touching `data/`)
- Weekly citation snapshot workflow and `scripts/collect_signals.py`
  (first Living Index signal source)

### Verification status at launch
- 7 Tier 1 entries marked `unverified` — targeted for full sourcing in v1.0.1
- 108 entries marked `partially_verified` — carry primary source URLs but
  have not been end-to-end fact-checked

### Known limitations
- The site (`site/`) is not yet built. It will ship in v1.1.
- The Research Graph (`graph/`) is not yet populated. Relationships will be
  added progressively as entries are verified.
- No research reports in `research/` yet. First report planned for Q3 2026.
