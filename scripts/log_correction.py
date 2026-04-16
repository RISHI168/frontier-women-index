#!/usr/bin/env python3
"""
Interactive helper for appending a correction to CORRECTIONS.md.

Usage:
    python scripts/log_correction.py

Prompts for details and prepends a properly formatted entry to CORRECTIONS.md.
"""

import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).parent.parent
LOG = REPO / "CORRECTIONS.md"


def prompt(label: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{label}{suffix}: ").strip()
    return value or default


def main():
    if not LOG.exists():
        print(f"Error: {LOG} not found", file=sys.stderr)
        sys.exit(1)

    print("Log a correction to CORRECTIONS.md")
    print("----------------------------------")
    print()

    subject = prompt("Subject (leader name or 'Global issue')")
    if not subject:
        print("Subject is required. Aborting.")
        sys.exit(1)

    nature = prompt("Nature (brief description of what was wrong)")
    reporter = prompt("Reported by (GitHub handle, or 'internal review')", "internal review")
    resolution = prompt("Resolution (what changed; include PR link if merged)")
    source_diff = prompt("Source diff path (e.g., 'data/leaders/slug.yaml')")

    today = str(date.today())

    entry = f"""\
## {today} · {subject}

**Nature:** {nature}
**Reported by:** {reporter}
**Resolution:** {resolution}
**Source diff:** `{source_diff}`

"""

    # Find the "## Entries" section and insert the new entry immediately after
    content = LOG.read_text()
    marker = "## Entries\n"
    idx = content.find(marker)
    if idx < 0:
        print("Error: Could not find '## Entries' marker in CORRECTIONS.md", file=sys.stderr)
        sys.exit(1)
    insertion_point = idx + len(marker)

    # If the placeholder "_No corrections have been logged yet._" line is
    # present, we want to remove it the first time we add an entry.
    placeholder = "_No corrections have been logged yet. The Index was launched on April 2026._\n\n---"
    if placeholder in content:
        content = content.replace(placeholder + "\n\n", "")
        content = content.replace(placeholder, "")

    new_content = (
        content[:insertion_point]
        + "\n<!-- New entries are added at the top. -->\n\n"
        + entry
        + content[insertion_point:].lstrip("\n")
    )

    # Avoid duplicating the HTML comment if it's already present
    new_content = new_content.replace(
        "<!-- New entries are added at the top. -->\n\n<!-- New entries are added at the top. -->\n\n",
        "<!-- New entries are added at the top. -->\n\n",
    )

    LOG.write_text(new_content)
    print()
    print(f"Correction logged in {LOG}")
    print("Remember to commit and push to the project repo.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAborted.")
        sys.exit(1)
