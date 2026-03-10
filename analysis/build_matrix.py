#!/usr/bin/env python3
"""
Build cross-citation matrix and generate figures/tables.

Reads: data/processed/classified_citations.json
       data/processed/per_paper_summary.json
       data/processed/period_analysis.json
       data/raw/paper_metadata.json

Outputs: figures/cross_domain_matrix.tex    (LaTeX table)
         figures/cross_domain_trends.tex    (LaTeX table, time-resolved)
         figures/domain_flow.csv            (for external visualization)
         data/processed/cross_matrix.json   (domain x domain counts)

Usage:
    python build_matrix.py
"""

import json
import os
from collections import defaultdict

SCRIPT_DIR = os.path.dirname(__file__)
RAW_DIR = os.path.join(SCRIPT_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(SCRIPT_DIR, "data", "processed")
FIGURES_DIR = os.path.join(SCRIPT_DIR, "figures")

PERIODS = [
    (1987, 1995, "1987--1995"),
    (1996, 2005, "1996--2005"),
    (2006, 2015, "2006--2015"),
    (2016, 2026, "2016--2026"),
]

DOMAIN_ORDER = ["Physics", "Biomedical", "Biology", "Engineering", "Finance", "CS/ML"]


def main():
    os.makedirs(FIGURES_DIR, exist_ok=True)

    with open(os.path.join(RAW_DIR, "paper_metadata.json")) as f:
        metadata = json.load(f)
    with open(os.path.join(PROCESSED_DIR, "classified_citations.json")) as f:
        all_classified = json.load(f)
    with open(os.path.join(PROCESSED_DIR, "period_analysis.json")) as f:
        period_analysis = json.load(f)

    # --- Cross-citation matrix: seed_domain → citing_domain ---
    matrix = defaultdict(lambda: defaultdict(int))
    for label, classified in all_classified.items():
        seed_domain = metadata[label]["seed_domain"]
        for cit in classified:
            if cit["primary_domain"] != "Unknown":
                matrix[seed_domain][cit["primary_domain"]] += 1

    # Save matrix
    with open(os.path.join(PROCESSED_DIR, "cross_matrix.json"), "w") as f:
        json.dump({k: dict(v) for k, v in matrix.items()}, f, indent=2)

    # --- LaTeX: cross-domain matrix ---
    present_domains = [d for d in DOMAIN_ORDER if d in matrix or
                       any(d in v for v in matrix.values())]

    lines = [
        r"\begin{table}[h]",
        r"\centering",
        r"\caption{Cross-citation matrix: seed domain (rows) $\to$ citing domain (columns)}",
        r"\label{tab:cross-matrix}",
        r"\begin{tabular}{l" + "r" * len(present_domains) + "}",
        r"\toprule",
        r"\textbf{Seed domain} & " + " & ".join(
            [r"\textbf{" + d + "}" for d in present_domains]
        ) + r" \\",
        r"\midrule",
    ]
    for seed_d in present_domains:
        if seed_d not in matrix:
            continue
        vals = [str(matrix[seed_d].get(d, 0)) for d in present_domains]
        lines.append(f"{seed_d} & " + " & ".join(vals) + r" \\")
    lines.extend([r"\bottomrule", r"\end{tabular}", r"\end{table}"])

    with open(os.path.join(FIGURES_DIR, "cross_domain_matrix.tex"), "w") as f:
        f.write("\n".join(lines))

    # --- LaTeX: time-resolved trends ---
    lines = [
        r"\begin{table}[h]",
        r"\centering",
        r"\caption{Cross-domain citation rates by period (Semantic Scholar API)}",
        r"\label{tab:citation-trends}",
        r"\begin{tabular}{lrrrrl}",
        r"\toprule",
        r"\textbf{Period} & \textbf{N} & \textbf{Obs.\ cross} & \textbf{Expected} & $\chi^2$ & $p$ \\",
        r"\midrule",
    ]
    for _, _, label in PERIODS:
        d = period_analysis.get(label, {})
        n = d.get("total", 0)
        obs = f"{d.get('obs_rate', 0):.1%}"
        exp = f"{d.get('exp_rate', 0):.1%}"
        chi2 = f"{d.get('chi2', 0):.1f}"
        p = d.get("p_value", 1.0)
        p_str = f"{p:.4f}" if p >= 0.0001 else r"$<$0.0001"
        lines.append(f"{label} & {n} & {obs} & {exp} & {chi2} & {p_str} \\\\")
    lines.extend([r"\bottomrule", r"\end{tabular}", r"\end{table}"])

    with open(os.path.join(FIGURES_DIR, "cross_domain_trends.tex"), "w") as f:
        f.write("\n".join(lines))

    # --- CSV: domain flow (for Sankey/heatmap in external tools) ---
    with open(os.path.join(FIGURES_DIR, "domain_flow.csv"), "w") as f:
        f.write("seed_domain,citing_domain,count\n")
        for seed_d in sorted(matrix.keys()):
            for cite_d in sorted(matrix[seed_d].keys()):
                f.write(f"{seed_d},{cite_d},{matrix[seed_d][cite_d]}\n")

    print("Generated:")
    print(f"  {FIGURES_DIR}/cross_domain_matrix.tex")
    print(f"  {FIGURES_DIR}/cross_domain_trends.tex")
    print(f"  {FIGURES_DIR}/domain_flow.csv")
    print(f"  {PROCESSED_DIR}/cross_matrix.json")
    return 0


if __name__ == "__main__":
    exit(main())
