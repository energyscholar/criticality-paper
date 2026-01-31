#!/usr/bin/env python3
"""
Citation network analysis for cross-domain criticality paper.
Uses Semantic Scholar API (public, no key required).
Requires only stdlib + numpy (no requests/scipy).

Output: citation_results.json + LaTeX table fragment
"""

import urllib.request
import urllib.error
import json
import time
import math
import sys
import os
from collections import defaultdict

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

RATE_LIMIT = 3.2  # seconds between API calls
MAX_CITATIONS_PER_PAPER = 2000
CACHE_FILE = "citation_cache.json"
RESULTS_FILE = "citation_results.json"

# Seed papers: identifier (DOI or title), assigned domain, label
SEED_PAPERS = [
    {
        "id": "DOI:10.1103/PhysRevLett.59.381",
        "domain": "Physics",
        "label": "Bak et al. 1987",
        "year": 1987,
    },
    {
        "id": "DOI:10.1103/PhysRevE.49.1685",
        "domain": "Biomedical",
        "label": "Peng et al. 1994",
        "year": 1994,
    },
    {
        "id": "DOI:10.1103/PhysRevE.69.045104",
        "domain": "Engineering",
        "label": "Crucitti et al. 2004",
        "year": 2004,
    },
    {
        "id": "DOI:10.1063/1.2737822",
        "domain": "Engineering",
        "label": "Dobson et al. 2007",
        "year": 2007,
    },
    {
        "id": "DOI:10.1038/376046a0",
        "domain": "Finance",
        "label": "Mantegna & Stanley 1995",
        "year": 1995,
    },
    {
        "id": "ARXIV:1312.6120",
        "domain": "CS/ML",
        "label": "Saxe et al. 2013",
        "year": 2013,
    },
    # Books/reports - use title search
    {
        "search": "The origins of order self-organization selection evolution Kauffman",
        "domain": "Biology",
        "label": "Kauffman 1993",
        "year": 1993,
    },
    {
        "search": "echo state approach analysing training recurrent neural networks Jaeger",
        "domain": "CS/ML",
        "label": "Jaeger 2001",
        "year": 2001,
    },
    {
        "search": "Critical Phenomena Natural Sciences Chaos Fractals Sornette",
        "domain": "Physics",
        "label": "Sornette 2004",
        "year": 2004,
    },
    {
        "search": "Fractal market analysis chaos theory Peters",
        "domain": "Finance",
        "label": "Peters 1994",
        "year": 1994,
    },
]

# Map Semantic Scholar fieldsOfStudy to our domains
FIELD_TO_DOMAIN = {
    "Physics": "Physics",
    "Mathematics": "Physics",
    "Biology": "Biomedical",
    "Medicine": "Biomedical",
    "Computer Science": "CS/ML",
    "Engineering": "Engineering",
    "Economics": "Finance",
    "Business": "Finance",
    "Environmental Science": "Engineering",
    "Geology": "Physics",
    "Materials Science": "Physics",
    "Chemistry": "Physics",
    "Psychology": "Biomedical",
    "Sociology": "Social Science",
    "Political Science": "Social Science",
    "Art": "Other",
    "History": "Other",
    "Philosophy": "Other",
    "Geography": "Other",
    "Linguistics": "Other",
    "Agricultural and Food Sciences": "Other",
    "Education": "Other",
}

PERIODS = [
    (1987, 2000, "1987--2000"),
    (2001, 2010, "2001--2010"),
    (2011, 2025, "2011--2025"),
]


