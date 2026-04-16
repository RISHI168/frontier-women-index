# Contributing to the Frontier Women Index

Thanks for being here. The Index is designed to be improved by the community while keeping the editorial bar high. This document explains how.

## What you can contribute

1. **Nominate a new leader** — someone you believe meets the [inclusion criteria](./METHODOLOGY.md#scope) but isn't in the Index yet.
2. **Verify an unverified entry** — the fastest way to make a real difference. See the list of entries marked `verification_status: unverified` or `partially_verified`.
3. **Submit a correction** — found a wrong citation, outdated role, or factual error? File a correction issue.
4. **Add a relationship** — know that Leader A was Leader B's PhD advisor, or that they co-founded a company? Help build the Research Graph.
5. **Propose a signal source** — know of a data source that would make the Index richer? Open a discussion.
6. **Write a research notebook** — have an analytical angle on the data? Contribute to `/notebooks/`.

## Before you contribute

Read [`METHODOLOGY.md`](./METHODOLOGY.md). It explains how tiers are assigned, what evidence counts, and how edge cases are handled. Contributions that don't follow the methodology will be asked to revise before merging — not rejected, just slowed down. Save everyone time by reading it first.

## How to nominate a leader

1. Open a new issue using the [Nominate a Leader template](./.github/ISSUE_TEMPLATE/nominate-leader.md).
2. Fill in every required field. At minimum, you must provide:
   - Full name and current primary role (with institutional URL)
   - Proposed tier (1-5) with justification citing specific METHODOLOGY criteria
   - At least 3 primary sources backing the major claims
   - Google Scholar or Semantic Scholar profile URL (or explicit note if unavailable)
3. A maintainer will respond within 7 days with one of: accept (and convert to a PR), request revisions, or decline with reasoning.
4. Accepted nominations become YAML files at `data/leaders/<slug>.yaml`.

### What doesn't get in

- Nominations based only on job titles ("Chief AI Officer at [company]")
- Nominations without primary sources for at least the tier-justifying claims
- Self-nominations without third-party evidence of claimed impact
- Nominations that duplicate an existing entry under an alternate spelling (search first)

## How to verify an entry

Verification upgrades an entry's `verification_status` from `unverified` or `partially_verified` to `verified`. It requires:

- A source URL on every `current_role`
- A source URL on every `award`
- A source URL on every `venture` (with `capital_raised_usd` sourced to a credible funding announcement, not a press release)
- Citation counts with `citations_source` set and `citations_snapshot_date` within the last 30 days
- At least one `second_reviewer` name in the `verification` block

**The workflow:**

1. Pick an entry marked `partially_verified` or `unverified` from `data/leaders/`.
2. Open a branch: `git checkout -b verify/<leader-slug>`.
3. Add sources to each claim. Prefer primary institutional sources. See [Sourcing standards](./METHODOLOGY.md#sourcing-standards).
4. Update `verification.status` to `verified`, set `verification.last_reviewed` to today's date, and add your name as `verification.reviewer`.
5. Open a PR with the title `verify: <Leader Name>`.
6. A maintainer will review as second reviewer. On approval, your name appears in the entry as `second_reviewer` and the PR is merged.

## How to submit a correction

Found something wrong? Two paths depending on severity.

**For factual errors** (wrong year, wrong institution, misspelled name, broken link): open a pull request directly. Update the YAML, update `CORRECTIONS.md` with a one-line entry (the script `scripts/log_correction.py` helps with format), and submit.

**For substantive disputes** (tier placement, inclusion, whether a claim is supported by evidence): open an issue first using the [Correction template](./.github/ISSUE_TEMPLATE/correction.md). These get discussed before any change is made.

All corrections, once merged, are logged in [`CORRECTIONS.md`](./CORRECTIONS.md) with date, nature, and resolution.

## How to add relationships

The `relationships` field in each leader's YAML powers the Research Graph. Valid relationship types:

- `advisor` / `advisee` — PhD or postdoctoral supervision
- `co-author` — co-authored a paper (include only for papers with 3 or fewer authors, or where the relationship is notable)
- `co-founder` — co-founded a company, lab, or institute
- `predecessor` / `successor` — held the same institutional role in sequence
- `collaborator` — sustained non-trivial collaboration (multiple papers, joint grants, shared lab space)

Every relationship must include a `source` URL. Example:

```yaml
relationships:
  - type: advisee
    target: chelsea-finn
    context: PhD supervision at Stanford, 2014-2018
    source: https://ai.stanford.edu/~cbfinn/
```

Relationships are symmetric: if you add Leader A as advisor to Leader B, also add Leader B as advisee to Leader A. The validation script will flag missing reciprocals.

## Code contributions

For changes to `scripts/`, `site/`, or `notebooks/`:

1. Open an issue describing the change before writing significant code, unless it's a trivial bug fix.
2. Follow the existing code style (Python: PEP 8 + type hints where reasonable; TypeScript: Prettier default).
3. Include tests where practical. For data migration or validation scripts, include a test fixture.
4. Run `python scripts/validate_data.py` locally before submitting.

## Review timeline

- **Nominations:** response within 7 days.
- **Corrections:** merged within 7 days, or a response explaining why longer.
- **Verification PRs:** reviewed within 14 days. These get priority because they directly improve quality.
- **Code PRs:** no SLA. Maintainers review as capacity allows.

## Getting credit

Contributors to the Index get credit in several ways:

- Your GitHub handle appears as `verification.reviewer` or `verification.second_reviewer` on every entry you verify.
- Your name is added to `CONTRIBUTORS.md` after your first merged PR.
- Substantial contributions (verifying 20+ entries, authoring a research report, shipping a significant feature) are acknowledged in the relevant quarterly report's credits section.

## Decorum

This is a project about women's contributions to science. We do not tolerate harassment, dismissiveness of the project's focus, or dismissiveness of any contributor's work. The [Code of Conduct](./CODE_OF_CONDUCT.md) applies to all interactions in issues, PRs, discussions, and any associated spaces.

## Questions

Open a GitHub Discussion. For sensitive matters (conflict of interest, safety concerns about a listed leader), email the maintainers directly — addresses in [`MAINTAINERS.md`](./MAINTAINERS.md).
