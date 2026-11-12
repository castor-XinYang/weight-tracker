# Build session reports. Usage: make s2 | make s1 | make all | make clean
LATEXMK  ?= latexmk
LMK_OPTS ?= -pdf -interaction=nonstopmode -file-line-error -halt-on-error

.PHONY: all s1 s2 clean open

all: s1 s2

s1:
	cd sessions/s1-2025-07 && $(LATEXMK) $(LMK_OPTS) main.tex && $(LATEXMK) -c main.tex

s2:
	python3 scripts/build.py s2
	cd sessions/s2-2026-11 && $(LATEXMK) $(LMK_OPTS) main.tex && $(LATEXMK) -c main.tex

clean:
	cd sessions/s1-2025-07 && $(LATEXMK) -c main.tex
	cd sessions/s2-2026-11 && $(LATEXMK) -c main.tex
	rm -rf sessions/*/generated

open: s2
	open sessions/s2-2026-11/main.pdf
