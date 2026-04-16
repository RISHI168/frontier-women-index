# Methodology

This document explains how entries are selected, ranked, verified, and maintained in the Frontier Women Index. It is the editorial spine of the project.

## Scope

### What we include

**Fields covered.** Frontier intelligence and its substrate layers: AI/ML foundations and safety, BioIntelligence and AI-driven biology, robotics and embodied AI, quantum computing, space and aerospace, neuroscience (where it informs or is informed by AI), frontier materials science, and AI-adjacent enterprise infrastructure (AI chips, AI networking, AI data infrastructure).

**Who counts as a "leader."** A researcher, founder, or institutional leader whose individual body of work has made a measurable, attributable contribution to one of the covered fields. We prioritize:

- Authors of highly-cited foundational papers (citation counts verified via Google Scholar or Semantic Scholar)
- Founders of companies that have raised substantial capital or achieved significant market impact
- Directors of major research institutions
- Winners of top-tier scientific prizes (Nobel, Kavli, Breakthrough, MacArthur, Gruber, Turing, ACM A.M. Turing Award)
- Holders of named professorships at R1 research institutions, where accompanied by independent evidence of research impact

**Who does not count.** We do not include leaders purely on the basis of: corporate title alone (without underlying research or building contribution), social media following, speaking-circuit visibility, advocacy work unaccompanied by technical or institutional contribution, or presence in other "top women in tech" lists. The index is about frontier research and building contribution, not visibility.

### Geographic and origin framing

We tag origin separately from current work location. A researcher born and trained in India who now works in the US is tagged `origin: India`, `migration_path: [India, US]`, `india_connection: true`. This matters because the Index tracks where talent originates, not only where it ends up.

The 20-Indian / 95-global split is a framing choice, not a quota. Indian and Indian-origin leaders are over-indexed relative to their global share because one of the Index's research questions is the geographic distribution of frontier leadership. Other geographic breakdowns (e.g., European women, African women) are tracked in data but not currently surfaced as splits. Future editions may add them.

## The tier system

Tiers are the Index's central editorial construct. They are ordinal, not cardinal — a Tier 2 leader is not "twice as important" as a Tier 4 leader; they occupy different categories of contribution.

### Tier 1: Nobel Laureates and Equivalent

Reserved for holders of:

- Nobel Prize in Physics, Chemistry, or Physiology/Medicine
- Fields Medal (mathematics)
- Abel Prize (mathematics)
- ACM A.M. Turing Award (computer science)

Approximately 7-10 women per decade enter this tier across all covered fields. Current count: **7**.

### Tier 2: Foundational Contributors

Reserved for:

- Authors of papers that have fundamentally shifted a field, as measured by (a) citation count in the top 1% of the field, AND (b) recognized institutional validation (MacArthur Fellowship, named professorship at a top-10 department, or role as founding researcher of a category-defining lab)
- Founders of companies that have either (a) achieved unicorn valuations in frontier fields, OR (b) delivered breakthrough scientific products (first-in-class drugs, novel computing architectures, etc.)

Current count: **~10**.

### Tier 3: Major Institutional Leaders and High-Impact Researchers

Reserved for:

- Holders of the Kavli Prize, Breakthrough Prize, Gruber Prize, or similar second-tier scientific honors
- Directors of major research institutes or programs (MIT CSAIL, Broad Institute divisions, Max Planck units)
- C-suite leadership of companies with $10B+ market capitalization in AI/frontier fields
- Founders of companies with $500M+ raised in frontier sectors

Current count: **~20**.

### Tier 4: Major Leaders

Reserved for:

- Established researchers with sustained institutional leadership (5+ years at director level or equivalent)
- Named professors at R1 institutions with verified research impact
- Founders of companies with $50M-$500M raised
- Holders of top-tier national honors (Padma Bhushan, FRS, NAE membership)

Current count: **~35**.

### Tier 5: Rising Stars

Reserved for:

- Researchers typically under 40 with strong early-career signals (NSF CAREER Awards, Forbes 30 Under 30 in frontier categories, emerging body of work)
- Founders of pre-unicorn companies in frontier fields
- Individuals whose trajectory suggests probable Tier 4 or above within 5 years

Current count: **~40**.

## Tier assignment process

Every tier assignment is recorded in the leader's YAML file under `tier_justification`. This field must cite the specific credentials that place the leader in their tier. Example:

```yaml
tier: 2
tier_justification: >
  MacArthur Fellow 2013 (foundational institutional validation).
  Co-authored "Attention Is All You Need" (Vaswani et al., 2017),
  currently the 3rd most-cited ML paper of the decade.
  Both conditions for Tier 2 are met.
```

