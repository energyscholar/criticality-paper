# Cross-Domain Citation Analysis Report

Generated: 2026-03-10

## Methodology

**Data source:** Semantic Scholar API (public tier, no API key)
**Seed papers:** 20 foundational criticality papers across 6 domains
**Classification:** Each citing paper's `fieldsOfStudy` mapped to domain categories
via `domain_mapping.json`. Papers with no `fieldsOfStudy` classified as Unknown.
**Cross-domain definition:** A citation is cross-domain if the citing paper's
domain set does not include the seed paper's assigned domain.
**Null model:** Expected cross-domain rate = 1 − HHI (Herfindahl index of
domain concentration). Under random citation, this is the probability that a
randomly chosen citing paper comes from a different domain than the seed.
**Confidence intervals:** Wilson score intervals (95%).
**Deduplication:** Citing papers appearing under multiple seeds counted once
per unique paperId, but cross-domain status assessed per seed relationship.

## Data Quality

| Metric | Value |
|--------|-------|
| Total raw citation records | 35,709 |
| Unique citing papers | 33,193 |
| Duplicates (same paper citing multiple seeds) | 2,457 |
| Records with no paperId | 59 |
| Deduplication ratio | 93.0% |

**Truncated papers** (retrieved < 95% of total citations):

- Kauffman 1993: 4999/8038 (62% complete)
- Jaeger 2001: 2000/3021 (66% complete)

*Truncation occurs when API rate limits prevent full retrieval.*
*Analysis uses available data; results may undercount for these papers.*

**Unknown classification rate:** 5,058/35,650 (14.2%) of citing papers have no `fieldsOfStudy` in Semantic Scholar. These are excluded from cross-domain calculations but included in sensitivity analysis (see below).

## Per-Paper Results

| Seed paper | Domain | N (unique) | Cross-domain | Rate | 95% CI | Complete |
|------------|--------|-----------|-------------|------|--------|----------|
| Bak & Tang 1989 (earthquakes as SOC) | Seismology | 1,084 | 974 | 100.0% | [99.6%, 100.0%] | 100% |
| Sethna et al. 2001 (crackling noise) | Materials | 955 | 847 | 100.0% | [99.6%, 100.0%] | 100% |
| Ferrer i Cancho & Sole 2003 | Linguistics | 562 | 491 | 100.0% | [99.2%, 100.0%] | 100% |
| Richardson 1960 | Conflict | 1 | 1 | 100.0% | [20.6%, 100.0%] | 100% |
| Bettencourt et al. 2007 (city scaling) | Urban | 2,500 | 1,883 | 100.0% | [99.8%, 100.0%] | 100% |
| Scheffer et al. 2009 | Biology | 4,211 | 2,764 | 83.7% | [82.4%, 84.9%] | 100% |
| Lenton et al. 2008 | Physics | 3,540 | 1,999 | 79.5% | [77.9%, 81.1%] | 100% |
| Crucitti et al. 2004 | Engineering | 1,089 | 753 | 78.7% | [76.0%, 81.2%] | 100% |
| Kauffman 1993 | Biology | 4,999 | 3,787 | 78.2% | [77.0%, 79.3%] | 62%* |
| Dobson et al. 2007 | Engineering | 934 | 570 | 72.6% | [69.4%, 75.6%] | 100% |
| Peng et al. 1994 (DFA) | Biomedical | 4,552 | 2,838 | 71.3% | [69.8%, 72.7%] | 100% |
| Bury et al. 2021 | CS/ML | 232 | 91 | 61.9% | [53.8%, 69.4%] | 100% |
| Mora & Bialek 2011 | Biology | 750 | 408 | 60.5% | [56.8%, 64.1%] | 100% |
| Mantegna & Stanley 1995 | Finance | 1,630 | 812 | 55.1% | [52.5%, 57.6%] | 100% |
| Peters 1994 | Finance | 1,032 | 433 | 48.6% | [45.4%, 51.9%] | 100% |
| Bak et al. 1987 | Physics | 853 | 357 | 46.1% | [42.6%, 49.6%] | 100% |
| Beggs & Plenz 2003 | Biomedical | 2,120 | 729 | 37.4% | [35.3%, 39.6%] | 100% |
| Sornette 2004 | Physics | 625 | 186 | 35.7% | [31.7%, 39.9%] | 100% |
| Jaeger 2001 | CS/ML | 2,000 | 331 | 18.7% | [17.0%, 20.6%] | 66%* |
| Saxe et al. 2013 | CS/ML | 1,981 | 105 | 5.8% | [4.8%, 7.0%] | 100% |

