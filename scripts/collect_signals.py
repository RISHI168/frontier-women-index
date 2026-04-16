#!/usr/bin/env python3
"""
Weekly citation snapshot via Semantic Scholar API.

Reads every leader YAML in data/leaders/, looks up their current citation count
via Semantic Scholar, and appends a row to signals/scholar_deltas.csv.

This is the first Living Index signal. Runs every Monday via GitHub Actions.

Usage:
    python scripts/collect_signals.py [--dry-run]

Environment variables:
    SEMANTIC_SCHOLAR_API_KEY    Optional. Increases rate limit. Free API key at
                                https://www.semanticscholar.org/product/api.

Output format (signals/scholar_deltas.csv):
    date,leader_id,name,citations,h_index,source_url,notes
"""

import os
import sys
import csv
import time
from datetime import date
from pathlib import Path

try:
    import yaml
    import requests
except ImportError:
    print("Required: pip install pyyaml requests")
    sys.exit(1)


REPO = Path(__file__).parent.parent
LEADERS_DIR = REPO / "data" / "leaders"
SIGNALS_DIR = REPO / "signals"
OUTPUT_CSV = SIGNALS_DIR / "scholar_deltas.csv"

API_BASE = "https://api.semanticscholar.org/graph/v1"
API_KEY = os.environ.get("SEMANTIC_SCHOLAR_API_KEY", "").strip()

# Respectful rate limit even with a key. Semantic Scholar's public tier is
# strict; with an API key we can safely go ~1/sec.
RATE_LIMIT_SECONDS = 1.2


def api_headers():
    headers = {"User-Agent": "FrontierWomenIndex/1.0 (https://frontierwomenindex.org)"}
    if API_KEY:
        headers["x-api-key"] = API_KEY
    return headers


def find_author(name: str, scholar_hint: str = None):
    """Look up an author by name on Semantic Scholar.

    Returns a dict with {authorId, citationCount, hIndex, name} if found,
    else None.

    Strategy:
      1. If a Google Scholar URL is provided, we can't map it directly (S2 uses
         different IDs), but the name alone is usually enough.
      2. Search by name, take the highest-citation match as the most likely
         candidate. If top result has <100 citations, flag as low-confidence.
    """
    try:
        resp = requests.get(
            f"{API_BASE}/author/search",
            params={
                "query": name,
                "limit": 5,
                "fields": "authorId,name,affiliations,citationCount,hIndex,paperCount",
            },
            headers=api_headers(),
            timeout=15,
        )
    except requests.RequestException as e:
        return None, f"request_failed: {e}"

    if resp.status_code == 429:
        # Rate-limited — back off and retry once
        time.sleep(5)
        try:
            resp = requests.get(
                f"{API_BASE}/author/search",
                params={"query": name, "limit": 5,
                        "fields": "authorId,name,citationCount,hIndex"},
                headers=api_headers(),
                timeout=15,
            )
        except requests.RequestException as e:
            return None, f"retry_failed: {e}"

    if resp.status_code != 200:
        return None, f"http_{resp.status_code}"

    data = resp.json()
    candidates = data.get("data", []) or []
    if not candidates:
        return None, "no_match"

    # Pick highest-citation match
    best = max(candidates, key=lambda c: c.get("citationCount") or 0)
    if (best.get("citationCount") or 0) < 100:
        return best, "low_confidence"
    return best, "ok"


def load_leader(path: Path):
    try:
        return yaml.safe_load(path.read_text())
    except Exception as e:
        print(f"  skip {path.name}: parse error: {e}", file=sys.stderr)
        return None


def ensure_csv():
    SIGNALS_DIR.mkdir(parents=True, exist_ok=True)
    if not OUTPUT_CSV.exists():
        with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow([
                "date", "leader_id", "name",
                "citations", "h_index",
                "source_url", "notes",
            ])


def main():
    dry_run = "--dry-run" in sys.argv
    today = str(date.today())

    if not LEADERS_DIR.exists():
        print(f"Error: {LEADERS_DIR} does not exist", file=sys.stderr)
        sys.exit(1)

    ensure_csv()
    leader_files = sorted(LEADERS_DIR.glob("*.yaml"))
    print(f"Collecting signals for {len(leader_files)} leaders"
          f"{' (dry run)' if dry_run else ''}")
    if not API_KEY:
        print("  (no SEMANTIC_SCHOLAR_API_KEY set — running at public rate limit)")

    rows_to_write = []
    stats = {"ok": 0, "low_confidence": 0, "no_match": 0, "error": 0}

    for i, path in enumerate(leader_files, 1):
        leader = load_leader(path)
        if not leader:
            stats["error"] += 1
            continue

        name = leader.get("name", "")
        slug = leader.get("id", path.stem)
        scholar_hint = (leader.get("links") or {}).get("scholar")

        result, status = find_author(name, scholar_hint)
        if status.startswith("http_") or status.startswith("request_failed") or status.startswith("retry_failed"):
            stats["error"] += 1
            note = f"lookup_error: {status}"
            citations, h_index, source_url = "", "", ""
        elif status == "no_match":
            stats["no_match"] += 1
            note = "no_match"
            citations, h_index, source_url = "", "", ""
        else:
            stats[status] += 1
            citations = result.get("citationCount", "")
            h_index = result.get("hIndex", "")
            author_id = result.get("authorId", "")
            source_url = f"https://www.semanticscholar.org/author/{author_id}" if author_id else ""
            note = status

        rows_to_write.append([
            today, slug, name, citations, h_index, source_url, note,
        ])

        # Progress indicator every 10 leaders
        if i % 10 == 0:
            print(f"  [{i}/{len(leader_files)}] {name}: {note}")

        time.sleep(RATE_LIMIT_SECONDS)

    # Write all new rows
    if not dry_run:
        with OUTPUT_CSV.open("a", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerows(rows_to_write)

    print("\nSummary:")
    print(f"  matched (high confidence): {stats['ok']}")
    print(f"  matched (low confidence):  {stats['low_confidence']}")
    print(f"  no match found:            {stats['no_match']}")
    print(f"  errors:                    {stats['error']}")
    if dry_run:
        print("\n(dry run — no changes written)")
    else:
        print(f"\nAppended {len(rows_to_write)} rows to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