Tier assignments are reviewed quarterly. A leader may move up a tier when new honors are awarded; they are not moved down except in cases of documented misconduct that would fail the inclusion criteria retrospectively.

## Verification levels

Each leader carries a `verification_status` field. This is honest transparency about how thoroughly each entry has been fact-checked.

### `verified`

Every factual claim in the entry (role, institution, award, citation count, funding raised) has an accompanying URL in the `sources` field. The entry has been reviewed end-to-end by at least one maintainer and one external reviewer.

All Tier 1 entries must be fully verified before merging.

### `partially_verified`

Major claims are sourced, but secondary or narrative claims may rely on curator judgment. For example: an entry might cite the Nobel Prize announcement and the Google Scholar profile but not have a source for a specific quote about the researcher's motivation.

This is the default state for most entries at launch.

### `unverified`

The entry is a stub based on well-known public information but has not been systematically checked. These entries display a visible badge on the site and are flagged for community verification.

## Sourcing standards

Every sourced claim must link to one of the following, in order of preference:

1. **Primary institutional sources** (university faculty pages, institutional bios, company leadership pages)
2. **Nobel Foundation, Kavli Foundation, MacArthur Foundation, or similar award-granting body pages**
3. **Peer-reviewed publications** or **ArXiv preprints** with DOIs
4. **Major wire services and established publications** (Reuters, AP, Nature, Science, Bloomberg, FT, WSJ, NYT) for news claims
5. **Google Scholar or Semantic Scholar** for citation counts (with snapshot dates)
6. **Company SEC filings or verified funding announcements** for capital claims
7. **Wikipedia** — acceptable for well-established biographical facts but not for primary citation; prefer upstream sources where available

**Not acceptable as primary sources:** LinkedIn profiles (which can be edited by the subject), personal websites that do not credibly document the claims made, press releases without independent verification, other "top women" listicles.

## Handling disputes, misconduct, and sensitive situations

### Corrections

All substantive corrections are:
1. Filed as an issue using the correction template
2. Reviewed within 7 days
3. Implemented with a public diff in the relevant YAML file
4. Logged in [`CORRECTIONS.md`](./CORRECTIONS.md) with date, nature of correction, and resolution

### Removal requests

If a leader requests removal from the Index, we engage in good faith. We do not remove entries solely to suppress accurate public information about public figures in their professional capacity, but we do honor removal requests when:
- The leader's work is not substantively frontier-intelligence-related and their inclusion was an editorial error
- The individual is not a public figure in the scientific or technology community and their inclusion exposes them to undue attention
- Legal or safety considerations apply

All removal decisions are logged in `CORRECTIONS.md` with the stated reason (unless safety-sensitive).

### Misconduct allegations

If credible allegations of research misconduct, harassment, or other serious ethical violations are brought forward about a listed leader, we:
1. Add a time-stamped note to the leader's entry acknowledging the allegation
2. Do not remove the entry while allegations remain unresolved
3. Update the entry with the outcome when institutional findings are public
4. Reassess tier placement if findings conclusively undermine the contributions that justified the tier

We do not adjudicate misconduct ourselves. We track what credible institutions and courts have found.

## Conflicts of interest

Maintainers and founding sponsors may have professional relationships with listed leaders. All such relationships are disclosed in `MAINTAINERS.md`. No maintainer may be the sole reviewer for an entry about a leader they have a current professional or personal relationship with.

The founding sponsor (TechFondue) has no editorial control. If TechFondue's business interests ever come to overlap with a listed leader's company in a way that creates a conflict, this will be disclosed in the relevant entry.

## Update cadence

- **Weekly:** Automated citation snapshot via Semantic Scholar API; commits to `signals/scholar_deltas.csv`
- **Monthly:** Manual review of major news for funding events, new roles, new awards
- **Quarterly:** Full verification pass on a rotating 25% of entries; quarterly research report published
- **Annually:** Full methodology review; tier thresholds recalibrated if fields have shifted significantly

## Versioning

The Index follows semantic versioning:

- **Major version** (1.0 → 2.0): Methodology changes that affect tier definitions or scope
- **Minor version** (1.0 → 1.1): Additions or removals of >5% of entries; new data fields added to the schema
- **Patch version** (1.0 → 1.0.1): Corrections, additions, or updates to individual entries

Each release is tagged in Git and accompanied by a changelog entry.

## This document is a living standard

We will revise this methodology when we find its rules are producing wrong answers. All methodology revisions are logged in `CHANGELOG.md` and reflected in a version bump. The intent is that a reader five years from now can look at Version 1.0 of this methodology, understand exactly how the Version 1.0 data was produced, and trust that subsequent changes are documented.

---

*Last updated: April 2026. Maintained by the Frontier Women Index project.*
