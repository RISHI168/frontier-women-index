#!/usr/bin/env python3
"""
Migrate existing JSX leader data into YAML files matching the Frontier Women Index schema.

Usage:
    python scripts/migrate_jsx_to_yaml.py <path-to-jsx-file>

This is a one-time script to bootstrap the data/leaders/ directory from the
original React artifact. After running it, leader files can be edited
independently and the JSX is retired as a data source.
"""

import re
import sys
import json
from pathlib import Path
from datetime import date

try:
    import yaml
except ImportError:
    print("PyYAML required. Install with: pip install pyyaml")
    sys.exit(1)


# Map domain strings from JSX to schema enum values
DOMAIN_MAP = {
    "AI": "AI",
    "BioIntelligence": "BioIntelligence",
    "BioScience": "BioIntelligence",
    "Biotechnology": "BioIntelligence",
    "Biosensors": "BioIntelligence",
    "Robotics": "Robotics",
    "Quantum Computing": "Quantum Computing",
    "Space": "Space",
    "Aerospace": "Aerospace",
    "Astrophysics": "Space",
    "Neuroscience": "Neuroscience",
    "Enterprise Tech": "Enterprise Tech",
    "Semiconductors": "Semiconductors",
    "STEM": "STEM",
}


def slugify(name: str) -> str:
    """Convert a leader's name to a URL-safe id slug."""
    # Remove honorifics, periods
    s = re.sub(r"^(Dr\.?|Prof\.?)\s+", "", name, flags=re.IGNORECASE)
    s = s.lower()
    # Handle common accented characters
    replacements = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u",
                    "ñ": "n", "ć": "c", "ö": "o", "ü": "u", "ő": "o"}
    for k, v in replacements.items():
        s = s.replace(k, v)
    # Remove anything that isn't alphanumeric or whitespace
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    # Collapse whitespace to single hyphens
    s = re.sub(r"\s+", "-", s.strip())
    # Collapse multiple hyphens
    s = re.sub(r"-+", "-", s)
    return s


def parse_origin(o: str) -> dict:
    """Parse the origin string into structured country/migration data."""
    # Common patterns: "US", "India (Pune)", "China → US", "India → UK"
    origin = {}

    # Migration arrow pattern
    if "→" in o:
        parts = [p.strip() for p in o.split("→")]
        origin["country_of_birth"] = parts[0].split("(")[0].strip()
        origin["country_of_work"] = parts[-1].split("(")[0].strip()
        origin["migration_path"] = [p.split("(")[0].strip() for p in parts]
    elif "/" in o:
        # e.g., "Ghana/Canada → US" already handled above; "US/UK/India"
        parts = [p.strip() for p in o.split("/")]
        origin["country_of_birth"] = parts[0]
        if len(parts) > 1:
            origin["country_of_work"] = parts[-1]
            origin["migration_path"] = parts
    else:
        origin["country_of_birth"] = o.split("(")[0].strip()

    # Normalize common abbreviations
    norm = {"US": "United States", "UK": "United Kingdom"}
    for key in ["country_of_birth", "country_of_work"]:
        if key in origin and origin[key] in norm:
            origin[key] = norm[origin[key]]
    if "migration_path" in origin:
        origin["migration_path"] = [norm.get(p, p) for p in origin["migration_path"]]

    # Set india_connection flag
    india_markers = ["India", "Indian"]
    origin["india_connection"] = any(
        m in o for m in india_markers
    )

    return origin


def parse_title(t: str) -> list:
    """Parse the title field into current_roles array.

    Title format in JSX: "Professor, UC Berkeley · Founder, IGI"
    Multiple roles are separated by ' · '.
    """
    roles = []
    parts = [p.strip() for p in t.split("·")]
    for part in parts:
        if "," in part:
            title, institution = [x.strip() for x in part.split(",", 1)]
            roles.append({"title": title, "institution": institution})
        else:
            # Single word or un-comma-separated; treat whole thing as title
            roles.append({"title": part, "institution": "unspecified"})
    return roles


