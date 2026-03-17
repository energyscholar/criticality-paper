# arXiv v3 Submission — Pre-Flight Checklist

**Paper:** 2601.22389
**Date prepared:** 2026-03-16
**Status:** READY TO SUBMIT

---

## FILES TO UPLOAD

Upload TWO files individually (do NOT use tar.gz — it fails on Check Files):

```
/home/bruce/software/criticality-paper/Stephenson_CrossDomainCriticality_2026.tex
/home/bruce/software/criticality-paper/Stephenson_CrossDomainCriticality_2026.bbl
```

Use .bbl (pre-compiled bibliography), NOT .bib. The .bbl is self-contained and
skips BibTeX — more reliable on arXiv.

Supplementary PDF is NOT uploaded to arXiv (tar.gz with anc/ directory fails
repeatedly). The paper text already references supplementary material; we will
provide it to FACETS directly. The arXiv Comments field notes its existence.

---

## METADATA — copy-paste ready

### Title
```
Convergent Discovery of Critical Phenomena Mathematics Across Disciplines
```

### Authors
```
Bruce Stephenson, Robin Macomber
```

### Abstract
```
Techniques for detecting critical phenomena---phase transitions where correlation length diverges and small perturbations have large effects---have been developed across multiple fields over nine decades. We survey between six and twelve disciplines (depending on classification criteria) where researchers derived functionally corresponding measures of correlation scaling, with little documented awareness of each other's work. The physicist's correlation length $\xi$, the cardiologist's DFA scaling exponent $\alpha$, the financial analyst's Hurst exponent $H$, and the machine learning engineer's spectral radius $\chi$ all detect critical signatures under different notation.

We classify each surveyed domain as independent derivation, domain transfer, or empirical precursor, and present citation network evidence that cross-domain citations remained significantly below random-mixing expectations (under a simple null model of domain mixing) during the formative period (1987--2010). The framework that motivated this investigation---derived from distributed systems engineering and presented in the Supplementary Material---is excluded from the survey count given the authors' dual role.

Building on prior syntheses---notably Sornette's 2004 textbook---this paper contributes a taxonomy of discovery types and quantitative documentation of the convergence pattern.
```

### Comments
```
26 pages (double-spaced), 4 tables, supplementary material. v3: FACETS-compliant formatting, Genesis moved to supplementary material, pitchfork bifurcation correction, expanded climate/thermohaline section with Mysak lineage, citation sensitivity analysis, CRediT author contributions, author ORCIDs. Prepared for submission to FACETS (Canadian Science Publishing)
```

### Report number
```
(leave blank)
```

### Journal reference
```
(leave blank)
```

### External DOI
```
(leave blank)
```

### ACM class
```
(leave blank)
```

### MSC class
```
82B26; 82B27
```

### Primary Category
```
physics.soc-ph
```

---

## arXiv UPLOAD STEPS

1. Go to https://arxiv.org/user/ → find 2601.22389 → click **Replace**
2. Delete All existing files if any are listed from a previous attempt
3. Upload the .tex file, then upload the .bbl file (2 separate uploads)
4. Click **Check Files** — should show both files, no errors
5. Proceed to **Process** — let arXiv compile the .tex + .bib into PDF
6. Verify compiled PDF renders correctly (26 pages, 4 tables)
7. **Metadata**: paste fields from above (title, authors, abstract, comments, MSC, category)
8. **Preview**: verify title, abstract, author list, check compiled PDF
9. **Submit**

**Expected processing time:** ~2 days before v3 goes live on arxiv.org.

---

## SAME DAY — after arXiv submission confirmed

- [ ] Send Mysak thank-you email (draft: mysak-thankyou-draft.md)
- [ ] Send FACETS pre-submission inquiry (draft: FACETS-outreach-drafts.md Section 1)
      — update arXiv link in inquiry to note "v3 submitted, processing"
- [ ] Send PDF to Robin for review
- [ ] Notify Robin: his ORCID (0009-0002-2843-8568) is in the paper

## AFTER arXiv v3 goes live (~2 days)

- [ ] Verify v3 displays correctly on arxiv.org
- [ ] Verify compiled PDF matches local build (26 pages, 4 tables)
- [ ] Confirm FACETS inquiry sent (or send now if held for v3)
- [ ] Verify referee emails ready: Scheffer (marten.scheffer@wur.nl), Lenton (T.M.Lenton@exeter.ac.uk)

---

## BUILD VERIFICATION (2026-03-16)

- Compilation: **clean, 0 warnings, 0 undefined references**
- Pages: **26** (double-spaced, line-numbered)
- Tables: **4** (classification, citations, equivalence, timeline)
- Figures: **0**
- References: **32 citations, 28 bib entries**
- Supplementary: **3 pages** (operator definitions, Ising test, Genesis)
- Abstract: **176 words** (limit: 200) ✓
- PLS: **286 words** (range: 250-500) ✓
- PLS title: **86 characters** (range: 80-95) ✓
- Key words: **6** (limit: 6) ✓

## FACETS COMPLIANCE SUMMARY

| Requirement | Status |
|------------|--------|
| No appendices | ✓ Genesis in supplementary |
| Corresponding author on title page | ✓ Bruce, footnote |
| Author addresses (city/state/country) | ✓ Albany OR / Lompoc CA |
| ORCIDs | ✓ Both authors |
| CRediT contributions | ✓ Footnote |
| Key words ≤ 6 | ✓ |
| Abstract ≤ 200 words | ✓ 176 |
| PLS 250-500 words + title 80-95 chars | ✓ 286 / 86 |
| Harvard citation style (Author Year) | ✓ natbib, no comma |
| Double-spaced + line numbers | ✓ |
| Funding statement | ✓ |
| COI disclosure | ✓ |
| AI disclosure | ✓ |
| Data availability | ✓ |
| Supplementary material referenced in text | ✓ |
