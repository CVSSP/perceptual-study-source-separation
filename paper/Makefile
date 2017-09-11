make:
	@pdflatex ICASSP
	@biber ICASSP
	pdflatex ICASSP
clean:
	@rm *aux *out *log *blg *bcf *bbl *xml
read:
	@evince ICASSP.pdf&
exportrefs:
	@biber ICASSP.bcf --output_format=bibtex
