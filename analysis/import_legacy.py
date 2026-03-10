#!/usr/bin/env python3
"""
One-time migration: import v1 citation_cache.json into per-paper files.
Run once, then use fetch_citations.py for new papers.
"""

import json
import os

SCRIPT_DIR = os.path.dirname(__file__)
RAW_DIR = os.path.join(SCRIPT_DIR, "data", "raw")
LEGACY_FILE = os.path.join(RAW_DIR, "legacy_cache_v1.json")

# Map v1 cache keys → new seed labels (from domain_mapping.json)
LABEL_MAP = {
    "Bak et al. 1987": "Bak et al. 1987",
    "Peng et al. 1994": "Peng et al. 1994 (DFA)",
    "Crucitti et al. 2004": "Crucitti et al. 2004",
    "Dobson et al. 2007": "Dobson et al. 2007",
    "Mantegna & Stanley 1995": "Mantegna & Stanley 1995",
    "Saxe et al. 2013": "Saxe et al. 2013",
    "Kauffman 1993": "Kauffman 1993",
    "Jaeger 2001": "Jaeger 2001",
    "Sornette 2004": "Sornette 2004",
    "Peters 1994": "Peters 1994",
}


def safe_filename(label):
    return label.replace(" ", "_").replace("&", "and").replace(".", "").replace("(", "").replace(")", "")


def main():
    with open(LEGACY_FILE) as f:
        cache = json.load(f)

    # Load or create metadata
    metadata_file = os.path.join(RAW_DIR, "paper_metadata.json")
    metadata = {}

    imported = 0
    for cache_key, data in cache.items():
        old_label = data.get("label", cache_key)
        new_label = LABEL_MAP.get(old_label, old_label)
        safe_name = safe_filename(new_label)
        citation_file = os.path.join(RAW_DIR, f"citations_{safe_name}.json")

        # Extract citations list
        citations = data.get("citations", [])

        # Write per-paper citation file
        with open(citation_file, "w") as f:
            json.dump(citations, f)

        # Build metadata entry
        metadata[new_label] = {
            "paper_id": data.get("paper_id", ""),
            "title": data.get("title", ""),
            "year": None,  # not stored in v1 cache
            "citation_count": data.get("total_citation_count", len(citations)),
            "retrieved_count": data.get("retrieved_count", len(citations)),
            "seed_domain": data.get("seed_domain", ""),
            "cache_key": cache_key,
            "file": f"citations_{safe_name}.json",
            "source": "imported_from_v1",
        }
        imported += 1
        print(f"  Imported: {new_label} ({len(citations)} citations)")

    with open(metadata_file, "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"\nImported {imported} papers from legacy cache")
    print(f"Metadata: {metadata_file}")
    return 0


if __name__ == "__main__":
    exit(main())
