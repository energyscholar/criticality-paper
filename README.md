# Criticality Paper - LaTeX Build Environment

This directory contains the LaTeX source files for the paper "Convergent Discovery of Critical Phenomena Mathematics Across Disciplines: A Cross-Domain Analysis" by Bruce Stephenson and Robin Macomber.

## Files

- `criticality-paper.tex` - Main LaTeX source file
- `criticality-paper.bib` - BibTeX bibliography file
- `Makefile` - Build automation
- `FreeTheMath-QRR-PrePub.pdf` - Original PDF (preserved for reference)

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
