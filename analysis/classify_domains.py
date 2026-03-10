#!/usr/bin/env python3
"""
Classify citations by domain and compute cross-domain rates.

Reads: data/raw/citations_*.json + data/raw/paper_metadata.json
       domain_mapping.json

Outputs: data/processed/classified_citations.json
         data/processed/per_paper_summary.json
         data/processed/period_analysis.json

Usage:
    python classify_domains.py
"""

import json
import os
import math
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(__file__)
RAW_DIR = os.path.join(SCRIPT_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(SCRIPT_DIR, "data", "processed")
MAPPING_FILE = os.path.join(SCRIPT_DIR, "domain_mapping.json")

PERIODS = [
    (1987, 1995, "1987--1995"),
    (1996, 2005, "1996--2005"),
    (2006, 2015, "2006--2015"),
    (2016, 2026, "2016--2026"),
]


def load_mapping():
    with open(MAPPING_FILE) as f:
        return json.load(f)


def classify_citation(citing_paper, seed_domain, field_to_domain):
    """Classify a single citation. Returns (primary_domain, is_cross_domain)."""
    cp = citing_paper.get("citingPaper", citing_paper)
    fields = cp.get("fieldsOfStudy") or []
    if not fields:
        return "Unknown", None

    domains = set()
    for f in fields:
        mapped = field_to_domain.get(f, "Other")
        domains.add(mapped)

    is_cross = seed_domain not in domains
    primary = list(domains)[0] if domains else "Unknown"
    return primary, is_cross


def chi_squared_pvalue(chi2, df=1):
    """Chi-squared p-value for df=1."""
    if df == 1:
        return math.erfc(math.sqrt(chi2 / 2.0))
    # General case
    a = df / 2.0
    x = chi2 / 2.0
    if x == 0:
        return 1.0
    total = 0.0
    term = 1.0 / a
    total = term
    for n in range(1, 300):
        term *= x / (a + n)
        total += term
        if abs(term) < 1e-15:
            break
    lower_gamma = total * math.exp(-x + a * math.log(x) - math.lgamma(a))
    return 1.0 - lower_gamma


def main():
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    mapping = load_mapping()
    field_to_domain = mapping["field_to_domain"]

    metadata_file = os.path.join(RAW_DIR, "paper_metadata.json")
    if not os.path.exists(metadata_file):
        print("ERROR: Run fetch_citations.py first")
        return 1

    with open(metadata_file) as f:
        metadata = json.load(f)

    print(f"Classifying citations for {len(metadata)} papers")
    print("=" * 60)

    all_classified = {}
    per_paper_summary = []

    for label, meta in metadata.items():
        citation_file = os.path.join(RAW_DIR, meta["file"])
        if not os.path.exists(citation_file):
            print(f"  {label}: citation file missing, skipping")
            continue

        with open(citation_file) as f:
            citations = json.load(f)

        seed_domain = meta["seed_domain"]
        classified = []
        domain_counts = defaultdict(int)
        cross_count = 0
        unknown_count = 0

        for cit in citations:
            cp = cit.get("citingPaper", cit)
            year = cp.get("year")
            primary, is_cross = classify_citation(cit, seed_domain, field_to_domain)

            entry = {
                "year": year,
                "primary_domain": primary,
                "is_cross_domain": is_cross,
                "title": cp.get("title", ""),
            }
            classified.append(entry)
            domain_counts[primary] += 1

            if is_cross is None:
                unknown_count += 1
            elif is_cross:
                cross_count += 1

        total_known = len(classified) - unknown_count
        cross_rate = cross_count / total_known if total_known > 0 else 0

        print(f"  {label}: {len(classified)} citations, "
              f"{cross_count} cross-domain ({cross_rate:.1%}), "
              f"{unknown_count} unknown")

        all_classified[label] = classified
        per_paper_summary.append({
            "label": label,
            "seed_domain": seed_domain,
            "total": len(classified),
            "total_known": total_known,
            "cross_domain": cross_count,
            "unknown": unknown_count,
            "cross_rate": round(cross_rate, 4),
            "domain_counts": dict(domain_counts),
        })

    # Period analysis (aggregate across all papers)
    print(f"\n{'=' * 60}")
    print("Period analysis")

    period_analysis = {}
    for start, end, label in PERIODS:
        same = 0
        cross = 0
        domain_counts = defaultdict(int)

        for paper_label, classified in all_classified.items():
            seed_domain = metadata[paper_label]["seed_domain"]
            for cit in classified:
                year = cit["year"]
                if year is None or year < start or year > end:
                    continue
                if cit["is_cross_domain"] is None:
                    continue
                domain_counts[cit["primary_domain"]] += 1
                if cit["is_cross_domain"]:
                    cross += 1
                else:
                    same += 1

        total = same + cross
        if total == 0:
            period_analysis[label] = {
                "total": 0, "same": 0, "cross": 0,
                "obs_rate": 0, "exp_rate": 0, "chi2": 0, "p_value": 1.0,
            }
            continue

        obs_rate = cross / total

        # Null model: HHI-based expected cross-domain rate
        total_classified = sum(domain_counts.values())
        hhi = sum((c / total_classified) ** 2 for c in domain_counts.values())
        exp_rate = 1.0 - hhi

        # Chi-squared
        expected_cross = total * exp_rate
        expected_same = total * (1 - exp_rate)
        if expected_cross > 0 and expected_same > 0:
            chi2 = ((cross - expected_cross) ** 2 / expected_cross +
                     (same - expected_same) ** 2 / expected_same)
            p_val = chi_squared_pvalue(chi2)
        else:
            chi2, p_val = 0.0, 1.0

        period_analysis[label] = {
            "total": total,
            "same": same,
            "cross": cross,
            "obs_rate": round(obs_rate, 4),
            "exp_rate": round(exp_rate, 4),
            "chi2": round(chi2, 2),
            "p_value": round(p_val, 6),
            "domain_counts": dict(domain_counts),
        }

        print(f"  {label}: N={total}, cross={obs_rate:.1%} (exp {exp_rate:.1%}), "
              f"chi2={chi2:.1f}, p={p_val:.6f}")

    # Save results
    with open(os.path.join(PROCESSED_DIR, "classified_citations.json"), "w") as f:
        json.dump(all_classified, f)
    with open(os.path.join(PROCESSED_DIR, "per_paper_summary.json"), "w") as f:
        json.dump(per_paper_summary, f, indent=2)
    with open(os.path.join(PROCESSED_DIR, "period_analysis.json"), "w") as f:
        json.dump(period_analysis, f, indent=2)

    print(f"\nResults saved to {PROCESSED_DIR}/")
    return 0


if __name__ == "__main__":
    exit(main())
