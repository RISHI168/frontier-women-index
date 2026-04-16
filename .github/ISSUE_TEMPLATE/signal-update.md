---
name: Signal Update
about: Report a new funding round, role change, award, or other significant event
title: "Signal: <Leader Name> — <event>"
labels: signal, needs-review
assignees: ""
---

## Event type

- [ ] Funding round (Series A/B/C, seed, grant, etc.)
- [ ] New role or institutional change (new professorship, new CEO/founder role, board appointment)
- [ ] Award or honor received
- [ ] Major publication (landmark paper, book, or body of work)
- [ ] Company milestone (IPO, acquisition, unicorn status, etc.)
- [ ] Other (please describe)

## Which leader

**Leader name:**
**Entry file:** `data/leaders/<slug>.yaml`

## Event details

**Date of event:**
**Brief description:**
**Primary source URL:**

For funding events:
- **Amount:** USD (numeric)
- **Round type:** (seed / Series A / etc.)
- **Lead investor (if public):**

For role changes:
- **New role:**
- **New institution:**
- **Previous role being replaced or added to:**

For awards:
- **Award name:**
- **Awarding organization:**
- **Year:**

## Why this matters

Briefly: how does this event change how we should think about this leader, their trajectory, or their field? (1-3 sentences. This may be referenced in signal summaries.)

## Suggested entry updates

List the specific YAML fields that should be updated. Example:
- Add to `awards[]`: `{name: "MacArthur Fellowship", year: 2026, source: "https://..."}`
- Update `current_roles[0].institution`: from "X" to "Y"
- Add to `ventures[]`: `{name: "New Company", type: "company", founded: 2026, capital_raised_usd: 50000000}`

## Have you already fixed this?

- [ ] Yes, I've opened a PR: `#____`
- [ ] No, maintainers should apply the update

---

## Conflict of interest

Do you have a personal or professional relationship with the subject?

**Relationship:** (or "none")
