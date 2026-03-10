#!/usr/bin/env python3
"""
Fetch citation data from Semantic Scholar API for all seed papers.

Outputs: data/raw/citations_{paper_id}.json (one file per seed paper)
         data/raw/paper_metadata.json (resolved paper IDs and metadata)

Usage:
    python fetch_citations.py                # fetch all, using cache
    python fetch_citations.py --refresh      # re-fetch even if cached
    python fetch_citations.py --paper "Bak"  # fetch only matching seed
"""

import urllib.request
import urllib.error
import json
import time
import sys
import os
import argparse

RATE_LIMIT = 5.0  # seconds between API calls — be polite to S2
MAX_CITATIONS_PER_PAPER = 10000  # no artificial cap; let API decide
BASE_URL = "https://api.semanticscholar.org/graph/v1"
RAW_DIR = os.path.join(os.path.dirname(__file__), "data", "raw")
MAPPING_FILE = os.path.join(os.path.dirname(__file__), "domain_mapping.json")


def api_get(url, retries=3):
    """GET with rate limiting and retries."""
    for attempt in range(retries):
        try:
            time.sleep(RATE_LIMIT)
            req = urllib.request.Request(
                url, headers={"User-Agent": "CriticalityPaperAnalysis/2.0"}
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = 120 * (attempt + 1)  # back off generously
                print(f"  Rate limited, waiting {wait}s (being polite)...")
                time.sleep(wait)
            elif e.code == 404:
                return None
            else:
                print(f"  HTTP {e.code} on attempt {attempt + 1}/{retries}")
                time.sleep(30)
        except Exception as e:
            print(f"  Error: {e} on attempt {attempt + 1}/{retries}")
            time.sleep(30)
    return None


def find_paper(seed):
    """Resolve a seed paper to its Semantic Scholar ID."""
    if "id" in seed:
        url = f"{BASE_URL}/paper/{seed['id']}?fields=paperId,title,year,citationCount,fieldsOfStudy"
        data = api_get(url)
        if data and "paperId" in data:
            return data

    if "search" in seed:
        query = urllib.request.quote(seed["search"])
        url = f"{BASE_URL}/paper/search?query={query}&fields=paperId,title,year,citationCount,fieldsOfStudy&limit=5"
        data = api_get(url)
        if data and data.get("data"):
            best = None
            for p in data["data"]:
                if p.get("year") and abs(p["year"] - seed["year"]) <= 2:
                    if best is None or (p.get("citationCount") or 0) > (
                        best.get("citationCount") or 0
                    ):
                        best = p
            return best or data["data"][0]

    return None


def get_citations(paper_id, max_count=MAX_CITATIONS_PER_PAPER):
    """Retrieve all citations with pagination."""
    all_citations = []
    offset = 0
    limit = 1000

    while offset < max_count:
        url = (
            f"{BASE_URL}/paper/{paper_id}/citations"
            f"?fields=paperId,title,year,fieldsOfStudy,externalIds"
            f"&offset={offset}&limit={limit}"
        )
        data = api_get(url)
        if not data or not data.get("data"):
            break

        batch = data["data"]
        all_citations.extend(batch)
        print(f"    {len(all_citations)} citations (offset {offset})")

        if len(batch) < limit:
            break
        offset += limit

    return all_citations


def main():
    parser = argparse.ArgumentParser(description="Fetch citation data from Semantic Scholar")
    parser.add_argument("--refresh", action="store_true", help="Re-fetch even if cached")
    parser.add_argument("--paper", type=str, help="Only fetch seeds matching this substring")
    args = parser.parse_args()

    os.makedirs(RAW_DIR, exist_ok=True)

    with open(MAPPING_FILE) as f:
        mapping = json.load(f)

    seeds = mapping["seed_papers"]
    if args.paper:
        seeds = [s for s in seeds if args.paper.lower() in s["label"].lower()]
        print(f"Filtered to {len(seeds)} seed(s) matching '{args.paper}'")

    metadata_file = os.path.join(RAW_DIR, "paper_metadata.json")
    if os.path.exists(metadata_file):
        with open(metadata_file) as f:
            metadata = json.load(f)
    else:
        metadata = {}

    print(f"Fetching citations for {len(seeds)} seed papers")
    print(f"Max {MAX_CITATIONS_PER_PAPER} citations per paper, {RATE_LIMIT}s rate limit")
    print("=" * 60)

    for i, seed in enumerate(seeds):
        label = seed["label"]
        print(f"\n[{i + 1}/{len(seeds)}] {label} (domain: {seed['domain']})")

        # Check if already cached
        cache_key = seed.get("id", seed.get("search", label))
        safe_name = label.replace(" ", "_").replace("&", "and").replace(".", "")
        citation_file = os.path.join(RAW_DIR, f"citations_{safe_name}.json")

        if os.path.exists(citation_file) and not args.refresh:
            print("  Cached, skipping (use --refresh to re-fetch)")
            continue

        # Resolve paper
        paper = find_paper(seed)
        if not paper:
            print(f"  WARNING: Not found on Semantic Scholar")
            continue

        paper_id = paper["paperId"]
        cit_count = paper.get("citationCount", 0)
        print(f"  Found: {paper.get('title', 'N/A')[:70]}")
        print(f"  Total citations: {cit_count}")

        # Fetch citations
        citations = get_citations(paper_id)
        print(f"  Retrieved: {len(citations)}")

        # Save raw citation data
        with open(citation_file, "w") as f:
            json.dump(citations, f)

        # Update metadata
        metadata[label] = {
            "paper_id": paper_id,
            "title": paper.get("title", ""),
            "year": paper.get("year"),
            "citation_count": cit_count,
            "retrieved_count": len(citations),
            "seed_domain": seed["domain"],
            "cache_key": cache_key,
            "file": os.path.basename(citation_file),
        }

        with open(metadata_file, "w") as f:
            json.dump(metadata, f, indent=2)

    print(f"\n{'=' * 60}")
    print(f"Done. {len(metadata)} papers in metadata.")
    print(f"Raw data in: {RAW_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
