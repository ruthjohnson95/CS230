.PHONY: all clean

all : report.pdf

report.pdf : main.tex
	pdflatex $^

clean : *.aux *.log *.out *.pdf 
	rm -rf $^