def api_get(url, retries=3):
    """GET request with rate limiting and retries."""
    for attempt in range(retries):
        try:
            time.sleep(RATE_LIMIT)
            req = urllib.request.Request(url, headers={"User-Agent": "CriticalityPaperAnalysis/1.0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = 60 * (attempt + 1)
                print(f"  Rate limited, waiting {wait}s...")
                time.sleep(wait)
            elif e.code == 404:
                return None
            else:
                print(f"  HTTP {e.code} on attempt {attempt+1}/{retries}")
                time.sleep(10)
        except Exception as e:
            print(f"  Error: {e} on attempt {attempt+1}/{retries}")
            time.sleep(10)
    return None


def find_paper(seed):
    """Look up a seed paper on Semantic Scholar."""
    base = "https://api.semanticscholar.org/graph/v1"

    if "id" in seed:
        url = f"{base}/paper/{seed['id']}?fields=paperId,title,year,citationCount,fieldsOfStudy"
        data = api_get(url)
        if data and "paperId" in data:
            return data

    if "search" in seed:
        query = urllib.request.quote(seed["search"])
        url = f"{base}/paper/search?query={query}&fields=paperId,title,year,citationCount,fieldsOfStudy&limit=5"
        data = api_get(url)
        if data and data.get("data"):
            # Pick best match by year proximity
            best = None
            for p in data["data"]:
                if p.get("year") and abs(p["year"] - seed["year"]) <= 2:
                    if best is None or (p.get("citationCount") or 0) > (best.get("citationCount") or 0):
                        best = p
            return best or data["data"][0]

    # Fallback: title search
    if "id" in seed and seed["id"].startswith("DOI:"):
        query = urllib.request.quote(seed["label"])
        url = f"{base}/paper/search?query={query}&fields=paperId,title,year,citationCount,fieldsOfStudy&limit=3"
        data = api_get(url)
        if data and data.get("data"):
            return data["data"][0]

    return None


def get_citations(paper_id, max_count=MAX_CITATIONS_PER_PAPER):
    """Retrieve citations with pagination."""
    base = "https://api.semanticscholar.org/graph/v1"
    all_citations = []
    offset = 0
    limit = 1000

    while offset < max_count:
        url = (
            f"{base}/paper/{paper_id}/citations"
            f"?fields=paperId,title,year,fieldsOfStudy"
            f"&offset={offset}&limit={limit}"
        )
        data = api_get(url)
        if not data or not data.get("data"):
            break

        batch = data["data"]
        all_citations.extend(batch)
        print(f"    Retrieved {len(all_citations)} citations (offset {offset})")

        if len(batch) < limit:
            break
        offset += limit

    return all_citations


def classify_citation(citing_paper, seed_domain):
    """Classify a citation as same-domain or cross-domain."""
    fields = citing_paper.get("fieldsOfStudy") or []
    if not fields:
        return "Unknown", None

    # Map to our domain categories
    domains = set()
    for f in fields:
        mapped = FIELD_TO_DOMAIN.get(f, "Other")
        domains.add(mapped)

    # Check if any of the citing paper's domains match the seed's domain
    is_cross_domain = seed_domain not in domains
    primary = list(domains)[0] if domains else "Unknown"
    return primary, is_cross_domain


def chi_squared_pvalue(chi2, df=1):
    """Compute chi-squared p-value using incomplete gamma function approximation."""
    # For df=1: p = erfc(sqrt(chi2/2))
    if df == 1:
        return math.erfc(math.sqrt(chi2 / 2.0))

    # General case using series approximation of regularized lower incomplete gamma
    # P(a, x) where a = df/2, x = chi2/2
    a = df / 2.0
    x = chi2 / 2.0
    if x == 0:
        return 1.0

    # Use series expansion for lower incomplete gamma
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


def analyze_results(paper_results):
    """Compute cross-domain rates, null model, chi-squared test."""
    # Aggregate citations by period
    period_data = {}
    for start, end, label in PERIODS:
        same = 0
        cross = 0
        domain_counts = defaultdict(int)

        for pr in paper_results:
            for cit in pr["citations"]:
                cp = cit.get("citingPaper", cit)
                year = cp.get("year")
                if year is None or year < start or year > end:
                    continue

                primary_domain, is_cross = classify_citation(cp, pr["seed_domain"])
                if is_cross is None:
                    continue  # skip unclassifiable

                domain_counts[primary_domain] += 1
                if is_cross:
                    cross += 1
                else:
                    same += 1

        total = same + cross
        if total == 0:
            period_data[label] = {
                "total": 0, "same": 0, "cross": 0,
                "obs_rate": 0, "exp_rate": 0, "chi2": 0, "p_value": 1.0,
                "domain_counts": dict(domain_counts),
            }
            continue

        obs_rate = cross / total

        # Null model: expected cross-domain rate = 1 - Σ(p_i²)
        # where p_i is domain share among citing papers
        total_classified = sum(domain_counts.values())
        hhi = sum((c / total_classified) ** 2 for c in domain_counts.values()) if total_classified > 0 else 1.0
        exp_rate = 1.0 - hhi

        # Chi-squared test: observed vs expected
        expected_cross = total * exp_rate
        expected_same = total * (1 - exp_rate)

        if expected_cross > 0 and expected_same > 0:
            chi2 = ((cross - expected_cross) ** 2 / expected_cross +
                     (same - expected_same) ** 2 / expected_same)
            p_val = chi_squared_pvalue(chi2, df=1)
        else:
            chi2 = 0.0
            p_val = 1.0

        period_data[label] = {
            "total": total,
            "same": same,
            "cross": cross,
            "obs_rate": round(obs_rate, 4),
            "exp_rate": round(exp_rate, 4),
            "chi2": round(chi2, 2),
            "p_value": round(p_val, 6),
            "domain_counts": dict(domain_counts),
        }

    return period_data


def generate_latex_table(period_data):
    """Generate LaTeX table fragment for the paper."""
    lines = [
        r"\begin{table}[h]",
        r"\centering",
        r"\caption{Cross-domain citation rates by period (Semantic Scholar API, \today)}",
        r"\label{tab:citations}",
        r"\begin{tabular}{lrrrrl}",
        r"\toprule",
        r"\textbf{Period} & \textbf{N} & \textbf{Obs.\ cross-domain} & \textbf{Expected} & $\chi^2$ & $p$ \\",
        r"\midrule",
    ]

    for _, _, label in PERIODS:
        d = period_data.get(label, {})
        n = d.get("total", 0)
        obs = f"{d.get('obs_rate', 0):.1%}"
        exp = f"{d.get('exp_rate', 0):.1%}"
        chi2 = f"{d.get('chi2', 0):.1f}"
        p = d.get("p_value", 1.0)
        p_str = f"{p:.4f}" if p >= 0.0001 else f"$<$0.0001"
        lines.append(f"{label} & {n} & {obs} & {exp} & {chi2} & {p_str} \\\\")

    lines.extend([
        r"\bottomrule",
        r"\end{tabular}",
        r"\end{table}",
    ])
    return "\n".join(lines)


def main():
    print("=" * 60)
    print("Cross-Domain Citation Analysis")
    print("Semantic Scholar API (public, rate-limited)")
    print("=" * 60)

    # Load cache if exists
    cache = {}
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE) as f:
            cache = json.load(f)
        print(f"Loaded cache with {len(cache)} papers")

    paper_results = []
    api_notes = []

    for i, seed in enumerate(SEED_PAPERS):
        print(f"\n[{i+1}/{len(SEED_PAPERS)}] {seed['label']} (domain: {seed['domain']})")

        # Check cache
        cache_key = seed.get("id", seed.get("search", seed["label"]))
        if cache_key in cache:
            print("  Using cached data")
            paper_results.append(cache[cache_key])
            continue

        # Find paper
        paper = find_paper(seed)
        if not paper:
            print(f"  WARNING: Could not find paper on Semantic Scholar")
            api_notes.append(f"{seed['label']}: not found in Semantic Scholar")
            continue

        paper_id = paper["paperId"]
        cit_count = paper.get("citationCount", 0)
        print(f"  Found: {paper.get('title', 'N/A')[:60]}...")
        print(f"  Citations: {cit_count}")

        if cit_count > MAX_CITATIONS_PER_PAPER:
            api_notes.append(
                f"{seed['label']}: {cit_count} total citations, sampled first {MAX_CITATIONS_PER_PAPER}"
            )

        # Get citations
        citations = get_citations(paper_id)
        print(f"  Retrieved {len(citations)} citations")

        result = {
            "label": seed["label"],
            "seed_domain": seed["domain"],
            "paper_id": paper_id,
            "title": paper.get("title", ""),
            "total_citation_count": cit_count,
            "retrieved_count": len(citations),
            "citations": citations,
        }
        paper_results.append(result)
        cache[cache_key] = result

        # Save cache incrementally
        with open(CACHE_FILE, "w") as f:
            json.dump(cache, f)

    # Analysis
    print("\n" + "=" * 60)
    print("ANALYSIS")
    print("=" * 60)

    period_data = analyze_results(paper_results)

    for _, _, label in PERIODS:
        d = period_data.get(label, {})
        print(f"\n{label}:")
        print(f"  Total citations: {d.get('total', 0)}")
        print(f"  Cross-domain: {d.get('cross', 0)} ({d.get('obs_rate', 0):.1%})")
        print(f"  Expected (null): {d.get('exp_rate', 0):.1%}")
        print(f"  Chi-squared: {d.get('chi2', 0):.2f}, p = {d.get('p_value', 1.0):.6f}")
        print(f"  Domain counts: {d.get('domain_counts', {})}")

    # Counter-evidence check: Sornette early cross-domain
    print("\n--- Counter-evidence check ---")
    for pr in paper_results:
        if "Sornette" in pr["label"]:
            early_cross = 0
            early_total = 0
            for cit in pr["citations"]:
                cp = cit.get("citingPaper", cit)
                year = cp.get("year")
                if year and 1987 <= year <= 2010:
                    _, is_cross = classify_citation(cp, pr["seed_domain"])
                    if is_cross is not None:
                        early_total += 1
                        if is_cross:
                            early_cross += 1
            if early_total > 0:
                rate = early_cross / early_total
                print(f"  Sornette 2004 early cross-domain rate: {rate:.1%} ({early_cross}/{early_total})")
                if rate > 0.3:
                    api_notes.append(
                        f"Counter-evidence: Sornette (2004) shows {rate:.0%} cross-domain "
                        f"citation rate in 2001--2010, consistent with its role as cross-domain synthesis"
                    )

    # LaTeX table
    latex = generate_latex_table(period_data)
    print("\n--- LaTeX Table ---")
    print(latex)

    # Per-paper summary for reporting
    per_paper = []
    for pr in paper_results:
        total = pr["retrieved_count"]
        cross_count = 0
        for cit in pr["citations"]:
            cp = cit.get("citingPaper", cit)
            _, is_cross = classify_citation(cp, pr["seed_domain"])
            if is_cross:
                cross_count += 1
        per_paper.append({
            "label": pr["label"],
            "domain": pr["seed_domain"],
            "total_retrieved": total,
            "total_cited": pr.get("total_citation_count", total),
            "cross_domain": cross_count,
        })

    # Save results
    results = {
        "seed_papers_analyzed": len(paper_results),
        "per_paper": per_paper,
        "periods": {label: period_data.get(label, {}) for _, _, label in PERIODS},
        "api_notes": api_notes,
        "latex_table": latex,
    }

    with open(RESULTS_FILE, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to {RESULTS_FILE}")
    print(f"Cache saved to {CACHE_FILE}")
    print(f"Seed papers analyzed: {len(paper_results)}/{len(SEED_PAPERS)}")
    print(f"API notes: {len(api_notes)}")
    for note in api_notes:
        print(f"  - {note}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
