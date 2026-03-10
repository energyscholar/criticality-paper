# Cross-Domain Citation Analysis Report

Generated: 2026-03-10

## Methodology

**Data source:** Semantic Scholar API (public tier, no API key)
**Seed papers:** 15 foundational criticality papers across 6 domains
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
| Total raw citation records | 30,592 |
| Unique citing papers | 28,591 |
| Duplicates (same paper citing multiple seeds) | 1,957 |
| Records with no paperId | 44 |
| Deduplication ratio | 93.5% |

**Truncated papers** (retrieved < 95% of total citations):

- Kauffman 1993: 4999/8038 (62% complete)
- Jaeger 2001: 2000/3021 (66% complete)

*Truncation occurs when API rate limits prevent full retrieval.*
*Analysis uses available data; results may undercount for these papers.*

**Unknown classification rate:** 4,152/30,548 (13.6%) of citing papers have no `fieldsOfStudy` in Semantic Scholar. These are excluded from cross-domain calculations but included in sensitivity analysis (see below).

## Per-Paper Results

| Seed paper | Domain | N (unique) | Cross-domain | Rate | 95% CI | Complete |
|------------|--------|-----------|-------------|------|--------|----------|
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
| 1987--1995 | 34 | 32.4% | [19.1%, 49.2%] | 72.7% | 27.8 | <0.0001 | siloed |
| 1996--2005 | 2,281 | 63.8% | [61.8%, 65.7%] | 80.5% | 402.8 | <0.0001 | siloed |
| 2006--2015 | 9,969 | 68.8% | [67.9%, 69.7%] | 84.1% | 1754.8 | <0.0001 | siloed |
| 2016--2026 | 14,110 | 55.5% | [54.7%, 56.4%] | 75.5% | 3049.3 | <0.0001 | siloed |

**Interpretation:** Observed cross-domain rate is *below* the HHI null model
in every period (all p < 0.0001). Citations are more domain-siloed than
random chance would predict, consistent with independent development of
criticality methods within domains rather than cross-pollination.

## Sensitivity Analysis

### Unknown classification bounds

| Period | Observed (known only) | Worst case | Best case | Unknown % |
|--------|-----------------------|-----------|-----------|-----------|
| 1987--1995 | 32.4% | 29.7% | 37.8% | 8.1% |
| 1996--2005 | 63.8% | 61.4% | 65.1% | 3.7% |
| 2006--2015 | 68.8% | 65.1% | 70.5% | 5.3% |
| 2016--2026 | 55.5% | 45.2% | 63.8% | 18.7% |

*Worst case: all unknowns counted as same-domain. Best case: all unknowns counted as cross-domain.*

### Merged Biology + Biomedical

| Period | Standard | Merged Bio/Biomedical |
|--------|----------|-----------------------|
| 1987--1995 | 32.4% | 26.5% |
| 1996--2005 | 63.8% | 54.1% |
| 2006--2015 | 68.8% | 61.0% |
| 2016--2026 | 55.5% | 43.7% |

*Merging Biology and Biomedical into one domain reduces apparent cross-domain*
*flow modestly, as expected. Core finding (siloing) is robust to this choice.*

## Cross-Citation Matrix

Rows = seed paper domain, columns = citing paper domain.

| | Physics | Biomedical | Biology | Engineering | Finance | CS/ML | Seismology | Hydrology | Materials | Linguistics | Conflict | Urban | Epidemiology |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Physics** | 786 | 541 | 209 | 727 | 367 | 559 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **Biomedical** | 1732 | 1290 | 657 | 326 | 425 | 1417 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **Biology** | 924 | 1563 | 1491 | 750 | 517 | 2552 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **Engineering** | 167 | 104 | 13 | 353 | 42 | 1032 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **Finance** | 928 | 143 | 20 | 66 | 774 | 373 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **CS/ML** | 185 | 278 | 129 | 83 | 8 | 3044 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

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
