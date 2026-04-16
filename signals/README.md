# signals/

Time-series data on leaders' trajectories. This is the "Living Index" half of the project.

## What's in this folder

### `scholar_deltas.csv`

A weekly snapshot of Google Scholar / Semantic Scholar citation counts and h-indices for each leader. Appended to (not overwritten) each week by the `weekly-signals.yml` GitHub Action via `scripts/collect_signals.py`.

Columns:
- `date` — the date the snapshot was taken (ISO YYYY-MM-DD)
- `leader_id` — slug matching the YAML file
- `name` — leader's full name
- `citations` — total citation count at snapshot time
- `h_index` — current h-index
- `source_url` — Semantic Scholar profile URL used for the lookup
- `notes` — match quality (`ok`, `low_confidence`, `no_match`) or error description

The site's "Citation Movers" view at `/signals` reads this CSV and computes week-over-week deltas, showing which leaders have gained the most citations in any given quarter.

## What's coming

**Planned signal sources for v1.1 through v1.3:**

1. **ArXiv watch** — new papers posted by each leader, detected daily
2. **Funding events** — manually curated + AI-assisted tracking of company funding rounds
3. **Awards timeline** — systematic tracking of when new awards are announced
4. **Institutional changes** — role changes, new appointments, founder moves

Each new signal source will live as its own CSV or YAML file in this folder, documented here, and wired to the site dashboard.

## Why this matters

Citation counts and funding rounds are public information but are hard to aggregate. The value the Index adds is doing this aggregation consistently, transparently, and on a weekly cadence, so readers can see *movement* rather than just a static snapshot. Investors and journalists rely on this kind of temporal signal; it doesn't exist for women in frontier science in any single place. That gap is what this folder is here to fill.

## For contributors

If you spot an error in a signal (wrong Semantic Scholar match, missing author, anomalous delta), please open an issue using the [Signal Update template](../.github/ISSUE_TEMPLATE/signal-update.md). Signals are harder to correct than leader entries (they're time-series, not static), so we handle updates carefully.
