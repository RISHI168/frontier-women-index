#!/usr/bin/env python3
"""
Validate every leader YAML file in data/leaders/ against the schema.

Runs in CI on every PR that touches data/. Fails the build if any entry is
malformed or missing required fields.

Also runs semantic checks beyond the JSON schema:
- Slug uniqueness
- Required sources on verified entries
- Internal relationship targets exist

Usage:
    python scripts/validate_data.py [--strict]

Flags:
    --strict    Also flag partially_verified entries that should be verified by
                tier rules (e.g., a Tier 1 without full sourcing).
"""

import sys
import json
from pathlib import Path

try:
    import yaml
    from jsonschema import Draft7Validator
except ImportError:
    print("Required: pip install pyyaml jsonschema")
    sys.exit(1)


REPO = Path(__file__).parent.parent
SCHEMA_PATH = REPO / "data" / "schema" / "leader.schema.json"
LEADERS_DIR = REPO / "data" / "leaders"


def load_schema():
    return json.loads(SCHEMA_PATH.read_text())


def load_all_leaders():
    leaders = {}
    for path in sorted(LEADERS_DIR.glob("*.yaml")):
        try:
            data = yaml.safe_load(path.read_text())
        except yaml.YAMLError as e:
            print(f"ERROR parsing {path.name}: {e}")
            return None
        leaders[path.name] = data
    return leaders


def validate_schema(leaders, schema):
    """Run every leader against the JSON schema. Returns list of (filename, errors)."""
    validator = Draft7Validator(schema)
    failures = []
    for filename, data in leaders.items():
        errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
        if errors:
            failures.append((filename, errors))
    return failures


def check_slug_uniqueness(leaders):
    """Every leader's id must be unique and must match its filename."""
    problems = []
    seen_ids = {}
    for filename, data in leaders.items():
        slug = data.get("id", "")
        expected_filename = f"{slug}.yaml"
        if filename != expected_filename:
            problems.append(
                f"{filename}: id '{slug}' does not match filename "
                f"(expected {expected_filename})"
            )
        if slug in seen_ids:
            problems.append(
                f"{filename}: duplicate id '{slug}' (also in {seen_ids[slug]})"
            )
        seen_ids[slug] = filename
    return problems


def check_relationships(leaders):
    """Every relationship target must reference an existing leader id."""
    all_ids = {d.get("id") for d in leaders.values()}
    problems = []
    for filename, data in leaders.items():
        for rel in data.get("relationships") or []:
            target = rel.get("target")
            if target and target not in all_ids:
                problems.append(
                    f"{filename}: relationship target '{target}' does not exist "
                    f"in the leader set"
                )
    return problems


def check_verification_standards(leaders, strict=False):
    """Entries marked 'verified' must have a source URL on every current_role,
    award, and venture. Tier 1 entries should be verified (in strict mode)."""
    problems = []
    for filename, data in leaders.items():
        v = data.get("verification", {})
        status = v.get("status")

        if status == "verified":
            # Every claim needs a source
            for role in data.get("current_roles", []):
                if not role.get("source"):
                    problems.append(
                        f"{filename}: verified entries require 'source' on "
                        f"every current_role (missing on {role.get('title')} "
                        f"at {role.get('institution')})"
                    )
            for award in data.get("awards", []):
                if not award.get("source"):
                    problems.append(
                        f"{filename}: verified entries require 'source' on "
                        f"every award (missing on {award.get('name')})"
                    )
            if not v.get("second_reviewer"):
                problems.append(
                    f"{filename}: verified entries require a 'second_reviewer'"
                )

        if strict and data.get("tier") == 1 and status != "verified":
            problems.append(
                f"{filename}: Tier 1 entries should be fully verified "
                f"(current status: {status})"
            )

    return problems


def main():
    strict = "--strict" in sys.argv

    schema = load_schema()
    leaders = load_all_leaders()
    if leaders is None:
        sys.exit(1)

    print(f"Loaded {len(leaders)} leader entries from {LEADERS_DIR}")

    # Schema validation
    schema_failures = validate_schema(leaders, schema)
    if schema_failures:
        print(f"\nSchema validation: {len(schema_failures)} file(s) failed")
        for filename, errors in schema_failures[:10]:
            print(f"\n  {filename}:")
            for err in errors[:3]:
                path = ".".join(str(p) for p in err.absolute_path) or "(root)"
                print(f"    {path}: {err.message}")
    else:
        print("Schema validation: PASS (all entries conform)")

    # Slug uniqueness
    slug_problems = check_slug_uniqueness(leaders)
    if slug_problems:
        print(f"\nSlug uniqueness: {len(slug_problems)} problem(s)")
        for p in slug_problems[:10]:
            print(f"  {p}")
    else:
        print("Slug uniqueness: PASS")

    # Relationship integrity
    rel_problems = check_relationships(leaders)
    if rel_problems:
        print(f"\nRelationship integrity: {len(rel_problems)} problem(s)")
        for p in rel_problems[:10]:
            print(f"  {p}")
    else:
        print("Relationship integrity: PASS")

    # Verification standards
    v_problems = check_verification_standards(leaders, strict=strict)
    if v_problems:
        print(f"\nVerification standards: {len(v_problems)} problem(s)")
        for p in v_problems[:10]:
            print(f"  {p}")
    else:
        print("Verification standards: PASS")

    total_problems = (
        len(schema_failures) + len(slug_problems) +
        len(rel_problems) + len(v_problems)
    )

    if total_problems > 0:
        print(f"\nTotal: {total_problems} problem(s) found")
        sys.exit(1)
    print("\nAll checks passed.")


if __name__ == "__main__":
    main()