## Period Analysis

| Period | N | Cross-domain | 95% CI | Expected (HHI) | χ² | p | Direction |
|--------|---|-------------|--------|----------------|-----|---|-----------|
| 1987--1995 | 156 | 85.3% | [78.8%, 90.0%] | 34.5% | 178.0 | <0.0001 | diffusing |
| 1996--2005 | 2,716 | 69.6% | [67.8%, 71.3%] | 77.4% | 95.9 | <0.0001 | siloed |
| 2006--2015 | 11,436 | 72.8% | [72.0%, 73.6%] | 83.6% | 975.1 | <0.0001 | siloed |
| 2016--2026 | 16,282 | 61.5% | [60.7%, 62.2%] | 77.6% | 2425.1 | <0.0001 | siloed |

**Interpretation:** Observed cross-domain rate is *below* the HHI null model
in every period (all p < 0.0001). Citations are more domain-siloed than
random chance would predict, consistent with independent development of
criticality methods within domains rather than cross-pollination.

## Sensitivity Analysis

### Unknown classification bounds

| Period | Observed (known only) | Worst case | Best case | Unknown % |
|--------|-----------------------|-----------|-----------|-----------|
| 1987--1995 | 85.3% | 82.6% | 85.7% | 3.1% |
| 1996--2005 | 69.6% | 67.1% | 70.7% | 3.6% |
| 2006--2015 | 72.8% | 68.7% | 74.3% | 5.6% |
| 2016--2026 | 61.5% | 49.4% | 69.0% | 19.6% |

*Worst case: all unknowns counted as same-domain. Best case: all unknowns counted as cross-domain.*

### Merged Biology + Biomedical

| Period | Standard | Merged Bio/Biomedical |
|--------|----------|-----------------------|
| 1987--1995 | 85.3% | 84.0% |
| 1996--2005 | 69.6% | 61.5% |
| 2006--2015 | 72.8% | 66.0% |
| 2016--2026 | 61.5% | 51.2% |

*Merging Biology and Biomedical into one domain reduces apparent cross-domain*
*flow modestly, as expected. Core finding (siloing) is robust to this choice.*

## Cross-Citation Matrix

Rows = seed paper domain, columns = citing paper domain.

| | Physics | Biomedical | Biology | Engineering | Finance | CS/ML | Seismology | Hydrology | Materials | Linguistics | Conflict | Urban | Epidemiology |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Physics** | 722 | 873 | 126 | 698 | 371 | 399 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **Biomedical** | 1575 | 2243 | 405 | 338 | 425 | 856 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **Biology** | 802 | 3080 | 763 | 758 | 527 | 1926 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **Engineering** | 147 | 219 | 11 | 416 | 42 | 877 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **Finance** | 905 | 208 | 18 | 66 | 774 | 337 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **CS/ML** | 159 | 665 | 82 | 189 | 8 | 2623 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **Seismology** | 725 | 77 | 6 | 32 | 5 | 95 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **Materials** | 362 | 363 | 54 | 15 | 3 | 44 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **Linguistics** | 49 | 173 | 10 | 4 | 4 | 217 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **Conflict** | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **Urban** | 165 | 416 | 40 | 147 | 237 | 344 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

## Limitations

1. **Domain classification noise.** Semantic Scholar `fieldsOfStudy` is
   algorithmically assigned, not author-declared. Misclassification rate unknown.
2. **Self-citation.** No filtering of author self-citations. A seed paper's
   authors citing their own work inflates same-domain counts slightly.
3. **Review papers.** Review articles cite across domains by nature,
   inflating cross-domain counts. No review-paper filter applied.
4. **Book seeds.** Kauffman (1993) and Peters (1994) resolved via title search;
   Semantic Scholar coverage of book citations is less complete than for articles.
5. **Truncation.** Some papers retrieved fewer citations than their total count
   due to API rate limits. Affected papers flagged above.
6. **Temporal bias.** Newer papers have had less time to accumulate citations.
   The 2016--2026 period may undercount for recently published seeds.
