#!/bin/bash
# Simple build script for Stephenson_CrossDomainCriticality_2026.pdf

set -e  # Exit on error

echo "Building Stephenson_CrossDomainCriticality_2026.pdf..."
echo ""

echo "Step 1/4: First LaTeX pass..."
pdflatex -interaction=nonstopmode Stephenson_CrossDomainCriticality_2026.tex

echo ""
echo "Step 2/4: Processing bibliography..."
bibtex Stephenson_CrossDomainCriticality_2026

echo ""
echo "Step 3/4: Second LaTeX pass..."
pdflatex -interaction=nonstopmode Stephenson_CrossDomainCriticality_2026.tex

echo ""
echo "Step 4/4: Final LaTeX pass..."
pdflatex -interaction=nonstopmode Stephenson_CrossDomainCriticality_2026.tex

echo ""
echo "Build complete! Output: Stephenson_CrossDomainCriticality_2026.pdf"
echo ""
echo "To view: xdg-open Stephenson_CrossDomainCriticality_2026.pdf"
