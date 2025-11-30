# Makefile for building criticality-paper.pdf

# Main target
MAIN = criticality-paper

# Commands
LATEX = pdflatex
BIBTEX = bibtex
RM = rm -f

# Build the PDF (with bibliography)
all: $(MAIN).pdf

# Full build with bibliography
$(MAIN).pdf: $(MAIN).tex $(MAIN).bib
	$(LATEX) $(MAIN)
	$(BIBTEX) $(MAIN)
	$(LATEX) $(MAIN)
	$(LATEX) $(MAIN)

# Quick build without bibliography update
quick: $(MAIN).tex
	$(LATEX) $(MAIN)

# Clean auxiliary files
clean:
	$(RM) $(MAIN).aux $(MAIN).log $(MAIN).bbl $(MAIN).blg $(MAIN).out $(MAIN).toc

# Clean everything including PDF
cleanall: clean
	$(RM) $(MAIN).pdf

# View the PDF (Linux)
view: $(MAIN).pdf
	xdg-open $(MAIN).pdf &

# Help
help:
	@echo "Available targets:"
	@echo "  all      - Build the PDF with bibliography (default)"
	@echo "  quick    - Quick build without updating bibliography"
	@echo "  clean    - Remove auxiliary files"
	@echo "  cleanall - Remove all generated files including PDF"
	@echo "  view     - Open the PDF with default viewer"
	@echo "  help     - Show this help message"

.PHONY: all quick clean cleanall view help
