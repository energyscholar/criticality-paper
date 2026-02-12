# Criticality Paper - LaTeX Build Environment

This directory contains the LaTeX source files for the paper "Convergent Discovery of Critical Phenomena Mathematics Across Disciplines: A Cross-Domain Analysis" by Bruce Stephenson and Robin Macomber.

## arXiv Publication

- **arXiv ID:** [2601.22389](https://arxiv.org/abs/2601.22389)
- **Primary Category:** physics.soc-ph
- **Cross-list Groups:** physics, cs, q-bio
- **Announced:** January 2026
- **Author page:** http://arxiv.org/a/stephenson_b_2
- **ORCID (Stephenson):** https://orcid.org/0009-0005-6842-6686
- **arXiv version:** v2 live as of 2 Feb 2026
- **v1 submitted:** 29 Jan 2026 (16kb)
- **v2 posted:** 2 Feb 2026 (22kb)
- **Categories:** physics.soc-ph, cond-mat.stat-mech
- **MSC class:** 82B26, 82B27
- **License:** CC BY 4.0
- **Pages:** 17, no figures, plain-language summary in Appendix B

## Files

- `Stephenson_CrossDomainCriticality_2026.tex` - Main LaTeX source file
- `Stephenson_CrossDomainCriticality_2026.bib` - BibTeX bibliography file
- `Makefile` - Build automation

## Prerequisites

You need a LaTeX distribution installed. On Ubuntu/Debian:

```bash
sudo apt-get update
sudo apt-get install -y texlive-latex-base texlive-latex-extra texlive-fonts-recommended texlive-bibtex-extra texlive-science
```

## Building the PDF

### Using Make (recommended)

```bash
# Full build with bibliography
make

# Quick build (no bibliography update)
make quick

# Clean auxiliary files
make clean

# Clean everything including PDF
make cleanall

# View PDF after building
make view
```

### Manual build

```bash
# Full build with bibliography
pdflatex criticality-paper
bibtex criticality-paper
pdflatex criticality-paper
pdflatex criticality-paper

# Quick build without bibliography
pdflatex criticality-paper
```

## Build Process Explained

The full build requires multiple passes:
1. **First pdflatex run**: Generates `.aux` file with citation references
2. **bibtex run**: Processes bibliography from `.bib` file
3. **Second pdflatex run**: Incorporates bibliography references
4. **Third pdflatex run**: Resolves all cross-references and page numbers

## Editing the Paper

The main content is in `criticality-paper.tex`. The file is organized as follows:

- **Preamble** (lines 1-30): Document class, packages, and formatting
- **Title/Authors** (lines 32-48): Paper metadata
- **Abstract** (lines 52-60): Paper summary
- **Sections**: Introduction, Cross-Domain Discoveries, Mathematical Equivalence, etc.
- **Appendices**: QRR validation test and plain language explanation

### TODO Comments

The source preserves TODO placeholders for sections that need completion:
- Search for `\todo{` to find all TODO items
- These appear as red text in the compiled PDF
- Example: `\todo{[Robin]: Add 1-2 sentences about...}`

### Bibliography Management

References are stored in `criticality-paper.bib` using BibTeX format. To add a new reference:

1. Add entry to `.bib` file with a unique cite key
2. Cite in text using `\cite{citekey}`
3. Rebuild with `make` to update bibliography

## Common Issues

### Missing packages
If you get errors about missing LaTeX packages, install them:
```bash
sudo apt-get install texlive-full  # Comprehensive (large download)
```

### Bibliography not updating
After modifying `.bib` file, run full build:
```bash
make cleanall && make
```

### Font warnings
Font warnings are usually safe to ignore. If you want to eliminate them:
```bash
sudo apt-get install texlive-fonts-extra
```

## Output

Successfully building produces:
- `criticality-paper.pdf` - The compiled paper
- Various auxiliary files (`.aux`, `.log`, `.bbl`, `.blg`, `.out`)

## Comparing with Original

To verify the build matches the original:
```bash
# View both PDFs side by side
evince criticality-paper.pdf FreeTheMath-QRR-PrePub.pdf &
```

## Getting Help

Run `make help` to see available build targets:
```bash
make help
```

## License

This paper discusses public domain mathematical knowledge. See the paper for details on knowledge accessibility and intellectual property implications.

## Contact

For questions about this work:
- Bruce Stephenson: energyscholar@gmail.com
- Robin Macomber: robin@macomber.com
