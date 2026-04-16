# data/leaders/

One YAML file per leader. Each file is a complete profile.

**Total entries at v1.0:** 115

## File structure

Each file is named `<slug>.yaml` where `slug` matches the leader's `id` field and is a URL-safe lowercase version of their name.

Examples:
- `jennifer-doudna.yaml`
- `fei-fei-li.yaml`
- `anima-anandkumar.yaml`
- `ritu-karidhal-srivastava.yaml`

## Schema

Every file conforms to [`../schema/leader.schema.json`](../schema/leader.schema.json). The required fields are:

- `id` — the slug, must match filename
- `name` — full name
- `origin` — country of birth (and optionally country of work, migration path)
- `current_roles` — at least one current role
- `domains` — primary domain + optional sub-domains
- `tier` — integer 1-5
- `tier_justification` — why this tier (must cite METHODOLOGY criteria)
- `summary` — narrative 80-800 character summary
- `links` — at minimum, a `primary` URL
- `verification` — status + last reviewed date

Optional but encouraged:
- `education`, `previous_roles`, `awards`, `ventures`, `key_works`,
  `relationships`, `metrics`, `tags`

## Editing

Edit any file, validate, commit.

```bash
# Edit a file
vi data/leaders/jennifer-doudna.yaml

# Validate your changes
python scripts/validate_data.py

# If validation passes, commit
git add data/leaders/jennifer-doudna.yaml
git commit -m "verify: Jennifer Doudna — add sources for every claim"
```

CI will re-validate on the PR.

## Tier distribution

As of v1.0:

| Tier | Label                            | Count |
|------|----------------------------------|-------|
| 1    | Nobel Laureates and equivalent   | 7     |
| 2    | Foundational Contributors        | 9     |
| 3    | Top Tier Institutional Leaders   | 19    |
| 4    | Major Leaders                    | 35    |
| 5    | Rising Stars                     | 45    |

## Verification status at v1.0

| Status                | Count |
|-----------------------|-------|
| `verified`            | 0     |
| `partially_verified`  | 108   |
| `unverified`          | 7     |

All 7 Tier 1 entries are marked `unverified` at launch and are the first priority for the verification pass. See [`../../CONTRIBUTING.md`](../../CONTRIBUTING.md#how-to-verify-an-entry).