def parse_citations(ct_str):
    """Parse citation strings like '~161,822', '~60K', 'h-index ~198' into structured data.

    Accepts a string, a JSX-null literal 'null', or None. Returns a dict or None.
    """
    if not ct_str or ct_str == "null":
        return None
    # Strip outer quotes if present (e.g., '"~161,822"' from JSX extraction)
    ct_str = str(ct_str).strip().strip('"').strip("'")
    if not ct_str or ct_str == "null":
        return None

    metrics = {}

    # h-index pattern
    hi_match = re.search(r"h-?index\s*~?\s*(\d+)", ct_str, re.IGNORECASE)
    if hi_match:
        metrics["h_index"] = int(hi_match.group(1))

    # Citation count pattern: strip tilde and commas, look for digits
    clean = ct_str.replace("~", "").replace(",", "").strip()
    m = re.search(r"(\d+)\s*[Kk]?", clean)
    if m and "h-index" not in ct_str.lower():
        num = int(m.group(1))
        if "K" in clean or "k" in clean:
            num *= 1000
        metrics["citations_scholar"] = num

    return metrics if metrics else None


def extract_entries(jsx_text: str):
    """Extract all leader object literals from the JSX file.

    Looks for {n:"...",t:"...",...} blocks.
    Uses a state machine that handles nested quotes.
    """
    entries = []
    # Find each {n:"..."} block
    # JSX format has n:, t:, d:, e:, o:, b:, tg:, c:, ct:, url:, cat:, tier:
    # We use a carefully crafted regex that handles the fields in order
    pattern = re.compile(
        r'\{n:"((?:[^"\\]|\\.)*)",'
        r't:"((?:[^"\\]|\\.)*)",'
        r'd:"((?:[^"\\]|\\.)*)",'
        r'e:"((?:[^"\\]|\\.)*)",'
        r'o:"((?:[^"\\]|\\.)*)",'
        r'b:"((?:[^"\\]|\\.)*)",'
        r'tg:"((?:[^"\\]|\\.)*)",'
        r'c:"[^"]*",'
        r'(?:ct:(null|"[^"]*"),)?'
        r'url:"((?:[^"\\]|\\.)*)",'
        r'cat:"([^"]*)",'
        r'tier:(\d+)',
        re.DOTALL,
    )

    for m in pattern.finditer(jsx_text):
        n, t, d, e, o, b, tg, ct, url, cat, tier = m.groups()
        # Unescape quotes
        def unesc(s):
            return s.replace('\\"', '"').replace("\\'", "'") if s else s
        entries.append({
            "n": unesc(n), "t": unesc(t), "d": d, "e": e, "o": o,
            "b": unesc(b), "tg": tg, "ct": ct, "url": unesc(url),
            "cat": cat, "tier": int(tier),
        })
        # Also handle trailing entries where ct might come after url
        # (the original JSX has both orderings)

    # Fallback: entries with ct after url/cat (present in some tiers)
    alt = re.compile(
        r'\{n:"((?:[^"\\]|\\.)*)",'
        r't:"((?:[^"\\]|\\.)*)",'
        r'd:"((?:[^"\\]|\\.)*)",'
        r'e:"((?:[^"\\]|\\.)*)",'
        r'o:"((?:[^"\\]|\\.)*)",'
        r'b:"((?:[^"\\]|\\.)*)",'
        r'tg:"((?:[^"\\]|\\.)*)",'
        r'c:"[^"]*",'
        r'url:"((?:[^"\\]|\\.)*)",'
        r'cat:"([^"]*)",'
        r'tier:(\d+)'
        r',ct:(null|"[^"]*")',
        re.DOTALL,
    )

    existing_names = {e["n"] for e in entries}
    for m in alt.finditer(jsx_text):
        n, t, d, e, o, b, tg, url, cat, tier, ct = m.groups()
        if n not in existing_names:
            entries.append({
                "n": n, "t": t, "d": d, "e": e, "o": o,
                "b": b, "tg": tg, "ct": ct, "url": url,
                "cat": cat, "tier": int(tier),
            })

    return entries


def build_tier_justification(tier: int, tag: str, summary: str) -> str:
    """Build a placeholder tier_justification that references the tag and summary."""
    tier_labels = {
        1: "Tier 1 (Nobel Laureate / equivalent)",
        2: "Tier 2 (Foundational Contributor)",
        3: "Tier 3 (Top Tier Institutional Leader / High-Impact Researcher)",
        4: "Tier 4 (Major Leader)",
        5: "Tier 5 (Rising Star)",
    }
    return (
        f"{tier_labels[tier]}. Tagged as '{tag}'. "
        f"Placeholder justification — to be fleshed out with specific criteria citations "
        f"during verification pass. See METHODOLOGY.md for tier definitions."
    )


