MAIN = main

.PHONY: all clean

all:
	latexmk -pdf $(MAIN).tex

clean:
	latexmk -C $(MAIN).tex
	rm -f *.bbl *.run.xml *.synctex.gz
