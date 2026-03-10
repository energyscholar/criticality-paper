# Citation Network Analysis

Supporting analysis for: *Cross-Domain Criticality: Universal Patterns from Physics to Finance*
(Stephenson 2026, submitted to FACETS)

## Method

Quantify cross-domain citation flow among foundational criticality papers using
Semantic Scholar API data. Tests the paper's central thesis: that criticality
concepts were independently rediscovered across domains rather than transferred.

**Null model:** Expected cross-domain rate = 1 − HHI, where HHI is the
Herfindahl–Hirschman index of domain concentration among citing papers.
If observed cross-domain rate < expected, citations are more domain-siloed
than chance; if higher, ideas are flowing across boundaries.

## Pipeline

```
fetch_citations.py  →  data/raw/citations_*.json
classify_domains.py →  data/processed/{classified,per_paper,period}_*.json
build_matrix.py     →  figures/*.tex, figures/domain_flow.csv
```

Run in order. Each script is standalone (stdlib + json, no external deps).

`import_legacy.py` is a one-time migration script that imported 10 seed papers
from the v1 `citation_cache.json` (January 2026 fetch). Those 10 papers do not
need re-fetching unless `--refresh` is passed to `fetch_citations.py`.

## Seed Papers

15 foundational papers across 6 domains (Physics, Biomedical, Biology,
Engineering, Finance, CS/ML). Defined in `domain_mapping.json`.

| # | Paper | Domain | Source |
|---|-------|--------|--------|
| 1 | Bak et al. 1987 | Physics | v1 import |
| 2 | Peng et al. 1994 (DFA) | Biomedical | v1 import |
| 3 | Crucitti et al. 2004 | Engineering | v1 import |
| 4 | Dobson et al. 2007 | Engineering | v1 import |
| 5 | Mantegna & Stanley 1995 | Finance | v1 import |
| 6 | Saxe et al. 2013 | CS/ML | v1 import |
| 7 | Kauffman 1993 | Biology | v1 import |
| 8 | Jaeger 2001 | CS/ML | v1 import |
| 9 | Sornette 2004 | Physics | v1 import |
| 10 | Peters 1994 | Finance | v1 import |
| 11 | Scheffer et al. 2009 | Biology | v2 fetch |
| 12 | Lenton et al. 2008 | Physics | v2 fetch |
| 13 | Beggs & Plenz 2003 | Biomedical | v2 fetch |
| 14 | Mora & Bialek 2011 | Biology | v2 fetch |
| 15 | Bury et al. 2021 | CS/ML | v2 fetch |

## Data

- `data/raw/` — API responses (gitignored, ~3MB per run, regenerable)
- `data/processed/` — classified results (tracked)
- `figures/` — LaTeX table fragments and CSV for visualization

## Regeneration

To regenerate from scratch (no cache):
```
python fetch_citations.py --refresh   # ~30 min, all 15 papers
python classify_domains.py
python build_matrix.py
```

To fetch only new/missing papers (uses existing cache):
```
python fetch_citations.py             # skips cached, ~15 min for 5 new
```

## Requirements

Python 3.8+. No external packages (uses urllib, json, math).
Rate limit: 3.2s between API calls (Semantic Scholar public tier).