def entry_to_yaml(entry: dict) -> dict:
    """Convert a parsed JSX entry to a schema-compliant dict ready to serialize."""
    leader = {}
    leader["id"] = slugify(entry["n"])
    leader["name"] = entry["n"]
    leader["origin"] = parse_origin(entry["o"])
    leader["current_roles"] = parse_title(entry["t"])

    # Domains
    primary_d = entry["d"].split(" / ")[0].strip()
    secondary = [p.strip() for p in entry["d"].split(" / ")[1:]]
    leader["domains"] = {
        "primary": DOMAIN_MAP.get(primary_d, primary_d),
    }
    if secondary:
        leader["domains"]["secondary"] = secondary

    # Tier and justification
    leader["tier"] = entry["tier"]
    leader["tier_justification"] = build_tier_justification(
        entry["tier"], entry["tg"], entry["b"]
    )

    # Metrics
    metrics = parse_citations(entry["ct"])
    if metrics:
        metrics["citations_snapshot_date"] = str(date(2026, 1, 1))
        leader["metrics"] = metrics

    # Summary
    leader["summary"] = entry["b"]

    # Links
    leader["links"] = {"primary": entry["url"]}
    if "wikipedia.org" in entry["url"]:
        leader["links"]["wikipedia"] = entry["url"]

    # Verification — everyone starts as partially_verified except Tier 1
    # which we'll mark for priority full verification
    leader["verification"] = {
        "status": "partially_verified" if entry["tier"] > 1 else "unverified",
        "last_reviewed": str(date.today()),
        "reviewer": "migration-script",
        "notes": (
            "Migrated from original JSX artifact on " + str(date.today()) +
            ". Needs manual verification pass before status can be upgraded to 'verified'. "
            "Tier 1 entries are explicitly marked 'unverified' until they receive a "
            "full sourcing pass with every claim backed by a URL."
        ),
    }

    # Tags — derive from tag line + origin
    tags = []
    if leader["origin"].get("india_connection"):
        tags.append("india-connection")
    tag_lower = entry["tg"].lower()
    if "nobel" in tag_lower:
        tags.append("nobel-laureate")
    if "kavli" in tag_lower:
        tags.append("kavli-prize")
    if "macarthur" in tag_lower:
        tags.append("macarthur-fellow")
    if "breakthrough" in tag_lower:
        tags.append("breakthrough-prize")
    if "founder" in tag_lower or "ceo" in tag_lower:
        tags.append("founder-or-ceo")
    if tags:
        leader["tags"] = tags

    return leader


def dump_yaml(data: dict) -> str:
    """Dump a dict to YAML with good formatting for human editing."""
    # Custom ordering that puts short metadata first, long narrative last
    ordered_keys = [
        "id", "name", "honorific", "also_known_as",
        "origin", "current_roles", "previous_roles", "education",
        "domains", "tier", "tier_justification",
        "metrics", "awards", "ventures", "key_works",
        "summary", "links", "relationships", "verification", "tags",
    ]
    ordered = {}
    for k in ordered_keys:
        if k in data:
            ordered[k] = data[k]

    # PyYAML settings for readability
    return yaml.dump(
        ordered,
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
        width=100,
    )


def main():
    if len(sys.argv) != 2:
        print("Usage: python migrate_jsx_to_yaml.py <path-to-jsx-file>")
        sys.exit(1)

    jsx_path = Path(sys.argv[1])
    if not jsx_path.exists():
        print(f"Error: file not found: {jsx_path}")
        sys.exit(1)

    jsx_text = jsx_path.read_text()
    entries = extract_entries(jsx_text)

    print(f"Extracted {len(entries)} entries from {jsx_path.name}")

    out_dir = Path(__file__).parent.parent / "data" / "leaders"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Track generated slugs to catch collisions
    slugs_seen = {}

    for entry in entries:
        leader = entry_to_yaml(entry)
        slug = leader["id"]

        if slug in slugs_seen:
            # Collision — append a suffix (handle multi-person entries)
            print(f"  Slug collision: {slug}. Adjusting.")
            counter = 2
            while f"{slug}-{counter}" in slugs_seen:
                counter += 1
            slug = f"{slug}-{counter}"
            leader["id"] = slug

        slugs_seen[slug] = True
        out_path = out_dir / f"{slug}.yaml"
        out_path.write_text(dump_yaml(leader))

    print(f"Wrote {len(slugs_seen)} leader YAML files to {out_dir}/")
    print(f"\nNext steps:")
    print(f"  1. Review a sample: cat {out_dir}/jennifer-doudna.yaml")
    print(f"  2. Validate the schema: python scripts/validate_data.py")
    print(f"  3. Start the Tier 1 verification pass (7 entries)")


if __name__ == "__main__":
    main()
