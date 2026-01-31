# Citation Analysis Results — For Auditor Review

**Generated:** 2026-01-30
**Script:** `citation_analysis.py`
**Data cache:** `citation_cache.json`
**Full JSON:** `citation_results.json`

---

## Summary

10/10 seed papers retrieved from Semantic Scholar API. Cross-domain citation rates are **significantly below** the null model in all three periods (p < 0.0001), and the rate **increases over time** — both supporting the independent discovery thesis.

## Raw Results

| Period | N | Observed cross-domain | Expected (null) | chi-squared | p |
|--------|---|----------------------|-----------------|-------------|---|
| 1987-2000 | 287 | 42.9% | 67.9% | 82.6 | <0.0001 |
| 2001-2010 | 1,500 | 50.7% | 76.4% | 551.2 | <0.0001 |
| 2011-2025 | 10,664 | 51.8% | 64.1% | 708.1 | <0.0001 |

## Domain Distribution by Period

### 1987-2000 (N=287)
- Physics: 113 (39.4%)
- Finance: 110 (38.3%)
- CS/ML: 33 (11.5%)
- Biomedical: 21 (7.3%)
- Engineering: 6 (2.1%)
- Other/Social: 4 (1.4%)

### 2001-2010 (N=1,500)
- Physics: 457 (30.5%)
- Finance: 411 (27.4%)
- CS/ML: 353 (23.5%)
- Biomedical: 120 (8.0%)
- Engineering: 113 (7.5%)
- Other/Social: 46 (3.1%)

### 2011-2025 (N=10,664)
- CS/ML: 5,943 (55.7%)
- Biomedical: 1,538 (14.4%)
- Physics: 1,286 (12.1%)
- Finance: 1,075 (10.1%)
- Engineering: 488 (4.6%)
- Other/Social: 334 (3.1%)

## Counter-Evidence

- **Sornette 2004 early cross-domain rate:** 25.6% (34/133 citations in 2001-2010)
  - This is LOWER than the aggregate, not higher — Sornette's synthesis was primarily cited within Physics, not cross-domain. Interesting and somewhat unexpected.

## Sampling Limitations

- Peng et al. 1994: 4,550 total citations, sampled first 2,000
- Kauffman 1993: 8,091 total citations, sampled first 2,000
- Jaeger 2001: 3,021 total citations, sampled first 2,000
- All other papers: complete citation data retrieved

## Interpretation Issues for Auditor

1. **Null model choice:** The Herfindahl-based null (1 - sum of p_i^2) assumes random mixing. The significant departure in ALL periods confirms domain clustering — but this is a weak test since academic citations are always domain-clustered to some degree. The more informative signal is the **trend**: 42.9% → 50.7% → 51.8% increasing cross-domain rate.

2. **CS/ML dominance in 2011-2025:** Saxe (2013) and Jaeger (2001) drive the late-period sample heavily toward CS/ML (55.7% of all citations). This may inflate the Herfindahl concentration and depress the expected rate. The Auditor should consider whether period-specific or paper-specific analysis is more appropriate.

3. **Absolute vs relative rates:** Observed cross-domain rates of 43-52% are actually quite high in absolute terms. The "below expected" finding depends entirely on the null model. An alternative framing: cross-domain citation increased from 43% to 52% over three decades, consistent with growing integration.

4. **Sornette as counter-evidence:** Sornette 2004's LOW cross-domain rate (25.6%) is surprising given it's a cross-domain synthesis textbook. This may mean it was primarily adopted within physics as a reference work, not used as a bridge by other domains. This complicates the expected counter-evidence narrative (T6.8).

5. **Missing seed papers:** The analysis covers 10 papers but not Onsager (1944) or Greenshields (1935) — both predate reliable Semantic Scholar coverage. Also missing: Kerner (2004). Adding these might change the picture.

## Auditor Decision Points

- **How to frame the null model:** Standard Herfindahl, or propose alternative?
- **How to handle the trend:** Focus on increasing rate over time, or on below-expected in each period?
- **How to report Sornette counter-evidence:** Low cross-domain rate for a synthesis work is interesting but doesn't fit the expected T6.8 narrative of "high early cross-domain rate"
- **Whether to add more seed papers** to improve coverage
- **Whether to normalize** for CS/ML dominance in the late period
