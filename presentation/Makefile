# Compile with: make
# Requires XeLaTeX, Metropolis, Fira Sans / Fira Mono, and PGFPlots.

.PHONY: all clean

TEX := andres_herencia.tex
PDF := andres_herencia.pdf

all: $(PDF)

$(PDF): $(TEX)
	latexmk -xelatex -interaction=nonstopmode -halt-on-error $(TEX)

clean:
	latexmk -C
