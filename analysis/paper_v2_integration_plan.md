# Plan: Integrating New Domain Findings into Paper v2 (red-team revised)

## Context

Citation analysis expanded from 10 → 20 seed papers across 13 domains.
Key finding: S2 field classification only works cleanly for 6 broad domains
(Physics, Biomedical, Biology, Engineering, Finance, CS/ML). The 7 new
"domain" seeds (seismology, materials, linguistics, conflict, urban,
hydrology, epidemiology) are classified by S2 into those same 6 categories.

This means: quantitative cross-domain analysis should use the 6 broad
domains. The new domains add narrative depth and historical evidence.

## What to Add to Paper v2

### 1. Section 2 (Background): Expand the historical scope

Add a paragraph on the "1940s trio" — three scientists in three unrelated
fields independently discovered power laws in the same decade:
- Gutenberg & Richter 1944 (seismology)
- Richardson 1948 (conflict/warfare)
- Zipf 1949 (linguistics)

None cited each other. This is the paper's thesis distilled to a historical
vignette. 2-3 sentences maximum.

### 2. Section 2.2: Add brief domain mentions

The paper already covers Physics, Biomedical, Finance, Engineering, CS/ML,
Climate, Biology. Add one-sentence mentions of:
- **Seismology:** Gutenberg-Richter law (1944) is arguably the cleanest
  natural power law, predating SOC by 43 years.
- **Materials science:** Barkhausen noise (1919) predates SOC by 68 years.
  Sethna's "crackling noise" (2001) unified magnets, earthquakes, and
  fracture under one universality class.
- **Linguistics:** Zipf's law (1949) as power-law word frequency; Ferrer i
  Cancho showed language sits at a phase transition between order and chaos.
- **Urban science:** Bettencourt-West (2007) universal city scaling exponents.

### 3. Section 3 (Citation analysis): Keep 6-domain quantitative framework

The quantitative analysis (cross-citation matrix, chi-squared, sensitivity)
should remain on the 6 S2-resolvable domains. Footnote explains why:
"Semantic Scholar field classifications resolve to approximately six broad
domains; finer-grained distinctions (e.g., seismology within physics)
require manual coding beyond the scope of this automated analysis."

### 4. Section 3: Add the expanded dataset summary

Update citation counts: 20 seed papers, 33,193 unique citing papers,
13 named domains. The cross-citation matrix can be presented at the
6-domain level. Mention the per-paper cross-domain rates for new seeds
as supporting evidence of breadth.

### 5. The Hurst-Mandelbrot pipeline (Section 2 or new subsection)

Trace the chain: Hurst (hydrology, 1951) → Mandelbrot (math, 1968) →
Peng (DFA/physiology, 1994) → finance applications. This is the most
complete cross-domain transfer story in the paper — a concept born in
hydrology, formalized in mathematics, applied in biomedicine, adopted
in finance. Each community partially unaware of the others.

### 6. New references to add to .bib

- gutenberg_richter1944 (or cite via Bak & Tang 1989)
- zipf1949 (book: Human Behavior and Principle of Least Effort)
- ferrer_cancho2003 (PNAS: Least effort and scaling in language)
- sethna2001 (Nature: Crackling noise)
- richardson1960 (Statistics of Deadly Quarrels)
- bettencourt2007 (PNAS: Growth, innovation, scaling in cities)
- barkhausen1919 (if available; otherwise cite Sethna's review)

### 7. What NOT to add

- Do not add a separate "seismology section" or "linguistics section" —
  the paper is already long enough. Brief mentions integrate naturally
  into the existing narrative structure.
- Do not change the quantitative analysis framework to 13 domains —
  S2 can't support it. Acknowledge the limitation honestly.
- Do not add the epidemiology or social physics domains — these borrow
  explicitly from physics (weaker independence case).
- Richardson's war data is narratively useful but has no S2 citation
  data to support quantitative claims.

## Implementation Approach

This is a surgical expansion: ~500 words of new text, ~7 new references,
no structural changes to the paper. The narrative becomes richer without
changing the analytical framework or conclusions.

Key message strengthened: "Not six domains but at least thirteen — and
the earliest independent discovery (Barkhausen, 1919) predates formal
criticality theory by half a century."
