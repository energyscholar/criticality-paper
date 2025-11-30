#!/bin/bash
# Simple build script for criticality-paper.pdf

set -e  # Exit on error

echo "Building criticality-paper.pdf..."
echo ""

echo "Step 1/4: First LaTeX pass..."
pdflatex -interaction=nonstopmode criticality-paper.tex

echo ""
echo "Step 2/4: Processing bibliography..."
bibtex criticality-paper

echo ""
echo "Step 3/4: Second LaTeX pass..."
pdflatex -interaction=nonstopmode criticality-paper.tex

echo ""
echo "Step 4/4: Final LaTeX pass..."
pdflatex -interaction=nonstopmode criticality-paper.tex

echo ""
echo "Build complete! Output: criticality-paper.pdf"
echo ""
echo "To view: xdg-open criticality-paper.pdf"
